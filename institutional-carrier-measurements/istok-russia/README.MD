# Istok, Russia — Blind Carrier Detection and Local H-D Geometry

## Overview

This directory contains a reproducible analysis of high-frequency induction magnetometer data recorded at **Istok, Russia (IST)** by the Institute for Space-Earth Environmental Research (ISEE), Nagoya University, in collaboration with the Institute of Solar-Terrestrial Physics, Siberian Branch of the Russian Academy of Sciences.

The analysis was designed in stages.

The expected carrier frequency, phase relationship, polarization direction, or local geometry was **not supplied to the blind-search algorithm**.

The analysis sequence was:

1. blind frequency search,
2. frequency refinement,
3. full-day local H-D geometry,
4. time-shift null test.

The central methodological rule was:

> **The program must not know the result expected by the model.**

The term **carrier** is used here as terminology of the Measurable Science model. ISEE provides the magnetometer measurements; it does not identify the detected structure as a carrier.

---

## 1. Station and Data

**Station:** Istok  
**Code:** IST  
**Country:** Russia  
**Geographic coordinates:** 70.03° N, 88.01° E  
**Sampling frequency:** 64 Hz  
**Instrument type:** induction magnetometer  
**Components analysed:** H and D

Principal CDF file:

`isee_induction_ist_2017032800_v01.cdf`

Observation interval:

**2017-03-28 00:00:00 UTC – 2017-03-28 23:59:45.984375 UTC**

Number of samples:

**5,528,704**

Measured median sample interval:

**0.015625 s**

The sampling rate derived directly from the timestamps is therefore exactly:

**64 Hz**

The CDF metadata states that the sampling was triggered by a GPS clock signal.

Detailed provenance, calibration information, metadata, and institutional references are documented in:

`references/istok_instrument_and_data_sources.md`

---

# 2. Blind Search

The first stage searched for phase-organized structures in the H-D relationship without inserting an expected carrier frequency.

The search began at **1 Hz** with a frequency increment of:

**0.001 Hz**

Phase organization was measured using the **phase-locking value (PLV)** derived from Hilbert phases.

The algorithm determined the statistical threshold and grouped adjacent frequencies exceeding that threshold.

Multiple smaller coherent regions were detected.

One region was strongly dominant.

## Dominant blind-search structure

**Start:** 6.321 Hz  
**End:** 8.267 Hz  
**Blind peak:** 7.603 Hz  
**Peak mean PLV:** 0.539361  
**Integrated PLV score:** 94,838.911  
**Classification:** Phase Coherent Band

The next substantial detected region had an integrated score of approximately:

**2,433**

The dominant structure therefore exceeded it by approximately a factor of:

**39**

under this scoring method.

The blind result was not a single razor-thin spectral line.

It was a broad region of organized H-D phase relationship.

Blind-search outputs are stored in:

`results/blind/`

---

# 3. Frequency Refinement

Only after the blind algorithm had identified the dominant region was a fine-frequency refinement performed.

The refinement used:

- H-D components
- 64 Hz sampling
- actual UTC epochs from the CDF
- fixed 60-second windows
- 6.3–8.5 Hz refinement interval
- 0.001 Hz frequency step
- fourth-order Butterworth filtering
- 0.1 Hz analysis bandwidth
- Hilbert phase
- PLV

No expected carrier frequency was inserted into the refinement.

## Aggregate results

**Mean-profile maximum:** 7.667 Hz  
**Mean PLV:** 0.650972

**Median-profile maximum:** 7.708 Hz  
**Median PLV:** 0.718406

Weighted centres:

**Mean-profile weighted centre:** 7.625890 Hz  
**Median-profile weighted centre:** 7.567168 Hz

---

## Peak Motion Versus Structural Centre

The instantaneous hourly maximum moved substantially through the detected frequency region.

Hourly peak-frequency standard deviation:

**0.610312 Hz**

By contrast, the hourly weighted centre was considerably more stable:

**0.104090 Hz**

The weighted centre was therefore approximately:

**5.9 times more stable**

than the instantaneous peak when compared by standard deviation.

This distinction is important.

The result is more consistent with a **broad phase-organized structure with a comparatively stable centre** than with a perfectly fixed narrow radio-frequency line.

Refinement outputs are stored in:

`results/refinement/`

---

# 4. Full-Day Local H-D Geometry

The next stage asked a different question.

If the detected frequency structure represents an organized physical relationship between the two horizontal magnetic components, does that relationship have a persistent local geometry?

The complete daily H-D record was filtered in the blind-detected interval:

**6.321–8.267 Hz**

The continuous daily record was filtered before subdivision into one-minute windows.

For each usable minute, the analysis calculated:

- H-D phase-locking value,
- H-D phase difference,
- PCA major and minor axes,
- minor/major axis ratio,
- local major-axis orientation,
- signed H-D trajectory area,
- clockwise/counter-clockwise rotation.

A common scaling factor was used for H and D so that their measured amplitude relationship was preserved.

## Full-day result

Usable one-minute windows:

**1,439**

The local H-D trajectories showed a persistent preferred rotational relationship throughout the analysed day.

The geometry analysis also showed a preferred local orientation and a predominantly elliptical rather than purely linear H-D relationship.

