# Eskdalemuir Instrument and Data Sources

## Purpose

This document records the provenance, instrumentation, sampling information,
calibration sources and external references used for the Eskdalemuir analysis
in this repository.

The purpose is to keep the institutional measurements and their calibration
separate from the interpretation developed in the Measurable Science model.

---

# 1. Observatory

The measurements originate from:

**Eskdalemuir Geophysical Observatory**  
Scottish Borders, United Kingdom

Approximate observatory coordinates reported in the scientific literature:

**55.31° N, 3.21° W**

Eskdalemuir is operated as a geomagnetic observatory by the
British Geological Survey (BGS).

BGS describes the site as a rural location with a quiet magnetic environment,
suitable for high-frequency geomagnetic measurements.

---

# 2. High-frequency induction-coil system

In June 2012, the British Geological Survey installed two high-frequency
induction-coil magnetometers at Eskdalemuir.

The system measures two horizontal components of rapid variations in the
Earth's magnetic field.

The channels are:

- **CH1 — North–South**
- **CH2 — East–West**

Sampling frequency:

**100 Hz**

The induction coils are sensitive to rapid magnetic-field variations in the
Extremely Low Frequency (ELF) range.

BGS describes the induction-coil system as operating over approximately:

**0.1–100 Hz**

for the high-frequency monitoring application.

An induction-coil magnetometer consists of insulated copper wire wound around
a magnetic core. A changing magnetic field induces a voltage in the coil,
allowing rapid magnetic-field variations to be measured.

---

# 3. British Geological Survey source

Official BGS high-frequency magnetometer information:

https://www.geomag.bgs.ac.uk/research/inductioncoils.html

Eskdalemuir Observatory information:

https://www.geomag.bgs.ac.uk/operations/eskdale.html

The official BGS page confirms that two 100 Hz induction-coil magnetometers
were installed at Eskdalemuir in June 2012.

---

# 4. 2012 institutional dataset

The primary institutional dataset used for the blind 2012 analysis is:

**British Geological Survey (2018)**  
*2012 High frequency magnetic field induction coil data from Eskdalemuir
Observatory, UK*

DOI:

https://doi.org/10.5285/6dcca520-47f2-45bd-9fd1-61354450d17d

BGS dataset catalogue:

https://www2.bgs.ac.uk/nationalgeosciencedatacentre/citedData/catalogue/6dcca520-47f2-45bd-9fd1-61354450d17d.html

BGS describes this dataset as:

- high-frequency magnetic-field measurements;
- two horizontal induction coils;
- 100 Hz sampling;
- hourly ASCII data files;
- Eskdalemuir Observatory, United Kingdom;
- September 2012 through December 2012.

The BGS dataset also includes calibration information and example MATLAB
code for converting the raw measurements to physical units.

### Important date-scope note

The official BGS 2012 dataset identified by the DOI above is explicitly
documented as covering:

**September 2012 – December 2012**

Therefore, analyses claimed specifically against this DOI should use that
documented period unless independent provenance is established for additional
files.

Local working directories used during development contained files carrying
earlier 2012 timestamps. Those files must not be attributed to the
September–December BGS DOI solely from their filenames.

This distinction is retained deliberately so that dataset provenance remains
auditable.

---

# 5. Independent scientific calibration reference

A detailed independent description and validation of the Eskdalemuir
high-frequency data and calibration is provided by:

**Atsushi Nishizawa, Atsushi Taruya, and Yoshiaki Himemoto (2026)**  
*Axion Dark Matter Search from Terrestrial Magnetic Fields at Extremely Low
Frequencies*  
Progress of Theoretical and Experimental Physics, 2026, 073E02.

DOI:

https://doi.org/10.1093/ptep/ptag108

The authors used publicly available Eskdalemuir magnetic-field data recorded
from:

**1 September 2012 – 4 November 2022**

They identify the sensors as:

**CM11E1 induction coils**

