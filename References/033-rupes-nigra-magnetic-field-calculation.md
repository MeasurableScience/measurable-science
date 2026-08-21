# Reference 033 — Magnetic field calculation for the hypothetical Rupes Nigra

## Purpose

This reference documents the mathematical model used in the book to estimate the magnetic field at the top of the hypothetical central volcanic structure identified in the author's model with Mercator's Rupes Nigra.

The calculation is not evidence that Rupes Nigra exists or that its magnetic properties are known.

It is a first-order physical test based on:

- the dimensions previously derived from the historical description and physical model;
- a working value for natural remanent magnetization taken from documented basaltic rocks.

---

## Input parameters

The hypothetical structure is approximated as a uniformly magnetized vertical cylinder.

Working dimensions:

- diameter:

**D = 47 km**

- radius:

**R = 23.5 km = 23,500 m**

- height:

**L = 60 km = 60,000 m**

The height is a rounded working value within the approximately **56–67 km** vertical range obtained in the previous first-breakthrough calculation.

Working magnetization:

**M = 32.5 A/m**

The origin and justification of this value are documented separately in:

**Reference 032 — Volcanic rock composition and natural remanent magnetization**

It is an intermediate modelling value between approximately 10 A/m for strongly magnetized young oceanic basalt and approximately 55 A/m for the median measured magnetization of the unusually magnetic Stardalur basalt in Iceland.

---

## Model

For a uniformly magnetized finite cylinder with magnetization directed along its vertical axis, the magnetic field on the axis immediately above the centre of the upper surface can be approximated by:

\[
B =
\frac{\mu_0 M}{2}
\frac{L}{\sqrt{L^2+R^2}}
\]

where:

- \(B\) = magnetic flux density;
- \(\mu_0\) = permeability of free space;
- \(M\) = uniform magnetization of the cylinder;
- \(L\) = cylinder height;
- \(R\) = cylinder radius.

The permeability of free space is:

\[
\mu_0 = 4\pi \times 10^{-7}\ \mathrm{H/m}
\]

---

## Substitution

Using:

\[
M = 32.5\ \mathrm{A/m}
\]

\[
L = 60,000\ \mathrm{m}
\]

\[
R = 23,500\ \mathrm{m}
\]

gives:

\[
B =
\frac{(4\pi \times 10^{-7})(32.5)}{2}
\times
\frac{60,000}
{\sqrt{60,000^2+23,500^2}}
\]

First calculate the geometric factor:

\[
\sqrt{60,000^2+23,500^2}
\approx 64,438\ \mathrm{m}
\]

therefore:

\[
\frac{60,000}{64,438}
\approx 0.931
\]

The magnetic field becomes:

\[
B \approx 1.90\times10^{-5}\ \mathrm{T}
\]

or:

\[
B \approx 19.0\ \mu\mathrm{T}
\]

---

# Result

For the stated working assumptions, the estimated magnetic field immediately above the centre of the upper surface is approximately:

# **19 μT**

---

## Interpretation

A magnetic field of approximately 19 μT is not an extreme field.

For comparison, the Earth's present-day surface magnetic field is commonly of the order of several tens of microtesla.

The model therefore does not require the hypothetical structure to behave like an exceptionally powerful permanent magnet.

It requires only a very large body of naturally magnetized volcanic material with a coherent net remanent magnetization.

Because of the enormous dimensions of the hypothetical structure, even a moderate magnetization measured in amperes per metre can produce a local magnetic field in the microtesla range.

---

## Important assumptions

This is an idealized upper-order geometric model.

It assumes:

1. the structure can be approximated as a cylinder;
2. the diameter is approximately 47 km;
3. the height is approximately 60 km;
4. the average net magnetization is 32.5 A/m;
5. the magnetization has a coherent dominant vertical direction;
6. the magnetic material is distributed sufficiently uniformly for the cylinder approximation to be useful;
7. demagnetization, hydrothermal alteration and complex internal mineral structure are not explicitly resolved;
8. external magnetic fields and surrounding geological material are not included.

The real magnetic field of a natural body would depend strongly on its internal structure, mineralogy, magnetic domain orientation and geological history.

---

## Why coherent magnetization matters

The presence of magnetite or titanomagnetite alone does not guarantee a strong external magnetic field.

If magnetic domains are randomly oriented, much of their field cancels.

The calculation therefore uses **net remanent magnetization**, not the saturation magnetization of pure magnetite.

This distinction is essential.

The value of 32.5 A/m represents a bulk rock magnetization, not the intrinsic magnetization of an individual magnetic mineral.

---

## Sensitivity to magnetization

Because the field in this model is directly proportional to magnetization, other working values can be estimated immediately.

For the same 47 km diameter and 60 km height:

- **M = 10 A/m** → approximately **5.85 μT**
- **M = 20 A/m** → approximately **11.7 μT**
- **M = 32.5 A/m** → approximately **19.0 μT**
- **M = 55 A/m** → approximately **32.2 μT**
- **M = 128 A/m** → approximately **74.9 μT**

The book uses **32.5 A/m** only as a working intermediate value.

---

## Relevance to the next calculation

The resulting field of approximately **19 μT** becomes an input for the next physical test.

The hypothetical central structure is surrounded by a very large body of moving saline water.

Seawater is electrically conductive.

A conductive fluid moving through a magnetic field experiences motional electromagnetic induction.

The next calculation therefore examines whether the combination:

**magnetic central structure + moving saline water**

can produce an electromotive force and electrical current in the surrounding system.

That calculation is treated separately from this reference.