The result should be interpreted as **local two-component polarization geometry**.

It is not a direct image of the global shape of the proposed carrier.

Geometry outputs are stored in:

`results/geometry/`

---

# 5. Time-Shift Null Test

A control experiment was then performed.

The purpose was to determine whether the observed geometry depended on the **actual simultaneous relationship** between H and D, or whether similar results would appear when the two channels were temporally unrelated.

Two analyses were compared.

### Real data

`H(t)` versus `D(t)`

### Null control

`H(t)` versus `D(t + 5 minutes)`

Everything else remained unchanged:

- same source data,
- same frequency interval,
- same filtering,
- same one-minute window length,
- same geometry algorithm.

The comparison used exactly:

**1,434 windows**

for both cases.

## Null-test result

| Quantity | Real H-D | D shifted +5 min |
|---|---:|---:|
| Windows | 1,434 | 1,434 |
| Median PLV | 0.477285 | 0.075219 |
| Median phase difference | 107.993° | -6.922° |
| Median axis ratio | 0.729807 | 0.839053 |
| Median orientation | -28.620° | 0.237° |
| Orientation SD | 25.460° | 35.192° |
| CW windows | 1,434 | 690 |
| CCW windows | 0 | 744 |
| CW fraction | **100.0%** | **48.12%** |
| CCW fraction | **0.0%** | **51.88%** |

The simultaneous H-D pair therefore retained the same rotational sense in:

**1,434 of 1,434 windows.**

After shifting D by five minutes, the directional distribution became approximately balanced:

**48.12% CW / 51.88% CCW**

At the same time, median PLV decreased from:

**0.4773 → 0.0752**

or by a factor of approximately:

**6.35**

This control shows that the observed local organization depends strongly on the real simultaneous H-D relationship.

It is not reproduced when the temporal correspondence of the two components is deliberately broken.

Null-test outputs are stored in:

`results/null-test/`

---

# 6. What Was Measured

The following observations are direct results of the analysis:

1. A blind H-D phase-coherence search identified a dominant region at **6.321–8.267 Hz**.

2. The blind maximum occurred at **7.603 Hz**.

3. Fine refinement placed aggregate maxima near **7.67–7.71 Hz**.

4. The weighted frequency centre was substantially more stable than the instantaneous peak frequency.

5. The simultaneous H-D components showed a persistent local rotational relationship throughout the analysed day.

6. In the matched null-test subset, the real H-D pair showed the same rotational sense in **1,434/1,434 windows**.

7. Shifting D by five minutes reduced median PLV from approximately **0.477 to 0.075** and changed the directional distribution from **100/0** to approximately **48/52**.

These are mathematical results obtained from the institutional magnetometer record.

---

# 7. What Was Not Established

This analysis does **not**, by itself, establish:

- the global geometry of the detected structure,
- that the structure is a scalar standing wave,
- its physical generation mechanism,
- its planetary-scale energy,
- or the carrier interpretation proposed by the Measurable Science model.

In particular, the Istok CDF contains no usable instrumental `phase_difference` calibration values for this record.

The phase-difference field contains only fill values.

Consequently, the reported H-D phase and polarization geometry describe the relationship between the **recorded channels** and are not presented as an independently instrument-phase-corrected absolute polarization measurement.

---

# 8. Model Interpretation

In the Measurable Science model, the blind-detected structure is interpreted as a local measurement of one of four proposed natural electromagnetic carriers.

That interpretation is separate from the institutional measurement and mathematical result.

The evidence chain is therefore kept explicit:

**ISEE measurement**

↓

**blind phase-coherent structure**

↓

**independent frequency refinement**

↓

**local H-D geometry**

↓

**time-shift null test**

↓

**model interpretation**

The institutional source establishes the measurement.

The scripts establish the mathematical analysis.

The carrier interpretation belongs to the Measurable Science model.

---

# 9. Repository Structure

```text
istok-russia/
├── README.md
│
├── references/
│   └── istok_instrument_and_data_sources.md
│
├── scripts/
│   ├── istok_blind_plv_60s.py
│   ├── istok_plv_refined.py
│   ├── istok_parse_calibration.py
│   ├── istok_carrier_shape_fullday.py
│   └── istok_shift_null_test.py
│
└── results/
    ├── blind/
    ├── refinement/
    ├── geometry/
    └── null-test/
```

The exact result filenames within each directory correspond to the outputs generated by the scripts preserved in this repository.

---

# 10. Reproducibility Principle

The analysis was deliberately separated into discovery and testing stages.

The broad frequency search was performed first.

Only after a dominant region had been identified were refinement and geometry analyses applied to that region.

The five-minute time shift was then used as a null test of the observed simultaneous H-D relationship.

The intended principle is simple:

> **Do not tell the program what the model expects. Let the measurement produce the result first, and compare the result with the model afterwards.**

---

# 11. Data Source

Institute for Space-Earth Environmental Research (ISEE), Nagoya University.

**Geomagnetic field variation data measured by a ground induction magnetometer at Istok, Russia.**

Dataset DOI:

https://doi.org/10.34515/DATA.GND-0018-0002-0101_v01

Detailed institutional references, CDF metadata, calibration information, and data-use requirements are documented in:

`references/istok_instrument_and_data_sources.md`