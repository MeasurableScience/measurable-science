#!/usr/bin/env python3

"""
CARISMA - wide refinement of the phase-coherent structure

Stations:
    FCHU
    FSMI
    ISLL
    MSTK
    PINA

Search:
    6.800 - 8.400 Hz
    step = 0.001 Hz

Method unchanged from previous refinement:
    - 20 Hz ICM20 data
    - one 60 s window per hourly file
    - minute 30:00-31:00
    - CH1 vs CH2
    - Butterworth bandpass
    - Hilbert phase
    - PLV
    - hourly peak
    - hourly weighted center
    - aggregate mean/median profile

All outputs:
    CAR68_84/
"""

import os
import re
import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import butter, sosfiltfilt, hilbert


# ============================================================
# SETTINGS
# ============================================================

DATA_DIR = "."
OUT_DIR = "CAR68_84"

STATIONS = [
    "FCHU",
    "FSMI",
    "ISLL",
    "MSTK",
    "PINA"
]

FS = 20.0

WINDOW_START_SEC = 30 * 60
WINDOW_SECONDS = 60.0
N_WINDOW = int(FS * WINDOW_SECONDS)

# ============================================================
# WIDER SEARCH
# ============================================================

FREQ_MIN = 6.800
FREQ_MAX = 8.400
FREQ_STEP = 0.001

BANDWIDTH = 0.100
FILTER_ORDER = 4

os.makedirs(
    OUT_DIR,
    exist_ok=True
)


FILE_RE = re.compile(
    r"^(\d{8})([A-Z0-9]+)(\d{2})\.ICM20$",
    re.I
)


# ============================================================
# READ ONE 60-S WINDOW
# ============================================================

def read_window(path):

    ch1 = []
    ch2 = []

    start = WINDOW_START_SEC
    end = (
        WINDOW_START_SEC
        +
        WINDOW_SECONDS
    )

    with open(
        path,
        "r",
        encoding="ascii",
        errors="replace"
    ) as f:

        for line in f:

            if not line:
                continue

            if line.startswith("#"):
                continue

            p = line.split()

            if len(p) < 3:
                continue

            try:

                t = p[0]

                mm = int(
                    t[2:4]
                )

                ss = float(
                    t[4:]
                )

                sec_in_hour = (
                    mm * 60.0
                    +
                    ss
                )

            except Exception:
                continue


            if sec_in_hour < start:
                continue

            if sec_in_hour >= end:
                break


            try:

                v1 = float(
                    p[1]
                )

                v2 = float(
                    p[2]
                )

            except Exception:
                continue


            if (
                np.isfinite(v1)
                and
                np.isfinite(v2)
            ):

                ch1.append(v1)
                ch2.append(v2)


    if len(ch1) < int(
        0.95 * N_WINDOW
    ):
        return None, None


    a = np.asarray(
        ch1[:N_WINDOW],
        dtype=np.float64
    )

    b = np.asarray(
        ch2[:N_WINDOW],
        dtype=np.float64
    )


    if (
        len(a) != N_WINDOW
        or
        len(b) != N_WINDOW
    ):
        return None, None


    a -= np.mean(a)
    b -= np.mean(b)

    return a, b


# ============================================================
# PLV
# ============================================================

def calculate_plv(
    a,
    b,
    frequency
):

    half_bw = (
        BANDWIDTH
        /
        2.0
    )

    low = (
        frequency
        -
        half_bw
    )

    high = (
        frequency
        +
        half_bw
    )


    if low <= 0:
        return np.nan

    if high >= FS / 2.0:
        return np.nan


    sos = butter(
        FILTER_ORDER,
        [low, high],
        btype="bandpass",
        fs=FS,
        output="sos"
    )


    af = sosfiltfilt(
        sos,
        a
    )

    bf = sosfiltfilt(
        sos,
        b
    )


    phase_a = np.angle(
        hilbert(af)
    )

    phase_b = np.angle(
        hilbert(bf)
    )


    phase_difference = (
        phase_a
        -
        phase_b
    )


    return float(
        np.abs(
            np.mean(
                np.exp(
                    1j
                    *
                    phase_difference
                )
            )
        )
    )


# ============================================================
# WEIGHTED CENTER
# ============================================================

