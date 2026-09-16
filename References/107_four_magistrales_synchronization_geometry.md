# Reference 107 — Four Magistrales and Synchronization Geometry

## Purpose

This document gives the complete mathematical derivation of the synchronization resultant used in *Measurable Science*.

The calculation begins with the previously defined directions of the four magistrales and the system axis 0°/180°.

The MASTER–FEEDBACK line is **not** used to derive the Cartesian resultant or its magnitude R. It enters only later, when its angular separation is used as the scale onto which the dimensionless resultant is transferred.

The geographical positions of the Tropics are also **not** used as an input. They are introduced only after the geometrical result has been obtained.

The calculation therefore follows the sequence:

    four magistrales
        ↓
    deviations from the 0°/180° system axis
        ↓
    phase-dependent amplitudes
        ↓
    Cartesian vector sum
        ↓
    resultant magnitude R
        ↓
    MASTER–FEEDBACK angular scale
        ↓
    comparison with the Tropics

---

## 1. Four magistrales

On the north-centered azimuthal projection, the four magistrales have the following directions:

    M1 = 60°
    M2 = 130°
    M3 = 210°
    M4 = 335°

The system reference is the 0°/180° axis.

Because 0° and 180° are opposite directions of the same axis, each magistrale can be expressed by its signed deviation from the nearest direction of that axis.

This gives:

    M1 = 60°   → Δ1 = +60°
    M2 = 130°  → Δ2 = -50°
    M3 = 210°  → Δ3 = +30°
    M4 = 335°  → Δ4 = -25°

Therefore:

    M = (60°, 130°, 210°, 335°)

and:

    Δ = (+60°, -50°, +30°, -25°)

No numerical normalization factor is introduced in the calculation below.

---

## 2. Phase-dependent amplitude

Let phi represent the common phase of the system.

For each magistrale, the phase-dependent amplitude is defined as:

    Ai(phi) = cos(phi - Δi)

Each amplitude acts along the actual direction of its magistrale.

The unit vector of magistrale i is:

    ui = (cos Mi, sin Mi)

Therefore, the vector contribution of each magistrale is:

    Vi(phi) = Ai(phi) × ui

or:

    Vi(phi) = cos(phi - Δi) × (cos Mi, sin Mi)

The combined resultant is simply the sum of the four contributions:

    Rvec(phi) = V1(phi) + V2(phi) + V3(phi) + V4(phi)

No additional scaling or fitting parameter is used in this sum.

---

## 3. Cartesian components of the resultant

The X component is:

    X(phi) = Σ cos(phi - Δi) cos(Mi)

The Y component is:

    Y(phi) = Σ cos(phi - Δi) sin(Mi)

Using:

    cos(phi - Δi)
    =
    cos(phi) cos(Δi) + sin(phi) sin(Δi)

the X component becomes:

    X(phi)
    =
    cos(phi) Σ[cos(Δi) cos(Mi)]
    +
    sin(phi) Σ[sin(Δi) cos(Mi)]

Similarly:

    Y(phi)
    =
    cos(phi) Σ[cos(Δi) sin(Mi)]
    +
    sin(phi) Σ[sin(Δi) sin(Mi)]

The four coefficients can now be calculated directly from the four magistrale directions and their signed deviations.

### X coefficient multiplying cos(phi)

    Cx =
      cos(60°)  cos(60°)
    + cos(-50°) cos(130°)
    + cos(30°)  cos(210°)
    + cos(-25°) cos(335°)

Numerically:

    Cx = -0.0917821063

### X coefficient multiplying sin(phi)

    Sx =
      sin(60°)  cos(60°)
    + sin(-50°) cos(130°)
    + sin(30°)  cos(210°)
    + sin(-25°) cos(335°)

Numerically:

    Sx = +0.1093816549

### Y coefficient multiplying cos(phi)

    Cy =
      cos(60°)  sin(60°)
    + cos(-50°) sin(130°)
    + cos(30°)  sin(210°)
    + cos(-25°) sin(335°)

Numerically:

    Cy = +0.1093816549

### Y coefficient multiplying sin(phi)

    Sy =
      sin(60°)  sin(60°)
    + sin(-50°) sin(130°)
    + sin(30°)  sin(210°)
    + sin(-25°) sin(335°)

Numerically:

    Sy = +0.0917821063

Therefore, the complete Cartesian resultant is:

    X(phi)
    =
    -0.0917821063 cos(phi)
    +0.1093816549 sin(phi)

    Y(phi)
    =
    +0.1093816549 cos(phi)
    +0.0917821063 sin(phi)

