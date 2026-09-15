# Kunigami, Japan — Blind Carrier and H–D Phase-Geometry Analysis

## Overview

This directory contains an independent analysis of 64 Hz ground induction magnetometer data from Kunigami (KNG), Japan.

The analysis was designed around a strict methodological rule:

> The program must not know the expected result.

The carrier frequency was therefore not inserted into the initial search. The analysis began with a blind scan across 1–10 Hz using the two independently recorded horizontal magnetic components, H and D.

Only after a candidate frequency region had emerged from the blind analysis was that region examined at higher frequency resolution and subjected to geometric and control tests.

The complete analysis chain was:

**RAW CDF AUDIT → BLIND FREQUENCY SEARCH → FREQUENCY REFINEMENT → FULL-DAY H–D SHAPE → HARMONIC SHAPE TEST → CYCLE-RESOLVED SHAPE → SYNTHETIC ELLIPSE NULL**

The principal blind-selected candidate was:

**7.9–8.1 Hz**

The subsequent analyses investigated the stability, temporal occurrence, phase organization, and H–D geometry associated with this frequency region.

---

## 1. Station and Data

**Station:** Kunigami (KNG)  
**Country:** Japan  
**Coordinates:** 26.7567° N, 128.208° E  
**Date analyzed:** 2022-01-01  
**Sampling rate:** 64 Hz  
**Files:** 24 hourly CDF files  
**Total nominal samples:** 5,529,600

The data were obtained from the Institute for Space-Earth Environmental Research (ISEE), Nagoya University.

The dataset is identified by:

**DOI:** `10.34515/DATA.GND-0063-0002-0101_v01`

Official dataset title:

> Geomagnetic field variation data measured by a ground induction magnetometer at Kunigami, Japan

The CDF files contain three nominal induction channels:

- `dH/dt`
- `dD/dt`
- `dZ/dt`

The analysis presented here uses the two horizontal channels H and D.

The Z channel in the examined files contained the CDF fill value and was therefore not used.

No observation time was inferred solely from the CDF filename. Actual timestamps stored in `epoch_db_dt` were used when selecting analysis windows.

---

## 2. Raw CDF Audit

Before any filtering, PLV calculation, carrier search, or shape analysis, all 24 hourly CDF files were inspected directly using:

`scripts/isee_cdf_raw_audit.py`

The audit intentionally contains:

- no expected carrier frequency,
- no band-pass filtering,
- no PLV calculation,
- no frequency selection,
- no geometric reconstruction.

Each hourly file contained:

**230,400 samples × 3 nominal channels**

which is consistent with one hour sampled at 64 Hz:

`3600 × 64 = 230,400`

The nominal Epoch sampling interval was:

**15,625 µs**

corresponding to:

**64.000000 Hz**

The actual first timestamp of the analyzed daily sequence was:

`2021-12-31T23:59:57.770000`

and the final timestamp was:

`2022-01-01T23:59:57.964375`

The audit also compared `epoch_db_dt` with `time_db_dt` at selected samples. The inspected timestamps agreed exactly.

The predefined UTC minute-30 windows contained 3,839–3,840 samples depending on the exact Epoch alignment.

H and D were confirmed to be distinct recorded channels rather than exact copies or sign-reversed duplicates.

The Z channel consisted of the CDF fill value and was excluded from all subsequent analysis.

The raw audit therefore established the timing, sampling, channel identity, and usable H/D input before any carrier analysis was performed.

---

## 3. Blind Frequency Search

Script:

`scripts/kunigami_blind_frequency_search.py`

The first frequency analysis was deliberately blind.

### Search parameters

- Frequency range: **1.0–10.0 Hz**
- Frequency step: **0.1 Hz**
- Sampling rate: **64 Hz**
- Window length: **60 s**
- Window position: **minute 30 of every UTC hour**
- Number of hourly observations: **24**
- Components: **H and D**
- Filter: fourth-order Butterworth band-pass
- Total filter bandwidth: **0.4 Hz**
- Phase estimator: Hilbert transform
- Metric: Phase Locking Value (PLV)

For every frequency tested, the instantaneous H and D phases were obtained from the analytic signals and their phase locking was measured as:

`PLV = |mean(exp(i * (phase_H - phase_D)))|`

The program contained no 7.9 Hz, 8.0 Hz, 8.1 Hz, or other expected carrier frequency.

