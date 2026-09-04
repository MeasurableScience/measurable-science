import pandas as pd
import numpy as np
import xarray as xr
import math
from datetime import datetime, timezone
from pathlib import Path
from eccodes import *

# ============================================================
# MAUAO
# ============================================================

LAT = -37.63030
LON = 176.17198

GRID_FILE = Path("ICON-DREAM-Global_grid.nc")

MONTHS = ["01", "07"]

OUTPUT = Path("mauao_januar_jul_2010_sa_stepenima.csv")


# ============================================================
# POLOŽAJ SUNCA
# ============================================================

def solar_position_utc(dt, lat, lon):

    year = dt.year
    month = dt.month
    day = dt.day

    hour_decimal = (
        dt.hour
        + dt.minute / 60
        + dt.second / 3600
    )

    if month <= 2:
        year -= 1
        month += 12

    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)

    JD = (
        math.floor(365.25 * (year + 4716))
        + math.floor(30.6001 * (month + 1))
        + day
        + B
        - 1524.5
        + hour_decimal / 24
    )

    T = (JD - 2451545.0) / 36525.0

    L0 = (
        280.46646
        + T * (36000.76983 + T * 0.0003032)
    ) % 360

    M = (
        357.52911
        + T * (35999.05029 - 0.0001537 * T)
    ) % 360

    Mrad = math.radians(M)

    C = (
        math.sin(Mrad)
        * (1.914602 - T * (0.004817 + 0.000014 * T))
        + math.sin(2 * Mrad)
        * (0.019993 - 0.000101 * T)
        + math.sin(3 * Mrad)
        * 0.000289
    )

    true_long = L0 + C

    omega = 125.04 - 1934.136 * T

    apparent_long = (
        true_long
        - 0.00569
        - 0.00478 * math.sin(math.radians(omega))
    )

    mean_obliq = (
        23
        + (
            26
            + (
                21.448
                - T * (
                    46.815
                    + T * (
                        0.00059
                        - T * 0.001813
                    )
                )
            ) / 60
        ) / 60
    )

    obliq = (
        mean_obliq
        + 0.00256
        * math.cos(math.radians(omega))
    )

    decl = math.degrees(
        math.asin(
            math.sin(math.radians(obliq))
            * math.sin(math.radians(apparent_long))
        )
    )

    y = math.tan(
        math.radians(obliq / 2)
    ) ** 2

    eq_time = 4 * math.degrees(
        y * math.sin(2 * math.radians(L0))
        - 2 * 0.016708634 * math.sin(Mrad)
        + 4 * 0.016708634 * y
        * math.sin(Mrad)
        * math.cos(2 * math.radians(L0))
        - 0.5 * y * y
        * math.sin(4 * math.radians(L0))
        - 1.25
        * (0.016708634 ** 2)
        * math.sin(2 * Mrad)
    )

    minutes = (
        dt.hour * 60
        + dt.minute
        + dt.second / 60
    )

    true_solar_time = (
        minutes
        + eq_time
        + 4 * lon
    ) % 1440

    hour_angle = (
        true_solar_time / 4
        - 180
    )

    if hour_angle < -180:
        hour_angle += 360

    ha = math.radians(hour_angle)
    lat_r = math.radians(lat)
    dec_r = math.radians(decl)

    cos_zenith = (
        math.sin(lat_r) * math.sin(dec_r)
        + math.cos(lat_r)
        * math.cos(dec_r)
        * math.cos(ha)
    )

    cos_zenith = max(
        -1,
        min(1, cos_zenith)
    )

    zenith = math.degrees(
        math.acos(cos_zenith)
    )

    elevation = 90 - zenith

    az = math.degrees(
        math.atan2(
            math.sin(ha),
            math.cos(ha) * math.sin(lat_r)
            - math.tan(dec_r) * math.cos(lat_r)
        )
    )

    azimuth = (az + 180) % 360

    return elevation, azimuth, decl


# ============================================================
# GRID
# ============================================================

print("Otvaram ICON-DREAM-Global grid...")

ds = xr.open_dataset(GRID_FILE)

grid_lats = np.degrees(
    ds["clat"].values
)

grid_lons = np.degrees(
    ds["clon"].values
)

grid_lons = (
    (grid_lons + 180) % 360
) - 180

lon_scale = math.cos(
    math.radians(LAT)
)

dist2 = (
    (grid_lats - LAT) ** 2
    + (
        (grid_lons - LON)
        * lon_scale
    ) ** 2
)

nearest_index = int(
    np.argmin(dist2)
)

selected_lat = float(grid_lats[nearest_index])
selected_lon = float(grid_lons[nearest_index])


# ============================================================
# TAČNA UDALJENOST DO IZABRANE ĆELIJE
# ============================================================

def haversine_km(lat1, lon1, lat2, lon2):

    R = 6371.0088

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )

    return (
        2 * R
        * math.asin(math.sqrt(a))
    )


