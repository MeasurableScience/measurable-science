from pathlib import Path
import pandas as pd
import numpy as np

# ============================================================
# DIRECT INSTRUMENT -> NIST WAVELENGTH TEST
# No Monte Carlo. No random shifts.
# ============================================================

OLINO_FILE = Path("olino_all_matches.csv")
RITTER_FILE = Path("ritter_nist_all_matches.csv")
NIST_FILE = Path("nist_russell_spiral_test_350_860.csv")

OUT_OLINO_ALL = Path("direct_olino_all_matches.csv")
OUT_OLINO_SUMMARY = Path("direct_olino_summary.csv")

OUT_RITTER_ALL = Path("direct_ritter_all_matches.csv")
OUT_RITTER_SUMMARY = Path("direct_ritter_summary.csv")

# ------------------------------------------------------------
# Instrument limits
# ------------------------------------------------------------

# JETI SpecBos 1211 wavelength accuracy
OLINO_TOLERANCE_NM = 0.500

# Ritter echelle resolving power
RITTER_R = 26000.0

ELEMENTS = [
    "Li", "Be", "B", "C", "Si", "P", "S", "Cl",
    "F", "O", "H", "Ne", "Na", "Mg", "Al"
]


def find_column(df, possibilities):
    for col in possibilities:
        if col in df.columns:
            return col
    return None


def normalize_element(x):
    if pd.isna(x):
        return None

    s = str(x).strip()

    # NIST "element" column in our downloaded CSV contains
    # values such as "H I", "Ne I", "Mg I" OR sometimes
    # atomic symbols directly.
    #
    # Also handle values like "H", "Ne", "Mg".
    s = s.replace('"', '').replace("'", "").strip()

    # Remove ionization-state suffix if present
    parts = s.split()
    if len(parts) >= 1:
        s = parts[0]

    # Remove possible trailing numeric ionization notation
    while len(s) > 1 and s[-1].isdigit():
        s = s[:-1]

    s = s.strip()

    if not s:
        return None

    return s[0].upper() + s[1:].lower()


# ============================================================
# LOAD NIST
# ============================================================

nist = pd.read_csv(NIST_FILE)
print("\nRAW NIST element values:")
print(nist["element"].dropna().astype(str).unique()[:50])

print("\nNIST columns:")
print(list(nist.columns))

element_col = find_column(
    nist,
    ["element", "Element", "spectrum", "Spectrum"]
)

wl_col = find_column(
    nist,
    [
        "obs_wl_air(nm)",
        "ritz_wl_air(nm)",
        "nist_wavelength_nm",
        "Observed Wavelength",
        "Ritz Wavelength"
    ]
)

if element_col is None:
    raise RuntimeError(
        "Ne mogu da pronadjem element/spectrum kolonu u NIST fajlu."
    )

if wl_col is None:
    raise RuntimeError(
        "Ne mogu da pronadjem wavelength kolonu u NIST fajlu."
    )

nist["element_clean"] = nist[element_col].astype(str).str.strip()

def nist_number(series):
    """
    Convert NIST CSV numeric fields such as:
        582.89063
        ="582.89063"
        = "582.89063"
    into real floats.
    """
    s = series.astype(str).str.strip()

    s = (
        s.str.replace('="', '', regex=False)
         .str.replace('"', '', regex=False)
         .str.replace('=', '', regex=False)
         .str.strip()
    )

    return pd.to_numeric(s, errors="coerce")


# Prefer observed wavelength
nist["nist_nm"] = nist_number(nist[wl_col])

# If observed wavelength is missing, use Ritz wavelength
if "ritz_wl_air(nm)" in nist.columns:
    ritz = nist_number(nist["ritz_wl_air(nm)"])
    nist["nist_nm"] = nist["nist_nm"].fillna(ritz)

nist = nist[
    nist["element_clean"].isin(ELEMENTS)
    & nist["nist_nm"].notna()
].copy()

print("\nNIST line counts:")
print(
    nist.groupby("element_clean")
    .size()
    .sort_values(ascending=False)
)


# ============================================================
# OLINO
# ============================================================

olino_raw = pd.read_csv(OLINO_FILE)

required = {"olino_nm", "feature_type"}

