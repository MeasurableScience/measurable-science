# Reference 109 — Glaveja Solar Radiation and ICON-DREAM Analysis

## Purpose

This reference documents the solar-radiation analysis performed for the Glaveja area in Serbia.

The purpose of the analysis was to test whether changes in the local radiation regime occur only under particular solar-geometrical conditions.

An important limitation must be stated at the beginning:

The radiation values used here are not direct field measurements made by an instrument located on Glaveja.

They originate from the Deutscher Wetterdienst (DWD) ICON-DREAM reanalysis system.

For this reason, the analysis is used to identify candidate geometrical transitions, but not to claim an exact measured activation angle.

---

## Official data source

Deutscher Wetterdienst (DWD)

ICON-DREAM Reanalysis

Official dataset:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-EU/

Official dataset description and DOI:

https://opendata.dwd.de/climate_environment/CDC/help/landing_pages/doi_landingpage_ICON-DREAM_v1-en.html

ICON-DREAM is a meteorological reanalysis produced by the German national meteorological service, Deutscher Wetterdienst.

According to DWD, ICON-DREAM is based on the ICON numerical weather-prediction modelling framework.

The European nested domain has a spatial resolution of approximately:

6.5 km

The system combines the numerical model with assimilated meteorological observations.

Therefore, a radiation value extracted for the grid point nearest Glaveja represents a model/reanalysis estimate for that grid cell rather than a direct pyranometer measurement made on the mountain itself.

---

## Radiation parameters

Two DWD parameters were used:

ASWDIR_S

Surface down solar direct radiation

Unit:

W/m²

and:

ASWDIFD_S

Surface down solar diffuse radiation

Unit:

W/m²

The DWD parameter documentation identifies both quantities as surface solar-radiation fields.

For the analysis:

direct = ASWDIR_S

diffuse = ASWDIFD_S

and:

total = direct + diffuse

---

## Glaveja extraction

The grid point used for the extraction was the ICON-DREAM-EU point nearest the Glaveja study area.

The working dataset contains hourly radiation values together with calculated solar geometry:

date

UTC

solar elevation

solar azimuth

solar declination

direct radiation

diffuse radiation

total radiation

The analysed July–October 2010 dataset contains:

2,952 hourly records

The solar angles were added in order to compare changes in radiation with the geometrical position of the Sun.

---

## Observed structure

When the hourly radiation series was compared with solar elevation and azimuth, abrupt changes in the radiation regime appeared under restricted geometrical conditions.

The transitions were not distributed randomly over all solar positions.

They clustered within particular combinations of:

solar elevation

solar azimuth

seasonal position

and time of year.

This made it possible to investigate the hypothesis that a local radiation regime may become active only when particular geometrical conditions are satisfied.

---

## Why an exact activation angle is not claimed

Initial inspection suggested that some transitions could be associated with relatively narrow solar-angle ranges.

However, a more detailed examination showed that the apparent transition times also had a strong relationship with fixed UTC intervals.

This is important because the source is a numerical reanalysis rather than a local radiation instrument.

The ICON-DREAM values are generated within the temporal and spatial structure of the numerical modelling and data-assimilation system.

Consequently, an abrupt transition in the extracted series cannot automatically be interpreted as a physical radiation switch occurring on Glaveja at exactly the calculated solar angle.

For this reason, no exact Kremenac activation angle is claimed from this dataset.

---

## What can be concluded

The analysis supports a more limited observation:

Changes in the extracted radiation regime appear only when particular geometrical and seasonal conditions are satisfied.

This is consistent with the possibility of a restricted working range and therefore provides a useful candidate for further testing.

However:

ICON-DREAM can identify the candidate region of interest.

It cannot, by itself, establish the exact physical activation angle of a local system on Glaveja.

That requires direct field measurements.

---

## Relation to the model

In the model presented in *Measurable Science*, the Kremenac pair is proposed as a phase-dependent part of the local solar system associated with Glaveja.

The proposed sequence is:

global phase
→ local geometrical condition
→ Kremenac working range
→ change in local radiation regime

The ICON-DREAM analysis was used to search for the predicted transition without assuming that the model must be correct.

The appearance of restricted radiation transitions is therefore treated as a clue, not as proof of the proposed mechanism.

A stronger test would require simultaneous local measurements of:

direct solar radiation

diffuse solar radiation

UV radiation

electromagnetic field

solar elevation and azimuth

with precise timestamps.

Such measurements would allow the transition angle to be determined independently of the ICON-DREAM numerical model.

---

## Methodological conclusion

The most important result of this analysis is not a specific angle.

It is the distinction between two observations:

1. Radiation transitions appear within restricted geometrical and seasonal conditions.

2. The available DWD radiation series is model/reanalysis output and therefore cannot determine whether the apparent sharp transition is a real local physical threshold.

The exact activation geometry remains an experimentally testable prediction.

---

## Sources

Deutscher Wetterdienst (DWD)

ICON-DREAM Reanalysis, Version 1

DOI:

10.5676/dwd/icon-dream_v1

DWD ICON-DREAM Open Data:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-EU/

DWD ICON-DREAM Parameter Tables:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-EU/ParameterTables_ICON.pdf