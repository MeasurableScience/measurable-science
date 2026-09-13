import glob
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# ESK MAIN-PULSE RAW PROBE
#
# Uses event times already found independently from
# carrier-band energy.
#
# Then goes BACK to untouched RAW CH1 counts.
#
# NO FILTER
# NO HILBERT
# NO ENERGY TRANSFORM
# NO FFT
# NO AUTOCORRELATION
# NO EXPECTED 30 s PERIOD
# NO SAMPLE DISCARDING
# ============================================================


DATA_FOLDER = "."

EVENT_FILE = "ESK_MAIN_ENERGY_EVENTS.csv"

CHANNEL = "CH1"

YEAR = 2012
MONTH = 6
DAY = 19

FS = 100.0


# Window around each already-detected event.
WINDOW_BEFORE_S = 2.0
WINDOW_AFTER_S = 2.0


# A small immediate region used only to measure
# raw behaviour right around the event.
CORE_HALF_WIDTH_S = 0.10


# ============================================================
# RAW READER
# ============================================================

def read_raw(filename):

    data = []

    with open(filename, "r", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:
                data.append(float(line))

            except ValueError:
                pass

    return np.asarray(data, dtype=np.float64)


# ============================================================
# LOAD ALL RAW FILES
# ============================================================

pattern = os.path.join(
    DATA_FOLDER,
    f"{CHANNEL}_{YEAR}_{MONTH:02d}_{DAY:02d}_*.dat"
)

files = sorted(glob.glob(pattern))


print("=" * 80)
print("ESK MAIN-PULSE RAW PROBE")
print("=" * 80)

print()
print("RAW files:", len(files))

if not files:
    raise RuntimeError("No RAW files found.")


parts = []

for filename in files:

    x = read_raw(filename)

    print(
        os.path.basename(filename),
        f"{len(x):,} samples"
    )

    parts.append(x)


raw = np.concatenate(parts)


print()
print(
    "Total RAW samples:",
    f"{len(raw):,}"
)

print(
    "Duration:",
    f"{len(raw)/FS/3600:.6f} h"
)


# ============================================================
# LOAD PREVIOUSLY FOUND EVENT TIMES
# ============================================================

events = pd.read_csv(EVENT_FILE)


if "peak_s" in events.columns:

    peak_seconds = events["peak_s"].to_numpy(
        dtype=float
    )

elif "peak_seconds" in events.columns:

    peak_seconds = events["peak_seconds"].to_numpy(
        dtype=float
    )

else:

    raise RuntimeError(
        "Cannot find peak_s or peak_seconds "
        "column in event CSV."
    )


peak_samples = np.rint(
    peak_seconds * FS
).astype(int)


print()
print(
    "Previously detected main events:",
    len(peak_samples)
)


# ============================================================
# WINDOW SETTINGS
# ============================================================

before_n = int(
    WINDOW_BEFORE_S * FS
)

after_n = int(
    WINDOW_AFTER_S * FS
)

core_n = int(
    CORE_HALF_WIDTH_S * FS
)


# ============================================================
# DIRECT RAW METRICS AT EACH EVENT
# ============================================================

rows = []

valid_windows = []


for event_number, peak_idx in enumerate(
    peak_samples,
    start=1
):

    start = peak_idx - before_n
    stop = peak_idx + after_n + 1

    if start < 0 or stop > len(raw):
        continue

    w = raw[start:stop]

    valid_windows.append(w.copy())


    # --------------------------------------------------------
    # Raw sample immediately before / at / after event
    # --------------------------------------------------------

    raw_before = raw[peak_idx - 1]
    raw_at = raw[peak_idx]
    raw_after = raw[peak_idx + 1]


    jump_into = (
        raw_at -
        raw_before
    )

    jump_out = (
        raw_after -
        raw_at
    )


    # --------------------------------------------------------
    # 4-second local RAW statistics
    # --------------------------------------------------------

    local_min = np.min(w)
    local_max = np.max(w)

    local_range = (
        local_max -
        local_min
    )

    local_mean = np.mean(w)

    local_std = np.std(w)


    # --------------------------------------------------------
    # Core ±0.10 s around event
    # --------------------------------------------------------

    core_start = (
        peak_idx -
        core_n
    )

    core_stop = (
        peak_idx +
        core_n +
        1
    )

    core = raw[
        core_start:core_stop
    ]

    core_range = (
        np.max(core) -
        np.min(core)
    )

    core_std = np.std(core)


    # --------------------------------------------------------
    # First-difference strength inside local window
    # --------------------------------------------------------

    diff = np.diff(w)

    max_abs_step = np.max(
        np.abs(diff)
    )

    max_step_position = (
        np.argmax(
            np.abs(diff)
        )
        /
        FS
        -
        WINDOW_BEFORE_S
    )


    rows.append({

        "event":
            event_number,

        "peak_s":
            peak_seconds[event_number - 1],

        "peak_sample":
            peak_idx,

        "raw_before":
            raw_before,

        "raw_at":
            raw_at,

        "raw_after":
            raw_after,

        "jump_into_counts":
            jump_into,

        "jump_out_counts":
            jump_out,

        "local_min_counts":
            local_min,

        "local_max_counts":
            local_max,

        "local_range_counts":
            local_range,

        "local_mean_counts":
            local_mean,

        "local_std_counts":
            local_std,

        "core_range_counts":
            core_range,

        "core_std_counts":
            core_std,

        "max_abs_step_counts":
            max_abs_step,

        "max_step_relative_s":
            max_step_position
    })


result = pd.DataFrame(rows)


# ============================================================
# EVENT-TRIGGERED RAW AVERAGE
#
# If RAW itself has a repeatable structure aligned with the
# carrier-energy pulse, averaging 1000+ events will reveal it.
#
# No filtering is performed.
# ============================================================

windows = np.asarray(
    valid_windows,
    dtype=np.float64
)


relative_t = (
    np.arange(
        windows.shape[1]
    )
    /
    FS
    -
    WINDOW_BEFORE_S
)


raw_event_mean = np.mean(
    windows,
    axis=0
)

raw_event_median = np.median(
    windows,
    axis=0
)


# Remove each event's own mean ONLY for a second diagnostic
# plot, so huge DC offsets do not hide a repeating RAW shape.
#
# This does not filter the signal.
centered_windows = (
    windows
    -
    np.mean(
        windows,
        axis=1,
        keepdims=True
    )
)


centered_mean = np.mean(
    centered_windows,
    axis=0
)

centered_median = np.median(
    centered_windows,
    axis=0
)


# ============================================================
# CONTROL WINDOWS
#
# For each pair of consecutive events, take the midpoint.
#
# This does NOT assume 30 s.
# It simply creates a RAW control location between actual
# detected events.
# ============================================================

control_windows = []


for a, b in zip(
    peak_samples[:-1],
    peak_samples[1:]
):

    midpoint = int(
        round(
            (a + b) / 2
        )
    )

    start = (
        midpoint -
        before_n
    )

    stop = (
        midpoint +
        after_n +
        1
    )

    if start < 0 or stop > len(raw):
        continue

    control_windows.append(
        raw[start:stop].copy()
    )


control_windows = np.asarray(
    control_windows,
    dtype=np.float64
)


control_centered = (
    control_windows
    -
    np.mean(
        control_windows,
        axis=1,
        keepdims=True
    )
)


control_mean = np.mean(
    control_centered,
    axis=0
)


# ============================================================
# SUMMARY
# ============================================================

print()
print("=" * 80)
print("RAW EVENT SUMMARY")
print("=" * 80)

print()
print(
    "Valid event windows:",
    len(windows)
)

print(
    "Control windows:",
    len(control_windows)
)


print()
print(
    "Median |jump into event|:",
    f"{np.median(np.abs(result['jump_into_counts'])):.3f}",
    "counts"
)

print(
    "Median |jump out|:",
    f"{np.median(np.abs(result['jump_out_counts'])):.3f}",
    "counts"
)

print(
    "Median local RAW range:",
    f"{np.median(result['local_range_counts']):.3f}",
    "counts"
)

print(
    "Median local RAW std:",
    f"{np.median(result['local_std_counts']):.3f}",
    "counts"
)

print(
    "Median core ±0.10s range:",
    f"{np.median(result['core_range_counts']):.3f}",
    "counts"
)

print(
    "Median max absolute sample step:",
    f"{np.median(result['max_abs_step_counts']):.3f}",
    "counts"
)


# ============================================================
# SAVE TABLE
# ============================================================

result.to_csv(
    "ESK_MAIN_PULSES_RAW_PROBE.csv",
    index=False
)


# ============================================================
# GRAPH 1
# FIRST 12 RAW EVENT WINDOWS
# ============================================================

plt.figure(
    figsize=(14, 6)
)


for w in centered_windows[:12]:

    plt.plot(
        relative_t,
        w,
        linewidth=0.8,
        alpha=0.6
    )


plt.axvline(
    0.0,
    linestyle="--",
    label="Carrier-energy event time"
)

plt.xlabel(
    "Time relative to energy event (s)"
)

plt.ylabel(
    "RAW counts - local mean removed"
)

plt.title(
    "ESK RAW CH1 around first 12 main energy events"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "ESK_RAW_AROUND_FIRST_12_EVENTS.png",
    dpi=180
)

plt.close()


# ============================================================
# GRAPH 2
# AVERAGE OF ALL EVENT-ALIGNED RAW WINDOWS
# ============================================================

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    relative_t,
    centered_mean,
    label="Mean RAW shape"
)

