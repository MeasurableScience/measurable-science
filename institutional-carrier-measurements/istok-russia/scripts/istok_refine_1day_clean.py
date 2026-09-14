#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ISTOK (IST) 64-Hz CDF — one-day fine carrier refinement.

Same refinement estimator used for Scotland / Kunigami:
- all IST CDF files in current folder
- actual UTC hourly windows selected from epoch_db_dt
- one fixed 60-s window per UTC hour: minute 30:00–31:00
- H-D only
- 64 Hz
- fine scan 6.3–8.5 Hz
- step 0.001 Hz
- total Butterworth bandwidth 0.1 Hz
- 4th-order Butterworth
- Hilbert PLV

Outputs:
    IST_REFINED_PROFILE.csv
    IST_REFINED_AGGREGATE.csv
    IST_REFINED_HOURLY.csv
    IST_REFINED_SUMMARY.csv

This is refinement, not a new discovery scan.
No expected carrier frequency is supplied.
Weighted center = positive PLV excess above the median baseline.
"""

import os
import glob
import numpy as np
import pandas as pd
import cdflib
from scipy.signal import butter, sosfiltfilt, hilbert

FS = 64.0
WINDOW_MINUTE = 30
WINDOW_SECONDS = 60
N_WINDOW = int(FS * WINDOW_SECONDS)

FREQ_MIN = 6.3
FREQ_MAX = 8.5
FREQ_STEP = 0.001
BANDWIDTH = 0.1
FILTER_ORDER = 4

OUT_PROFILE = "IST_REFINED_PROFILE.csv"
OUT_AGGREGATE = "IST_REFINED_AGGREGATE.csv"
OUT_HOURLY = "IST_REFINED_HOURLY.csv"
OUT_SUMMARY = "IST_REFINED_SUMMARY.csv"


def calculate_plv(a, b):
    pa = np.angle(hilbert(a))
    pb = np.angle(hilbert(b))
    return float(np.abs(np.mean(np.exp(1j * (pa - pb)))))


def labels(cdf):
    x = np.asarray(cdf.varget("label_db_dt")).ravel()
    return [
        z.decode(errors="replace").strip()
        if isinstance(z, bytes) else str(z).strip()
        for z in x
    ]


def load_ist(path):
    cdf = cdflib.CDF(path)
    db = np.asarray(cdf.varget("db_dt"))
    ep = np.asarray(cdf.varget("epoch_db_dt"))
    labs = labels(cdf)

    if db.ndim != 2:
        raise RuntimeError(f"{path}: db_dt is {db.shape}, expected 2-D")
    if db.shape[0] <= 16 and db.shape[1] > db.shape[0]:
        db = db.T
    if db.shape[1] < 2:
        raise RuntimeError(f"{path}: expected at least H,D; db_dt={db.shape}")

    dt = np.asarray(
        cdflib.cdfepoch.to_datetime(ep),
        dtype="datetime64[us]"
    )
    if len(dt) != len(db):
        raise RuntimeError(
            f"{path}: epoch/db length mismatch {len(dt)} != {len(db)}"
        )

    return db.astype(np.float64, copy=False), dt, labs


def hourly_windows(db, dt):
    hour_key = dt.astype("datetime64[h]")
    unique_hours = np.unique(hour_key)

    for hk in unique_hours:
        in_hour = (
            (dt - hk)
            .astype("timedelta64[us]")
            .astype(np.int64) / 1e6
        )

        mask = (
            (hour_key == hk) &
            (in_hour >= WINDOW_MINUTE * 60) &
            (in_hour < WINDOW_MINUTE * 60 + WINDOW_SECONDS)
        )
        idx = np.flatnonzero(mask)

        if len(idx) < int(0.95 * N_WINDOW):
            continue

        idx = idx[:N_WINDOW]
        block = db[idx, :2]

        if len(block) < int(0.95 * N_WINDOW):
            continue

        hour_text = np.datetime_as_string(hk, unit="h")
        yield hour_text, block


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


def scan_window(a, b, filters):
    vals = np.empty(len(filters), dtype=float)
    vals.fill(np.nan)

    for i, sos in enumerate(filters):
        if sos is None:
            continue
        try:
            af = sosfiltfilt(sos, a)
            bf = sosfiltfilt(sos, b)
            vals[i] = calculate_plv(af, bf)
        except Exception:
            vals[i] = np.nan

    return vals


def weighted_center(freqs, values):
    f = np.asarray(freqs, dtype=float)
    v = np.asarray(values, dtype=float)

    good = np.isfinite(f) & np.isfinite(v)
    if not np.any(good):
        return np.nan

    f = f[good]
    v = v[good]

    baseline = np.median(v)
    w = np.maximum(v - baseline, 0.0)

    sw = np.sum(w)
    if sw <= 0:
        return np.nan

    return float(np.sum(f * w) / sw)


def robust_stats(values):
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]

    if len(x) == 0:
        return {
            "n": 0,
            "mean": np.nan,
            "median": np.nan,
            "mad": np.nan,
            "std": np.nan,
            "q05": np.nan,
            "q95": np.nan,
        }

    med = float(np.median(x))
    return {
        "n": int(len(x)),
        "mean": float(np.mean(x)),
        "median": med,
        "mad": float(np.median(np.abs(x - med))),
        "std": float(np.std(x, ddof=1)) if len(x) > 1 else 0.0,
        "q05": float(np.quantile(x, 0.05)),
        "q95": float(np.quantile(x, 0.95)),
    }


def main():
    paths = sorted(set(
        glob.glob("isee_induction_ist_*.cdf") +
        glob.glob("isee_induction_ist_*.CDF")
    ))

    if not paths:
        raise RuntimeError("No isee_induction_ist_*.cdf files found.")

    freqs = np.round(
        np.arange(
            FREQ_MIN,
            FREQ_MAX + FREQ_STEP / 2.0,
            FREQ_STEP
        ),
        6
    )
    filters = [make_filter(f) for f in freqs]

    print("================================================")
    print(" ISTOK IST — FINE REFINEMENT")
    print("================================================")
    print(f"Files: {len(paths)}")
    print(
        f"fs={FS:g} Hz | scan={FREQ_MIN:.3f}-{FREQ_MAX:.3f} Hz "
        f"| step={FREQ_STEP:.3f} Hz"
    )
    print(
        f"bandwidth={BANDWIDTH:.3f} Hz | "
        "one window/UTC hour = minute 30:00-31:00"
    )
    print("pair: H-D")
    print("REFINEMENT ONLY — NO EXPECTED FREQUENCY IS USED")
    print()

    profile_rows = []
    hourly_rows = []
    printed_labels = False

    for path in paths:
        db, dt, labs = load_ist(path)

        if not printed_labels:
            print("CDF labels:", labs)
            print()
            printed_labels = True

        windows = list(hourly_windows(db, dt))
        print(
            f"{os.path.basename(path)}: "
            f"{len(windows)} usable hourly windows"
        )

        for hour_text, block in windows:
            a = block[:, 0].copy()
            b = block[:, 1].copy()

            good = np.isfinite(a) & np.isfinite(b)
            if np.count_nonzero(good) < int(0.95 * N_WINDOW):
                continue

            a = a[good]
            b = b[good]
            a -= np.mean(a)
            b -= np.mean(b)

            plv = scan_window(a, b, filters)

            if not np.any(np.isfinite(plv)):
                print(f"  skip {hour_text}: no finite PLV values")
                continue

            best_i = int(np.nanargmax(plv))
            peak_hz = float(freqs[best_i])
            peak_plv = float(plv[best_i])
            wc = weighted_center(freqs, plv)

            hourly_rows.append({
                "Station": "IST",
                "UTC_Hour": hour_text,
                "Peak_Hz": peak_hz,
                "Peak_PLV": peak_plv,
                "Weighted_Center_Hz": wc,
            })

            for f, v in zip(freqs, plv):
                profile_rows.append({
                    "Station": "IST",
                    "UTC_Hour": hour_text,
                    "Frequency_Hz": float(f),
                    "PLV": float(v) if np.isfinite(v) else np.nan,
                })

            wc_text = f"{wc:.4f}" if np.isfinite(wc) else "nan"
            print(
                f"  {hour_text} H-D: "
                f"peak={peak_hz:.3f} Hz "
                f"PLV={peak_plv:.4f} "
                f"wcenter={wc_text}"
            )

    profile = pd.DataFrame(profile_rows)
    hourly = pd.DataFrame(hourly_rows)

    if profile.empty or hourly.empty:
        raise RuntimeError("No usable IST hourly windows were analyzed.")

    profile.to_csv(OUT_PROFILE, index=False)
    hourly.to_csv(OUT_HOURLY, index=False)

    agg = (
        profile.groupby("Frequency_Hz", as_index=False)["PLV"]
        .agg(
            Mean_PLV="mean",
            Median_PLV="median",
            Hours_Available="count",
        )
        .sort_values("Frequency_Hz")
        .reset_index(drop=True)
    )
    agg.insert(0, "Station", "IST")
    agg.to_csv(OUT_AGGREGATE, index=False)

    mean_i = int(np.nanargmax(agg["Mean_PLV"].to_numpy(float)))
    median_i = int(np.nanargmax(agg["Median_PLV"].to_numpy(float)))

    mean_peak_hz = float(agg.iloc[mean_i]["Frequency_Hz"])
    mean_peak_plv = float(agg.iloc[mean_i]["Mean_PLV"])

    median_peak_hz = float(agg.iloc[median_i]["Frequency_Hz"])
    median_peak_plv = float(agg.iloc[median_i]["Median_PLV"])

    wc_mean = weighted_center(
        agg["Frequency_Hz"],
        agg["Mean_PLV"]
    )
    wc_median = weighted_center(
        agg["Frequency_Hz"],
        agg["Median_PLV"]
    )

    peak_stats = robust_stats(hourly["Peak_Hz"])
    wc_stats = robust_stats(hourly["Weighted_Center_Hz"])

    summary = pd.DataFrame([{
        "Station": "IST",
        "Usable_Hourly_Windows": len(hourly),
        "Valid_Hourly_Weighted_Centers": wc_stats["n"],

        "Aggregate_Peak_Mean_PLV_Hz": mean_peak_hz,
        "Aggregate_Peak_Mean_PLV": mean_peak_plv,

        "Aggregate_Peak_Median_PLV_Hz": median_peak_hz,
        "Aggregate_Peak_Median_PLV": median_peak_plv,

        "Weighted_Center_Mean_Profile_Hz": wc_mean,
        "Weighted_Center_Median_Profile_Hz": wc_median,

        "Hourly_Peak_Mean_Hz": peak_stats["mean"],
        "Hourly_Peak_Median_Hz": peak_stats["median"],
        "Hourly_Peak_MAD_Hz": peak_stats["mad"],
        "Hourly_Peak_STD_Hz": peak_stats["std"],
        "Hourly_Peak_Q05_Hz": peak_stats["q05"],
        "Hourly_Peak_Q95_Hz": peak_stats["q95"],

        "Hourly_WCenter_Mean_Hz": wc_stats["mean"],
        "Hourly_WCenter_Median_Hz": wc_stats["median"],
        "Hourly_WCenter_MAD_Hz": wc_stats["mad"],
        "Hourly_WCenter_STD_Hz": wc_stats["std"],
        "Hourly_WCenter_Q05_Hz": wc_stats["q05"],
        "Hourly_WCenter_Q95_Hz": wc_stats["q95"],
    }])

    summary.to_csv(OUT_SUMMARY, index=False)

    print()
    print("================================================")
    print(" FROZEN ISTOK FINE REFINEMENT RESULT")
    print("================================================")
    print(f"Usable hourly windows           : {len(hourly)}")
    print(
        f"Valid hourly weighted centers   : "
        f"{wc_stats['n']} / {len(hourly)}"
    )
    print()
    print(
        f"Aggregate peak of MEAN PLV      : "
        f"{mean_peak_hz:.3f} Hz"
    )
    print(
        f"Mean PLV at that bin            : "
        f"{mean_peak_plv:.6f}"
    )
    print(
        f"Aggregate peak of MEDIAN PLV    : "
        f"{median_peak_hz:.3f} Hz"
    )
    print(
        f"Median PLV at that bin          : "
        f"{median_peak_plv:.6f}"
    )
    print()
    print(
        f"Weighted center of MEAN profile : "
        f"{wc_mean:.6f} Hz"
    )
    print(
        f"Weighted center of MEDIAN prof. : "
        f"{wc_median:.6f} Hz"
    )
    print()
    print(
        f"Hourly peak median              : "
        f"{peak_stats['median']:.6f} Hz"
    )
    print(
        f"Hourly peak MAD                 : "
        f"{peak_stats['mad']:.6f} Hz"
    )
    print(
        f"Hourly peak 5–95%               : "
        f"{peak_stats['q05']:.6f} – "
        f"{peak_stats['q95']:.6f} Hz"
    )
    print()
    print(
        f"Hourly weighted-center median   : "
        f"{wc_stats['median']:.6f} Hz"
    )
    print(
        f"Hourly weighted-center MAD      : "
        f"{wc_stats['mad']:.6f} Hz"
    )
    print(
        f"Hourly w.center 5–95%           : "
        f"{wc_stats['q05']:.6f} – "
        f"{wc_stats['q95']:.6f} Hz"
    )
    print()
    print("Saved:")
    print(" ", OUT_PROFILE)
    print(" ", OUT_AGGREGATE)
    print(" ", OUT_HOURLY)
    print(" ", OUT_SUMMARY)


if __name__ == "__main__":
    main()
