# CARISMA Induction-Coil Magnetometer Data

## Institutional source

CARISMA (Canadian Array for Realtime Investigations of Magnetic Activity)
is the magnetometer component of the Geospace Observatory Canada program.

The array is operated by the University of Alberta and is funded by the
Canadian Space Agency.

Official CARISMA website:

https://www.carisma.ca/

CARISMA data repository:

https://www.carisma.ca/carisma-data-repository


## Induction-coil magnetometers

CARISMA operates induction-coil magnetometers (ICMs) at several stations
within the array.

Each ICM site contains two orthogonal induction coils aligned approximately
with magnetic North and magnetic East.

The sensors are installed in buried enclosures on gravel beds for drainage
and mechanical stability.

The induction-coil magnetometers are connected to a 24-bit data acquisition
system with GPS timing.

The CARISMA documentation states that the instruments are sampled internally
at 100 samples per second.

Official instrument documentation:

https://carisma.ca/backgrounder/carisma-induction-coils


## Frequency response

CARISMA describes the induction-coil system as operating over approximately:

0.001–30 Hz

The response above 1 Hz is approximately flat due to active feedback and
filtering.

CARISMA gives a transformation factor above 1 Hz of:

20 mV/nT

The published magnetic noise levels include approximately:

- <= 20 pT/sqrt(Hz) at 0.01 Hz
- <= 2 pT/sqrt(Hz) at 0.1 Hz
- <= 0.2 pT/sqrt(Hz) at 1 Hz
- <= 0.04 pT/sqrt(Hz) at 10 Hz

These specifications place the frequency region examined in this analysis
within the intended operating range of the instruments.


## Data product used in this analysis

The analysis in this directory uses the CARISMA ICM20 data product.

The Canadian Space Agency documentation describes the 20 Hz ICM product as:

- two-component horizontal magnetic field
- sampling rate: 20 Hz
- resolution: 0.05 pT
- ASCII format

CARISMA also provides documentation for its ICM data format and states that
ICM data are available in ASCII and CDF formats.

Official CARISMA ICM data-format documentation:

https://carisma.ca/carisma-data/icm-data-format

Canadian Space Agency Geospace Observatory Canada documentation:

https://www.asc-csa.gc.ca/eng/funding-programs/funding-opportunities/ao/2014-ss-go-science.asp


## Stations used

Five CARISMA stations equipped with induction-coil magnetometers were used
in this analysis:

| Code | Station | Geodetic Latitude | Geodetic Longitude |
|------|---------|------------------:|-------------------:|
| FCHU | Fort Churchill | 58.763 N | 265.920 E |
| FSMI | Fort Smith | 60.017 N | 248.050 E |
| ISLL | Island Lake | 53.856 N | 265.340 E |
| MSTK | Ministik Lake | 53.351 N | 247.026 E |
| PINA | Pinawa | 50.199 N | 263.960 E |

Equivalent west longitudes are approximately:

- FCHU: 94.080 W
- FSMI: 111.950 W
- ISLL: 94.660 W
- MSTK: 112.974 W
- PINA: 96.040 W

Official CARISMA station information:

https://carisma.ca/station-information

CARISMA explicitly lists FCHU, FSMI, ISLL, MSTK and PINA among the sites
equipped with induction-coil magnetometers.


## Public availability and reproducibility

CARISMA provides a public data repository and an alternate data tree for
access to its measurements.

Access to the repository is free, although registration may be required for
the main repository interface.

The purpose of using these data in the Measurable Science analysis is to
allow the measurement source to remain independent of the proposed model.

The original measurements were produced by CARISMA independently of this
project.

The analysis can therefore be repeated by obtaining the corresponding
CARISMA measurements and running the scripts provided in this repository.


## Data-use acknowledgement

CARISMA specifies an acknowledgement for work produced using its data:

> The authors thank I.R. Mann, D.K. Milling and the rest of the CARISMA
> team for data. CARISMA is operated by the University of Alberta,
> funded by the Canadian Space Agency.

CARISMA data-use requirements:

https://carisma.ca/carisma-data/data-use-requirements


## Recommended CARISMA reference

CARISMA requests that users cite the following reference paper:

Mann, I. R., et al. (2008).

**The Upgraded CARISMA Magnetometer Array in the THEMIS Era.**

Space Science Reviews, 141, 413–451.

DOI:

https://doi.org/10.1007/s11214-008-9457-6

CARISMA-hosted copy:

https://www.carisma.ca/PDFDocs/CARISMAReference.pdf


## Interpretation boundary

CARISMA provides the magnetometers, measurement infrastructure and
measurement data used in this analysis.

CARISMA does not identify the frequency structure reported by the
Measurable Science analysis as a "carrier."

The term **carrier**, its proposed geometry, and its physical interpretation
belong to the Measurable Science model.

This distinction is maintained throughout the accompanying analysis:

**institutional measurement -> reproducible analysis -> model interpretation**