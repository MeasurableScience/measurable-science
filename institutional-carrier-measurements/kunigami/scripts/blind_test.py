#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KUNIGAMI (KNG) 64-Hz CDF — fast blind 60-s PLV carrier search.

Direct analogue of the supplied CARISMA fast test:
- all KNG CDF files in current folder
- ONE fixed 60-s window per hourly file: minute 30:00–31:00
- physical pair dH/dt vs dD/dt only
- 64 Hz
- blind scan 1.0–10.0 Hz, step 0.1 Hz
- 0.4-Hz total Butterworth bandwidth
- Hilbert PLV
- per-hour threshold = max(0.30, median(PLV)+2*MAD)
- aggregate score = sum(PLV*10) for passing bins
- same clustering logic as CARISMA
- no expected carrier frequency supplied

Requires:
python3 -m pip install cdflib numpy pandas scipy --break-system-packages
"""

import os, glob, re
import numpy as np
import pandas as pd
import cdflib
from scipy.signal import butter, sosfiltfilt, hilbert, savgol_filter

FS = 64.0
WINDOW_START_SEC = 30 * 60
WINDOW_SECONDS = 60
N_WINDOW = int(FS * WINDOW_SECONDS)

FREQ_MIN = 1.0
FREQ_MAX = 10.0
FREQ_STEP = 0.1
BANDWIDTH = 0.4
FILTER_ORDER = 4
MIN_ABSOLUTE_PLV = 0.30

OUT_PROFILE = "KNG_PLV_60S_PROFILE.csv"
OUT_VOTES = "KNG_PLV_60S_VOTES.csv"
OUT_CARRIERS = "KNG_PLV_60S_CARRIERS.csv"

FILE_RE = re.compile(r"isee_induction_kng_(\d{8})(\d{2})_v\d+\.cdf$", re.I)


def calculate_plv(a, b):
    pa = np.angle(hilbert(a))
    pb = np.angle(hilbert(b))
    return float(np.abs(np.mean(np.exp(1j * (pa - pb)))))


def get_labels(cdf):
    try:
        x = np.asarray(cdf.varget("label_db_dt")).ravel()
        return [z.decode(errors="replace").strip() if isinstance(z, bytes)
                else str(z).strip() for z in x]
    except Exception:
        return []


def read_60s_window(path):
    cdf = cdflib.CDF(path)
    db = np.asarray(cdf.varget("db_dt"))

    if db.ndim != 2:
        raise RuntimeError(f"{path}: db_dt shape {db.shape}, expected 2-D")
    if db.shape[0] <= 16 and db.shape[1] > db.shape[0]:
        db = db.T
    if db.shape[1] < 2:
        raise RuntimeError(f"{path}: fewer than 2 db_dt components")

    labels = get_labels(cdf)

    # Use Epoch to select actual UTC minute 30, rather than assuming record zero.
    epoch = np.asarray(cdf.varget("epoch_db_dt"))
    dt = np.asarray(cdflib.cdfepoch.to_datetime(epoch), dtype="datetime64[us]")

    # Minute and second within each timestamp.
    minute_start = dt.astype("datetime64[m]")
    hour_start = dt.astype("datetime64[h]")
    sec_from_hour = (dt - hour_start).astype("timedelta64[us]").astype(np.int64) / 1e6

    mask = (sec_from_hour >= WINDOW_START_SEC) & (sec_from_hour < WINDOW_START_SEC + WINDOW_SECONDS)
    idx = np.flatnonzero(mask)

    if len(idx) < int(0.95 * N_WINDOW):
        return None, None, labels, len(idx)

    # Exactly first 3840 samples from minute 30.
    idx = idx[:N_WINDOW]
    a = db[idx, 0].astype(np.float64)
    b = db[idx, 1].astype(np.float64)

    good = np.isfinite(a) & np.isfinite(b)
    if np.count_nonzero(good) < int(0.95 * N_WINDOW):
        return None, None, labels, int(np.count_nonzero(good))

    a = a[good]
    b = b[good]

    # Require near-full window; trim to common expected size only when available.
    if len(a) >= N_WINDOW:
        a = a[:N_WINDOW]
        b = b[:N_WINDOW]

    a -= np.mean(a)
    b -= np.mean(b)
    return a, b, labels, len(a)


def make_filter(center):
    half = BANDWIDTH / 2.0
    low, high = center - half, center + half
    if low <= 0 or high >= FS / 2.0:
        return None
    return butter(FILTER_ORDER, [low, high], btype="bandpass", fs=FS, output="sos")


def scan_window(a, b, freqs, filters):
    vals = []
    for sos in filters:
        if sos is None:
            vals.append(np.nan)
            continue
        try:
            af = sosfiltfilt(sos, a)
            bf = sosfiltfilt(sos, b)
            vals.append(calculate_plv(af, bf))
        except Exception:
            vals.append(np.nan)
    return np.asarray(vals, dtype=float)


def robust_threshold(values):
    x = values[np.isfinite(values)]
    if len(x) == 0:
        return np.nan
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    return max(MIN_ABSOLUTE_PLV, med + 2.0 * mad)


def cluster_profile(agg):
    d = agg.sort_values("Frequency_Hz").copy()
    scores = d["Integrated_PLV_Score"].to_numpy(float)
    finite = scores[np.isfinite(scores)]
    if not len(finite):
        return []

    med = np.median(finite)
    mad = np.median(np.abs(finite - med))
    dyn = max(8.0, med + 1.5 * mad)
    smooth = savgol_filter(scores, 5, 2, mode="interp") if len(scores) >= 5 else scores.copy()
    active = smooth >= dyn
    freqs = d["Frequency_Hz"].to_numpy(float)

    groups, cur = [], []
    for i, ok in enumerate(active):
        if not ok:
            if cur:
                groups.append(cur); cur = []
            continue
        if not cur or freqs[i] - freqs[cur[-1]] <= 0.15 + 1e-9:
            cur.append(i)
        else:
            groups.append(cur); cur = [i]
    if cur:
        groups.append(cur)

    rows = []
    for g in groups:
        sub = d.iloc[g]
        peak_i = sub["Integrated_PLV_Score"].idxmax()
        peak = d.loc[peak_i]
        lo, hi = float(sub.Frequency_Hz.min()), float(sub.Frequency_Hz.max())

        gi = int(np.argmax(smooth[g]))
        ai = g[gi]
        peak_sm = smooth[ai]
        left = smooth[max(0, ai-2):ai]
        right = smooth[ai+1:min(len(smooth), ai+3)]
        shoulders = np.concatenate([left, right]) if len(left)+len(right) else np.array([0.0])
        shoulder = float(np.median(shoulders))
        prom = 100.0 * max(0.0, peak_sm-shoulder) / max(abs(shoulder), 1e-12)

        rows.append({
            "Station": "KNG",
            "Start_Hz": lo,
            "End_Hz": hi,
            "Center_Hz": (lo+hi)/2.0,
            "Width_Hz": hi-lo,
            "Peak_Hz": float(peak.Frequency_Hz),
            "Peak_Mean_PLV": float(peak.Mean_Raw_PLV),
            "Peak_Hours_Active": int(peak.Hours_Active),
            "Integrated_PLV_Score": float(sub.Integrated_PLV_Score.sum()),
            "Local_Prominence_pct": prom,
            "Classification": "Sharp Carrier Peak" if prom >= 35.0 else "Phase Coherent Band",
            "Dynamic_Score_Threshold": dyn,
        })
    return rows


def main():
    freqs = np.round(np.arange(FREQ_MIN, FREQ_MAX + FREQ_STEP/2, FREQ_STEP), 10)
    filters = [make_filter(f) for f in freqs]

    files = []
    for path in sorted(glob.glob("*.cdf") + glob.glob("*.CDF")):
        m = FILE_RE.match(os.path.basename(path))
        if m:
            files.append((m.group(1), int(m.group(2)), path))

    if not files:
        raise RuntimeError("No isee_induction_kng_YYYYMMDDHH_vXX.cdf files found.")

    print("================================================")
    print(" KUNIGAMI KNG BLIND 60-S PLV CARRIER SEARCH")
    print("================================================")
    print(f"Files: {len(files)}")
    print(f"fs={FS:g} Hz | scan={FREQ_MIN:.1f}-{FREQ_MAX:.1f} Hz | step={FREQ_STEP:.1f} Hz")
    print(f"bandwidth={BANDWIDTH:.1f} Hz | one window/file = UTC minute 30:00-31:00")
    print("pair=db_dt[0] vs db_dt[1]; labels are printed from CDF")
    print("NO EXPECTED FREQUENCY IS USED")
    print()

    profile_rows, vote_rows = [], []
    printed_labels = False

    for n, (date, hour, path) in enumerate(files, 1):
        a, b, labels, nsamp = read_60s_window(path)

        if not printed_labels:
            print("CDF labels:", labels)
            if len(labels) >= 2:
                print(f"Analysis pair: {labels[0]} vs {labels[1]}")
            print()
            printed_labels = True

        if a is None:
            print(f"  skip {date} {hour:02d}: only {nsamp} usable minute-30 samples")
            continue

        plv = scan_window(a, b, freqs, filters)
        threshold = robust_threshold(plv)
        passed = np.isfinite(plv) & (plv >= threshold)

        for f, v, ok in zip(freqs, plv, passed):
            profile_rows.append({
                "Station": "KNG", "Date": date, "Hour_UTC": hour,
                "Frequency_Hz": f, "PLV": v,
                "Hour_Threshold": threshold, "Passed": int(ok)
            })
            if ok:
                vote_rows.append({
                    "Station": "KNG", "Date": date, "Hour_UTC": hour,
                    "Frequency_Hz": f, "PLV": v, "Score": v*10.0
                })

        best_i = int(np.nanargmax(plv))
        print(f"  [{n:02d}/{len(files):02d}] {date} {hour:02d}:00  "
              f"best={freqs[best_i]:.1f} Hz PLV={plv[best_i]:.4f} thr={threshold:.4f}")

    profile = pd.DataFrame(profile_rows)
    votes = pd.DataFrame(vote_rows)
    profile.to_csv(OUT_PROFILE, index=False)
    votes.to_csv(OUT_VOTES, index=False)

    aggregate_rows = []
    for f in freqs:
        raw = profile[profile.Frequency_Hz == f].PLV.dropna()
        active = votes[votes.Frequency_Hz == f] if not votes.empty else pd.DataFrame()
        aggregate_rows.append({
            "Station": "KNG",
            "Frequency_Hz": f,
            "Hours_Available": int(len(raw)),
            "Hours_Active": int(len(active)),
            "Mean_Raw_PLV": float(raw.mean()) if len(raw) else np.nan,
            "Median_Raw_PLV": float(raw.median()) if len(raw) else np.nan,
            "Mean_Active_PLV": float(active.PLV.mean()) if len(active) else np.nan,
            "Integrated_PLV_Score": float(active.Score.sum()) if len(active) else 0.0,
        })

    agg = pd.DataFrame(aggregate_rows)
    carriers = pd.DataFrame(cluster_profile(agg))
    carriers.to_csv(OUT_CARRIERS, index=False)

    print("\n================================================")
    print(" FROZEN BLIND KUNIGAMI RESULTS")
    print("================================================")
    if carriers.empty:
        print("No aggregate carrier clusters passed.")
    else:
        cols = ["Station","Start_Hz","End_Hz","Center_Hz","Peak_Hz",
                "Peak_Mean_PLV","Peak_Hours_Active","Integrated_PLV_Score","Classification"]
        print(carriers[cols].to_string(index=False))

    print("\nSaved:")
    print(" ", OUT_PROFILE)
    print(" ", OUT_VOTES)
    print(" ", OUT_CARRIERS)
    print("\nFreeze these values before comparing with any other carrier.")


if __name__ == "__main__":
    main()
