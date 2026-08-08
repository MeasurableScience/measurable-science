import pandas as pd
import numpy as np
import scipy.signal as signal
import os
import glob

# ==============================================================================
# --- Blind statistical threshold ---
# ==============================================================================
USE_STATISTICAL_THRESHOLD = True  # True = median + 2*MAD (objektivna statistika), False = procentil
MIN_ABSOLUTE_PLV = 0.30           # Apsolutni pod za PLV (stavi None ako ne želiš nikakvo ograničenje)
# ==============================================================================

def apply_preprocessing(sig, dt, mode='raw'):
    if mode == 'raw':
        return sig
    elif mode == 'diff':
        return np.gradient(sig, dt)
    elif mode == 'spectral_whitening':
        fft_sig = np.fft.rfft(sig)
        magnitude = np.abs(fft_sig)
        magnitude[magnitude == 0] = 1e-12
        whitened_fft = fft_sig / magnitude
        return np.fft.irfft(whitened_fft, n=len(sig))
    else:
        raise ValueError(f"Nepoznat preprocessing mod: {mode}")

def calculate_plv(sig1, sig2):
    analytic1 = signal.hilbert(sig1)
    analytic2 = signal.hilbert(sig2)
    phase_diff = np.angle(analytic1) - np.angle(analytic2)
    return np.abs(np.mean(np.exp(1j * phase_diff)))

def extract_channels_strict(df, prep_mode='raw'):
    dt = df['t_s'].diff().median()
    fs = 1.0 / dt
    
    mx, my, mz = df['mx'].values, df['my'].values, df['mz'].values
    
    p_mx = apply_preprocessing(mx, dt, prep_mode)
    p_my = apply_preprocessing(my, dt, prep_mode)
    p_mz = apply_preprocessing(mz, dt, prep_mode)
    
    raw_coords = np.column_stack([p_mx, p_my, p_mz])
    raw_centered = raw_coords - np.mean(raw_coords, axis=0)
    _, _, vh = np.linalg.svd(raw_centered, full_matrices=False)
    pca_comp = np.dot(raw_centered, vh[0])
    
    horiz_h = np.sqrt(p_mx**2 + p_my**2)
    total_mag = np.sqrt(p_mx**2 + p_my**2 + p_mz**2)
    
    channels = {
        'X': p_mx,
        'Y': p_my,
        'Z': p_mz,
        'Horiz_H': horiz_h,
        'Total_Mag': total_mag,
        'PCA_PC1': pca_comp
    }
    
    return channels, fs

def process_single_window_plv_only(channels_win, fs, frequencies, bandwidth=0.4):
    half_bw = bandwidth / 2.0
    plv_metrics = []
    
    for f in frequencies:
        lowcut, highcut = f - half_bw, f + half_bw
        if lowcut <= 0.1 or highcut >= (fs / 2.0):
            continue
            
        sos = signal.butter(4, [lowcut, highcut], btype='bandpass', fs=fs, output='sos')
        f_x = signal.sosfiltfilt(sos, channels_win['X'])
        f_y = signal.sosfiltfilt(sos, channels_win['Y'])
        f_z = signal.sosfiltfilt(sos, channels_win['Z'])
        f_h = signal.sosfiltfilt(sos, channels_win['Horiz_H'])
        f_m = signal.sosfiltfilt(sos, channels_win['Total_Mag'])
        f_p = signal.sosfiltfilt(sos, channels_win['PCA_PC1'])
        
        plv_pairs = [
            calculate_plv(f_x, f_y), calculate_plv(f_x, f_z), calculate_plv(f_y, f_z),
            calculate_plv(f_h, f_z), calculate_plv(f_m, f_p), calculate_plv(f_h, f_p)
        ]
        
        plv_metrics.append({'freq_Hz': round(f, 2), 'PLV': np.mean(plv_pairs)})
        
    return pd.DataFrame(plv_metrics)

