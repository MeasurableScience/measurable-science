# Istok Induction Magnetometer — Instrument and Data Sources

## 1. Station

**Station:** Istok  
**Station code:** IST  
**Country:** Russia  
**Geographic latitude:** 70.03° N  
**Geographic longitude:** 88.01° E  
**Geomagnetic latitude:** 60.6°  
**Geomagnetic longitude:** 166.6°  
**L value:** 4.07  

The station is part of the ground-based induction magnetometer network operated by the Institute for Space-Earth Environmental Research (ISEE), Nagoya University, in collaboration with the Institute of Solar-Terrestrial Physics, Siberian Branch of the Russian Academy of Sciences.

For the period analysed in this study, the station used an induction magnetometer sampled at 64 Hz.

The CDF metadata identifies the magnetometer type as:

> Induction

and the data type as:

> Time Derivative

The sampling was synchronized by a GPS clock:

> 64Hz sampling triggered by GPS clock signal

The recorded horizontal components are H and D.

The CDF metadata gives their positive directions as:

> positive = northward, eastward

---

## 2. Dataset

The dataset used here is the ISEE ground-based induction magnetometer dataset for Istok, Russia.

Official dataset:

**Geomagnetic field variation data measured by a ground induction magnetometer at Istok, Russia**

DOI:

**10.34515/DATA.GND-0018-0002-0101_v01**

Institute for Space-Earth Environmental Research (ISEE), Nagoya University.

Official dataset documentation:

https://www.isee.nagoya-u.ac.jp/doi/10.34515/DATA_GND-0018-0002-0101_v01.html

ISEE magnetometer network:

http://stdb2.isee.nagoya-u.ac.jp/magne/

---

## 3. File Used in the Analysis

The principal CDF file used for the analysis documented in this repository was:

`isee_induction_ist_2017032800_v01.cdf`

The internal CDF metadata identifies it as:

`ISEE_INDUCTION_IST_2017032800_V01`

Station:

`Istok`

Station code:

`IST`

Observation date:

**2017-03-28**

Start:

**2017-03-28 00:00:00 UTC**

End:

**2017-03-28 23:59:45.984375 UTC**

Time resolution:

**1/64 s**

The file contains:

**5,528,704 samples**

The measured median sample interval was:

**0.015625 s**

corresponding exactly to:

**64 Hz**

The file therefore contains almost one complete UTC day of high-frequency induction magnetometer observations.

---

## 4. CDF Variables

The CDF contains the following relevant variables:

- `epoch_db_dt`
- `db_dt`
- `frequency`
- `sensitivity`
- `phase_difference`

The `db_dt` variable has three array columns in the CDF structure, while the station metadata specifies two active measurement channels.

The analysis therefore uses the two horizontal measured components:

- H
- D

The third array column is not used in the analysis.

The `db_dt` variable is stored in:

**V**

The CDF identifies it as:

`dB_dt`

with a time resolution of 1/64 s.

---

## 5. Instrument Sensitivity

The global CDF metadata gives the quick sensitivity as:

**0.1 V/nT at 1 Hz**

However, the dataset documentation explicitly distinguishes between frequencies below and above approximately 1 Hz.

For frequencies below approximately 1 Hz, the metadata states:

> dB/dt (nT/s) = data (V) / quick_sensitivity

For frequencies above approximately 1 Hz, the metadata instructs the user to apply the exact sensitivity curve to obtain the absolute amplitude of waves.

The CDF therefore contains a dedicated frequency-dependent calibration table:

- `frequency`
- `sensitivity`

The sensitivity variable is expressed in:

**V/nT**

For the analysed carrier region, the CDF calibration table gives:

| Frequency | H sensitivity | D sensitivity |
|---:|---:|---:|
| 5 Hz | 0.1 V/nT | 0.1 V/nT |
| 6 Hz | 0.1 V/nT | 0.1 V/nT |
| 7 Hz | 0.1 V/nT | 0.1 V/nT |
| 8 Hz | 0.1 V/nT | 0.1 V/nT |
| 9 Hz | 0.1 V/nT | 0.1 V/nT |
| 10 Hz | 0.1 V/nT | 0.1 V/nT |

