#!/usr/bin/env python3
"""
CARISMA induction-coil blind PLV carrier search
Adapted from the Eskdalemuir 60 s PLV scan.

Input:
    2026-09-04_to_2026-09-04_icm_all_data.zip

CARISMA ICM20 format verified from the supplied archive:
    # STATION YYYYMMDD lat lon H... D... pT 20Hz
    HHMMSS.sss   channel_1   channel_2   quality

Blind analysis:
- each station independently
- one fixed 60 s window per available hour: minute 30:00-31:00
- sample rate 20 Hz
- 1.0-9.5 Hz, step 0.1 Hz
- 0.4 Hz total Butterworth bandpass width
- Hilbert phase-locking value (PLV) between the two coil channels
- per-hour threshold = max(0.30, median(PLV)+2*MAD)
- aggregate score = sum(PLV*10) for bins passing threshold
- carrier clustering follows the previous Eskdalemuir logic

No expected carrier frequency is supplied to the detector.
"""

import os
import re
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, hilbert, savgol_filter

DATA_DIR = "."

FS = 20.0
WINDOW_START_SEC = 30 * 60
WINDOW_SECONDS = 60
N_WINDOW = int(FS * WINDOW_SECONDS)

FREQ_MIN = 1.0
FREQ_MAX = 9.5
FREQ_STEP = 0.1
BANDWIDTH = 0.4
FILTER_ORDER = 4

MIN_ABSOLUTE_PLV = 0.30

OUT_PROFILE = "CARISMA_PLV_60S_PROFILE.csv"
OUT_VOTES = "CARISMA_PLV_60S_VOTES.csv"
OUT_CARRIERS = "CARISMA_PLV_60S_CARRIERS.csv"

FILE_RE = re.compile(r"^(\d{8})([A-Z0-9]+)(\d{2})\.ICM20$", re.I)


def calculate_plv(a, b):
    pa = np.angle(hilbert(a))
    pb = np.angle(hilbert(b))
    return float(np.abs(np.mean(np.exp(1j * (pa - pb)))))


def read_60s_window(path):
    """
    Read only samples from 30:00.000 through 30:59.950 of the hourly file.
    Columns 2 and 3 are the two induction-coil channels.
    """
    start_ms = WINDOW_START_SEC * 1000
    end_ms = (WINDOW_START_SEC + WINDOW_SECONDS) * 1000

    c1 = []
    c2 = []

    with open(path, "r", encoding="ascii", errors="replace") as text:
        for line in text:
            if not line or line.startswith("#"):
                continue

            p = line.split()
            if len(p) < 3:
                continue

            t = p[0]
            if len(t) < 10 or "." not in t:
                continue

            try:
                hh = int(t[0:2])
                mm = int(t[2:4])
                ss = float(t[4:])
                sec_in_hour = mm * 60.0 + ss
                ms = int(round(sec_in_hour * 1000.0))
            except Exception:
                continue

            if ms < start_ms:
                continue
            if ms >= end_ms:
                break

            try:
                v1 = float(p[1])
                v2 = float(p[2])
            except ValueError:
                continue

            if np.isfinite(v1) and np.isfinite(v2):
                c1.append(v1)
                c2.append(v2)

    if len(c1) < int(0.95 * N_WINDOW):
        return None, None

    # Exactly the first 60 s worth if there are extras.
    a = np.asarray(c1[:N_WINDOW], dtype=np.float64)
    b = np.asarray(c2[:N_WINDOW], dtype=np.float64)

    a -= np.mean(a)
    b -= np.mean(b)

    return a, b


def make_filter(center):
    half = BANDWIDTH / 2.0
    low = center - half
    high = center + half

    if low <= 0 or high >= FS / 2.0:
        return None

    return butter(
        FILTER_ORDER,
        [low, high],
        btype="bandpass",
        fs=FS,
        output="sos"
    )


def scan_window(a, b, freqs, filters):
    vals = []

    for f, sos in zip(freqs, filters):
        if sos is None:
            vals.append(np.nan)
            continue

        try:
            af = sosfiltfilt(sos, a)
            bf = sosfiltfilt(sos, b)
            vals.append(calculate_plv(af, bf))
        except Exception:
            vals.append(np.nan)

    return np.asarray(vals, dtype=np.float64)


