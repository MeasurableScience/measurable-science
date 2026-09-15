#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ISEE CDF audit — use unchanged on BOTH Kunigami (KNG) and Istok (IST).

No filtering, no PLV, no carrier search.
Checks:
- db_dt labels and shape
- Epoch start/end and median sampling interval
- time_db_dt vs Epoch consistency, when available
- actual UTC minute-30 windows
- H/D/Z statistics and Pearson correlations
- linear H~aD+b fit and residual ratio
- exact equality / sign equality checks
- first sample values for selected windows
"""

import glob
import os
import numpy as np
import cdflib

FS_EXPECTED = 64.0
WINDOW_MINUTE = 30
WINDOW_SECONDS = 60
N_EXPECTED = int(FS_EXPECTED * WINDOW_SECONDS)
MAX_WINDOWS_TO_PRINT = None   # None = print every usable UTC hour


def txt(x):
    return x.decode(errors="replace").strip() if isinstance(x, bytes) else str(x).strip()


def pearson(a, b):
    good = np.isfinite(a) & np.isfinite(b)
    if np.count_nonzero(good) < 3:
        return np.nan
    return float(np.corrcoef(a[good], b[good])[0, 1])


def linear_fit_stats(a, b):
    """Fit a ~= slope*b + intercept; return slope/intercept/residual std ratio."""
    good = np.isfinite(a) & np.isfinite(b)
    a = a[good]
    b = b[good]
    if len(a) < 3 or np.std(b) == 0:
        return np.nan, np.nan, np.nan
    slope, intercept = np.polyfit(b, a, 1)
    resid = a - (slope * b + intercept)
    ratio = np.std(resid) / np.std(a) if np.std(a) else np.nan
    return float(slope), float(intercept), float(ratio)


def audit_file(path):
    cdf = cdflib.CDF(path)
    db = np.asarray(cdf.varget("db_dt"))
    ep = np.asarray(cdf.varget("epoch_db_dt"))
    labels = [txt(x) for x in np.asarray(cdf.varget("label_db_dt")).ravel()]

    if db.ndim != 2:
        raise RuntimeError(f"db_dt has unexpected shape {db.shape}")
    if db.shape[0] <= 16 and db.shape[1] > db.shape[0]:
        db = db.T

    dt = np.asarray(cdflib.cdfepoch.to_datetime(ep), dtype="datetime64[us]")

    print("\n" + "=" * 90)
    print(os.path.basename(path))
    print("=" * 90)
    print("db_dt shape :", db.shape)
    print("labels      :", labels)
    print("Epoch start :", np.datetime_as_string(dt[0], unit="us"))
    print("Epoch end   :", np.datetime_as_string(dt[-1], unit="us"))

    dus = np.diff(dt).astype("timedelta64[us]").astype(np.int64)
    good_dt = dus[dus > 0]
    if len(good_dt):
        med_us = float(np.median(good_dt))
        print(f"Epoch dt    : {med_us:.3f} us")
        print(f"Epoch fs    : {1e6/med_us:.9f} Hz")
        print("dt min/max  :", int(np.min(good_dt)), "/", int(np.max(good_dt)), "us")

    # Compare explicit time_db_dt to Epoch if present.
    try:
        tdb = np.asarray(cdf.varget("time_db_dt"))
        print("time_db_dt  :", tdb.shape)
        if len(tdb) == len(dt) and tdb.ndim == 2 and tdb.shape[1] >= 8:
            # Build datetime64[us] strings safely for a few strategic rows.
            test_idx = sorted(set([0, min(1, len(dt)-1), len(dt)//2, len(dt)-1]))
            print("Epoch vs time_db_dt samples:")
            for i in test_idx:
                r = tdb[i]
                s = (f"{int(r[0]):04d}-{int(r[1]):02d}-{int(r[2]):02d}T"
                     f"{int(r[3]):02d}:{int(r[4]):02d}:{int(r[5]):02d}."
                     f"{int(r[6]):03d}{int(r[7]):03d}")
                td = np.datetime64(s, "us")
                delta_us = int((dt[i] - td).astype("timedelta64[us]").astype(np.int64))
                print(f"  i={i:8d} Epoch={np.datetime_as_string(dt[i], unit='us')} "
                      f"time_db_dt={s} delta={delta_us} us")
    except Exception as e:
        print("time_db_dt  : unavailable:", repr(e))

    hour_key = dt.astype("datetime64[h]")
    unique_hours = np.unique(hour_key)

    print("\nUTC minute-30 window audit:")
    usable = 0

    for hk in unique_hours:
        sec = (dt - hk).astype("timedelta64[us]").astype(np.int64) / 1e6
        mask = ((hour_key == hk) &
                (sec >= WINDOW_MINUTE * 60) &
                (sec < WINDOW_MINUTE * 60 + WINDOW_SECONDS))
        idx = np.flatnonzero(mask)

        if len(idx) < int(0.95 * N_EXPECTED):
            continue

        idx = idx[:N_EXPECTED]
        block = db[idx, :]
        usable += 1

        H = block[:, 0].astype(float)
        D = block[:, 1].astype(float)
        Z = block[:, 2].astype(float) if block.shape[1] >= 3 else None

        h0 = np.datetime_as_string(dt[idx[0]], unit="us")
        h1 = np.datetime_as_string(dt[idx[-1]], unit="us")

        corr_hd = pearson(H, D)
        slope, intercept, resid_ratio = linear_fit_stats(H, D)

        eq_hd = np.mean(H == D)
        eq_hmd = np.mean(H == -D)

        print("\n", np.datetime_as_string(hk, unit="h"))
        print(f"  samples={len(idx)} first={h0} last={h1}")
        print(f"  H: mean={np.mean(H): .8g} std={np.std(H): .8g} min={np.min(H): .8g} max={np.max(H): .8g}")
        print(f"  D: mean={np.mean(D): .8g} std={np.std(D): .8g} min={np.min(D): .8g} max={np.max(D): .8g}")
        print(f"  corr(H,D)={corr_hd: .12f}")
        print(f"  H ~= a*D+b: a={slope: .12g} b={intercept: .12g} residual_std/H_std={resid_ratio: .12g}")
        print(f"  exact H==D={eq_hd:.6f}   exact H==-D={eq_hmd:.6f}")

        if Z is not None:
            print(f"  Z: mean={np.mean(Z): .8g} std={np.std(Z): .8g} min={np.min(Z): .8g} max={np.max(Z): .8g}")
            print(f"  corr(H,Z)={pearson(H,Z): .12f}   corr(D,Z)={pearson(D,Z): .12f}")

        print("  first 5 H/D/Z:")
        for row in block[:5, :min(3, block.shape[1])]:
            print("   ", "  ".join(f"{float(v): .10g}" for v in row))

        if MAX_WINDOWS_TO_PRINT is not None and usable >= MAX_WINDOWS_TO_PRINT:
            break

    print("\nUsable minute-30 windows:", usable)


def main():
    files = sorted(set(glob.glob("isee_induction_*.cdf") +
                       glob.glob("isee_induction_*.CDF")))
    if not files:
        raise RuntimeError("No isee_induction_*.cdf files found in current folder.")

    print("ISEE RAW CDF AUDIT — NO PLV / NO FILTERING / NO EXPECTED FREQUENCY")
    print("Files found:", len(files))
    for path in files:
        audit_file(path)


if __name__ == "__main__":
    main()
