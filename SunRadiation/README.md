# Sun Radiation Analysis

This directory contains the data and scripts used for the solar-radiation
tests described in *Measurable Science*.

## Locations

### Glaveja, Serbia

Coordinates:

43.875341° N, 21.080022° E

Source:
DWD ICON-DREAM-EU reanalysis.

Parameters:

- ASWDIR_S — surface downward direct solar radiation
- ASWDIFD_S — surface downward diffuse solar radiation

Processed data:

`data/glaveja/glaveja_jul_oktobar_2010.csv`

### Mauao, New Zealand

Coordinates:

37.63030° S, 176.17198° E

Source:
DWD ICON-DREAM-Global reanalysis.

Parameters:

- ASWDIR_S — surface downward direct solar radiation
- ASWDIFD_S — surface downward diffuse solar radiation

Processed data:

`data/mauao/mauao_january_2010.csv`
`data/mauao/mauao_july_2010.csv`

## Reproducibility

The original DWD files are not stored in this repository because of their
size.

Download links to the original datasets are provided below.

https://opendata.dwd.de/climate_environment/REA/ICON-DREAM-Global/hourly/?utm_source=chatgpt.com

The scripts in `scripts/` reproduce the extraction, solar-position
calculation and analysis used in the book.