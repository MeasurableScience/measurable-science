# Lunar Spectrum Independent Analysis - OliNo and Ritter Observatory

## Purpose

This reference documents an independent comparison of two publicly available measurements of lunar light with laboratory atomic wavelengths.

The purpose of the analysis was not to search specifically for neon or any other predetermined element. Spectral candidates were first extracted from the measured lunar spectra using fixed criteria. Element identification was performed only afterward.

Two independent observational sources were used:

1. OliNo - Spectrum of Moon Light
2. Ritter Observatory Public Archive - Moon spectra

Laboratory wavelengths were obtained from the NIST Atomic Spectra Database (ASD), Standard Reference Database 78.

The analysis distinguishes between:

* measured spectral features;
* laboratory wavelength compatibility;
* ambiguous matches;
* element-exclusive matches within the tested element set;
* interpretation of those results.

A wavelength match is treated as compatibility with an atomic line, not by itself as proof of the chemical origin of the measured lunar feature.

---

## 1. OliNo lunar spectrum

Marcel van der Steen measured the spectrum of the full Moon on 14 April 2014 using a JETI SpecBos 1211 spectroradiometer.

The instrument was mounted on a tripod and operated in luminance mode while pointed toward the Moon.

The publicly available CSV contains the average of 24 measurements.

Original source:

https://olino.org/blog/us/articles/2015/10/05/spectrum-of-moon-light/

A copy of the dataset used in this analysis is stored with this reference:

`113_data/olino_moon_spectrum.csv`

### Instrument characteristics used in the test

Relevant SpecBos 1211 characteristics:

* spectral range: approximately 350-1000 nm
* wavelength sampling: 1 nm
* optical bandwidth: approximately 4.5 nm FWHM
* wavelength accuracy: +/- 0.5 nm

For direct comparison with laboratory wavelengths, the declared wavelength accuracy was used.

MATCH if:

```
abs(lambda_measured - lambda_NIST) <= 0.5 nm
```

The 4.5 nm optical bandwidth was not used as the wavelength-matching tolerance. It describes the instrument's ability to resolve nearby spectral features, whereas +/- 0.5 nm describes wavelength-position accuracy.

Because of the relatively low spectral resolution, one OliNo feature may be compatible with lines belonging to several different elements.

---

## 2. Ritter Observatory lunar spectra

The second dataset was obtained independently from the Ritter Observatory Public Archive, University of Toledo.

Original archive:

https://astro1.panet.utoledo.edu/~wwritter/archive/FITS-spectra/Moon/Moon.html

The two lunar echelle spectra used were:

`960327.012.fits`

Wavelength coverage:

```
4650-6100 Angstrom
```

12 echelle apertures.

`961116.012.fits`

Wavelength coverage:

```
5286-6597 Angstrom
```

9 echelle apertures.

Copies of the exact files used in this analysis are stored with this reference:

`113_data/ritter_960327.012.fits`

`113_data/ritter_961116.012.fits`

These are archived processed spectra rather than raw CCD frames.

According to the Ritter Observatory archive documentation, archived spectra underwent normal spectroscopic processing including bias subtraction, flat-field correction, spectral extraction and wavelength calibration.

### Instrument resolution

The standard Ritter echelle configuration had a resolving power of approximately:

```
R = 26,000
```

For the same instrument configuration, an instrumental FWHM of approximately 0.23 Angstrom at 5875 Angstrom is documented, corresponding to approximately the same resolving power.

Because no documented absolute wavelength uncertainty for these particular lunar observations was found, no arbitrary +/- nm accuracy was assigned.

Instead, one instrumental resolution element was used:

```
delta_lambda = lambda / 26,000
```

A candidate was classified as wavelength-compatible when:

```
abs(lambda_measured - lambda_NIST)
    <= lambda_measured / 26,000
```

Approximate resolution elements are:

```
465.0 nm   -> 0.0179 nm
500.0 nm   -> 0.0192 nm
587.5 nm   -> 0.0226 nm
656.0 nm   -> 0.0252 nm
```

This criterion should be understood as a spectral-resolution compatibility window, not as a claim that Ritter Observatory specified an absolute wavelength accuracy equal to these values.

---

## 3. Laboratory reference wavelengths

Atomic wavelengths were obtained from:

NIST Atomic Spectra Database (ASD)
Standard Reference Database 78

Official database:

https://physics.nist.gov/PhysRefData/ASD/lines_form.html

The analysis used neutral-atom spectral lines in the relevant wavelength range for fifteen elements:

```
Li
Be
B
C
Si
P
S
Cl
F
O
H
Ne
Na
Mg
Al
```

