#!/usr/bin/env python3

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import (
    find_peaks,
    peak_prominences,
    peak_widths,
    savgol_filter
)


# ============================================================
# CARISMA - DOMINANT COMMON RIDGE ACROSS 5 STATIONS
#
# PURPOSE:
#
# Find the strongest COMMON frequency structure shared by
# all five CARISMA stations.
#
# We DO NOT define a global 90% width anymore.
#
# Instead:
#
#   1. remove local PLV floor for every station
#   2. normalize each station to 0..1
#   3. calculate geometric mean across all 5 stations
#   4. lightly smooth the common profile
#   5. blindly find the most PROMINENT common peak
#   6. measure:
#
#      - peak frequency
#      - prominence
#      - left prominence base
#      - right prominence base
#      - valley-to-valley width
#      - half-prominence width
#      - local weighted center of that ridge
#
# Input:
#
#   CAR68_84/FCHU/profile.csv
#   CAR68_84/FSMI/profile.csv
#   CAR68_84/ISLL/profile.csv
#   CAR68_84/MSTK/profile.csv
#   CAR68_84/PINA/profile.csv
#
# Output:
#
#   COMMON_RING/common_profile.csv
#   COMMON_RING/common_summary.csv
#   COMMON_RING/common_ridge.png
# ============================================================


INPUT_ROOT = "CAR68_84"
OUTPUT_ROOT = "COMMON_RING"

STATIONS = [
    "FCHU",
    "FSMI",
    "ISLL",
    "MSTK",
    "PINA"
]

os.makedirs(
    OUTPUT_ROOT,
    exist_ok=True
)


# ============================================================
# SMOOTHING
# ============================================================
#
# Frequency step is 0.001 Hz.
#
# 21 points = 0.021 Hz smoothing scale.
#
# This is deliberately small compared with the structure
# we are trying to measure.
#
# It suppresses single-bin teeth / zeros without defining
# the width of the ridge in advance.
# ============================================================

SMOOTH_WINDOW_BINS = 21
SMOOTH_POLYORDER = 3


# ============================================================
# LOAD STATION PROFILES
# ============================================================

frequency = None

station_normalized = {}
station_raw = {}


print()
print("=" * 84)
print(" CARISMA - DOMINANT COMMON RIDGE")
print("=" * 84)
print()


for station in STATIONS:

    path = os.path.join(
        INPUT_ROOT,
        station,
        "profile.csv"
    )

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Missing profile: {path}"
        )


    df = pd.read_csv(
        path
    )


    f = df[
        "Frequency_Hz"
    ].to_numpy(
        dtype=float
    )

    y = df[
        "Mean_PLV"
    ].to_numpy(
        dtype=float
    )


    good = (
        np.isfinite(f)
        &
        np.isfinite(y)
    )

    f = f[good]
    y = y[good]


    if frequency is None:

        frequency = f.copy()

    else:

        if (
            len(f) != len(frequency)
            or
            not np.allclose(
                f,
                frequency,
                atol=1e-10
            )
        ):

            raise ValueError(
                f"{station}: frequency grid differs."
            )


    # --------------------------------------------------------
    # LOCAL FLOOR REMOVAL
    # --------------------------------------------------------

    floor = float(
        np.min(y)
    )

    excess = (
        y
        -
        floor
    )

    excess = np.clip(
        excess,
        0,
        None
    )


    maximum = float(
        np.max(excess)
    )


    if maximum <= 0:

        raise ValueError(
            f"{station}: no positive PLV excess."
        )


    normalized = (
        excess
        /
        maximum
    )


    station_raw[
        station
    ] = y

    station_normalized[
        station
    ] = normalized


    print(
        f"{station}: "
        f"floor={floor:.6f}  "
        f"normalized peak=1.000"
    )


# ============================================================
# COMMON GEOMETRIC PROFILE
# ============================================================

matrix = np.vstack(
    [
        station_normalized[
            station
        ]
        for station in STATIONS
    ]
)


EPS = 1e-12


common_raw = np.exp(
    np.mean(
        np.log(
            np.clip(
                matrix,
                EPS,
                None
            )
        ),
        axis=0
    )
)


