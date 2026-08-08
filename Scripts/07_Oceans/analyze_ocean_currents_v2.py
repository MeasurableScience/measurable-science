#!/usr/bin/env python3
"""
Ocean Current Analyzer v2.0

Robust analyzer for PANGAEA tab-separated current-meter files, including:
- Yermak Plateau Y1/Y3/Y4/Y5 processed mooring format
- AURORA1 current-meter format
- Generic PANGAEA tables containing Date/Time, Cur vel U and Cur vel V

Outputs:
- per_series_summary.csv
- tidal_constituents.csv
- errors.csv
- PNG plots for each usable current series
- vertical profile plots for each mooring/file
- PDF report containing all generated figures

Usage:
    python3 analyze_ocean_currents_v2.py INPUT_FOLDER -o results
    python3 analyze_ocean_currents_v2.py file1.tab file2.tab -o results
"""

from __future__ import annotations

import argparse
import math
import re
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

try:
    from scipy import signal
except ImportError as exc:
    raise SystemExit(
        "SciPy is required. Install dependencies with:\n"
        "python3 -m pip install numpy pandas scipy matplotlib"
    ) from exc


CONSTITUENTS = {
    "M2": 12.4206012,
    "S2": 12.0000000,
    "N2": 12.6583475,
    "K2": 11.9672348,
    "K1": 23.9344721,
    "O1": 25.8193387,
    "P1": 24.0658877,
    "Q1": 26.8683567,
}

TIME_CANDIDATES = ("Date/Time", "DATE/TIME", "datetime", "time")
U_CANDIDATES = ("Cur vel U [cm/s]", "Cur vel U", "u", "U")
V_CANDIDATES = ("Cur vel V [cm/s]", "Cur vel V", "v", "V")
DEPTH_CANDIDATES = ("Depth water [m]", "Depth water", "depth", "Depth")
SERIAL_CANDIDATES = ("Ser No", "Serial number", "Serial", "SN")
GEAR_CANDIDATES = ("Gear ID", "Gear", "Instrument ID")
EVENT_CANDIDATES = ("Event", "Event label")


@dataclass
class ParsedFile:
    path: Path
    dataframe: pd.DataFrame
    format_name: str


def clean_column_name(name: object) -> str:
    return re.sub(r"\s+", " ", str(name).strip())


def find_column(columns: Iterable[str], candidates: Iterable[str]) -> str | None:
    cols = list(columns)
    exact = {clean_column_name(c).casefold(): c for c in cols}
    for candidate in candidates:
        hit = exact.get(clean_column_name(candidate).casefold())
        if hit is not None:
            return hit

    # Fallback: tolerant matching.
    for c in cols:
        lc = clean_column_name(c).casefold()
        for candidate in candidates:
            needle = clean_column_name(candidate).casefold()
            if needle in lc or lc in needle:
                return c
    return None


def detect_header_line(path: Path) -> int:
    """
    Return zero-based line number of the actual tabular header.
    It must contain Date/Time and both current components.
    """
    with path.open("r", encoding="utf-8-sig", errors="replace") as handle:
        for i, line in enumerate(handle):
            stripped = line.strip()
            if not stripped or stripped.startswith("/*") or stripped.startswith("*"):
                continue
            parts = [clean_column_name(x) for x in line.rstrip("\r\n").split("\t")]
            folded = {p.casefold() for p in parts}
            has_time = any("date/time" in p or p in {"datetime", "time"} for p in folded)
            has_u = any("cur vel u" in p or p == "u" for p in folded)
            has_v = any("cur vel v" in p or p == "v" for p in folded)
            if has_time and has_u and has_v:
                return i
    raise ValueError("Could not find a table header containing Date/Time, Cur vel U and Cur vel V")


