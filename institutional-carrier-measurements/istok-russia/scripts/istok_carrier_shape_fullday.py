#!/usr/bin/env python3

import glob
import numpy as np
import pandas as pd
import cdflib
import matplotlib.pyplot as plt

from scipy.signal import butter, sosfiltfilt, hilbert

FS = 64.0
LO = 6.321
HI = 8.267

paths = sorted(glob.glob("isee_induction_ist_*.cdf"))

if not paths:
    raise RuntimeError("No IST CDF found")

sos = butter(
    4, [LO, HI],
    btype="bandpass",
    fs=FS,
    output="sos"
)

rows = []
examples = []

for path in paths:

    cdf = cdflib.CDF(path)

    epoch = cdf.varget("epoch_db_dt")
    t = np.asarray(
        cdflib.cdfepoch.to_datetime(epoch),
        dtype="datetime64[ns]"
    )

    x = np.asarray(cdf.varget("db_dt"), dtype=float)

    H = x[:, 0]
    D = x[:, 1]

    good = (
        np.isfinite(H) &
        np.isfinite(D) &
        (H > -1e30) &
        (D > -1e30)
    )

    t = t[good]
    H = H[good]
    D = D[good]

    # remove DC offset
    H = H - np.mean(H)
    D = D - np.mean(D)

    # filter whole continuous day once
    Hf = sosfiltfilt(sos, H)
    Df = sosfiltfilt(sos, D)

    first = t[0].astype("datetime64[m]")
    last  = t[-1].astype("datetime64[m]")

    minutes = np.arange(
        first,
        last + np.timedelta64(1, "m"),
        np.timedelta64(1, "m")
    )

    for start in minutes:

        end = start + np.timedelta64(1, "m")

        m = (t >= start) & (t < end)

        if np.sum(m) < int(FS * 60 * 0.95):
            continue

        h = Hf[m]
        d = Df[m]

        # normalize separately so shape is not dominated
        # simply by channel amplitude
        scale = np.sqrt(np.mean(h**2 + d**2))

        if scale == 0:
            continue

        hn = h / scale
        dn = d / scale

        # ------------------------------------------
        # ANALYTIC PHASE
        # ------------------------------------------

        ah = hilbert(hn)
        ad = hilbert(dn)

        ph = np.angle(ah)
        pd_ = np.angle(ad)

        delta = np.angle(
            np.mean(np.exp(1j * (pd_ - ph)))
        )

        plv = np.abs(
            np.mean(np.exp(1j * (pd_ - ph)))
        )

        phase_deg = np.degrees(delta)

        # ------------------------------------------
        # PCA GEOMETRY
        # ------------------------------------------

        M = np.column_stack((hn, dn))

        cov = np.cov(M, rowvar=False)

        vals, vecs = np.linalg.eigh(cov)

        order = np.argsort(vals)[::-1]

        vals = vals[order]
        vecs = vecs[:, order]

        major = vals[0]
        minor = vals[1]

        pca_ratio = minor / major

        axis_ratio = np.sqrt(
            minor / major
        )

        v = vecs[:, 0]

        orientation = np.degrees(
            np.arctan2(v[1], v[0])
        )

        # axis has 180-degree ambiguity
        if orientation >= 90:
            orientation -= 180

        if orientation < -90:
            orientation += 180

        # ------------------------------------------
        # ROTATION DIRECTION
        # signed polygon area in H-D plane
        # ------------------------------------------

        area = np.sum(
            hn[:-1] * dn[1:] -
            dn[:-1] * hn[1:]
        )

        rotation = "CCW" if area > 0 else "CW"

        rows.append({
            "UTC_Start": str(start),
            "Samples": int(np.sum(m)),
            "PLV": plv,
            "Phase_D_minus_H_deg": phase_deg,
            "PCA_Minor_Major": pca_ratio,
            "Axis_Ratio": axis_ratio,
            "Orientation_deg": orientation,
            "Signed_Area": area,
            "Rotation": rotation
        })

        # save a few examples spread through day
        hour = pd.Timestamp(str(start)).hour
        minute = pd.Timestamp(str(start)).minute

        if minute == 30 and hour in [0, 4, 8, 12, 16, 20]:
            examples.append(
                (str(start), hn.copy(), dn.copy())
            )


