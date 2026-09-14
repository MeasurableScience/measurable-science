#!/usr/bin/env python3

import glob
import numpy as np
import pandas as pd
import cdflib

from scipy.signal import butter, sosfiltfilt, hilbert

# ============================================================
# ISTOK — 5 MINUTE H-D SHIFT NULL TEST
# ============================================================

FS = 64.0

LO = 6.321
HI = 8.267

SHIFT_MINUTES = 5
SHIFT_SAMPLES = int(SHIFT_MINUTES * 60 * FS)

MINUTE_SECONDS = 60

OUT_CSV = "IST_SHIFT_NULL_5MIN.csv"
OUT_SUMMARY = "IST_SHIFT_NULL_5MIN_SUMMARY.csv"


# ============================================================
# FILTER
# ============================================================

sos = butter(
    4,
    [LO, HI],
    btype="bandpass",
    fs=FS,
    output="sos"
)


# ============================================================
# LOAD ISTOK
# ============================================================

paths = sorted(glob.glob("isee_induction_ist_*.cdf"))

if not paths:
    raise RuntimeError("No IST CDF found")

path = paths[0]

cdf = cdflib.CDF(path)

epoch = cdf.varget("epoch_db_dt")

times = np.asarray(
    cdflib.cdfepoch.to_datetime(epoch),
    dtype="datetime64[ns]"
)

x = np.asarray(
    cdf.varget("db_dt"),
    dtype=float
)

H = x[:, 0]
D = x[:, 1]


# ============================================================
# VALID DATA
# ============================================================

good = (
    np.isfinite(H) &
    np.isfinite(D) &
    (H > -1e30) &
    (D > -1e30)
)

times = times[good]
H = H[good]
D = D[good]

H = H - np.mean(H)
D = D - np.mean(D)


# ============================================================
# FILTER WHOLE DAY ONCE
# ============================================================

print("Filtering full day...")

Hf = sosfiltfilt(sos, H)
Df = sosfiltfilt(sos, D)

if len(Hf) <= SHIFT_SAMPLES:
    raise RuntimeError("Record too short for shift")


# ============================================================
# GEOMETRY FUNCTION
# ============================================================

def geometry(h, d):

    # One COMMON scale preserves H:D amplitude relationship
    scale = np.sqrt(
        np.mean(h**2 + d**2)
    )

    if not np.isfinite(scale) or scale == 0:
        return None

    hn = h / scale
    dn = d / scale

    # --------------------------------------------------------
    # PHASE / PLV
    # --------------------------------------------------------

    ah = hilbert(hn)
    ad = hilbert(dn)

    ph = np.angle(ah)
    pd_ = np.angle(ad)

    z = np.mean(
        np.exp(1j * (pd_ - ph))
    )

    plv = np.abs(z)
    phase_deg = np.degrees(np.angle(z))

    # --------------------------------------------------------
    # PCA
    # --------------------------------------------------------

    M = np.column_stack((hn, dn))

    cov = np.cov(
        M,
        rowvar=False
    )

    vals, vecs = np.linalg.eigh(cov)

    order = np.argsort(vals)[::-1]

    vals = vals[order]
    vecs = vecs[:, order]

    major = vals[0]
    minor = vals[1]

    if major <= 0 or minor < 0:
        return None

    pca_ratio = minor / major

    axis_ratio = np.sqrt(
        minor / major
    )

    v = vecs[:, 0]

    orientation = np.degrees(
        np.arctan2(v[1], v[0])
    )

    # 180 degree ambiguity
    if orientation >= 90:
        orientation -= 180

    if orientation < -90:
        orientation += 180

    # --------------------------------------------------------
    # ROTATION
    # --------------------------------------------------------

    signed_area = np.sum(
        hn[:-1] * dn[1:] -
        dn[:-1] * hn[1:]
    )

    rotation = (
        "CCW"
        if signed_area > 0
        else "CW"
    )

    return {
        "PLV": plv,
        "Phase_D_minus_H_deg": phase_deg,
        "PCA_Minor_Major": pca_ratio,
        "Axis_Ratio": axis_ratio,
        "Orientation_deg": orientation,
        "Signed_Area": signed_area,
        "Rotation": rotation
    }