def read_pangaea_tab(path: Path) -> ParsedFile:
    header_line = detect_header_line(path)
    df = pd.read_csv(
        path,
        sep="\t",
        skiprows=header_line,
        header=0,
        dtype=str,
        engine="python",
        encoding="utf-8-sig",
        on_bad_lines="skip",
    )
    df.columns = [clean_column_name(c) for c in df.columns]

    time_col = find_column(df.columns, TIME_CANDIDATES)
    u_col = find_column(df.columns, U_CANDIDATES)
    v_col = find_column(df.columns, V_CANDIDATES)
    depth_col = find_column(df.columns, DEPTH_CANDIDATES)
    serial_col = find_column(df.columns, SERIAL_CANDIDATES)
    gear_col = find_column(df.columns, GEAR_CANDIDATES)
    event_col = find_column(df.columns, EVENT_CANDIDATES)

    missing = [
        label for label, col in
        (("Date/Time", time_col), ("Cur vel U", u_col), ("Cur vel V", v_col))
        if col is None
    ]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    out = pd.DataFrame()
    out["time"] = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    out["u_cm_s"] = pd.to_numeric(df[u_col], errors="coerce")
    out["v_cm_s"] = pd.to_numeric(df[v_col], errors="coerce")
    out["depth_m"] = (
        pd.to_numeric(df[depth_col], errors="coerce") if depth_col else np.nan
    )
    out["serial"] = df[serial_col].astype(str).str.strip() if serial_col else ""
    out["gear"] = df[gear_col].astype(str).str.strip() if gear_col else ""
    out["event"] = df[event_col].astype(str).str.strip() if event_col else path.stem

    # Keep only actual current rows. This removes CTD/MicroCAT rows from Y files.
    out = out.dropna(subset=["time", "u_cm_s", "v_cm_s"]).copy()
    if out.empty:
        raise ValueError("No rows with valid Date/Time, Cur vel U and Cur vel V were found")

    if serial_col:
        fmt = "AURORA/current-meter"
    elif gear_col:
        fmt = "Yermak/ADCP"
    else:
        fmt = "generic"

    return ParsedFile(path=path, dataframe=out, format_name=fmt)


def assign_series_ids(parsed: ParsedFile) -> pd.DataFrame:
    """
    AURORA: group by instrument serial number.
    Y moorings: ADCP depths may move because of mooring blow-down, so assign
    a stable bin index by sorting depth at every timestamp within each Gear ID.
    Generic: use rounded depth or a single series.
    """
    df = parsed.dataframe.copy()

    if parsed.format_name == "AURORA/current-meter":
        serial = df["serial"].replace({"": "unknown"})
        df["series_id"] = "SN" + serial.astype(str)
        df["nominal_depth_m"] = df.groupby("series_id")["depth_m"].transform("median")

    elif parsed.format_name == "Yermak/ADCP":
        df["gear"] = df["gear"].replace({"": "unknown"})
        # Stable vertical-cell index for each timestamp and gear.
        df = df.sort_values(["gear", "time", "depth_m"], kind="stable")
        df["bin_index"] = df.groupby(["gear", "time"], dropna=False).cumcount()
        df["series_id"] = (
            "Gear" + df["gear"].astype(str) + "_bin" +
            df["bin_index"].astype(int).astype(str).str.zfill(2)
        )
        df["nominal_depth_m"] = df.groupby("series_id")["depth_m"].transform("median")

    else:
        if df["depth_m"].notna().any():
            rounded = df["depth_m"].round(1)
            df["series_id"] = "depth_" + rounded.astype(str) + "m"
            df["nominal_depth_m"] = rounded
        else:
            df["series_id"] = "current"
            df["nominal_depth_m"] = np.nan

    return df.sort_values(["series_id", "time"])


def infer_dt_hours(times: pd.Series) -> float:
    t = pd.to_datetime(times, utc=True).sort_values().drop_duplicates()
    if len(t) < 3:
        return float("nan")
    diffs = t.diff().dt.total_seconds().dropna().to_numpy() / 3600.0
    diffs = diffs[np.isfinite(diffs) & (diffs > 0)]
    return float(np.median(diffs)) if len(diffs) else float("nan")


