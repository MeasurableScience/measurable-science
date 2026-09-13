# Eskdalemuir, Scotland — Institutional Carrier Measurement

## Overview

This directory contains the analysis of high-frequency induction-coil
magnetometer data recorded at Eskdalemuir, Scotland.

The purpose of the analysis was to test whether an independently recorded
institutional magnetic-field dataset contains a persistent phase-organized
structure that can be detected without supplying the expected carrier
frequency to the search algorithm.

The analysis was intentionally divided into separate stages:

1. blind frequency discovery;
2. independent frequency refinement;
3. absolute magnetic-field and energy analysis;
4. investigation of large energy events;
5. clean local two-component geometry analysis.

The frequency expected by the model was not supplied to the blind search.

---

## Instrument and data

The Eskdalemuir system uses two horizontal induction-coil magnetometers
recording rapid variations of the Earth's magnetic field.

The data analyzed here are sampled at:

**100 samples per second (100 Hz)**

The two horizontal channels are referred to as:

- `CH1`
- `CH2`

Instrument provenance, calibration information, original data sources and
supporting publications are documented separately in:

`references/eskdalemuir_instrument_and_data_sources.md`

---

# 1. Blind frequency search

The first analysis searched the frequency range:

**1–10 Hz**

No expected carrier frequency was supplied to the program.

The analysis used the phase relationship between the two independently
measured horizontal magnetic components rather than selecting the strongest
FFT amplitude.

Phase organization was quantified using the Phase Locking Value:

`PLV = |mean(exp(i * (phi1 - phi2)))|`

where `phi1` and `phi2` are the instantaneous phases of CH1 and CH2.

The search identified a dominant phase-organized cluster at:

**6.8–8.2 Hz**

with a coarse maximum near:

**7.6 Hz**

Main blind-search outputs are stored in:

`results/blind/`

including:

- `ESK_PLV_60S_CARRIERS.csv`
- `ESK_PLV_60S_PROFILE.csv`
- `ESK_PLV_60S_VOTES.csv`

---

# 2. Independent frequency refinement

After the 6.8–8.2 Hz region had already been identified by the blind search,
a separate high-resolution refinement was performed.

The refinement searched:

**6.5–8.5 Hz**

with a frequency step of:

**0.001 Hz**

The expected final frequency was not supplied to the refinement algorithm.

The refinement used 12 independently selected days distributed through the
analyzed period and produced 272 usable hourly measurements.

Main results:

| Quantity | Result |
|---|---:|
| Aggregate peak of mean profile | **7.748 Hz** |
| Aggregate peak mean PLV | **0.554263** |
| Aggregate peak of median profile | **7.742 Hz** |
| Aggregate peak median PLV | **0.579494** |
| Weighted center, mean profile | **7.658007 Hz** |
| Weighted center, median profile | **7.666985 Hz** |
| Hourly weighted-center mean | **7.517651 Hz** |
| Hourly weighted-center SD | **0.152219 Hz** |

The instantaneous spectral maximum moved substantially more than the
weighted center of the structure.

This is important because the detected feature is therefore better described
as an organized frequency region with a relatively stable center than as a
single perfectly stationary spectral line.

Refinement outputs are stored in:

`results/refinement/`

including:

- `ESK_REFINED_12DAY_AGGREGATE.csv`
- `ESK_REFINED_12DAY_HOURLY.csv`
- `ESK_REFINED_12DAY_PROFILE.csv`
- `ESK_REFINED_12DAY_SUMMARY.csv`

---

# 3. Absolute magnetic-field and energy analysis

PLV measures phase organization. It is not a measure of field energy.

Absolute magnetic-field analysis was therefore performed separately using
the raw digitizer data and the published Eskdalemuir calibration.

Digitizer conversion factors used:

- CH1: `3.491 × 10^-6 V/count`
- CH2: `3.475 × 10^-6 V/count`

The induction-coil response in the carrier region is approximately:

**50.205 mV/nT**

The raw signal was converted to calibrated magnetic spectral density and
integrated across the previously identified carrier band:

**6.8–8.2 Hz**

For a number of complete hourly records, values near:

**456 nT RMS**

were obtained.

For magnetic RMS amplitude, the corresponding magnetic energy density is:

`u_B = B_rms^2 / (2 * mu_0)`

For approximately 456 nT RMS:

**u_B ≈ 8.3 × 10^-8 J/m^3**

This is a local magnetic-field measurement.

---

## Model-scale energy calculation

The carrier model used in this project assigns approximately one quarter of
the Earth's surface to one carrier.

Using an effective model height of approximately:

**50 km**

gives a model volume of approximately:

**6.38 × 10^18 m^3**

If the locally measured magnetic energy density were representative of this
entire model volume, the corresponding magnetic-energy scale would be:

**≈ 5.3 × 10^11 J**

or approximately:

- **530 GJ**
- **147 MWh**

This is explicitly a model-dependent spatial extrapolation.

It is **not** a direct measurement of the total energy of a planetary-scale
carrier.

---

# 4. Large energy events

Time-resolved analysis revealed a separate and much stronger class of events.

A total of:

**1,312 major events**

were identified.

Their timing showed a strong concentration near a 30-second interval:

- mean interval: **≈ 29.99 s**
- median interval: **≈ 30.00 s**

Subsequent inspection showed that the events coincide with very large
changes already present in the raw magnetometer data.

