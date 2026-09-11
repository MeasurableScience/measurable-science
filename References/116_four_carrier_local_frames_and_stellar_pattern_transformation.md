# [116] Four Carrier-Local Coordinate Frames and Invariant Stellar Pattern Transformation

## Purpose

This reference extends the four-magistrale synchronization geometry established in Reference [107].

The purpose of the calculation is to test three questions:

1. Can four irregularly separated carriers each define a local orthogonal coordinate frame?
2. Can one stellar pattern be transformed into all four local frames without changing its internal geometry?
3. Is this mathematical structure compatible with geographically separated observations of the same stellar field?

No stellar-emission mechanism is assumed in the calculation.

The physical interpretation of one source record being reproduced in several local frames is considered only after the geometric tests are completed.

---

## 1. Previously Fixed Four-Carrier Geometry

Reference [107] used four fixed magistrale directions on a north-centered azimuthal projection:

M1 = 60 deg  
M2 = 130 deg  
M3 = 210 deg  
M4 = 335 deg

The combined phase-dependent resultant was:

X(phi) = -0.091782 cos(phi) + 0.109382 sin(phi)

Y(phi) = 0.109382 cos(phi) + 0.091782 sin(phi)

Its magnitude is:

R = sqrt(0.091782^2 + 0.109382^2)

R = 0.142787806

The direction of the resultant is:

theta(phi) = theta0 - phi

with:

theta0 = 129.999878 deg

approximately:

theta(phi) = 130 deg - phi

The magnitude R is constant while the direction rotates through a complete cycle.

Reference [107] used the MASTER-FEEDBACK angular separation:

D_MF = 162.92 deg

as the angular scale.

This produced:

A = D_MF * R

A = 162.92 * 0.142787806

A = 23.262989 deg

The calculation was completed before comparison with the geographical tropic value of approximately 23.44 deg.

Difference:

23.44 - 23.262989 = 0.177011 deg

Relative difference:

0.177011 / 23.44 * 100 = 0.7552 percent

In the model, this result is interpreted as the approximate Cancer-Capricorn solstitial displacement.

---

## 2. The Equinox Problem

The previous calculation establishes one pair of opposite solstitial extrema.

If Cancer-Capricorn represents one axis, the corresponding Aries-Libra equinoctial axis must be separated from it by one quarter of a complete cycle:

360 deg / 4 = 90 deg

However, the four carriers themselves are not separated by 90 deg.

Their successive angular separations are:

M1 -> M2 = 70 deg  
M2 -> M3 = 80 deg  
M3 -> M4 = 125 deg  
M4 -> M1 = 85 deg

Other pairwise separations are:

M1 <-> M3 = 150 deg  
M2 <-> M4 = 155 deg

Therefore, an orthogonal solstice/equinox frame cannot be obtained by treating the four carrier directions themselves as the four axes of one cross.

A different possibility must be tested:

each carrier may measure the common rotating resultant relative to its own direction.

---

## 3. Carrier-Local Angle

Let alpha_i be the fixed direction of carrier Mi.

For each carrier define:

beta_i(phi) = theta(phi) - alpha_i

where:

theta(phi) = theta0 - phi

Therefore:

beta_i(phi) = theta0 - phi - alpha_i

The same common resultant is used for all four carriers.

Only the local zero direction changes.

The four characteristic local states are:

beta_i = 0 deg  
beta_i = 90 deg  
beta_i = 180 deg  
beta_i = 270 deg

These form two opposite axes:

0 deg <-> 180 deg

and:

90 deg <-> 270 deg

The axes are exactly orthogonal.

---

## 4. Numerical Carrier-Local Frames

Using:

theta0 = 129.999878 deg

the phases at which the common resultant reaches the four characteristic states were calculated independently for every carrier.

### M1 = 60 deg

Local 0 deg:

phi = 69.999878 deg

Local 90 deg:

phi = 339.999878 deg

Local 180 deg:

phi = 249.999878 deg

Local 270 deg:

phi = 159.999878 deg

The corresponding absolute directions of the local frame are:

60 deg  
150 deg  
240 deg  
330 deg

### M2 = 130 deg

Local 0 deg:

phi = 359.999878 deg

Local 90 deg:

phi = 269.999878 deg

Local 180 deg:

phi = 179.999878 deg

Local 270 deg:

phi = 89.999878 deg

Absolute local-frame directions:

130 deg  
220 deg  
310 deg  
40 deg

### M3 = 210 deg

Local 0 deg:

phi = 279.999878 deg

Local 90 deg:

phi = 189.999878 deg

Local 180 deg:

phi = 99.999878 deg

Local 270 deg:

phi = 9.999878 deg

Absolute local-frame directions:

210 deg  
300 deg  
30 deg  
120 deg

