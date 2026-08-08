import numpy as np
import pandas as pd
import scipy.signal as signal
import scipy.integrate as integrate
import os
import glob

def bandpass_filter_exact(data, flow, fhigh, fs):
    """Applies a 4th-order zero-phase Butterworth bandpass filter."""
    lowcut = max(0.05, flow)
    highcut = min(fs / 2.0 - 0.05, fhigh)
    
    if lowcut >= highcut:
        return np.zeros_like(data)
        
    sos = signal.butter(4, [lowcut, highcut], btype='bandpass', fs=fs, output='sos')
    return signal.sosfiltfilt(sos, data)

def remove_overlapping_bands(df, overlap_threshold=0.75):
    """Intelligent deduplication: Removes redundant overlapping bands."""
    if df.empty:
        return df
        
    df = df.sort_values(by='Integrated_Energy', ascending=False).reset_index(drop=True)
    keep = []
    
    for i, row_i in df.iterrows():
        flow_i, fhigh_i = row_i['Flow'], row_i['Fhigh']
        width_i = fhigh_i - flow_i
        
        is_redundant = False
        for k in keep:
            flow_k, fhigh_k = df.loc[k, ['Flow', 'Fhigh']]
            width_k = fhigh_k - flow_k
            
            inter_low = max(flow_i, flow_k)
            inter_high = min(fhigh_i, fhigh_k)
            
            if inter_low < inter_high:
                inter_width = inter_high - inter_low
                min_width = min(width_i, width_k)
                if min_width > 0 and (inter_width / min_width) >= overlap_threshold:
                    is_redundant = True
                    break
                    
        if not is_redundant:
            keep.append(i)
            
    return df.loc[keep].reset_index(drop=True)