plt.plot(
    relative_t,
    centered_median,
    label="Median RAW shape"
)

plt.axvline(
    0.0,
    linestyle="--",
    label="Energy-event time"
)

plt.xlabel(
    "Time relative to energy event (s)"
)

plt.ylabel(
    "RAW counts - event mean removed"
)

plt.title(
    f"ESK RAW event-triggered average - "
    f"{len(centered_windows)} events"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "ESK_RAW_EVENT_TRIGGERED_AVERAGE.png",
    dpi=180
)

plt.close()


# ============================================================
# GRAPH 3
# EVENT vs MIDPOINT CONTROL
# ============================================================

plt.figure(
    figsize=(14, 6)
)

plt.plot(
    relative_t,
    centered_mean,
    label="RAW aligned to main energy events"
)

plt.plot(
    relative_t,
    control_mean,
    label="RAW aligned to between-event controls"
)

plt.axvline(
    0.0,
    linestyle="--"
)

plt.xlabel(
    "Relative time (s)"
)

plt.ylabel(
    "Mean-centered RAW counts"
)

plt.title(
    "ESK RAW: energy-event positions vs between-event controls"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "ESK_RAW_EVENT_VS_CONTROL.png",
    dpi=180
)

plt.close()


# ============================================================
# GRAPH 4
# MAX RAW SAMPLE-STEP POSITION
#
# If ADC/reset behaviour occurs at the energy-event time,
# these positions may cluster near zero.
# ============================================================