### Dynamic detection criterion

For each hourly frequency profile, the detection threshold was calculated from that profile itself:

`threshold = max(0.30, median(PLV) + 2 × MAD(PLV))`

Candidate frequencies therefore had to rise above a dynamically estimated background rather than a threshold chosen for a particular expected frequency.

Passing frequency bins were accumulated across the 24 hourly observations and contiguous active regions were identified.

---

## 4. Blind Result

The blind search identified several frequency structures across 1–10 Hz.

Among them, a compact candidate occurred at:

**7.9–8.1 Hz**

with:

- blind peak frequency: **7.9 Hz**
- peak mean PLV across the 24 hourly observations: **0.236945**
- individual hourly PLV values within the 7.9–8.1 Hz candidate region reaching approximately **0.457**
- classification: **Sharp Carrier Peak**

At exactly 7.9 Hz:

- mean PLV: **0.236945**
- median PLV: **0.223510**
- maximum hourly PLV: **0.404139**

Within the complete 7.9–8.1 Hz region, the largest individual hourly PLV was:

**0.456806 at 8.0 Hz**

If the maximum of 7.9, 8.0, and 8.1 Hz is selected independently for each sampled hour, the mean hourly regional maximum is approximately:

**0.284**

### Temporal coverage

An important distinction must be made between the existence of measurable phase organization and crossing the blind detection threshold.

The 7.9–8.1 Hz region was measurable in all:

**24 / 24 hourly observations**

during the analyzed day.

However, individual bins exceeded the deliberately strict blind detection criterion only intermittently:

- 7.9 Hz: 7 threshold-passing hourly observations
- 8.0 Hz: 5 threshold-passing hourly observations
- 8.1 Hz: 6 threshold-passing hourly observations

Therefore these counts should not be interpreted as the carrier existing for only those hours.

They describe threshold crossings — periods of comparatively strong phase organization — rather than the temporal existence of the frequency region itself.

Because the blind experiment sampled one predefined 60-second interval per hour, the correct statement is that the region was measurable in all 24 sampled hours. This analysis alone does not establish continuous presence during every second of the 24-hour period.

---

## 5. Frequency Refinement

Script:

`scripts/kunigami_frequency_refinement.py`

After the blind analysis had been completed, a higher-resolution frequency scan was performed.

This was a refinement test, not a new blind discovery experiment.

### Refinement parameters

- Frequency range: **6.5–8.5 Hz**
- Frequency step: **0.001 Hz**
- Filter bandwidth: **0.1 Hz**
- Filter order: **4**
- Window length: **60 s**
- Window position: **minute 30**
- Hourly observations: **24**
- Components: **H and D**
- Metric: Hilbert PLV

For each hourly observation, two frequency estimators were retained:

1. the frequency of the highest PLV point;
2. a weighted center describing the broader elevated PLV structure.

### Refinement results

Aggregate peak of the mean PLV profile:

**7.896 Hz**

Aggregate peak of the median PLV profile:

**7.523 Hz**

Weighted center of the mean aggregate profile:

**7.409204 Hz**

Weighted center of the median aggregate profile:

**7.440591 Hz**

The dispersion of the hourly maximum-frequency estimator was:

**STD = 0.571588 Hz**

The dispersion of the hourly weighted-center estimator was:

**STD = 0.119880 Hz**

Therefore:

`0.571588 / 0.119880 ≈ 4.77`

The weighted center was approximately:

**4.77 times more stable**

than the instantaneous hourly maximum-frequency estimator.

This distinction is important because the strongest instantaneous PLV bin can move substantially while the broader organized frequency structure remains considerably more stable.

The refinement result is therefore not interpreted as a perfectly stationary narrow spectral line.

---

## 6. Full-Day H–D Phase Geometry

Script:

`scripts/kunigami_blind_shape_fullday.py`

After the frequency region had been selected by the blind search, the H–D relationship inside the frozen:

**7.9–8.1 Hz**

region was examined geometrically.

The frequency band was not broadened in order to obtain a desired shape.

A total of:

**1,440 non-overlapping 60-second windows**

were analyzed.

For each window, the filtered H and D signals were treated as a two-dimensional trajectory.

The analysis examined:

- H–D PLV,
- relative H–D phase,
- PCA axis ratio,
- rotation direction,
- angular harmonic structure.

### Full-day shape statistics