# Also useful for diagnostic comparison

common_arithmetic = np.mean(
    matrix,
    axis=0
)

common_minimum = np.min(
    matrix,
    axis=0
)


# ============================================================
# LIGHT SMOOTHING
# ============================================================

window = SMOOTH_WINDOW_BINS


if window >= len(common_raw):

    window = len(common_raw) - 1


if window % 2 == 0:

    window -= 1


if window < 5:

    raise ValueError(
        "Profile too short for smoothing."
    )


common_smooth = savgol_filter(
    common_raw,
    window_length=window,
    polyorder=SMOOTH_POLYORDER,
    mode="interp"
)


common_smooth = np.clip(
    common_smooth,
    0,
    None
)


# ============================================================
# FIND ALL COMMON PEAKS
# ============================================================

peaks, _ = find_peaks(
    common_smooth
)


if len(peaks) == 0:

    raise RuntimeError(
        "No common peaks found."
    )


prominences, left_bases, right_bases = (
    peak_prominences(
        common_smooth,
        peaks
    )
)


# ============================================================
# DOMINANT PEAK = HIGHEST PROMINENCE
# ============================================================

best_number = int(
    np.argmax(
        prominences
    )
)


peak_index = int(
    peaks[
        best_number
    ]
)

prominence = float(
    prominences[
        best_number
    ]
)

left_base_index = int(
    left_bases[
        best_number
    ]
)

right_base_index = int(
    right_bases[
        best_number
    ]
)


peak_hz = float(
    frequency[
        peak_index
    ]
)

peak_value = float(
    common_smooth[
        peak_index
    ]
)


left_base_hz = float(
    frequency[
        left_base_index
    ]
)

right_base_hz = float(
    frequency[
        right_base_index
    ]
)


left_base_value = float(
    common_smooth[
        left_base_index
    ]
)

right_base_value = float(
    common_smooth[
        right_base_index
    ]
)


valley_width_hz = (
    right_base_hz
    -
    left_base_hz
)


# ============================================================
# HALF-PROMINENCE WIDTH
# ============================================================
#
# scipy peak_widths measures width at:
#
# peak height - prominence * rel_height
#
# rel_height = 0.5
#
# therefore half prominence.
# ============================================================

width_result = peak_widths(
    common_smooth,
    np.array(
        [peak_index]
    ),
    rel_height=0.5,
    prominence_data=(
        np.array(
            [prominence]
        ),
        np.array(
            [left_base_index]
        ),
        np.array(
            [right_base_index]
        )
    )
)


width_bins = float(
    width_result[0][0]
)

half_level = float(
    width_result[1][0]
)

left_ip = float(
    width_result[2][0]
)

right_ip = float(
    width_result[3][0]
)


# Convert fractional sample index -> frequency

sample_index = np.arange(
    len(frequency),
    dtype=float
)


left_half_hz = float(
    np.interp(
        left_ip,
        sample_index,
        frequency
    )
)

right_half_hz = float(
    np.interp(
        right_ip,
        sample_index,
        frequency
    )
)


half_prominence_width_hz = (
    right_half_hz
    -
    left_half_hz
)


# ============================================================
# LOCAL WEIGHTED CENTER OF THE DOMINANT RIDGE
# ============================================================
#
# Only between prominence bases.
#
# We subtract the higher of the two base levels so the broad
# global background does not shift the ridge center.
# ============================================================

local_f = frequency[
    left_base_index:
    right_base_index + 1
]

local_y = common_smooth[
    left_base_index:
    right_base_index + 1
]


local_floor = max(
    left_base_value,
    right_base_value
)


local_excess = (
    local_y
    -
    local_floor
)

local_excess = np.clip(
    local_excess,
    0,
    None
)


if np.sum(
    local_excess
) > 0:

    local_center_hz = float(
        np.sum(
            local_f
            *
            local_excess
        )
        /
        np.sum(
            local_excess
        )
    )

else:

    local_center_hz = peak_hz


# ============================================================
# ASYMMETRY
# ============================================================

