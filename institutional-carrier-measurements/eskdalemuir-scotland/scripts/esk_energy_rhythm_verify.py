import numpy as np
import pandas as pd
from scipy.signal import welch, find_peaks, detrend

# ============================================================
# BLIND VERIFICATION OF ENERGY RHYTHM
# Uses already-created 0.01 s energy series.
#
# IMPORTANT:
# No expected period is supplied.
# ============================================================

FILE = "ESK_CH1_2012_06_19_ENERGY_001S.csv"

FS = 100.0

# Analyse independent 10-minute blocks
BLOCK_SECONDS = 600

# Blind modulation search range
# 0.2 s to 30 s
MIN_PERIOD = 0.2
MAX_PERIOD = 30.0

# Peak detection for energy envelope
# Minimum separation is deliberately only 0.15 s,
# NOT an expected rhythm.
MIN_PEAK_DISTANCE_S = 0.15


print("=" * 72)
print("ESK BLIND ENERGY RHYTHM VERIFICATION")
print("=" * 72)

df = pd.read_csv(
    FILE,
    usecols=[
        "timestamp",
        "magnetic_energy_density_J_m3"
    ]
)

time = pd.to_datetime(df["timestamp"])
energy = df["magnetic_energy_density_J_m3"].to_numpy(
    dtype=np.float64
)

print("Samples :", f"{len(energy):,}")
print("Duration:", f"{len(energy)/FS/3600:.3f} h")
print()


# ============================================================
# PART 1
# BLIND DOMINANT PERIOD IN EACH INDEPENDENT BLOCK
# ============================================================

block_n = int(BLOCK_SECONDS * FS)

block_results = []

for start in range(0, len(energy) - block_n + 1, block_n):

    stop = start + block_n

    x = energy[start:stop]

    med = np.median(x)

    if not np.isfinite(med) or med <= 0:
        continue

    # Relative energy variation
    x = x / med - 1.0
    x = detrend(x)

    nperseg = min(len(x), 2**16)

    f, pxx = welch(
        x,
        fs=FS,
        window="hann",
        nperseg=nperseg,
        noverlap=nperseg // 2,
        detrend="linear",
        scaling="density"
    )

    fmin = 1.0 / MAX_PERIOD
    fmax = 1.0 / MIN_PERIOD

    mask = (
        (f >= fmin) &
        (f <= fmax)
    )

    ff = f[mask]
    pp = pxx[mask]

    if len(ff) == 0:
        continue

    # Blindly choose strongest spectral peak
    idx = np.argmax(pp)

    best_f = ff[idx]
    best_period = 1.0 / best_f

    block_results.append({
        "block_start": time.iloc[start],
        "frequency_Hz": best_f,
        "period_seconds": best_period,
        "PSD": pp[idx]
    })


blocks = pd.DataFrame(block_results)

blocks.to_csv(
    "ESK_CH1_2012_06_19_BLOCK_RHYTHMS.csv",
    index=False
)


print("=" * 72)
print("INDEPENDENT 10-MINUTE BLOCKS")
print("=" * 72)

print("Blocks analysed:", len(blocks))

if len(blocks):

    print(
        "Median blind period :",
        f"{blocks['period_seconds'].median():.6f} s"
    )

    print(
        "Mean blind period   :",
        f"{blocks['period_seconds'].mean():.6f} s"
    )

    print(
        "Std                 :",
        f"{blocks['period_seconds'].std():.6f} s"
    )

    print(
        "Q05-Q95             :",
        f"{blocks['period_seconds'].quantile(0.05):.6f}",
        "-",
        f"{blocks['period_seconds'].quantile(0.95):.6f}",
        "s"
    )

    print()
    print("First 20 blocks:")
    print(
        blocks[
            ["block_start", "frequency_Hz", "period_seconds"]
        ].head(20).to_string(index=False)
    )


