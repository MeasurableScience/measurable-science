from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter

# ============================================================
# BLIND MOON SPECTRUM ANALYSIS
#
# PURPOSE:
#   Find spectral structures WITHOUT knowing expected
#   wavelengths of Ne, Na, H, etc.
#
# INPUT:
#   004_measurementsMoonSpectrum_OliNo.org_.csv
#
# OUTPUT:
#   blind_candidates.csv
#   moon_spectrum.png
#   moon_detrended.png
#
# IMPORTANT:
#   Do NOT compare candidates with atomic line tables
#   until blind_candidates.csv has been frozen/saved.
# ============================================================

BASE = Path(__file__).resolve().parent

CSV_FILE = BASE / "004_measurementsMoonSpectrum_OliNo.org_.csv"

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

# OliNo sampling is approximately 1 nm.
# We avoid the very edges because detector response can become poor.
ANALYSIS_MIN_NM = 350.0
ANALYSIS_MAX_NM = 900.0

# Width used to estimate the slowly varying continuum.
# Must be much wider than a narrow spectral feature.
CONTINUUM_WINDOW_NM = 31.0

# Minimum prominence in robust-sigma units.
# 3.0 is intentionally not extremely strict for the first blind pass.
MIN_PROMINENCE_SIGMA = 3.0

# Candidate peaks must be separated by at least this amount.
MIN_DISTANCE_NM = 2.0


# ============================================================
# READ CSV
# ============================================================

def read_olino_csv(path):
    """
    OliNo files may contain metadata before the numerical table,
    so search for the beginning of the wavelength table.
    """

    raw_lines = path.read_text(
        encoding="utf-8",
        errors="replace"
    ).splitlines()

    print(f"File: {path.name}")
    print(f"Total text lines: {len(raw_lines)}")

    # Print first lines so we know exactly what file structure we received.
    print("\nFIRST 25 LINES:")
    print("-" * 70)

    for i, line in enumerate(raw_lines[:25], start=1):
        print(f"{i:3d}: {line}")

    print("-" * 70)

    # Instead of trusting headers, extract rows whose first field
    # is a plausible wavelength.
    rows = []

    for line in raw_lines:
        # OliNo CSV can use ; as delimiter.
        if ";" in line:
            parts = line.split(";")
        elif "," in line:
            parts = line.split(",")
        elif "\t" in line:
            parts = line.split("\t")
        else:
            continue

        parts = [p.strip().replace('"', '') for p in parts]

        if len(parts) < 2:
            continue

        try:
            wavelength_text = parts[0].lower().replace("nm", "").strip()
            wavelength = float(wavelength_text.replace(",", "."))
        except ValueError:
            continue

        # Wavelength sanity check
        if not 200 <= wavelength <= 1200:
            continue

        # Find the first usable numeric measurement after wavelength.
        numbers = []

        for p in parts[1:]:
            p2 = p.replace(",", ".")

            try:
                numbers.append(float(p2))
            except ValueError:
                numbers.append(np.nan)

        if len(numbers) == 0:
            continue

        rows.append([wavelength] + numbers)

    if not rows:
        raise RuntimeError(
            "No spectral rows found. Check the printed first lines."
        )

    # Pad rows because metadata/export formats can contain different columns.
    max_len = max(len(r) for r in rows)

    padded = [
        r + [np.nan] * (max_len - len(r))
        for r in rows
    ]

    columns = ["wavelength_nm"] + [
        f"value_{i}"
        for i in range(1, max_len)
    ]

    df = pd.DataFrame(padded, columns=columns)

    return df


df = read_olino_csv(CSV_FILE)

print("\nDetected numerical table:")
print(df.head())
print()
print(df.tail())
print()
print(f"Rows: {len(df)}")
print(f"Wavelength range: "
      f"{df.wavelength_nm.min():.3f} - "
      f"{df.wavelength_nm.max():.3f} nm")


