# Reference 108 — Phased Array Phase Steering

## Purpose

This reference documents the established phased-array principle used as a technical analogy in *Measurable Science*.

The relevant principle is simple:

A set of spatially separated elements does not need to move physically in order to move the direction of maximum constructive interference.

The direction of the maximum can be changed by changing the relative phase between the elements.

---

## Source

Peter Delos, Bob Broughton, Jon Kraft

"Phased Array Antenna Patterns—Part 1: Linear Array Beam Characteristics and Array Factor"

Analog Devices, Analog Dialogue.

Source:

https://www.analog.com/en/resources/analog-dialogue/articles/phased-array-antenna-patterns-part1.html

---

## Established phased-array principle

Analog Devices describes beam steering using multiple spatially separated antenna elements.

A time delay or an equivalent phase shift is introduced between neighboring elements.

When the phase relationship corresponds to a particular direction, the signals arrive in phase at the point of combination and add coherently.

This produces a maximum response in that direction.

Changing the relative phase changes the direction of this maximum without requiring physical movement of the antenna elements.

For two neighboring elements separated by distance d, the propagation-path difference for beam angle θ is:

L = d sin θ

For wavelength λ, this path difference can be represented as a phase difference:

ΔΦ = 2πd sin θ / λ

Therefore the direction θ of the maximum is directly related to the relative phase ΔΦ between the elements.

The physical positions of the elements remain fixed.

What changes is their phase relationship, and therefore the spatial direction in which constructive interference occurs.

---

## Constructive interference

For a simplified two-element system:

E₁ = A₁ cos(ωt + φ₁)

E₂ = A₂ cos(ωt + φ₂)

The relative phase is:

Δφ = φ₂ − φ₁

Changing Δφ changes the spatial conditions under which the two waves arrive in phase.

Where they arrive in phase, they add constructively and produce a maximum.

Thus:

fixed spatial elements
→ controlled phase difference
→ constructive interference
→ movable maximum

No mechanical movement of the individual elements is required.

---

## Relation to the model

The established phased-array principle above does not demonstrate that mountains form a phased-array antenna or that they produce a solar point.

That is the hypothesis tested in *Measurable Science*.

The technical analogy is used because the geometry identified around Glaveja contains spatially separated elements with different orientations:

Blagotini
→ polar/reference input

Glaveja
→ combining/resonant point

Kremenci
→ local phase elements

Within the model, the proposed sequence is:

global phase
→ local reference
→ Glaveja
→ phase relationship of local elements
→ spatial constructive maximum

The hypothesis is that changing the phase relationship can move the position of this maximum while the physical elements themselves remain stationary.

In the model, this moving constructive maximum is interpreted as the local solar point.

---

## Testable consequence

If the Kremenac pair participates only within a particular phase range, its contribution should not be equally strong throughout the entire annual cycle.

The model therefore predicts that entering or leaving the Kremenac working range should produce a measurable change in the local radiation regime.

This prediction can be tested independently against measured radiation data.

---

## What this reference supports

This source supports:

- beam steering by relative phase shift;
- coherent addition of signals;
- constructive interference producing a directional maximum;
- changing beam direction without mechanically moving the antenna elements;
- the mathematical relationship between element spacing, wavelength, phase difference and beam direction.

It does not independently support:

- the identification of Glaveja, Blagotini or Kremenci as antenna elements;
- the existence of local solar points;
- the proposed natural-computer architecture.

Those are hypotheses of the model and are tested separately.