#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kunigami (KNG) — blind local shape analysis

Purpose
-------
Analyse the local H-D geometry inside the frequency region previously
identified by the independent blind frequency search.

IMPORTANT:
The program is NOT told to search for a square.

It measures angular/radial symmetry orders m = 1...6 and reports which
symmetry is dominant in each time window.

Input:
    Kunigami ISEE induction-magnetometer CDF files
    64 Hz
    H and D horizontal components

Previously detected frequency region:
    7.9–8.1 Hz

Method:
    1. Read and concatenate all KNG CDF files for the selected day.
    2. Band-pass filter the continuous H and D records once.
    3. Split into 60-second windows.
    4. Preserve the H:D amplitude relationship using one common scale.
    5. Construct the local H-D trajectory.
    6. Calculate:
       - PLV
       - median phase difference
       - PCA orientation
       - PCA minor/major axis ratio
       - CW / CCW rotation
       - radial angular harmonics m = 1...6
       - dominant symmetry order
    7. Save per-window results, summary and diagnostic figures.

The model prediction is NOT used by the algorithm.
"""

import os
import glob
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import butter, sosfiltfilt, hilbert
from cdflib import CDF, cdfepoch


# ============================================================
# USER SETTINGS
# ============================================================

DATA_DIR = "."

FILE_PATTERN = "isee_induction_kng_20220101*_v01.cdf"

FS = 64.0

F_LOW = 7.9
F_HIGH = 8.1

FILTER_ORDER = 4

WINDOW_SECONDS = 60
WINDOW_SAMPLES = int(FS * WINDOW_SECONDS)

MIN_VALID_FRACTION = 0.98

MAX_SYMMETRY_ORDER = 6

OUTPUT_PREFIX = "KNG_SHAPE"

# Number of angular bins used for the radial shape profile
N_ANGLE_BINS = 360

# Ignore very small radii near trajectory centre when estimating angle
MIN_RADIUS_FRACTION = 0.05


# ============================================================
# CDF READING
# ============================================================

def read_kng_cdf(path):
    """
    Read one Kunigami CDF file.

    Expected variables:
        epoch_db_dt
        db_dt

    db_dt:
        column 0 = H
        column 1 = D
    """

    cdf = CDF(path)

    epoch = np.asarray(cdf.varget("epoch_db_dt"))
    data = np.asarray(cdf.varget("db_dt"), dtype=float)

    if data.ndim != 2 or data.shape[1] < 2:
        raise ValueError(
            f"{path}: db_dt does not contain at least two components."
        )

    times = np.asarray(cdfepoch.to_datetime(epoch))

    h = data[:, 0]
    d = data[:, 1]

    return times, h, d


def load_all_files():
    files = sorted(glob.glob(os.path.join(DATA_DIR, FILE_PATTERN)))

    if not files:
        raise FileNotFoundError(
            f"No files found: {os.path.join(DATA_DIR, FILE_PATTERN)}"
        )

    print(f"Found {len(files)} files")

    all_times = []
    all_h = []
    all_d = []

    for i, path in enumerate(files, 1):
        print(f"[{i:02d}/{len(files):02d}] {os.path.basename(path)}")

        times, h, d = read_kng_cdf(path)

        all_times.append(times)
        all_h.append(h)
        all_d.append(d)

    times = np.concatenate(all_times)
    h = np.concatenate(all_h)
    d = np.concatenate(all_d)

    order = np.argsort(times)

    times = times[order]
    h = h[order]
    d = d[order]

    return files, times, h, d


# ============================================================
# FILTERING
# ============================================================

def bandpass_filter(x):
    sos = butter(
        FILTER_ORDER,
        [F_LOW, F_HIGH],
        btype="bandpass",
        fs=FS,
        output="sos",
    )

    return sosfiltfilt(sos, x)


# ============================================================
# BASIC GEOMETRY
# ============================================================

def common_normalize(h, d):
    """
    One common normalization factor for both channels.

    This preserves the original H:D amplitude ratio and avoids
    artificially forcing the PCA geometry toward ±45 degrees.
    """

    scale = np.sqrt(np.mean(h * h + d * d))

    if not np.isfinite(scale) or scale <= 0:
        return None, None

    return h / scale, d / scale


def phase_metrics(h, d):
    ah = hilbert(h)
    ad = hilbert(d)

    ph = np.angle(ah)
    pd_ = np.angle(ad)

    delta = np.angle(np.exp(1j * (pd_ - ph)))

    plv = np.abs(np.mean(np.exp(1j * delta)))

    mean_phase = np.angle(
        np.mean(np.exp(1j * delta))
    )

    return plv, np.degrees(mean_phase)


def pca_geometry(h, d):
    xy = np.column_stack([h, d])

    cov = np.cov(xy, rowvar=False)

    vals, vecs = np.linalg.eigh(cov)

    idx = np.argsort(vals)[::-1]

    vals = vals[idx]
    vecs = vecs[:, idx]

    major = max(vals[0], 0.0)
    minor = max(vals[1], 0.0)

    if major <= 0:
        axis_ratio = np.nan
    else:
        axis_ratio = np.sqrt(minor / major)

    v = vecs[:, 0]

    orientation = np.degrees(np.arctan2(v[1], v[0]))

    # PCA orientation has 180° ambiguity.
    while orientation >= 90:
        orientation -= 180

    while orientation < -90:
        orientation += 180

    return axis_ratio, orientation


def rotation_direction(h, d):
    """
    Signed polygon area of the H-D trajectory.
    """

    x1 = h[:-1]
    y1 = d[:-1]

    x2 = h[1:]
    y2 = d[1:]

    signed_area = 0.5 * np.sum(x1 * y2 - x2 * y1)

    if signed_area > 0:
        direction = "CCW"
    elif signed_area < 0:
        direction = "CW"
    else:
        direction = "NONE"

    return signed_area, direction


# ============================================================
# BLIND SHAPE ANALYSIS
# ============================================================

def radial_angular_profile(h, d, n_bins=N_ANGLE_BINS):
    """
    Convert H-D trajectory into radius as a function of angle.

    No particular symmetry is assumed.
    """

    # Robust trajectory centre
    hc = h - np.median(h)
    dc = d - np.median(d)

    r = np.sqrt(hc * hc + dc * dc)

    if not np.any(np.isfinite(r)):
        return None

    max_r = np.nanmax(r)

    if max_r <= 0:
        return None

    keep = (
        np.isfinite(hc)
        & np.isfinite(dc)
        & np.isfinite(r)
        & (r >= MIN_RADIUS_FRACTION * max_r)
    )

    hc = hc[keep]
    dc = dc[keep]
    r = r[keep]

    if len(r) < 100:
        return None

    theta = np.mod(np.arctan2(dc, hc), 2 * np.pi)

    edges = np.linspace(0, 2 * np.pi, n_bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])

    bin_index = np.digitize(theta, edges) - 1
    bin_index[bin_index == n_bins] = n_bins - 1

    radial = np.full(n_bins, np.nan)

    for i in range(n_bins):
        values = r[bin_index == i]

        if len(values) > 0:
            # upper radial envelope is more informative about shape
            radial[i] = np.percentile(values, 90)

    valid = np.isfinite(radial)

    if np.count_nonzero(valid) < n_bins * 0.5:
        return None

    # Circular interpolation across missing angular bins
    idx = np.arange(n_bins)

    valid_idx = idx[valid]
    valid_values = radial[valid]

    ext_idx = np.concatenate([
        valid_idx - n_bins,
        valid_idx,
        valid_idx + n_bins
    ])

    ext_values = np.tile(valid_values, 3)

    radial_interp = np.interp(idx, ext_idx, ext_values)

    mean_r = np.mean(radial_interp)

    if mean_r <= 0:
        return None

    radial_norm = radial_interp / mean_r

    return centers, radial_norm


def angular_harmonics(theta, radius):
    """
    Blindly measure angular harmonics m = 1...MAX_SYMMETRY_ORDER.

    A_m = | mean( r(theta) * exp(-i m theta) ) |

    The radial profile is normalized to mean 1.

    No specific order is preferred by the code.
    """

    amplitudes = {}
    phases = {}

    for m in range(1, MAX_SYMMETRY_ORDER + 1):

        z = np.mean(
            radius * np.exp(-1j * m * theta)
        )

        amplitudes[m] = np.abs(z)

        # Shape orientation corresponding to this harmonic.
        # Divide the complex phase by m.
        orientation = -np.angle(z) / m

        orientation_deg = np.degrees(orientation)

        period = 360.0 / m

        orientation_deg = np.mod(
            orientation_deg,
            period
        )

        phases[m] = orientation_deg

    dominant_m = max(
        amplitudes,
        key=amplitudes.get
    )

    return amplitudes, phases, dominant_m


def square_like_corner_ratio(theta, radius):
    """
    Generic fourfold contrast diagnostic.

    This is NOT used to decide whether the shape is a square.

    It simply measures how strongly the radial envelope varies
    four times during one full rotation.
    """

    z4 = np.mean(radius * np.exp(-4j * theta))

    return np.abs(z4)


# ============================================================
# WINDOW ANALYSIS
# ============================================================

def analyse_window(h, d):
    finite = np.isfinite(h) & np.isfinite(d)

    fraction = np.mean(finite)

    if fraction < MIN_VALID_FRACTION:
        return None

    h = h[finite]
    d = d[finite]

    if len(h) < 100:
        return None

    hn, dn = common_normalize(h, d)

    if hn is None:
        return None

    plv, phase_deg = phase_metrics(hn, dn)

    axis_ratio, orientation = pca_geometry(hn, dn)

    signed_area, rotation = rotation_direction(hn, dn)

    profile = radial_angular_profile(hn, dn)

    if profile is None:
        return None

    theta, radius = profile

    amps, phases, dominant_m = angular_harmonics(
        theta,
        radius
    )

    result = {
        "PLV": plv,
        "Phase_D_minus_H_deg": phase_deg,
        "Axis_Ratio": axis_ratio,
        "PCA_Orientation_deg": orientation,
        "Signed_Area": signed_area,
        "Rotation": rotation,
        "Dominant_m": dominant_m,
        "Dominant_m_Amplitude": amps[dominant_m],
    }

    for m in range(1, MAX_SYMMETRY_ORDER + 1):
        result[f"A{m}"] = amps[m]
        result[f"Phi{m}_deg"] = phases[m]

    result["Fourfold_Amplitude"] = square_like_corner_ratio(
        theta,
        radius
    )

    return result


# ============================================================
# SUMMARY
# ============================================================

def circular_orientation_result(values, symmetry_order):
    """
    Mean orientation for an m-fold symmetric shape.

    Angles separated by 360/m degrees are equivalent.
    """

    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.nan, np.nan

    period = 360.0 / symmetry_order

    phi = np.radians(
        values * symmetry_order
    )

    z = np.mean(np.exp(1j * phi))

    mean_angle = (
        np.degrees(np.angle(z))
        / symmetry_order
    )

    mean_angle = np.mod(mean_angle, period)

    concentration = np.abs(z)

    return mean_angle, concentration


def make_summary(df):
    summary = {}

    summary["Windows"] = len(df)

    summary["Median_PLV"] = df["PLV"].median()

    summary["Median_Phase_deg"] = df[
        "Phase_D_minus_H_deg"
    ].median()

    summary["Median_Axis_Ratio"] = df[
        "Axis_Ratio"
    ].median()

    summary["Median_PCA_Orientation_deg"] = df[
        "PCA_Orientation_deg"
    ].median()

    for m in range(1, MAX_SYMMETRY_ORDER + 1):
        summary[f"Median_A{m}"] = df[f"A{m}"].median()
        summary[f"Mean_A{m}"] = df[f"A{m}"].mean()

    dominant_counts = (
        df["Dominant_m"]
        .value_counts()
        .sort_index()
    )

    for m in range(1, MAX_SYMMETRY_ORDER + 1):
        count = int(dominant_counts.get(m, 0))

        summary[f"Dominant_m{m}_Count"] = count
        summary[f"Dominant_m{m}_Percent"] = (
            100.0 * count / len(df)
        )

    cw = int((df["Rotation"] == "CW").sum())
    ccw = int((df["Rotation"] == "CCW").sum())

    summary["CW_Count"] = cw
    summary["CCW_Count"] = ccw

    if cw + ccw:
        summary["CW_Percent"] = (
            100 * cw / (cw + ccw)
        )
        summary["CCW_Percent"] = (
            100 * ccw / (cw + ccw)
        )

    fourfold_orientation, fourfold_concentration = (
        circular_orientation_result(
            df["Phi4_deg"],
            4
        )
    )

    summary["Fourfold_Mean_Orientation_deg"] = (
        fourfold_orientation
    )

    summary["Fourfold_Orientation_Concentration"] = (
        fourfold_concentration
    )

    return pd.DataFrame([summary])


# ============================================================
# FIGURES
# ============================================================

def plot_symmetry_distribution(df):
    medians = [
        df[f"A{m}"].median()
        for m in range(1, MAX_SYMMETRY_ORDER + 1)
    ]

    x = np.arange(1, MAX_SYMMETRY_ORDER + 1)

    plt.figure(figsize=(8, 5))
    plt.bar(x, medians)
    plt.xlabel("Angular symmetry order m")
    plt.ylabel("Median normalized radial harmonic amplitude")
    plt.title(
        "Kunigami — Blind Angular Symmetry Test\n"
        f"{F_LOW:.1f}–{F_HIGH:.1f} Hz"
    )
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_PREFIX}_SYMMETRY.png",
        dpi=180
    )

    plt.close()


def plot_dominant_order(df):
    counts = [
        (df["Dominant_m"] == m).sum()
        for m in range(1, MAX_SYMMETRY_ORDER + 1)
    ]

    x = np.arange(1, MAX_SYMMETRY_ORDER + 1)

    plt.figure(figsize=(8, 5))
    plt.bar(x, counts)
    plt.xlabel("Dominant symmetry order m")
    plt.ylabel("Number of 60 s windows")
    plt.title(
        "Kunigami — Dominant Shape Symmetry per Window"
    )
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_PREFIX}_DOMINANT_M.png",
        dpi=180
    )

    plt.close()


def plot_fourfold_orientation(df):
    values = df["Phi4_deg"].dropna().values

    plt.figure(figsize=(8, 5))
    plt.hist(values, bins=36)
    plt.xlabel("m=4 orientation (deg, modulo 90°)")
    plt.ylabel("Windows")
    plt.title(
        "Kunigami — Fourfold Orientation Distribution"
    )
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_PREFIX}_M4_ORIENTATION.png",
        dpi=180
    )

    plt.close()


def plot_example_trajectories(example_windows):
    if not example_windows:
        return

    n = min(6, len(example_windows))

    fig, axes = plt.subplots(
        2,
        3,
        figsize=(11, 7)
    )

    axes = axes.ravel()

    for i in range(6):

        ax = axes[i]

        if i >= n:
            ax.axis("off")
            continue

        timestamp, h, d, dominant_m = (
            example_windows[i]
        )

        ax.plot(h, d, linewidth=0.6)

        ax.set_aspect(
            "equal",
            adjustable="box"
        )

        ax.set_title(
            f"{timestamp}\n"
            f"dominant m={dominant_m}"
        )

        ax.set_xlabel("H")
        ax.set_ylabel("D")

    fig.suptitle(
        "Kunigami — Representative H-D Trajectories\n"
        f"{F_LOW:.1f}–{F_HIGH:.1f} Hz"
    )

    fig.tight_layout()

    fig.savefig(
        f"{OUTPUT_PREFIX}_EXAMPLES.png",
        dpi=180
    )

    plt.close(fig)


# ============================================================
# MAIN
# ============================================================

def main():

    warnings.filterwarnings(
        "ignore",
        category=RuntimeWarning
    )

    files, times, h_raw, d_raw = load_all_files()

    print()
    print("Samples:", len(h_raw))
    print("First :", times[0])
    print("Last  :", times[-1])

    finite = (
        np.isfinite(h_raw)
        & np.isfinite(d_raw)
    )

    if np.mean(finite) < 0.99:
        print(
            "WARNING: non-finite values exist in the record."
        )

    # Interpolate isolated invalid points before continuous filtering.
    def fill_invalid(x):
        x = np.asarray(x, dtype=float)

        good = np.isfinite(x)

        if not np.any(good):
            raise ValueError("Channel contains no valid samples.")

        idx = np.arange(len(x))

        return np.interp(
            idx,
            idx[good],
            x[good]
        )

    h_clean = fill_invalid(h_raw)
    d_clean = fill_invalid(d_raw)

    print(
        f"Filtering full continuous record: "
        f"{F_LOW:.3f}–{F_HIGH:.3f} Hz"
    )

    h_f = bandpass_filter(h_clean)
    d_f = bandpass_filter(d_clean)

    total_windows = len(h_f) // WINDOW_SAMPLES

    print(
        "60-second windows:",
        total_windows
    )

    rows = []
    examples = []

    for w in range(total_windows):

        i0 = w * WINDOW_SAMPLES
        i1 = i0 + WINDOW_SAMPLES

        h = h_f[i0:i1]
        d = d_f[i0:i1]

        result = analyse_window(h, d)

        if result is None:
            continue

        result["Window"] = w
        result["UTC"] = str(times[i0])

        rows.append(result)

        if len(examples) < 6:

            hn, dn = common_normalize(h, d)

            examples.append(
                (
                    str(times[i0]),
                    hn,
                    dn,
                    result["Dominant_m"],
                )
            )

        if (w + 1) % 100 == 0:
            print(
                f"Processed {w + 1}/{total_windows}"
            )

    df = pd.DataFrame(rows)

    if df.empty:
        raise RuntimeError(
            "No usable windows were produced."
        )

    summary = make_summary(df)

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    windows_file = (
        f"{OUTPUT_PREFIX}_1MIN.csv"
    )

    summary_file = (
        f"{OUTPUT_PREFIX}_SUMMARY.csv"
    )

    df.to_csv(
        windows_file,
        index=False
    )

    summary.to_csv(
        summary_file,
        index=False
    )

    plot_symmetry_distribution(df)
    plot_dominant_order(df)
    plot_fourfold_orientation(df)
    plot_example_trajectories(examples)

    # --------------------------------------------------------
    # TERMINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("KUNIGAMI BLIND SHAPE ANALYSIS")
    print("=" * 70)

    print(
        f"Band: {F_LOW:.3f}–{F_HIGH:.3f} Hz"
    )

    print(
        f"Usable windows: {len(df)}"
    )

    print(
        f"Median PLV: "
        f"{df['PLV'].median():.6f}"
    )

    print(
        f"Median phase D-H: "
        f"{df['Phase_D_minus_H_deg'].median():.3f} deg"
    )

    print(
        f"Median PCA axis ratio: "
        f"{df['Axis_Ratio'].median():.6f}"
    )

    print()
    print("Median angular harmonic amplitudes:")

    median_amps = {}

    for m in range(
        1,
        MAX_SYMMETRY_ORDER + 1
    ):
        value = df[f"A{m}"].median()

        median_amps[m] = value

        print(
            f"  m={m}: {value:.6f}"
        )

    dominant_global = max(
        median_amps,
        key=median_amps.get
    )

    print()
    print(
        "Strongest median symmetry order:",
        f"m={dominant_global}"
    )

    print()
    print("Dominant order by individual window:")

    counts = (
        df["Dominant_m"]
        .value_counts()
        .sort_index()
    )

    for m in range(
        1,
        MAX_SYMMETRY_ORDER + 1
    ):

        n = int(counts.get(m, 0))

        pct = 100 * n / len(df)

        print(
            f"  m={m}: {n} "
            f"({pct:.2f}%)"
        )

    cw = (df["Rotation"] == "CW").sum()
    ccw = (df["Rotation"] == "CCW").sum()

    print()
    print(
        f"Rotation: CW={cw}, CCW={ccw}"
    )

    if cw + ccw:
        print(
            f"CW={100*cw/(cw+ccw):.2f}%  "
            f"CCW={100*ccw/(cw+ccw):.2f}%"
        )

    orientation, concentration = (
        circular_orientation_result(
            df["Phi4_deg"],
            4
        )
    )

    print()
    print(
        "m=4 mean orientation:",
        f"{orientation:.3f} deg modulo 90 deg"
    )

    print(
        "m=4 orientation concentration:",
        f"{concentration:.6f}"
    )

    print()
    print("Saved:")
    print(" ", windows_file)
    print(" ", summary_file)
    print(
        " ",
        f"{OUTPUT_PREFIX}_SYMMETRY.png"
    )
    print(
        " ",
        f"{OUTPUT_PREFIX}_DOMINANT_M.png"
    )
    print(
        " ",
        f"{OUTPUT_PREFIX}_M4_ORIENTATION.png"
    )
    print(
        " ",
        f"{OUTPUT_PREFIX}_EXAMPLES.png"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()