missing = required - set(olino_raw.columns)

if missing:
    raise RuntimeError(
        f"Nedostaju OliNo kolone: {', '.join(sorted(missing))}"
    )

# IMPORTANT:
# olino_all_matches contains repeated rows because one measured
# candidate may already have many NIST matches.
# We reconstruct ONLY the original measured candidates here.

olino = (
    olino_raw[
        ["olino_nm", "feature_type", "sigma_score"]
    ]
    .drop_duplicates()
    .copy()
)

olino["olino_nm"] = pd.to_numeric(
    olino["olino_nm"],
    errors="coerce"
)

olino = olino[
    olino["olino_nm"].notna()
].copy()

olino = (
    olino
    .sort_values("olino_nm")
    .reset_index(drop=True)
)

print("\n" + "=" * 80)
print("OLINO DIRECT TEST")
print("=" * 80)
print(f"Candidates           : {len(olino)}")
print(f"Instrument tolerance : +/- {OLINO_TOLERANCE_NM:.3f} nm")

olino_matches = []

for _, cand in olino.iterrows():

    measured = float(cand["olino_nm"])

    for element in ELEMENTS:

        lines = nist[
            nist["element_clean"] == element
        ]

        for _, line in lines.iterrows():

            nist_nm = float(line["nist_nm"])
            delta = measured - nist_nm
            abs_delta = abs(delta)

            if abs_delta <= OLINO_TOLERANCE_NM:

                olino_matches.append({
                    "instrument": "OliNo_SpecBos1211",
                    "element": element,
                    "measured_nm": measured,
                    "nist_nm": nist_nm,
                    "delta_nm": delta,
                    "abs_delta_nm": abs_delta,
                    "allowed_nm": OLINO_TOLERANCE_NM,
                    "fraction_of_limit":
                        abs_delta / OLINO_TOLERANCE_NM,
                    "feature_type": cand["feature_type"],
                    "sigma_score": cand["sigma_score"]
                })


olino_out = pd.DataFrame(olino_matches)

olino_out.to_csv(
    OUT_OLINO_ALL,
    index=False
)

olino_summary_rows = []

for element in ELEMENTS:

    x = olino_out[
        olino_out["element"] == element
    ]

    unique_candidates = (
        x["measured_nm"].nunique()
        if len(x)
        else 0
    )

    emission = (
        x.loc[
            x["feature_type"] == "EMISSION_LIKE",
            "measured_nm"
        ].nunique()
        if len(x)
        else 0
    )

    absorption = (
        x.loc[
            x["feature_type"] == "ABSORPTION_LIKE",
            "measured_nm"
        ].nunique()
        if len(x)
        else 0
    )

    best_delta = (
        x["abs_delta_nm"].min()
        if len(x)
        else np.nan
    )

    olino_summary_rows.append({
        "element": element,
        "matched_candidates": unique_candidates,
        "emission_candidates": emission,
        "absorption_candidates": absorption,
        "best_abs_delta_nm": best_delta
    })


olino_summary = pd.DataFrame(
    olino_summary_rows
).sort_values(
    ["matched_candidates", "best_abs_delta_nm"],
    ascending=[False, True]
)

olino_summary.to_csv(
    OUT_OLINO_SUMMARY,
    index=False
)

print("\nOLINO RESULT")
print(olino_summary.to_string(index=False))


# ============================================================
# RITTER
# ============================================================

ritter_raw = pd.read_csv(RITTER_FILE)

print("\nRitter columns:")
print(list(ritter_raw.columns))

ritter_nm_col = find_column(
    ritter_raw,
    ["ritter_nm", "candidate_nm", "measured_nm"]
)

feature_col = find_column(
    ritter_raw,
    ["feature_type", "type"]
)

sigma_col = find_column(
    ritter_raw,
    ["sigma_score", "score"]
)

if ritter_nm_col is None:
    raise RuntimeError(
        "Ne mogu da pronadjem Ritter wavelength kolonu."
    )

cols = [ritter_nm_col]

if feature_col:
    cols.append(feature_col)

if sigma_col:
    cols.append(sigma_col)

ritter = (
    ritter_raw[cols]
    .drop_duplicates()
    .copy()
)

