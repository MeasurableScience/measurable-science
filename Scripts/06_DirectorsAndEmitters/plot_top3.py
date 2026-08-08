import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ==========================================
# KONFIGURACIJA I PALETE BOJA (Lako podešavanje)
# ==========================================
CONFIG = {
    'input_file': "ALL_SITES_TOP3_ENERGY_SUMMARY.csv",
    'output_image': "ADVANCED_TOP3_COMPARISON_REPORT.png",
    'style': "whitegrid",
    'palette_ranks': {
        'Rank 1': '#2b5c8f',  # Plava za Rank 1
        'Rank 2': '#d95f02',  # Narandžasta za Rank 2
        'Rank 3': '#7570b3'   # Ljubičasta za Rank 3
    },
    'font_family': 'sans-serif'
}

def plot_advanced_top3_report():
    if not os.path.exists(CONFIG['input_file']):
        print(f"[X] Greška: Fajl '{CONFIG['input_file']}' ne postoji.")
        return

    # Učitavanje podataka
    df = pd.read_csv(CONFIG['input_file'])
    if df.empty:
        print("[X] Upozorenje: CSV fajl je prazan.")
        return

    # Postavljanje stila
    sns.set_theme(style=CONFIG['style'])
    plt.rcParams.update({
        'font.family': CONFIG['font_family'],
        'axes.edgecolor': '#cccccc',
        'axes.linewidth': 1.0
    })

    # 1. SORTIRANJE LOKACIJA PO MAKSIMALNOJ ENERGIJI (Najjače lokacije prve)
    sorted_sites = (
        df.groupby("Site")["Integrated_Energy"]
          .max()
          .sort_values(ascending=False)
          .index.tolist()
    )
    df['Site'] = pd.Categorical(df['Site'], categories=sorted_sites, ordered=True)
    df = df.sort_values(by=['Site', 'Integrated_Energy'], ascending=[True, False]).reset_index(drop=True)

    # Dodajemo rang unutar svake lokacije (1, 2, 3) i string oznake za hue
    df['Rank'] = df.groupby('Site').cumcount() + 1
    df['Rank_Label'] = 'Rank ' + df['Rank'].astype(str)

    # Izračunavanje procenata Z-osi energije (Z_Axis_Energy / Integrated_Energy * 100)
    if 'Z_Axis_Energy' in df.columns and 'Integrated_Energy' in df.columns:
        df['Z_Pct'] = (df['Z_Axis_Energy'] / df['Integrated_Energy']) * 100
    else:
        df['Z_Pct'] = 0.0

    # 2. IZRAČUNAVANJE NORMALIZOVANE ENERIJE (Rank 1 = 100% po lokaciji)
    max_energy_per_site = df.groupby('Site')['Integrated_Energy'].transform('max')
    df['Normalized_Energy'] = (df['Integrated_Energy'] / max_energy_per_site) * 100

    # Kreiramo figuru sa 3 potprozora (subplot-a)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 16))

    # --- PANEL 1: Apsolutna Integrisana Energija ---
    sns.barplot(
        data=df, 
        x='Site', 
        y='Integrated_Energy', 
        hue='Rank_Label', 
        ax=ax1, 
        palette=CONFIG['palette_ranks'],
        edgecolor='none',
        alpha=0.9
    )
    ax1.set_title("A. Uporedni prikaz Top 3 Integrisane Energije po Lokacijama", fontsize=13, fontweight='bold', pad=15)
    ax1.set_xlabel("")
    ax1.set_ylabel("Integrisana Energija [3D]", fontsize=10, fontweight='bold')
    ax1.tick_params(axis='x', rotation=15)
    ax1.legend(title='Pozicija', frameon=True, facecolor='white', framealpha=0.9, loc='upper right')
    ax1.grid(True, linestyle='--', alpha=0.5, axis='y')

    # --- PANEL 2: Normalizovana Energija (Dominacija kanala u %) ---
    sns.barplot(
        data=df, 
        x='Site', 
        y='Normalized_Energy', 
        hue='Rank_Label', 
        ax=ax2, 
        palette=CONFIG['palette_ranks'],
        edgecolor='none',
        alpha=0.9
    )
    ax2.set_title("B. Relativna dominacija kanala (Rank 1 = 100%)", fontsize=13, fontweight='bold', pad=15)
    ax2.set_xlabel("")
    ax2.set_ylabel("Udeo u energiji [%]", fontsize=10, fontweight='bold')
    ax2.set_ylim(0, 105)
    ax2.tick_params(axis='x', rotation=15)
    ax2.legend().set_visible(False)
    ax2.grid(True, linestyle='--', alpha=0.5, axis='y')

    # --- PANEL 3: Frekventni opsezi i Pik frekvencije ---
    y_ticks_positions = []
    y_ticks_labels = []
    y_offset = 0
    site_spacing = 1.5

    for site in sorted_sites:
        site_data = df[df['Site'] == site].sort_values(by='Rank')
        for _, row in site_data.iterrows():
            flow = row['Flow']
            fhigh = row['Fhigh']
            rank = row['Rank']
            rank_key = f"Rank {rank}"
            peak_hz = row.get('Peak_Center_Hz', (flow + fhigh) / 2)
            color = CONFIG['palette_ranks'].get(rank_key, '#333333')
            
            # Crtamo horizontalnu traku za frekventni opseg
            ax3.barh(y_offset, width=(fhigh - flow), left=flow, height=0.45, 
                     color=color, alpha=0.85, edgecolor='black', linewidth=0.5)
            
            # Tekst sa opsegom i pik frekvencijom
            mid_freq = flow + (fhigh - flow) / 2
            label_text = f"R{rank}: {row['Range']} ({peak_hz:.1f} Hz)"
            ax3.text(mid_freq, y_offset, label_text, 
                     va='center', ha='center', fontsize=8, color='white', fontweight='bold')

            y_ticks_positions.append(y_offset)
            y_ticks_labels.append(f"{site} (R{rank})")
            y_offset += 0.6
        y_offset += site_spacing

    ax3.set_title("C. Frekventni opsezi i centralne pik frekvencije Top 3 signala", fontsize=13, fontweight='bold', pad=15)
    ax3.set_xlabel("Frekvencija [Hz]", fontsize=10, fontweight='bold')
    ax3.set_ylabel("Lokacija & Rang", fontsize=10, fontweight='bold')
    ax3.set_yticks(y_ticks_positions)
    ax3.set_yticklabels(y_ticks_labels, fontsize=9)
    ax3.grid(True, linestyle='--', alpha=0.5, axis='x')

    # Završno doterivanje izgleda
    plt.tight_layout()
    plt.savefig(CONFIG['output_image'], dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n[✓] Uspešno generisan napredni izveštaj sa 3 panela: '{CONFIG['output_image']}'")

if __name__ == "__main__":
    plot_advanced_top3_report()