with:

- CH1: North–South
- CH2: East–West
- sampling frequency: 100 Hz.

The raw measurements are stored in digitizer units and require conversion to
physical magnetic-field units.

---

# 6. Digitizer conversion

The conversion factors reported by Nishizawa et al. are:

| Channel | Digitizer conversion |
|---|---:|
| CH1 | **3.491 × 10^-6 V/count** |
| CH2 | **3.475 × 10^-6 V/count** |

These factors convert the raw digitizer counts to voltage.

A second, frequency-dependent calibration is then required to convert voltage
to magnetic-field amplitude.

---

# 7. Frequency-dependent induction-coil calibration

The published Eskdalemuir calibration converts magnetic-field amplitude in
nanotesla to output voltage in millivolts.

Selected calibration values are:

| Frequency (Hz) | Calibration (mV/nT) |
|---:|---:|
| 100 | 50.151 |
| 50 | 50.282 |
| 32 | 50.258 |
| 18 | 50.223 |
| 10 | 50.209 |
| 5.6 | 50.204 |
| 3.2 | 50.199 |
| 1.8 | 50.200 |
| 1.0 | 50.169 |
| 0.56 | 50.167 |
| 0.32 | 50.157 |
| 0.18 | 50.139 |
| 0.10 | 50.077 |
| 0.056 | 49.939 |
| 0.032 | 49.540 |
| 0.018 | 48.237 |
| 0.010 | 44.639 |
| 0.007 | 40.402 |
| 0.005 | 34.041 |
| 0.003 | 22.464 |
| 0.002 | 13.736 |
| 0.001 | 4.530 |

Source:

Nishizawa, Taruya & Himemoto (2026), Appendix A, Table A1.

---

# 8. Calibration in the detected 6.8–8.2 Hz region

The calibration response is effectively flat across the frequency region used
for the carrier analysis.

The nearest published calibration points are:

- 5.6 Hz → 50.204 mV/nT
- 10 Hz → 50.209 mV/nT

Interpolation across 6.8–8.2 Hz therefore gives approximately:

**50.205–50.207 mV/nT**

For the calculations in this repository, approximately:

**50.205 mV/nT**

is used where a single representative calibration value is required.

Combining the digitizer conversion with this response gives approximately:

**CH1**

3.491 × 10^-6 V/count ÷ 0.050205 V/nT

≈ **6.95 × 10^-5 nT/count**

≈ **0.0695 pT/count**

**CH2**

3.475 × 10^-6 V/count ÷ 0.050205 V/nT

≈ **6.92 × 10^-5 nT/count**

≈ **0.0692 pT/count**

These values apply specifically to the approximately 7–8 Hz region and
should not be treated as universal calibration constants across the complete
instrument bandwidth.

---

# 9. Independent calibration validation

Nishizawa et al. independently checked whether the historical calibration
remained reliable during the long observational period.

They compared the spectral magnetic-field amplitudes derived from the
high-frequency induction-coil system with measurements from an independent
instrument at Eskdalemuir available through INTERMAGNET.

Their comparison showed consistency between the systems over the examined
period.

The authors therefore concluded that the calibration factors remained
reliable for their 2012–2022 analysis.

This validation is important for the present repository because the absolute
magnetic-field and magnetic-energy calculations depend on the conversion from
raw digitizer counts to physical magnetic-field units.

---

# 10. Schumann-resonance context

The approximately 7–8 Hz region is not an unknown part of the terrestrial
electromagnetic spectrum.

Conventional geophysics identifies the first Schumann resonance in this
region, with the first resonance commonly occurring near:

**7.8 Hz**

Schumann resonances are conventionally interpreted as electromagnetic
resonances of the Earth–ionosphere cavity.

Nishizawa et al. explicitly identify the prominent feature near 7.8 Hz in
their Eskdalemuir analysis as the first Schumann resonance.