The response stored in this CDF is therefore flat across the frequency region used in the present carrier analysis.

For absolute magnetic-wave amplitude in this range, the conversion represented by the CDF calibration is:

`B [nT] = signal [V] / 0.1 [V/nT]`

---

## 6. Instrumental Phase Calibration

The CDF contains a variable named:

`phase_difference`

with units of degrees.

However, for this Istok file all entries in this variable are equal to the CDF fill value:

`-1 × 10^31`

Consequently, no usable frequency-dependent instrumental phase correction is available from this file.

This is an important limitation for the geometry analysis.

The H-D phase relationships reported in this repository are therefore measured phase relationships between the recorded H and D channels and are **not corrected using an independent instrumental phase-response calibration**.

This limitation must be retained when interpreting absolute polarization angles or phase differences.

---

## 7. Blind Carrier Search

The carrier region used in the subsequent Istok analyses was not inserted into the search algorithm as an expected frequency.

A blind phase-coherence search was performed on the H-D pair.

The scan began at 1 Hz with a frequency increment of:

**0.001 Hz**

The algorithm independently determined its statistical threshold and grouped adjacent frequencies exceeding that threshold.

The dominant phase-coherent structure was:

**6.321–8.267 Hz**

with a blind-search maximum at:

**7.603 Hz**

Peak mean PLV:

**0.539361**

Integrated PLV score:

**94,838.911**

The structure was classified algorithmically as a:

**Phase Coherent Band**

Other smaller coherent regions were also detected by the blind search, but the 6.321–8.267 Hz structure was strongly dominant in the resulting integrated score.

The frequency interval used in later geometry analysis therefore originates from the blind search result rather than from a manually inserted expected carrier frequency.

---

## 8. Frequency Refinement

After the blind search identified the dominant region, a finer analysis was performed within the detected region.

The refinement used:

- H-D components
- 64 Hz sampling
- actual CDF UTC epochs
- fixed 60-second windows
- 6.3–8.5 Hz refinement range
- 0.001 Hz frequency step
- fourth-order Butterworth band-pass filters
- 0.1 Hz analysis bandwidth
- Hilbert-transform phase
- phase-locking value (PLV)

No expected carrier frequency was supplied to the refinement algorithm.

The refined aggregate results were:

**Mean-profile maximum:** 7.667 Hz  
**Mean PLV at maximum:** 0.650972

**Median-profile maximum:** 7.708 Hz  
**Median PLV at maximum:** 0.718406

Aggregate weighted centres were:

**Mean-profile weighted centre:** 7.625890 Hz  
**Median-profile weighted centre:** 7.567168 Hz

The hourly instantaneous peak frequency was substantially more variable than the hourly weighted centre.

Hourly peak frequency standard deviation:

**0.610312 Hz**

Hourly weighted-centre standard deviation:

**0.104090 Hz**

Thus, by this measure, the weighted centre was approximately:

**5.9 times more stable**

than the instantaneous hourly peak.

This distinction is important because the detected structure behaves as a broad phase-organized region rather than as a perfectly fixed narrow radio-frequency line.

---

## 9. Local H-D Geometry

The detected 6.321–8.267 Hz region was subsequently analysed for local two-component H-D geometry.

The full daily record was filtered continuously before subdivision into one-minute analysis windows.

A common normalization factor was applied to H and D so that the physical H:D amplitude relationship was preserved.

For each usable minute the analysis calculated:

- H-D phase-locking value
- H-D phase difference
- PCA major and minor axes
- minor/major axis ratio
- local major-axis orientation
- signed H-D trajectory area
- clockwise/counter-clockwise rotation

The full-day analysis produced:

**1,439 usable one-minute windows**

The observed H-D relationship showed a persistent preferred rotational sense throughout the analysed day.

