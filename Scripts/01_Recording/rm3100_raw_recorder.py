"""
==================================================
Project:
    Measurable Science

Script:
    RM3100 Raw Recorder

Purpose:
    Records raw magnetic field measurements produced
    by the RM3100 acquisition firmware.

    The recorder stores the original serial output
    exactly as received without parsing, filtering,
    calibration or interpretation.

    Recording metadata are stored together with the
    raw measurements.

Author:
    Mladan Ilic

License:
    MIT

Version:
    1.0

Usage:
    python3 rm3100_raw_recorder.py

Dependencies:
    pip install pyserial
==================================================
"""

import csv
import os
import time
from datetime import datetime

import serial
from serial.tools import list_ports


DEFAULT_BAUDRATE = 115200
OUTPUT_DIR = "recordings"
RECORDER_NAME = "rm3100_raw_recorder.py"
VERSION = "1.0"
FIRMWARE = "RM3100 acquisition firmware"


def select_port():
    ports = list(list_ports.comports())

    if not ports:
        raise RuntimeError("No serial devices found.")

    print("\nAvailable serial ports:\n")

    for index, port in enumerate(ports, start=1):
        print(f"{index}. {port.device}    {port.description}")

    while True:
        try:
            choice = int(input("\nSelect port: "))

            if 1 <= choice <= len(ports):
                return ports[choice - 1].device
        except ValueError:
            pass

        print("Invalid selection.")


def next_filename():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    existing = [
        filename
        for filename in os.listdir(OUTPUT_DIR)
        if filename.startswith("recording_") and filename.endswith(".csv")
    ]

    numbers = []

    for filename in existing:
        try:
            number = int(filename[10:13])
            numbers.append(number)
        except (ValueError, IndexError):
            pass

    next_number = max(numbers, default=0) + 1

    return os.path.join(
        OUTPUT_DIR,
        f"recording_{next_number:03d}.csv",
    )


def read_positive_duration():
    while True:
        try:
            duration = float(input("Recording duration (seconds): "))

            if duration > 0:
                return duration
        except ValueError:
            pass

        print("Enter a valid positive number.")


def main():
    print("=" * 50)
    print("Measurable Science")
    print("RM3100 Recorder")
    print("=" * 50)

    try:
        port = select_port()
    except RuntimeError as error:
        print(f"\nError: {error}")
        return

    location = input("\nLocation: ").strip() or "Unknown"
    note = input("Note (optional): ").strip()
    duration = read_positive_duration()

    filename = next_filename()
    start_time = datetime.now()

    print("\nRecording...")
    print(f"Port      : {port}")
    print(f"Baudrate  : {DEFAULT_BAUDRATE}")
    print(f"Location  : {location}")

    if note:
        print(f"Note      : {note}")

    print(f"Output    : {filename}")
    print("Press Ctrl+C to stop.\n")

    count = 0
    start = time.perf_counter()
    stopped_by_user = False

    try:
        with serial.Serial(
            port,
            DEFAULT_BAUDRATE,
            timeout=1,
        ) as ser, open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.writer(file)

            writer.writerow(["# Project", "Measurable Science"])
            writer.writerow(["# Recorder", RECORDER_NAME])
            writer.writerow(["# Version", VERSION])
            writer.writerow(["# Firmware", FIRMWARE])
            writer.writerow(["# Port", port])
            writer.writerow(["# Baudrate", DEFAULT_BAUDRATE])
            writer.writerow(["# Location", location])
            writer.writerow(["# Note", note])
            writer.writerow([
                "# Start Time",
                start_time.isoformat(timespec="milliseconds"),
            ])
            writer.writerow(["# Requested Duration (s)", duration])
            writer.writerow([])

            writer.writerow([
                "sample_id",
                "pc_timestamp",
                "elapsed_s",
                "raw_data",
            ])

            ser.reset_input_buffer()

            # Discard the first line because the serial stream may be opened
            # in the middle of an already transmitted record.
            ser.readline()

            try:
                while True:
                    now = time.perf_counter()

                    if now - start >= duration:
                        break

                    raw = ser.readline()

                    if not raw:
                        continue

                    line = raw.decode(
                        "utf-8",
                        errors="replace",
                    ).strip()

                    if not line:
                        continue

                    elapsed = time.perf_counter() - start
                    count += 1

                    writer.writerow([
                        count,
                        datetime.now().isoformat(
                            timespec="milliseconds"
                        ),
                        round(elapsed, 6),
                        line,
                    ])

            except KeyboardInterrupt:
                stopped_by_user = True
                print("\nRecording stopped by user.")

            total = time.perf_counter() - start
            average_rate = count / total if total > 0 else 0.0

            writer.writerow([])
            writer.writerow(["# Samples", count])
            writer.writerow(["# Actual Duration (s)", round(total, 3)])
            writer.writerow([
                "# Average Rate (Hz)",
                round(average_rate, 3),
            ])
            writer.writerow([
                "# Stop Reason",
                "User interruption" if stopped_by_user else "Duration completed",
            ])

    except serial.SerialException as error:
        print(f"\nCould not open or read serial port: {port}")
        print(f"Reason: {error}")
        print(
            "Close Serial Monitor, screen, or any other program "
            "using this port and try again."
        )
        return
    except OSError as error:
        print(f"\nFile error: {error}")
        return

    print("\nFinished.")
    print(f"Samples : {count}")
    print(f"Duration: {total:.2f} s")
    print(f"Rate    : {average_rate:.2f} Hz")
    print(f"Saved to: {filename}")


if __name__ == "__main__":
    main()

