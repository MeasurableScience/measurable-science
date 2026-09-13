#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ESKDALEMUIR — 12-day fine PLV refinement of the already blind-detected
6.8–8.2 Hz annual carrier band.

Purpose:
- DO NOT rediscover the carrier.
- The annual blind scan already found 6.8–8.2 Hz with peak 7.6 Hz.
- This script only refines that region on an objective 12-day subset.

Subset:
- Data span Sep–Dec 2012.
- For each month choose the available paired-data day nearest 5th, 15th, 25th.
- Use every paired hour on those selected days.
- From each hour load only minute 30:00–30:59 (60 s), same as the original scan.

Fine scan:
- CH1 vs CH2
- fs = 100 Hz
- 6.5–8.5 Hz
- step = 0.001 Hz
- Butterworth order 4
- bandwidth = 0.1 Hz (kept from supplied Scottish script)
- Hilbert PLV

Important:
Because this is a refinement over a restricted frequency range, it does NOT
recompute the original broad-band median+2*MAD discovery threshold. Narrowing
the range would change that threshold. Instead, this script reports:
- aggregate mean/median PLV profile
- aggregate peak frequency
- weighted center of the aggregate profile
- per-hour peak frequency
- per-hour weighted center
- median/MAD/std/quantiles of those hourly values

