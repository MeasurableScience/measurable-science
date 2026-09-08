from pathlib import Path
import re

import numpy as np
import pandas as pd

from astropy.io import fits
from scipy.signal import savgol_filter, find_peaks


# ============================================================
# RITTER MOON — TWO FILE BLIND TEST v2
#
# IMPORTANT:
#   NO atomic line wavelengths.
#   NO element identification.
#
# Frozen analysis parameters from v1 are preserved.
# Only the IRAF MULTISPEC parsing is being repaired.
# ============================================================


FILES = [
    "960327.012.fits",
    "961116.012.fits",
]

OUT = Path("ritter_two_blind_v2_output")
OUT.mkdir(exist_ok=True)


# ============================================================
# FROZEN BLIND PARAMETERS — DO NOT CHANGE
# ============================================================

SIGMA_LIMIT = 4.0
CONTINUUM_NM = 1.5
EDGE_FRACTION = 0.03
MIN_DISTANCE_NM = 0.05
MATCH_TOLERANCE_NM = 0.03


# ============================================================
# HELPERS
# ============================================================

def robust_sigma(x):

    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]

    if len(x) == 0:
        return np.nan

    med = np.median(x)
    mad = np.median(np.abs(x - med))

    return 1.4826 * mad


# ============================================================
# IRAF MULTISPEC
# ============================================================

def get_multispec(header):
    """
    Ritter stores one long IRAF MULTISPEC string across
    WAT2_001, WAT2_002, WAT2_003 ...

    CRITICAL:
    These cards are pieces of ONE continuous string.
    Do NOT insert extra spaces between cards.
    """

    pairs = []

    for key in header.keys():

        key_string = str(key)

        if key_string.startswith("WAT2_"):

            try:
                number = int(
                    key_string.split("_")[1]
                )
            except Exception:
                continue

            pairs.append(
                (
                    number,
                    str(header[key])
                )
            )

    pairs.sort(
        key=lambda x: x[0]
    )

    return "".join(
        value
        for number, value in pairs
    )


def extract_spec_records(header):
    """
    Parse IRAF MULTISPEC records such as:

    spec1 = "1 48 0 4649.1683 0.0415799 1149 ..."

    For the Ritter files used here the first six values are:

      aperture
      beam
      dispersion type
      starting wavelength
      wavelength increment
      number of pixels
    """

    wat = get_multispec(header)
        # ========================================================
    # REPAIR THREE KNOWN RITTER WAT2 CARD-BOUNDARY JOIN ERRORS
    #
    # These are NOT scientific corrections and do not alter
    # wavelengths to fit any target.
    # They only restore missing separators between FITS cards.
    # ========================================================

    wat = wat.replace(
        "0.0424645582175631149",
        "0.042464558217563 1149"
    )

    wat = wat.replace(
        'spec10 = "1039 0 5721.452263136',
        'spec10 = "10 39 0 5721.452263136'
    )

    wat = wat.replace(
        "5999.62323706670.054778135435754",
        "5999.6232370667 0.054778135435754"
    )

    # Capture complete quoted spec strings.
    pattern = re.compile(
        r'spec\s*(\d+)\s*=\s*"([^"]*)"',
        flags=re.IGNORECASE
    )

    matches = list(
        pattern.finditer(wat)
    )

    records = {}

    for match in matches:

        spec_number = int(
            match.group(1)
        )

        text = match.group(2)

        fields = text.split()

        if len(fields) < 6:

            print(
                "BAD SPEC {}: only {} fields"
                .format(
                    spec_number,
                    len(fields)
                )
            )

            continue

        try:

            aperture = int(
                float(fields[0])
            )

            beam = int(
                float(fields[1])
            )

            dtype = int(
                float(fields[2])
            )

            w1 = float(
                fields[3]
            )

            dw = float(
                fields[4]
            )

            nw = int(
                float(fields[5])
            )

        except Exception as e:

            print(
                "BAD SPEC {}: {}"
                .format(
                    spec_number,
                    e
                )
            )

            continue

        records[spec_number] = {
            "aperture": aperture,
            "beam": beam,
            "dtype": dtype,
            "w1": w1,
            "dw": dw,
            "nw": nw,
            "raw_spec": text,
        }

    return records, wat


