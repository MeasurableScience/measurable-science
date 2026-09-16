import pandas as pd
import numpy as np

CSV_FILE = "ESK_CLEAN_CARRIER_GEOMETRY.csv"

THRESHOLD = 0.30
N_SHUFFLES = 10000
SEED = 12345

df = pd.read_csv(CSV_FILE)

df["rotation"] = (
    df["rotation"]
    .astype(str)
    .str.strip()
    .str.upper()
)

df = df[
    df["rotation"].isin(["CW", "CCW"])
    & df["phase_plv"].notna()
].copy()

high = df["phase_plv"] >= THRESHOLD

n_high = int(high.sum())
real_cw = int(
    ((df["rotation"] == "CW") & high).sum()
)

real_pct = 100 * real_cw / n_high

print("=" * 65)
print("ESKDALMUIR PLV-HANDEDNESS SHUFFLE NULL")
print("=" * 65)

print(f"Total windows       : {len(df)}")
print(f"PLV threshold       : {THRESHOLD}")
print(f"Windows >= threshold: {n_high}")
print(f"Observed CW          : {real_cw}/{n_high}")
print(f"Observed CW percent  : {real_pct:.6f}%")

rng = np.random.default_rng(SEED)

rotation = df["rotation"].to_numpy()

null_cw = np.empty(N_SHUFFLES, dtype=int)

for i in range(N_SHUFFLES):

    shuffled = rng.permutation(rotation)

    null_cw[i] = np.sum(
        shuffled[high.to_numpy()] == "CW"
    )

p_value = (
    np.sum(null_cw >= real_cw) + 1
) / (
    N_SHUFFLES + 1
)

print()
print(f"Shuffles             : {N_SHUFFLES}")
print(
    f"Null mean CW         : "
    f"{null_cw.mean():.2f}/{n_high}"
)
print(
    f"Null mean percent    : "
    f"{100 * null_cw.mean()/n_high:.4f}%"
)
print(
    f"Best null result     : "
    f"{null_cw.max()}/{n_high}"
)
print(
    f"Shuffles >= observed : "
    f"{np.sum(null_cw >= real_cw)}"
)

print(f"Monte Carlo p-value  : {p_value:.8f}")

print()
print("DONE")