plt.figure(
    figsize=(14, 5)
)

plt.hist(
    result[
        "max_step_relative_s"
    ],
    bins=np.arange(
        -WINDOW_BEFORE_S,
        WINDOW_AFTER_S + 0.02,
        0.02
    )
)

plt.axvline(
    0.0,
    linestyle="--",
    label="Energy-event time"
)

plt.xlabel(
    "Position of largest RAW sample-to-sample step (s)"
)

plt.ylabel(
    "Number of events"
)

plt.title(
    "Where does the largest RAW step occur around each energy event?"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "ESK_RAW_MAX_STEP_POSITION.png",
    dpi=180
)

plt.close()


print()
print("=" * 80)
print("DONE")
print("=" * 80)

print()
print("Filter used       : NO")
print("Hilbert used      : NO")
print("FFT used          : NO")
print("Autocorrelation   : NO")
print("Samples discarded : 0")
print("Expected period   : NONE")

print()
print("Saved:")
print("  ESK_MAIN_PULSES_RAW_PROBE.csv")
print("  ESK_RAW_AROUND_FIRST_12_EVENTS.png")
print("  ESK_RAW_EVENT_TRIGGERED_AVERAGE.png")
print("  ESK_RAW_EVENT_VS_CONTROL.png")
print("  ESK_RAW_MAX_STEP_POSITION.png")