import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# SETTINGS
# ============================================================

CSV_FILE = "ESK_CLEAN_CARRIER_GEOMETRY.csv"
OUT_DIR = Path("ESK_TEMPORAL_FINGERPRINT_RESULTS")

PLV_THRESHOLDS = [
    0.00,
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
]

OUT_DIR.mkdir(exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def circular_mean_deg(values):
    """
    Circular mean for ordinary directed angles (-180..180).
    Used for phase difference.
    """
    x = pd.to_numeric(values, errors="coerce").dropna().to_numpy()

    if len(x) == 0:
        return np.nan

    r = np.deg2rad(x)
    s = np.mean(np.sin(r))
    c = np.mean(np.cos(r))

    return np.rad2deg(np.arctan2(s, c))


def axial_mean_deg(values):
    """
    Mean orientation for an undirected axis.
    0 deg and 180 deg represent the same axis.
    """
    x = pd.to_numeric(values, errors="coerce").dropna().to_numpy()

    if len(x) == 0:
        return np.nan

    r = np.deg2rad(2.0 * x)
    s = np.mean(np.sin(r))
    c = np.mean(np.cos(r))

    angle = 0.5 * np.rad2deg(np.arctan2(s, c))

    # Normalize to [-90, 90)
    if angle >= 90:
        angle -= 180
    if angle < -90:
        angle += 180

    return angle


def summarize(group):
    """
    Produce the same fingerprint summary for any subset
    of clean windows.
    """
    n = len(group)

    cw = int((group["rotation"] == "CW").sum())
    ccw = int((group["rotation"] == "CCW").sum())

    valid_rotation = cw + ccw

    cw_pct = (
        100.0 * cw / valid_rotation
        if valid_rotation > 0
        else np.nan
    )

    ccw_pct = (
        100.0 * ccw / valid_rotation
        if valid_rotation > 0
        else np.nan
    )

    return pd.Series({
        "N_windows": n,

        "CW": cw,
        "CCW": ccw,
        "CW_percent": cw_pct,
        "CCW_percent": ccw_pct,

        "PLV_median":
            group["phase_plv"].median(),

        "PLV_mean":
            group["phase_plv"].mean(),

        "phase_circular_mean_deg":
            circular_mean_deg(
                group["mean_phase_difference_deg"]
            ),

        "phase_median_deg":
            group["mean_phase_difference_deg"].median(),

        "minor_major_median":
            group["pca_minor_major_ratio"].median(),

        "ellipticity_median":
            group["ellipticity_ratio"].median(),

        "orientation_axial_mean_deg":
            axial_mean_deg(
                group["polarization_orientation_deg"]
            ),

        "orientation_median_deg":
            group["polarization_orientation_deg"].median(),

        "vector_rms_median_nT":
            group["vector_rms_nT"].median(),
    })


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(CSV_FILE)

df["window_time_utc"] = pd.to_datetime(
    df["window_time_utc"],
    errors="coerce"
)

df = df.dropna(subset=["window_time_utc"]).copy()

df["rotation"] = (
    df["rotation"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df["month"] = df["window_time_utc"].dt.month
df["month_name"] = df["window_time_utc"].dt.month_name()
df["utc_hour"] = df["window_time_utc"].dt.hour
df["date"] = df["window_time_utc"].dt.date


print()
print("=" * 70)
print("ESKDALMUIR TEMPORAL / POLARIZATION FINGERPRINT")
print("=" * 70)

print(f"Input file: {CSV_FILE}")
print(f"Total clean windows: {len(df):,}")
print(
    "Time range:",
    df["window_time_utc"].min(),
    "to",
    df["window_time_utc"].max()
)


# ============================================================
# 1. OVERALL RESULT
# ============================================================

overall = summarize(df).to_frame().T

overall.to_csv(
    OUT_DIR / "ESK_OVERALL_FINGERPRINT.csv",
    index=False
)

print()
print("OVERALL")
print(overall.to_string(index=False))


# ============================================================
# 2. PLV THRESHOLD TEST
# ============================================================

threshold_rows = []

for threshold in PLV_THRESHOLDS:

    sub = df[df["phase_plv"] >= threshold].copy()

    if len(sub) == 0:
        continue

    s = summarize(sub)

    row = {
        "PLV_threshold": threshold,
        **s.to_dict()
    }

    threshold_rows.append(row)


plv_test = pd.DataFrame(threshold_rows)

plv_test.to_csv(
    OUT_DIR / "ESK_PLV_THRESHOLD_HANDEDNESS.csv",
    index=False
)

print()
print("=" * 70)
print("PLV THRESHOLD TEST")
print("=" * 70)

print(
    plv_test[
        [
            "PLV_threshold",
            "N_windows",
            "CW",
            "CCW",
            "CW_percent",
            "PLV_median",
            "phase_circular_mean_deg",
            "ellipticity_median",
        ]
    ].to_string(index=False)
)


# ============================================================
# 3. CW VS CCW FINGERPRINT
# ============================================================

rotation_rows = []

for rotation, group in df.groupby("rotation"):

    if rotation not in ["CW", "CCW"]:
        continue

    s = summarize(group)

    row = {
        "rotation_group": rotation,
        **s.to_dict()
    }

    rotation_rows.append(row)


rotation_comparison = pd.DataFrame(rotation_rows)

rotation_comparison.to_csv(
    OUT_DIR / "ESK_CW_VS_CCW_FINGERPRINT.csv",
    index=False
)

print()
print("=" * 70)
print("CW VS CCW")
print("=" * 70)

print(rotation_comparison.to_string(index=False))


# ============================================================
# 4. MONTHLY FINGERPRINT
# ============================================================

monthly_rows = []

for month, group in df.groupby("month"):

    s = summarize(group)

    row = {
        "month": int(month),
        "month_name": group["month_name"].iloc[0],
        **s.to_dict()
    }

    monthly_rows.append(row)


monthly = pd.DataFrame(monthly_rows)
monthly = monthly.sort_values("month")

monthly.to_csv(
    OUT_DIR / "ESK_MONTHLY_FINGERPRINT.csv",
    index=False
)

print()
print("=" * 70)
print("MONTHLY FINGERPRINT")
print("=" * 70)

print(
    monthly[
        [
            "month",
            "month_name",
            "N_windows",
            "CW",
            "CCW",
            "CW_percent",
            "PLV_median",
            "phase_circular_mean_deg",
            "minor_major_median",
            "ellipticity_median",
            "orientation_axial_mean_deg",
        ]
    ].to_string(index=False)
)


# ============================================================
# 5. UTC HOUR FINGERPRINT
# ============================================================

hour_rows = []

for hour, group in df.groupby("utc_hour"):

    s = summarize(group)

    row = {
        "utc_hour": int(hour),
        **s.to_dict()
    }

    hour_rows.append(row)


hourly = pd.DataFrame(hour_rows)
hourly = hourly.sort_values("utc_hour")

hourly.to_csv(
    OUT_DIR / "ESK_UTC_HOUR_FINGERPRINT.csv",
    index=False
)

print()
print("=" * 70)
print("UTC-HOUR FINGERPRINT")
print("=" * 70)

print(
    hourly[
        [
            "utc_hour",
            "N_windows",
            "CW",
            "CCW",
            "CW_percent",
            "PLV_median",
            "phase_circular_mean_deg",
            "minor_major_median",
            "ellipticity_median",
            "orientation_axial_mean_deg",
        ]
    ].to_string(index=False)
)


# ============================================================
# 6. MONTH x UTC HOUR MATRIX
# ============================================================

matrix = pd.crosstab(
    df["month"],
    df["utc_hour"]
)

matrix.to_csv(
    OUT_DIR / "ESK_MONTH_X_UTC_HOUR_COUNTS.csv"
)


cw_matrix = (
    df.assign(
        is_cw=(df["rotation"] == "CW").astype(float)
    )
    .pivot_table(
        index="month",
        columns="utc_hour",
        values="is_cw",
        aggfunc="mean"
    )
    * 100.0
)

cw_matrix.to_csv(
    OUT_DIR / "ESK_MONTH_X_UTC_HOUR_CW_PERCENT.csv"
)


# ============================================================
# 7. DAILY FINGERPRINT
# ============================================================

daily_rows = []

for date, group in df.groupby("date"):

    s = summarize(group)

    row = {
        "date": date,
        **s.to_dict()
    }

    daily_rows.append(row)


daily = pd.DataFrame(daily_rows)

daily.to_csv(
    OUT_DIR / "ESK_DAILY_FINGERPRINT.csv",
    index=False
)


# ============================================================
# FINISH
# ============================================================

print()
print("=" * 70)
print("DONE")
print("=" * 70)

print(f"Results written to: {OUT_DIR.resolve()}")

print()
print("Main files:")
print("  ESK_OVERALL_FINGERPRINT.csv")
print("  ESK_PLV_THRESHOLD_HANDEDNESS.csv")
print("  ESK_CW_VS_CCW_FINGERPRINT.csv")
print("  ESK_MONTHLY_FINGERPRINT.csv")
print("  ESK_UTC_HOUR_FINGERPRINT.csv")
print("  ESK_MONTH_X_UTC_HOUR_COUNTS.csv")
print("  ESK_MONTH_X_UTC_HOUR_CW_PERCENT.csv")
print("  ESK_DAILY_FINGERPRINT.csv")