def process_all_sites_single_csv_only():
    print("\n" + "=" * 115)
    print(" AUTOMATED BATCH ANALYSIS: TOP 3 ENERGY BANDS -> SINGLE CSV (NO PLOTS) ")
    print("=" * 115)

    plv_csv_path = "PLV_CARRIERS_ALL_SITES.csv"
    if not os.path.exists(plv_csv_path):
        print(f"[X] Greška: PLV fajl '{plv_csv_path}' ne postoji u trenutnom folderu.")
        return

    plv_df = pd.read_csv(plv_csv_path)
    plv_df.columns = [c.strip() for c in plv_df.columns]

    if 'Site' not in plv_df.columns:
        print("[X] Greška: Kolona 'Site' nije pronađena u PLV tabeli.")
        return

    unique_sites = plv_df['Site'].dropna().unique()
    print(f"\n[✓] Pronađeno {len(unique_sites)} lokacija u PLV tabeli: {list(unique_sites)}")

    all_top3_records = []

    for site_keyword in unique_sites:
        site_keyword_lower = str(site_keyword).strip().lower()
        print(f"\n" + "-" * 115)
        print(f" Obrada lokacije: [{site_keyword.upper()}]")
        print("-" * 115)

        site_rows = plv_df[plv_df['Site'].astype(str).str.lower() == site_keyword_lower].copy()
        if site_rows.empty:
            print(f" [!] Nema redova za lokaciju {site_keyword}.")
            continue

        all_csvs = glob.glob("*.csv")
        matching_csvs = [f for f in all_csvs if site_keyword_lower in f.lower() and f.lower() != 'plv_carriers_all_sites.csv' and not f.lower().endswith('_energy.csv') and not f.lower().endswith('_report.png')]

        if not matching_csvs:
            print(f" [X] Nije pronađen nijedan sirovi CSV fajl za lokaciju '{site_keyword}'. Preskačem.")
            continue
        
        raw_csv_path = matching_csvs[0]
        print(f" [✓] Pronađen sirovi CSV fajl: '{raw_csv_path}'")

        try:
            raw_df = pd.read_csv(raw_csv_path, comment='#')
            raw_df.columns = [c.strip() for c in raw_df.columns]

            if not all(col in raw_df.columns for col in ['t_s', 'mx', 'my', 'mz']):
                print(f" [X] Fajl {raw_csv_path} nema obavezne kolone. Preskačem.")
                continue

            t = raw_df['t_s'].values.astype(float)
            dt = np.median(np.diff(t))
            fs = 1.0 / dt if dt > 0 else 200.0

            mx = raw_df['mx'].values.astype(float)
            my = raw_df['my'].values.astype(float)
            mz = raw_df['mz'].values.astype(float)

            nperseg_val = int(fs * 64)
            if nperseg_val > len(mx):
                nperseg_val = max(512, len(mx) // 2)

            f_psd, pxx_x = signal.welch(mx, fs=fs, nperseg=nperseg_val, noverlap=nperseg_val // 2)
            _, pxx_y = signal.welch(my, fs=fs, nperseg=nperseg_val, noverlap=nperseg_val // 2)
            _, pxx_z = signal.welch(mz, fs=fs, nperseg=nperseg_val, noverlap=nperseg_val // 2)
            pxx_xyz = pxx_x + pxx_y + pxx_z

            results = []
            for idx, row in site_rows.iterrows():
                try:
                    fr_str = str(row['Cluster_Range_Hz']).strip()
                    flow, fhigh = [float(x.strip()) for x in fr_str.split('-')]
                    f_center = float(row['Peak_Freq_Hz'])
                    proc_mode = str(row['Prep_Mode'])
                    z_node_val = float(row.get('Z_Node_Pct', row.get('z_node_pct', 0.0)))
                except Exception:
                    continue

                x_f = bandpass_filter_exact(mx, flow, fhigh, fs)
                y_f = bandpass_filter_exact(my, flow, fhigh, fs)
                z_f = bandpass_filter_exact(mz, flow, fhigh, fs)

                inst_power_3d = x_f**2 + y_f**2 + z_f**2
                e_cum_3d = np.sum(inst_power_3d) * dt
                e_cum_z = np.sum(z_f**2) * dt
                rate_3d = e_cum_3d / (t[-1] - t[0])

                hx = signal.hilbert(x_f)
                hy = signal.hilbert(y_f)
                hz = signal.hilbert(z_f)
                vector_env = np.sqrt(np.abs(hx)**2 + np.abs(hy)**2 + np.abs(hz)**2)

                mask_band = (f_psd >= flow) & (f_psd <= fhigh)
                if np.sum(mask_band) > 1:
                    psd_band_power = integrate.trapezoid(pxx_xyz[mask_band], f_psd[mask_band])
                elif np.sum(mask_band) == 1:
                    df_freq = f_psd[1] - f_psd[0] if len(f_psd) > 1 else 1.0
                    psd_band_power = pxx_xyz[mask_band][0] * df_freq
                else:
                    nearest_idx = np.argmin(np.abs(f_psd - f_center))
                    df_freq = f_psd[1] - f_psd[0] if len(f_psd) > 1 else 1.0
                    psd_band_power = pxx_xyz[nearest_idx] * df_freq

                results.append({
                    'Site': site_keyword,
                    'Raw_File': raw_csv_path,
                    'Range': f"{flow:.1f} - {fhigh:.1f} Hz",
                    'Flow': flow,
                    'Fhigh': fhigh,
                    'Peak_Center_Hz': f_center,
                    'Prep_Mode': proc_mode,
                    'Z_Node_PLV': z_node_val,
                    'Integrated_Energy': e_cum_3d,
                    'PSD_Band_Power': psd_band_power,
                    'Z_Axis_Energy': e_cum_z,
                    'Peak_Envelope': np.max(vector_env),
                    'Mean_Envelope': np.mean(vector_env),
                    'Energy_Rate': rate_3d
                })

            if not results:
                continue

            res_df = pd.DataFrame(results)
            res_df = res_df.drop_duplicates(subset=['Range'])
            res_df = remove_overlapping_bands(res_df, overlap_threshold=0.75)

            res_df = res_df.sort_values(by='Integrated_Energy', ascending=False).reset_index(drop=True)
            top3_df = res_df.head(3).copy()

            all_top3_records.append(top3_df)
            print(f" [✓] Uspešno izdvojeno top 3 za lokaciju '{site_keyword}'.")

        except Exception as e:
            print(f" [X] Greška pri obradi lokacije {site_keyword}: {e}")

    # Snimanje svih top 3 rezultata u JEDAN zajednički CSV fajl
    if all_top3_records:
        master_top3_df = pd.concat(all_top3_records, ignore_index=True)
        master_filename = "ALL_SITES_TOP3_ENERGY_SUMMARY.csv"
        master_top3_df.to_csv(master_filename, index=False)
        print(f"\n[✓] Uspešno kreiran jedinstveni fajl: '{master_filename}'")

    print("\n" + "=" * 115)
    print(" [USPEH] Obrada završena, CSV fajl je spreman!")
    print("=" * 115)

if __name__ == "__main__":
    process_all_sites_single_csv_only()