def weighted_center(
    frequencies,
    values
):

    f = np.asarray(
        frequencies,
        dtype=np.float64
    )

    v = np.asarray(
        values,
        dtype=np.float64
    )


    good = (
        np.isfinite(f)
        &
        np.isfinite(v)
    )

    f = f[good]
    v = v[good]


    if len(v) == 0:
        return np.nan


    # Remove local PLV floor before weighting.
    floor = np.min(v)

    weights = (
        v
        -
        floor
    )


    if np.sum(weights) <= 0:
        return np.nan


    return float(
        np.sum(
            f
            *
            weights
        )
        /
        np.sum(
            weights
        )
    )


# ============================================================
# FREQUENCY GRID
# ============================================================

frequencies = np.round(
    np.arange(
        FREQ_MIN,
        FREQ_MAX
        +
        FREQ_STEP / 2.0,
        FREQ_STEP
    ),
    6
)


# ============================================================
# FIND ALL CARISMA FILES
# ============================================================

all_records = []


for path in glob.glob(
    os.path.join(
        DATA_DIR,
        "*.ICM20"
    )
):

    name = os.path.basename(
        path
    )

    m = FILE_RE.match(
        name
    )

    if not m:
        continue


    date, station, hour = (
        m.groups()
    )

    station = station.upper()


    if station not in STATIONS:
        continue


    all_records.append(
        (
            station,
            date,
            int(hour),
            path
        )
    )


# ============================================================
# PROCESS ONE STATION
# ============================================================

