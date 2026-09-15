#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Kunigami — flattened quadrilateral geometry test

This script does NOT assume that the measured shape is a square
or quadrilateral.

It uses the already completed blind H-D shape analysis and measures
the simultaneous presence of:

    A2 = twofold component     -> elongation / flattening
    A4 = fourfold component    -> fourfold deformation

It also measures whether the orientations of the m=2 and m=4
components maintain an organized relationship.

Input:
    KNG_SHAPE_1MIN.csv

Outputs:
    KNG_QUAD_1MIN.csv
    KNG_QUAD_SUMMARY.csv
    KNG_QUAD_A2_A4_SCATTER.png
    KNG_QUAD_RATIO.png
    KNG_QUAD_JOINT.png
    KNG_QUAD_PHASE_RELATION.png
    KNG_QUAD_TOP_WINDOWS.csv
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


INPUT_FILE = "KNG_SHAPE_1MIN.csv"

OUTPUT_PREFIX = "KNG_QUAD"


# ============================================================
# HELPERS
# ============================================================

def circular_difference_mod90(a, b):
    """
    Smallest signed angular difference between two orientations
    where 90-degree rotations are equivalent.

    Result range:
        -45 ... +45 degrees
    """

    d = (a - b + 45.0) % 90.0 - 45.0
    return d