Rounded to six decimal places:

    X(phi)
    =
    -0.091782 cos(phi)
    +0.109382 sin(phi)

    Y(phi)
    =
    +0.109382 cos(phi)
    +0.091782 sin(phi)

Thus the numerical coefficients arise directly from the four magistrale directions:

    (60°, 130°, 210°, 335°)

and their signed deviations:

    (+60°, -50°, +30°, -25°)

They are not fitted to the solar result.

---

## 4. Magnitude of the resultant

The magnitude of the resultant is:

    R = sqrt(X² + Y²)

For clarity, define:

    a = 0.0917821063
    b = 0.1093816549

Then:

    X = -a cos(phi) + b sin(phi)

    Y =  b cos(phi) + a sin(phi)

Therefore:

    R² = X² + Y²

Substituting X and Y:

    R²
    =
    [-a cos(phi) + b sin(phi)]²
    +
    [ b cos(phi) + a sin(phi)]²

Expanding the first term:

    [-a cos(phi) + b sin(phi)]²
    =
    a² cos²(phi)
    - 2ab cos(phi) sin(phi)
    + b² sin²(phi)

Expanding the second term:

    [b cos(phi) + a sin(phi)]²
    =
    b² cos²(phi)
    + 2ab cos(phi) sin(phi)
    + a² sin²(phi)

Adding them gives:

    R²
    =
    a² cos²(phi)
    - 2ab cos(phi) sin(phi)
    + b² sin²(phi)
    + b² cos²(phi)
    + 2ab cos(phi) sin(phi)
    + a² sin²(phi)

The two mixed terms cancel exactly:

    -2ab cos(phi) sin(phi)
    +
     2ab cos(phi) sin(phi)
    =
    0

Therefore:

    R²
    =
    a²[cos²(phi) + sin²(phi)]
    +
    b²[cos²(phi) + sin²(phi)]

Since:

    cos²(phi) + sin²(phi) = 1

we obtain:

    R² = a² + b²

Therefore:

    R
    =
    sqrt(a² + b²)

or:

    R
    =
    sqrt(
        0.0917821063²
        +
        0.1093816549²
    )

Numerically:

    R = 0.1427876097

Rounded to six decimal places:

    R = 0.142788

The important result is:

    R does not depend on phi.

The phase changes the direction of the resultant, but it does not change its magnitude.

---

## 5. Why the resultant describes a circle

For every value of phi:

    X² + Y² = R²

and:

    R = 0.142788

Therefore:

    X² + Y² = 0.142788²

This is the equation of a circle centered at the origin.

The circular form is therefore not introduced as an assumption.

It follows directly from the phase-dependent sum of the four magistrales.

The direction of the resultant can be written approximately as:

    theta(phi) ≈ 130° - phi

As phi passes through one complete cycle:

    0° → 360°

the endpoint of the resultant makes one complete rotation while remaining at the constant radius:

    R = 0.142788

A quarter-cycle produces a 90° rotation:

    phi → phi + 90°

    theta → theta - 90°

A half-cycle produces the opposite vector:

    phi → phi + 180°

    theta → theta - 180°

Directly from the Cartesian equations:

    X(phi + 180°) = -X(phi)

    Y(phi + 180°) = -Y(phi)

Therefore:

    Rvec(phi + 180°) = -Rvec(phi)

The vector has reached the opposite side of the same circle.

Its magnitude has not changed:

    |Rvec(phi + 180°)| = |Rvec(phi)| = 0.142788

After a complete cycle:

    Rvec(phi + 360°) = Rvec(phi)

Thus the phase-dependent resultant is a 360° rotating vector of constant magnitude.

---

## 6. The 0°/180° system axis

The derivation above uses the 0°/180° system axis.

The directions:

    0° and 180°

are opposite directions of the same straight axis:

    0° <-> 180°

This distinction is important.

The resultant is a directed vector and therefore completes a full cycle over 360°.

The underlying geometrical axis is bidirectional:

    0° <-> 180°

After half a cycle, the vector has changed direction but occupies the opposite direction of the same axis.

Therefore:

    Rvec(phi + 180°) = -Rvec(phi)

while:

    |Rvec(phi + 180°)| = |Rvec(phi)|

If the signed projection of the resultant onto an axis is represented by P, its two extrema are:

    Pmax = +R

    Pmin = -R

Numerically:

    Pmax = +0.142788

    Pmin = -0.142788