distance_km = haversine_km(
    LAT,
    LON,
    selected_lat,
    selected_lon
)

print()
print("========================================")
print("MAUAO GRID")
print("========================================")
print(f"Target Mauao:       {LAT:.6f}, {LON:.6f}")
print(
    f"Selected grid cell: "
    f"{selected_lat:.6f}, {selected_lon:.6f}"
)
print(f"Distance:           {distance_km:.3f} km")
print(f"Grid index:         {nearest_index}")
print("========================================")
print()

ds.close()


# ============================================================
# ČITANJE GRIB FAJLA
# ============================================================

def read_grib(file_path, column_name):

    rows = []

    print("Čitam:", file_path.name)

    with open(file_path, "rb") as f:

        while True:

            gid = codes_grib_new_from_file(f)

            if gid is None:
                break

            try:

                date = int(
                    codes_get(
                        gid,
                        "validityDate"
                    )
                )

                time = int(
                    codes_get(
                        gid,
                        "validityTime"
                    )
                )

                values = codes_get_values(gid)

                value = float(
                    values[nearest_index]
                )

                rows.append({
                    "date": date,
                    "time": time,
                    column_name: value
                })

            finally:

                codes_release(gid)

    return pd.DataFrame(rows)


# ============================================================
# JANUAR I JUL
# ============================================================

all_months = []

for month in MONTHS:

    direct_file = Path(
        f"ICON-DREAM-Global_2010{month}_ASWDIR_S_hourly.grb"
    )

    diffuse_file = Path(
        f"ICON-DREAM-Global_2010{month}_ASWDIFD_S_hourly.grb"
    )

    if not direct_file.exists():
        print("NEMA:", direct_file)
        continue

    if not diffuse_file.exists():
        print("NEMA:", diffuse_file)
        continue

    direct = read_grib(
        direct_file,
        "direct"
    )

    diffuse = read_grib(
        diffuse_file,
        "diffuse"
    )

    month_df = pd.merge(
        direct,
        diffuse,
        on=["date", "time"]
    )

    all_months.append(month_df)


if not all_months:

    print("Nijedan mesec nije pronađen.")
    raise SystemExit


df = pd.concat(
    all_months,
    ignore_index=True
)

df = df.sort_values(
    ["date", "time"]
).reset_index(drop=True)

df["total"] = (
    df["direct"]
    + df["diffuse"]
)


# ============================================================
# DODAJ POLOŽAJ SUNCA
# ============================================================

elevations = []
azimuths = []
declinations = []
utc_times = []

print()
print("Računam položaj Sunca...")

for _, row in df.iterrows():

    date_str = str(
        int(row["date"])
    )

    t = int(row["time"])

    hour = t // 100
    minute = t % 100

    dt = datetime(
        int(date_str[0:4]),
        int(date_str[4:6]),
        int(date_str[6:8]),
        hour,
        minute,
        tzinfo=timezone.utc
    )

    elev, azim, decl = solar_position_utc(
        dt,
        LAT,
        LON
    )

    utc_times.append(
        f"{hour:02d}:{minute:02d}"
    )

    elevations.append(elev)
    azimuths.append(azim)
    declinations.append(decl)


df["UTC"] = utc_times

df["sun_elevation_deg"] = np.round(
    elevations,
    2
)

df["sun_azimuth_deg"] = np.round(
    azimuths,
    2
)

df["sun_declination_deg"] = np.round(
    declinations,
    2
)

df["direct"] = df["direct"].round(1)
df["diffuse"] = df["diffuse"].round(1)
df["total"] = df["total"].round(1)


df = df[
    [
        "date",
        "UTC",
        "sun_elevation_deg",
        "sun_azimuth_deg",
        "sun_declination_deg",
        "direct",
        "diffuse",
        "total"
    ]
]


# ============================================================
# SNIMI SVE + ODVOJENO JANUAR I JUL
# ============================================================

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

january = df[
    df["date"].astype(str).str[4:6] == "01"
].copy()

july = df[
    df["date"].astype(str).str[4:6] == "07"
].copy()

january.to_csv(
    "mauao_januar_2010.csv",
    index=False,
    encoding="utf-8-sig"
)

july.to_csv(
    "mauao_jul_2010.csv",
    index=False,
    encoding="utf-8-sig"
)


print()
print("========================================")
print("GOTOVO")
print("========================================")
print()
print("Grid index:", nearest_index)
print(
    "Grid tačka:",
    f"{selected_lat:.6f}, {selected_lon:.6f}"
)
print(
    "Udaljenost od Mauao:",
    f"{distance_km:.3f} km"
)
print()
print("Svi podaci:")
print("mauao_januar_jul_2010_sa_stepenima.csv")
print()
print("Januar:")
print("mauao_januar_2010.csv")
print()
print("Jul:")
print("mauao_jul_2010.csv")
print()
print("Broj svih redova:", len(df))
print("Januar:", len(january))
print("Jul:", len(july))