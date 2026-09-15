#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kunigami — synthetic ellipse null test

Purpose
-------
Test whether the cycle-resolved geometry algorithm itself generates
a substantial m=4 component from a simple two-component sinusoidal
ellipse.

No quadrilateral structure is inserted.

The synthetic H-D signal contains:
    H(t) = cos(phase)
    D(t) = r * cos(phase + delta)

where r and delta vary over broad ranges.

For every synthetic ellipse the same radial-profile / harmonic
measurement used for the Kunigami cycle reconstruction is applied.

The observed Kunigami result is NOT used to construct the synthetic
signals. It is shown only after the null distribution has been made.

Observed KNG cycle result:
    median axis ratio = 0.289825
    median A2         = 0.284080
    median A4         = 0.122290
    median A4/A2      = 0.431722
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

SEED = 20260915
N_SYNTHETIC = 100000
PHASE_POINTS = 64
MAX_SYMMETRY_ORDER = 6

OUTPUT_PREFIX = "KNG_SYNTHETIC_NULL"

# Observed values — comparison only
OBS_AXIS_RATIO = 0.289825
OBS_A2 = 0.284080
OBS_A4 = 0.122290
OBS_RATIO = 0.431722


# ============================================================
# SAME GEOMETRY FUNCTIONS AS REAL TEST
# ============================================================

def common_normalize(h, d):

    h = h - np.mean(h)
    d = d - np.mean(d)

    scale = np.sqrt(
        np.mean(h*h + d*d)
    )

    if scale <= 0:
        return None, None

    return h / scale, d / scale


def pca_axis_ratio(h, d):

    xy = np.column_stack([h, d])

    cov = np.cov(
        xy,
        rowvar=False
    )

    vals = np.linalg.eigvalsh(cov)
    vals = np.sort(vals)[::-1]

    if vals[0] <= 0:
        return np.nan

    return np.sqrt(
        max(vals[1], 0.0) / vals[0]
    )


def radial_profile(h, d):

    theta = np.mod(
        np.arctan2(d, h),
        2*np.pi
    )

    r = np.sqrt(h*h + d*d)

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

    r_ext = np.tile(r, 3)

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
            r * np.exp(-1j*m*theta)
        )

        amps[m] = abs(z)

    return amps


# ============================================================
# SYNTHETIC NULL
# ============================================================

rng = np.random.default_rng(SEED)

phase = np.linspace(
    0,
    2*np.pi,
    PHASE_POINTS,
    endpoint=False
)

rows = []

print("=" * 72)
print("KUNIGAMI — SYNTHETIC ELLIPSE NULL")
print("=" * 72)
print("Synthetic ellipses:", N_SYNTHETIC)
print("No m=4 / quadrilateral term is inserted.")
print()

for i in range(N_SYNTHETIC):

    # Independent amplitude ratio.
    # Broad range intentionally covers nearly equal components
    # through strongly flattened trajectories.
    amplitude_ratio = rng.uniform(
        0.15,
        1.0
    )

    # Broad phase relation.
    # Avoid exact 0/180 singular straight lines.
    delta_deg = rng.uniform(
        5.0,
        175.0
    )

    delta = np.radians(delta_deg)

    h = np.cos(phase)

    d = (
        amplitude_ratio *
        np.cos(phase + delta)
    )

    hn, dn = common_normalize(h, d)

    axis_ratio = pca_axis_ratio(
        hn,
        dn
    )

    theta, radial = radial_profile(
        hn,
        dn
    )

    amps = harmonics(
        theta,
        radial
    )

    a2 = amps[2]
    a4 = amps[4]

    ratio = (
        a4 / a2
        if a2 > 1e-12
        else np.nan
    )

    dominant_m = max(
        amps,
        key=amps.get
    )

    rows.append({
        "Amplitude_Ratio": amplitude_ratio,
        "Phase_Difference_deg": delta_deg,
        "Axis_Ratio": axis_ratio,
        "A1": amps[1],
        "A2": amps[2],
        "A3": amps[3],
        "A4": amps[4],
        "A5": amps[5],
        "A6": amps[6],
        "A4_over_A2": ratio,
        "Dominant_m": dominant_m,
    })

    if (i + 1) % 10000 == 0:
        print(
            f"Processed {i+1}/{N_SYNTHETIC}"
        )


df = pd.DataFrame(rows)

df.to_csv(
    f"{OUTPUT_PREFIX}.csv",
    index=False
)


# ============================================================
# MATCH REAL KNG FLATTENING
# ============================================================

# Compare the real result especially with synthetic ellipses
# having similar PCA axis ratio.

tol = 0.02

matched = df[
    np.abs(
        df["Axis_Ratio"]
        - OBS_AXIS_RATIO
    ) <= tol
].copy()


# ============================================================
# SUMMARY
# ============================================================

def percentile_of_observation(series, observed):

    x = np.asarray(
        series.dropna(),
        dtype=float
    )

    return (
        100.0 *
        np.mean(x <= observed)
    )


all_ratio_percentile = percentile_of_observation(
    df["A4_over_A2"],
    OBS_RATIO
)

