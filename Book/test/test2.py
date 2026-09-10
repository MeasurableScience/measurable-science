import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.units as u

# ==========================================
# DEFINICIJA TESTA I PODATAKA
# ==========================================

print(
    "=== SLEPI ASTRONOMSKI TEST: 3D PROPAGACIJA U FIKSNOM ICRS/J2000 PROSTORU ==="
)
print(
    "UPOZORENJE: Vrednosti za ±13.000 godina su linearna ekstrapolacija današnjih"
)
print(
    "astrometrijskih parametara (bez uzimanja u obzir orbitalnih acceleracija ili perturbacija).\n"
)

# Fiksni centar neba (CPU) u ICRS/J2000
CPU = np.array([0.0, 0.0, 1.0])

# Epohе koje se testiraju
epochs = [-11000, -10000, -4000, 2000, 8000, 14000, 15000]

# Katalogizovani astrometrijski podaci za J2000.0
stars_data = {
    "Polaris": SkyCoord(
        ra="02h31m49.09456s",
        dec="+89d15m50.7923s",
        distance=(1000.0 / 7.54) * u.pc,
        pm_ra_cosdec=44.48 * u.mas / u.yr,
        pm_dec=-11.85 * u.mas / u.yr,
        radial_velocity=-16.42 * u.km / u.s,
        frame="icrs",
    ),

    "Sigma Octantis": SkyCoord(
        ra="21h08m46.86357s",
        dec="-88d57m23.3983s",
        distance=(1000.0 / 11.1005) * u.pc,
        pm_ra_cosdec=26.323 * u.mas / u.yr,
        pm_dec=4.721 * u.mas / u.yr,
        radial_velocity=11.9 * u.km / u.s,
        frame="icrs",
    ),

    "Spica": SkyCoord(
        ra="13h25m11.57937s",
        dec="-11d09m40.7501s",
        distance=(1000.0 / 13.06) * u.pc,
        pm_ra_cosdec=-42.35 * u.mas / u.yr,
        pm_dec=-30.67 * u.mas / u.yr,
        radial_velocity=-3.310 * u.km / u.s,
        frame="icrs",
    ),
}
# Priprema početnih Dekartovih vektora i brzina (izbegava vremenske skale u Astropy-ju)
star_vectors = {}
for name, coord in stars_data.items():
    cart = coord.cartesian
    r0 = cart.xyz.to(u.pc).value  # Početni položaj [x, y, z] u parsecima
    v_xyz = cart.differentials["s"].d_xyz.to(u.pc / u.yr).value  # Brzina [vx, vy, vz] u pc/yr
    unit_j2000 = r0 / np.linalg.norm(r0)
    star_vectors[name] = {"r0": r0, "v_xyz": v_xyz, "j2000_unit": unit_j2000}

results_table = []
trajectory_data = {
    name: {"r": [], "theta": [], "years": []} for name in stars_data
}

# ==========================================
# PROPAGACIJA I PRORAČUN
# ==========================================

for year in epochs:
    dt_years = year - 2000.0

    for name, data in star_vectors.items():
        # Direktan 3D pomak u Dekartovom prostoru: r(t) = r0 + v * dt
        r_t = data["r0"] + data["v_xyz"] * dt_years
        v_star = r_t / np.linalg.norm(r_t)

        # 1. Pravi 3D ugao od CPU ([0,0,1])
        dot_product = np.clip(np.dot(CPU, v_star), -1.0, 1.0)
        distance_from_cpu = np.degrees(np.arccos(dot_product))

        # 2. Azimut / položajni ugao oko CPU u fiksnoj ravni
        position_angle = np.degrees(np.arctan2(v_star[1], v_star[0]))
        if position_angle < 0:
            position_angle += 360.0

        # 3. Ukupni stvarni ugaoni pomak od J2000 položaja
        v_j2000 = data["j2000_unit"]
        disp_dot = np.clip(np.dot(v_j2000, v_star), -1.0, 1.0)
        total_displacement = np.degrees(np.arccos(disp_dot))

        results_table.append(
            {
                "YEAR": year,
                "STAR": name,
                "ANGLE_FROM_CPU": distance_from_cpu,
                "POS_ANGLE": position_angle,
                "TOTAL_DISP": total_displacement,
            }
        )

        trajectory_data[name]["r"].append(distance_from_cpu)
        trajectory_data[name]["theta"].append(np.radians(position_angle))
        trajectory_data[name]["years"].append(year)

# ==========================================
# ISPIS TABELE
# ==========================================

print(
    f"{'YEAR':<8} | {'STAR':<16} | {'ANGLE_FROM_FIXED_CPU':<22} | {'POS_ANGLE_AROUND_CPU':<22} | {'DISP_FROM_J2000':<18}"
)
print("-" * 96)

for row in results_table:
    print(
        f"{row['YEAR']:<8} | {row['STAR']:<16} | {row['ANGLE_FROM_CPU']:<22.4f} | {row['POS_ANGLE']:<22.4f} | {row['TOTAL_DISP']:<18.4f}"
    )

print("\n" + "=" * 96)
print("SUMARNI REZULTATI ZA PERIOD OD -11000 DO +15000 GODINA:")
print("=" * 96)

for name in stars_data:
    star_rows = [r for r in results_table if r["STAR"] == name]
    r_min_epoch = [r for r in star_rows if r["YEAR"] == -11000][0]
    r_max_epoch = [r for r in star_rows if r["YEAR"] == 15000][0]

    dist_change = r_max_epoch["ANGLE_FROM_CPU"] - r_min_epoch["ANGLE_FROM_CPU"]
    max_displacement = max([r["TOTAL_DISP"] for r in star_rows])
    pa_change = r_max_epoch["POS_ANGLE"] - r_min_epoch["POS_ANGLE"]

    print(f"\nZvezda: {name}")
    print(
        f"  - Ukupna promena udaljenosti od CPU (-11k do +15k god): {dist_change:+.4f}°"
    )
    print(
        f"  - Maksimalni stvarni ugaoni pomak u fiksnom prostoru: {max_displacement:.4f}°"
    )
    print(
        f"  - Ukupna promena položajnog ugla oko CPU: {pa_change:+.4f} stepeni"
    )

print("\n" + "=" * 96)

# ==========================================
# POLARNI GRAFIKON
# ==========================================

fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(8, 8))
colors = {"Polaris": "blue", "Sigma Octantis": "green", "Spica": "red"}

for name, data in trajectory_data.items():
    r = data["r"]
    theta = data["theta"]

    ax.plot(
        theta,
        r,
        marker="o",
        linestyle="-",
        label=name,
        color=colors.get(name, "black"),
    )
    ax.text(
        theta[0],
        r[0],
        f" {name} (-11k)",
        fontsize=9,
        color=colors.get(name, "black"),
    )
    ax.text(
        theta[-1],
        r[-1],
        f" {name} (+15k)",
        fontsize=9,
        color=colors.get(name, "black"),
    )

ax.set_title(
    "Putanje zvezda u fiksnom ICRS/J2000 prostoru\n(CPU = [0, 0, 1] u centru, radijus = ugaoni razmak u stepenima)",
    va="bottom",
    pad=20,
)
ax.set_rmax(max([max(d["r"]) for d in trajectory_data.values()]) * 1.1)
ax.grid(True)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

print("Generisanje polarnog grafikona...")
plt.show()