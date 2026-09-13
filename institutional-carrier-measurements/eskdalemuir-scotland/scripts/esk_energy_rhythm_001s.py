import os
import glob
import re
import numpy as np
import pandas as pd

from scipy.signal import (
    butter,
    sosfiltfilt,
    hilbert,
    welch,
    find_peaks,
    detrend
)

# ============================================================
# ESKDALEMUIR - BLIND ENERGY RHYTHM SEARCH
# One day, CH1, full 100 Hz temporal resolution
#
# IMPORTANT:
# - Carrier band was found previously: 6.8-8.2 Hz
# - NO modulation/rhythm frequency is supplied to this script.
# - The script asks: how does the ENERGY of that band vary?
# ============================================================

DATA_FOLDER = "."

CHANNEL = "CH1"

YEAR = 2012
MONTH = 6
DAY = 19

FS = 100.0

# Already independently identified carrier band
F_LOW = 6.8
F_HIGH = 8.2

# CH1 digitizer calibration
V_PER_COUNT = 3.491e-6       # V/count

MU0 = 4.0 * np.pi * 1e-7

# Model geometry - ONLY for optional U_model output
R_EARTH = 6_371_000.0
HEIGHT = 50_000.0
MODEL_AREA = np.pi * R_EARTH**2      # 1/4 Earth surface
MODEL_VOLUME = MODEL_AREA * HEIGHT

# ------------------------------------------------------------
# BGS / Nishizawa et al. calibration table
# Frequency [Hz] -> response [mV/nT]
# ------------------------------------------------------------

CAL_FREQ = np.array([
    0.001,
    0.002,
    0.003,
    0.005,
    0.007,
    0.010,
    0.018,
    0.032,
    0.056,
    0.10,
    0.18,
    0.32,
    0.56,
    1.0,
    1.8,
    3.2,
    5.6,
    10.0,
    18.0,
    32.0,
    50.0,
    100.0
], dtype=float)

CAL_MV_PER_NT = np.array([
    4.530,
    13.736,
    22.464,
    34.041,
    40.402,
    44.639,
    48.237,
    49.540,
    49.939,
    50.077,
    50.139,
    50.157,
    50.167,
    50.169,
    50.200,
    50.199,
    50.204,
    50.209,
    50.223,
    50.258,
    50.282,
    50.151
], dtype=float)


# ============================================================
# READ RAW DAT
# ============================================================

def read_dat(filename):

    data = []

    with open(filename, "r", errors="ignore") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:
                value = float(line)
                data.append(value)
            except ValueError:
                continue

    return np.asarray(data, dtype=np.float64)


# ============================================================
# CALIBRATION
# ============================================================

def calibration_response(freq_hz):

    """
    Interpolated response in V/T.
    Table is mV/nT.

    1 mV/nT = 1e6 V/T
    """

    response_mv_nt = np.interp(
        freq_hz,
        CAL_FREQ,
        CAL_MV_PER_NT
    )

    return response_mv_nt * 1e6


# Because response is essentially flat across 6.8-8.2 Hz,
# use response at band centre for time-domain amplitude.
F_CENTER = (F_LOW + F_HIGH) / 2.0

RESPONSE_V_PER_T = calibration_response(F_CENTER)

TESLA_PER_COUNT = V_PER_COUNT / RESPONSE_V_PER_T


# ============================================================
# FIND DAY FILES
# ============================================================

pattern = os.path.join(
    DATA_FOLDER,
    f"{CHANNEL}_{YEAR:04d}_{MONTH:02d}_{DAY:02d}_*.dat"
)

files = glob.glob(pattern)


def get_hour(filename):

    name = os.path.basename(filename)

    m = re.search(
        rf"{CHANNEL}_{YEAR:04d}_{MONTH:02d}_{DAY:02d}_(\d{{2}})\.dat$",
        name
    )

    if m:
        return int(m.group(1))

    return 999


files = sorted(files, key=get_hour)

if len(files) == 0:
    raise RuntimeError(
        f"No files found for "
        f"{CHANNEL} {YEAR:04d}-{MONTH:02d}-{DAY:02d}"
    )


print()
print("=" * 72)
print("ESK ENERGY RHYTHM SEARCH")
print("=" * 72)

print("Date             :", f"{YEAR:04d}-{MONTH:02d}-{DAY:02d}")
print("Channel          :", CHANNEL)
print("Carrier band     :", f"{F_LOW}-{F_HIGH} Hz")
print("Sampling         :", FS, "Hz")
print("Time resolution  : 0.01 s")
print("Files found      :", len(files))
print("Tesla/count      :", f"{TESLA_PER_COUNT:.12e}")
print()


# ============================================================
# PROCESS EACH HOUR SEPARATELY
#
# This avoids filtering across file boundaries/gaps.
# We discard edge seconds because filtfilt/Hilbert edges
# can produce artificial amplitude changes.
# ============================================================

sos = butter(
    4,
    [F_LOW, F_HIGH],
    btype="bandpass",
    fs=FS,
    output="sos"
)

