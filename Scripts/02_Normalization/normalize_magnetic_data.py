#!/usr/bin/env python3
"""
Project: Measurable Science
Script : normalize_magnetic_data.py

Normalizes supported magnetic CSV formats from the script's directory into:
t_s,mx,my,mz,yaw_deg
"""

import csv
import re
from pathlib import Path

RM_PATTERN = re.compile(
    r"Magx:(-?\d+),Magy:(-?\d+),Magz:(-?\d+),Yaw:(-?\d+\.?\d*)"
)

def detect(header):
    h=[x.strip() for x in header]
    if "raw_data" in h and "elapsed_s" in h:
        return "rm3100"
    if "t_s" in h and "mx" in h and "my" in h and "mz" in h:
        return "clean"
    if "timestamp" in h and "mx" in h and "my" in h and "mz" in h:
        return "wt901"
    return None

# Automatski uzima folder u kome se sama skripta nalazi
src_dir = Path(__file__).resolve().parent

# Pronalaženje svih .csv fajlova u tom folderu
csv_files = [f for f in src_dir.glob("*.csv") if not f.name.endswith("_normalized.csv")]

if not csv_files:
    raise SystemExit(f"No CSV files found in the directory: {src_dir}")

print(f"Working directory : {src_dir}")
print(f"Found {len(csv_files)} CSV file(s) to process.\n" + "-" * 40)

for src in csv_files:
    out = src.with_name(src.stem + "_normalized.csv")

    try:
        with src.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)

            metadata = []
            header = None

            for row in reader:
                if not row:
                    continue
                if row[0].startswith("#"):
                    metadata.append(row)
                    continue
                header = row
                break

            if header is None:
                print(f"Skipping {src.name}: Empty or invalid file.")
                print("-" * 40)
                continue

            fmt = detect(header)
            if fmt is None:
                print(f"Skipping {src.name}: Unsupported format.")
                print("-" * 40)
                continue

            with out.open("w", encoding="utf-8", newline="") as writer_file:
                writer = csv.writer(writer_file)

                writer.writerow(["# format", "MSMR-1.0"])
                writer.writerow(["# source", src.name])
                writer.writerow(["# detected_format", fmt])
                writer.writerow([])
                writer.writerow(["t_s", "mx", "my", "mz", "yaw_deg"])

                h = {k.strip(): i for i, k in enumerate(header)}
                count = 0

                for row in reader:
                    if not row:
                        continue
                    if row[0].startswith("#"):
                        continue

                    try:
                        if fmt == "rm3100":
                            m = RM_PATTERN.search(row[h["raw_data"]])
                            if not m:
                                continue
                            writer.writerow([
                                row[h["elapsed_s"]],
                                m.group(1),
                                m.group(2),
                                m.group(3),
                                m.group(4)
                            ])

                        elif fmt == "clean":
                            writer.writerow([
                                row[h["t_s"]],
                                row[h["mx"]],
                                row[h["my"]],
                                row[h["mz"]],
                                row[h["yaw_deg"]] if "yaw_deg" in h else ""
                            ])

                        elif fmt == "wt901":
                            yaw = row[h["yaw_deg"]] if "yaw_deg" in h else ""
                            if row[h["mx"]] == "" or row[h["my"]] == "" or row[h["mz"]] == "":
                                continue
                            t0 = row[h["timestamp"]]
                            writer.writerow([
                                t0,
                                row[h["mx"]],
                                row[h["my"]],
                                row[h["mz"]],
                                yaw
                            ])

                        count += 1

                    except Exception:
                        pass

        print(f"File            : {src.name}")
        print(f"Detected format : {fmt}")
        print(f"Samples written : {count}")
        print(f"Output          : {out.name}")
        print("-" * 40)

    except Exception as e:
        print(f"Error processing {src.name}: {e}")
        print("-" * 40)