Median PLV:

**0.235087**

Median phase difference D−H:

**10.830°**

Median PCA axis ratio:

**0.762273**

Rotation counts:

- clockwise: **745**
- counter-clockwise: **695**

or:

- CW: **51.74%**
- CCW: **48.26%**

No persistent single rotation direction was therefore found in the full-day 60-second reconstruction.

---

## 7. Harmonic Shape Analysis

The angular geometry of the reconstructed H–D trajectories was examined using harmonic components.

Median harmonic amplitudes were:

- m1 = **0.001911**
- m2 = **0.087414**
- m3 = **0.001965**
- m4 = **0.054220**
- m5 = **0.001939**
- m6 = **0.038338**

The dominant harmonic order per 60-second window was:

- m2: **963 windows — 66.88%**
- m4: **368 windows — 25.56%**
- m6: **109 windows — 7.57%**

Odd-order components were nearly absent from the dominant-window classification.

The reconstruction visually appeared strongly flattened and approximately quadrilateral-like.

However, visual appearance alone was not accepted as sufficient evidence for a unique geometric classification.

---

## 8. Flattened-Quadrilateral Test

Script:

`scripts/kunigami_flattened_quadrilateral_test.py`

Because the reconstructed trajectory appeared flattened and approximately quadrilateral-like, the relationship between the second- and fourth-order angular components was examined explicitly.

The analysis tested the coexistence of:

- A2 — twofold organization
- A4 — fourfold geometric contribution

A fourth-order component was present, but the relative orientation between the A2 and A4 components was not stably locked across the complete dataset.

The m4 orientation concentration was:

**0.041063**

This prevented a claim that the signal represented a uniquely stable quadrilateral geometry.

The result motivated a more stringent cycle-resolved analysis.

---

## 9. Cycle-Resolved Shape Analysis

Script:

`scripts/kunigami_cycle_shape.py`

The 60-second windows contain hundreds of oscillation cycles. A long-window trajectory can therefore obscure the geometry of individual cycles.

The selected frequency region was consequently analyzed cycle by cycle.

Total detected cycles:

**691,133**

Usable cycles:

**691,113**

Cycles were grouped in sets of:

**16 cycles per group**

producing:

**43,194 usable groups**

### Cycle-resolved results

Median PCA axis ratio:

**0.289825**

Median A2:

**0.284080**

Median A4:

**0.122290**

Median A4/A2:

**0.431722**

Dominant harmonic classification:

**m2: 42,693 / 43,194 groups**

or:

**98.84%**

This is substantially stronger twofold organization than was visible in the longer 60-second trajectory analysis.

The cycle-resolved trajectory is therefore strongly flattened and overwhelmingly dominated by m=2 symmetry.

However:

> m=2 describes symmetry order; it does not uniquely identify geometric shape.

A highly flattened ellipse can also produce strong m=2 organization.

For this reason, a synthetic geometric null test was performed.

---

## 10. Synthetic Ellipse Null Control

Script:

`scripts/kunigami_synthetic_shape_null.py`

The purpose of this control was to determine whether the observed A4 and A4/A2 values uniquely distinguish the real trajectory from an ordinary strongly flattened ellipse.

The null simulation generated:

**100,000 synthetic ellipses**

No quadrilateral deformation or m4 component was deliberately inserted into the synthetic shapes.

### Real Kunigami values

- axis ratio: **0.289825**
- A2: **0.284080**
- A4: **0.122290**
- A4/A2: **0.431722**

### Full synthetic ellipse population

Median synthetic values:

- A2: **0.291524**
- A4: **0.124613**
- A4/A2: **0.427455**

### Axis-matched synthetic subset

Synthetic ellipses with approximately matching flattening:

**axis ratio = 0.290 ± 0.020**

Number of matched synthetic cases:

**6,626**

Median values:

- axis ratio: **0.289454**
- A2: **0.285578**
- A4: **0.119694**
- A4/A2: **0.419128**

The real Kunigami A4 value was at approximately the:

**61.73rd percentile**

of the synthetic ellipse distribution.

The real A4/A2 ratio was at approximately the:

**83.07th percentile**

of the synthetic ellipse distribution.

### Interpretation of the null control

The control produced an important negative result.

The A4 and A4/A2 statistics used here are not sufficient to distinguish a strongly flattened quadrilateral-like trajectory from a strongly flattened ellipse.