Because the CDF does not provide usable instrumental phase-correction values, these results describe the geometry of the recorded H-D channels and should not be interpreted as an independently phase-calibrated absolute polarization measurement.

---

## 10. Five-Minute Time-Shift Null Test

A time-shift control was performed to determine whether the observed H-D organization depended on the simultaneous relationship between the two recorded components.

Two otherwise identical analyses were compared:

**Real pair**

`H(t)` versus `D(t)`

and:

**Time-shifted control**

`H(t)` versus `D(t + 5 minutes)`

Both tests used the same:

- source file
- carrier frequency interval
- filtering method
- one-minute windows
- geometry algorithm

Only the temporal relationship between H and D was changed.

Using the same 1,434 windows in both tests, the results were:

| Quantity | Real H-D | D shifted +5 min |
|---|---:|---:|
| Windows | 1,434 | 1,434 |
| Median PLV | 0.477285 | 0.075219 |
| Median phase difference | 107.993° | -6.922° |
| Median axis ratio | 0.729807 | 0.839053 |
| Median orientation | -28.620° | 0.237° |
| Orientation SD | 25.460° | 35.192° |
| CW | 1,434 | 690 |
| CCW | 0 | 744 |
| CW fraction | 100.0% | 48.12% |
| CCW fraction | 0.0% | 51.88% |

The real simultaneous H-D data therefore produced one rotational sense in all 1,434 analysed windows.

After the D channel was shifted by five minutes, the directional distribution became approximately balanced between clockwise and counter-clockwise rotation, while median PLV decreased from approximately 0.477 to 0.075.

This control demonstrates that the observed local H-D organization depends strongly on the actual simultaneous relationship between the two recorded components.

It does **not**, by itself, establish the global geometry, physical origin, or interpretation of the detected structure.

---

## 11. Measurement and Interpretation

The institutional dataset establishes that magnetic-field variations were recorded at Istok using a 64 Hz induction magnetometer.

The analysis in this repository establishes that a blind H-D phase-coherence search identifies a dominant structure in the 6.321–8.267 Hz region and that the simultaneously recorded H and D components exhibit a reproducible local phase and rotational relationship within that region.

The term **carrier** is the terminology used in the Measurable Science model for the structure extracted by this analysis.

ISEE does not identify this structure as a "carrier", nor do the institutional measurements by themselves establish the global carrier interpretation proposed in the model.

The distinction is therefore:

**Institutional measurement:** recorded induction-magnetometer H-D data.

**Mathematical result:** blind phase-coherent band, refined frequency organization, local H-D geometry, and time-shift control.

**Model interpretation:** the detected structure is interpreted as a local measurement of a natural carrier proposed by the Measurable Science model.

These levels should not be conflated.

---

## 12. Reproducibility

The repository preserves the analysis in separate stages:

`results/blind/`

Blind frequency discovery.

`results/refinement/`

Fine frequency refinement.

`results/geometry/`

Full-day local H-D geometry.

`results/null-test/`

Five-minute H-D time-shift control.

Corresponding analysis scripts are stored in:

`scripts/`

The original institutional CDF data should be obtained from the official ISEE source rather than treated as data generated by this repository.

---

## 13. Primary References

Shiokawa, K., Nomura, R., Sakaguchi, K., Otsuka, Y., Hamaguchi, Y., Satoh, M., Katoh, Y., Yamamoto, Y., Shevtsov, B. M., Smirnov, S., Poddelsky, I., & Connors, M. (2010).

**The STEL induction magnetometer network for observation of high-frequency geomagnetic pulsations.**

*Earth, Planets and Space*, 62(6), 517–524.

DOI:

https://doi.org/10.5047/eps.2010.05.003


Institute for Space-Earth Environmental Research (ISEE), Nagoya University.

**Geomagnetic field variation data measured by a ground induction magnetometer at Istok, Russia.**

Dataset DOI:

https://doi.org/10.34515/DATA.GND-0018-0002-0101_v01


ISEE Ground-Based Magnetometer Network:

http://stdb2.isee.nagoya-u.ac.jp/magne/