def robust_threshold(values):
    x = values[np.isfinite(values)]
    if len(x) == 0:
        return np.nan

    med = np.median(x)
    mad = np.median(np.abs(x - med))
    return max(MIN_ABSOLUTE_PLV, med + 2.0 * mad)


def cluster_station(station_profile):
    """
    Cluster active 0.1-Hz bins using the same aggregate-score idea
    as the previous Eskdalemuir script.
    """
    d = station_profile.sort_values("Frequency_Hz").copy()

    scores = d["Integrated_PLV_Score"].to_numpy(dtype=float)
    finite = scores[np.isfinite(scores)]

    if len(finite) == 0:
        return []

    med = np.median(finite)
    mad = np.median(np.abs(finite - med))
    dynamic_threshold = max(8.0, med + 1.5 * mad)

    if len(scores) >= 5:
        smooth = savgol_filter(scores, 5, 2, mode="interp")
    else:
        smooth = scores.copy()

    active = smooth >= dynamic_threshold
    freqs = d["Frequency_Hz"].to_numpy(dtype=float)

    groups = []
    current = []

    for i, is_active in enumerate(active):
        if not is_active:
            if current:
                groups.append(current)
                current = []
            continue

        if not current:
            current = [i]
        elif freqs[i] - freqs[current[-1]] <= 0.15 + 1e-9:
            current.append(i)
        else:
            groups.append(current)
            current = [i]

    if current:
        groups.append(current)

    rows = []

    for g in groups:
        sub = d.iloc[g].copy()
        peak_i = sub["Integrated_PLV_Score"].idxmax()
        peak = d.loc[peak_i]

        lo = float(sub["Frequency_Hz"].min())
        hi = float(sub["Frequency_Hz"].max())
        center = (lo + hi) / 2.0
        width = hi - lo

        # Simple local prominence on the smoothed aggregate score.
        gi = int(np.argmax(smooth[g]))
        absolute_idx = g[gi]
        peak_sm = smooth[absolute_idx]

        left = smooth[max(0, absolute_idx - 2):absolute_idx]
        right = smooth[absolute_idx + 1:min(len(smooth), absolute_idx + 3)]
        shoulders = np.concatenate([left, right]) if len(left) + len(right) else np.array([0.0])
        shoulder = float(np.median(shoulders)) if len(shoulders) else 0.0
        prominence_pct = 100.0 * max(0.0, peak_sm - shoulder) / max(abs(shoulder), 1e-12)

        rows.append({
            "Station": str(sub["Station"].iloc[0]),
            "Start_Hz": lo,
            "End_Hz": hi,
            "Center_Hz": center,
            "Width_Hz": width,
            "Peak_Hz": float(peak["Frequency_Hz"]),
            "Peak_Mean_PLV": float(peak["Mean_Raw_PLV"]),
            "Peak_Hours_Active": int(peak["Hours_Active"]),
            "Integrated_PLV_Score": float(sub["Integrated_PLV_Score"].sum()),
            "Local_Prominence_pct": prominence_pct,
            "Classification": "Sharp Carrier Peak" if prominence_pct >= 35.0 else "Phase Coherent Band",
            "Dynamic_Score_Threshold": dynamic_threshold,
        })

    return rows