# ============================================================
# PART 2
# PEAK-TO-PEAK TEST
#
# Smooth energy only very slightly (0.05 s)
# to suppress sample-level numerical jitter.
# This does NOT impose a multi-second period.
# ============================================================

SMOOTH_SECONDS = 0.05
smooth_n = max(1, int(SMOOTH_SECONDS * FS))

kernel = np.ones(smooth_n) / smooth_n

energy_smooth = np.convolve(
    energy,
    kernel,
    mode="same"
)


# Robust prominence threshold
median_e = np.median(energy_smooth)

mad_e = np.median(
    np.abs(energy_smooth - median_e)
)

prominence = 2.0 * mad_e

min_distance = int(
    MIN_PEAK_DISTANCE_S * FS
)


peaks, props = find_peaks(
    energy_smooth,
    distance=min_distance,
    prominence=prominence
)


peak_times_seconds = peaks / FS

intervals = np.diff(peak_times_seconds)


# Keep intervals inside our blind analysis range
valid = (
    (intervals >= MIN_PERIOD) &
    (intervals <= MAX_PERIOD)
)

intervals_valid = intervals[valid]


print()
print("=" * 72)
print("PEAK-TO-PEAK ENERGY TEST")
print("=" * 72)

print("Detected peaks:", f"{len(peaks):,}")
print(
    "Valid intervals:",
    f"{len(intervals_valid):,}"
)


if len(intervals_valid):

    print(
        "Median interval:",
        f"{np.median(intervals_valid):.6f} s"
    )

    print(
        "Mean interval  :",
        f"{np.mean(intervals_valid):.6f} s"
    )

    print(
        "MAD interval   :",
        f"{np.median(np.abs(
            intervals_valid -
            np.median(intervals_valid)
        )):.6f} s"
    )


# ============================================================
# HISTOGRAM - automatically determine common spacings
# 0.01 s bins, matching original temporal resolution
# ============================================================

bins = np.arange(
    MIN_PERIOD,
    MAX_PERIOD + 0.01,
    0.01
)

hist, edges = np.histogram(
    intervals_valid,
    bins=bins
)

centres = (
    edges[:-1] +
    edges[1:]
) / 2


top = np.argsort(hist)[::-1][:20]


hist_results = []

for idx in top:

    if hist[idx] == 0:
        continue

    hist_results.append({
        "interval_seconds": centres[idx],
        "count": hist[idx]
    })


hist_df = pd.DataFrame(hist_results)

hist_df.to_csv(
    "ESK_CH1_2012_06_19_PEAK_INTERVALS.csv",
    index=False
)


print()
print("MOST COMMON PEAK SPACINGS")
print("-" * 72)

for i, row in hist_df.iterrows():

    print(
        f"{i+1:2d}. "
        f"{row['interval_seconds']:.3f} s"
        f"   count = {int(row['count'])}"
    )


# ============================================================
# PART 3
# Does one period dominate repeatedly through the day?
#
# We do NOT specify which period.
# Automatically cluster block periods to 0.01 s bins.
# ============================================================

if len(blocks):

    p = blocks["period_seconds"].to_numpy()

    pbins = np.arange(
        MIN_PERIOD,
        MAX_PERIOD + 0.01,
        0.01
    )

    phist, pedges = np.histogram(
        p,
        bins=pbins
    )

    pcentres = (
        pedges[:-1] +
        pedges[1:]
    ) / 2

    ptop = np.argsort(phist)[::-1][:10]

    print()
    print("=" * 72)
    print("MOST COMMON BLIND BLOCK PERIODS")
    print("=" * 72)

    for rank, idx in enumerate(ptop, start=1):

        if phist[idx] == 0:
            continue

        print(
            f"{rank:2d}. "
            f"{pcentres[idx]:.3f} s"
            f"   blocks = {phist[idx]}"
        )


print()
print("=" * 72)
print("DONE")
print("=" * 72)

print()
print(
    "No expected modulation period was supplied."
)