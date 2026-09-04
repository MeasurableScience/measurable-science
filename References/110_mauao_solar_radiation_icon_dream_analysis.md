# Mauao Solar Radiation — ICON-DREAM Global Analysis

## Purpose

This reference documents the extraction of hourly solar-radiation data for Mauao (Mount Maunganui), New Zealand, from the Deutscher Wetterdienst (DWD) ICON-DREAM-Global reanalysis.

The purpose is to make the analysis reproducible.

The repository contains:

- the Python extraction script;
- the processed January 2010 CSV;
- the processed July 2010 CSV;
- the combined January–July CSV;
- links and exact filenames for the original DWD source data.

The original multi-gigabyte DWD GRIB and grid files are not stored in this repository.

---

## Target location

Mauao summit:

- Latitude: **−37.63030°**
- Longitude: **176.17198°**

The extraction script reads the native ICON-DREAM-Global grid and automatically selects the grid cell nearest to this coordinate.

The selected grid point and its distance from Mauao are printed by the script when it is executed.

---

## Data source

Source:

**Deutscher Wetterdienst (DWD) — ICON-DREAM-Global**

Main dataset directory:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-Global/

ICON-DREAM-Global is provided on the native ICON global grid with an approximate horizontal resolution of **13 km**.

The data are organized by temporal resolution and parameter. Monthly GRIB files are available inside the corresponding parameter directories.

For this analysis, hourly surface solar-radiation fields were used.

---

## Radiation parameters

Two DWD parameters are required.

### ASWDIR_S

**Surface down solar direct radiation**

Unit:

**W/m²**

Hourly directory:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-Global/hourly/ASWDIR_S/

### ASWDIFD_S

**Surface down solar diffuse radiation**

Unit:

**W/m²**

Hourly directory:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-Global/hourly/ASWDIFD_S/

The total radiation used in the processed CSV files is calculated as:

**total = direct + diffuse**

---

## Original files required

Download the following four hourly GRIB files from DWD.

### January 2010

Direct radiation:

`ICON-DREAM-Global_201001_ASWDIR_S_hourly.grb`

Diffuse radiation:

`ICON-DREAM-Global_201001_ASWDIFD_S_hourly.grb`

### July 2010

Direct radiation:

`ICON-DREAM-Global_201007_ASWDIR_S_hourly.grb`

Diffuse radiation:

`ICON-DREAM-Global_201007_ASWDIFD_S_hourly.grb`

These files are large and are therefore not duplicated in this GitHub repository.

They can be downloaded directly from the DWD hourly parameter directories listed above.

---

## ICON-DREAM-Global grid

The native ICON grid is also required because the GRIB values are stored according to the ICON grid-cell ordering.

Download:

`ICON-DREAM-Global_grid.nc`

from:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-Global/invariant/

Direct grid file:

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-Global/invariant/ICON-DREAM-Global_grid.nc

The extraction script reads the `clat` and `clon` cell-centre coordinates from this file and finds the cell nearest to Mauao.

No grid cell is manually selected to obtain a preferred radiation result.

---

## Repository files

All files belonging to this analysis are stored in:

`SunRadiation/`

The relevant files are:

```text
SunRadiation/
├── 110_mauao_solar_radiation_icon_dream_analysis.md
├── mauao_radiation.py
├── mauao_januar_2010.csv
├── mauao_jul_2010.csv
└── mauao_januar_jul_2010_sa_stepenima.csv