### M4 = 335 deg

Local 0 deg:

phi = 154.999878 deg

Local 90 deg:

phi = 64.999878 deg

Local 180 deg:

phi = 334.999878 deg

Local 270 deg:

phi = 244.999878 deg

Absolute local-frame directions:

335 deg  
65 deg  
155 deg  
245 deg

---

## 5. Result: Irregular Carriers, Regular Local Quadrature

The calculation produces an important distinction.

The carrier directions remain irregularly separated:

70 deg  
80 deg  
125 deg  
85 deg

They do not form a 90-degree cross.

However, the local coordinate frame of every individual carrier is:

0 deg  
90 deg  
180 deg  
270 deg

Therefore:

carrier separation != local coordinate quadrature

The 90-degree structure does not arise from the physical angular separation between M1, M2, M3 and M4.

It arises because each carrier measures the same rotating resultant relative to its own fixed direction.

In the model interpretation:

local 0-180 deg = Cancer-Capricorn axis

local 90-270 deg = Aries-Libra axis

The mathematical result itself establishes the orthogonal local axes. The identification of these axes with Cancer-Capricorn and Aries-Libra is a model interpretation.

---

## 6. Transformation of a Common Stellar Pattern

The next question is whether four local coordinate frames require four independent stellar patterns.

Let a common set of stellar addresses be:

Z = {z_1, z_2, ..., z_n}

For carrier Mi, define a rigid local transformation:

Z_i = T_i(Z)

For a two-dimensional angular representation, the transformation may be written as:

T_i =
[ cos(alpha_i)  -sin(alpha_i) ]
[ sin(alpha_i)   cos(alpha_i) ]

or equivalently by subtracting the carrier direction from every angular address.

For any two stellar directions z_a and z_b, a rigid rotation preserves their angular separation:

angle(z_a, z_b) = angle(T_i z_a, T_i z_b)

Therefore a common stellar pattern can be expressed in several differently oriented local coordinate frames without changing the geometry of the pattern itself.

---

## 7. Numerical Pattern-Invariance Test

A blind geometric control was performed using arbitrary angular addresses:

7 deg  
41 deg  
96 deg  
173 deg  
251 deg

These values were not astronomical targets.

They were selected only to test whether the four transformations alter the internal pattern.

For each carrier, all addresses were transformed into its local frame.

Every pairwise angular separation was then recalculated.

Maximum change in any pairwise separation:

0.000000000000 deg

within numerical precision.

Result:

one common angular pattern can be represented in all four carrier-local frames without geometric deformation.

This result is a mathematical property of rigid rotation and does not by itself establish a physical stellar projection mechanism.

---

## 8. Geographic Mapping of the Carrier Directions

The synchronization zero-axis is placed approximately through the Cape Verde sector.

For the numerical geographic test a reference meridian of approximately:

lambda0 = 25 deg W

was used.

On the north-centered azimuthal representation, the carrier directions then correspond approximately to:

M1:

-25 + 60 = 35 deg E

M2:

-25 + 130 = 105 deg E

M3:

-25 + 210 = 185 deg E = 175 deg W

M4:

-25 + 335 = 310 deg E = 50 deg W

Therefore:

M1 = 35 deg E  
M2 = 105 deg E  
M3 = 175 deg W  
M4 = 50 deg W

These results are consistent with the carrier routes identified before the present test:

M1: Jerusalem-Cappadocia sector

M2: Southeast Asian sector between Sumatra and Borneo

M3: Pacific sector

M4: eastern Brazil-Atlantic sector

The geographic descriptions were not derived from the cities used in the later stellar comparison.

---

## 9. Geographic Local Axes

After establishing the carrier meridians, the 90-degree local axes were calculated without using observer locations.

The resulting frozen geographic frame was:

| Carrier | 0 deg | +90 deg | 180 deg | -90 deg |
| --- | ---: | ---: | ---: | ---: |
| M1 | 35 E | 125 E | 145 W | 55 W |
| M2 | 105 E | 165 W | 75 W | 15 E |
| M3 | 175 W | 85 W | 5 E | 95 E |
| M4 | 50 W | 40 E | 130 E | 140 W |

These values were frozen before comparison with selected observer locations.

---

## 10. Geographic Control

After the axes had been calculated, several geographically separated locations were compared with the frozen meridians.

### Santiago

Longitude approximately:

70.59 deg W

Nearest previously calculated axis:

75 deg W

Difference:

4.41 deg

### Madrid

Longitude approximately:

3.68 deg W

Nearest previously calculated axis:

5 deg E

Difference:

8.68 deg

### Beijing

Longitude approximately:

116.33 deg E

Nearest previously calculated axis:

125 deg E

Difference:

8.67 deg

### Australia

An initial exploratory comparison used Sydney.