This conventional interpretation must be kept separate from the carrier
interpretation developed in the Measurable Science project.

The institutional measurements establish the magnetic-field data.

The carrier is the interpretation tested in this repository.

---

# 11. Independent published use of Eskdalemuir induction-coil data

The Eskdalemuir high-frequency induction-coil measurements have also been used
in peer-reviewed geophysical research.

One relevant example is:

**Beggan et al. (2018)**  
*Observation of Ionospheric Alfvén Resonances at 1–30 Hz and Their
Superposition With the Schumann Resonances*  
Journal of Geophysical Research: Space Physics.

DOI:

https://doi.org/10.1029/2018JA025264

This work uses Eskdalemuir induction-coil measurements and explicitly lists
the BGS yearly dataset DOIs.

Its use of the same institutional measurement system provides an additional
published provenance trail for the Eskdalemuir high-frequency data.

---

# 12. Measurement versus interpretation

The evidence chain used in this repository is intentionally separated into
two levels.

## Institutional measurement

The following originate from external institutional or published sources:

- observatory location;
- induction-coil instrumentation;
- channel orientation;
- 100 Hz sampling;
- raw digitizer measurements;
- digitizer voltage conversion;
- frequency-dependent calibration;
- independent calibration validation.

## Measurable Science analysis

The following are results or interpretations produced by the analysis in this
repository:

- blind PLV search;
- automatically detected frequency cluster;
- frequency refinement;
- absolute magnetic-field calculation in the selected band;
- magnetic-energy calculation;
- event detection;
- event-interval analysis;
- clean two-component geometry analysis;
- interpretation in terms of the carrier model.

The British Geological Survey and the authors cited above do **not** claim to
have detected a "carrier" as that term is used in this project.

Their measurements provide the independent institutional data against which
the model is tested.

---

# 13. Reproducibility principle

The order of analysis is important.

The expected carrier frequency was not taken from the calibration literature
and inserted into the blind search.

The evidence chain is:

**institutional raw measurement  
→ blind search  
→ detected frequency region  
→ independent refinement  
→ calibration  
→ absolute magnetic-field analysis  
→ energy analysis  
→ event analysis  
→ geometry analysis  
→ model interpretation**

Calibration is applied after the relevant frequency region has been selected
where absolute physical units are required.

This separation prevents the published calibration curve or the known
Schumann-resonance frequency from acting as the frequency-selection rule for
the blind discovery stage.

---

# References

## British Geological Survey

British Geological Survey.  
*High-frequency Magnetometers — Induction Coils.*  
BGS Geomagnetism.

https://www.geomag.bgs.ac.uk/research/inductioncoils.html

British Geological Survey.  
*Eskdalemuir Magnetic Observatory.*

https://www.geomag.bgs.ac.uk/operations/eskdale.html

British Geological Survey (2018).  
*2012 High frequency magnetic field induction coil data from Eskdalemuir
Observatory, UK.*

https://doi.org/10.5285/6dcca520-47f2-45bd-9fd1-61354450d17d

## Calibration

Nishizawa, A., Taruya, A., & Himemoto, Y. (2026).  
*Axion Dark Matter Search from Terrestrial Magnetic Fields at Extremely Low
Frequencies.*  
Progress of Theoretical and Experimental Physics, 2026, 073E02.

https://doi.org/10.1093/ptep/ptag108

## Independent scientific use

Beggan, C. D., et al. (2018).  
*Observation of Ionospheric Alfvén Resonances at 1–30 Hz and Their
Superposition With the Schumann Resonances.*  
Journal of Geophysical Research: Space Physics.

https://doi.org/10.1029/2018JA025264

---

# Data acknowledgement

When reproducing or redistributing BGS material, the applicable BGS licence
and acknowledgement requirements should be followed.

The BGS catalogue specifies acknowledgement of the use of induction-coil data
from Eskdalemuir Observatory supplied by the British Geological Survey and
the applicable NERC copyright notice.