def run_gross_scan_dataset_plv(df, dataset_name, prep_mode='raw', window_sec_list=[20, 30, 45, 60, 90, 120]):
    channels, fs = extract_channels_strict(df, prep_mode=prep_mode)
    n_samples = len(df)
    frequencies = np.arange(1.0, 10.1, 0.1)
    
    all_raw_votes = []
    
    for win_sec in window_sec_list:
        win_samples = int(win_sec * fs)
        n_windows = max(1, n_samples // win_samples)
        
        for w in range(n_windows):
            start_idx = w * win_samples
            end_idx = min((w + 1) * win_samples, n_samples)
            
            if (end_idx - start_idx) < int(fs * 4):
                continue
                
            win_channels = {k: v[start_idx:end_idx] for k, v in channels.items()}
            win_res = process_single_window_plv_only(win_channels, fs, frequencies)
            
            if win_res.empty:
                continue
                
            plv_values = win_res['PLV'].values
            
            # --- UBACIVANJE POTPUNO SLEPOG/STATISTIČKOG PRAGA ---
            if USE_STATISTICAL_THRESHOLD:
                med = np.median(plv_values)
                mad = np.median(np.abs(plv_values - med))
                # median + 2*MAD određuje prag sam na osnovu šuma u prozoru
                threshold = med + 2.0 * mad
            else:
                threshold = np.percentile(plv_values, 85)
            
            # Primena MIN_ABSOLUTE_PLV ako je definisan u konfiguraciji
            if MIN_ABSOLUTE_PLV is not None:
                final_threshold = max(threshold, MIN_ABSOLUTE_PLV)
            else:
                final_threshold = threshold
            
            valid_rows = win_res[win_res['PLV'] >= final_threshold]
            
            for _, row in valid_rows.iterrows():
                plv_val = row['PLV']
                score_val = float(plv_val * 10.0)
                
                all_raw_votes.append({
                    'dataset': dataset_name,
                    'prep_mode': prep_mode,
                    'window_sec': win_sec,
                    'window_id': w,
                    'frequency': round(row['freq_Hz'], 2),
                    'score': score_val,
                    'raw_plv_val': plv_val
                })
                    
    return pd.DataFrame(all_raw_votes)

def form_plv_clusters(df_votes, min_freq=1.0, max_freq=10.0, step=0.1):
    if df_votes.empty:
        return pd.DataFrame()

    all_freqs = np.round(np.arange(min_freq, max_freq + step, step), 2)
    freq_scores = df_votes.groupby('frequency')['score'].sum().reindex(all_freqs, fill_value=0).reset_index()
    scores = freq_scores['score'].values
    
    if np.all(scores == 0):
        return pd.DataFrame()
        
    med = np.median(scores)
    mad = np.median(np.abs(scores - med))
    dyn_threshold = max(8.0, med + 1.5 * mad)
    
    smoothed_scores = signal.savgol_filter(scores, window_length=5, polyorder=2) if len(scores) >= 5 else scores
    active_mask = smoothed_scores >= dyn_threshold
    active_freqs = freq_scores['frequency'].values[active_mask]
    
    if len(active_freqs) == 0:
        return pd.DataFrame()
        
    raw_clusters = []
    current_cluster = [active_freqs[0]]
    
    for f in active_freqs[1:]:
        if round(f - current_cluster[-1], 2) <= 0.15:
            current_cluster.append(f)
        else:
            raw_clusters.append(current_cluster)
            current_cluster = [f]
    raw_clusters.append(current_cluster)
    
    cluster_summary = []
    for cl in raw_clusters:
        if not cl:
            continue
        f_start, f_end = cl[0], cl[-1]
        width = round(f_end - f_start, 2)
        
        cl_sub = freq_scores[(freq_scores['frequency'] >= f_start) & (freq_scores['frequency'] <= f_end)]
        total_plv_score = cl_sub['score'].sum()
        peak_row = cl_sub.loc[cl_sub['score'].idxmax()]
        
        p_idx = np.where(all_freqs == peak_row['frequency'])[0][0]
        p_val = scores[p_idx]
        left_min = np.min(scores[max(0, p_idx-4):p_idx]) if p_idx > 0 else 0
        right_min = np.min(scores[p_idx+1:min(len(scores), p_idx+5)]) if p_idx < len(scores)-1 else 0
        local_prominence = p_val - max(left_min, right_min)
        
        sub_votes = df_votes[(df_votes['frequency'] >= f_start) & (df_votes['frequency'] <= f_end)]
        avg_raw_plv = sub_votes['raw_plv_val'].mean() if 'raw_plv_val' in sub_votes.columns else 0.0
        wins_breakdown = sub_votes.groupby('window_sec')['score'].sum().to_dict()
        
        c_type = "Sharp Carrier Peak" if local_prominence >= 35 else "Phase Coherent Band"
        
        cluster_summary.append({
            'Cluster_Range_Hz': f"{f_start:.1f} - {f_end:.1f}",
            'Cluster_Width_Hz': width,
            'Peak_Freq_Hz': round(peak_row['frequency'], 2),
            'PLV_Peak_Score': peak_row['score'],
            'Prominence': round(local_prominence, 1),
            'Mean_Raw_PLV': round(avg_raw_plv, 3),
            'Cluster_Type': c_type,
            'Integrated_PLV_Score': total_plv_score,
            'Active_Windows_Count': len(wins_breakdown)
        })
        
    res_df = pd.DataFrame(cluster_summary)
    if res_df.empty:
        return res_df
    return res_df.sort_values(by='Integrated_PLV_Score', ascending=False).reset_index(drop=True)

if __name__ == '__main__':
    csv_files = glob.glob("*.csv")
    input_files = [f for f in csv_files if not f.startswith('audit_log') and not 'clusters' in f and not 'BENCHMARK' in f]
    
    print(f"Pronađeno {len(input_files)} CSV snimaka za ČISTU PLV ANALIZU: {input_files}\n")
    
    all_site_results = []
    
    for csv_file in sorted(input_files):
        site_name = os.path.basename(csv_file).replace('.csv', '')
        print(f"====================================================")
        print(f"PLV ANALIZA FAZNIH NOSILACA: {site_name}")
        print(f"====================================================")
        
        try:
            df = pd.read_csv(csv_file, comment='#')
            
            for prep in ['raw', 'diff', 'spectral_whitening']:
                print(f" -> Pokrećem PLV Scan (1–10 Hz) [Mod: {prep.upper()}]...")
                df_votes = run_gross_scan_dataset_plv(df, dataset_name=site_name, prep_mode=prep)
                
                clusters = form_plv_clusters(df_votes, min_freq=1.0, max_freq=10.0)
                if not clusters.empty:
                    clusters['Site'] = site_name
                    clusters['Prep_Mode'] = prep
                    all_site_results.append(clusters)
                    
                    print(f"\n--- TOP FAZNI NOSILCI (PLV) ZA [{site_name}] (Mod: {prep}) ---")
                    print(clusters.head(5)[['Cluster_Range_Hz', 'Peak_Freq_Hz', 'Cluster_Width_Hz', 'Prominence', 'Mean_Raw_PLV', 'Integrated_PLV_Score']].to_string(index=False))
                    print("-" * 65)
                else:
                    print(f"    -> Nema fazno sinhronizovanih klastera za mod {prep}.")
        except Exception as e:
            print(f"[GREŠKA] Problem pri obradi {csv_file}: {e}")
            
    if all_site_results:
        final_summary = pd.concat(all_site_results, ignore_index=True)
        final_summary.to_csv('PLV_CARRIERS_ALL_SITES.csv', index=False)
        print("\n====================================================")
        print("[USPEH] PLV Obrada je završena!")
        print("Rezultati faznih nosilaca sačuvani u 'PLV_CARRIERS_ALL_SITES.csv'")
        print("====================================================")