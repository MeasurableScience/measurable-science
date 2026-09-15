#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KUNIGAMI (KNG) 64-Hz CDF — one-day fine carrier refinement.

This is a refinement analysis, not a new blind discovery scan.
It uses all available KNG hourly CDF files in the current folder,
one fixed 60-s window per hour (UTC minute 30:00–31:00), H-D only.

Fine scan:
    6.5–8.5 Hz
    step 0.001 Hz
    total Butterworth bandwidth 0.1 Hz
    4th-order Butterworth
    Hilbert PLV

Outputs:
    KNG_REFINED_1DAY_PROFILE.csv
    KNG_REFINED_1DAY_AGGREGATE.csv
    KNG_REFINED_1DAY_HOURLY.csv
    KNG_REFINED_1DAY_SUMMARY.csv

Important:
- No expected carrier frequency is supplied.
- No discovery threshold is recomputed inside the restricted fine band.
- Weighted center uses positive PLV excess above each profile/window median.
"""

import os
import glob
import re
import numpy as np
import pandas as pd
import cdflib
from scipy.signal import butter, sosfiltfilt, hilbert

FS = 64.0
WINDOW_START_SEC = 30 * 60
WINDOW_SECONDS = 60
N_WINDOW = int(FS * WINDOW_SECONDS)

FREQ_MIN = 6.5
FREQ_MAX = 8.5
FREQ_STEP = 0.001
BANDWIDTH = 0.1
FILTER_ORDER = 4

OUT_PROFILE = "KNG_REFINED_1DAY_PROFILE.csv"
OUT_AGGREGATE = "KNG_REFINED_1DAY_AGGREGATE.csv"
OUT_HOURLY = "KNG_REFINED_1DAY_HOURLY.csv"
OUT_SUMMARY = "KNG_REFINED_1DAY_SUMMARY.csv"

FILE_RE = re.compile(
    r"isee_induction_kng_(\d{8})(\d{2})_v\d+\.cdf$",
    re.I
)


def calculate_plv(a, b):
    pa = np.angle(hilbert(a))
    pb = np.angle(hilbert(b))
    return float(np.abs(np.mean(np.exp(1j * (pa - pb)))))


def get_labels(cdf):
    try:
        x = np.asarray(cdf.varget("label_db_dt")).ravel()
        return [
            z.decode(errors="replace").strip()
            if isinstance(z, bytes) else str(z).strip()
            for z in x
        ]
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

    epoch = np.asarray(cdf.varget("epoch_db_dt"))
    dt = np.asarray(
        cdflib.cdfepoch.to_datetime(epoch),
        dtype="datetime64[us]"
    )

    hour_start = dt.astype("datetime64[h]")
    sec_from_hour = (
        (dt - hour_start)
        .astype("timedelta64[us]")
        .astype(np.int64) / 1e6
    )

    mask = (
        (sec_from_hour >= WINDOW_START_SEC) &
        (sec_from_hour < WINDOW_START_SEC + WINDOW_SECONDS)
    )
    idx = np.flatnonzero(mask)

    if len(idx) < int(0.95 * N_WINDOW):
        return None, None, labels, len(idx)

    idx = idx[:N_WINDOW]
    a = db[idx, 0].astype(np.float64)
    b = db[idx, 1].astype(np.float64)

    good = np.isfinite(a) & np.isfinite(b)
    if np.count_nonzero(good) < int(0.95 * N_WINDOW):
        return None, None, labels, int(np.count_nonzero(good))

    a = a[good]
    b = b[good]

    if len(a) >= N_WINDOW:
        a = a[:N_WINDOW]
        b = b[:N_WINDOW]

    a -= np.mean(a)
    b -= np.mean(b)

    return a, b, labels, len(a)


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
    freqs = np.asarray(freqs, dtype=float)
    values = np.asarray(values, dtype=float)

    good = np.isfinite(freqs) & np.isfinite(values)
    if not np.any(good):
        return np.nan

    f = freqs[good]
    v = values[good]

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
            "mean": np.nan,
            "median": np.nan,
            "mad": np.nan,
            "std": np.nan,
            "q05": np.nan,
            "q95": np.nan,
        }

    med = float(np.median(x))
    return {
        "mean": float(np.mean(x)),
        "median": med,
        "mad": float(np.median(np.abs(x - med))),
        "std": float(np.std(x, ddof=1)) if len(x) > 1 else 0.0,
        "q05": float(np.quantile(x, 0.05)),
        "q95": float(np.quantile(x, 0.95)),
    }


def main():
    freqs = np.round(
        np.arange(
            FREQ_MIN,
            FREQ_MAX + FREQ_STEP / 2.0,
            FREQ_STEP
        ),
        6
    )
    filters = [make_filter(f) for f in freqs]

    files = []
    for path in sorted(glob.glob("*.cdf") + glob.glob("*.CDF")):
        m = FILE_RE.match(os.path.basename(path))
        if m:
            files.append((m.group(1), int(m.group(2)), path))

    if not files:
        raise RuntimeError(
            "No isee_induction_kng_YYYYMMDDHH_vXX.cdf files found."
        )

    dates = sorted({date for date, _, _ in files})
    if len(dates) > 1:
        print("WARNING: more than one KNG date found:", ", ".join(dates))
        print("All matching files will be analyzed.")

    print("================================================")
    print(" KUNIGAMI KNG — ONE-DAY FINE REFINEMENT")
    print("================================================")
    print(f"Matching hourly files: {len(files)}")
    print(f"Dates: {', '.join(dates)}")
    print(
        f"fs={FS:g} Hz | scan={FREQ_MIN:.3f}-{FREQ_MAX:.3f} Hz "
        f"| step={FREQ_STEP:.3f} Hz"
    )
    print(
        f"bandwidth={BANDWIDTH:.3f} Hz | "
        "one window/file = UTC minute 30:00-31:00"
    )
    print("pair=db_dt[0] vs db_dt[1] (expected H vs D)")
    print("REFINEMENT ONLY — NO EXPECTED FREQUENCY IS USED")
    print()

    profile_rows = []
    hourly_rows = []
    printed_labels = False

    usable = 0

    for n, (date, hour, path) in enumerate(files, 1):
        a, b, labels, nsamp = read_60s_window(path)

        if not printed_labels:
            print("CDF labels:", labels)
            if len(labels) >= 2:
                print(f"Analysis pair: {labels[0]} vs {labels[1]}")
            print()
            printed_labels = True

        if a is None:
            print(
                f"  skip {date} {hour:02d}: "
                f"only {nsamp} usable minute-30 samples"
            )
            continue

        usable += 1
        plv = scan_window(a, b, filters)

        if not np.any(np.isfinite(plv)):
            print(f"  skip {date} {hour:02d}: no finite PLV values")
            continue

        best_i = int(np.nanargmax(plv))
        peak_hz = float(freqs[best_i])
        peak_plv = float(plv[best_i])
        wc = weighted_center(freqs, plv)

        hourly_rows.append({
            "Station": "KNG",
            "Date": date,
            "Hour_UTC": hour,
            "Peak_Hz": peak_hz,
            "Peak_PLV": peak_plv,
            "Weighted_Center_Hz": wc,
        })

        for f, v in zip(freqs, plv):
            profile_rows.append({
                "Station": "KNG",
                "Date": date,
                "Hour_UTC": hour,
                "Frequency_Hz": float(f),
                "PLV": float(v) if np.isfinite(v) else np.nan,
            })

        print(
            f"  [{n:02d}/{len(files):02d}] "
            f"{date} {hour:02d}:00  "
            f"peak={peak_hz:.3f} PLV={peak_plv:.4f} "
            f"wcenter={wc:.4f}"
        )

    profile = pd.DataFrame(profile_rows)
    hourly = pd.DataFrame(hourly_rows)

    if profile.empty or hourly.empty:
        raise RuntimeError("No usable KNG hourly windows were analyzed.")

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
    agg.insert(0, "Station", "KNG")
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
        "Station": "KNG",
        "Dates": ",".join(dates),
        "Matching_Files": len(files),
        "Usable_Hourly_Windows": len(hourly),

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
    print(" FROZEN 1-DAY FINE REFINEMENT RESULT")
    print("================================================")
    print(f"Date(s)                        : {', '.join(dates)}")
    print(f"Usable hourly windows          : {len(hourly)}")
    print()
    print(
        f"Aggregate peak of MEAN PLV     : "
        f"{mean_peak_hz:.3f} Hz"
    )
    print(
        f"Mean PLV at that bin           : "
        f"{mean_peak_plv:.6f}"
    )
    print(
        f"Aggregate peak of MEDIAN PLV   : "
        f"{median_peak_hz:.3f} Hz"
    )
    print(
        f"Median PLV at that bin         : "
        f"{median_peak_plv:.6f}"
    )
    print()
    print(
        f"Weighted center of MEAN profile: "
        f"{wc_mean:.6f} Hz"
    )
    print(
        f"Weighted center of MEDIAN prof.: "
        f"{wc_median:.6f} Hz"
    )
    print()
    print(
        f"Hourly peak median             : "
        f"{peak_stats['median']:.6f} Hz"
    )
    print(
        f"Hourly peak MAD                : "
        f"{peak_stats['mad']:.6f} Hz"
    )
    print(
        f"Hourly peak 5–95%              : "
        f"{peak_stats['q05']:.6f} – "
        f"{peak_stats['q95']:.6f} Hz"
    )
    print()
    print(
        f"Hourly weighted-center median  : "
        f"{wc_stats['median']:.6f} Hz"
    )
    print(
        f"Hourly weighted-center MAD     : "
        f"{wc_stats['mad']:.6f} Hz"
    )
    print(
        f"Hourly w.center 5–95%          : "
        f"{wc_stats['q05']:.6f} – "
        f"{wc_stats['q95']:.6f} Hz"
    )
    print()
    print("Saved:")
    print(" ", OUT_PROFILE)
    print(" ", OUT_AGGREGATE)
    print(" ", OUT_HOURLY)
    print(" ", OUT_SUMMARY)
    print()
    print(
        "Freeze these values before comparing KNG "
        "with Scotland, Istok, or CARISMA."
    )


if __name__ == "__main__":
    main()
