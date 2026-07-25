# Measurement Protocol

This document describes the recommended procedure for collecting measurements that can be compared with other datasets contained in the **Measurable Science** project.

These recommendations are intended to improve reproducibility and simplify comparison between measurements collected by different researchers around the world.

The procedures described here are recommendations, not mandatory requirements.

Alternative measurement methods are welcome provided they are adequately documented.

---

# Measurement Objective

The current research focuses on signals containing information within the frequency range:

**0 Hz – 20 Hz**

Your equipment is **not required** to be limited to this range.

Measurements recorded at higher frequencies are fully acceptable and often desirable.

The only requirement is that the submitted recordings contain usable information within the **0–20 Hz** frequency range.

---

The **0–20 Hz** frequency range was selected because it is the primary focus of the research currently presented in this repository.

Contributors are encouraged to preserve the complete original recordings whenever possible, even when they contain frequencies well above 20 Hz.

Future research may investigate additional frequency ranges, making the original unprocessed data valuable for analyses beyond the current scope of the project.

---

# Measurement Equipment

There is no mandatory hardware.

Any measurement system capable of recording signals within the required frequency range may be used.

Examples include:

- induction coils
- magnetometers
- accelerometers
- laboratory instruments
- software-defined measurement systems
- custom-built electronics
- other experimental sensors

The equipment documented elsewhere in this repository represents only a few possible approaches.

If you already have your own measurement system, you are encouraged to use it.

---

# Sampling Frequency

There is no required sampling frequency.

Please include the sampling frequency used during acquisition.

Higher sampling frequencies are welcome provided the original measurements are preserved.

---

# Recording Duration

There is no minimum recording duration.

Longer recordings generally provide more opportunities for analysis.

Please include:

- recording start time
- recording duration
- local time zone

---

# Raw Data

Whenever possible, please submit the original, unprocessed recordings.

Avoid filtering, smoothing or modifying the original data before submission.

Processed data, graphs and screenshots are welcome as supplementary material but should not replace the original measurements.

---

# Accepted Data Formats

The repository accepts raw measurement data in many formats, including:

- CSV
- WAV
- TXT
- JSON
- Binary
- NumPy
- MATLAB
- HDF5
- or any other format preserving the original measurements.

Large datasets should preferably be compressed using ZIP or 7Z.

---

# Recommended Metadata

Please include as much information as possible.

Recommended information includes:

- measurement date
- local time
- time zone
- country
- location
- GPS coordinates (if available)
- equipment used
- sensor model
- sampling frequency
- software used
- firmware version (if applicable)
- sensor orientation (if applicable)

---

# Environmental Information

If known, please also include:

- indoor or outdoor measurement
- weather conditions
- nearby power lines
- nearby electrical equipment
- thunderstorms
- significant electromagnetic interference
- any observations that may help interpret the data

---

# Photographs

Whenever possible, include photographs showing:

- the measurement setup
- sensor placement
- surrounding environment

Photographs often provide valuable context during later analysis.

---

# Suggested Folder Structure

Each submitted experiment may be organized as follows.

Experiment/

├── Data/

├── Photos/

├── Experiment.md

└── AdditionalFiles/

---

# Experiment Documentation

A template for documenting experiments is available in:

Templates/Experiment.md

Use of the template is recommended but not required.

---

# Independent Methods

This repository is intentionally hardware independent.

The objective is **not** to standardize measurement equipment.

The objective is to compare observations obtained using different instruments, different methodologies and different locations.

Independent measurements performed using different techniques often provide the strongest scientific evidence.

---

# Questions

If you are unsure whether your measurements are suitable for this project, please contact the project maintainer before submitting your data.