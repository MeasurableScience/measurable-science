# Recording

The **Recording** directory contains tools and guidelines used to acquire experimental measurements throughout the **Measurable Science** project.

Reliable scientific analysis begins with reliable measurements.

For this reason, the recording process focuses on preserving the original data together with as much information about the recording conditions as possible.

The complete measurement methodology is described in the accompanying book.

The objective of this directory is not to provide recording software for every possible sensor, but to demonstrate transparent recording methods that anyone can reproduce.

---

# Purpose

The recording tools are intended to:

- acquire raw measurements directly from sensors;
- preserve the original data without modification;
- record measurement metadata whenever possible;
- produce datasets suitable for independent verification and analysis.

The recording software intentionally performs as little processing as possible.

Signal processing and analysis are performed later using scripts contained in other sections of this repository.

---

# Recording Metadata

Whenever possible, every recording should include:

- recording location;
- date;
- local time;
- GPS coordinates (when available);
- sensor type;
- sampling frequency;
- recording duration;
- measurement orientation (if applicable);
- optional notes describing the recording conditions.

Photographs of the measurement setup are also strongly recommended whenever practical.

Well documented measurements are significantly more valuable than undocumented recordings.

---

# Raw Data

The primary objective of every recorder is to preserve the original measurements.

Whenever possible, raw data should be stored exactly as recorded, without filtering, calibration or post-processing.

Processing can always be performed later.

Original measurements cannot be recreated.

---

# Included Recorder

This repository currently includes a recorder for the **RM3100** magnetometer.

The recorder demonstrates the general philosophy used throughout this project:

- preserve the original measurements;
- automatically record useful metadata;
- keep the software simple and transparent;
- avoid unnecessary processing during acquisition.

It is intended to serve both as a practical tool and as an example that can easily be adapted for other hardware.

---

# Audio Recording

Audio measurements used in this project are recorded using **Audacity**.

Audacity is free, open-source software available for Windows, Linux and macOS.

Simply install Audacity, select the desired recording device, choose the required sample rate and press **Record**.

The recorded audio files can then be analyzed using the scripts provided elsewhere in this repository.

---

# Other Sensors

Different researchers may use different hardware.

Examples include:

- other magnetometers;
- inertial measurement units (IMU);
- GPS receivers;
- microphones;
- custom microcontrollers;
- other compatible sensors.

The methodology remains the same regardless of the recording device.

The important part is preserving the original measurements together with sufficient recording metadata.

---

# Adapting the Recorder

The recording scripts in this repository are intentionally simple.

If your hardware, operating system or communication interface is different, there is no need to write new software from scratch.

Simply provide one of the example scripts together with a description of your hardware to your preferred AI assistant.

Modern AI models can help you:

- adapt the recorder to another operating system;
- support different serial interfaces;
- modify the script for another sensor;
- change sampling parameters;
- record additional channels;
- troubleshoot communication problems.

The methodology remains identical even if the implementation changes.

---

# Open Research

Researchers are encouraged to adapt these recording tools to their own equipment and contribute improvements.

The objective is **not** to use identical hardware or identical software.

The objective is to obtain transparent, reproducible measurements that can be independently verified by anyone following the same methodology.