def main():
    freqs = np.round(
        np.arange(FREQ_MIN, FREQ_MAX + FREQ_STEP / 2.0, FREQ_STEP),
        10
    )
    filters = [make_filter(f) for f in freqs]

    print("================================================")
    print(" CARISMA ICM20 BLIND 60-S PLV CARRIER SEARCH")
    print("================================================")
    print(f"DATA_DIR: {os.path.abspath(DATA_DIR)}")
    print(f"fs={FS:g} Hz | scan={FREQ_MIN:.1f}-{FREQ_MAX:.1f} Hz | step={FREQ_STEP:.1f} Hz")
    print(f"bandwidth={BANDWIDTH:.1f} Hz | window=minute 30:00-31:00")
    print()

    records = []
    for path in sorted(os.listdir(DATA_DIR)):
        name = os.path.basename(path)
        m = FILE_RE.match(name)
        if not m:
            continue
        date, station, hour = m.groups()
        records.append((station.upper(), date, int(hour), os.path.join(DATA_DIR, path)))

    if not records:
        raise RuntimeError("No *.ICM20 files found in the current folder.")

    stations = sorted(set(r[0] for r in records))
    print("Stations found:", ", ".join(stations))
    print()

    profile_rows = []
    vote_rows = []

    for station in stations:
        station_files = [r for r in records if r[0] == station]
        station_files.sort(key=lambda r: (r[1], r[2]))

        print(f"--- {station}: {len(station_files)} hourly files ---")

        for n, (_, date, hour, path) in enumerate(station_files, 1):
            a, b = read_60s_window(path)

            if a is None:
                print(f"  skip {date} {hour:02d}: insufficient minute-30 data")
                continue

            plv = scan_window(a, b, freqs, filters)
            threshold = robust_threshold(plv)
            passed = np.isfinite(plv) & (plv >= threshold)

            for f, v, ok in zip(freqs, plv, passed):
                profile_rows.append({
                    "Station": station,
                    "Date": date,
                    "Hour_UTC": hour,
                    "Frequency_Hz": f,
                    "PLV": v,
                    "Hour_Threshold": threshold,
                    "Passed": int(ok),
                })

                if ok:
                    vote_rows.append({
                        "Station": station,
                        "Date": date,
                        "Hour_UTC": hour,
                        "Frequency_Hz": f,
                        "PLV": v,
                        "Score": v * 10.0,
                    })

            best_i = int(np.nanargmax(plv))
            print(
                f"  [{n:02d}/{len(station_files):02d}] "
                f"{date} {hour:02d}:00  "
                f"best={freqs[best_i]:.1f} Hz "
                f"PLV={plv[best_i]:.4f} "
                f"thr={threshold:.4f}"
            )

    profile = pd.DataFrame(profile_rows)
    votes = pd.DataFrame(vote_rows)

    profile.to_csv(OUT_PROFILE, index=False)
    votes.to_csv(OUT_VOTES, index=False)

    # Aggregate independently for each station/frequency.
    aggregate_rows = []

    for station in sorted(profile["Station"].unique()):
        ps = profile[profile["Station"] == station]
        vs = votes[votes["Station"] == station] if not votes.empty else pd.DataFrame()

        for f in freqs:
            raw = ps[ps["Frequency_Hz"] == f]["PLV"].dropna()

            if votes.empty:
                active = pd.DataFrame()
            else:
                active = vs[vs["Frequency_Hz"] == f]

            aggregate_rows.append({
                "Station": station,
                "Frequency_Hz": f,
                "Hours_Available": int(len(raw)),
                "Hours_Active": int(len(active)),
                "Mean_Raw_PLV": float(raw.mean()) if len(raw) else np.nan,
                "Median_Raw_PLV": float(raw.median()) if len(raw) else np.nan,
                "Mean_Active_PLV": float(active["PLV"].mean()) if len(active) else np.nan,
                "Integrated_PLV_Score": float(active["Score"].sum()) if len(active) else 0.0,
            })

    agg = pd.DataFrame(aggregate_rows)

    carrier_rows = []
    for station in sorted(agg["Station"].unique()):
        carrier_rows.extend(
            cluster_station(agg[agg["Station"] == station])
        )

    carriers = pd.DataFrame(carrier_rows)
    carriers.to_csv(OUT_CARRIERS, index=False)

    print()
    print("================================================")
    print(" FROZEN BLIND CARISMA RESULTS")
    print("================================================")

    if carriers.empty:
        print("No aggregate carrier clusters passed the clustering threshold.")
    else:
        cols = [
            "Station", "Start_Hz", "End_Hz", "Center_Hz",
            "Peak_Hz", "Peak_Mean_PLV", "Peak_Hours_Active",
            "Integrated_PLV_Score", "Classification"
        ]
        print(carriers[cols].to_string(index=False))

    print()
    print("Saved:")
    print(" ", OUT_PROFILE)
    print(" ", OUT_VOTES)
    print(" ", OUT_CARRIERS)
    print()
    print("Freeze these blind values before comparing with Scotland or any expected frequency.")


if __name__ == "__main__":
    main()