def regularize(group: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    group = (
        group[["time", "u_cm_s", "v_cm_s"]]
        .dropna()
        .sort_values("time")
        .drop_duplicates("time", keep="last")
        .set_index("time")
    )
    dt_h = infer_dt_hours(pd.Series(group.index))
    if not np.isfinite(dt_h) or dt_h <= 0:
        raise ValueError("Could not infer a valid sampling interval")

    seconds = max(1, int(round(dt_h * 3600)))
    freq = pd.to_timedelta(seconds, unit="s")
    regular = group.resample(freq).mean()

    # Interpolate only short gaps; long gaps remain NaN.
    max_gap_samples = max(1, int(round(6.0 / dt_h)))
    regular[["u_cm_s", "v_cm_s"]] = regular[["u_cm_s", "v_cm_s"]].interpolate(
        method="time", limit=max_gap_samples, limit_area="inside"
    )
    return regular, dt_h


def harmonic_fit(t_hours: np.ndarray, values: np.ndarray, period_h: float) -> dict:
    mask = np.isfinite(t_hours) & np.isfinite(values)
    t = t_hours[mask]
    y = values[mask]
    if len(y) < 24:
        return {"amplitude": np.nan, "phase_deg": np.nan, "r2": np.nan, "offset": np.nan}

    omega = 2.0 * np.pi / period_h
    X = np.column_stack([np.ones_like(t), np.cos(omega * t), np.sin(omega * t)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    fitted = X @ beta
    ss_res = np.sum((y - fitted) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    amp = float(np.hypot(beta[1], beta[2]))
    phase = float(np.degrees(np.arctan2(-beta[2], beta[1])) % 360.0)
    r2 = float(1.0 - ss_res / ss_tot) if ss_tot > 0 else np.nan
    return {"amplitude": amp, "phase_deg": phase, "r2": r2, "offset": float(beta[0])}


def vector_harmonic_and_ellipse(t_hours: np.ndarray, u: np.ndarray, v: np.ndarray, period_h: float) -> dict:
    fu = harmonic_fit(t_hours, u, period_h)
    fv = harmonic_fit(t_hours, v, period_h)

    omega = 2.0 * np.pi / period_h
    mask = np.isfinite(t_hours) & np.isfinite(u) & np.isfinite(v)
    if mask.sum() < 24:
        return {
            **{f"u_{k}": val for k, val in fu.items()},
            **{f"v_{k}": val for k, val in fv.items()},
            "major_cm_s": np.nan, "minor_cm_s": np.nan,
            "orientation_deg": np.nan, "rotation": "unknown",
        }

    t = t_hours[mask]
    X = np.column_stack([np.ones_like(t), np.cos(omega*t), np.sin(omega*t)])
    bu, *_ = np.linalg.lstsq(X, u[mask], rcond=None)
    bv, *_ = np.linalg.lstsq(X, v[mask], rcond=None)

    # Parametric ellipse: [u,v] = center + A * [cos, sin].
    A = np.array([[bu[1], bu[2]], [bv[1], bv[2]]], dtype=float)
    U_svd, singular, _ = np.linalg.svd(A)
    major = float(singular[0])
    minor_abs = float(singular[1])
    major_vector = U_svd[:, 0]
    orientation = float(np.degrees(np.arctan2(major_vector[0], major_vector[1])) % 180.0)

    # Signed rotation from trajectory over one cycle.
    phase = np.linspace(0, 2*np.pi, 721)
    uv = A @ np.vstack([np.cos(phase), np.sin(phase)])
    signed_area = 0.5 * np.sum(uv[0, :-1] * np.diff(uv[1]) - uv[1, :-1] * np.diff(uv[0]))
    # In east/north coordinates positive signed area is CCW.
    rotation = "CCW" if signed_area > 0 else "CW"
    minor = minor_abs if rotation == "CCW" else -minor_abs

    return {
        **{f"u_{k}": val for k, val in fu.items()},
        **{f"v_{k}": val for k, val in fv.items()},
        "major_cm_s": major,
        "minor_cm_s": minor,
        "orientation_deg": orientation,
        "rotation": rotation,
    }


def welch_spectrum(values: np.ndarray, dt_h: float) -> tuple[np.ndarray, np.ndarray]:
    x = np.asarray(values, dtype=float)
    mask = np.isfinite(x)
    if mask.sum() < 32:
        return np.array([]), np.array([])
    # Fill remaining gaps only for spectral estimation.
    s = pd.Series(x).interpolate(limit_direction="both")
    x = signal.detrend(s.to_numpy())
    fs = 1.0 / dt_h  # samples per hour
    nperseg = min(len(x), max(32, int(round(24 * 14 / dt_h))))
    f, p = signal.welch(x, fs=fs, nperseg=nperseg, detrend="linear", scaling="density")
    return f, p


def safe_name(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_.-]+", "_", text)
    return text.strip("_")[:160] or "series"


def make_series_plots(
    file_stem: str,
    series_id: str,
    depth_m: float,
    regular: pd.DataFrame,
    dt_h: float,
    out_dir: Path,
) -> list[Path]:
    paths: list[Path] = []
    u = regular["u_cm_s"].to_numpy(float)
    v = regular["v_cm_s"].to_numpy(float)
    time = regular.index
    label = f"{file_stem} | {series_id} | depth≈{depth_m:.1f} m" if np.isfinite(depth_m) else f"{file_stem} | {series_id}"
    stem = safe_name(f"{file_stem}_{series_id}")

    # Time series, limited to first 30 days for readability.
    fig, ax = plt.subplots(figsize=(11, 4.8))
    view = regular.iloc[:max(1, int(round(30*24/dt_h)))]
    ax.plot(view.index, view["u_cm_s"], label="U east-west")
    ax.plot(view.index, view["v_cm_s"], label="V north-south")
    ax.set_title(label + " — first 30 days")
    ax.set_ylabel("Current velocity [cm/s]")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    p = out_dir / f"{stem}_timeseries.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    paths.append(p)

    # Spectrum in cycles/day, focusing on tidal band.
    fu, pu = welch_spectrum(u, dt_h)
    fv, pv = welch_spectrum(v, dt_h)
    if len(fu):
        fig, ax = plt.subplots(figsize=(9, 5.5))
        cpd = fu * 24.0
        ax.semilogy(cpd[1:], pu[1:], label="U")
        ax.semilogy(cpd[1:], pv[1:], label="V")
        for name, period in CONSTITUENTS.items():
            freq_cpd = 24.0 / period
            ax.axvline(freq_cpd, linewidth=0.8, alpha=0.5)
            ax.text(freq_cpd, ax.get_ylim()[1] / 2, name, rotation=90, va="center", ha="right", fontsize=8)
        ax.set_xlim(0, min(6, np.nanmax(cpd)))
        ax.set_xlabel("Frequency [cycles/day]")
        ax.set_ylabel("PSD [(cm/s)² per cycles/hour]")
        ax.set_title(label + " — Welch spectrum")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        p = out_dir / f"{stem}_spectrum.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)

    # Hodograph.
    mask = np.isfinite(u) & np.isfinite(v)
    if mask.sum() >= 24:
        stride = max(1, mask.sum() // 5000)
        uu = u[mask][::stride]
        vv = v[mask][::stride]
        fig, ax = plt.subplots(figsize=(6.5, 6.5))
        ax.plot(uu, vv, linewidth=0.6, alpha=0.65)
        ax.axhline(0, linewidth=0.8)
        ax.axvline(0, linewidth=0.8)
        ax.set_aspect("equal", adjustable="datalim")
        ax.set_xlabel("U east [cm/s]")
        ax.set_ylabel("V north [cm/s]")
        ax.set_title(label + " — hodograph")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        p = out_dir / f"{stem}_hodograph.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)

        # Progressive vector diagram, both net and demeaned track.
        dt_seconds = dt_h * 3600.0
        u_fill = pd.Series(u).interpolate(limit_direction="both").to_numpy()
        v_fill = pd.Series(v).interpolate(limit_direction="both").to_numpy()
        x_km = np.cumsum(u_fill * 0.01 * dt_seconds) / 1000.0
        y_km = np.cumsum(v_fill * 0.01 * dt_seconds) / 1000.0
        xd_km = np.cumsum((u_fill - np.nanmean(u_fill)) * 0.01 * dt_seconds) / 1000.0
        yd_km = np.cumsum((v_fill - np.nanmean(v_fill)) * 0.01 * dt_seconds) / 1000.0

        fig, ax = plt.subplots(figsize=(7, 6))
        ax.plot(x_km, y_km, label="Net transport")
        ax.plot(xd_km, yd_km, label="Mean removed", alpha=0.8)
        ax.scatter([x_km[0]], [y_km[0]], marker="o", label="Start")
        ax.scatter([x_km[-1]], [y_km[-1]], marker="x", label="End")
        ax.set_xlabel("East displacement [km]")
        ax.set_ylabel("North displacement [km]")
        ax.set_title(label + " — progressive vector diagram")
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_aspect("equal", adjustable="datalim")
        fig.tight_layout()
        p = out_dir / f"{stem}_pvd.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)

    return paths


def analyze_file(parsed: ParsedFile, out_dir: Path, min_samples: int) -> tuple[list[dict], list[dict], list[Path]]:
    df = assign_series_ids(parsed)
    file_stem = parsed.path.stem
    series_rows: list[dict] = []
    tide_rows: list[dict] = []
    figures: list[Path] = []

    for series_id, group in df.groupby("series_id", sort=True):
        group = group.sort_values("time")
        if len(group) < min_samples:
            continue

        regular, dt_h = regularize(group)
        valid_pair = regular[["u_cm_s", "v_cm_s"]].dropna()
        if len(valid_pair) < min_samples:
            continue

        depth_m = float(group["nominal_depth_m"].median()) if group["nominal_depth_m"].notna().any() else np.nan
        t0 = regular.index[0]
        t_hours = (regular.index - t0).total_seconds().to_numpy() / 3600.0
        u = regular["u_cm_s"].to_numpy(float)
        v = regular["v_cm_s"].to_numpy(float)
        speed = np.hypot(u, v)

        series_rows.append({
            "file": parsed.path.name,
            "format": parsed.format_name,
            "series_id": series_id,
            "nominal_depth_m": depth_m,
            "start_utc": regular.index.min().isoformat(),
            "end_utc": regular.index.max().isoformat(),
            "sampling_interval_h": dt_h,
            "raw_rows": len(group),
            "regular_samples": len(regular),
            "valid_pairs": len(valid_pair),
            "coverage_fraction": len(valid_pair) / len(regular),
            "mean_u_cm_s": np.nanmean(u),
            "mean_v_cm_s": np.nanmean(v),
            "mean_speed_cm_s": np.nanmean(speed),
            "max_speed_cm_s": np.nanmax(speed),
            "std_u_cm_s": np.nanstd(u),
            "std_v_cm_s": np.nanstd(v),
        })

        for name, period_h in CONSTITUENTS.items():
            fit = vector_harmonic_and_ellipse(t_hours, u, v, period_h)
            tide_rows.append({
                "file": parsed.path.name,
                "format": parsed.format_name,
                "series_id": series_id,
                "nominal_depth_m": depth_m,
                "constituent": name,
                "period_h": period_h,
                **fit,
            })

        series_dir = out_dir / "series_plots"
        series_dir.mkdir(parents=True, exist_ok=True)
        figures.extend(make_series_plots(file_stem, series_id, depth_m, regular, dt_h, series_dir))

    # Vertical M2 profiles.
    if tide_rows:
        tides = pd.DataFrame(tide_rows)
        m2 = tides[tides["constituent"] == "M2"].dropna(subset=["nominal_depth_m"]).sort_values("nominal_depth_m")
        if len(m2) >= 2:
            prof_dir = out_dir / "profile_plots"
            prof_dir.mkdir(parents=True, exist_ok=True)

            fig, ax = plt.subplots(figsize=(6, 7))
            ax.plot(m2["major_cm_s"], m2["nominal_depth_m"], marker="o")
            ax.invert_yaxis()
            ax.set_xlabel("M2 ellipse major axis [cm/s]")
            ax.set_ylabel("Depth [m]")
            ax.set_title(file_stem + " — M2 amplitude vs depth")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            p = prof_dir / f"{safe_name(file_stem)}_M2_amplitude_depth.png"
            fig.savefig(p, dpi=150)
            plt.close(fig)
            figures.append(p)

            fig, ax = plt.subplots(figsize=(6, 7))
            phase = np.degrees(np.angle(
                m2["u_amplitude"].to_numpy() * np.exp(1j*np.radians(m2["u_phase_deg"].to_numpy())) +
                1j * m2["v_amplitude"].to_numpy() * np.exp(1j*np.radians(m2["v_phase_deg"].to_numpy()))
            )) % 360
            ax.scatter(phase, m2["nominal_depth_m"])
            ax.invert_yaxis()
            ax.set_xlim(0, 360)
            ax.set_xlabel("Approximate vector phase [deg]")
            ax.set_ylabel("Depth [m]")
            ax.set_title(file_stem + " — M2 phase vs depth")
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            p = prof_dir / f"{safe_name(file_stem)}_M2_phase_depth.png"
            fig.savefig(p, dpi=150)
            plt.close(fig)
            figures.append(p)

    return series_rows, tide_rows, figures


def collect_input_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        p = Path(item).expanduser()
        if p.is_dir():
            files.extend(sorted(p.rglob("*.tab")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"WARNING: input does not exist: {p}", file=sys.stderr)
    # De-duplicate while preserving order.
    seen = set()
    result = []
    for p in files:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            result.append(p)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze PANGAEA ocean current-meter .tab files")
    parser.add_argument("inputs", nargs="+", help=".tab files and/or folders containing .tab files")
    parser.add_argument("-o", "--output", default="results_v2", help="output folder")
    parser.add_argument("--min-samples", type=int, default=96, help="minimum valid samples per series")
    parser.add_argument("--no-pdf", action="store_true", help="skip combined PDF report")
    args = parser.parse_args()

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    files = collect_input_files(args.inputs)
    if not files:
        print("No .tab input files found.", file=sys.stderr)
        return 2

    all_series: list[dict] = []
    all_tides: list[dict] = []
    all_figures: list[Path] = []
    errors: list[dict] = []

    print(f"Found {len(files)} .tab file(s).")
    for path in files:
        try:
            print(f"\nReading: {path.name}")
            parsed = read_pangaea_tab(path)
            print(f"  format: {parsed.format_name}")
            print(f"  valid current rows: {len(parsed.dataframe):,}")
            series, tides, figures = analyze_file(parsed, out_dir, args.min_samples)
            print(f"  analyzed series: {len(series)}")
            all_series.extend(series)
            all_tides.extend(tides)
            all_figures.extend(figures)
        except Exception as exc:
            print(f"  ERROR: {exc}", file=sys.stderr)
            errors.append({
                "file": path.name,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            })

    pd.DataFrame(all_series).to_csv(out_dir / "per_series_summary.csv", index=False)
    pd.DataFrame(all_tides).to_csv(out_dir / "tidal_constituents.csv", index=False)
    pd.DataFrame(errors).to_csv(out_dir / "errors.csv", index=False)

    if all_figures and not args.no_pdf:
        pdf_path = out_dir / "ocean_current_report.pdf"
        with PdfPages(pdf_path) as pdf:
            for image_path in all_figures:
                try:
                    img = plt.imread(image_path)
                    fig, ax = plt.subplots(figsize=(11.69, 8.27))
                    ax.imshow(img)
                    ax.axis("off")
                    ax.set_title(image_path.stem, fontsize=9)
                    fig.tight_layout()
                    pdf.savefig(fig)
                    plt.close(fig)
                except Exception as exc:
                    print(f"WARNING: could not add {image_path.name} to PDF: {exc}", file=sys.stderr)

    print("\nFinished.")
    print(f"Results folder: {out_dir.resolve()}")
    print(f"Series analyzed: {len(all_series)}")
    print(f"Tidal fits written: {len(all_tides)}")
    print(f"Errors: {len(errors)}")
    return 0 if all_series else 1


if __name__ == "__main__":
    raise SystemExit(main())