def circular_concentration_mod90(values_deg):
    """
    Circular concentration for an orientation variable with
    90-degree periodicity.

    1.0 = perfectly concentrated
    0.0 = uniformly distributed
    """

    values = np.asarray(values_deg, dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.nan

    # 90-degree periodicity -> multiply angle by 4
    phi = np.radians(values * 4.0)

    z = np.mean(np.exp(1j * phi))

    return np.abs(z)


def circular_mean_mod90(values_deg):
    values = np.asarray(values_deg, dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.nan

    phi = np.radians(values * 4.0)

    z = np.mean(np.exp(1j * phi))

    angle = np.degrees(np.angle(z)) / 4.0

    return angle % 90.0


# ============================================================
# LOAD
# ============================================================

df = pd.read_csv(INPUT_FILE)

required = [
    "UTC",
    "A2",
    "A4",
    "Phi2_deg",
    "Phi4_deg",
    "PLV",
    "Axis_Ratio",
    "Dominant_m",
]

missing = [c for c in required if c not in df.columns]

if missing:
    raise ValueError(
        "Missing columns: " + ", ".join(missing)
    )


# ============================================================
# BASIC METRICS
# ============================================================

df["Flattening_A2"] = df["A2"]
df["Fourfold_A4"] = df["A4"]

eps = 1e-12

df["A4_over_A2"] = (
    df["A4"] / (df["A2"] + eps)
)

# Joint strength:
# high only if BOTH A2 and A4 are substantial.
df["Joint_A2_A4"] = np.sqrt(
    df["A2"] * df["A4"]
)

# Alternative product, preserved separately.
df["Product_A2_A4"] = (
    df["A2"] * df["A4"]
)


# ============================================================
# ORIENTATION RELATION
# ============================================================

# m=2 orientation has 180° periodicity.
# For comparison with m=4, reduce it modulo 90°.
df["Phi2_mod90_deg"] = (
    df["Phi2_deg"] % 90.0
)

df["Phi4_mod90_deg"] = (
    df["Phi4_deg"] % 90.0
)

df["Phi2_Phi4_Difference_deg"] = [
    circular_difference_mod90(a, b)
    for a, b in zip(
        df["Phi2_mod90_deg"],
        df["Phi4_mod90_deg"],
    )
]

# Absolute orientation mismatch
df["Phi2_Phi4_AbsDifference_deg"] = np.abs(
    df["Phi2_Phi4_Difference_deg"]
)


# ============================================================
# EMPIRICAL DISTRIBUTION
# ============================================================

a2_median = df["A2"].median()
a4_median = df["A4"].median()

a2_q75 = df["A2"].quantile(0.75)
a4_q75 = df["A4"].quantile(0.75)

joint_median = df["Joint_A2_A4"].median()
joint_q75 = df["Joint_A2_A4"].quantile(0.75)
joint_q90 = df["Joint_A2_A4"].quantile(0.90)
joint_q95 = df["Joint_A2_A4"].quantile(0.95)


# These are descriptive groups, NOT physical classifications.

df["Both_Above_Median"] = (
    (df["A2"] >= a2_median)
    &
    (df["A4"] >= a4_median)
)

df["Both_Upper_Quartile"] = (
    (df["A2"] >= a2_q75)
    &
    (df["A4"] >= a4_q75)
)

df["Joint_Top10pct"] = (
    df["Joint_A2_A4"] >= joint_q90
)

df["Joint_Top5pct"] = (
    df["Joint_A2_A4"] >= joint_q95
)


# ============================================================
# SUMMARY
# ============================================================

orientation_difference_mean = circular_mean_mod90(
    df["Phi2_Phi4_Difference_deg"]
)

orientation_difference_concentration = (
    circular_concentration_mod90(
        df["Phi2_Phi4_Difference_deg"]
    )
)

summary = {
    "Windows": len(df),

    "Median_A2": df["A2"].median(),
    "Mean_A2": df["A2"].mean(),

    "Median_A4": df["A4"].median(),
    "Mean_A4": df["A4"].mean(),

    "Median_A4_over_A2":
        df["A4_over_A2"].median(),

    "Mean_A4_over_A2":
        df["A4_over_A2"].mean(),

    "Median_Joint_A2_A4":
        df["Joint_A2_A4"].median(),

    "Joint_A2_A4_Q75":
        joint_q75,

    "Joint_A2_A4_Q90":
        joint_q90,

    "Joint_A2_A4_Q95":
        joint_q95,

    "Both_Above_Median_Count":
        int(df["Both_Above_Median"].sum()),

    "Both_Above_Median_Percent":
        100.0 * df["Both_Above_Median"].mean(),

    "Both_Upper_Quartile_Count":
        int(df["Both_Upper_Quartile"].sum()),

    "Both_Upper_Quartile_Percent":
        100.0 * df["Both_Upper_Quartile"].mean(),

    "Median_Phi2_Phi4_AbsDifference_deg":
        df["Phi2_Phi4_AbsDifference_deg"].median(),

    "Mean_Phi2_Phi4_AbsDifference_deg":
        df["Phi2_Phi4_AbsDifference_deg"].mean(),

    "Phi2_Phi4_Circular_Mean_Difference_deg":
        orientation_difference_mean,

    "Phi2_Phi4_Relation_Concentration":
        orientation_difference_concentration,

    "Median_PLV":
        df["PLV"].median(),

    "Median_Axis_Ratio":
        df["Axis_Ratio"].median(),

    "m2_Dominant_Count":
        int((df["Dominant_m"] == 2).sum()),

    "m4_Dominant_Count":
        int((df["Dominant_m"] == 4).sum()),

    "m6_Dominant_Count":
        int((df["Dominant_m"] == 6).sum()),
}

summary_df = pd.DataFrame([summary])


# ============================================================
# TOP JOINT WINDOWS
# ============================================================

top_columns = [
    "UTC",
    "PLV",
    "Axis_Ratio",
    "A2",
    "A4",
    "A4_over_A2",
    "Joint_A2_A4",
    "Phi2_deg",
    "Phi4_deg",
    "Phi2_Phi4_Difference_deg",
    "Dominant_m",
]

top = (
    df.sort_values(
        "Joint_A2_A4",
        ascending=False
    )
    .head(100)[top_columns]
)


# ============================================================
# SAVE CSV
# ============================================================

df.to_csv(
    f"{OUTPUT_PREFIX}_1MIN.csv",
    index=False
)

summary_df.to_csv(
    f"{OUTPUT_PREFIX}_SUMMARY.csv",
    index=False
)

top.to_csv(
    f"{OUTPUT_PREFIX}_TOP_WINDOWS.csv",
    index=False
)


# ============================================================
# PLOTS
# ============================================================

# ------------------------------------------------------------
# A2 vs A4
# ------------------------------------------------------------

plt.figure(figsize=(8, 7))

plt.scatter(
    df["A2"],
    df["A4"],
    s=12,
    alpha=0.5
)

plt.axvline(
    a2_median,
    linestyle="--"
)

plt.axhline(
    a4_median,
    linestyle="--"
)

plt.xlabel("A2 — twofold / flattening component")
plt.ylabel("A4 — fourfold component")

plt.title(
    "Kunigami — A2 vs A4\n"
    "7.9–8.1 Hz"
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_PREFIX}_A2_A4_SCATTER.png",
    dpi=180
)

plt.close()


# ------------------------------------------------------------
# A4 / A2 ratio
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

ratio_for_plot = df[
    np.isfinite(df["A4_over_A2"])
]["A4_over_A2"]

# Avoid extreme tails dominating display only.
upper = ratio_for_plot.quantile(0.99)

plt.hist(
    ratio_for_plot[
        ratio_for_plot <= upper
    ],
    bins=60
)

plt.axvline(
    ratio_for_plot.median(),
    linestyle="--"
)

plt.xlabel("A4 / A2")
plt.ylabel("60 s windows")

plt.title(
    "Kunigami — Fourfold / Flattening Ratio"
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_PREFIX}_RATIO.png",
    dpi=180
)

