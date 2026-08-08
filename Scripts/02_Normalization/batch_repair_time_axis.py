#!/usr/bin/env python3
"""
Project: Measurable Science
Script : batch_repair_time_axis.py

Purpose:
Automatski prolazi kroz sve CSV fajlove u folderu, rekonstruiše pristine,
perfektno uniformnu 200 Hz vremensku osu (t_s = np.arange(N) / 200.0) 
za hardverske uređaje zaključane na fiksnu frekvenciju (npr. WT901C / RM3100).
Čuva sirove merne podatke 100% netaknutim (1:1 očuvanje) bez ikakve interpolacije.
"""

import os
import numpy as np
import pandas as pd
from pathlib import Path

def batch_repair_time_axes():
    print("\n" + "=" * 90)
    print(" BATCH TIME AXIS REPAIR (FIXED 200 Hz HARDWARE RATE) - AUTOMATSKA OBRADA FOLDERA ")
    print("=" * 90)

    # Koristimo trenutni radni direktorijum
    current_dir = Path.cwd()
    csv_files = list(current_dir.glob("*.csv"))

    # Filtriramo fajl da ne obrađujemo već popravljene fajlove (koji sadrže _timefixed200.csv u imenu)
    target_files = [f for f in csv_files if "_timefixed200" not in f.name]

    if not target_files:
        print(f"\n[X] Nema pronađenih sirovih CSV fajlova u folderu: {current_dir}")
        return

    print(f"\n[✓] Pronađeno {len(target_files)} fajlova za automatsku popravku vremenske ose.")
    target_fs = 200.0

    success_count = 0

    for src in target_files:
        print("-" * 75)
        print(f" Obrada fajla: {src.name}...")

        try:
            # Učitavanje CSV fajla uz preskakanje komentara
            df = pd.read_csv(src, comment='#')
        except Exception as e:
            print(f"    [!] Greška pri čitanju fajla '{src.name}': {e}")
            continue

        # Očišćena imena kolona
        df.columns = [c.strip() for c in df.columns]

        if 't_s' not in df.columns and 'timestamp' not in df.columns:
            print(f"    [!] Preskočeno: Fajl ne sadrži kolonu za vreme ('t_s' ili 'timestamp').")
            continue

        n_samples = len(df)
        if n_samples == 0:
            print(f"    [!] Preskočeno: Fajl je prazan.")
            continue

        # Kreiranje savršeno uniformne vremenske ose bez OS/USB jitter-a
        t_repaired = np.arange(n_samples, dtype=float) / target_fs
        total_duration = t_repaired[-1] if n_samples > 0 else 0.0

        print(f"    - Ukupno uzoraka (N)          : {n_samples}")
        print(f"    - Korigovano trajanje snimka  : {total_duration:.2f} s")
        print(f"    - Hardverska frekvencija      : {target_fs:.2f} Hz")

        # Zamena ili ubacivanje korigovane vremenske ose
        if 't_s' in df.columns:
            df['t_s'] = t_repaired
        elif 'timestamp' in df.columns:
            df['timestamp'] = t_repaired
            df.rename(columns={'timestamp': 't_s'}, inplace=True)
        else:
            df.insert(0, 't_s', t_repaired)

        # Generisanje izlaznog fajla sa sufiksom _timefixed200.csv
        out_name = src.stem + "_timefixed200.csv"
        out_path = src.with_name(out_name)

        with out_path.open("w", encoding="utf-8", newline="") as wf:
            wf.write(f"# format,MSMR-1.0\n")
            wf.write(f"# source,{src.name}\n")
            wf.write(f"# note,hardware_locked_200hz_time_axis_batch_repaired\n")
            wf.write(f"# fixed_fs,{target_fs:.2f}\n")
            wf.write(f"# total_samples,{n_samples}\n\n")
            df.to_csv(wf, index=False)

        print(f"    [USPEH] Sačuvan korigovani fajl: '{out_path.name}'")
        success_count += 1

    print("\n" + "=" * 90)
    print(f" [ZAVRŠENO] Uspešno obrađeno {success_count} od {len(target_files)} fajlova.")
    print(" Svi fajlovi sada imaju idealnu, stabilnu 200 Hz vremensku osu bez interpolacije signala!")
    print("=" * 90 + "\n")

if __name__ == "__main__":
    batch_repair_time_axes()