Therefore the synthetic control:

- does **not** prove that the observed trajectory is an ellipse;
- does **not** disprove the quadrilateral-like visual appearance;
- does show that the present A4/A2 metric cannot uniquely classify the geometry.

The strongest supported geometric conclusion is therefore:

> The blind-selected 7.9–8.1 Hz H–D trajectory is strongly flattened and strongly twofold-organized. Cycle-resolved analysis gives a median axis ratio of approximately 0.29 and m=2 dominance in 98.84% of usable cycle groups. The reconstructed trajectory visually exhibits flattened quadrilateral-like characteristics, but the A4/A2 statistic used here cannot uniquely distinguish such a shape from a strongly flattened ellipse.

---

## 11. What Was Blind and What Was Not

The chronological order of the analysis is important.

### Blind stage

The original search:

- scanned 1–10 Hz;
- used 0.1 Hz frequency steps;
- contained no expected carrier frequency;
- calculated H–D PLV;
- calculated its threshold from the observed frequency profile;
- identified candidate regions from the data.

The 7.9–8.1 Hz candidate therefore existed before the geometric analysis.

### Post-selection stages

Only after the blind result was frozen were the following performed:

- 0.001 Hz frequency refinement;
- H–D trajectory reconstruction;
- harmonic decomposition;
- flattened-quadrilateral testing;
- cycle-resolved geometry;
- synthetic ellipse null testing.

These later analyses must not be described as independent blind discoveries of the carrier frequency.

They are tests of a frequency region selected by the preceding blind experiment.

---

## 12. Main Experimental Findings

The analysis supports the following observations.

1. A blind H–D PLV scan across 1–10 Hz independently identified a compact candidate region at **7.9–8.1 Hz**.

2. The blind peak occurred at **7.9 Hz**, with a mean PLV of **0.236945** across the 24 hourly observations.

3. Individual hourly PLV values inside the candidate region reached approximately **0.457**.

4. The 7.9–8.1 Hz region was measurable in **all 24 sampled hours**, although the strict blind threshold was exceeded only intermittently.

5. High-resolution refinement produced an aggregate mean-profile maximum at **7.896 Hz**.

6. The weighted frequency center varied substantially less than the instantaneous hourly maximum: **0.119880 Hz versus 0.571588 Hz STD**, a stability ratio of approximately **4.77**.

7. Full-day H–D reconstruction showed a flattened trajectory containing predominantly even-order geometric organization.

8. Cycle-resolved analysis strengthened this result dramatically, producing a median axis ratio of **0.289825** and m=2 dominance in **98.84%** of usable cycle groups.

9. The synthetic ellipse null demonstrated that the current A4/A2 statistic cannot uniquely distinguish the observed flattened quadrilateral-like appearance from a strongly flattened ellipse.

The frequency and phase-organization result is therefore stronger than the unique geometric-classification result.

---

## 13. Interpretation Limits

Several distinctions are intentionally preserved.

The blind PLV result measures phase organization between the independently recorded H and D components. It is not by itself a measurement of electromagnetic energy.

A frequency with high PLV does not necessarily have the largest spectral amplitude.

The 7.9–8.1 Hz structure should not be described as an infinitely narrow stationary spectral line. Its instantaneous maximum changes with time.

Threshold crossings measure comparatively strong episodes of phase organization. They should not be confused with the existence or non-existence of measurable PLV outside those crossings.

The statement that the region was measurable throughout the day refers to all 24 predefined hourly observations. The original blind experiment sampled one 60-second window per hour and therefore does not establish uninterrupted second-by-second detection over the complete 24 hours.

The geometric reconstruction is local to the H–D measurements at Kunigami. It must not be interpreted as a direct image of a global electromagnetic structure.

The synthetic ellipse null specifically prevents a unique quadrilateral classification using the present A4/A2 metric.

No causal relationship with meteorological, geological, biological, or other external phenomena is established by this analysis.

---

## 14. Reproducibility

The analysis scripts are retained in the order in which their scientific roles should be understood:

```text
scripts/
├── isee_cdf_raw_audit.py
├── kunigami_blind_frequency_search.py
├── kunigami_frequency_refinement.py
├── kunigami_blind_shape_fullday.py
├── kunigami_flattened_quadrilateral_test.py
├── kunigami_cycle_shape.py
└── kunigami_synthetic_shape_null.py