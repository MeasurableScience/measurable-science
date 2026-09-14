#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ISTOK (IST) 64-Hz CDF — fast blind 60-s PLV carrier search.

Same fast protocol as the supplied KNG/CARISMA test:
- all IST CDF files in current folder
- ONE fixed 60-s window per UTC hour: minute 30:00–31:00
- db_dt physical channels: dH/dt, dD/dt, dZ/dt
- tests all three physical pairs independently: H-D, H-Z, D-Z
- 64 Hz
- blind scan 1.0–10.0 Hz, step 0.1 Hz
- 0.4-Hz Butterworth bandwidth
- Hilbert PLV
- per-hour/pair threshold = max(0.30, median(PLV)+2*MAD)
- aggregate score = sum(PLV*10) for passing bins
- same clustering logic as KNG/CARISMA
- no expected carrier frequency supplied

Important IST difference:
A single IST CDF may span many UTC hours. Windows are therefore selected from
epoch_db_dt by actual UTC hour, not from the filename.
"""

import os, glob
import numpy as np
import pandas as pd
import cdflib
from scipy.signal import butter, sosfiltfilt, hilbert, savgol_filter

FS = 64.0
WINDOW_MINUTE = 30
WINDOW_SECONDS = 60
N_WINDOW = int(FS * WINDOW_SECONDS)

FREQ_MIN = 1.0
FREQ_MAX = 10.0
FREQ_STEP = 0.001
BANDWIDTH = 0.4
FILTER_ORDER = 4
MIN_ABSOLUTE_PLV = 0.30

OUT_PROFILE = "IST_FAST_PLV_60S_PROFILE.csv"
OUT_VOTES = "IST_FAST_PLV_60S_VOTES.csv"
OUT_CARRIERS = "IST_FAST_PLV_60S_CARRIERS.csv"

PAIRS = [(0, 1, "H-D")]

def calculate_plv(a, b):
    pa = np.angle(hilbert(a))
    pb = np.angle(hilbert(b))
    return float(np.abs(np.mean(np.exp(1j * (pa - pb)))))


def labels(cdf):
    x = np.asarray(cdf.varget("label_db_dt")).ravel()
    return [z.decode(errors="replace").strip() if isinstance(z, bytes)
            else str(z).strip() for z in x]


def make_filter(center):
    half = BANDWIDTH / 2.0
    low, high = center - half, center + half
    if low <= 0 or high >= FS / 2:
        return None
    return butter(FILTER_ORDER, [low, high], btype="bandpass",
                  fs=FS, output="sos")


def scan_window(a, b, filters):
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
    if not len(x):
        return np.nan
    med = np.median(x)
    mad = np.median(np.abs(x - med))
    return max(MIN_ABSOLUTE_PLV, med + 2.0 * mad)


def load_ist(path):
    cdf = cdflib.CDF(path)
    db = np.asarray(cdf.varget("db_dt"))
    ep = np.asarray(cdf.varget("epoch_db_dt"))
    labs = labels(cdf)

    if db.ndim != 2:
        raise RuntimeError(f"{path}: db_dt is {db.shape}, expected 2-D")
    if db.shape[0] <= 16 and db.shape[1] > db.shape[0]:
        db = db.T
    if db.shape[1] < 3:
        raise RuntimeError(f"{path}: expected H,D,Z; db_dt={db.shape}")

    dt = np.asarray(cdflib.cdfepoch.to_datetime(ep), dtype="datetime64[us]")
    if len(dt) != len(db):
        raise RuntimeError(f"{path}: epoch/db length mismatch {len(dt)} != {len(db)}")

    return db.astype(np.float64, copy=False), dt, labs


def hourly_windows(db, dt):
    # Actual UTC hour key for every sample.
    hour_key = dt.astype("datetime64[h]")
    unique_hours = np.unique(hour_key)

    for hk in unique_hours:
        # Seconds elapsed from start of this UTC hour.
        in_hour = (dt - hk).astype("timedelta64[us]").astype(np.int64) / 1e6
        mask = ((hour_key == hk) &
                (in_hour >= WINDOW_MINUTE * 60) &
                (in_hour < WINDOW_MINUTE * 60 + WINDOW_SECONDS))
        idx = np.flatnonzero(mask)

        if len(idx) < int(0.95 * N_WINDOW):
            continue

        idx = idx[:N_WINDOW]
        block = db[idx, :3]
        if len(block) < int(0.95 * N_WINDOW):
            continue

        # ISO UTC hour for reporting.
        hour_text = np.datetime_as_string(hk, unit="h")
        yield hour_text, block


def cluster_pair(agg, pair_name):
    d = agg[agg.Pair == pair_name].sort_values("Frequency_Hz").copy()
    if d.empty:
        return []

    scores = d.Integrated_PLV_Score.to_numpy(float)
    finite = scores[np.isfinite(scores)]
    if not len(finite):
        return []

    med = np.median(finite)
    mad = np.median(np.abs(finite - med))
    dyn = max(8.0, med + 1.5 * mad)
    smooth = savgol_filter(scores, 5, 2, mode="interp") if len(scores) >= 5 else scores
    active = smooth >= dyn
    freqs = d.Frequency_Hz.to_numpy(float)

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
        peak_i = sub.Integrated_PLV_Score.idxmax()
        peak = d.loc[peak_i]
        lo = float(sub.Frequency_Hz.min())
        hi = float(sub.Frequency_Hz.max())

        gi = int(np.argmax(smooth[g]))
        ai = g[gi]
        peak_sm = smooth[ai]
        left = smooth[max(0, ai-2):ai]
        right = smooth[ai+1:min(len(smooth), ai+3)]
        shoulders = np.concatenate([left, right]) if len(left)+len(right) else np.array([0.0])
        shoulder = float(np.median(shoulders))
        prom = 100.0 * max(0.0, peak_sm - shoulder) / max(abs(shoulder), 1e-12)

        rows.append({
            "Station": "IST",
            "Pair": pair_name,
            "Start_Hz": lo,
            "End_Hz": hi,
            "Center_Hz": (lo + hi) / 2.0,
            "Width_Hz": hi - lo,
            "Peak_Hz": float(peak.Frequency_Hz),
            "Peak_Mean_PLV": float(peak.Mean_Raw_PLV),
            "Peak_Hours_Active": int(peak.Hours_Active),
            "Integrated_PLV_Score": float(sub.Integrated_PLV_Score.sum()),
            "Local_Prominence_pct": prom,
            "Classification": "Sharp Carrier Peak" if prom >= 35 else "Phase Coherent Band",
            "Dynamic_Score_Threshold": dyn,
        })
    return rows


def main():
    paths = sorted(set(glob.glob("isee_induction_ist_*.cdf") +
                       glob.glob("isee_induction_ist_*.CDF")))
    if not paths:
        raise RuntimeError("No isee_induction_ist_*.cdf files found.")

    freqs = np.round(np.arange(FREQ_MIN, FREQ_MAX + FREQ_STEP/2, FREQ_STEP), 10)
    filters = [make_filter(f) for f in freqs]

    print("================================================")
    print(" ISTOK IST FAST BLIND 60-S PLV CARRIER SEARCH")
    print("================================================")
    print(f"Files: {len(paths)}")
    print(f"fs={FS:g} Hz | scan={FREQ_MIN:.1f}-{FREQ_MAX:.1f} Hz | step={FREQ_STEP:.1f} Hz")
    print(f"bandwidth={BANDWIDTH:.1f} Hz | one window/UTC hour = minute 30")
    print("pairs: H-D")
    print("NO EXPECTED FREQUENCY IS USED\n")

    profile_rows, vote_rows = [], []
    total_windows = 0
    printed_labels = False

    for path in paths:
        db, dt, labs = load_ist(path)
        if not printed_labels:
            print("CDF labels:", labs)
            printed_labels = True

        windows = list(hourly_windows(db, dt))
        print(f"{os.path.basename(path)}: {len(windows)} usable hourly windows")

        for hour_text, block in windows:
            total_windows += 1

            for ia, ib, pname in PAIRS:
                a = block[:, ia].copy()
                b = block[:, ib].copy()
                good = np.isfinite(a) & np.isfinite(b)

                if np.count_nonzero(good) < int(0.95 * N_WINDOW):
                    continue

                a = a[good]
                b = b[good]
                a -= np.mean(a)
                b -= np.mean(b)

                plv = scan_window(a, b, filters)
                threshold = robust_threshold(plv)
                passed = np.isfinite(plv) & (plv >= threshold)

                for f, v, ok in zip(freqs, plv, passed):
                    profile_rows.append({
                        "Station": "IST",
                        "UTC_Hour": hour_text,
                        "Pair": pname,
                        "Frequency_Hz": f,
                        "PLV": v,
                        "Hour_Threshold": threshold,
                        "Passed": int(ok),
                    })
                    if ok:
                        vote_rows.append({
                            "Station": "IST",
                            "UTC_Hour": hour_text,
                            "Pair": pname,
                            "Frequency_Hz": f,
                            "PLV": v,
                            "Score": v * 10.0,
                        })

                best_i = int(np.nanargmax(plv))
                print(f"  {hour_text} {pname}: best={freqs[best_i]:.3f} Hz "
                      f"PLV={plv[best_i]:.4f} thr={threshold:.4f}")

    profile = pd.DataFrame(profile_rows)
    votes = pd.DataFrame(vote_rows)
    profile.to_csv(OUT_PROFILE, index=False)
    votes.to_csv(OUT_VOTES, index=False)

    aggregate_rows = []
    for pname in [p[2] for p in PAIRS]:
        ps = profile[profile.Pair == pname]
        vs = votes[votes.Pair == pname] if not votes.empty else pd.DataFrame()

        for f in freqs:
            raw = ps[ps.Frequency_Hz == f].PLV.dropna()
            active = vs[vs.Frequency_Hz == f] if not vs.empty else pd.DataFrame()
            aggregate_rows.append({
                "Station": "IST",
                "Pair": pname,
                "Frequency_Hz": f,
                "Hours_Available": int(len(raw)),
                "Hours_Active": int(len(active)),
                "Mean_Raw_PLV": float(raw.mean()) if len(raw) else np.nan,
                "Median_Raw_PLV": float(raw.median()) if len(raw) else np.nan,
                "Mean_Active_PLV": float(active.PLV.mean()) if len(active) else np.nan,
                "Integrated_PLV_Score": float(active.Score.sum()) if len(active) else 0.0,
            })

    agg = pd.DataFrame(aggregate_rows)

    rows = []
    for pname in [p[2] for p in PAIRS]:
        rows.extend(cluster_pair(agg, pname))

    carriers = pd.DataFrame(rows)
    carriers.to_csv(OUT_CARRIERS, index=False)

    print("\n================================================")
    print(" FROZEN BLIND ISTOK RESULTS")
    print("================================================")
    print("Usable UTC-hour windows:", total_windows)

    if carriers.empty:
        print("No aggregate carrier clusters passed.")
    else:
        cols = ["Pair","Start_Hz","End_Hz","Center_Hz","Peak_Hz",
                "Peak_Mean_PLV","Peak_Hours_Active","Integrated_PLV_Score",
                "Classification"]
        print(carriers[cols].to_string(index=False))

    print("\nSaved:")
    print(" ", OUT_PROFILE)
    print(" ", OUT_VOTES)
    print(" ", OUT_CARRIERS)


if __name__ == "__main__":
    main()