# ============================================================
# WAVELENGTH AXIS
# ============================================================

def wavelength_axis(rec, npix):

    nw = rec["nw"]

    # Sanity check.
    if nw < 100 or nw > 100000:

        raise RuntimeError(
            "suspicious nw={}".format(nw)
        )

    n = min(
        int(npix),
        int(nw)
    )

    pix = np.arange(
        n,
        dtype=float
    )

    dtype = rec["dtype"]

    if dtype == 0:

        wave_A = (
            rec["w1"]
            + rec["dw"] * pix
        )

    elif dtype == 1:

        wave_A = 10.0 ** (
            rec["w1"]
            + rec["dw"] * pix
        )

    else:

        raise RuntimeError(
            "unsupported dtype={}"
            .format(dtype)
        )

    # Angstrom -> nm
    return wave_A / 10.0


# ============================================================
# STORAGE
# ============================================================

all_candidates = []
coverage_rows = []
diagnostic_rows = []
parser_rows = []


# ============================================================
# PROCESS FILES
# ============================================================

for filename in FILES:

    path = Path(filename)

    print("\n")
    print("=" * 72)
    print("FILE:", filename)
    print("=" * 72)

    if not path.exists():

        print("FILE MISSING")

        diagnostic_rows.append({
            "file": filename,
            "order": "",
            "status": "FILE_MISSING",
            "details": ""
        })

        continue

    # --------------------------------------------------------
    # OPEN FITS
    # --------------------------------------------------------

    try:

        with fits.open(path) as hdul:

            hdu = next(
                h for h in hdul
                if h.data is not None
            )

            header = hdu.header

            data = np.squeeze(
                np.asarray(
                    hdu.data,
                    dtype=float
                )
            )

    except Exception as e:

        print(
            "OPEN FAILED:",
            e
        )

        diagnostic_rows.append({
            "file": filename,
            "order": "",
            "status": "OPEN_FAILED",
            "details": str(e)
        })

        continue

    if data.ndim == 1:

        data = data[
            np.newaxis,
            :
        ]

    print(
        "data shape:",
        data.shape
    )

    if data.ndim != 2:

        diagnostic_rows.append({
            "file": filename,
            "order": "",
            "status": "BAD_DATA_SHAPE",
            "details": str(data.shape)
        })

        continue

    # --------------------------------------------------------
    # PARSE MULTISPEC
    # --------------------------------------------------------

    specs, wat = extract_spec_records(
        header
    )

    print(
        "data orders:",
        data.shape[0]
    )

    print(
        "wavelength solutions:",
        len(specs)
    )

    # Save complete WAT string for inspection.
    wat_file = (
        OUT /
        "{}_WAT2.txt".format(
            filename.replace(
                ".fits",
                ""
            )
        )
    )

    wat_file.write_text(
        wat,
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # RECORD PARSER RESULT
    # --------------------------------------------------------

    for spec_number in sorted(
        specs.keys()
    ):

        rec = specs[
            spec_number
        ]

        parser_rows.append({
            "file":
                filename,

            "spec":
                spec_number,

            "aperture":
                rec["aperture"],

            "beam":
                rec["beam"],

            "dtype":
                rec["dtype"],

            "w1_A":
                rec["w1"],

            "dw_A":
                rec["dw"],

            "nw":
                rec["nw"],

            "raw_spec":
                rec["raw_spec"]
        })

        print(
            "spec {:2d}: "
            "dtype={} "
            "w1={:.6f} A "
            "dw={:.9f} A "
            "nw={}"
            .format(
                spec_number,
                rec["dtype"],
                rec["w1"],
                rec["dw"],
                rec["nw"]
            )
        )

    # --------------------------------------------------------
    # ANALYZE EACH ORDER
    # --------------------------------------------------------

    for order_index in range(
        data.shape[0]
    ):

        spec_number = (
            order_index + 1
        )

        if spec_number not in specs:

            print(
                "SKIP order {}: "
                "no wavelength solution"
                .format(spec_number)
            )

            diagnostic_rows.append({
                "file": filename,
                "order": spec_number,
                "status":
                    "NO_WAVELENGTH_SOLUTION",
                "details": ""
            })

            continue

        rec = specs[
            spec_number
        ]

        flux = np.asarray(
            data[order_index],
            dtype=float
        )

        # ----------------------------------------------------
        # WAVELENGTH AXIS
        # ----------------------------------------------------

        try:

            wave = wavelength_axis(
                rec,
                len(flux)
            )

        except Exception as e:

            print(
                "SKIP order {}: {}"
                .format(
                    spec_number,
                    e
                )
            )

            diagnostic_rows.append({
                "file": filename,
                "order": spec_number,
                "status":
                    "WAVELENGTH_FAILED",
                "details": str(e)
            })

            continue

        flux = flux[
            :len(wave)
        ]

        # ----------------------------------------------------
        # FINITE VALUES
        # ----------------------------------------------------

        mask = (
            np.isfinite(wave)
            &
            np.isfinite(flux)
        )

        wave = wave[mask]
        flux = flux[mask]

        if len(wave) < 100:

            diagnostic_rows.append({
                "file": filename,
                "order": spec_number,
                "status":
                    "TOO_FEW_POINTS",
                "details":
                    "points={}".format(
                        len(wave)
                    )
            })

            continue

        # ----------------------------------------------------
        # SORT
        # ----------------------------------------------------

        idx = np.argsort(
            wave
        )

        wave = wave[idx]
        flux = flux[idx]

        # ----------------------------------------------------
        # EDGE TRIM
        # ----------------------------------------------------

        trim = int(
            len(wave)
            * EDGE_FRACTION
        )

        if (
            trim > 0
            and
            len(wave)
            > 2 * trim + 100
        ):

            wave = wave[
                trim:-trim
            ]

            flux = flux[
                trim:-trim
            ]

        # ----------------------------------------------------
        # SAMPLING
        # ----------------------------------------------------

        sampling = np.median(
            np.diff(wave)
        )

        if (
            not np.isfinite(sampling)
            or sampling <= 0
        ):

            diagnostic_rows.append({
                "file": filename,
                "order": spec_number,
                "status":
                    "BAD_SAMPLING",
                "details":
                    str(sampling)
            })

            continue

        # ----------------------------------------------------
        # COVERAGE
        # ----------------------------------------------------

        coverage_rows.append({
            "file":
                filename,

            "order":
                spec_number,

            "start_nm":
                float(
                    wave.min()
                ),

            "end_nm":
                float(
                    wave.max()
                ),

            "sampling_nm":
                float(
                    sampling
                ),

            "pixels":
                len(wave),

            "dtype":
                rec["dtype"],

            "w1_A":
                rec["w1"],

            "dw_A":
                rec["dw"],

            "nw_header":
                rec["nw"]
        })

        print(
            "ORDER {:2d}: "
            "{:9.3f} - {:9.3f} nm "
            "step={:.6f} nm "
            "pixels={}"
            .format(
                spec_number,
                wave.min(),
                wave.max(),
                sampling,
                len(wave)
            )
        )

        # ----------------------------------------------------
        # CONTINUUM
        # ----------------------------------------------------

        win = int(
            round(
                CONTINUUM_NM
                / sampling
            )
        )

        if win % 2 == 0:
            win += 1

        win = max(
            win,
            11
        )

        if win >= len(flux):

            win = (
                len(flux) - 1
            )

            if win % 2 == 0:
                win -= 1

        if win < 5:

            diagnostic_rows.append({
                "file": filename,
                "order": spec_number,
                "status":
                    "BAD_CONTINUUM_WINDOW",
                "details":
                    str(win)
            })

            continue

        try:

            continuum = savgol_filter(
                flux,
                window_length=win,
                polyorder=3
            )

        except Exception as e:

            diagnostic_rows.append({
                "file": filename,
                "order": spec_number,
                "status":
                    "CONTINUUM_FAILED",
                "details": str(e)
            })

            continue

        # ----------------------------------------------------
        # NORMALIZED RESIDUAL
        # ----------------------------------------------------

        continuum_floor = (
            np.nanmedian(
                np.abs(
                    continuum
                )
            )
            * 1e-8
        )

        scale = np.maximum(
            np.abs(
                continuum
            ),
            continuum_floor
        )

        residual = (
            flux - continuum
        ) / scale

        sigma = robust_sigma(
            residual
        )

        if (
            not np.isfinite(sigma)
            or sigma <= 0
        ):

            diagnostic_rows.append({
                "file": filename,
                "order": spec_number,
                "status":
                    "BAD_SIGMA",
                "details":
                    str(sigma)
            })

            continue

        prominence = (
            SIGMA_LIMIT
            * sigma
        )

        distance_points = max(
            1,
            int(
                round(
                    MIN_DISTANCE_NM
                    / sampling
                )
            )
        )

        # ----------------------------------------------------
        # BLIND LOCAL HIGHS
        # ----------------------------------------------------

        pos, pos_properties = (
            find_peaks(
                residual,
                prominence=prominence,
                distance=distance_points
            )
        )

        # ----------------------------------------------------
        # BLIND LOCAL LOWS
        # ----------------------------------------------------

        neg, neg_properties = (
            find_peaks(
                -residual,
                prominence=prominence,
                distance=distance_points
            )
        )

        # ----------------------------------------------------
        # SAVE LOCAL HIGHS
        # ----------------------------------------------------

        for j, p in enumerate(pos):

            all_candidates.append({
                "file":
                    filename,

                "order":
                    spec_number,

                "wavelength_nm":
                    float(
                        wave[p]
                    ),

                "type":
                    "EMISSION_LIKE",

                "sigma_score":
                    float(
                        pos_properties[
                            "prominences"
                        ][j]
                        / sigma
                    ),

                "fractional_residual":
                    float(
                        residual[p]
                    ),

                "sampling_nm":
                    float(
                        sampling
                    )
            })

        # ----------------------------------------------------
        # SAVE LOCAL LOWS
        # ----------------------------------------------------

        for j, p in enumerate(neg):

            all_candidates.append({
                "file":
                    filename,

                "order":
                    spec_number,

                "wavelength_nm":
                    float(
                        wave[p]
                    ),

                "type":
                    "ABSORPTION_LIKE",

                "sigma_score":
                    float(
                        neg_properties[
                            "prominences"
                        ][j]
                        / sigma
                    ),

                "fractional_residual":
                    float(
                        residual[p]
                    ),

                "sampling_nm":
                    float(
                        sampling
                    )
            })

        diagnostic_rows.append({
            "file":
                filename,

            "order":
                spec_number,

            "status":
                "OK",

            "details":
                "high={} low={} sigma={:.8g}"
                .format(
                    len(pos),
                    len(neg),
                    sigma
                )
        })


# ============================================================
# SAVE PARSER INFORMATION
# ============================================================

parser_df = pd.DataFrame(
    parser_rows
)

parser_df.to_csv(
    OUT /
    "ritter_v2_parser.csv",
    index=False
)


# ============================================================
# SAVE DIAGNOSTICS
# ============================================================

diagnostics = pd.DataFrame(
    diagnostic_rows
)

diagnostics.to_csv(
    OUT /
    "ritter_v2_diagnostics.csv",
    index=False
)


# ============================================================
# SAVE COVERAGE
# ============================================================

coverage = pd.DataFrame(
    coverage_rows
)

coverage.to_csv(
    OUT /
    "ritter_v2_coverage.csv",
    index=False
)


# ============================================================
# SAVE CANDIDATES
# ============================================================

cand = pd.DataFrame(
    all_candidates
)

if len(cand):

    cand = cand.sort_values(
        [
            "wavelength_nm",
            "type",
            "file"
        ]
    ).reset_index(
        drop=True
    )

cand.to_csv(
    OUT /
    "ritter_v2_blind_candidates.csv",
    index=False
)


# ============================================================
# CROSS-MATCH THE TWO RITTER OBSERVATIONS
#
# Same type only.
# Frozen tolerance = 0.03 nm.
# ============================================================

matches = []


if len(cand):

    a = cand[
        cand["file"]
        == FILES[0]
    ].copy()

    b = cand[
        cand["file"]
        == FILES[1]
    ].copy()

    for _, r1 in a.iterrows():

        same_type = b[
            b["type"]
            == r1["type"]
        ]

        if len(same_type) == 0:
            continue

        delta = np.abs(
            same_type[
                "wavelength_nm"
            ].values
            -
            r1[
                "wavelength_nm"
            ]
        )

        j = int(
            np.argmin(
                delta
            )
        )

        if (
            delta[j]
            <= MATCH_TOLERANCE_NM
        ):

            r2 = (
                same_type.iloc[j]
            )

            matches.append({
                "type":
                    r1["type"],

                "file1_order":
                    int(
                        r1["order"]
                    ),

                "file2_order":
                    int(
                        r2["order"]
                    ),

                "file1_wavelength_nm":
                    float(
                        r1[
                            "wavelength_nm"
                        ]
                    ),

                "file2_wavelength_nm":
                    float(
                        r2[
                            "wavelength_nm"
                        ]
                    ),

                "difference_nm":
                    float(
                        delta[j]
                    ),

                "mean_wavelength_nm":
                    float(
                        (
                            r1[
                                "wavelength_nm"
                            ]
                            +
                            r2[
                                "wavelength_nm"
                            ]
                        )
                        / 2.0
                    ),

                "file1_sigma_score":
                    float(
                        r1[
                            "sigma_score"
                        ]
                    ),

                "file2_sigma_score":
                    float(
                        r2[
                            "sigma_score"
                        ]
                    )
            })


match_df = pd.DataFrame(
    matches
)

if len(match_df):

    match_df = (
        match_df
        .sort_values(
            "mean_wavelength_nm"
        )
        .reset_index(
            drop=True
        )
    )


match_df.to_csv(
    OUT /
    "ritter_v2_blind_matches.csv",
    index=False
)


# ============================================================
# SUMMARY
# ============================================================

successful_orders = 0

if len(diagnostics):

    successful_orders = int(
        (
            diagnostics[
                "status"
            ]
            == "OK"
        ).sum()
    )


summary = pd.DataFrame([
    {
        "version":
            "RITTER_BLIND_V2",

        "files":
            len(FILES),

        "expected_orders":
            21,

        "parsed_wavelength_solutions":
            len(parser_df),

        "successful_orders":
            successful_orders,

        "coverage_orders":
            len(coverage),

        "blind_candidates":
            len(cand),

        "blind_matches":
            len(match_df),

        "sigma_limit":
            SIGMA_LIMIT,

        "continuum_nm":
            CONTINUUM_NM,

        "minimum_distance_nm":
            MIN_DISTANCE_NM,

        "match_tolerance_nm":
            MATCH_TOLERANCE_NM,

        "atomic_tables_used":
            False
    }
])


summary.to_csv(
    OUT /
    "ritter_v2_summary.csv",
    index=False
)


# ============================================================
# TERMINAL SUMMARY
# ============================================================

print("\n")
print("=" * 72)
print("RITTER BLIND V2 FINISHED")
print("=" * 72)

print(
    "Expected orders:             21"
)

print(
    "Parsed wavelength solutions:",
    len(parser_df)
)

print(
    "Successful analyzed orders: ",
    successful_orders
)

print(
    "Blind candidates:            ",
    len(cand)
)

print(
    "Blind matches:               ",
    len(match_df)
)

print("\nOUTPUT DIRECTORY:")
print(OUT)

print("\nCSV:")
print("ritter_v2_parser.csv")
print("ritter_v2_diagnostics.csv")
print("ritter_v2_coverage.csv")
print("ritter_v2_blind_candidates.csv")
print("ritter_v2_blind_matches.csv")
print("ritter_v2_summary.csv")

print("\nNO ATOMIC LINE TABLE WAS USED.")