def process_station(station):

    station_dir = os.path.join(
        OUT_DIR,
        station
    )

    os.makedirs(
        station_dir,
        exist_ok=True
    )


    records = [
        r
        for r in all_records
        if r[0] == station
    ]

    records.sort(
        key=lambda x: (
            x[1],
            x[2]
        )
    )


    print()
    print("=" * 80)
    print(
        f" {station} - WIDE 6.800-8.400 Hz REFINEMENT"
    )
    print("=" * 80)

    print(
        "Hourly files:",
        len(records)
    )

    print(
        "Frequency bins:",
        len(frequencies)
    )


    if not records:

        print(
            "No files."
        )

        return None


    all_profiles = []
    hourly_rows = []


    for file_number, (
        _,
        date,
        hour,
        path
    ) in enumerate(
        records,
        start=1
    ):

        a, b = read_window(
            path
        )


        if a is None:

            print(
                f"[{file_number:02d}/{len(records):02d}] "
                f"{date} {hour:02d}:00 SKIPPED"
            )

            continue


        plv_values = np.empty(
            len(frequencies),
            dtype=np.float64
        )


        for i, frequency in enumerate(
            frequencies
        ):

            try:

                plv_values[i] = (
                    calculate_plv(
                        a,
                        b,
                        frequency
                    )
                )

            except Exception:

                plv_values[i] = np.nan


        good = np.isfinite(
            plv_values
        )


        if not np.any(good):
            continue


        valid_f = frequencies[
            good
        ]

        valid_plv = plv_values[
            good
        ]


        peak_index = np.argmax(
            valid_plv
        )


        peak_frequency = float(
            valid_f[
                peak_index
            ]
        )

        peak_plv = float(
            valid_plv[
                peak_index
            ]
        )


        wcenter = weighted_center(
            valid_f,
            valid_plv
        )


        hourly_rows.append({

            "Date":
                date,

            "Hour_UTC":
                hour,

            "Peak_Hz":
                peak_frequency,

            "Peak_PLV":
                peak_plv,

            "Weighted_Center_Hz":
                wcenter
        })


        all_profiles.append(
            plv_values
        )


        print(
            f"[{file_number:02d}/{len(records):02d}] "
            f"{date} {hour:02d}:00  "
            f"peak={peak_frequency:.3f} Hz  "
            f"PLV={peak_plv:.4f}  "
            f"center={wcenter:.3f} Hz"
        )


    if not all_profiles:

        print(
            "No usable windows."
        )

        return None


    matrix = np.vstack(
        all_profiles
    )


    hourly = pd.DataFrame(
        hourly_rows
    )


    # ========================================================
    # AGGREGATE PROFILE
    # ========================================================

    mean_profile = np.nanmean(
        matrix,
        axis=0
    )

    median_profile = np.nanmedian(
        matrix,
        axis=0
    )


    mean_peak_index = np.nanargmax(
        mean_profile
    )

    median_peak_index = np.nanargmax(
        median_profile
    )


    mean_peak_frequency = float(
        frequencies[
            mean_peak_index
        ]
    )

    mean_peak_plv = float(
        mean_profile[
            mean_peak_index
        ]
    )


    median_peak_frequency = float(
        frequencies[
            median_peak_index
        ]
    )

    median_peak_plv = float(
        median_profile[
            median_peak_index
        ]
    )


    mean_weighted_center = (
        weighted_center(
            frequencies,
            mean_profile
        )
    )

    median_weighted_center = (
        weighted_center(
            frequencies,
            median_profile
        )
    )


    # ========================================================
    # HOURLY STATISTICS
    # ========================================================

    hourly_peak = hourly[
        "Peak_Hz"
    ].to_numpy(
        dtype=np.float64
    )


    hourly_wc = hourly[
        "Weighted_Center_Hz"
    ].to_numpy(
        dtype=np.float64
    )


    # Important: remove only non-finite summary values.
    # Raw/hourly output remains untouched.
    valid_wc = hourly_wc[
        np.isfinite(
            hourly_wc
        )
    ]


    peak_median = np.median(
        hourly_peak
    )

    peak_mad = np.median(
        np.abs(
            hourly_peak
            -
            peak_median
        )
    )


    if len(valid_wc):

        wc_mean = np.mean(
            valid_wc
        )

        wc_median = np.median(
            valid_wc
        )

        wc_mad = np.median(
            np.abs(
                valid_wc
                -
                wc_median
            )
        )

        wc_std = (
            np.std(
                valid_wc,
                ddof=1
            )
            if len(valid_wc) > 1
            else 0.0
        )

        wc_q05 = np.quantile(
            valid_wc,
            0.05
        )

        wc_q95 = np.quantile(
            valid_wc,
            0.95
        )

    else:

        wc_mean = np.nan
        wc_median = np.nan
        wc_mad = np.nan
        wc_std = np.nan
        wc_q05 = np.nan
        wc_q95 = np.nan


    # ========================================================
    # SAVE PROFILE
    # ========================================================

    profile = pd.DataFrame({

        "Frequency_Hz":
            frequencies,

        "Mean_PLV":
            mean_profile,

        "Median_PLV":
            median_profile
    })


    profile.to_csv(
        os.path.join(
            station_dir,
            "profile.csv"
        ),
        index=False
    )


    hourly.to_csv(
        os.path.join(
            station_dir,
            "hourly.csv"
        ),
        index=False
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    summary_row = {

        "Station":
            station,

        "Usable_Hourly_Windows":
            len(hourly),

        "Valid_Hourly_WCenters":
            len(valid_wc),

        "Search_Min_Hz":
            FREQ_MIN,

        "Search_Max_Hz":
            FREQ_MAX,

        "Frequency_Step_Hz":
            FREQ_STEP,

        "Bandpass_Width_Hz":
            BANDWIDTH,

        "Aggregate_Peak_Mean_PLV_Hz":
            mean_peak_frequency,

        "Aggregate_Peak_Mean_PLV":
            mean_peak_plv,

        "Aggregate_Peak_Median_PLV_Hz":
            median_peak_frequency,

        "Aggregate_Peak_Median_PLV":
            median_peak_plv,

        "Weighted_Center_Mean_Profile_Hz":
            mean_weighted_center,

        "Weighted_Center_Median_Profile_Hz":
            median_weighted_center,

        "Hourly_Peak_Mean_Hz":
            np.mean(
                hourly_peak
            ),

        "Hourly_Peak_Median_Hz":
            peak_median,

        "Hourly_Peak_MAD_Hz":
            peak_mad,

        "Hourly_Peak_STD_Hz":
            np.std(
                hourly_peak,
                ddof=1
            ),

        "Hourly_Peak_Q05_Hz":
            np.quantile(
                hourly_peak,
                0.05
            ),

        "Hourly_Peak_Q95_Hz":
            np.quantile(
                hourly_peak,
                0.95
            ),

        "Hourly_WCenter_Mean_Hz":
            wc_mean,

        "Hourly_WCenter_Median_Hz":
            wc_median,

        "Hourly_WCenter_MAD_Hz":
            wc_mad,

        "Hourly_WCenter_STD_Hz":
            wc_std,

        "Hourly_WCenter_Q05_Hz":
            wc_q05,

        "Hourly_WCenter_Q95_Hz":
            wc_q95
    }


    pd.DataFrame(
        [summary_row]
    ).to_csv(
        os.path.join(
            station_dir,
            "summary.csv"
        ),
        index=False
    )


    # ========================================================
    # GRAPH
    # ========================================================

    plt.figure(
        figsize=(15, 7)
    )


    plt.plot(
        frequencies,
        mean_profile,
        label="Mean PLV"
    )


    plt.plot(
        frequencies,
        median_profile,
        label="Median PLV"
    )


    plt.axvline(
        mean_weighted_center,
        linestyle="--",
        label=(
            "Mean weighted center "
            f"{mean_weighted_center:.3f} Hz"
        )
    )


    plt.axvline(
        median_weighted_center,
        linestyle=":",
        label=(
            "Median weighted center "
            f"{median_weighted_center:.3f} Hz"
        )
    )


    plt.xlabel(
        "Frequency (Hz)"
    )

    plt.ylabel(
        "CH1-CH2 PLV"
    )

    plt.title(
        f"CARISMA {station} - wide phase-coherent structure "
        "(6.80-8.40 Hz)"
    )


    plt.legend()

    plt.tight_layout()


    plt.savefig(
        os.path.join(
            station_dir,
            "profile.png"
        ),
        dpi=180
    )


    plt.close()


    # ========================================================
    # PRINT
    # ========================================================

    print()

    print(
        f"{station}:"
    )

    print(
        f"  aggregate mean peak     = "
        f"{mean_peak_frequency:.3f} Hz"
    )

    print(
        f"  aggregate median peak   = "
        f"{median_peak_frequency:.3f} Hz"
    )

    print(
        f"  mean-profile center     = "
        f"{mean_weighted_center:.6f} Hz"
    )

    print(
        f"  median-profile center   = "
        f"{median_weighted_center:.6f} Hz"
    )

    print(
        f"  hourly center mean      = "
        f"{wc_mean:.6f} Hz"
    )

    print(
        f"  hourly center median    = "
        f"{wc_median:.6f} Hz"
    )

    print(
        f"  hourly center MAD       = "
        f"{wc_mad:.6f} Hz"
    )

    print(
        f"  hourly center STD       = "
        f"{wc_std:.6f} Hz"
    )

    print(
        f"  hourly center Q05-Q95   = "
        f"{wc_q05:.6f} - {wc_q95:.6f} Hz"
    )


    return summary_row


# ============================================================
# RUN ALL FIVE STATIONS
# ============================================================

master_rows = []


for station in STATIONS:

    result = process_station(
        station
    )

    if result is not None:

        master_rows.append(
            result
        )


# ============================================================
# MASTER SUMMARY
# ============================================================

if master_rows:

    master = pd.DataFrame(
        master_rows
    )


    master.to_csv(
        os.path.join(
            OUT_DIR,
            "ALL_STATIONS_SUMMARY.csv"
        ),
        index=False
    )


    print()
    print("=" * 80)
    print(" ALL STATIONS - 6.800-8.400 Hz")
    print("=" * 80)
    print()


    columns = [

        "Station",

        "Aggregate_Peak_Mean_PLV_Hz",

        "Aggregate_Peak_Median_PLV_Hz",

        "Weighted_Center_Mean_Profile_Hz",

        "Weighted_Center_Median_Profile_Hz",

        "Hourly_WCenter_Mean_Hz",

        "Hourly_WCenter_Median_Hz",

        "Hourly_WCenter_MAD_Hz",

        "Hourly_WCenter_STD_Hz"
    ]


    print(
        master[
            columns
        ].to_string(
            index=False
        )
    )


    print()
    print(
        "Saved:",
        os.path.join(
            OUT_DIR,
            "ALL_STATIONS_SUMMARY.csv"
        )
    )


print()
print("DONE")