if len(matched):

    matched_ratio_percentile = (
        percentile_of_observation(
            matched["A4_over_A2"],
            OBS_RATIO
        )
    )

    matched_a4_percentile = (
        percentile_of_observation(
            matched["A4"],
            OBS_A4
        )
    )

else:

    matched_ratio_percentile = np.nan
    matched_a4_percentile = np.nan


summary = {
    "Synthetic_Count":
        len(df),

    "Observed_KNG_Axis_Ratio":
        OBS_AXIS_RATIO,

    "Observed_KNG_A2":
        OBS_A2,

    "Observed_KNG_A4":
        OBS_A4,

    "Observed_KNG_A4_over_A2":
        OBS_RATIO,

    "Synthetic_Median_Axis_Ratio":
        df["Axis_Ratio"].median(),

    "Synthetic_Median_A2":
        df["A2"].median(),

    "Synthetic_Median_A4":
        df["A4"].median(),

    "Synthetic_Median_A4_over_A2":
        df["A4_over_A2"].median(),

    "Observed_Ratio_Percentile_All_Ellipses":
        all_ratio_percentile,

    "Matched_Axis_Tolerance":
        tol,

    "Matched_Ellipse_Count":
        len(matched),

    "Matched_Median_A2":
        matched["A2"].median()
        if len(matched) else np.nan,

    "Matched_Median_A4":
        matched["A4"].median()
        if len(matched) else np.nan,

    "Matched_Median_A4_over_A2":
        matched["A4_over_A2"].median()
        if len(matched) else np.nan,

    "Observed_A4_Percentile_Matched":
        matched_a4_percentile,

    "Observed_Ratio_Percentile_Matched":
        matched_ratio_percentile,
}

pd.DataFrame(
    [summary]
).to_csv(
    f"{OUTPUT_PREFIX}_SUMMARY.csv",
    index=False
)


# ============================================================
# DOMINANT ORDERS
# ============================================================

counts = (
    df["Dominant_m"]
    .value_counts()
    .sort_index()
)

print()
print("Dominant symmetry in synthetic ellipses:")

for m in range(1, 7):

    n = int(counts.get(m, 0))

    print(
        f"  m={m}: {n} "
        f"({100*n/len(df):.2f}%)"
    )


# ============================================================
# PLOT — MATCHED ELLIPSES
# ============================================================

if len(matched):

    plt.figure(figsize=(9, 6))

    plt.hist(
        matched["A4_over_A2"]
            .replace([np.inf, -np.inf], np.nan)
            .dropna(),
        bins=70
    )

    plt.axvline(
        OBS_RATIO,
        linestyle="--",
        linewidth=2,
        label=f"KNG observed = {OBS_RATIO:.3f}"
    )

    plt.xlabel("A4 / A2")
    plt.ylabel("Synthetic ellipses")

    plt.title(
        "Kunigami Null Test — Ordinary Ellipses\n"
        f"matched axis ratio "
        f"{OBS_AXIS_RATIO:.3f} ± {tol:.2f}"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_PREFIX}_MATCHED_RATIO.png",
        dpi=180
    )

    plt.close()


# ============================================================
# TERMINAL REPORT
# ============================================================

print()
print("=" * 72)
print("RESULT")
print("=" * 72)

print()
print("REAL KUNIGAMI:")
print(
    f"  Axis ratio : {OBS_AXIS_RATIO:.6f}"
)
print(
    f"  A2         : {OBS_A2:.6f}"
)
print(
    f"  A4         : {OBS_A4:.6f}"
)
print(
    f"  A4/A2      : {OBS_RATIO:.6f}"
)

print()
print("ALL SYNTHETIC ELLIPSES:")
print(
    "  Median A2    :",
    f"{df['A2'].median():.6f}"
)
print(
    "  Median A4    :",
    f"{df['A4'].median():.6f}"
)
print(
    "  Median A4/A2 :",
    f"{df['A4_over_A2'].median():.6f}"
)

print()
print(
    f"MATCHED ELLIPSES "
    f"(axis ratio {OBS_AXIS_RATIO:.3f} ± {tol:.2f}):"
)
print(
    "  Count:",
    len(matched)
)

if len(matched):

    print(
        "  Median axis ratio:",
        f"{matched['Axis_Ratio'].median():.6f}"
    )

    print(
        "  Median A2:",
        f"{matched['A2'].median():.6f}"
    )

    print(
        "  Median A4:",
        f"{matched['A4'].median():.6f}"
    )

    print(
        "  Median A4/A2:",
        f"{matched['A4_over_A2'].median():.6f}"
    )

    print()
    print(
        "Observed KNG A4 percentile "
        "within matched ellipses:",
        f"{matched_a4_percentile:.2f}%"
    )

    print(
        "Observed KNG A4/A2 percentile "
        "within matched ellipses:",
        f"{matched_ratio_percentile:.2f}%"
    )

print()
print("Saved:")
print(
    f"  {OUTPUT_PREFIX}.csv"
)
print(
    f"  {OUTPUT_PREFIX}_SUMMARY.csv"
)

if len(matched):
    print(
        f"  {OUTPUT_PREFIX}_MATCHED_RATIO.png"
    )

print("=" * 72)