The event analysis contains repeated amplitude classes in the order of
**tens of thousands of nanotesla**, including individual values around:

- **50,000 nT**
- **60,000 nT**
- **70,000 nT**
- and higher values in the same order of magnitude.

The physical origin of these large raw events has **not been established by
this analysis**.

They are therefore not classified here as carrier energy, but they are also
not discarded or reclassified as instrumental noise without independent
evidence.

They are retained as a separate measured phenomenon.

---

## Energy scale of a 70,000 nT event

For scale only:

**70,000 nT = 70 µT**

The instantaneous magnetic energy density corresponding to this field
magnitude is:

`u_B = B^2 / (2 * mu_0)`

which gives approximately:

**1.95 × 10^-3 J/m^3**

If this local magnetic energy density were hypothetically representative of
the same model volume:

**6.38 × 10^18 m^3**

the corresponding energy scale would be approximately:

**1.24 × 10^16 J**

or:

- **12.4 PJ**
- **3.45 TWh**
- approximately **3 megatons TNT equivalent**

This calculation is included only to show the physical scale associated with
the measured field magnitude.

It does **not** establish that an individual event releases this amount of
energy, nor does it establish that the large events originate from the
carrier.

---

# 5. Large-event diagnostic

A narrow-band event-centered analysis was also performed.

This test demonstrated an important methodological limitation.

A sufficiently large discontinuity in the raw signal contains broadband
spectral energy. Passing such a discontinuity through a narrow 6.8–8.2 Hz
band-pass filter can generate strong ringing inside the carrier band.

Therefore, event-centered filtered amplitude and phase geometry cannot by
themselves be used as reliable measurements of the underlying carrier
geometry.

For this reason, the large-event intervals were separated from the final
geometry analysis.

The events themselves remain in the dataset and are documented separately.

---

# 6. Clean local carrier geometry

The final geometry test was performed independently of the large events.

Paired CH1/CH2 hourly records were examined using fixed 60-second windows.
Intervals containing large raw discontinuities were rejected using an
objective first-difference criterion before calculating the final
two-component geometry.

Results:

| Quantity | Result |
|---|---:|
| Paired hours examined | **4,786** |
| Accepted clean windows | **2,502** |
| Rejected raw-step windows | **1,858** |
| Rejected length/data windows | **426** |
| Median vector RMS | **0.0011425 nT = 1.1425 pT** |
| Median CH1–CH2 PLV | **0.350450** |
| Median phase difference | **-99.022°** |
| Median PCA minor/major ratio | **0.617965** |
| Median ellipticity | **0.170164** |
| Median local orientation | **-12.066°** |
| Clockwise windows | **2,397** |
| Counter-clockwise windows | **105** |

Of the 2,502 accepted clean windows:

**95.8% showed the same signed rotation direction in the local CH1–CH2
measurement plane.**

The polarization was not predominantly circular:

- **58.55%** of windows had ellipticity below 0.20;
- **0%** had ellipticity above 0.80.

The clean signal therefore shows a strongly preferred local rotation
direction together with an elongated two-component polarization structure.

These measurements describe the **local magnetic projection at the
Eskdalemuir station**.

They are not a direct spatial image of a planetary-scale carrier.

Geometry outputs are stored in:

`results/geometry/`

including:

- `ESK_CLEAN_CARRIER_GEOMETRY.csv`
- `ESK_CLEAN_CARRIER_GEOMETRY_SUMMARY.csv`
- `ESK_CLEAN_PHASE_DIFFERENCE.png`
- `ESK_CLEAN_ELLIPTICITY.png`
- `ESK_CLEAN_ORIENTATION.png`
- `ESK_CLEAN_PHASE_PLANE_EXAMPLES.png`

The analysis script is:

`scripts/esk_clean_carrier_geometry.py`

---

# Interpretation

The Eskdalemuir analysis produced four distinct observational results:

1. a blindly detected phase-organized structure at **6.8–8.2 Hz**;
2. a refined and comparatively stable frequency center near **7.66 Hz**;
3. measurable absolute magnetic-field energy within the detected band,
   together with a separate population of much larger time-organized events;
4. a strongly preferred local two-component rotation direction after the
   large raw discontinuities were removed.

These results should not be treated as four measurements of the same
quantity.

They answer different questions about frequency organization, absolute field
magnitude, temporal structure and local polarization.

In the carrier model developed in this project, their combination is
interpreted as the local measurable signature of the Scottish carrier.

The measurements themselves establish the properties reported above.

The interpretation of those properties as a planetary-scale carrier remains
a model interpretation.

---

# Reproducibility

The purpose of this directory is to keep the evidence chain reproducible.

The complete analysis should allow the following sequence to be independently
checked:

**original institutional data  
→ provenance  
→ preprocessing  
→ blind search  
→ frequency refinement  
→ calibration  
→ energy analysis  
→ event analysis  
→ clean geometry analysis  
→ numerical results**

Expected directory structure:

    eskdalemuir-scotland/
    ├── README.md
    ├── references/
    │   └── eskdalemuir_instrument_and_data_sources.md
    ├── scripts/
    └── results/
        ├── blind/
        ├── refinement/
        ├── energy/
        ├── energy-events/
        └── geometry/

Raw institutional data are not modified to obtain the expected model result.

Where filtering, rejection criteria or model-dependent spatial
extrapolations are used, they are documented separately from the original
measurement.

The central reproducibility rule of this analysis is:

**The program must not know the result it is expected to find.**