ritter[ritter_nm_col] = pd.to_numeric(
    ritter[ritter_nm_col],
    errors="coerce"
)

ritter = (
    ritter[
        ritter[ritter_nm_col].notna()
    ]
    .sort_values(ritter_nm_col)
    .reset_index(drop=True)
)

print("\n" + "=" * 80)
print("RITTER DIRECT TEST")
print("=" * 80)
print(f"Candidates        : {len(ritter)}")
print(f"Resolving power R : {RITTER_R:,.0f}")
print("Tolerance         : measured wavelength / R")

ritter_matches = []

for _, cand in ritter.iterrows():

    measured = float(
        cand[ritter_nm_col]
    )

    # Local resolution element
    allowed = measured / RITTER_R

    feature = (
        cand[feature_col]
        if feature_col
        else ""
    )

    sigma = (
        cand[sigma_col]
        if sigma_col
        else np.nan
    )

    for element in ELEMENTS:

        lines = nist[
            nist["element_clean"] == element
        ]

        for _, line in lines.iterrows():

            nist_nm = float(line["nist_nm"])
            delta = measured - nist_nm
            abs_delta = abs(delta)

            if abs_delta <= allowed:

                ritter_matches.append({
                    "instrument": "Ritter_echelle",
                    "element": element,
                    "measured_nm": measured,
                    "nist_nm": nist_nm,
                    "delta_nm": delta,
                    "abs_delta_nm": abs_delta,
                    "allowed_nm": allowed,
                    "fraction_of_limit":
                        abs_delta / allowed,
                    "feature_type": feature,
                    "sigma_score": sigma
                })


ritter_out = pd.DataFrame(
    ritter_matches
)

ritter_out.to_csv(
    OUT_RITTER_ALL,
    index=False
)

ritter_summary_rows = []

for element in ELEMENTS:

    x = ritter_out[
        ritter_out["element"] == element
    ]

    unique_candidates = (
        x["measured_nm"].nunique()
        if len(x)
        else 0
    )

    emission = (
        x.loc[
            x["feature_type"] == "EMISSION_LIKE",
            "measured_nm"
        ].nunique()
        if len(x)
        else 0
    )

    absorption = (
        x.loc[
            x["feature_type"] == "ABSORPTION_LIKE",
            "measured_nm"
        ].nunique()
        if len(x)
        else 0
    )

    best_delta = (
        x["abs_delta_nm"].min()
        if len(x)
        else np.nan
    )

    ritter_summary_rows.append({
        "element": element,
        "matched_candidates": unique_candidates,
        "emission_candidates": emission,
        "absorption_candidates": absorption,
        "best_abs_delta_nm": best_delta
    })


ritter_summary = pd.DataFrame(
    ritter_summary_rows
).sort_values(
    ["matched_candidates", "best_abs_delta_nm"],
    ascending=[False, True]
)

ritter_summary.to_csv(
    OUT_RITTER_SUMMARY,
    index=False
)

print("\nRITTER RESULT")
print(
    ritter_summary.to_string(index=False)
)


# ============================================================
# PARTICULARLY CLOSE MATCHES
# ============================================================

print("\n" + "=" * 80)
print("CLOSEST OLINO MATCHES")
print("=" * 80)

if len(olino_out):
    print(
        olino_out.sort_values(
            "fraction_of_limit"
        )[
            [
                "element",
                "measured_nm",
                "nist_nm",
                "abs_delta_nm",
                "allowed_nm",
                "fraction_of_limit",
                "feature_type"
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


print("\n" + "=" * 80)
print("CLOSEST RITTER MATCHES")
print("=" * 80)

if len(ritter_out):
    print(
        ritter_out.sort_values(
            "fraction_of_limit"
        )[
            [
                "element",
                "measured_nm",
                "nist_nm",
                "abs_delta_nm",
                "allowed_nm",
                "fraction_of_limit",
                "feature_type"
            ]
        ]
        .head(30)
        .to_string(index=False)
    )


print("\nFiles written:")
print(f"  {OUT_OLINO_ALL}")
print(f"  {OUT_OLINO_SUMMARY}")
print(f"  {OUT_RITTER_ALL}")
print(f"  {OUT_RITTER_SUMMARY}")

print("\nDONE.")