No expected frequency is inserted.
"""

import os
import re
import glob
import sys
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, hilbert

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------

FS = 100.0

START_TIME = pd.Timestamp("2012-09-01 00:00:00")
END_TIME   = pd.Timestamp("2012-12-31 23:00:00")

FREQ_MIN = 6.5
FREQ_MAX = 8.5
FREQ_STEP = 0.001

BANDWIDTH = 0.1
FILTER_ORDER = 4

WINDOW_SEC = 60
WINDOW_START_SEC = 30 * 60
N_WINDOW = int(FS * WINDOW_SEC)

TARGET_DAYS = (5, 15, 25)

OUT_PROFILE   = "ESK_REFINED_12DAY_PROFILE.csv"
OUT_AGGREGATE = "ESK_REFINED_12DAY_AGGREGATE.csv"
OUT_HOURLY    = "ESK_REFINED_12DAY_HOURLY.csv"
OUT_SUMMARY   = "ESK_REFINED_12DAY_SUMMARY.csv"

FILE_RE = re.compile(r"CH([12])_(\d{4})_(\d{2})_(\d{2})_(\d{2})\.dat$")


# ------------------------------------------------------------
# FILE HANDLING
# ------------------------------------------------------------

def parse_file(path):
    name = os.path.basename(path)
    m = FILE_RE.match(name)
    if not m:
        return None, None

    ch = int(m.group(1))
    try:
        ts = pd.Timestamp(
            year=int(m.group(2)),
            month=int(m.group(3)),
            day=int(m.group(4)),
            hour=int(m.group(5)),
        )
    except Exception:
        return None, None

    return ch, ts


def build_pairs():
    ch1 = {}
    ch2 = {}

    for path in glob.glob("CH1_2012_*.dat"):
        ch, ts = parse_file(path)
        if ch == 1 and ts is not None and START_TIME <= ts <= END_TIME:
            ch1[ts] = path

    for path in glob.glob("CH2_2012_*.dat"):
        ch, ts = parse_file(path)
        if ch == 2 and ts is not None and START_TIME <= ts <= END_TIME:
            ch2[ts] = path

    common = sorted(set(ch1) & set(ch2))

    print()
    print("==============================================")
    print("ESKDALEMUIR 12-DAY FINE PLV REFINEMENT")
    print("==============================================")
    print(f"CH1 u periodu : {len(ch1)}")
    print(f"CH2 u periodu : {len(ch2)}")
    print(f"Upareni sati  : {len(common)}")
    if common:
        print(f"Prvi par      : {common[0]}")
        print(f"Poslednji par : {common[-1]}")
    print("==============================================")

    if not common:
        raise RuntimeError("Nema uparenih CH1/CH2 podataka.")

    # Available calendar days with at least one paired hour.
    by_month = {}
    for ts in common:
        by_month.setdefault((ts.year, ts.month), set()).add(ts.normalize())

    selected_days = []
    for ym in sorted(by_month):
        days = sorted(by_month[ym])
        for target in TARGET_DAYS:
            chosen = min(days, key=lambda d: (abs(d.day - target), d.day))
            if chosen not in selected_days:
                selected_days.append(chosen)

    selected_days = sorted(selected_days)
    selected_set = set(selected_days)
    selected_hours = [ts for ts in common if ts.normalize() in selected_set]

    print()
    print("Objektivno izabrani dani:")
    for d in selected_days:
        n = sum(ts.normalize() == d for ts in selected_hours)
        print(f"  {d.date()}   paired hours={n}")
    print(f"Selected days : {len(selected_days)}")
    print(f"Selected hours: {len(selected_hours)}")
    print()

    return ch1, ch2, selected_hours, selected_days


def load_60s(path):
    start_sample = int(WINDOW_START_SEC * FS)
    x = np.loadtxt(
        path,
        dtype=np.float64,
        skiprows=start_sample,
        max_rows=N_WINDOW,
    )
    return np.asarray(x, dtype=np.float64).ravel()


# ------------------------------------------------------------
# PLV
# ------------------------------------------------------------

def calculate_plv(a, b):
    pa = np.angle(hilbert(a))
    pb = np.angle(hilbert(b))
    return float(np.abs(np.mean(np.exp(1j * (pa - pb)))))


def make_filters(freqs):
    filters = []
    half = BANDWIDTH / 2.0

    for f in freqs:
        low = float(f - half)
        high = float(f + half)

        if low <= 0.0 or high >= FS / 2.0:
            filters.append(None)
            continue

        sos = butter(
            FILTER_ORDER,
            [low, high],
            btype="bandpass",
            fs=FS,
            output="sos",
        )
        filters.append(sos)

    return filters


def scan_window(a, b, filters):
    a = a - np.mean(a)
    b = b - np.mean(b)

    vals = np.empty(len(filters), dtype=np.float64)
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
    """
    Center of PLV structure after subtracting its own local median baseline.
    This prevents a flat background PLV level from pulling the centroid toward
    the arithmetic middle of 6.5–8.5 Hz.
    """
    f = np.asarray(freqs, dtype=float)
    v = np.asarray(values, dtype=float)
    good = np.isfinite(f) & np.isfinite(v)

    if not np.any(good):
        return np.nan

    f = f[good]
    v = v[good]
    baseline = np.median(v)
    w = np.maximum(v - baseline, 0.0)

    if np.sum(w) <= 0:
        return np.nan

    return float(np.sum(f * w) / np.sum(w))


def robust_mad(x):
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if not len(x):
        return np.nan
    med = np.median(x)
    return float(np.median(np.abs(x - med)))


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    ch1_files, ch2_files, hours, selected_days = build_pairs()

    freqs = np.round(
        np.arange(FREQ_MIN, FREQ_MAX + FREQ_STEP / 2.0, FREQ_STEP),
        3,
    )
    filters = make_filters(freqs)

    print(f"Fine grid      : {FREQ_MIN:.3f}–{FREQ_MAX:.3f} Hz")
    print(f"Step           : {FREQ_STEP:.3f} Hz")
    print(f"Bins           : {len(freqs)}")
    print(f"Bandwidth      : {BANDWIDTH:.3f} Hz")
    print(f"Window         : minute 30, {WINDOW_SEC} s")
    print("NO EXPECTED FREQUENCY IS USED")
    print()

    profile_rows = []
    hourly_rows = []

    usable = 0

    for i, ts in enumerate(hours, 1):
        try:
            a = load_60s(ch1_files[ts])
            b = load_60s(ch2_files[ts])

            n = min(len(a), len(b))
            if n < int(0.95 * N_WINDOW):
                print(f"SKIP {ts}: too short CH1={len(a)} CH2={len(b)}")
                continue

            a = a[:N_WINDOW]
            b = b[:N_WINDOW]

            if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
                print(f"SKIP {ts}: non-finite values")
                continue

            plv = scan_window(a, b, filters)
            if not np.isfinite(plv).any():
                print(f"SKIP {ts}: no valid PLV")
                continue

            usable += 1

            best_i = int(np.nanargmax(plv))
            peak_f = float(freqs[best_i])
            peak_plv = float(plv[best_i])
            wc = weighted_center(freqs, plv)

            hourly_rows.append({
                "timestamp": ts,
                "Peak_Freq_Hz": peak_f,
                "Peak_PLV": peak_plv,
                "Weighted_Center_Hz": wc,
            })

            for f, v in zip(freqs, plv):
                profile_rows.append({
                    "timestamp": ts,
                    "frequency": float(f),
                    "PLV": float(v) if np.isfinite(v) else np.nan,
                })

            print(
                f"[{i:>3}/{len(hours)}] {ts}  "
                f"peak={peak_f:.3f} Hz  PLV={peak_plv:.4f}  "
                f"wcenter={wc:.4f} Hz"
            )

        except Exception as e:
            print(f"ERROR {ts}: {e}")

    if not profile_rows:
        raise RuntimeError("Nema validnih refinement rezultata.")

    profile = pd.DataFrame(profile_rows)
    hourly = pd.DataFrame(hourly_rows)

    profile.to_csv(OUT_PROFILE, index=False)
    hourly.to_csv(OUT_HOURLY, index=False)

    aggregate = (
        profile.groupby("frequency")["PLV"]
        .agg(["count", "mean", "median", "std"])
        .reset_index()
        .rename(columns={
            "count": "Hours_Available",
            "mean": "Mean_PLV",
            "median": "Median_PLV",
            "std": "Std_PLV",
        })
    )
    aggregate.to_csv(OUT_AGGREGATE, index=False)

    best_mean_i = int(aggregate["Mean_PLV"].idxmax())
    best_med_i = int(aggregate["Median_PLV"].idxmax())

    agg_peak_mean = float(aggregate.loc[best_mean_i, "frequency"])
    agg_peak_mean_plv = float(aggregate.loc[best_mean_i, "Mean_PLV"])

    agg_peak_median = float(aggregate.loc[best_med_i, "frequency"])
    agg_peak_median_plv = float(aggregate.loc[best_med_i, "Median_PLV"])

    agg_wc_mean = weighted_center(
        aggregate["frequency"].to_numpy(),
        aggregate["Mean_PLV"].to_numpy(),
    )
    agg_wc_median = weighted_center(
        aggregate["frequency"].to_numpy(),
        aggregate["Median_PLV"].to_numpy(),
    )

    hp = hourly["Peak_Freq_Hz"].to_numpy(float)
    hw = hourly["Weighted_Center_Hz"].to_numpy(float)

    summary = pd.DataFrame([{
        "Selected_Days": len(selected_days),
        "Usable_Hours": usable,

        "Aggregate_Peak_Mean_Hz": agg_peak_mean,
        "Aggregate_Peak_Mean_PLV": agg_peak_mean_plv,

        "Aggregate_Peak_Median_Hz": agg_peak_median,
        "Aggregate_Peak_Median_PLV": agg_peak_median_plv,

        "Aggregate_Weighted_Center_Mean_Hz": agg_wc_mean,
        "Aggregate_Weighted_Center_Median_Hz": agg_wc_median,

        "Hourly_Peak_Mean_Hz": float(np.nanmean(hp)),
        "Hourly_Peak_Median_Hz": float(np.nanmedian(hp)),
        "Hourly_Peak_MAD_Hz": robust_mad(hp),
        "Hourly_Peak_Std_Hz": float(np.nanstd(hp, ddof=1)) if len(hp) > 1 else np.nan,
        "Hourly_Peak_Q05_Hz": float(np.nanquantile(hp, 0.05)),
        "Hourly_Peak_Q95_Hz": float(np.nanquantile(hp, 0.95)),

        "Hourly_WCenter_Mean_Hz": float(np.nanmean(hw)),
        "Hourly_WCenter_Median_Hz": float(np.nanmedian(hw)),
        "Hourly_WCenter_MAD_Hz": robust_mad(hw),
        "Hourly_WCenter_Std_Hz": float(np.nanstd(hw, ddof=1)) if len(hw) > 1 else np.nan,
        "Hourly_WCenter_Q05_Hz": float(np.nanquantile(hw, 0.05)),
        "Hourly_WCenter_Q95_Hz": float(np.nanquantile(hw, 0.95)),
    }])

    summary.to_csv(OUT_SUMMARY, index=False)

    print()
    print("================================================")
    print(" FROZEN 12-DAY FINE REFINEMENT RESULT")
    print("================================================")
    print(f"Selected days                  : {len(selected_days)}")
    print(f"Usable hourly windows          : {usable}")
    print()
    print(f"Aggregate peak of MEAN PLV     : {agg_peak_mean:.3f} Hz")
    print(f"Mean PLV at that bin           : {agg_peak_mean_plv:.6f}")
    print(f"Aggregate peak of MEDIAN PLV   : {agg_peak_median:.3f} Hz")
    print(f"Median PLV at that bin         : {agg_peak_median_plv:.6f}")
    print()
    print(f"Weighted center of MEAN profile: {agg_wc_mean:.6f} Hz")
    print(f"Weighted center of MEDIAN prof.: {agg_wc_median:.6f} Hz")
    print()
    print(f"Hourly peak median             : {np.nanmedian(hp):.6f} Hz")
    print(f"Hourly peak MAD                : {robust_mad(hp):.6f} Hz")
    print(f"Hourly peak 5–95%              : "
          f"{np.nanquantile(hp,0.05):.6f} – {np.nanquantile(hp,0.95):.6f} Hz")
    print()
    print(f"Hourly weighted-center median  : {np.nanmedian(hw):.6f} Hz")
    print(f"Hourly weighted-center MAD     : {robust_mad(hw):.6f} Hz")
    print(f"Hourly w.center 5–95%          : "
          f"{np.nanquantile(hw,0.05):.6f} – {np.nanquantile(hw,0.95):.6f} Hz")
    print()
    print("Saved:")
    print(f"  {OUT_PROFILE}")
    print(f"  {OUT_AGGREGATE}")
    print(f"  {OUT_HOURLY}")
    print(f"  {OUT_SUMMARY}")


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise RuntimeError("Pokreni sa python3.")
    main()
