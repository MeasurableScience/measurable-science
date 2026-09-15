# Kunigami (KNG) Induction-Magnetometer Data

## Institutional source

The Kunigami induction-magnetometer measurements used in this analysis are provided by the Institute for Space-Earth Environmental Research (ISEE), Nagoya University, Japan.

The dataset is distributed through the ERG Science Center of ISEE, Nagoya University.

Official ISEE magnetometer website:

https://stdb2.isee.nagoya-u.ac.jp/magne/

Official ISEE magnetometer station information:

https://stdb2.isee.nagoya-u.ac.jp/magne/magne_stations.html

## Kunigami induction magnetometer

The station used in this analysis is:

**Kunigami (KNG), Japan**

Geographic coordinates:

* Latitude: 26.7567 N
* Longitude: 128.208 E

ISEE lists routine induction-magnetometer observations at Kunigami beginning on October 23, 2021.

For the Kunigami induction magnetometer, ISEE specifies:

* sampling rate: 64 Hz
* timing: GPS-clock triggered
* turnover frequency: 1.4 Hz for H and D
* H sensitivity: 0.3986 V/nT at 1.4 Hz

Official station and instrument information:

https://stdb2.isee.nagoya-u.ac.jp/magne/magne_stations.html

## Data product used in this analysis

The analysis in this directory uses the official dataset:

**Geomagnetic field variation data measured by a ground induction magnetometer at Kunigami, Japan**

The dataset is provided in CDF (Common Data Format).

Dataset DOI:

https://doi.org/10.34515/DATA.GND-0063-0002-0101_v01

Dataset version:

**v01**

Dataset creators:

* Atsuki Shinbori
* Yuichi Otsuka
* Kazuo Shiokawa

Institution:

Institute for Space-Earth Environmental Research, Nagoya University.

Publisher:

ERG Science Center, Institute for Space-Earth Environmental Research, Nagoya University.

The official dataset contains variations of three geomagnetic components:

* H
* D
* Z

at a sampling rate of 64 Hz, together with engineering parameters associated with the instrument.

The carrier analysis in this repository uses the two horizontal components:

**H and D**

## Instrument response and amplitude calibration

The official dataset documentation distinguishes between measurements below and above approximately 1 Hz.

For frequencies above approximately 1 Hz, the exact instrument sensitivity curve is required when absolute wave amplitudes are to be determined.

The principal carrier-search analysis presented in this directory does not identify the candidate frequency structure from absolute magnetic amplitude.

Instead, the analysis compares the instantaneous phase relationship between the simultaneously measured H and D components using the Hilbert Phase Locking Value (PLV).

The primary detection statistic is therefore a phase-coherence statistic rather than an absolute-amplitude estimate.

Official dataset record:

https://doi.org/10.34515/DATA.GND-0063-0002-0101_v01

## Data interval used in this analysis

The Kunigami analysis presented in this repository uses the complete set of 24 hourly CDF files associated with:

**2022-01-01**

The files range from:

`isee_induction_kng_2022010100_v01.cdf`

through:

`isee_induction_kng_2022010123_v01.cdf`

The combined dataset contains:

**5,529,600 samples**

The analysis does not construct measurement timestamps from the CDF filenames.

Instead, the actual `epoch_db_dt` timestamps stored inside the CDF files are read directly by the analysis software.

For the files used in this analysis, the combined record begins at approximately:

`2021-12-31T23:59:57.770000`

and ends at approximately:

`2022-01-01T23:59:57.964375`

The actual CDF epoch therefore remains the time reference throughout the analysis.

## Analysis sequence and independence of the blind search

The frequency region examined in the later Kunigami geometry analysis was not supplied to the initial discovery program as an expected carrier frequency.

The analysis sequence was:

1. raw CDF structure and timing audit;
2. blind H-D PLV frequency search from 1.0 to 10.0 Hz;
3. identification of statistically organized frequency regions;
4. fine frequency refinement;
5. local H-D geometry analysis inside the previously detected frequency region;
6. cycle-resolved H-D geometry reconstruction;
7. A2/A4 geometry testing;
8. synthetic-ellipse null testing.

The blind frequency search therefore preceded the geometry analysis.

No expected carrier frequency was supplied to the blind search.

Likewise, no square, quadrilateral, ellipse or other expected geometric form was supplied to the initial shape-analysis algorithm.

The geometry tests were performed only after the frequency region had already been identified independently.

## Public availability and reproducibility

The Kunigami measurements used here were produced independently of the Measurable Science project.

The dataset has a persistent DOI and is distributed through the ERG Science Center of ISEE, Nagoya University.

Dataset DOI:

https://doi.org/10.34515/DATA.GND-0063-0002-0101_v01

The original CDF measurements are not duplicated in this GitHub repository.

Instead, this repository records:

* the institutional data source;
* the persistent dataset DOI;
* the station used;
* the exact observation date;
* the original CDF filename pattern;
* the analysis scripts;
* the analysis parameters;
* the derived numerical results;
* the control and null tests.

This allows the original measurements to remain with their institutional provider while preserving a reproducible record of the subsequent analysis.

## Data-use information

The ISEE magnetometer website requests that users contact Kazuo Shiokawa before using ISEE magnetometer data in publications and/or presentations.

Official ISEE magnetometer information:

https://stdb2.isee.nagoya-u.ac.jp/magne/

The institutional source and dataset DOI are therefore identified explicitly throughout this repository.

The original ISEE measurements are kept conceptually separate from the subsequent Measurable Science analysis and interpretation.

## Recommended ISEE induction-magnetometer reference

A principal reference describing the ISEE induction-magnetometer network is:

Shiokawa, K., et al. (2010).

**The ISEE induction magnetometer network for observation of high-frequency geomagnetic pulsations.**

Earth, Planets and Space, 62, 517–524.

DOI:

https://doi.org/10.5047/eps.2010.05.003

## Dataset citation

The Kunigami dataset used in this analysis is:

Shinbori, A., Otsuka, Y., and Shiokawa, K.

**Geomagnetic field variation data measured by a ground induction magnetometer at Kunigami, Japan.**

Institute for Space-Earth Environmental Research, Nagoya University.

ERG Science Center.

Dataset version: v01.

DOI:

https://doi.org/10.34515/DATA.GND-0063-0002-0101_v01

## Interpretation boundary

ISEE and the ERG Science Center provide the magnetometer, measurement infrastructure and measurement data used in this analysis.

ISEE does not identify the frequency structure reported by the Measurable Science analysis as a **carrier**.

The identification of a phase-organized frequency region, the term **carrier**, its proposed geometry, its possible large-scale extent and its physical interpretation belong to the Measurable Science analysis and model.

The local H-D trajectory reconstructed from the Kunigami measurements is also not presented as a direct spatial image of an entire proposed large-scale carrier.

It represents a local two-component measurement obtained at one geographic station.

The measured quantities, computational results and subsequent model interpretation are therefore kept distinct throughout this work:

**institutional measurement -> reproducible analysis -> model interpretation**
