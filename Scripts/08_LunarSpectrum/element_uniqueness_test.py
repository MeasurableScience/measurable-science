from pathlib import Path
import pandas as pd
import numpy as np

# ============================================================
# ELEMENT UNIQUENESS TEST
#
# Uses ONLY results from the already completed direct
# instrument -> NIST wavelength test.
#
# NO Monte Carlo
# NO wavelength shifting
# NO new fitting
# NO changing instrumental windows
# ============================================================

OLINO_FILE = Path("direct_olino_all_matches.csv")
RITTER_FILE = Path("direct_ritter_all_matches.csv")

OUT_ALL = Path("element_uniqueness_all.csv")
OUT_SUMMARY = Path("element_uniqueness_summary.csv")
OUT_NEON = Path("neon_uniqueness_details.csv")


ELEMENTS = [
    "Li", "Be", "B", "C", "Si", "P", "S", "Cl",
    "F", "O", "H", "Ne", "Na", "Mg", "Al"
]


# ============================================================
# LOAD
# ============================================================

olino = pd.read_csv(OLINO_FILE)
ritter = pd.read_csv(RITTER_FILE)

olino["dataset"] = "OLINO"
ritter["dataset"] = "RITTER"

df = pd.concat(
    [olino, ritter],
    ignore_index=True
)


# ============================================================
# BASIC CHECK
# ============================================================

required = {
    "dataset",
    "element",
    "measured_nm",
    "nist_nm",
    "abs_delta_nm",
    "allowed_nm",
    "feature_type"
}

missing = required - set(df.columns)

if missing:
    raise RuntimeError(
        "Missing columns: " + ", ".join(sorted(missing))
    )


# ============================================================
# IMPORTANT:
#
# One measured candidate can match several NIST lines belonging
# to the SAME element.
#
# Example:
# measured candidate 500 nm
#
# Ne line A -> match
# Ne line B -> match
# Ne line C -> match
#
# This is still ONE element (Ne), not three competing elements.
#
# Therefore uniqueness is calculated using DISTINCT ELEMENTS
# matching each measured candidate.
# ============================================================


candidate_rows = []

group_cols = [
    "dataset",
    "measured_nm",
    "feature_type"
]

