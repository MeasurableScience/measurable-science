#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kunigami — cycle-resolved H-D shape reconstruction

Goal:
Reconstruct the average local H-D trajectory of one oscillation cycle
inside the previously blind-detected 7.9–8.1 Hz band.

The program is NOT told to search for a square or quadrilateral.

Method:
- read all 24 KNG CDF files
- concatenate full day
- band-pass 7.9–8.1 Hz
- obtain instantaneous phase from analytic signal
- divide data into individual cycles
- resample every cycle to the same phase grid
- group 16 consecutive cycles
- average their H-D trajectory
- measure:
    * PCA axis ratio
    * radial harmonics m=1..6
    * A2
    * A4
    * A4/A2
    * dominant symmetry
- save representative reconstructed cycles

This avoids overlaying ~480 cycles inside one 60-second window.
"""

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import butter, sosfiltfilt, hilbert
from cdflib import CDF, cdfepoch


# ============================================================
# SETTINGS
# ============================================================

DATA_DIR = "."
FILE_PATTERN = "isee_induction_kng_20220101*_v01.cdf"

FS = 64.0

F_LOW = 7.9
F_HIGH = 8.1

FILTER_ORDER = 4

# Number of phase points used to represent one reconstructed cycle
PHASE_POINTS = 64

# Average this many consecutive cycles together
CYCLES_PER_GROUP = 16

MAX_SYMMETRY_ORDER = 6

OUTPUT_PREFIX = "KNG_CYCLE_SHAPE"


# ============================================================
# LOAD DATA
# ============================================================

def read_cdf(path):

    cdf = CDF(path)

    epoch = np.asarray(
        cdf.varget("epoch_db_dt")
    )

    data = np.asarray(
        cdf.varget("db_dt"),
        dtype=float
    )

    times = np.asarray(
        cdfepoch.to_datetime(epoch)
    )

    h = data[:, 0]
    d = data[:, 1]

    return times, h, d


def load_all():

    files = sorted(
        glob.glob(
            os.path.join(
                DATA_DIR,
                FILE_PATTERN
            )
        )
    )

    if not files:
        raise FileNotFoundError(
            f"No files found: {FILE_PATTERN}"
        )

    print("Files:", len(files))

    T = []
    H = []
    D = []

    for i, path in enumerate(files, 1):

        print(
            f"[{i:02d}/{len(files):02d}]",
            os.path.basename(path)
        )

        t, h, d = read_cdf(path)

        T.append(t)
        H.append(h)
        D.append(d)

    t = np.concatenate(T)
    h = np.concatenate(H)
    d = np.concatenate(D)

    order = np.argsort(t)

    return (
        t[order],
        h[order],
        d[order]
    )


# ============================================================
# FILTER
# ============================================================

def fill_invalid(x):

    x = np.asarray(x, dtype=float)

    good = np.isfinite(x)

    idx = np.arange(len(x))

    return np.interp(
        idx,
        idx[good],
        x[good]
    )


def bandpass(x):

    sos = butter(
        FILTER_ORDER,
        [F_LOW, F_HIGH],
        btype="bandpass",
        fs=FS,
        output="sos"
    )

    return sosfiltfilt(
        sos,
        x
    )


# ============================================================
# PHASE-BASED CYCLE EXTRACTION
# ============================================================

def get_cycle_boundaries(reference):

    analytic = hilbert(reference)

    phase = np.unwrap(
        np.angle(analytic)
    )

    cycle_number = np.floor(
        (phase - phase[0]) / (2*np.pi)
    ).astype(int)

    jumps = np.where(
        np.diff(cycle_number) > 0
    )[0] + 1

    return jumps


def resample_cycle(h, d):

    n = len(h)

    if n < 5:
        return None

    old_phase = np.linspace(
        0,
        1,
        n,
        endpoint=False
    )

    new_phase = np.linspace(
        0,
        1,
        PHASE_POINTS,
        endpoint=False
    )

    hr = np.interp(
        new_phase,
        old_phase,
        h
    )

    dr = np.interp(
        new_phase,
        old_phase,
        d
    )

    return hr, dr


# ============================================================
# GEOMETRY
# ============================================================

def common_normalize(h, d):

    h = h - np.mean(h)
    d = d - np.mean(d)

    scale = np.sqrt(
        np.mean(
            h*h + d*d
        )
    )

    if scale <= 0:
        return None, None

    return h/scale, d/scale


def pca_axis_ratio(h, d):

    xy = np.column_stack(
        [h, d]
    )

    cov = np.cov(
        xy,
        rowvar=False
    )

    vals, vecs = np.linalg.eigh(cov)

    vals = np.sort(vals)[::-1]

    if vals[0] <= 0:
        return np.nan

    return np.sqrt(
        max(vals[1], 0)
        / vals[0]
    )


def radial_profile(h, d):

    theta = np.mod(
        np.arctan2(d, h),
        2*np.pi
    )

    r = np.sqrt(
        h*h + d*d
    )

    order = np.argsort(theta)

    theta = theta[order]
    r = r[order]

    target_theta = np.linspace(
        0,
        2*np.pi,
        360,
        endpoint=False
    )

    theta_ext = np.concatenate([
        theta - 2*np.pi,
        theta,
        theta + 2*np.pi
    ])

    r_ext = np.tile(
        r,
        3
    )

    profile = np.interp(
        target_theta,
        theta_ext,
        r_ext
    )

    profile /= np.mean(profile)

    return target_theta, profile


def harmonics(theta, r):

    amps = {}

    for m in range(
        1,
        MAX_SYMMETRY_ORDER + 1
    ):

        z = np.mean(
            r *
            np.exp(
                -1j*m*theta
            )
        )

        amps[m] = abs(z)

    return amps


# ============================================================
# MAIN
# ============================================================

def main():

    times, h_raw, d_raw = load_all()

    print()
    print("Samples:", len(h_raw))
    print("First:", times[0])
    print("Last :", times[-1])

    h_raw = fill_invalid(h_raw)
    d_raw = fill_invalid(d_raw)

    print()
    print(
        f"Filtering {F_LOW:.1f}-{F_HIGH:.1f} Hz"
    )

    h = bandpass(h_raw)
    d = bandpass(d_raw)

    # use H as phase reference
    boundaries = get_cycle_boundaries(h)

    print(
        "Detected cycles:",
        len(boundaries) - 1
    )

    cycles = []

    for i in range(
        len(boundaries) - 1
    ):

        i0 = boundaries[i]
        i1 = boundaries[i+1]

        hc = h[i0:i1]
        dc = d[i0:i1]

        out = resample_cycle(
            hc,
            dc
        )

        if out is not None:
            cycles.append(
                (
                    times[i0],
                    out[0],
                    out[1]
                )
            )

    print(
        "Usable cycles:",
        len(cycles)
    )

    rows = []
    examples = []

    n_groups = (
        len(cycles)
        // CYCLES_PER_GROUP
    )

    print(
        "Cycle groups:",
        n_groups
    )

    for g in range(n_groups):

        block = cycles[
            g*CYCLES_PER_GROUP:
            (g+1)*CYCLES_PER_GROUP
        ]

        H = np.stack(
            [x[1] for x in block]
        )

        D = np.stack(
            [x[2] for x in block]
        )

        # average phase-aligned cycles
        hm = np.mean(
            H,
            axis=0
        )

        dm = np.mean(
            D,
            axis=0
        )

        hn, dn = common_normalize(
            hm,
            dm
        )

        if hn is None:
            continue

        axis_ratio = pca_axis_ratio(
            hn,
            dn
        )

        theta, r = radial_profile(
            hn,
            dn
        )

        amps = harmonics(
            theta,
            r
        )

        dominant_m = max(
            amps,
            key=amps.get
        )

        A2 = amps[2]
        A4 = amps[4]

        ratio = (
            A4 / A2
            if A2 > 0
            else np.nan
        )

        row = {
            "UTC": str(block[0][0]),
            "Group": g,
            "Cycles": CYCLES_PER_GROUP,
            "Axis_Ratio": axis_ratio,
            "A2": A2,
            "A4": A4,
            "A4_over_A2": ratio,
            "Dominant_m": dominant_m
        }

        for m in range(
            1,
            MAX_SYMMETRY_ORDER + 1
        ):
            row[f"A{m}"] = amps[m]

        rows.append(row)

        if len(examples) < 12:

            examples.append(
                (
                    str(block[0][0]),
                    hn.copy(),
                    dn.copy(),
                    dominant_m,
                    A2,
                    A4,
                    ratio
                )
            )

    df = pd.DataFrame(rows)

    if df.empty:
        raise RuntimeError(
            "No groups analysed."
        )

    df.to_csv(
        f"{OUTPUT_PREFIX}_GROUPS.csv",
        index=False
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary = {
        "Groups": len(df),
        "Cycles_Per_Group":
            CYCLES_PER_GROUP,
        "Median_Axis_Ratio":
            df["Axis_Ratio"].median(),
        "Median_A2":
            df["A2"].median(),
        "Median_A4":
            df["A4"].median(),
        "Median_A4_over_A2":
            df["A4_over_A2"].median(),
    }

    for m in range(
        1,
        MAX_SYMMETRY_ORDER + 1
    ):

        count = int(
            (df["Dominant_m"] == m).sum()
        )

        summary[
            f"Dominant_m{m}_Count"
        ] = count

        summary[
            f"Dominant_m{m}_Percent"
        ] = (
            100.0 *
            count /
            len(df)
        )

    pd.DataFrame(
        [summary]
    ).to_csv(
        f"{OUTPUT_PREFIX}_SUMMARY.csv",
        index=False
    )

    # ========================================================
    # EXAMPLE SHAPES
    # ========================================================

    fig, axes = plt.subplots(
        3,
        4,
        figsize=(12, 10)
    )

    axes = axes.ravel()

    for i, ax in enumerate(axes):

        if i >= len(examples):
            ax.axis("off")
            continue

        utc, hn, dn, m, a2, a4, ratio = (
            examples[i]
        )

        ax.plot(
            hn,
            dn,
            linewidth=1.2
        )

        ax.set_aspect(
            "equal",
            adjustable="box"
        )

        ax.set_title(
            f"{utc}\n"
            f"m={m}  "
            f"A2={a2:.3f}  "
            f"A4={a4:.3f}\n"
            f"A4/A2={ratio:.2f}"
        )

        ax.set_xlabel("H")
        ax.set_ylabel("D")

    fig.suptitle(
        "Kunigami — Phase-Aligned Average Cycle Shapes\n"
        f"{F_LOW:.1f}-{F_HIGH:.1f} Hz, "
        f"{CYCLES_PER_GROUP} cycles/group"
    )

    fig.tight_layout()

    fig.savefig(
        f"{OUTPUT_PREFIX}_EXAMPLES.png",
        dpi=180
    )

    plt.close(fig)

    # ========================================================
    # HARMONIC DISTRIBUTION
    # ========================================================

    medians = [
        df[f"A{m}"].median()
        for m in range(
            1,
            MAX_SYMMETRY_ORDER + 1
        )
    ]

    plt.figure(
        figsize=(8,5)
    )

    plt.bar(
        range(
            1,
            MAX_SYMMETRY_ORDER + 1
        ),
        medians
    )

    plt.xlabel(
        "Symmetry order m"
    )

    plt.ylabel(
        "Median radial harmonic amplitude"
    )

    plt.title(
        "Kunigami — Cycle-Resolved Shape Symmetry"
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_PREFIX}_SYMMETRY.png",
        dpi=180
    )

    plt.close()

    # ========================================================
    # TERMINAL
    # ========================================================

    print()
    print("=" * 70)
    print(
        "KUNIGAMI CYCLE-RESOLVED SHAPE"
    )
    print("=" * 70)

    print(
        "Groups:",
        len(df)
    )

    print(
        "Cycles/group:",
        CYCLES_PER_GROUP
    )

    print()
    print(
        "Median axis ratio:",
        f"{df['Axis_Ratio'].median():.6f}"
    )

    print(
        "Median A2:",
        f"{df['A2'].median():.6f}"
    )

    print(
        "Median A4:",
        f"{df['A4'].median():.6f}"
    )

    print(
        "Median A4/A2:",
        f"{df['A4_over_A2'].median():.6f}"
    )

    print()
    print(
        "Dominant symmetry by group:"
    )

    for m in range(
        1,
        MAX_SYMMETRY_ORDER + 1
    ):

        n = int(
            (df["Dominant_m"] == m).sum()
        )

        pct = (
            100.0*n/len(df)
        )

        print(
            f"m={m}: "
            f"{n} "
            f"({pct:.2f}%)"
        )

    print()
    print("Saved:")
    print(
        f"  {OUTPUT_PREFIX}_GROUPS.csv"
    )
    print(
        f"  {OUTPUT_PREFIX}_SUMMARY.csv"
    )
    print(
        f"  {OUTPUT_PREFIX}_EXAMPLES.png"
    )
    print(
        f"  {OUTPUT_PREFIX}_SYMMETRY.png"
    )

    print("=" * 70)


if __name__ == "__main__":
    main()