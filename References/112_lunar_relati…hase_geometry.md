# Reference 112 --- Lunar Relative-Phase Geometry and Comparison with Observed Lunar Inclination

## Purpose

This reference documents the mathematical construction used in the book
to test whether the geometry of the four previously defined carriers
produces a lunar-scale angular offset without inserting a known lunar
angle into the calculation.

The procedure is deliberately separated into two stages:

1.  **Model calculation** --- performed only from the previously defined
    carrier directions and their common synchronization direction.
2.  **External comparison** --- performed only after the model result is
    frozen, using published astronomical values.

The comparison does not prove the proposed physical interpretation of
the Moon. It tests whether an independently obtained geometric result
coincides with a measured lunar angular scale.

------------------------------------------------------------------------

## 1. Previously defined carrier geometry

The four carrier directions used in the model are:

-   M1 = 60°
-   M2 = 130°
-   M3 = 210°
-   M4 = 335°

The common synchronization direction at the reference phase is:

-   S = 130°

No lunar orbital inclination, lunar declination, lunar period, or lunar
standstill value is used to obtain the result below.

------------------------------------------------------------------------

## 2. Relative carrier positions

For each carrier, define its angular position relative to the common
synchronization direction:

Δφ_i = M_i − S

This gives:

-   M1 − S = 60° − 130° = **−70°**
-   M2 − S = 130° − 130° = **0°**
-   M3 − S = 210° − 130° = **+80°**
-   M4 − S = 335° − 130° = **+205°**, equivalent to **−155°** on the
    shortest signed angular interval.

Therefore the relative carrier geometry is:

**−70°, 0°, +80°, −155°**

The two carriers immediately bracketing the common synchronization
direction are M1 and M3:

-   M1 = −70°
-   M3 = +80°

If they were perfectly symmetric about the common synchronization
direction, they would lie at −75° and +75°. Their actual midpoint is:

(-70° + 80°) / 2 = **+5.00°**

Thus the carrier geometry independently produces the angular offset:

**δ_model = 5.00°**

This value is frozen before comparison with lunar data.

------------------------------------------------------------------------

## 3. Comparison with the measured lunar orbital inclination

NASA's *Earth's Moon* fact sheet gives the Moon's orbital inclination to
the ecliptic as:

**i_Moon = 5.145°**

The difference from the model-derived value is:

5.145° − 5.000° = **0.145°**

Relative difference:

0.145° / 5.145° × 100 ≈ **2.82%**

Thus:

-   Model result: **5.000°**
-   Published lunar inclination: **5.145°**
-   Absolute difference: **0.145°**
-   Relative difference: **≈ 2.8%**

NASA also describes the lunar orbit more generally as tilted by about 5°
relative to the ecliptic.

------------------------------------------------------------------------

## 4. Combination with the previously derived solar geometry

The preceding solar synchronization calculation produced a model angular
displacement of:

**δ_solar = 23.26°**

This value was derived separately from the four-carrier synchronization
geometry and the MASTER--FEEDBACK angular span.

The lunar relative-phase result is:

**δ_lunar = 5.00°**

Without inserting measured lunar declination limits, the two
model-derived values can be combined:

23.26° + 5.00° = **28.26°**

23.26° − 5.00° = **18.26°**

Therefore the model predicts two characteristic angular limits:

**28.26° and 18.26°**

------------------------------------------------------------------------

## 5. Comparison with standard lunar standstill geometry

In standard astronomical geometry, the ecliptic is inclined by
approximately 23.4° to the celestial equator, while the Moon's orbit is
inclined by approximately 5.145° to the ecliptic.

When these inclinations reinforce one another, the Moon can reach
declinations of approximately:

23.44° + 5.145° ≈ **28.59°**

When they oppose one another, the corresponding limiting scale is
approximately:

23.44° − 5.145° ≈ **18.30°**

These are the familiar angular scales associated with major and minor
lunar standstill geometry. NASA describes major lunar standstills as the
extremes of the Moon's north--south range produced by the 18.6-year
precession of the lunar orbit. Historical observational material
published by *Sky & Telescope* reports extreme geocentric lunar
declinations near ±28.6° during a major standstill.

Comparison:

  -----------------------------------------------------------------------
  Quantity           Model geometry           Standard         Difference
                                          astronomical 
                                              geometry 
  -------------- ------------------ ------------------ ------------------
  Relative lunar             5.000°             5.145°             0.145°
  offset                                               

  Outer angular              28.26°            ≈28.59°             ≈0.33°
  limit                                                

  Inner angular              18.26°            ≈18.30°             ≈0.04°
  limit                                                
  -----------------------------------------------------------------------

The outer and inner values in the standard column are geometric
combinations of the terrestrial obliquity and lunar orbital inclination;
they are not additional input values used in the model calculation.

------------------------------------------------------------------------

## 6. Interpretation within the proposed model

The mathematical result alone establishes only the following:

1.  The previously defined four-carrier geometry gives a **5.00°**
    asymmetry about the common synchronization direction.
2.  This value was obtained without using a lunar inclination value.
3.  The independently published lunar orbital inclination is **5.145°**.
4.  Combining the model's previously derived solar displacement of
    **23.26°** with the new **5.00°** offset gives **28.26°** and
    **18.26°**, close to the standard lunar declination scales of
    approximately **28.59°** and **18.30°**.

The physical interpretation proposed in the book is a separate
hypothesis: the Sun corresponds to the common synchronization state of
all four carriers, whereas the Moon may represent the relative
phase/alignment of an individual carrier with respect to that common
synchronization point.

This reference does **not** establish that interpretation as an observed
physical mechanism. It documents the calculation and the subsequent
numerical comparison.

------------------------------------------------------------------------

## 7. Sources

### NASA --- Earth's Moon fact sheet

NASA Planetary Science Division, *Earth's Moon*.

Published value used here:

-   Orbit inclination to ecliptic: **5.145°**
-   Orbit period: **27.32 Earth days**

Source:

https://assets.science.nasa.gov/content/dam/science/psd/lunar-science/2023/09/Earths-Moon.pdf

### NASA Science --- Eclipses and the Moon

NASA explains that the Moon's orbit is tilted by about 5° relative to
the plane of Earth's orbit around the Sun.

Source:

https://science.nasa.gov/moon/eclipses/

### NASA Science --- Reference Systems

NASA's reference-system documentation describes the ecliptic as inclined
by approximately 23.4° to the celestial equator and defines celestial
declination.

Source:

https://science.nasa.gov/learn/basics-of-space-flight/chapter2-2/

### NASA Science --- Major Lunar Standstill 2024--2025

NASA Astronomy Picture of the Day describes major lunar standstills as
extremes in the north--south range of moonrise driven by the 18.6-year
precession period of the lunar orbit.

Source:

https://science.nasa.gov/image-article/apod-2025-june-20-major-lunar-standstill-2024-2025/

### Sky & Telescope --- Major Lunar Standstill

An observational example reports maximum lunar declination near
**28.60°** during a major lunar standstill.

Source:

https://skyandtelescope.org/online-gallery/major-lunar-standstill-2006/

------------------------------------------------------------------------

## Reproducibility note

The essential blind calculation can be reproduced directly:

``` text
M1 = 60°
M2 = 130°
M3 = 210°
M4 = 335°
S  = 130°

M1_relative = 60°  − 130° = −70°
M3_relative = 210° − 130° = +80°

midpoint = (−70° + 80°) / 2
         = 5.00°
```

Only after obtaining **5.00°** is the result compared with the published
lunar orbital inclination of **5.145°**.
