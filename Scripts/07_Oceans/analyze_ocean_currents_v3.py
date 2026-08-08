#!/usr/bin/env python3
"""
Ocean Current Analyzer v3.0 — cross-depth and cross-station analysis.

Place beside analyze_ocean_currents_v2.py and run on the same PANGAEA .tab files.

Adds:
- unwrapped M2 amplitude/phase/orientation profiles versus depth
- M2-band coherence and lag matrices between depths
- rotary CW/CCW spectra for representative depths
- EOF/PCA modes within each mooring
- optional cross-station EOF using representative series
- optional animated M2 vectors (GIF)

Usage:
  python3 analyze_ocean_currents_v3.py . -o results_v3
  python3 analyze_ocean_currents_v3.py *.tab -o results_v3 --animation
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import traceback
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy import signal

try:
    import analyze_ocean_currents_v2 as v2
except ImportError as exc:
    raise SystemExit(
        "analyze_ocean_currents_v2.py must be in the same folder as this script."
    ) from exc

M2_PERIOD_H = 12.4206012
M2_FREQ_CPH = 1.0 / M2_PERIOD_H


def safe_name(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", str(text)).strip("_")[:160] or "station"


def station_name(path: Path) -> str:
    name = path.stem
    m = re.search(r"\b(Y[1-5])(?:-1)?\b", name, re.I)
    if m:
        return m.group(1).upper()
    if "AURORA" in name.upper():
        return "AURORA1"
    return name


def collect_files(inputs: list[str]) -> list[Path]:
    return v2.collect_input_files(inputs)


def regular_series(parsed: v2.ParsedFile, min_samples: int) -> dict[str, dict]:
    df = v2.assign_series_ids(parsed)
    out: dict[str, dict] = {}
    for sid, g in df.groupby("series_id", sort=True):
        if len(g) < min_samples:
            continue
        try:
            reg, dt_h = v2.regularize(g)
        except Exception:
            continue
        valid = reg[["u_cm_s", "v_cm_s"]].dropna()
        if len(valid) < min_samples:
            continue
        depth = float(g["nominal_depth_m"].median()) if g["nominal_depth_m"].notna().any() else np.nan
        out[str(sid)] = {"data": reg, "dt_h": float(dt_h), "depth_m": depth}
    return out


def bandpass_m2(x: np.ndarray, dt_h: float, half_width_cph: float = 0.018) -> np.ndarray:
    """Zero-phase Butterworth bandpass around M2; preserves NaNs at long gaps."""
    x = np.asarray(x, float)
    if np.isfinite(x).sum() < 96:
        return np.full_like(x, np.nan)
    s = pd.Series(x).interpolate(limit_direction="both")
    fs = 1.0 / dt_h
    nyq = 0.5 * fs
    lo = max(1e-6, M2_FREQ_CPH - half_width_cph) / nyq
    hi = min(0.999, M2_FREQ_CPH + half_width_cph) / nyq
    if not (0 < lo < hi < 1):
        return np.full_like(x, np.nan)
    sos = signal.butter(4, [lo, hi], btype="bandpass", output="sos")
    y = signal.sosfiltfilt(sos, signal.detrend(s.to_numpy()))
    return y


def common_grid(series: dict[str, dict], max_series: int = 80) -> tuple[pd.DatetimeIndex, list[str], np.ndarray, np.ndarray, np.ndarray]:
    """Build common U/V matrices, selecting evenly spaced depths when needed."""
    items = sorted(series.items(), key=lambda kv: (np.nan_to_num(kv[1]["depth_m"], nan=1e9), kv[0]))
    if len(items) > max_series:
        idx = np.unique(np.linspace(0, len(items)-1, max_series).round().astype(int))
        items = [items[i] for i in idx]
    if not items:
        raise ValueError("No usable current series")

    dt_h = max(float(v["dt_h"]) for _, v in items)
    start = max(v["data"].index.min() for _, v in items)
    end = min(v["data"].index.max() for _, v in items)
    if start >= end:
        raise ValueError("Series have no overlapping time interval")
    freq = pd.to_timedelta(max(1, int(round(dt_h * 3600))), unit="s")
    grid = pd.date_range(start=start.ceil(freq), end=end.floor(freq), freq=freq, tz="UTC")
    if len(grid) < 96:
        raise ValueError("Overlapping interval is too short")

    names, depths, umat, vmat = [], [], [], []
    for sid, item in items:
        d = item["data"].resample(freq).mean().reindex(grid)
        d = d.interpolate(method="time", limit=max(1, int(round(6/dt_h))), limit_area="inside")
        if d[["u_cm_s", "v_cm_s"]].notna().all(axis=1).mean() < 0.75:
            continue
        names.append(sid)
        depths.append(item["depth_m"])
        umat.append(d["u_cm_s"].to_numpy(float))
        vmat.append(d["v_cm_s"].to_numpy(float))
    if len(names) < 2:
        raise ValueError("Fewer than two sufficiently complete overlapping series")
    return grid, names, np.asarray(depths), np.asarray(umat), np.asarray(vmat)


def harmonic_complex(t_h: np.ndarray, y: np.ndarray, period_h: float = M2_PERIOD_H) -> complex:
    mask = np.isfinite(t_h) & np.isfinite(y)
    if mask.sum() < 48:
        return complex(np.nan, np.nan)
    omega = 2*np.pi/period_h
    X = np.column_stack([np.ones(mask.sum()), np.cos(omega*t_h[mask]), np.sin(omega*t_h[mask])])
    b, *_ = np.linalg.lstsq(X, y[mask], rcond=None)
    # y = a cos + b sin = Re[(a + i*(-b)) exp(i wt)]
    return complex(b[1], -b[2])


def m2_profiles(station: str, names: list[str], depths: np.ndarray, grid: pd.DatetimeIndex,
                umat: np.ndarray, vmat: np.ndarray, out: Path) -> tuple[pd.DataFrame, list[Path]]:
    t_h = (grid-grid[0]).total_seconds().to_numpy()/3600
    rows = []
    for sid, dep, u, v in zip(names, depths, umat, vmat):
        cu = harmonic_complex(t_h, u)
        cv = harmonic_complex(t_h, v)
        # Parametric ellipse from complex component coefficients.
        A = np.array([[cu.real, -cu.imag], [cv.real, -cv.imag]])
        svu, sv, _ = np.linalg.svd(A)
        major, minor_abs = sv
        vec = svu[:, 0]
        orientation = np.degrees(np.arctan2(vec[0], vec[1])) % 180
        phase = np.degrees(np.angle(cu + 1j*cv)) % 360
        signed_det = np.linalg.det(A)
        rotation = "CCW" if signed_det > 0 else "CW"
        minor = minor_abs if rotation == "CCW" else -minor_abs
        rows.append(dict(station=station, series_id=sid, depth_m=dep,
                         m2_major_cm_s=major, m2_minor_cm_s=minor,
                         orientation_deg=orientation, vector_phase_deg=phase,
                         rotation=rotation))
    df = pd.DataFrame(rows).sort_values("depth_m")
    if len(df):
        phase_rad = np.unwrap(np.radians(df["vector_phase_deg"].to_numpy()))
        df["phase_unwrapped_deg"] = np.degrees(phase_rad)
        if len(df) >= 3 and np.ptp(df["depth_m"]) > 0:
            slope, intercept = np.polyfit(df["depth_m"], df["phase_unwrapped_deg"], 1)
            df["phase_gradient_deg_per_m"] = slope
            # Apparent vertical phase speed: period / phase gradient.
            df["apparent_vertical_phase_speed_m_s"] = (
                360.0 / abs(slope) / (M2_PERIOD_H*3600)
                if abs(slope) > 1e-8 else np.nan
            )
        else:
            df["phase_gradient_deg_per_m"] = np.nan
            df["apparent_vertical_phase_speed_m_s"] = np.nan

    figs = []
    if len(df) >= 2:
        fig, ax = plt.subplots(figsize=(6.5, 7))
        ax.plot(df["m2_major_cm_s"], df["depth_m"], marker="o", label="Major axis")
        ax.plot(np.abs(df["m2_minor_cm_s"]), df["depth_m"], marker="s", label="|Minor axis|")
        ax.invert_yaxis(); ax.grid(True, alpha=.3); ax.legend()
        ax.set_xlabel("M2 amplitude [cm/s]"); ax.set_ylabel("Depth [m]")
        ax.set_title(f"{station} — M2 ellipse amplitude profile")
        fig.tight_layout(); p=out/f"{safe_name(station)}_M2_amplitude_profile.png"; fig.savefig(p,dpi=160); plt.close(fig); figs.append(p)

        fig, ax = plt.subplots(figsize=(6.5, 7))
        ax.plot(df["phase_unwrapped_deg"], df["depth_m"], marker="o")
        ax.invert_yaxis(); ax.grid(True, alpha=.3)
        ax.set_xlabel("Unwrapped M2 vector phase [deg]"); ax.set_ylabel("Depth [m]")
        ax.set_title(f"{station} — M2 phase propagation")
        fig.tight_layout(); p=out/f"{safe_name(station)}_M2_phase_unwrapped.png"; fig.savefig(p,dpi=160); plt.close(fig); figs.append(p)

        fig, ax = plt.subplots(figsize=(6.5, 7))
        sc=ax.scatter(df["orientation_deg"], df["depth_m"], c=np.sign(df["m2_minor_cm_s"]), s=45)
        ax.invert_yaxis(); ax.grid(True, alpha=.3); ax.set_xlim(0,180)
        ax.set_xlabel("Ellipse major-axis orientation [deg from north]"); ax.set_ylabel("Depth [m]")
        ax.set_title(f"{station} — M2 orientation (sign: CW/CCW)")
        fig.tight_layout(); p=out/f"{safe_name(station)}_M2_orientation.png"; fig.savefig(p,dpi=160); plt.close(fig); figs.append(p)
    return df, figs


def pairwise_m2_metrics(depths: np.ndarray, umat: np.ndarray, vmat: np.ndarray, dt_h: float,
                        max_lag_h: float = 8.0) -> tuple[np.ndarray, np.ndarray]:
    n = len(depths)
    coh = np.full((n,n), np.nan)
    lag = np.full((n,n), np.nan)
    z = umat + 1j*vmat
    # Complex M2-band current; coherence estimated from real and imaginary jointly.
    zb = np.empty_like(z, dtype=complex)
    for i in range(n):
        zb[i] = bandpass_m2(umat[i], dt_h) + 1j*bandpass_m2(vmat[i], dt_h)
    maxlag = max(1, int(round(max_lag_h/dt_h)))
    for i in range(n):
        coh[i,i]=1; lag[i,i]=0
        for j in range(i+1,n):
            mask=np.isfinite(zb[i]) & np.isfinite(zb[j])
            if mask.sum()<96: continue
            a=zb[i,mask]; b=zb[j,mask]
            a=a-np.mean(a); b=b-np.mean(b)
            denom=np.sqrt(np.vdot(a,a).real*np.vdot(b,b).real)
            c=abs(np.vdot(a,b))/denom if denom>0 else np.nan
            coh[i,j]=coh[j,i]=c
            # Cross-correlation on complex vectors; positive means j lags i.
            corr=signal.correlate(b, a, mode="full", method="fft")
            lags=signal.correlation_lags(len(b),len(a),mode="full")
            keep=(lags>=-maxlag)&(lags<=maxlag)
            k=np.argmax(np.abs(corr[keep])); best=lags[keep][k]*dt_h
            lag[i,j]=best; lag[j,i]=-best
    return coh, lag


def heatmap(matrix: np.ndarray, labels: list[str], title: str, cbar: str, path: Path,
            vmin=None, vmax=None) -> Path:
    fig, ax=plt.subplots(figsize=(max(7,len(labels)*.25), max(6,len(labels)*.25)))
    im=ax.imshow(matrix, aspect="auto", origin="upper", vmin=vmin, vmax=vmax)
    step=max(1,math.ceil(len(labels)/20))
    ticks=np.arange(0,len(labels),step)
    ax.set_xticks(ticks, [labels[i] for i in ticks], rotation=90, fontsize=7)
    ax.set_yticks(ticks, [labels[i] for i in ticks], fontsize=7)
    ax.set_title(title); fig.colorbar(im,ax=ax,label=cbar); fig.tight_layout()
    fig.savefig(path,dpi=160); plt.close(fig); return path


def rotary_spectrum(station: str, names: list[str], depths: np.ndarray, umat: np.ndarray,
                    vmat: np.ndarray, dt_h: float, out: Path) -> tuple[pd.DataFrame,list[Path]]:
    # Representative shallow, middle, deep series.
    idx=np.unique(np.array([0,len(names)//2,len(names)-1],int))
    rows=[]; figs=[]
    for i in idx:
        u=pd.Series(umat[i]).interpolate(limit_direction="both").to_numpy()
        v=pd.Series(vmat[i]).interpolate(limit_direction="both").to_numpy()
        z=signal.detrend(u)+1j*signal.detrend(v)
        n=len(z); win=np.hanning(n); Z=np.fft.fft(z*win); f=np.fft.fftfreq(n,d=dt_h)
        ps=np.abs(Z)**2/(np.sum(win**2))
        pos=f>0; neg=f<0
        fp=f[pos]*24; pp=ps[pos]
        fn=-f[neg][::-1]*24; pn=ps[neg][::-1]
        m=min(len(fp),len(fn)); fp=fp[:m]; pp=pp[:m]; pn=pn[:m]
        rows.append(dict(station=station,series_id=names[i],depth_m=depths[i],
                         cw_power_m2=float(np.interp(24/M2_PERIOD_H,fp,pn)),
                         ccw_power_m2=float(np.interp(24/M2_PERIOD_H,fp,pp))))
        fig,ax=plt.subplots(figsize=(8,5))
        ax.semilogy(fp,pp,label="CCW (+frequency)"); ax.semilogy(fp,pn,label="CW (-frequency)")
        ax.axvline(24/M2_PERIOD_H,ls="--",label="M2"); ax.set_xlim(0,6)
        ax.set_xlabel("Frequency [cycles/day]"); ax.set_ylabel("Rotary power")
        ax.set_title(f"{station} | {names[i]} | depth≈{depths[i]:.1f} m — rotary spectrum")
        ax.grid(True,alpha=.3); ax.legend(); fig.tight_layout()
        p=out/f"{safe_name(station)}_{safe_name(names[i])}_rotary.png"; fig.savefig(p,dpi=160); plt.close(fig); figs.append(p)
    return pd.DataFrame(rows),figs


def eof_analysis(station: str, names: list[str], depths: np.ndarray, umat: np.ndarray,
                 vmat: np.ndarray, dt_h: float, out: Path) -> tuple[pd.DataFrame,list[Path]]:
    # M2-band EOF on concatenated U and V variables, standardized per variable.
    ub=np.asarray([bandpass_m2(x,dt_h) for x in umat]); vb=np.asarray([bandpass_m2(x,dt_h) for x in vmat])
    X=np.vstack([ub,vb]).T
    good=np.isfinite(X).mean(axis=1)>.9; X=X[good]
    if len(X)<96: return pd.DataFrame(),[]
    # Fill rare missing values by column means.
    means=np.nanmean(X,axis=0); inds=np.where(~np.isfinite(X)); X[inds]=means[inds[1]]
    X-=X.mean(axis=0); sd=X.std(axis=0); sd[sd==0]=1; X/=sd
    U,S,Vt=np.linalg.svd(X,full_matrices=False)
    var=S**2/np.sum(S**2)
    nm=min(5,len(var)); rows=[]
    for k in range(nm): rows.append(dict(station=station,mode=k+1,variance_fraction=var[k]))
    figs=[]
    fig,ax=plt.subplots(figsize=(7,4.5)); ax.bar(np.arange(1,nm+1),var[:nm]*100)
    ax.set_xlabel("EOF mode"); ax.set_ylabel("Explained variance [%]"); ax.set_title(f"{station} — M2-band EOF variance")
    ax.grid(True,axis="y",alpha=.3); fig.tight_layout(); p=out/f"{safe_name(station)}_EOF_variance.png"; fig.savefig(p,dpi=160); plt.close(fig); figs.append(p)
    for k in range(min(3,nm)):
        load=Vt[k]; lu=load[:len(names)]; lv=load[len(names):]
        fig,ax=plt.subplots(figsize=(6.5,7)); ax.plot(lu,depths,marker="o",label="U loading"); ax.plot(lv,depths,marker="s",label="V loading")
        ax.invert_yaxis(); ax.axvline(0,lw=.8); ax.grid(True,alpha=.3); ax.legend()
        ax.set_xlabel("Standardized EOF loading"); ax.set_ylabel("Depth [m]")
        ax.set_title(f"{station} — EOF {k+1} ({var[k]*100:.1f}%)")
        fig.tight_layout(); p=out/f"{safe_name(station)}_EOF{k+1}_depth.png"; fig.savefig(p,dpi=160); plt.close(fig); figs.append(p)
    return pd.DataFrame(rows),figs


def animation_m2(station: str, profile: pd.DataFrame, out: Path) -> Path | None:
    try:
        from matplotlib.animation import FuncAnimation, PillowWriter
    except Exception:
        return None
    if len(profile)<2: return None
    dep=profile["depth_m"].to_numpy(); amp=profile["m2_major_cm_s"].to_numpy(); ph=np.radians(profile["vector_phase_deg"].to_numpy())
    # Stylized vector using major amplitude and phase; scientific values remain in CSV.
    fig,ax=plt.subplots(figsize=(7,7)); ax.set_xlim(-1.2*np.nanmax(amp),1.2*np.nanmax(amp)); ax.set_ylim(np.nanmax(dep)+.05*np.ptp(dep),np.nanmin(dep)-.05*np.ptp(dep))
    ax.set_xlabel("M2 vector component [cm/s]"); ax.set_ylabel("Depth [m]"); ax.set_title(f"{station} — one M2 cycle")
    q=ax.quiver(np.zeros_like(dep),dep,np.zeros_like(dep),np.zeros_like(dep),angles="xy",scale_units="xy",scale=1)
    def update(frame):
        th=2*np.pi*frame/48; x=amp*np.cos(th+ph); y=np.zeros_like(x)
        q.set_UVC(x,y); return (q,)
    ani=FuncAnimation(fig,update,frames=48,interval=80,blit=True)
    p=out/f"{safe_name(station)}_M2_vectors.gif"; ani.save(p,writer=PillowWriter(fps=12)); plt.close(fig); return p


def make_pdf(figures: list[Path], path: Path):
    with PdfPages(path) as pdf:
        for p in figures:
            if p.suffix.lower() != ".png": continue
            try:
                img=plt.imread(p); fig,ax=plt.subplots(figsize=(11.69,8.27)); ax.imshow(img); ax.axis("off"); ax.set_title(p.stem,fontsize=9); fig.tight_layout(); pdf.savefig(fig); plt.close(fig)
            except Exception: pass


def main() -> int:
    ap=argparse.ArgumentParser(description="Ocean Current Analyzer v3: phase, coherence, lag, rotary spectra and EOF")
    ap.add_argument("inputs",nargs="+",help="PANGAEA .tab files and/or folders")
    ap.add_argument("-o","--output",default="results_v3")
    ap.add_argument("--min-samples",type=int,default=240)
    ap.add_argument("--max-depth-series",type=int,default=60,help="maximum series per station for matrix analyses")
    ap.add_argument("--animation",action="store_true")
    ap.add_argument("--no-pdf",action="store_true")
    args=ap.parse_args()
    out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
    plotdir=out/"plots"; plotdir.mkdir(exist_ok=True)
    files=collect_files(args.inputs)
    if not files: print("No .tab files found",file=sys.stderr); return 2
    profiles=[]; rotary=[]; eofrows=[]; pairrows=[]; figures=[]; errors=[]
    for path in files:
        st=station_name(path); print(f"\n{st}: {path.name}")
        try:
            parsed=v2.read_pangaea_tab(path); ser=regular_series(parsed,args.min_samples)
            grid,names,depths,umat,vmat=common_grid(ser,max_series=args.max_depth_series)
            dt_h=(grid[1]-grid[0]).total_seconds()/3600
            print(f"  common series={len(names)}, samples={len(grid)}, dt={dt_h:g} h")
            prof,fig=m2_profiles(st,names,depths,grid,umat,vmat,plotdir); profiles.append(prof); figures+=fig
            coh,lag=pairwise_m2_metrics(depths,umat,vmat,dt_h)
            labels=[f"{d:.0f}m" for d in depths]
            figures.append(heatmap(coh,labels,f"{st} — M2-band vector coherence","coherence",plotdir/f"{safe_name(st)}_M2_coherence.png",0,1))
            figures.append(heatmap(lag,labels,f"{st} — M2-band lag (column lags row)","hours",plotdir/f"{safe_name(st)}_M2_lag_hours.png",-8,8))
            for i in range(len(names)):
                for j in range(i+1,len(names)):
                    pairrows.append(dict(station=st,series_a=names[i],depth_a_m=depths[i],series_b=names[j],depth_b_m=depths[j],m2_vector_coherence=coh[i,j],lag_b_relative_to_a_h=lag[i,j]))
            r,fig=rotary_spectrum(st,names,depths,umat,vmat,dt_h,plotdir); rotary.append(r); figures+=fig
            e,fig=eof_analysis(st,names,depths,umat,vmat,dt_h,plotdir); eofrows.append(e); figures+=fig
            if args.animation:
                gif=animation_m2(st,prof,plotdir)
                if gif: print(f"  animation: {gif.name}")
        except Exception as exc:
            print(f"  ERROR: {exc}",file=sys.stderr); errors.append(dict(file=path.name,station=st,error=str(exc),traceback=traceback.format_exc()))
    pd.concat(profiles,ignore_index=True).to_csv(out/"m2_depth_profiles.csv",index=False) if profiles else pd.DataFrame().to_csv(out/"m2_depth_profiles.csv",index=False)
    pd.DataFrame(pairrows).to_csv(out/"m2_pairwise_coherence_lag.csv",index=False)
    pd.concat(rotary,ignore_index=True).to_csv(out/"rotary_m2_summary.csv",index=False) if rotary else pd.DataFrame().to_csv(out/"rotary_m2_summary.csv",index=False)
    pd.concat(eofrows,ignore_index=True).to_csv(out/"eof_variance_summary.csv",index=False) if eofrows else pd.DataFrame().to_csv(out/"eof_variance_summary.csv",index=False)
    pd.DataFrame(errors).to_csv(out/"errors_v3.csv",index=False)
    if figures and not args.no_pdf: make_pdf(figures,out/"ocean_current_v3_report.pdf")
    print(f"\nFinished. Output: {out.resolve()} | stations={len(profiles)} | errors={len(errors)}")
    return 0 if profiles else 1

if __name__=="__main__":
    raise SystemExit(main())