For reproducibility, the exact NIST wavelength table used in this analysis is stored in the repository as:

`113_data/nist_russell_spiral_test_350_860.csv`

The NIST table was created before the final element comparison.

---

## 4. Blind candidate extraction

The analysis was performed in two stages.

### Stage 1 - spectral feature detection

No chemical element was specified as the target.

The measured spectra were analysed relative to their local continua and candidate spectral deviations were extracted according to predetermined numerical criteria.

Candidates were classified as:

* emission-like
* absorption-like

At this stage no candidate was assigned to neon or any other chemical element.

The candidate lists were then frozen.

### Stage 2 - atomic wavelength comparison

Only after candidate extraction was completed were the measured wavelengths compared with the NIST laboratory line catalogue.

A candidate could produce three relevant outcomes:

NO MATCH

No tested atomic line lies inside the instrumental compatibility window.

AMBIGUOUS MATCH

Lines belonging to more than one tested element lie inside the compatibility window.

ELEMENT-ONLY MATCH

Within the fifteen tested elements, only one element has a laboratory line inside the compatibility window.

"Element-only" therefore means exclusive within the tested fifteen-element catalogue.

It does not mean that every possible atomic species, ion, molecule, atmospheric feature, solar spectral feature or instrumental effect has been excluded.

---

## 5. OliNo results

Blind extraction produced:

```
34 spectral candidates
```

The largest numbers of wavelength-compatible candidates were:

| Element | Compatible candidates |
| ------- | --------------------: |
| C       |                    14 |
| Mg      |                    10 |
| Ne      |                    10 |
| H       |                     6 |

Because of the limited resolution of the OliNo instrument, many candidates were compatible with more than one tested element.

For neon:

```
Ne-compatible = 10
Ne-only       = 2
ambiguous     = 8
```

The two Ne-only candidates were:

### Candidate 1

```
measured wavelength = 583.000000 nm
classification      = emission-like
NIST Ne wavelength  = 582.890630 nm
difference          = 0.109370 nm
allowed difference  = 0.500000 nm
```

Therefore:

```
0.109370 nm <= 0.500000 nm
```

### Candidate 2

```
measured wavelength = 430.000000 nm
classification      = absorption-like
NIST Ne wavelength  = 430.324800 nm
difference          = 0.324800 nm
allowed difference  = 0.500000 nm
```

Therefore:

```
0.324800 nm <= 0.500000 nm
```

Both candidates satisfy the declared OliNo wavelength-position tolerance.

---

## 6. Ritter Observatory results

Blind feature extraction from the selected Ritter spectra produced:

```
total candidates     = 638
emission-like        = 314
absorption-like      = 324
```

For neon, comparison with the NIST laboratory catalogue produced:

```
Ne-compatible = 53
Ne-only       = 47
ambiguous     = 6
```

Among the 47 Ne-only candidates:

```
emission-like   = 20
absorption-like = 27
```

### Closest neon wavelength agreement

The closest wavelength agreement was:

```
Ritter candidate = 519.321276 nm
NIST Ne line     = 519.322400 nm
```

Difference:

```
abs(519.321276 - 519.322400)
    = 0.001124 nm
```

One Ritter resolution element at this wavelength is:

```
519.321276 / 26,000
    = 0.01997 nm
```

Therefore:

```
0.001124 nm < 0.01997 nm
```

The measured candidate lies well inside the predefined one-resolution-element compatibility window.

Several additional Ne-only candidates showed millinanometre-scale agreement with NIST wavelengths.

---

## 7. Cross-dataset result

The important result is not that a single spectral feature happened to lie close to a neon wavelength.

The two datasets were produced independently using different instruments and observational procedures.

The final neon results were:

### OliNo

```
Ne-compatible = 10
Ne-only       = 2
ambiguous     = 8
```

### Ritter Observatory

```
Ne-compatible = 53
Ne-only       = 47
ambiguous     = 6
```

Therefore, both independent lunar spectra contain measured spectral candidates wavelength-compatible with laboratory neon lines.

The higher-resolution Ritter dataset provides substantially stronger discrimination between neon and the other fourteen tested elements.

---

## 8. What the analysis establishes

The following statements are direct results of the analysis.

### Measurement

Spectral features occur at measured wavelengths in both independent lunar datasets.

### Laboratory comparison

A subset of those measured wavelengths falls inside the predefined instrumental compatibility windows of laboratory Ne lines listed in the NIST Atomic Spectra Database.

### Cross-dataset result

Neon-compatible candidates occur independently in both datasets.

Within the fifteen-element comparison catalogue:

```
OliNo:
10 Ne-compatible
2 Ne-only

Ritter:
53 Ne-compatible
47 Ne-only
```