# ============================================================
# FIND BEST SPECTRAL VALUE COLUMN
# ============================================================

# We want the measurement column containing the largest number
# of finite, varying values.
candidate_columns = []

for col in df.columns:
    if col == "wavelength_nm":
        continue

    values = df[col].to_numpy(dtype=float)

    finite = np.isfinite(values)

    if finite.sum() < 100:
        continue

    std = np.nanstd(values)

    if std <= 0:
        continue

    candidate_columns.append(
        (col, finite.sum(), std)
    )

if not candidate_columns:
    raise RuntimeError("Could not find spectral measurement column.")

print("\nPossible measurement columns:")

for item in candidate_columns:
    print(item)

# Usually first valid measurement column is spectral radiance.
SIGNAL_COLUMN = candidate_columns[0][0]

print(f"\nUsing signal column: {SIGNAL_COLUMN}")


# ============================================================
# CLEAN DATA
# ============================================================

wave = df["wavelength_nm"].to_numpy(dtype=float)
signal = df[SIGNAL_COLUMN].to_numpy(dtype=float)

mask = (
    np.isfinite(wave)
    & np.isfinite(signal)
    & (wave >= ANALYSIS_MIN_NM)
    & (wave <= ANALYSIS_MAX_NM)
    & (signal > 0)
)

wave = wave[mask]
signal = signal[mask]

order = np.argsort(wave)

wave = wave[order]
signal = signal[order]

print(f"\nAnalysis points: {len(wave)}")
print(
    f"Analysis range: {wave.min():.2f} - "
    f"{wave.max():.2f} nm"
)

sampling = np.median(np.diff(wave))

print(f"Median wavelength step: {sampling:.4f} nm")


# ============================================================
# CONTINUUM REMOVAL
# ============================================================

window_points = int(
    round(CONTINUUM_WINDOW_NM / sampling)
)

# Savitzky-Golay requires odd window.
if window_points % 2 == 0:
    window_points += 1

window_points = max(window_points, 7)

if window_points >= len(signal):
    window_points = len(signal) - 1

    if window_points % 2 == 0:
        window_points -= 1

print(
    f"Continuum window: {window_points} points "
    f"(~{window_points * sampling:.1f} nm)"
)

continuum = savgol_filter(
    signal,
    window_length=window_points,
    polyorder=3
)

# Fractional residual:
#
# positive = local emission-like structure
# negative = local absorption-like structure

residual = (signal - continuum) / continuum


# ============================================================
# ROBUST NOISE ESTIMATE
# ============================================================

median_residual = np.median(residual)

mad = np.median(
    np.abs(residual - median_residual)
)

robust_sigma = 1.4826 * mad

print(f"Residual MAD: {mad:.6g}")
print(f"Robust sigma: {robust_sigma:.6g}")

threshold = MIN_PROMINENCE_SIGMA * robust_sigma

print(
    f"Blind prominence threshold: "
    f"{threshold:.6g} "
    f"({MIN_PROMINENCE_SIGMA:.1f} sigma)"
)


# ============================================================
# BLIND PEAK SEARCH
# ============================================================

distance_points = max(
    1,
    int(round(MIN_DISTANCE_NM / sampling))
)

# Positive residuals = emission-like
emission_idx, emission_props = find_peaks(
    residual,
    prominence=threshold,
    distance=distance_points
)

# Negative residuals = absorption-like
absorption_idx, absorption_props = find_peaks(
    -residual,
    prominence=threshold,
    distance=distance_points
)


# ============================================================
# BUILD CANDIDATE TABLE
# ============================================================

records = []

for n, idx in enumerate(emission_idx):
    records.append({
        "wavelength_nm": wave[idx],
        "type": "EMISSION_LIKE",
        "signal": signal[idx],
        "continuum": continuum[idx],
        "fractional_residual": residual[idx],
        "prominence": emission_props["prominences"][n],
        "sigma_score":
            emission_props["prominences"][n] / robust_sigma
    })

