import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# FIRMAMENT LONG-TERM TEST v0.1
#
# Cilj:
#   gledamo koliko se ZVEZDE pomeraju prema danas
#   izmerenim proper-motion vrednostima.
#
# Ovo NE ukljucuje precesiju koordinatne mreze.
# ==========================================================

stars = {
    "Polaris": {
        "ra": 37.954542,
        "dec": 89.264111,
        "pmra": 44.48,      # mas/yr, RA*cos(dec)
        "pmdec": -11.85
    },

    "Sigma Octantis": {
        "ra": 317.195250,
        "dec": -88.956500,
        "pmra": 26.323,
        "pmdec": 4.721
    },

    "Spica": {
        "ra": 201.298247,
        "dec": -11.161319,
        "pmra": -42.35,
        "pmdec": -30.67
    }
}


# epohe u odnosu na J2000
years = np.array([
    -13000,
    -12000,
    -6000,
    0,
    6000,
    12000,
    13000
])


def propagate(ra, dec, pmra, pmdec, years):

    dec_rad = np.radians(dec)

    # pmRA je katalogizovan kao dRA*cos(dec)
    dra_deg_year = (
        pmra / 3_600_000.0
    ) / np.cos(dec_rad)

    ddec_deg_year = (
        pmdec / 3_600_000.0
    )

    new_ra = ra + dra_deg_year * years
    new_dec = dec + ddec_deg_year * years

    new_ra %= 360.0

    return new_ra, new_dec


print()
print("FIRMAMENT LONG-TERM TEST")
print("========================")

results = {}

for name, s in stars.items():

    ra, dec = propagate(
        s["ra"],
        s["dec"],
        s["pmra"],
        s["pmdec"],
        years
    )

    results[name] = (ra, dec)

    print()
    print(name)
    print("-" * len(name))

    for y, r, d in zip(years, ra, dec):

        # udaljenost od naseg trenutnog referentnog centra
        radius = 90.0 - d

        print(
            f"{2000+y:7.0f}  "
            f"RA={r:10.5f}  "
            f"Dec={d:10.5f}  "
            f"R_from_center={radius:10.5f}"
        )


# ==========================================================
# CRTANJE
# ==========================================================

fig, ax = plt.subplots(figsize=(10,10))

ax.scatter(0, 0, s=120)
ax.text(
    0, 3,
    "CENTER / CPU reference",
    ha="center"
)


for name, (ra, dec) in results.items():

    theta = np.radians(ra)

    radius = 90.0 - dec

    x = radius * np.sin(theta)
    y = radius * np.cos(theta)

    ax.plot(x, y, marker="o", label=name)

    # danasnja tacka
    index_now = list(years).index(0)

    ax.text(
        x[index_now] + 2,
        y[index_now] + 2,
        name
    )


for r in [30,60,90,120,150,180]:

    circle = plt.Circle(
        (0,0),
        r,
        fill=False,
        alpha=0.2
    )

    ax.add_patch(circle)


ax.set_aspect("equal")

ax.set_xlim(-190,190)
ax.set_ylim(-190,190)

ax.set_title(
    "Measured proper-motion extrapolation\n"
    "-13,000 to +13,000 years from J2000"
)

ax.legend()
ax.grid(alpha=0.2)

plt.show()