for keys, group in df.groupby(group_cols, dropna=False):

    dataset, measured_nm, feature_type = keys

    elements = sorted(
        group["element"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    n_elements = len(elements)

    if n_elements == 1:
        status = "UNIQUE_ELEMENT_MATCH"
    elif n_elements > 1:
        status = "AMBIGUOUS"
    else:
        status = "NO_MATCH"

    candidate_rows.append({
        "dataset": dataset,
        "measured_nm": measured_nm,
        "feature_type": feature_type,
        "number_of_matching_elements": n_elements,
        "matching_elements": ",".join(elements),
        "status": status
    })


candidates = pd.DataFrame(candidate_rows)


# ============================================================
# ADD UNIQUENESS INFORMATION BACK TO EVERY MATCH
# ============================================================

df = df.merge(
    candidates,
    on=[
        "dataset",
        "measured_nm",
        "feature_type"
    ],
    how="left"
)


# ============================================================
# For each element count:
#
# TOTAL:
# candidate compatible with that element
#
# UNIQUE:
# that candidate matches ONLY that element
#
# AMBIGUOUS:
# candidate matches this element AND >=1 other element
#
# Also emission / absorption breakdown.
# ============================================================

summary_rows = []

for dataset in ["OLINO", "RITTER"]:

    d = df[df["dataset"] == dataset]

    for element in ELEMENTS:

        e = d[d["element"] == element].copy()

        # Remove duplicate NIST lines for same measured candidate.
        # We care about measured spectral candidates here.
        e_unique_candidates = (
            e.sort_values("abs_delta_nm")
             .drop_duplicates(
                 subset=[
                     "measured_nm",
                     "feature_type"
                 ]
             )
        )

        total = len(e_unique_candidates)

        unique = (
            e_unique_candidates[
                e_unique_candidates["status"]
                == "UNIQUE_ELEMENT_MATCH"
            ]
        )

        ambiguous = (
            e_unique_candidates[
                e_unique_candidates["status"]
                == "AMBIGUOUS"
            ]
        )

        unique_count = len(unique)
        ambiguous_count = len(ambiguous)

        unique_emission = (
            unique[
                unique["feature_type"]
                == "EMISSION_LIKE"
            ]["measured_nm"]
            .nunique()
        )

        unique_absorption = (
            unique[
                unique["feature_type"]
                == "ABSORPTION_LIKE"
            ]["measured_nm"]
            .nunique()
        )

        if total:
            unique_fraction = unique_count / total
        else:
            unique_fraction = np.nan

        if total:
            best_delta = (
                e_unique_candidates[
                    "abs_delta_nm"
                ].min()
            )
        else:
            best_delta = np.nan

        if unique_count:
            best_unique_delta = (
                unique[
                    "abs_delta_nm"
                ].min()
            )
        else:
            best_unique_delta = np.nan

        summary_rows.append({
            "dataset": dataset,
            "element": element,
            "total_matched_candidates": total,
            "unique_element_candidates": unique_count,
            "ambiguous_candidates": ambiguous_count,
            "unique_fraction": unique_fraction,
            "unique_emission": unique_emission,
            "unique_absorption": unique_absorption,
            "best_delta_nm": best_delta,
            "best_unique_delta_nm": best_unique_delta
        })


summary = pd.DataFrame(summary_rows)


# ============================================================
# SORT
# ============================================================

summary = summary.sort_values(
    [
        "dataset",
        "unique_element_candidates",
        "total_matched_candidates"
    ],
    ascending=[
        True,
        False,
        False
    ]
)


# ============================================================
# NEON DETAILS
# ============================================================

neon = df[
    df["element"] == "Ne"
].copy()

# Keep closest Ne NIST line for each measured candidate
neon = (
    neon.sort_values("abs_delta_nm")
        .drop_duplicates(
            subset=[
                "dataset",
                "measured_nm",
                "feature_type"
            ]
        )
        .sort_values(
            [
                "dataset",
                "status",
                "abs_delta_nm"
            ]
        )
)


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    OUT_ALL,
    index=False
)

summary.to_csv(
    OUT_SUMMARY,
    index=False
)

neon.to_csv(
    OUT_NEON,
    index=False
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 90)
print("ELEMENT UNIQUENESS TEST")
print("=" * 90)

for dataset in ["OLINO", "RITTER"]:

    print("\n")
    print("=" * 90)
    print(dataset)
    print("=" * 90)

    x = summary[
        summary["dataset"] == dataset
    ]

    print(
        x[
            [
                "element",
                "total_matched_candidates",
                "unique_element_candidates",
                "ambiguous_candidates",
                "unique_fraction",
                "unique_emission",
                "unique_absorption",
                "best_delta_nm",
                "best_unique_delta_nm"
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}"
        )
    )


# ============================================================
# NEON
# ============================================================

print("\n")
print("=" * 90)
print("NEON ONLY")
print("=" * 90)

for dataset in ["OLINO", "RITTER"]:

    n = neon[
        neon["dataset"] == dataset
    ]

    print(f"\n{dataset}")

    if len(n) == 0:
        print("No Ne matches.")
        continue

    total = len(n)

    unique_n = (
        n["status"]
        == "UNIQUE_ELEMENT_MATCH"
    ).sum()

    ambiguous_n = (
        n["status"]
        == "AMBIGUOUS"
    ).sum()

    print(f"Total Ne-compatible candidates : {total}")
    print(f"Ne-only candidates             : {unique_n}")
    print(f"Ambiguous Ne candidates        : {ambiguous_n}")

    print("\nDETAILS:")

    print(
        n[
            [
                "measured_nm",
                "feature_type",
                "nist_nm",
                "abs_delta_nm",
                "allowed_nm",
                "fraction_of_limit",
                "number_of_matching_elements",
                "matching_elements",
                "status"
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}"
        )
    )


print("\n")
print("=" * 90)
print("FILES WRITTEN")
print("=" * 90)

print(OUT_ALL)
print(OUT_SUMMARY)
print(OUT_NEON)

print("\nDONE.")