for n, idx in enumerate(absorption_idx):
    records.append({
        "wavelength_nm": wave[idx],
        "type": "ABSORPTION_LIKE",
        "signal": signal[idx],
        "continuum": continuum[idx],
        "fractional_residual": residual[idx],
        "prominence": absorption_props["prominences"][n],
        "sigma_score":
            absorption_props["prominences"][n] / robust_sigma
    })

candidates = pd.DataFrame(records)

if len(candidates):
    candidates = candidates.sort_values(
        "wavelength_nm"
    ).reset_index(drop=True)

    candidates.insert(
        0,
        "candidate_id",
        [
            f"C{i:03d}"
            for i in range(1, len(candidates) + 1)
        ]
    )

else:
    candidates = pd.DataFrame(
        columns=[
            "candidate_id",
            "wavelength_nm",
            "type",
            "signal",
            "continuum",
            "fractional_residual",
            "prominence",
            "sigma_score"
        ]
    )


# ============================================================
# SAVE FROZEN BLIND RESULT
# ============================================================

OUTPUT_CSV = BASE / "blind_candidates.csv"

candidates.to_csv(
    OUTPUT_CSV,
    index=False,
    float_format="%.8g"
)

print("\n" + "=" * 70)
print("BLIND CANDIDATES")
print("=" * 70)

if len(candidates):
    print(
        candidates[
            [
                "candidate_id",
                "wavelength_nm",
                "type",
                "sigma_score"
            ]
        ].to_string(index=False)
    )
else:
    print("No candidates passed threshold.")

print("\nTOTAL:")
print(f"Emission-like:   {len(emission_idx)}")
print(f"Absorption-like: {len(absorption_idx)}")
print(f"All candidates:  {len(candidates)}")

print(f"\nFrozen result saved to:")
print(OUTPUT_CSV)


# ============================================================
# GRAPH 1 — ORIGINAL SPECTRUM
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    wave,
    signal,
    linewidth=0.8,
    label="Measured spectrum"
)

plt.plot(
    wave,
    continuum,
    linewidth=1.2,
    label="Estimated continuum"
)

plt.xlabel("Wavelength (nm)")
plt.ylabel("Measured spectral value")
plt.title("OliNo Moon Spectrum — Blind Analysis")
plt.legend()
plt.grid(alpha=0.2)

plt.tight_layout()

OUT1 = BASE / "moon_spectrum.png"

plt.savefig(
    OUT1,
    dpi=180
)

plt.show()


# ============================================================
# GRAPH 2 — CONTINUUM REMOVED
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    wave,
    residual,
    linewidth=0.8
)

plt.axhline(
    0,
    linewidth=0.8
)

plt.axhline(
    threshold,
    linestyle="--",
    linewidth=0.8
)

plt.axhline(
    -threshold,
    linestyle="--",
    linewidth=0.8
)

if len(emission_idx):
    plt.scatter(
        wave[emission_idx],
        residual[emission_idx],
        marker="^",
        label="Emission-like candidates"
    )

if len(absorption_idx):
    plt.scatter(
        wave[absorption_idx],
        residual[absorption_idx],
        marker="v",
        label="Absorption-like candidates"
    )

plt.xlabel("Wavelength (nm)")
plt.ylabel("(signal - continuum) / continuum")
plt.title(
    "OliNo Moon Spectrum — Blind Local Spectral Structures"
)

plt.legend()
plt.grid(alpha=0.2)

plt.tight_layout()

OUT2 = BASE / "moon_detrended.png"

plt.savefig(
    OUT2,
    dpi=180
)

plt.show()

print("\nGraphs saved:")
print(OUT1)
print(OUT2)

print("\nIMPORTANT:")
print(
    "Do not compare these wavelengths with atomic line tables yet."
)
print(
    "blind_candidates.csv is the frozen blind result."
)