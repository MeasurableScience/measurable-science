import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import pymagglobal


# ============================================================
# SETTINGS
# ============================================================

LAT = 17.0
RADIUS = 6371.2

YEAR_START = 1590
YEAR_END = 1990
YEAR_STEP = 1.0

# Dense longitude grid used only to bracket roots.
# Final roots are refined with Brent's method.
LON_STEP = 0.5


# ============================================================
# LOAD GUFM1
# ============================================================

model = pymagglobal.Model("gufm1")

print("GUFM1 loaded")
print("Time range:", model.t_min, "-", model.t_max)
print("Maximum spherical harmonic degree:", model.l_max)
print()


# ============================================================
# FIELD CALCULATION
# ============================================================

def field_at(year, lat, lon):
    """
    Returns North, East, Down in nT.
    """

    grid = np.array([
        [90.0 - lat],   # colatitude
        [lon],
        [RADIUS],
        [year]
    ])

    north, east, down = pymagglobal.field(
        grid,
        model,
        field_type="nez",
        inp_gd=False,
        out_gd=False
    )

    return float(north[0]), float(east[0]), float(down[0])


def east_component(lon, year):
    """
    East component at fixed latitude.
    D = 0 or +/-180 when East = 0.
    We later retain only roots with North > 0.
    """
    north, east, down = field_at(year, LAT, lon)
    return east


# ============================================================
# FIND ALL TRUE-NORTH D=0 ROOTS
# ============================================================

def find_roots_for_year(year):

    longitudes = np.arange(-180.0, 180.0 + LON_STEP, LON_STEP)

    east_values = np.empty(len(longitudes))

    for i, lon in enumerate(longitudes):
        east_values[i] = east_component(lon, year)

    roots = []

    for i in range(len(longitudes) - 1):

        lon1 = longitudes[i]
        lon2 = longitudes[i + 1]

        e1 = east_values[i]
        e2 = east_values[i + 1]

        # Exact grid-point zero
        if e1 == 0.0:
            root = lon1

        # Sign change -> root between the two points
        elif e1 * e2 < 0.0:

            try:
                root = brentq(
                    lambda lon: east_component(lon, year),
                    lon1,
                    lon2,
                    xtol=1e-10
                )
            except ValueError:
                continue

        else:
            continue

        north, east, down = field_at(year, LAT, root)

        # CRITICAL:
        # East = 0 and North > 0 -> D = 0 degrees
        # East = 0 and North < 0 -> D = +/-180 degrees
        if north > 0:

            D = np.degrees(np.arctan2(east, north))

            roots.append({
                "year": year,
                "latitude_deg": LAT,
                "longitude_deg": root,
                "north_nT": north,
                "east_nT": east,
                "down_nT": down,
                "declination_deg": D
            })

    # Remove accidental duplicates
    unique = []

    for r in roots:

        duplicate = False

        for u in unique:
            if abs(r["longitude_deg"] - u["longitude_deg"]) < 1e-5:
                duplicate = True
                break

        if not duplicate:
            unique.append(r)

    unique.sort(key=lambda x: x["longitude_deg"])

    return unique


# ============================================================
# RUN 1590-1990
# ============================================================

all_rows = []

years = np.arange(
    YEAR_START,
    YEAR_END + YEAR_STEP / 2,
    YEAR_STEP
)

for year in years:

    roots = find_roots_for_year(year)

    print(
        f"{year:.0f}: "
        + ", ".join(
            f"{r['longitude_deg']:.3f}°"
            for r in roots
        )
        + f"   [{len(roots)} roots]"
    )

    for r in roots:
        all_rows.append(r)


# ============================================================
# SAVE RAW RESULTS
# ============================================================

df = pd.DataFrame(all_rows)

csv_name = "GUFM1_D0_17N_ALL_ROOTS.csv"

df.to_csv(csv_name, index=False)

print()
print("Saved:", csv_name)
print("Total D=0 crossings:", len(df))


# ============================================================
# ROOT COUNT THROUGH TIME
# ============================================================

counts = (
    df.groupby("year")
      .size()
      .reset_index(name="number_of_D0_crossings")
)

counts.to_csv(
    "GUFM1_D0_17N_ROOT_COUNT.csv",
    index=False
)

print("Saved: GUFM1_D0_17N_ROOT_COUNT.csv")


# ============================================================
# PLOT — RAW ROOTS
# ============================================================

plt.figure(figsize=(12, 7))

plt.scatter(
    df["year"],
    df["longitude_deg"],
    s=7
)

plt.axhline(
    -30,
    linestyle="--",
    linewidth=1,
    label="30°W reference"
)

plt.xlabel("Year")
plt.ylabel("Longitude of D=0 crossing (degrees)")
plt.title(
    "GUFM1 — all true-north D=0 crossings at latitude 17°N"
)

plt.xlim(YEAR_START, YEAR_END)
plt.ylim(-180, 180)

plt.grid(alpha=0.25)
plt.legend()

plt.tight_layout()

plot_name = "GUFM1_D0_17N_MOVEMENT.png"

plt.savefig(
    plot_name,
    dpi=200
)

print("Saved:", plot_name)

plt.show()


# ============================================================
# SIMPLE CHECK AROUND YEAR 1700
# ============================================================

print()
print("----- 1700 CHECK -----")

check = df[np.isclose(df["year"], 1700.0)]

if len(check):

    for _, row in check.iterrows():

        print(
            f"D=0 root: "
            f"{row['longitude_deg']:.6f}°, "
            f"N={row['north_nT']:.1f} nT, "
            f"E={row['east_nT']:.6f} nT"
        )

else:
    print("No D=0 root found at 17°N in 1700.")