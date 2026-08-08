import numpy as np
import pandas as pd
import scipy.signal as signal
import os

# ==============================================================================
# CONFIGURATION / KONFIGURACIJA
# ==============================================================================
CSV_FILE = "kapadokia-restoran_normalized.csv"
TARGET_FREQ = 1.6      # Centralna frekvencija za pretragu (Hz)
BANDWIDTH = 0.25       # Širina bandpass filtera (Hz)
SEARCH_WINDOW = 0.3    # Prozor za detekciju tačnog pika (+/- Hz)

# Parametri za klizni prozor
WIN_SEC = 4.0          # Dužina kliznog prozora u sekundama
OVERLAP = 0.75         # Preklapanje prozora (75%)

# ==============================================================================
# FUNCTIONS / FUNKCIJE
# ==============================================================================
def load_data(filepath):
    """ Učitava CSV fajl, uklanja duplikate u vremenu i računa sampling rate. """
    df = pd.read_csv(filepath, comment='#').drop_duplicates(subset=['t_s']).sort_values('t_s').reset_index(drop=True)
    t = df['t_s'].values - df['t_s'].values[0]
    sr = 1.0 / np.mean(np.diff(t)[np.diff(t) > 0])
    return sr, t, df['mx'].values.astype(np.float64), df['my'].values.astype(np.float64), df['mz'].values.astype(np.float64)