half_left_radius = (
    local_center_hz
    -
    left_half_hz
)

half_right_radius = (
    right_half_hz
    -
    local_center_hz
)


half_asymmetry = (
    half_right_radius
    -
    half_left_radius
)


base_left_radius = (
    local_center_hz
    -
    left_base_hz
)

base_right_radius = (
    right_base_hz
    -
    local_center_hz
)


base_asymmetry = (
    base_right_radius
    -
    base_left_radius
)


# ============================================================
# QUALITY / EDGE FLAGS
# ============================================================

search_min = float(
    frequency[0]
)

search_max = float(
    frequency[-1]
)


step_hz = float(
    np.median(
        np.diff(
            frequency
        )
    )
)


EDGE_MARGIN_HZ = 0.020


left_edge_flag = (
    left_base_hz
    <=
    search_min
    +
    EDGE_MARGIN_HZ
)


right_edge_flag = (
    right_base_hz
    >=
    search_max
    -
    EDGE_MARGIN_HZ
)


ridge_closed_inside_window = (
    not left_edge_flag
    and
    not right_edge_flag
)


# ============================================================
# SAVE FULL PROFILE
# ============================================================

profile_out = pd.DataFrame({

    "Frequency_Hz":
        frequency,

    "Common_Geometric_Raw":
        common_raw,

    "Common_Geometric_Smoothed":
        common_smooth,

    "Common_Arithmetic":
        common_arithmetic,

    "Common_Minimum":
        common_minimum
})


for station in STATIONS:

    profile_out[
        f"{station}_Normalized"
    ] = station_normalized[
        station
    ]


profile_path = os.path.join(
    OUTPUT_ROOT,
    "common_profile.csv"
)


profile_out.to_csv(
    profile_path,
    index=False
)


# ============================================================
# SAVE SUMMARY
# ============================================================

summary = pd.DataFrame(
    [
        {

            "Stations":
                len(STATIONS),

            "Search_Min_Hz":
                search_min,

            "Search_Max_Hz":
                search_max,

            "Frequency_Step_Hz":
                step_hz,

            "Smoothing_Window_Hz":
                window * step_hz,

            "Dominant_Peak_Hz":
                peak_hz,

            "Dominant_Peak_Value":
                peak_value,

            "Dominant_Prominence":
                prominence,

            "Local_Weighted_Center_Hz":
                local_center_hz,

            "Left_Base_Hz":
                left_base_hz,

            "Right_Base_Hz":
                right_base_hz,

            "Valley_to_Valley_Width_Hz":
                valley_width_hz,

            "Left_Half_Prominence_Hz":
                left_half_hz,

            "Right_Half_Prominence_Hz":
                right_half_hz,

            "Half_Prominence_Width_Hz":
                half_prominence_width_hz,

            "Half_Prominence_Level":
                half_level,

            "Half_Left_Radius_Hz":
                half_left_radius,

            "Half_Right_Radius_Hz":
                half_right_radius,

            "Half_Asymmetry_Hz":
                half_asymmetry,

            "Base_Left_Radius_Hz":
                base_left_radius,

            "Base_Right_Radius_Hz":
                base_right_radius,

            "Base_Asymmetry_Hz":
                base_asymmetry,

            "Left_Base_Value":
                left_base_value,

            "Right_Base_Value":
                right_base_value,

            "Closed_Inside_Search_Window":
                ridge_closed_inside_window
        }
    ]
)


summary_path = os.path.join(
    OUTPUT_ROOT,
    "common_summary.csv"
)


summary.to_csv(
    summary_path,
    index=False
)


# ============================================================
# GRAPH
# ============================================================

plt.figure(
    figsize=(15, 8)
)


# faint station profiles

for station in STATIONS:

    plt.plot(
        frequency,
        station_normalized[
            station
        ],
        linewidth=0.8,
        alpha=0.20
    )


# raw common profile

plt.plot(
    frequency,
    common_raw,
    linewidth=1.2,
    alpha=0.45,
    label="Common geometric - raw"
)


# smoothed common profile

plt.plot(
    frequency,
    common_smooth,
    linewidth=3.0,
    label="Common geometric - smoothed"
)


