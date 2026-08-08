# Normalization

The **Normalization** directory contains scripts used to convert magnetic measurements acquired from different devices into a common file format.

Different sensors and recorders often produce different CSV structures, column names or metadata.

Scientific analysis becomes much simpler when every dataset follows the same format.

Normalization does **not** modify the measured values.

Its only purpose is to reorganize the data into a standardized structure that can be used by all analysis scripts in this repository.

---

# Purpose

The normalization scripts are intended to:

- convert supported CSV formats into a common format;
- preserve the original measurements;
- simplify subsequent analysis;
- eliminate differences between recording software.

No filtering, calibration or signal processing is performed during normalization.

---

# Standard Output Format

All supported input formats are converted into:

```text
t_s,mx,my,mz,yaw_deg
```

where:

- **t_s** — measurement timestamp (seconds);
- **mx** — magnetic field X component;
- **my** — magnetic field Y component;
- **mz** — magnetic field Z component;
- **yaw_deg** — yaw angle (if available).

This standardized format is used throughout the remaining scripts in the project.

---

# Supported Formats

The normalization script currently recognizes several recording formats automatically, including:

- RM3100 recorder output;
- WT901 recorder output;
- already normalized datasets.

Additional formats can easily be added if required.

---

# Why Normalization?

The objective of this step is to make every subsequent analysis independent of the recording hardware.

Once a dataset has been normalized, all analysis scripts can operate on the same input format regardless of:

- sensor model;
- recorder software;
- operating system;
- communication interface.

This keeps the analysis scripts simpler and easier to maintain.

---

# Adapting Other Formats

If your recorder produces a different CSV structure, there is usually no need to rewrite the analysis scripts.

Instead, simply adapt the normalization script to your file format.

Modern AI assistants can usually perform this task automatically if provided with:

- your CSV file;
- the normalization script included in this repository.

The objective is simply to produce the standard output format:

```text
t_s,mx,my,mz,yaw_deg
```

Once this format has been obtained, all subsequent scripts in the repository can be used without modification.

---

# Open Research

Normalization is intended only to standardize data organization.

It should never alter the original measurements.

Researchers are encouraged to preserve the original raw recordings and use normalized copies for subsequent analysis.

---

# Sampling Rate Verification

After normalization, every recording should be checked to ensure that the sampling frequency matches the actual operating frequency of the device.

Although the recorder stores timestamps for every received sample, the computer records data as they arrive through the communication interface. Small timing variations introduced by the operating system or serial communication can make the measured sampling frequency appear different from the sensor's true operating frequency.

For example, a sensor configured to operate at **200 Hz** may appear to have an average sampling rate of **223 Hz** if the data are analyzed directly from the recorded timestamps.

Phase-sensitive analyses such as PLV, carrier characterization, modulation analysis and bicoherence assume uniformly sampled data. Using the apparent PC timing instead of the sensor's actual sampling frequency can introduce errors into these analyses.

The included resampling script automatically:

- estimates the sampling frequency from the normalized recording;
- identifies whether the device was operating in approximately **100 Hz** or **200 Hz** mode;
- generates a uniformly sampled dataset at the correct device frequency.

The original normalized dataset is always preserved.

All subsequent analysis scripts in this repository are intended to operate on the uniformly sampled dataset.