# ============================================================
# COMMON TIME RANGE
#
# We remove last 5 minutes so REAL and SHIFTED
# use exactly same H time windows.
# ============================================================

max_time = times[-1] - np.timedelta64(
    SHIFT_MINUTES,
    "m"
)

first_minute = times[0].astype(
    "datetime64[m]"
)

last_minute = max_time.astype(
    "datetime64[m]"
)

minutes = np.arange(
    first_minute,
    last_minute + np.timedelta64(1, "m"),
    np.timedelta64(1, "m")
)


rows = []


# ============================================================
# PROCESS MINUTES
# ============================================================

for start in minutes:

    end = start + np.timedelta64(
        1,
        "m"
    )

    # use searchsorted rather than scanning whole day
    i0 = np.searchsorted(
        times,
        start,
        side="left"
    )

    i1 = np.searchsorted(
        times,
        end,
        side="left"
    )

    n = i1 - i0

    if n < int(FS * 60 * 0.95):
        continue

    # shifted D must exist
    if i1 + SHIFT_SAMPLES > len(Df):
        continue

    # --------------------------------------------------------
    # REAL PAIR
    # --------------------------------------------------------

    h_real = Hf[i0:i1]
    d_real = Df[i0:i1]

    # --------------------------------------------------------
    # SHIFTED PAIR
    #
    # H(t) vs D(t + 5 min)
    # --------------------------------------------------------

    h_shift = Hf[i0:i1]

    d_shift = Df[
        i0 + SHIFT_SAMPLES:
        i1 + SHIFT_SAMPLES
    ]

    if len(h_shift) != len(d_shift):
        continue

    real = geometry(
        h_real,
        d_real
    )

    shifted = geometry(
        h_shift,
        d_shift
    )

    if real is None or shifted is None:
        continue

    row = {
        "UTC_Start": str(start)
    }

    for k, v in real.items():
        row["REAL_" + k] = v

    for k, v in shifted.items():
        row["SHIFT_" + k] = v

    rows.append(row)


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(rows)

if df.empty:
    raise RuntimeError(
        "No usable windows"
    )

df.to_csv(
    OUT_CSV,
    index=False
)


# ============================================================
# SUMMARY FUNCTION
# ============================================================

def summarize(prefix):

    rot = df[
        prefix + "_Rotation"
    ]

    cw = int(
        np.sum(rot == "CW")
    )

    ccw = int(
        np.sum(rot == "CCW")
    )

    n = len(rot)

    return {
        "Windows": n,

        "Median_PLV":
            df[
                prefix + "_PLV"
            ].median(),

        "Median_Phase_deg":
            df[
                prefix +
                "_Phase_D_minus_H_deg"
            ].median(),

        "Median_Axis_Ratio":
            df[
                prefix +
                "_Axis_Ratio"
            ].median(),

        "Median_Orientation_deg":
            df[
                prefix +
                "_Orientation_deg"
            ].median(),

        "Orientation_STD_deg":
            df[
                prefix +
                "_Orientation_deg"
            ].std(),

        "CW_Count": cw,
        "CCW_Count": ccw,

        "CW_Percent":
            100.0 * cw / n,

        "CCW_Percent":
            100.0 * ccw / n
    }


real_summary = summarize("REAL")
shift_summary = summarize("SHIFT")


summary = pd.DataFrame([
    {
        "Test": "REAL",
        **real_summary
    },
    {
        "Test": "SHIFTED_5MIN",
        **shift_summary
    }
])

summary.to_csv(
    OUT_SUMMARY,
    index=False
)


# ============================================================
# OUTPUT
# ============================================================

print()
print("=" * 80)
print("ISTOK — 5 MINUTE SHIFT NULL TEST")
print("=" * 80)

print()
print(summary.to_string(index=False))

print()
print("Shift used:")
print(
    f"H(t) versus D(t + {SHIFT_MINUTES} min)"
)

print()
print("Saved:")
print(" ", OUT_CSV)
print(" ", OUT_SUMMARY)