# peak

plt.axvline(
    peak_hz,
    linestyle="--",
    linewidth=2.0,
    label=(
        f"Dominant peak {peak_hz:.4f} Hz"
    )
)


# local center

plt.axvline(
    local_center_hz,
    linestyle="-.",
    linewidth=2.0,
    label=(
        f"Local center {local_center_hz:.4f} Hz"
    )
)


# prominence bases

plt.axvline(
    left_base_hz,
    linestyle=":",
    linewidth=1.5,
    label=(
        f"Left base {left_base_hz:.4f}"
    )
)


plt.axvline(
    right_base_hz,
    linestyle=":",
    linewidth=1.5,
    label=(
        f"Right base {right_base_hz:.4f}"
    )
)


# half prominence horizontal

plt.hlines(
    half_level,
    left_half_hz,
    right_half_hz,
    linewidth=3.0,
    label=(
        "Half-prominence width "
        f"{half_prominence_width_hz:.4f} Hz"
    )
)


# mark half-width crossings

plt.scatter(
    [
        left_half_hz,
        right_half_hz
    ],
    [
        half_level,
        half_level
    ],
    s=60
)


# dominant peak marker

plt.scatter(
    [
        peak_hz
    ],
    [
        peak_value
    ],
    s=90
)


plt.xlabel(
    "Frequency (Hz)"
)

plt.ylabel(
    "Normalized common phase-coherence structure"
)

plt.title(
    "CARISMA - dominant common ridge across 5 stations"
)

plt.legend(
    ncol=2
)

plt.tight_layout()


image_path = os.path.join(
    OUTPUT_ROOT,
    "common_ridge.png"
)


plt.savefig(
    image_path,
    dpi=180
)

plt.close()


# ============================================================
# REPORT
# ============================================================

print()
print("=" * 84)
print(" DOMINANT COMMON RIDGE")
print("=" * 84)
print()


print(
    f"Dominant peak             = "
    f"{peak_hz:.6f} Hz"
)

print(
    f"Peak prominence           = "
    f"{prominence:.6f}"
)

print(
    f"Local weighted center     = "
    f"{local_center_hz:.6f} Hz"
)


print()
print("--- PROMINENCE BASES ---")
print()


print(
    f"Left base                 = "
    f"{left_base_hz:.6f} Hz"
)

print(
    f"Right base                = "
    f"{right_base_hz:.6f} Hz"
)

print(
    f"Valley-to-valley width    = "
    f"{valley_width_hz:.6f} Hz"
)


print()
print("--- HALF PROMINENCE ---")
print()


print(
    f"Left half crossing        = "
    f"{left_half_hz:.6f} Hz"
)

print(
    f"Right half crossing       = "
    f"{right_half_hz:.6f} Hz"
)

print(
    f"Half-prominence width     = "
    f"{half_prominence_width_hz:.6f} Hz"
)


print()
print("--- SYMMETRY ---")
print()


print(
    f"Half left radius          = "
    f"{half_left_radius:.6f} Hz"
)

print(
    f"Half right radius         = "
    f"{half_right_radius:.6f} Hz"
)

print(
    f"Half asymmetry            = "
    f"{half_asymmetry:+.6f} Hz"
)


print()

print(
    f"Base left radius          = "
    f"{base_left_radius:.6f} Hz"
)

print(
    f"Base right radius         = "
    f"{base_right_radius:.6f} Hz"
)

print(
    f"Base asymmetry            = "
    f"{base_asymmetry:+.6f} Hz"
)


print()
print("--- WINDOW CHECK ---")
print()


print(
    f"Ridge closed inside window = "
    f"{ridge_closed_inside_window}"
)


if not ridge_closed_inside_window:

    print()
    print(
        "WARNING: a prominence base touches the "
        "search-window edge."
    )

    print(
        "The frequency window must be expanded "
        "before interpreting full ridge width."
    )


print()
print("=" * 84)
print(" SAVED")
print("=" * 84)

print(
    profile_path
)

print(
    summary_path
)

print(
    image_path
)

print()
print("DONE")