Sydney is approximately:

151.22 deg E

This was not the longitude predicted by the frozen carrier geometry.

The model-derived M4 opposite axis had already been calculated as:

130 deg E

The appropriate test was therefore not to move the calculated axis toward Sydney, but to retain:

130 deg E

This meridian crosses Australia.

The later stellar test consequently used the frozen 130 deg E Australian meridian rather than Sydney as the model-defined Australian reference.

No carrier angle was changed to improve the geographic comparison.

---

## 11. Stellar Observation Geometry Test

A second control used ten real stellar directions:

Polaris  
Sirius  
Canopus  
Betelgeuse  
Spica  
Arcturus  
Vega  
Antares  
Achernar  
Alpha Centauri

The comparison was made at the same local sidereal phase so that differences caused only by different local sky times would not be confused with the local-frame geometry.

For ten stars there are:

10 * 9 / 2 = 45

independent star-pair comparisons.

---

## 12. Sydney-Santiago Exploratory Control

Before replacing Sydney with the model-derived Australian meridian, an exploratory same-latitude comparison was performed.

Sydney latitude:

-33.8688 deg

Santiago latitude:

-33.4489 deg

Latitude difference:

0.4199 deg

At the same local sidereal phase, the ten stellar directions gave:

mean local-direction difference = 0.3250 deg

maximum local-direction difference = 0.4199 deg

For all 45 internal star-pair angular separations:

maximum pattern change = 0.000000000000 deg

within numerical precision.

This demonstrated the expected invariance of the stellar pattern under a change of local frame.

Sydney was not subsequently treated as a predicted carrier-axis location.

---

## 13. Madrid-Beijing Control

Madrid latitude:

40.4168 deg N

Beijing latitude:

39.9042 deg N

Latitude difference:

0.5126 deg

At equal local sidereal phase:

mean stellar local-direction difference = 0.3968 deg

maximum difference = 0.5126 deg

For all 45 internal stellar angular separations:

maximum pattern change = 0.000000000000 deg

within numerical precision.

The stellar pattern remained geometrically unchanged while its local orientation depended on the observer frame.

---

## 14. Frozen Australian Axis-Santiago Control

The final Australian comparison retained the previously calculated:

130 deg E

axis.

A representative inland Australian point was used at:

24 deg S, 130 deg E

Santiago was:

33.4489 deg S, 70.6693 deg W

Latitude difference:

9.4489 deg

At the same local sidereal phase:

mean local stellar-direction difference = 7.312 deg

maximum local stellar-direction difference = 9.448 deg

However, across all 45 star-pair angular separations:

maximum internal-pattern change = 0.000000000000 deg

within numerical precision.

The local orientation changed, while the internal stellar geometry remained invariant.

---

## 15. What the Tests Establish

The calculations establish the following mathematical results.

First, the four irregular carrier directions can each define their own orthogonal local coordinate frame.

Second, the 90-degree local quadrature does not require the carriers themselves to be separated by 90 degrees.

Third, one common angular stellar pattern can be transformed into all four local frames without changing any internal angular relationship between its points.

Fourth, geographically separated observers can have differently oriented local stellar fields while the internal stellar pattern remains unchanged.

The numerical tests produced zero change, within numerical precision, in all tested internal star-pair angular separations.

Therefore:

one common stellar record is mathematically sufficient to generate several differently oriented local representations.

---

## 16. Limits of the Result

The calculations do not establish that the physical firmament is an electromagnetic display.

They also do not establish that one physical stellar emitter supplies four projected stellar images.

Rigid coordinate transformations in conventional spherical astronomy also preserve angular relationships between stars.

Therefore the observation:

one stellar pattern -> several local orientations

is compatible with both conventional coordinate geometry and the proposed model.

What has been established here is narrower:

the four-carrier geometry does not mathematically require four independent copies of the same stellar pattern.

This permits the following model hypothesis to be tested separately:

one stellar source/address -> four carrier-local representations

rather than:

four independent sources -> four copies of the same stellar pattern

The physical mechanism, if such a mechanism exists, requires independent evidence.

---

## 17. Model Consequence for Further Testing

If the firmament functions as an information-bearing layer in the proposed natural-computer architecture, a single stellar address could in principle be stored or generated once and transformed according to the local frame of each carrier.

Symbolically:

Z -> {T1(Z), T2(Z), T3(Z), T4(Z)}

For a constellation consisting of several stellar addresses:

C_k = P(z_1, z_2, ..., z_n)

the same transformation gives:

C_k,i = T_i(C_k)

Because rigid transformation preserves the internal angular relationships, the constellation remains the same geometric pattern in every carrier-local frame.

This provides the mathematical basis for the next question:

If a constellation can remain one invariant pattern across several local representations, what information does that pattern represent to the natural computer?