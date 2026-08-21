# Reference 037 — Electrical resistance and voltage of the hypothetical Rupes Nigra column

## Purpose

This reference documents the first-order calculation used in the book
to estimate the electrical resistance and potential difference of the
hypothetical Rupes Nigra volcanic column.

Reference 036 produced an idealized current scale of approximately:

I = 33 MA

The present calculation asks what potential difference could develop
along the volcanic column if a current of this magnitude were conducted
through it.

This is a theoretical model calculation, not a measurement of Rupes Nigra.

---

## Physical method

The calculation uses Ohm's law:

V = IR

where:

- V = potential difference (V)
- I = electric current (A)
- R = electrical resistance (Ω)

For a uniform conducting body:

R = ρL/A

where:

- ρ = electrical resistivity of the material (Ω·m)
- L = conductor length (m)
- A = conductor cross-sectional area (m²)

---

## Geometry of the working model

Diameter of the volcanic column:

D = 47 km

D = 47,000 m

Radius:

r = 23,500 m

Cross-sectional area:

A = πr²

A = π × (23,500)²

A ≈ 1.735 × 10^9 m²

The model separates the column into two sections:

1. submerged section:

L1 = 250 km = 250,000 m

2. section above water:

L2 = 60 km = 60,000 m

Total modeled length:

L = 310 km

---

## Electrical resistivity

Electrical resistivity of basalt is not a single constant.

It depends strongly on:

- water content;
- pore-fluid salinity;
- porosity and fractures;
- temperature;
- mineral composition;
- alteration.

Water-saturated volcanic rock can therefore be orders of magnitude
more conductive than dry volcanic rock.

For the first working calculation the model uses:

Submerged / seawater-saturated section:

ρ1 ≈ 35 Ω·m

Upper, less water-saturated volcanic section:

ρ2 ≈ 3350 Ω·m

These values are not claimed to describe Rupes Nigra.

They are working resistivities selected within measured orders of
magnitude for conductive saturated basaltic material and substantially
more resistive volcanic material.

---

## Scientific basis

Electrical measurements of basaltic and volcanic rocks demonstrate
the strong dependence of bulk resistivity on pore water, salinity,
temperature and alteration.

A useful early experimental source for seawater-saturated basalt is:

U.S. Geological Survey

Electrical resistivity measurements of seawater-saturated basaltic
rock.

USGS Open-File Report 68-341.

https://pubs.usgs.gov/publication/ofr68341

The broader geophysical literature likewise shows that volcanic
formations can span several orders of magnitude in resistivity,
depending particularly on fluid content and hydrothermal alteration.

Because of this large natural range, the values used here should be
treated as working parameters for the model rather than universal
resistivities of basalt.

---

## Resistance of the submerged section

Using:

ρ1 = 35 Ω·m

L1 = 250,000 m

A = 1.735 × 10^9 m²

R1 = ρ1 L1 / A

R1 ≈ (35 × 250,000) / (1.735 × 10^9)

R1 ≈ 0.0050 Ω

---

## Resistance of the upper section

Using:

ρ2 = 3350 Ω·m

L2 = 60,000 m

A = 1.735 × 10^9 m²

R2 = ρ2 L2 / A

R2 ≈ (3350 × 60,000) / (1.735 × 10^9)

R2 ≈ 0.116 Ω

---

## Total resistance

The two sections are treated as series components:

Rtotal = R1 + R2

Rtotal ≈ 0.0050 + 0.116

Rtotal ≈ 0.121 Ω

Therefore the working electrical resistance of the entire modeled
column is approximately:

# R ≈ 0.12 Ω

---

## Potential difference at 33 MA

From Reference 036:

I ≈ 33,000,000 A

Using Ohm's law:

V = IR

V ≈ 33,000,000 × 0.121

V ≈ 3,993,000 V

Therefore:

# V ≈ 4.0 MV

The first working estimate therefore places the summit potential
difference in the megavolt range.

---

## Sensitivity to upper-column resistivity

Because the upper 60 km dominates the resistance, the result is
particularly sensitive to its assumed resistivity.

For example, if the effective resistivity of the upper section were
approximately:

ρ2 ≈ 8600 Ω·m

then:

R2 ≈ 0.297 Ω

Adding the submerged section gives approximately:

Rtotal ≈ 0.302 Ω

At 33 MA:

V ≈ 33,000,000 × 0.302

V ≈ 9,970,000 V

or approximately:

# 10 MV

Thus the working model naturally produces potential differences in
the approximate range of several megavolts, with the exact value
depending strongly on the electrical properties of the upper column.

---

## Comparison with a 100 V/m potential gradient

A potential gradient of:

100 V/m

maintained over:

60 km = 60,000 m

would correspond mathematically to:

V = 100 × 60,000

V = 6,000,000 V

Therefore:

# V = 6 MV

This value lies within the same order of magnitude as the approximately
4–10 MV range obtained independently from the resistance/current model.

This comparison should not be interpreted as assuming that the modern
atmospheric electric field remains constant at 100 V/m through 60 km
of altitude.

The approximately 100 V/m fair-weather atmospheric electric field is
a near-surface value and changes substantially with altitude.

The significance here is only the numerical comparison of scales:

33 MA + modeled volcanic resistance -> several MV

100 V/m × 60 km -> 6 MV

Both independently produce a megavolt-scale potential difference.

---

## Result used in the book

For the working parameters:

- current ≈ 33 MA;
- column diameter ≈ 47 km;
- submerged length ≈ 250 km;
- exposed length ≈ 60 km;
- submerged resistivity ≈ 35 Ω·m;
- upper-column resistivity ≈ 3350 Ω·m;

the calculated potential difference is approximately:

# 4 MV

Reasonable variation of the poorly constrained upper-column
resistivity moves the result into the several-megavolt range,
including approximately:

# 6–10 MV

The next calculation examines whether electric potentials of this
order are sufficient to initiate electrical breakdown and ionization
of the rarefied atmosphere near 60 km altitude.