The two opposite states are therefore not two independently introduced amplitudes.

They are the two signed extrema of the same circular phase resultant.

---

## 7. MASTER–FEEDBACK angular scale

The MASTER–FEEDBACK line has not been used in deriving X, Y, or R.

It enters only at this stage.

The previously calculated MASTER–FEEDBACK distance is approximately:

    D = 18,117 km

Expressed as a great-circle angular separation:

    Da ≈ 162.92°

Within the model, this angular separation is used as the scale onto which the dimensionless resultant R is transferred.

The corresponding maximum displacement is defined as:

    A = Da × R

Therefore:

    A
    =
    162.92° × 0.142788

which gives:

    A ≈ 23.263°

Because the circular resultant reaches the two opposite directions of an axis, the signed extrema are:

    +A ≈ +23.263°

and:

    -A ≈ -23.263°

Thus the geometrical model produces:

    -23.263° <-> 0° <-> +23.263°

or, rounded:

    A ≈ ±23.26°

---

## 8. Comparison with the Tropics

Only after obtaining the geometrical result above is it compared with the geographical positions of the Tropics.

Approximate present absolute latitude of the Tropics:

    23.44°

Calculated model amplitude:

    23.263°

Absolute difference:

    delta
    =
    23.44° - 23.263°

    delta ≈ 0.177°

Relative difference:

    delta_rel
    =
    (0.177 / 23.44) × 100

    delta_rel ≈ 0.76%

Therefore:

    Model geometry:       ±23.26°
    Approximate Tropics:  ±23.44°
    Difference:            0.177° ≈ 0.76%

The geographical position of the Tropics was not used to determine the Cartesian coefficients, R, or the MASTER–FEEDBACK angular scale.

---

## 9. Interpretation within the model

The value:

    R = 0.142788

is produced by the phase-dependent vector combination of the four previously defined magistrales relative to the 0°/180° system axis.

The mathematical sequence is:

    M1, M2, M3, M4
        ↓
    signed deviations Δ1, Δ2, Δ3, Δ4
        ↓
    Ai(phi) = cos(phi - Δi)
        ↓
    X(phi), Y(phi)
        ↓
    R = sqrt(X² + Y²)
        ↓
    R = 0.142788

The constant magnitude means that the phase evolution produces a circular resultant rather than a changing radial amplitude.

The 0°/180° geometry also shows that the two opposite extrema are opposite directions of the same axis:

    +R <-> -R

Only after this result is obtained is the MASTER–FEEDBACK angular separation introduced:

    R = 0.142788
        ↓
    Da = 162.92°
        ↓
    A = Da × R
        ↓
    A ≈ ±23.26°

Within the model presented in *Measurable Science*, this quantity is interpreted as the range of the global synchronization point.

It does not represent the physical trajectory of a single Sun across the entire Earth.

The global synchronization point is treated as a phase address from which local regions can form their local solar points.

The comparison with the Tropics is therefore made after the mathematical result has been obtained, rather than being used as an input to the calculation.

---

## Numerical summary

Four magistrales:

    M1 = 60°
    M2 = 130°
    M3 = 210°
    M4 = 335°

System axis:

    0° <-> 180°

Signed deviations:

    Δ1 = +60°
    Δ2 = -50°
    Δ3 = +30°
    Δ4 = -25°

Phase amplitude:

    Ai(phi) = cos(phi - Δi)

Cartesian resultant:

    X(phi)
    =
    -0.0917821063 cos(phi)
    +0.1093816549 sin(phi)

    Y(phi)
    =
    +0.1093816549 cos(phi)
    +0.0917821063 sin(phi)

Rounded:

    X(phi)
    =
    -0.091782 cos(phi)
    +0.109382 sin(phi)

    Y(phi)
    =
    +0.109382 cos(phi)
    +0.091782 sin(phi)

Magnitude:

    R = sqrt(X² + Y²)

    R = 0.1427876097

    R ≈ 0.142788

Direction:

    theta(phi) ≈ 130° - phi

Half-cycle:

    Rvec(phi + 180°) = -Rvec(phi)

Full cycle:

    Rvec(phi + 360°) = Rvec(phi)

MASTER–FEEDBACK:

    Distance ≈ 18,117 km

    Angular separation ≈ 162.92°

Model displacement:

    A = 162.92° × 0.142788

    A ≈ 23.263°

Calculated range:

    -23.26° <-> +23.26°

Approximate Tropics:

    -23.44° <-> +23.44°

Difference:

    0.177° ≈ 0.76%