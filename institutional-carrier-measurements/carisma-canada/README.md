# CARISMA Canada — Carrier Structure Analysis

This directory contains a reproducible analysis of publicly available
induction-coil magnetometer measurements from the CARISMA network
(Canadian Array for Realtime Investigations of Magnetic Activity).

The analysis was performed as part of the **Measurable Science** project.

## Purpose

The purpose of this analysis was to test whether a persistent,
phase-organized electromagnetic structure could be independently detected
in measurements produced by a professional scientific magnetometer network.

Five geographically separated CARISMA stations were used:

- FCHU — Fort Churchill
- FSMI — Fort Smith
- ISLL — Island Lake
- MSTK — Ministik Lake
- PINA — Pinawa

The analysis therefore does not depend on a single local instrument or
measurement location.

## Measurement Data

The analysis uses publicly available CARISMA induction-coil magnetometer data.

The analyzed ICM20 data product contains two horizontal magnetic-field
components sampled at:

**20 samples per second (20 Hz)**

with magnetic-field values expressed in:

**picotesla (pT)**

The two induction-coil sensors at each station are orthogonally oriented,
approximately along magnetic North and East.

CARISMA induction-coil magnetometers are designed for measurements of weak
and rapidly varying magnetic fields in the extremely-low-frequency range.

Details of the instruments, data source, and official CARISMA documentation
are provided in:

`references/carisma_instrument_and_data_sources.md`

## Blind Search

The carrier frequency was not supplied to the discovery algorithm.

The initial analysis searched the frequency range without specifying an
expected carrier frequency.

For each analyzed interval, phase relationships between the two horizontal
magnetic components were calculated using the Hilbert phase and
Phase Locking Value (PLV):

PLV = |mean(exp(i * (phi1 - phi2)))|

Statistical thresholds and clustering were then used to identify persistent
frequency structures.

The guiding methodological rule was:

> **The program must not know the result it is expected to find.**

Only after the blind search identified the relevant structure was a finer
frequency analysis performed.

## Five-Station Result

Independent analysis of the five CARISMA stations revealed an organized
structure in approximately the same frequency region.

Individual spectral/phase maxima were not stationary. Their positions
changed between stations and over time.

However, the weighted center of the structure was substantially more stable
than the individual instantaneous peaks and remained close to:

**~7.6 Hz**

The five station profiles were subsequently combined to determine the
frequency structure shared by the network.

## Common Structure

The combined five-station analysis produced a dominant common ridge with:

**Dominant peak: 7.734 Hz**

The compact half-prominence region of this ridge was:

**7.695736 – 7.757423 Hz**

with a width of approximately:

**0.061687 Hz**

The wider prominence-base complex extended approximately from:

**7.475 – 8.169 Hz**

with a total width of:

**0.694 Hz**

These values were obtained from the measured CARISMA data and the analysis
procedures contained in this directory.

They were not entered into the algorithms as expected frequencies.

## Interpretation

The measured result is not a single perfectly stationary narrow frequency
line.

Instead, the analysis identifies a broader organized structure in which
local maxima can move while the center of the structure remains considerably
more stable.

In the **Measurable Science** model, this structure is interpreted as a
natural electromagnetic **carrier**.

The term **carrier** is the terminology and interpretation of the
Measurable Science model.

CARISMA measures magnetic-field variations and does **not** identify or
describe this structure as a "carrier."

This distinction is important:

**CARISMA provides the instruments and measurements.**

**The carrier identification results from the analysis presented here.**

## Reproducibility

The purpose of this directory is to preserve the complete path from
independent measurement to reported result.

The directory is organized as:

```text
carisma-canada/
├── README.md
├── references/
│   └── carisma_instrument_and_data_sources.md
├── scripts/
└── results/
    ├── blind/
    ├── station-refinement/
    └── common-structure/