EDGE_SECONDS = 5.0
EDGE_SAMPLES = int(EDGE_SECONDS * FS)

all_time = []
all_amplitude = []
all_energy_density = []
all_model_energy = []

total_samples = 0

for filename in files:

    hour = get_hour(filename)

    raw = read_dat(filename)

    print(
        os.path.basename(filename),
        " samples:",
        f"{len(raw):,}"
    )

    if len(raw) < 10 * FS:
        print("  SKIP - too short")
        continue

    total_samples += len(raw)

    # Remove DC offset
    raw = raw - np.mean(raw)

    # counts -> Tesla
    b_tesla = raw * TESLA_PER_COUNT

    # Isolate previously found carrier band
    filtered = sosfiltfilt(sos, b_tesla)

    # Analytic signal
    analytic = hilbert(filtered)

    # trenutna RMS amplituda nosača
    B_rms = np.abs(analytic) / np.sqrt(2)

    # magnetna energijska gustina
    u_b = B_rms**2 / (2 * MU0)

    U_model = u_b * MODEL_VOLUME

    # Remove filter/Hilbert edge artifacts
    if len(raw) > 2 * EDGE_SAMPLES:

        amplitude_peak = amplitude_peak[
            EDGE_SAMPLES:-EDGE_SAMPLES
        ]

        u_b = u_b[
            EDGE_SAMPLES:-EDGE_SAMPLES
        ]

        U_model = U_model[
            EDGE_SAMPLES:-EDGE_SAMPLES
        ]

        start_seconds = EDGE_SECONDS

    else:
        start_seconds = 0.0

    n = len(u_b)

    seconds_inside_hour = (
        start_seconds +
        np.arange(n) / FS
    )

    base = pd.Timestamp(
        year=YEAR,
        month=MONTH,
        day=DAY,
        hour=hour
    )

    timestamps = (
        base +
        pd.to_timedelta(
            seconds_inside_hour,
            unit="s"
        )
    )

    all_time.append(timestamps)
    all_amplitude.append(amplitude_peak)
    all_energy_density.append(u_b)
    all_model_energy.append(U_model)


# ============================================================
# JOIN DAY
# ============================================================

time = np.concatenate(all_time)

amplitude = np.concatenate(all_amplitude)

energy = np.concatenate(all_energy_density)

model_energy = np.concatenate(all_model_energy)


print()
print("=" * 72)
print("DAY SUMMARY")
print("=" * 72)

print("Raw samples read :", f"{total_samples:,}")
print("Energy samples   :", f"{len(energy):,}")

print(
    "Duration approx :",
    f"{len(energy) / FS / 3600:.3f} h"
)

print(
    "Median amplitude:",
    f"{np.median(amplitude) * 1e9:.9f} nT peak"
)

print(
    "Median u_B      :",
    f"{np.median(energy):.9e} J/m^3"
)

print(
    "Median U_model  :",
    f"{np.median(model_energy):.9e} J"
)


# ============================================================
# SAVE FULL 0.01 s SERIES
# ============================================================

df = pd.DataFrame({

    "timestamp": time,

    "B_envelope_peak_T": amplitude,

    "B_envelope_peak_nT":
        amplitude * 1e9,

    "magnetic_energy_density_J_m3":
        energy,

    "model_energy_J":
        model_energy
})


output_full = (
    f"ESK_{CHANNEL}_"
    f"{YEAR:04d}_{MONTH:02d}_{DAY:02d}_"
    f"ENERGY_001S.csv"
)

df.to_csv(
    output_full,
    index=False
)

print()
print("Saved:", output_full)


# ============================================================
# BLIND RHYTHM SEARCH
#
# IMPORTANT:
# We do NOT insert any expected rhythm.
#
# To avoid gaps between incomplete files creating false
# frequencies, the spectral search below uses only the
# longest continuous run.
# ============================================================

# Find time gaps larger than 1.5 samples

time_ns = pd.to_datetime(time).astype("int64").to_numpy()

dt = np.diff(time_ns) / 1e9

breaks = np.where(dt > (1.5 / FS))[0]


starts = np.concatenate(([0], breaks + 1))

ends = np.concatenate((breaks + 1, [len(energy)]))

lengths = ends - starts

best = np.argmax(lengths)

i0 = starts[best]
i1 = ends[best]

energy_cont = energy[i0:i1]


print()
print("=" * 72)
print("BLIND RHYTHM SEARCH")
print("=" * 72)

print(
    "Longest continuous segment:",
    f"{len(energy_cont) / FS:.2f} seconds"
)


# ============================================================
# NORMALISE / DETREND
# ============================================================

x = np.asarray(
    energy_cont,
    dtype=np.float64
)

# Relative variations around median
median_x = np.median(x)

if median_x == 0:
    raise RuntimeError(
        "Median energy is zero - cannot normalise."
    )

x = x / median_x - 1.0

x = detrend(x)


# ============================================================
# WELCH PERIOD SEARCH
#
# Search modulation frequencies only.
# Carrier itself is NOT being searched here.
#
# Since energy envelope is sampled at 100 Hz,
# Nyquist = 50 Hz.
#
# We report only modulation below 5 Hz initially,
# because the physical question is slower variation
# of carrier energy.
# ============================================================