df = pd.DataFrame(rows)

if df.empty:
    raise RuntimeError("No usable windows")

df.to_csv(
    "IST_CARRIER_SHAPE_1MIN.csv",
    index=False
)

# ------------------------------------------------
# SUMMARY
# ------------------------------------------------

cw = np.sum(df["Rotation"] == "CW")
ccw = np.sum(df["Rotation"] == "CCW")

summary = pd.DataFrame([{
    "Usable_Minutes": len(df),

    "Median_PLV":
        df["PLV"].median(),

    "Median_Phase_D_minus_H_deg":
        df["Phase_D_minus_H_deg"].median(),

    "Median_PCA_Minor_Major":
        df["PCA_Minor_Major"].median(),

    "Median_Axis_Ratio":
        df["Axis_Ratio"].median(),

    "Median_Orientation_deg":
        df["Orientation_deg"].median(),

    "Orientation_STD_deg":
        df["Orientation_deg"].std(),

    "CW_Count": cw,
    "CCW_Count": ccw,

    "CW_Percent":
        100 * cw / len(df),

    "CCW_Percent":
        100 * ccw / len(df)
}])

summary.to_csv(
    "IST_CARRIER_SHAPE_SUMMARY.csv",
    index=False
)

print()
print("=" * 70)
print("ISTOK CARRIER SHAPE")
print("=" * 70)

print(summary.to_string(index=False))


# ------------------------------------------------
# REPRESENTATIVE H-D TRAJECTORIES
# ------------------------------------------------

if examples:

    fig, axes = plt.subplots(
        2, 3,
        figsize=(12, 8)
    )

    axes = axes.flatten()

    for ax, (label, h, d) in zip(axes, examples):

        # first 10 seconds only, otherwise plot is too dense
        n = int(FS * 10)

        ax.plot(
            h[:n],
            d[:n],
            linewidth=0.7
        )

        ax.set_title(label)
        ax.set_xlabel("H normalized")
        ax.set_ylabel("D normalized")
        ax.set_aspect(
            "equal",
            adjustable="box"
        )

    plt.tight_layout()

    plt.savefig(
        "IST_CARRIER_SHAPE_EXAMPLES.png",
        dpi=200
    )

    plt.close()


# ------------------------------------------------
# ORIENTATION HISTOGRAM
# ------------------------------------------------

plt.figure(figsize=(9, 5))

plt.hist(
    df["Orientation_deg"],
    bins=72
)

plt.xlabel("Local H-D major-axis orientation (deg)")
plt.ylabel("Count")
plt.title("IST — carrier-band orientation")

plt.tight_layout()

plt.savefig(
    "IST_CARRIER_ORIENTATION.png",
    dpi=200
)

plt.close()


# ------------------------------------------------
# PHASE HISTOGRAM
# ------------------------------------------------

plt.figure(figsize=(9, 5))

plt.hist(
    df["Phase_D_minus_H_deg"],
    bins=72
)

plt.xlabel("D-H phase difference (deg)")
plt.ylabel("Count")
plt.title("IST — H-D phase relationship")

plt.tight_layout()

plt.savefig(
    "IST_CARRIER_PHASE.png",
    dpi=200
)

plt.close()


# ------------------------------------------------
# AXIS-RATIO HISTOGRAM
# ------------------------------------------------

plt.figure(figsize=(9, 5))

plt.hist(
    df["Axis_Ratio"],
    bins=60
)

plt.xlabel("Minor / major axis ratio")
plt.ylabel("Count")
plt.title("IST — local H-D shape")

plt.tight_layout()

plt.savefig(
    "IST_CARRIER_AXIS_RATIO.png",
    dpi=200
)

plt.close()


print()
print("Saved:")
print(" IST_CARRIER_SHAPE_1MIN.csv")
print(" IST_CARRIER_SHAPE_SUMMARY.csv")
print(" IST_CARRIER_SHAPE_EXAMPLES.png")
print(" IST_CARRIER_ORIENTATION.png")
print(" IST_CARRIER_PHASE.png")
print(" IST_CARRIER_AXIS_RATIO.png")