The strongest wavelength agreement found in the Ritter analysis differs from the corresponding NIST Ne wavelength by:

```
0.001124 nm
```

---

## 9. What the analysis does not establish

Wavelength compatibility alone does not establish where the corresponding spectral feature physically originated.

This analysis does not by itself exclude possible contributions from:

* the solar spectrum;
* the Earth's atmosphere;
* molecular absorption;
* instrumental response;
* atomic species not included in the fifteen-element comparison catalogue;
* ionized states not included in the neutral-atom comparison.

Therefore the experimentally reproducible conclusion is deliberately narrower:

> Two independent measurements of lunar light contain spectral candidates compatible with laboratory neon wavelengths. Under the predefined comparison criteria, two OliNo candidates and forty-seven Ritter candidates are exclusive to neon among the fifteen neutral elements tested.

Any physical interpretation of why neon appears in this comparison belongs to the model and is kept separate from the measurement itself.

---

## 10. Data files used

For reproducibility, the following exact input files should accompany this reference:

```
113_data/
|
|-- olino_moon_spectrum.csv
|-- ritter_960327.012.fits
|-- ritter_961116.012.fits
`-- nist_russell_spiral_test_350_860.csv
```

The original public sources should remain linked even when local copies are preserved.

---

## Original public sources

### OliNo

Marcel van der Steen
"Spectrum of moon light"
Measurement date: 14 April 2014
Published: 5 October 2015

https://olino.org/blog/us/articles/2015/10/05/spectrum-of-moon-light/

The page contains the downloadable measurement CSV and states that the published dataset is the average of 24 measurements.

### Ritter Observatory

Ritter Observatory Public Archive
University of Toledo
Moon spectra

https://astro1.panet.utoledo.edu/~wwritter/archive/FITS-spectra/Moon/Moon.html

The archive provides direct downloads of the FITS spectra, including:

```
960327.012.fits
961116.012.fits
```

### NIST Atomic Spectra Database

NIST Atomic Spectra Database
Standard Reference Database 78

https://physics.nist.gov/PhysRefData/ASD/lines_form.html

The repository copy:

`113_data/nist_russell_spiral_test_350_860.csv`

contains the exact wavelength table used for this analysis.

---

## Analysis code

All analysis scripts used in this test are publicly available in this repository.

The analysis was intentionally separated into blind spectral-feature detection and later atomic-wavelength comparison.

### 1. OliNo blind spectral analysis

[blind_moon_spectrum.py](../Scripts/08_LunarSpectrum/blind_moon_spectrum.py)

This script analyses the original OliNo lunar spectrum without using atomic wavelength tables or predetermined element wavelengths.

The detected spectral candidates are frozen before comparison with NIST data.

### 2. Ritter blind spectral analysis

[ritter_two_blind.py](../Scripts/08_LunarSpectrum/ritter_two_blind.py)

This script analyses the two selected Ritter Observatory lunar FITS spectra:

    960327.012.fits
    961116.012.fits

No atomic line wavelengths or element identifications are used during the blind candidate extraction.

### 3. Direct instrument-to-NIST test

[direct_instrument_nist_test.py](../Scripts/08_LunarSpectrum/direct_instrument_nist_test.py)

This script compares the previously extracted spectral candidates with laboratory wavelengths from NIST ASD using the predefined instrumental criteria.

    OliNo:
    abs(lambda_measured - lambda_NIST) <= 0.5 nm

    Ritter:
    abs(lambda_measured - lambda_NIST) <= lambda_measured / 26000

No Monte Carlo simulation, random wavelength shifting or post-hoc adjustment of the instrumental windows is used.

### 4. Element uniqueness test

[element_uniqueness_test.py](../Scripts/08_LunarSpectrum/element_uniqueness_test.py)

This script determines whether a wavelength-compatible spectral candidate is compatible with only one of the fifteen tested neutral elements or with several of them.

A candidate matching multiple NIST lines belonging to the same element is counted as one element match.

The final neon results are:

    OliNo:
    Ne-compatible = 10
    Ne-only       = 2
    ambiguous     = 8

    Ritter:
    Ne-compatible = 53
    Ne-only       = 47
    ambiguous     = 6

## Reproducibility

The observational data, laboratory wavelength source, analysis criteria and analysis code are provided so that the test can be independently checked.

Anyone can obtain the original lunar-spectrum data from the sources listed below, inspect the code, repeat the blind extraction, repeat the NIST wavelength comparison and verify the reported results.

Measurement, calculation and interpretation are kept separate.

If the reported result cannot be reproduced from the stated data and code, it should not be accepted.