def refined_carrier_analysis(filepath, target_freq=7.8, bw=0.25, win_sec=4.0, overlap=0.75):
    sr, t, mx, my, mz = load_data(filepath)
    
    # --- 1. PRECIZNO PRONALAŽENJE PIKA (AUTO-PEAK REFINEMENT) ---
    freqs, psd_z = signal.welch(mz, fs=sr, nperseg=int(sr*10))
    idx_search = np.where((freqs >= target_freq - SEARCH_WINDOW) & (freqs <= target_freq + SEARCH_WINDOW))[0]
    
    if len(idx_search) > 0:
        exact_peak_freq = freqs[idx_search[np.argmax(psd_z[idx_search])]]
    else:
        exact_peak_freq = target_freq
        
    # --- 2. FILTRIRANJE NA TAČNOJ FREKVENCIJI ---
    lowcut = max(0.1, exact_peak_freq - bw/2.0)
    highcut = min(sr/2.0 - 0.1, exact_peak_freq + bw/2.0)
    
    sos = signal.butter(4, [lowcut, highcut], btype='bandpass', fs=sr, output='sos')
    fx = signal.sosfiltfilt(sos, mx)
    fy = signal.sosfiltfilt(sos, my)
    fz = signal.sosfiltfilt(sos, mz)
    
    # --- 3. HILBERTOVA TRANSFORMACIJA I OMOTNICE ---
    hx, hy, hz = signal.hilbert(fx), signal.hilbert(fy), signal.hilbert(fz)
    env_x, env_y, env_z = np.abs(hx), np.abs(hy), np.abs(hz)
    env_total = np.sqrt(env_x**2 + env_y**2 + env_z**2)
    
    # --- 4. FAZE I SPEKTRALNA MATRICA KOVARIJANSE (GLOBALNA 3D POLARIZACIJA) ---
    phase_x, phase_y, phase_z = np.unwrap(np.angle(hx)), np.unwrap(np.angle(hy)), np.unwrap(np.angle(hz))
    
    dphi_xy = np.angle(np.mean(np.exp(1j * (phase_x - phase_y))))
    dphi_xz = np.angle(np.mean(np.exp(1j * (phase_x - phase_z))))
    dphi_yz = np.angle(np.mean(np.exp(1j * (phase_y - phase_z))))
    
    # Kompleksna matrica kovarijanse za 3D polarizaciju
    Z = np.vstack([hx, hy, hz])
    J = np.dot(Z, Z.conj().T) / Z.shape[1] # Polarizaciona matrica 3x3
    
    tr_J = np.trace(J).real
    deg_pol = np.sqrt(1.5 * (np.trace(np.dot(J, J)).real / (tr_J**2) - 1/3)) * 100
    
    # --- 5. GEOMETRIJSKA DEKOMPOZICIJA (EIGEN ANALYSIS) ---
    real_traj = np.vstack([fx, fy, fz])
    cov_m = np.cov(real_traj)
    e_val, e_vec = np.linalg.eigh(cov_m)
    idx = np.argsort(e_val)[::-1]
    l1, l2, l3 = e_val[idx]
    
    # Pravac glavne ose oscilovanja
    main_axis = e_vec[:, idx[0]]
    azimuth = np.degrees(np.arctan2(main_axis[1], main_axis[0]))
    elevation = np.degrees(np.arctan2(main_axis[2], np.sqrt(main_axis[0]**2 + main_axis[1]**2)))
    
    pow_x, pow_y, pow_z = np.mean(env_x**2), np.mean(env_y**2), np.mean(env_z**2)
    tot_pow = pow_x + pow_y + pow_z

    # --- 6. ANALIZA U KLIZNOM PROZORU ---
    win_samples = int(win_sec * sr)
    step_samples = int(win_samples * (1 - overlap))
    num_windows = max(1, (len(fx) - win_samples) // step_samples + 1)

    win_dphi_xy = []
    win_azimuths = []
    win_env = []

    for i in range(num_windows):
        i_start = i * step_samples
        i_end = i_start + win_samples
        if i_end > len(fx): break

        wx, wy, wz = hx[i_start:i_end], hy[i_start:i_end], hz[i_start:i_end]
        
        # Prosečna omotnica u prozoru
        win_env.append(np.mean(env_total[i_start:i_end]))

        # Faza u prozoru
        dphi_w = np.angle(np.mean(wx * np.conj(wy)))
        win_dphi_xy.append(np.degrees(dphi_w))

        # Azimut u prozoru
        cov_w = np.cov(np.vstack([fx[i_start:i_end], fy[i_start:i_end], fz[i_start:i_end]]))
        w_val, w_vec = np.linalg.eigh(cov_w)
        v_max = w_vec[:, np.argmax(w_val)]
        win_azimuths.append(np.degrees(np.arctan2(v_max[1], v_max[0])))

    win_env = np.array(win_env)
    win_dphi_xy = np.array(win_dphi_xy)
    win_azimuths = np.array(win_azimuths)

    std_dphi = np.std(win_dphi_xy) if len(win_dphi_xy) > 1 else 0.0
    std_az = np.std(win_azimuths) if len(win_azimuths) > 1 else 0.0

    # --- 7. TEST KOHERENCIJE (EKSPERIMENTALNI TEST HIPOTEZE O PAKETIMA) ---
    threshold_high = np.percentile(win_env, 75)  # Top 25% po energiji
    idx_high = np.where(win_env >= threshold_high)[0]
    idx_low = np.where(win_env < threshold_high)[0]

    std_dphi_high = np.std(win_dphi_xy[idx_high]) if len(idx_high) > 1 else 0.0
    std_dphi_low = np.std(win_dphi_xy[idx_low]) if len(idx_low) > 1 else 0.0

    std_az_high = np.std(win_azimuths[idx_high]) if len(idx_high) > 1 else 0.0
    std_az_low = np.std(win_azimuths[idx_low]) if len(idx_low) > 1 else 0.0

    mean_dphi_high = np.degrees(np.angle(np.mean(np.exp(1j * np.radians(win_dphi_xy[idx_high]))))) if len(idx_high) > 0 else 0.0

    # --- ISPIS REZULTATA ---
    print("=================================================================")
    print(f" PROFIL OBLIKA I FAZE (PRECIZISAN NA: {exact_peak_freq:.3f} Hz)")
    print("=================================================================")
    print(f"Fajl: {os.path.basename(filepath)} | Filter: {lowcut:.2f} - {highcut:.2f} Hz\n")
    
    print("--- 1. AMFLITUDA I OMOTNICA ---")
    print(f"Prosečna ukupna omotnica : {np.mean(env_total):.6f}")
    print(f"Udeo X / Y / Z   : {(pow_x/tot_pow)*100:.1f}% / {(pow_y/tot_pow)*100:.1f}% / {(pow_z/tot_pow)*100:.1f}%\n")
    
    print("--- 2. MEĐUFAZNE RELACIJE I 3D POLARIZACIJA (GLOBALNO) ---")
    print(f"Fazna razlika XY (Δφ_xy) : {dphi_xy:.4f} rad  ({np.degrees(dphi_xy):.1f}°)")
    print(f"Fazna razlika XZ (Δφ_xz) : {dphi_xz:.4f} rad  ({np.degrees(dphi_xz):.1f}°)")
    print(f"Fazna razlika YZ (Δφ_yz) : {dphi_yz:.4f} rad  ({np.degrees(dphi_yz):.1f}°)")
    print(f"Stepen 3D Polarizacije  : {deg_pol:.1f}%  (Visoke vrednosti = čist talas)\n")
    
    print("--- 3. GLAVNA OSA OSCILOVANJA ---")
    print(f"Azimut glavne ose       : {azimuth:.1f}°")
    print(f"Elevacija (Nagib)       : {elevation:.1f}°")
    print(f"Odnos osa (Elipsoid)    : Axis1=1.00, Axis2={l2/l1:.2f}, Axis3={l3/l1:.2f}\n")

    print("--- 4. DINAMIKA U KLIZNOM PROZORU ---")
    print(f"Broj analiziranih prozora : {len(win_dphi_xy)} (Dužina prozora: {win_sec}s)")
    print(f"Ukupno variranje Faze (Std Δφ_xy) : ±{std_dphi:.1f}°")
    print(f"Ukupno variranje Azimuta (Std Az) : ±{std_az:.1f}°\n")

    print("--- 5. TEST KOHERENCIJE (PROVERA HIPOTEZE O PAKETIMA) ---")
    print(f"Prag visoke energije (Top 25% RMS) : > {threshold_high:.6f}")
    print(f"Varijacija faze u VISOKOJ energiji : ±{std_dphi_high:.1f}°  (naspram NISKOJ: ±{std_dphi_low:.1f}°)")
    print(f"Varijacija azimuta u VISOKOJ energiji: ±{std_az_high:.1f}°  (naspram NISKOJ: ±{std_az_low:.1f}°)")
    print(f"Stabilizovana faza pri pikovima  : {mean_dphi_high:.1f}°")
    
    print("\nINTERPRETACIJA TESTA:")
    if std_dphi_high < std_dphi_low / 1.8:
        print(" -> Hipoteza POTVRĐENA: Faza se drastično stabilizuje pri skoku energije.")
        print("    Postoji dokaz o prisustvu koherentnog prolaznog događaja (paketa).")
    elif std_dphi_high < std_dphi_low:
        print(" -> Delimična stabilizacija: Faza jeste stabilnija pri većoj energiji, ali i dalje prisutna umerena varijacija.")
    else:
        print(" -> Hipoteza NIJE potvrđena: Nestabilnost faze je prisutna i pri visokoj energiji.")
        print("    Uzrok mogu biti superpozicija više modova, varijacije izvora ili šum.")
    print("=================================================================")

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
if __name__ == "__main__":
    refined_carrier_analysis(
        filepath=CSV_FILE, 
        target_freq=TARGET_FREQ, 
        bw=BANDWIDTH, 
        win_sec=WIN_SEC, 
        overlap=OVERLAP
    )