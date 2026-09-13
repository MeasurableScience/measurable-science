#!/usr/bin/env python3

from pathlib import Path
import re
import math

import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt, hilbert

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

FS = 100.0

F_LOW = 6.8
F_HIGH = 8.2
FILTER_ORDER = 4

# Same type of fixed 60 s window used in the blind search:
WINDOW_START_S = 30 * 60
WINDOW_LENGTH_S = 60.0

# Extra data on both sides before filtering.
FILTER_PAD_S = 10.0

# Raw discontinuity rejection.
# Robust z-score threshold for the largest first difference.
RAW_STEP_Z_THRESHOLD = 25.0

# Eskdalemuir calibration around 6.8–8.2 Hz
V_PER_COUNT_CH1 = 3.491e-6
V_PER_COUNT_CH2 = 3.475e-6

# ~50.205 mV/nT
V_PER_NT = 0.050205

NT_PER_COUNT_CH1 = V_PER_COUNT_CH1 / V_PER_NT
NT_PER_COUNT_CH2 = V_PER_COUNT_CH2 / V_PER_NT


OUT_WINDOWS = "ESK_CLEAN_CARRIER_GEOMETRY.csv"
OUT_SUMMARY = "ESK_CLEAN_CARRIER_GEOMETRY_SUMMARY.csv"

OUT_PHASE_HIST = "ESK_CLEAN_PHASE_DIFFERENCE.png"
OUT_ELLIPTICITY_HIST = "ESK_CLEAN_ELLIPTICITY.png"
OUT_ORIENTATION_HIST = "ESK_CLEAN_ORIENTATION.png"
OUT_PHASE_PLANE = "ESK_CLEAN_PHASE_PLANE_EXAMPLES.png"


# ============================================================
# RAW FILE INDEX
# ============================================================

RAW_RE = re.compile(
    r"CH([12])_(\d{4})_(\d{2})_(\d{2})_(\d{2})\.dat$",
    re.IGNORECASE,
)


def build_raw_index():

    index = {1: {}, 2: {}}

    for path in Path(".").rglob("CH*_*.dat"):

        m = RAW_RE.search(path.name)

        if not m:
            continue

        channel = int(m.group(1))

        ts = pd.Timestamp(
            year=int(m.group(2)),
            month=int(m.group(3)),
            day=int(m.group(4)),
            hour=int(m.group(5)),
        )

        if ts not in index[channel]:
            index[channel][ts] = path

    return index


# ============================================================
# RAW LOADING
# ============================================================

def load_raw(path):

    try:
        x = np.loadtxt(path, dtype=np.float64)
    except Exception:
        return None

    x = np.asarray(x, dtype=np.float64)

    if x.ndim != 1:
        x = x.ravel()

    return x


# ============================================================
# ROBUST RAW-DISCONTINUITY TEST
# ============================================================

def robust_step_score(x):

    """
    Largest first-difference expressed in robust sigma units.

    We do NOT use an expected carrier amplitude.
    This is only a quality-control test for large raw jumps.
    """

    d = np.diff(x)

    if len(d) == 0:
        return np.nan

    centre = np.median(d)

    mad = np.median(
        np.abs(d - centre)
    )

    robust_sigma = 1.4826 * mad

    if robust_sigma <= 0:
        robust_sigma = np.std(d)

    if robust_sigma <= 0:
        return 0.0

    score = np.max(
        np.abs(d - centre)
    ) / robust_sigma

    return float(score)


# ============================================================
# FILTER
# ============================================================

SOS = butter(
    FILTER_ORDER,
    [F_LOW, F_HIGH],
    btype="bandpass",
    fs=FS,
    output="sos",
)


def calibrate(x, channel):

    if channel == 1:
        return x * NT_PER_COUNT_CH1

    return x * NT_PER_COUNT_CH2


# ============================================================
# GEOMETRY / POLARIZATION
# ============================================================

def circular_mean_deg(angle_rad):

    z = np.mean(
        np.exp(1j * angle_rad)
    )

    return math.degrees(
        np.angle(z)
    )


