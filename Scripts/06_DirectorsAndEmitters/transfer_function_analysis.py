import numpy as np
import pandas as pd
import scipy.signal as signal
import os
import glob

def compute_hilbert_envelope(signal_data):
    """Računa analitičku kovertu signala preko Hilbertove transformacije."""
    analytic_signal = signal.hilbert(signal_data)
    return np.abs(analytic_signal)

def run_transfer_function_analysis():
    print("\n" + "=" * 115)
    print(" TRANSFER FUNCTION H(f) ANALYSIS: EMITER vs SHUMAN vs SITES ")
    print("=" * 115)

    summary_csv = "ALL_SITES_TOP3_ENERGY_SUMMARY.csv"
    if not os.path.exists(summary_csv):
        print(f"[X] Greška: Fajl '{summary_csv}' ne postoji. Prvo pokreni prethodnu skriptu da generišeš top 3 zapise.")
        return

    df_top3 = pd.read_csv(summary_csv)
    df_top3.columns = [c.strip() for c in df_top3.columns]

    if 'Site' not in df_top3.columns or 'Raw_File' not in df_top3.columns:
        print("[X] Greška: Nedostaju ključne kolone u sumarnom CSV fajlu.")
        return

    transfer_results = []
    unique_sites = df_top3['Site'].unique()
    print(f"\n[✓] Analiziram transfer funkcije za lokacije: {list(unique_sites)}")

    for site in unique_sites:
        site_rows = df_top3[df_top3['Site'] == site]
        raw_file = site_rows['Raw_File'].iloc[0]

        if not os.path.exists(raw_file):
            print(f" [!] Sirovi fajl {raw_file} nije pronađen za lokaciju {site}. Preskačem.")
            continue

        print(f"\n--- Obrada lokacije: [{site.upper()}] iz fajla {raw_file} ---")
        
        try:
            raw_df = pd.read_csv(raw_file, comment='#')
            raw_df.columns = [c.strip() for c in raw_df.columns]
            
            t = raw_df['t_s'].values.astype(float)
            dt = np.median(np.diff(t))
            fs = 1.0 / dt if dt > 0 else 200.0

            # Uzmemo z-komponentu kao meru signala na lokaciji
            signal_data = raw_df['mz'].values.astype(float)

            # Simulacija / Definisanje referentnog emitera / Šumana (bazirano na frekvencijama opsega)
            np.random.seed(42)
            t_ref = t
            shuman_ref = np.sin(2 * np.pi * 7.83 * t_ref) + 0.5 * np.sin(2 * np.pi * 14.3 * t_ref) + 0.1 * np.random.randn(len(t_ref))

            for idx, row in site_rows.iterrows():
                flow = float(row['Flow'])
                fhigh = float(row['Fhigh'])
                band_name = row['Range']

                # Bandpass filter signala na lokaciji
                lowcut = max(0.05, flow)
                highcut = min(fs / 2.0 - 0.05, fhigh)
                if lowcut >= highcut:
                    continue
                
                sos = signal.butter(4, [lowcut, highcut], btype='bandpass', fs=fs, output='sos')
                filtered_site = signal.sosfiltfilt(sos, signal_data)
                filtered_shuman = signal.sosfiltfilt(sos, shuman_ref)

                # Izračunavanje koverti (Envelope)
                env_site = compute_hilbert_envelope(filtered_site)
                env_shuman = compute_hilbert_envelope(filtered_shuman)

                # Izračunavanje Transfer Funkcije H(f) preko odnosa koverti
                env_shuman_safe = np.where(env_shuman == 0, 1e-6, env_shuman)
                h_f_vector = env_shuman_safe / (env_site + 1e-6)
                mean_hf = np.mean(h_f_vector)
                std_hf = np.std(h_f_vector)

                transfer_results.append({
                    'Site': site,
                    'Band': band_name,
                    'Mean_H_F': mean_hf,
                    'Std_H_F': std_hf,
                    'Env_Site_Mean': np.mean(env_site),
                    'Env_Shuman_Mean': np.mean(env_shuman)
                })

        except Exception as e:
            print(f" [X] Greška pri obradi lokacije {site}: {e}")

    if transfer_results:
        df_hf = pd.DataFrame(transfer_results)
        output_hf_file = "TRANSFER_FUNCTION_H_RESULTS.csv"
        df_hf.to_csv(output_hf_file, index=False)
        
        print("\n" + "=" * 115)
        print(f" [✓] ANALIZA ZAVRŠENA! Rezultati upisani u: '{output_hf_file}'")
        print("=" * 115)
        print(df_hf.to_string(index=False))
        print("=" * 115)
    else:
        print("[X] Nema rezultata za upis transfer funkcije.")

if __name__ == "__main__":
    run_transfer_function_analysis()