NPERSEG = min(
    len(x),
    2**20
)

f, pxx = welch(
    x,
    fs=FS,
    window="hann",
    nperseg=NPERSEG,
    noverlap=NPERSEG // 2,
    detrend="linear",
    scaling="density"
)


# Exclude zero / ultra-slow edge
mask = (
    (f >= 1.0 / 3600.0) &
    (f <= 5.0)
)

fm = f[mask]
pm = pxx[mask]


# ============================================================
# FIND SPECTRAL PEAKS BLINDLY
# ============================================================

peaks, properties = find_peaks(
    pm,
    prominence=np.median(pm) * 5.0
)

if len(peaks) == 0:

    # fallback: simply take strongest bins
    candidates = np.argsort(pm)[::-1][:20]

else:

    candidates = peaks[
        np.argsort(pm[peaks])[::-1]
    ][:20]


results = []

for idx in candidates:

    freq = fm[idx]

    if freq <= 0:
        continue

    period = 1.0 / freq

    results.append({
        "frequency_Hz": freq,
        "period_seconds": period,
        "period_minutes": period / 60.0,
        "period_hours": period / 3600.0,
        "PSD": pm[idx]
    })


rhythm_df = pd.DataFrame(results)


output_rhythm = (
    f"ESK_{CHANNEL}_"
    f"{YEAR:04d}_{MONTH:02d}_{DAY:02d}_"
    f"BLIND_ENERGY_RHYTHMS.csv"
)

rhythm_df.to_csv(
    output_rhythm,
    index=False
)


print()
print("TOP BLIND ENERGY RHYTHMS")
print("-" * 72)

if len(rhythm_df):

    for i, row in rhythm_df.head(15).iterrows():

        p = row["period_seconds"]

        if p < 60:

            ptext = f"{p:.6f} s"

        elif p < 3600:

            ptext = f"{p/60:.6f} min"

        else:

            ptext = f"{p/3600:.6f} h"

        print(
            f"{i+1:2d}. "
            f"f = {row['frequency_Hz']:.9f} Hz"
            f"   period = {ptext}"
            f"   PSD = {row['PSD']:.6e}"
        )

else:

    print("No spectral peaks detected.")


print()
print("Saved:", output_rhythm)


# ============================================================
# SHORT-LAG AUTOCORRELATION
#
# Direct autocorrelation of 8.6 million samples is expensive.
# For the first test we inspect 0.1-300 second repetition
# using FFT autocorrelation on a manageable continuous block.
# ============================================================

AUTO_MAX_SECONDS = 300.0

# Use up to first 30 minutes of longest continuous segment
auto_n = min(
    len(x),
    int(30 * 60 * FS)
)

xa = x[:auto_n]

xa = xa - np.mean(xa)

nfft = 1 << int(
    np.ceil(
        np.log2(2 * len(xa))
    )
)

X = np.fft.rfft(
    xa,
    n=nfft
)

acf = np.fft.irfft(
    X * np.conjugate(X),
    n=nfft
)[:len(xa)]

acf = acf / acf[0]

max_lag = min(
    int(AUTO_MAX_SECONDS * FS),
    len(acf) - 1
)

acf_short = acf[:max_lag + 1]

lags = (
    np.arange(len(acf_short))
    / FS
)


# Ignore zero lag and first 0.1 s
min_lag_samples = int(0.1 * FS)

acf_peaks, acf_props = find_peaks(
    acf_short[min_lag_samples:],
    prominence=0.01
)

acf_peaks = (
    acf_peaks +
    min_lag_samples
)


if len(acf_peaks):

    order = np.argsort(
        acf_short[acf_peaks]
    )[::-1]

    acf_peaks = acf_peaks[order][:20]


acf_results = []

for idx in acf_peaks:

    acf_results.append({
        "lag_seconds": lags[idx],
        "correlation": acf_short[idx]
    })


acf_df = pd.DataFrame(acf_results)


output_acf = (
    f"ESK_{CHANNEL}_"
    f"{YEAR:04d}_{MONTH:02d}_{DAY:02d}_"
    f"AUTOCORR_RHYTHMS.csv"
)

acf_df.to_csv(
    output_acf,
    index=False
)


print()
print("=" * 72)
print("TOP AUTOCORRELATION LAGS")
print("=" * 72)

if len(acf_df):

    for i, row in acf_df.head(15).iterrows():

        print(
            f"{i+1:2d}. "
            f"lag = {row['lag_seconds']:.6f} s"
            f"   correlation = "
            f"{row['correlation']:.6f}"
        )

else:

    print(
        "No strong short-lag autocorrelation "
        "peaks detected."
    )


print()
print("Saved:", output_acf)

print()
print("=" * 72)
print("DONE")
print("=" * 72)
print()
print(
    "IMPORTANT: no expected modulation period "
    "was supplied to the search."
)
print(
    "Carrier band 6.8-8.2 Hz is the only "
    "previously determined frequency constraint."
)