plt.close()


# ------------------------------------------------------------
# Joint A2-A4 strength
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    df["Joint_A2_A4"],
    bins=60
)

plt.axvline(
    joint_q90,
    linestyle="--",
    label="90th percentile"
)

plt.xlabel(
    "Joint A2-A4 strength = sqrt(A2 × A4)"
)

plt.ylabel("60 s windows")

plt.title(
    "Kunigami — Joint Flattening + Fourfold Strength"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_PREFIX}_JOINT.png",
    dpi=180
)

plt.close()


# ------------------------------------------------------------
# Relative orientation m2 vs m4
# ------------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    df["Phi2_Phi4_Difference_deg"],
    bins=45,
    range=(-45, 45)
)

plt.xlabel(
    "Relative orientation Phi2 − Phi4 (deg, modulo 90°)"
)

plt.ylabel("60 s windows")

plt.title(
    "Kunigami — Relative Orientation of m=2 and m=4"
)

plt.tight_layout()

plt.savefig(
    f"{OUTPUT_PREFIX}_PHASE_RELATION.png",
    dpi=180
)

plt.close()


# ============================================================
# TERMINAL REPORT
# ============================================================

print()
print("=" * 72)
print("KUNIGAMI — FLATTENED QUADRILATERAL TEST")
print("=" * 72)

print(f"Windows: {len(df)}")

print()
print("TWO-FOLD / FLATTENING COMPONENT")
print(
    f"Median A2: {df['A2'].median():.6f}"
)

print()
print("FOUR-FOLD COMPONENT")
print(
    f"Median A4: {df['A4'].median():.6f}"
)

print()
print("RELATIVE FOURFOLD STRENGTH")
print(
    "Median A4/A2:",
    f"{df['A4_over_A2'].median():.6f}"
)

print()
print("JOINT A2 + A4")
print(
    "Median joint strength:",
    f"{df['Joint_A2_A4'].median():.6f}"
)

print(
    "90th percentile:",
    f"{joint_q90:.6f}"
)

print(
    "95th percentile:",
    f"{joint_q95:.6f}"
)

print()
print("SIMULTANEOUSLY STRONG COMPONENTS")

n_med = int(
    df["Both_Above_Median"].sum()
)

print(
    "A2 and A4 both above their medians:",
    f"{n_med}/{len(df)} "
    f"({100*n_med/len(df):.2f}%)"
)

n_q75 = int(
    df["Both_Upper_Quartile"].sum()
)

print(
    "A2 and A4 both in upper quartile:",
    f"{n_q75}/{len(df)} "
    f"({100*n_q75/len(df):.2f}%)"
)

print()
print("m=2 / m=4 ORIENTATION RELATION")

print(
    "Median absolute relative angle:",
    f"{df['Phi2_Phi4_AbsDifference_deg'].median():.3f} deg"
)

print(
    "Circular relation concentration:",
    f"{orientation_difference_concentration:.6f}"
)

print()
print("DOMINANT ORDERS")

for m in [2, 4, 6]:
    n = int(
        (df["Dominant_m"] == m).sum()
    )

    print(
        f"m={m}: {n}/{len(df)} "
        f"({100*n/len(df):.2f}%)"
    )

print()
print("Saved:")

for filename in [
    f"{OUTPUT_PREFIX}_1MIN.csv",
    f"{OUTPUT_PREFIX}_SUMMARY.csv",
    f"{OUTPUT_PREFIX}_TOP_WINDOWS.csv",
    f"{OUTPUT_PREFIX}_A2_A4_SCATTER.png",
    f"{OUTPUT_PREFIX}_RATIO.png",
    f"{OUTPUT_PREFIX}_JOINT.png",
    f"{OUTPUT_PREFIX}_PHASE_RELATION.png",
]:
    print(" ", filename)

print("=" * 72)