def analyse_geometry(x, y):

    """
    x, y are already band-limited calibrated CH1/CH2 signals.

    No expected circle, ellipse, C-shape or angle is supplied.
    """

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)

    good = np.isfinite(x) & np.isfinite(y)

    x = x[good]
    y = y[good]

    if len(x) < 100:
        return None

    # Remove residual DC numerical offset
    x = x - np.mean(x)
    y = y - np.mean(y)

    # --------------------------------------------------------
    # Vector RMS amplitude
    # --------------------------------------------------------

    vector_rms_nT = math.sqrt(
        np.mean(x*x + y*y)
    )

    ch1_rms_nT = math.sqrt(
        np.mean(x*x)
    )

    ch2_rms_nT = math.sqrt(
        np.mean(y*y)
    )

    # --------------------------------------------------------
    # Analytic signals
    # --------------------------------------------------------

    zx = hilbert(x)
    zy = hilbert(y)

    phase_x = np.angle(zx)
    phase_y = np.angle(zy)

    phase_diff = phase_x - phase_y

    phase_vector = np.mean(
        np.exp(1j * phase_diff)
    )

    phase_plv = abs(phase_vector)

    mean_phase_difference_deg = math.degrees(
        np.angle(phase_vector)
    )

    # --------------------------------------------------------
    # PCA geometry
    # --------------------------------------------------------

    M = np.column_stack([x, y])

    cov = np.cov(
        M,
        rowvar=False,
    )

    eigvals, eigvecs = np.linalg.eigh(cov)

    order = np.argsort(eigvals)[::-1]

    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    major_sigma = math.sqrt(
        max(eigvals[0], 0.0)
    )

    minor_sigma = math.sqrt(
        max(eigvals[1], 0.0)
    )

    if major_sigma > 0:
        pca_ratio = minor_sigma / major_sigma
    else:
        pca_ratio = np.nan

    major_vec = eigvecs[:, 0]

    pca_axis_deg = math.degrees(
        math.atan2(
            major_vec[1],
            major_vec[0],
        )
    )

    # Axis orientation is equivalent modulo 180 degrees.
    pca_axis_deg = (
        (pca_axis_deg + 90.0) % 180.0
    ) - 90.0

    # --------------------------------------------------------
    # Polarization ellipse using analytic complex components
    #
    # Stokes-like parameters:
    # --------------------------------------------------------

    Cxx = np.mean(
        np.abs(zx) ** 2
    )

    Cyy = np.mean(
        np.abs(zy) ** 2
    )

    Cxy = np.mean(
        zx * np.conj(zy)
    )

    S0 = Cxx + Cyy
    S1 = Cxx - Cyy
    S2 = 2.0 * np.real(Cxy)
    S3 = -2.0 * np.imag(Cxy)

    if S0 > 0:

        s3_norm = np.clip(
            S3 / S0,
            -1.0,
            1.0,
        )

        orientation_rad = 0.5 * math.atan2(
            S2,
            S1,
        )

        ellipticity_angle_rad = (
            0.5 * math.asin(s3_norm)
        )

        ellipticity_ratio = abs(
            math.tan(
                ellipticity_angle_rad
            )
        )

        orientation_deg = math.degrees(
            orientation_rad
        )

        ellipticity_angle_deg = math.degrees(
            ellipticity_angle_rad
        )

    else:

        orientation_deg = np.nan
        ellipticity_angle_deg = np.nan
        ellipticity_ratio = np.nan

    # --------------------------------------------------------
    # Signed phase-plane area
    # --------------------------------------------------------

    signed_area = 0.5 * np.sum(
        x[:-1] * y[1:]
        -
        x[1:] * y[:-1]
    )

    if signed_area > 0:
        rotation = "CCW"
    elif signed_area < 0:
        rotation = "CW"
    else:
        rotation = "ZERO"

    return {
        "vector_rms_nT": vector_rms_nT,
        "ch1_rms_nT": ch1_rms_nT,
        "ch2_rms_nT": ch2_rms_nT,

        "phase_plv": phase_plv,
        "mean_phase_difference_deg":
            mean_phase_difference_deg,

        "pca_major_sigma_nT": major_sigma,
        "pca_minor_sigma_nT": minor_sigma,
        "pca_minor_major_ratio": pca_ratio,
        "pca_major_axis_deg": pca_axis_deg,

        "polarization_orientation_deg":
            orientation_deg,

        "ellipticity_angle_deg":
            ellipticity_angle_deg,

        "ellipticity_ratio":
            ellipticity_ratio,

        "signed_phase_plane_area_nT2":
            signed_area,

        "rotation":
            rotation,
    }


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("Indexing raw files...")

    index = build_raw_index()

    paired = sorted(
        set(index[1]) &
        set(index[2])
    )

    print()
    print("==============================================")
    print("ESKDALEMUIR CLEAN CARRIER GEOMETRY")
    print("==============================================")
    print(f"Band               : {F_LOW:.1f}-{F_HIGH:.1f} Hz")
    print(f"Sampling rate      : {FS:.1f} Hz")
    print(f"Window             : 60 s at minute 30")
    print(f"Raw step threshold : {RAW_STEP_Z_THRESHOLD:.1f} robust sigma")
    print(f"CH1 hourly files   : {len(index[1])}")
    print(f"CH2 hourly files   : {len(index[2])}")
    print(f"Paired hours       : {len(paired)}")

    if paired:
        print(f"First paired hour  : {paired[0]}")
        print(f"Last paired hour   : {paired[-1]}")

    print("==============================================")
    print()

    pad_n = int(
        round(FILTER_PAD_S * FS)
    )

    start_n = int(
        round(WINDOW_START_S * FS)
    )

    window_n = int(
        round(WINDOW_LENGTH_S * FS)
    )

    segment_start = start_n - pad_n
    segment_stop = start_n + window_n + pad_n

    rows = []

    example_trajectories = []

    rejected_step = 0
    rejected_length = 0
    rejected_filter = 0

    total = len(paired)

    for k, hour in enumerate(paired, start=1):

        x1 = load_raw(
            index[1][hour]
        )

        x2 = load_raw(
            index[2][hour]
        )

        if (
            x1 is None
            or x2 is None
            or len(x1) != len(x2)
            or len(x1) < segment_stop
        ):
            rejected_length += 1
            continue

        raw1 = x1[
            segment_start:segment_stop
        ]

        raw2 = x2[
            segment_start:segment_stop
        ]

        step_z1 = robust_step_score(raw1)
        step_z2 = robust_step_score(raw2)

        max_step_z = max(
            step_z1,
            step_z2,
        )

        # Objective removal of raw-discontinuity contaminated windows
        if (
            not np.isfinite(max_step_z)
            or max_step_z > RAW_STEP_Z_THRESHOLD
        ):
            rejected_step += 1
            continue

        # Calibration is valid here because filtering is specifically
        # limited to the 6.8–8.2 Hz region.
        n1 = calibrate(
            raw1,
            1,
        )

        n2 = calibrate(
            raw2,
            2,
        )

        try:
            f1 = sosfiltfilt(
                SOS,
                n1,
            )

            f2 = sosfiltfilt(
                SOS,
                n2,
            )

        except Exception:
            rejected_filter += 1
            continue

        # Remove the 10 s filter padding.
        f1 = f1[
            pad_n:pad_n + window_n
        ]

        f2 = f2[
            pad_n:pad_n + window_n
        ]

        metrics = analyse_geometry(
            f1,
            f2,
        )

        if metrics is None:
            rejected_filter += 1
            continue

        window_time = (
            hour
            + pd.Timedelta(
                seconds=WINDOW_START_S
            )
        )

        row = {
            "window_time_utc": window_time,
            "raw_step_z_ch1": step_z1,
            "raw_step_z_ch2": step_z2,
            "raw_step_z_max": max_step_z,
        }

        row.update(metrics)

        rows.append(row)

        # Keep a small, deterministic sample for plotting.
        if len(example_trajectories) < 40:

            xx = f1 - np.mean(f1)
            yy = f2 - np.mean(f2)

            scale = math.sqrt(
                np.mean(
                    xx*xx + yy*yy
                )
            )

            if scale > 0:
                xx = xx / scale
                yy = yy / scale

                example_trajectories.append(
                    (window_time, xx, yy)
                )

        if k % 250 == 0:
            print(
                f"{k:5d}/{total} paired hours"
            )

    df = pd.DataFrame(rows)

    df.to_csv(
        OUT_WINDOWS,
        index=False,
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary_rows = []

    def add_summary(name):

        if name not in df.columns:
            return

        s = pd.to_numeric(
            df[name],
            errors="coerce",
        )

        s = s[
            np.isfinite(s)
        ]

        if len(s) == 0:
            return

        summary_rows.append({
            "quantity": name,
            "N": len(s),
            "mean": float(np.mean(s)),
            "median": float(np.median(s)),
            "std": float(np.std(s)),
            "q05": float(np.quantile(s, 0.05)),
            "q25": float(np.quantile(s, 0.25)),
            "q75": float(np.quantile(s, 0.75)),
            "q95": float(np.quantile(s, 0.95)),
        })

    for quantity in [
        "vector_rms_nT",
        "phase_plv",
        "mean_phase_difference_deg",
        "pca_minor_major_ratio",
        "pca_major_axis_deg",
        "polarization_orientation_deg",
        "ellipticity_angle_deg",
        "ellipticity_ratio",
    ]:
        add_summary(quantity)

    summary_df = pd.DataFrame(
        summary_rows
    )

    summary_df.to_csv(
        OUT_SUMMARY,
        index=False,
    )

    # ========================================================
    # PLOTS
    # ========================================================

    if len(df):

        # Phase difference
        plt.figure(figsize=(8, 5))

        plt.hist(
            df[
                "mean_phase_difference_deg"
            ].dropna(),
            bins=72,
        )

        plt.xlabel(
            "Mean CH1–CH2 phase difference (deg)"
        )
        plt.ylabel("60 s windows")

        plt.title(
            "Eskdalemuir clean 6.8–8.2 Hz\n"
            "CH1–CH2 phase difference"
        )

        plt.tight_layout()
        plt.savefig(
            OUT_PHASE_HIST,
            dpi=180,
        )
        plt.close()

        # Ellipticity
        plt.figure(figsize=(8, 5))

        plt.hist(
            df[
                "ellipticity_ratio"
            ].dropna(),
            bins=60,
        )

        plt.xlabel(
            "Polarization ellipticity |minor/major|"
        )
        plt.ylabel("60 s windows")

        plt.title(
            "Eskdalemuir clean 6.8–8.2 Hz\n"
            "Polarization ellipticity"
        )

        plt.tight_layout()
        plt.savefig(
            OUT_ELLIPTICITY_HIST,
            dpi=180,
        )
        plt.close()

        # Orientation
        plt.figure(figsize=(8, 5))

        plt.hist(
            df[
                "polarization_orientation_deg"
            ].dropna(),
            bins=72,
        )

        plt.xlabel(
            "Polarization major-axis orientation (deg)"
        )
        plt.ylabel("60 s windows")

        plt.title(
            "Eskdalemuir clean 6.8–8.2 Hz\n"
            "Polarization orientation"
        )

        plt.tight_layout()
        plt.savefig(
            OUT_ORIENTATION_HIST,
            dpi=180,
        )
        plt.close()

    # Example normalized trajectories
    if example_trajectories:

        plt.figure(figsize=(8, 8))

        for timestamp, xx, yy in example_trajectories:

            # Downsample only for drawing.
            step = 5

            plt.plot(
                xx[::step],
                yy[::step],
                linewidth=0.6,
                alpha=0.18,
            )

        plt.axhline(
            0,
            linewidth=0.5,
        )

        plt.axvline(
            0,
            linewidth=0.5,
        )

        plt.xlabel(
            "CH1 normalized"
        )

        plt.ylabel(
            "CH2 normalized"
        )

        plt.title(
            "Eskdalemuir clean 6.8–8.2 Hz\n"
            "Example CH1–CH2 trajectories"
        )

        plt.axis("equal")
        plt.tight_layout()

        plt.savefig(
            OUT_PHASE_PLANE,
            dpi=180,
        )

        plt.close()

    # ========================================================
    # TERMINAL SUMMARY
    # ========================================================

    print()
    print("==============================================")
    print("CLEAN CARRIER GEOMETRY COMPLETE")
    print("==============================================")
    print(f"Paired hours examined : {total}")
    print(f"Accepted clean windows: {len(df)}")
    print(f"Rejected raw steps    : {rejected_step}")
    print(f"Rejected length/data  : {rejected_length}")
    print(f"Rejected filtering    : {rejected_filter}")
    print()

    if len(df):

        print(
            "Median vector RMS       : "
            f"{df['vector_rms_nT'].median():.9g} nT"
        )

        print(
            "Median phase PLV        : "
            f"{df['phase_plv'].median():.6f}"
        )

        print(
            "Median phase difference : "
            f"{df['mean_phase_difference_deg'].median():.3f} deg"
        )

        print(
            "Median PCA minor/major  : "
            f"{df['pca_minor_major_ratio'].median():.6f}"
        )

        print(
            "Median ellipticity      : "
            f"{df['ellipticity_ratio'].median():.6f}"
        )

        print(
            "Median orientation      : "
            f"{df['polarization_orientation_deg'].median():.3f} deg"
        )

        cw = int(
            np.sum(
                df["rotation"] == "CW"
            )
        )

        ccw = int(
            np.sum(
                df["rotation"] == "CCW"
            )
        )

        zero = int(
            np.sum(
                df["rotation"] == "ZERO"
            )
        )

        print(
            f"Rotation CW/CCW/ZERO    : "
            f"{cw}/{ccw}/{zero}"
        )

        # Useful generic descriptive fractions,
        # not shape assumptions.
        linear_fraction = np.mean(
            df["ellipticity_ratio"] < 0.2
        )

        circular_fraction = np.mean(
            df["ellipticity_ratio"] > 0.8
        )

        print(
            "Ellipticity < 0.20      : "
            f"{100*linear_fraction:.2f}%"
        )

        print(
            "Ellipticity > 0.80      : "
            f"{100*circular_fraction:.2f}%"
        )

    print()
    print("Created:")
    print(f"  {OUT_WINDOWS}")
    print(f"  {OUT_SUMMARY}")
    print(f"  {OUT_PHASE_HIST}")
    print(f"  {OUT_ELLIPTICITY_HIST}")
    print(f"  {OUT_ORIENTATION_HIST}")
    print(f"  {OUT_PHASE_PLANE}")
    print("==============================================")


if __name__ == "__main__":
    main()