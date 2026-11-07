

# Reference [C] — Formation of the Atom: Magnetic Relations, Spiral Electric Current, Electromagnetic Feedback and Photon Emission

## 1. Purpose and scope

Reference [A] introduces a mathematical framework in which fundamental units carry potential, while energy becomes manifested through their relations.

Reference [B] connects organized relational energy with the measured mass, magnetic moment and precession of the neutron.

Reference [C] examines the next proposed stage: the formation of the atom.

In the author's model, the neutron is a generator of matter, while the atom represents the first complete form of matter.

The proposed sequence is:

**MAGNETISM → MOTION → SPIRAL ORGANIZATION → ELECTROMAGNETIC INDUCTION → ELECTRIC CURRENT → ELECTROMAGNETIC FEEDBACK → ORGANIZED ATOMIC FORM → PHOTON EMISSION.**

The central question is:

**Can magnetic interactions contribute to the formation of a transient spiral electric current during proton–electron binding, and can electromagnetic feedback participate in the emergence of an organized atomic state?**

This reference examines that possibility through established electromagnetic equations, quantum current density, measured hydrogen properties and energy conservation.

The proposed electromagnetic shell is treated as an organizational concept within the model, not as a separately established physical membrane surrounding the atom.

---

## 2. Measured properties of the proton–electron system

### 2.1 Fundamental constants

The following values are based on the CODATA 2022 recommended constants.

| Quantity | Symbol | Value |
|---|---|---|
| Elementary charge | e | 1.602176634 × 10⁻¹⁹ C |
| Electron mass | m_e | 9.1093837139 × 10⁻³¹ kg |
| Proton mass | m_p | 1.67262192595 × 10⁻²⁷ kg |
| Electron magnetic moment, magnitude | abs(μ_e) | 9.2847646917 × 10⁻²⁴ J/T |
| Proton magnetic moment | μ_p | 1.41060679736 × 10⁻²⁶ J/T |
| Planck constant | h | 6.62607015 × 10⁻³⁴ J·s |
| Reduced Planck constant | ħ | h/(2π) |
| Speed of light | c | 299792458 m/s |
| Bohr radius | a₀ | approximately 5.291772105 × 10⁻¹¹ m |

Source: [NIST — CODATA Recommended Values](https://physics.nist.gov/constants)

The proton and electron possess opposite electric charges:

```text
q_p = +e

q_e = -e
```

Both particles also possess magnetic moments.

Their electric and magnetic properties allow them to participate in electromagnetic interactions.

### 2.2 Center of mass

For proton position `r_p` and electron position `r_e`, define:

```text
R = (m_p*r_p + m_e*r_e)/(m_p + m_e)

r = r_e - r_p
```

The reduced mass is:

```text
mu_red = (m_p*m_e)/(m_p + m_e)
```

Their individual coordinates relative to the center of mass satisfy:

```text
r_e - R = (m_p/(m_p + m_e))*r

r_p - R = -(m_e/(m_p + m_e))*r
```

Thus, proton and electron motion can be described through a common center of mass and a relative coordinate.

Because their masses differ greatly, any proposed spiral organization of their relative motion does not imply two identical geometrical spirals.

---

## 3. Magnetic interaction between proton and electron

### 3.1 Magnetic dipole interaction

In the classical point-dipole approximation, the magnetic interaction energy is:

```text
U_mag = (mu_0/(4*pi*r^3)) *
        [mu_p·mu_e - 3*(mu_p·r_hat)*(mu_e·r_hat)]
```

Here:

- `mu_p` and `mu_e` are magnetic-moment vectors.
- `r` is their separation.
- `r_hat` is the unit vector along their separation.
- `mu_0` is the vacuum permeability.

The interaction depends on both separation and orientation.

For fixed orientations, its radial force component is:

```text
F_r = -dU_mag/dr

F_r = 3*U_mag/r
```

The sign and magnitude depend on the configuration of the magnetic moments.

This provides a mathematical example of an interaction whose response changes with relative orientation.

In Reference [A], the proposed minimal phase-dependent relational interaction is:

```text
U_ij = -K_ij*cos(phi_ij)

K_ij = G(P_i, P_j)
```

Both expressions describe orientation-dependent energy, although their full mathematical structures and physical interpretations differ.

The comparison supports the use of angular interactions in the relational model without identifying fundamental units with conventional magnetic dipoles.

### 3.2 Relative strength of magnetic and electric forces

At the characteristic hydrogen distance:

```text
r = a_0
```

the classical magnetic dipole energy scale is:

```text
U_mag,scale = (mu_0/(4*pi)) *
              abs(mu_p*mu_e)/a_0^3
```

Numerically:

```text
U_mag,scale ≈ 8.84 × 10^-26 J

U_mag,scale ≈ 5.52 × 10^-7 eV
```

The corresponding radial force scale is:

```text
F_mag,scale = 3*U_mag,scale/a_0

F_mag,scale ≈ 5.01 × 10^-15 N
```

For comparison, the electrostatic force magnitude is:

```text
F_C = e^2/(4*pi*epsilon_0*a_0^2)

F_C ≈ 8.24 × 10^-8 N
```

Therefore:

```text
F_mag,scale/F_C ≈ 6.08 × 10^-8
```

At this distance, the classical magnetic dipole force scale is approximately 16 million times smaller than the electrostatic force.

This comparison establishes an important quantitative condition for the proposed model.

If magnetic interactions play a decisive organizational role during atomic formation, that role must be demonstrated through the system's dynamics rather than assumed from the existence of magnetic moments alone.

The comparison is an order-of-magnitude estimate. A complete quantum treatment must include the relevant spin interactions, including the contact contribution to hydrogen hyperfine structure.

---

## 4. Experimental evidence of magnetic interaction

### 4.1 Hydrogen hyperfine transition

The ground state of hydrogen contains two hyperfine configurations associated with the coupled electron and proton spins.

Their energy separation corresponds to the approximately 21-centimeter transition.

The measured frequency is approximately:

```text
f_H = 1,420,405,751.8 Hz
```

The corresponding energy difference is:

```text
Delta_E = h*f_H

Delta_E ≈ 9.41 × 10^-25 J

Delta_E ≈ 5.87 × 10^-6 eV
```

The associated period is:

```text
T = 1/f_H

T ≈ 7.04 × 10^-10 s
```

This establishes a measurable connection between the magnetic properties of the proton–electron system and its energy levels.

The transition frequency represents the frequency associated with the energy difference. It is not automatically the mechanical rotation frequency of either particle or the frequency of a spiral current.

For the proposed model, its importance is that an electrically neutral atom possesses measurable energy differences associated with the magnetic organization of its constituents.

Sources:

- [NIST — Hydrogen Hyperfine Transition](https://tf.nist.gov/general/pdf/2060.pdf)
- [NRAO — Hydrogen 21-cm Line](https://www.cv.nrao.edu/~sransom/web/Ch7.html)

---

## 5. Electromagnetic induction and the origin of current

### 5.1 Faraday's law

Maxwell–Faraday induction is described by:

```text
curl(E) = -dB/dt
```

Its integral form is:

```text
closed_integral(E·dl) = -dPhi_B/dt
```

where `Phi_B` represents magnetic flux through the chosen surface.

A time-dependent magnetic field can therefore generate a circulating electric field.

The electromagnetic sequence is:

**CHANGING MAGNETIC FIELD → INDUCED ELECTRIC FIELD → POSSIBLE CHARGE TRANSPORT.**

The final step depends on the presence and response of charged particles.

In the proposed atomic formation process, the relevant charges already exist: the proton and electron.

### 5.2 Electromagnetic force

In the classical approximation, the force on a charged particle is:

```text
F = q*(E + v × B)
```

An electromagnetic field can change the particle's motion.

Changing motion can alter the corresponding electric current, which in turn contributes to electromagnetic fields.

The author's proposed mechanism uses this mutual dependence as a possible route toward an organized atomic form.

The next question is whether the resulting current can possess spiral geometry.

---

## 6. Mathematical construction of a spiral electric current

### 6.1 Current density

For a classical charge distribution, electric current density is:

```text
J = rho*v
```

where:

- `rho` is electric charge density.
- `v` is velocity.

In cylindrical coordinates:

```text
J = J_r*r_hat + J_phi*phi_hat + J_z*z_hat
```

The components describe:

- `J_r`: radial transport.
- `J_phi`: azimuthal or circular transport.
- `J_z`: axial transport.

A planar flow with nonzero radial and azimuthal components can possess spiral streamlines.

### 6.2 Derivation of spiral geometry

For a planar current field, the streamline equation is:

```text
dr/dphi = r*(J_r/J_phi)
```

Suppose that, in the region considered:

```text
J_r/J_phi = k
```

where `k` is constant.

Then:

```text
dr/dphi = k*r
```

Separating variables:

```text
dr/r = k*dphi
```

Integration gives:

```text
ln(r/r_0) = k*(phi - phi_0)
```

Therefore:

```text
r(phi) = r_0*exp(k*(phi - phi_0))
```

**This is the equation of a logarithmic spiral.**

The result establishes that a current with an appropriate relationship between its radial and azimuthal components can form a spiral pattern.

The parameter `k` determines the character of that spiral:

- `k > 0`: radius increases with increasing angle.
- `k < 0`: radius decreases with increasing angle.
- `k = 0`: circular flow with constant radius.

This mathematical result gives a precise meaning to spiral current organization.

It does not require every microscopic charge carrier to follow a sharply defined classical trajectory. The spiral may describe the streamlines of a collective current field.

### 6.3 Conservation of charge

Any physically acceptable electric current must satisfy the continuity equation:

```text
d(rho)/dt + div(J) = 0
```

The equation expresses conservation of electric charge.

A stationary bound state cannot sustain an uncompensated net radial charge flux through every enclosing surface.

However, a transient current during the formation of a bound state can contain radial components while the charge distribution changes.

This distinction is central:

**THE CURRENT DURING FORMATION NEED NOT BE IDENTICAL TO THE CURRENT OF THE FINAL ORGANIZED STATE.**

---

## 7. Quantum currents during atomic transformation

### 7.1 Stationary hydrogen ground state

In a nonrelativistic approximation, the spatial wavefunction of the hydrogen ground state is:

```text
psi_1s(r) = exp(-r/a)/(sqrt(pi)*a^(3/2))
```

where `a` includes the reduced-mass correction.

The orbital probability-current density is:

```text
j = (hbar/mu_red)*Im[psi_conj*grad(psi)]
```

Here `psi_conj` denotes the complex conjugate of the wavefunction.

For a real stationary `1s` spatial wavefunction:

```text
j_orbital = 0
```

The orbital probability current therefore vanishes in this representation.

Spin-related magnetization currents are a separate contribution.

The absence of a radial orbital current in the stationary ground state does not establish that radial currents are absent during the earlier formation process.

### 7.2 Transient current from a quantum superposition

Consider a coherent superposition of two hydrogen states:

```text
Psi(r,t) =
    a*psi_1s(r)*exp(-i*E_1*t/hbar)
  + b*psi_2p(r)*exp(-i*E_2*t/hbar)
```

The coefficients `a` and `b` are complex amplitudes.

For simplicity, take real spatial orbitals and omit spin and vector-potential contributions in this example.

The probability-current density is:

```text
j = (hbar/mu_red)*Im[Psi_conj*grad(Psi)]
```

The interference contribution becomes:

```text
j = (hbar/mu_red) *
    Im[a_conj*b*exp(-i*(E_2-E_1)*t/hbar)] *
    [psi_1s*grad(psi_2p)
     - psi_2p*grad(psi_1s)]
```

This expression can be nonzero.

Because the two spatial orbitals have different radial and angular dependences, their interference can generate local current components absent from the individual stationary states.

**MATHEMATICAL RESULT: A time-dependent quantum superposition can produce local current during a transformation even when its individual stationary components carry no orbital current in the chosen representation.**

This example demonstrates the mathematical possibility of transient current.

It does not independently establish the complete spiral geometry or describe the full process of proton–electron capture.

---

## 8. The proposed spiral during atomic formation

The author proposes that, during the organization of a proton–electron system, changing electromagnetic relations can generate a transient current containing both radial and azimuthal components.

Let:

```text
J(r,t) = J_r(r,t)*r_hat
       + J_phi(r,t)*phi_hat
       + J_z(r,t)*z_hat
```

A spiral organization requires, over an appropriate region:

```text
J_r != 0

J_phi != 0
```

together with a spatial relationship that produces spiral streamlines.

The proposed sequence is:

**MAGNETIC INTERACTION → CHANGING MOTION → RADIAL AND AZIMUTHAL CURRENT → SPIRAL ORGANIZATION.**

The hypothesis concerns the process of forming the atom, not the requirement that the completed atom sustain a permanent inward spiral current.

The mathematical construction in Section 6 demonstrates how spiral current geometry can arise from the relevant current components.

The quantum example in Section 7 demonstrates that transient currents are compatible with time-dependent quantum states.

Together, these results establish a mathematical framework within which the proposed formation process can be examined.

### 8.1 The role of relative phase

In quantum mechanics, observable interference effects depend on physically relevant relative phases between states.

A global phase has no observable consequence, but a relative phase between coherent components can influence the current density.

This offers a possible connection to the phase-dependent relational construction introduced in Reference [A].

For that connection to become quantitative, the model must relate:

```text
Internal phase relation
          ↓
Electromagnetic interaction
          ↓
Relative phase of physical states
          ↓
Charge-current distribution
```

The proposed spiral requires the resulting current field to possess a suitable combination of radial and azimuthal components.

### 8.2 Distinguishing magnetic and electric contributions

The proton and electron interact through both electric and magnetic effects.

Their dominant long-range binding interaction is electric.

To examine the proposed organizational role of magnetism, a numerical calculation can compare:

```text
Case 1:
Electric interaction and radiation

Case 2:
Electric interaction, magnetic spin coupling and radiation
```

The difference between the resulting current distributions can isolate the contribution of magnetic coupling within the chosen physical approximation.

This provides a practical test of the proposed mechanism.

---

## 9. Electromagnetic feedback and organized form

### 9.1 Maxwell–Ampère equation

The relationship between electric current and magnetic field is described by:

```text
curl(B) = mu_0*J
        + mu_0*epsilon_0*dE/dt
```

Together with Faraday's law:

```text
curl(E) = -dB/dt
```

these equations describe a coupled electromagnetic system.

A changing current affects the magnetic field.

A changing magnetic field can induce an electric field.

The resulting electromagnetic fields can act back on charged matter.

Thus:

**MOTION CHANGES THE FIELD, AND THE FIELD ACTS ON MOTION.**

This is the physical basis for examining electromagnetic feedback during the proposed organization of the atom.

### 9.2 Electromagnetic energy

The energy density of the classical electromagnetic field is:

```text
u_EM = 0.5*epsilon_0*E^2
     + B^2/(2*mu_0)
```

The electromagnetic energy flux is represented by the Poynting vector:

```text
S = (1/mu_0)*(E × B)
```

Poynting's theorem states:

```text
d(u_EM)/dt + div(S) = -J·E
```

The equation relates:

- Changes in electromagnetic field energy.
- Energy transported by electromagnetic fields.
- Energy exchanged between fields and charged matter.

It therefore supplies a quantitative framework for analyzing energy transfer during the proposed formation process.

### 9.3 Electromagnetic organization

The author proposes that an appropriately organized electromagnetic feedback process can contribute to the formation of a stable atomic structure.

The proposed **electromagnetic shell** represents the resulting organization of relations.

It is not necessary for the final organized form to preserve every component of the motion involved in its formation.

In particular, the radial current associated with the transition may diminish or disappear as the system approaches a stationary bound state.

The proposed shell must correspond to a well-defined charge and current configuration whose properties can be examined mathematically.

A self-consistent electromagnetic configuration is not automatically stable. Stability requires examining how the configuration responds to disturbances and whether it possesses an appropriate bound-state energy structure.

The known hydrogen spectrum provides the experimental target for such an examination.

---

## 10. Photon emission and the formation of hydrogen

### 10.1 Radiative recombination

A proton and electron can form a hydrogen atom through radiative recombination:

```text
p + e^- -> H + gamma
```

The photon carries away energy and momentum.

This allows the system to make a transition from an unbound configuration to a bound atomic state while conserving total energy and momentum.

The process is experimentally established.

### 10.2 Energy conservation

Let:

```text
K_i = initial relative kinetic energy

E_bind = binding energy of the final atomic state

E_recoil = recoil kinetic energy of the atom
```

Then, in the initial center-of-mass frame and neglecting small corrections:

```text
E_gamma = K_i + E_bind - E_recoil
```

For formation of the hydrogen ground state:

```text
E_bind ≈ 13.5984 eV
```

If the initial relative kinetic energy is small, the emitted photon energy is close to the binding energy, with a small recoil correction.

The exact emission energy depends on the initial and final states.

### 10.3 Interpretation within the proposed model

The author interprets photon emission as a possible measurable manifestation of the transition into a newly organized form.

The proposed sequence is:

**CHANGING RELATIONS → ENERGY REDISTRIBUTION → ORGANIZED ATOMIC STATE + EMITTED PHOTON.**

In the language of the model:

**THE FLASH MARKS THE TRANSFORMATION. THE ORGANIZATION THAT REMAINS REPRESENTS THE FORM.**

The observed photon carries energy released during the transition.

The proposed electromagnetic shell is an additional interpretation of the resulting atomic organization and requires its own mathematical description.

---

## 11. Transformation and the recurrence of fundamental constituents

The author's proposed organizational sequence is:

**NEUTRINO → NEUTRON → ATOM.**

Known particle transformations provide a useful comparison.

### 11.1 Electron capture

In an energetically allowed nuclear electron-capture process, the local weak-interaction transformation is:

```text
p + e^- -> n + nu_e
```

In an actual nucleus, the process involves a parent nucleus transforming into a daughter nucleus.

The nuclear environment and the available energy determine whether electron capture can occur.

Source: [11 — Electron Capture](https://github.com/MeasurableScience/measurable-science/blob/main/References/011-electron-capture.md)

### 11.2 Free-neutron beta decay

A free neutron can undergo beta decay:

```text
n -> p + e^- + anti_nu_e
```

This is an experimentally established weak-interaction process.

The appearance of neutrinos and antineutrinos in these transformations is among the observations motivating the author's investigation of neutrino relations and matter organization.

The known decay processes do not establish that a neutron is assembled from neutrinos or that atomic binding results from the specific spiral mechanism proposed here.

Within the model, the reactions are examined as examples of how changing relations can correspond to different organized states and transformations.

**FORMATION AND DECAY ARE DIFFERENT OUTCOMES OF CHANGING ORGANIZATION.**

---

## 12. Quantitative test of the proposed spiral mechanism

The mathematical description can be developed into a numerical test focused on the formation process.

The test must examine whether the proposed current organization emerges from specified physical interactions.

### 12.1 Initial conditions

Specify an initially unbound proton–electron system with:

```text
Initial relative separation: r_0

Initial relative momentum: p_0

Electron spin state: s_e

Proton spin state: s_p

Initial orbital angular momentum: L_0

Initial electromagnetic state: EM_0
```

### 12.2 Dynamical model

A nonrelativistic quantum approximation can be written schematically as:

```text
H = H_kinetic
  + H_Coulomb
  + H_spin_orbit
  + H_spin_spin
  + H_other_corrections
  + H_radiation
```

The terms must be introduced consistently to avoid counting the same interaction more than once.

The inclusion of radiation is necessary for modeling spontaneous photon emission during capture.

The evolving quantum state satisfies:

```text
i*hbar*dPsi/dt = H*Psi
```

From the evolving state, calculate the charge density and current density:

```text
rho(r,t)

J(r,t)
```

The current must include the appropriate orbital and spin contributions for the chosen approximation.

### 12.3 Identifying spiral organization

Decompose the current:

```text
J_r(r,t)

J_phi(r,t)

J_z(r,t)
```

A useful local diagnostic is:

```text
Q(r,t) = abs(J_r*J_phi)
```

A nonzero value identifies regions containing simultaneous radial and azimuthal current components.

However:

```text
Q > 0
```

does not by itself establish a coherent spiral.

The current streamlines must also be examined.

A genuine spiral structure should emerge from the calculated current field rather than being imposed through the initial conditions.

### 12.4 Magnetic contribution

Compare the calculated current with and without the selected magnetic spin interactions, while preserving the consistency of the approximation.

Define:

```text
Delta_J = J_with_magnetic_coupling
        - J_reference
```

The result can show whether magnetic coupling produces a distinctive contribution to the radial–azimuthal current structure.

### 12.5 Energy and photon emission

Calculate:

```text
E_matter(t)

E_field(t)

E_radiation(t)
```

The total energy balance must satisfy:

```text
E_initial = E_final + E_emitted
```

with recoil and other relevant contributions included.

The emitted photon energy and its dependence on the initial state can then be compared with established hydrogen spectroscopy and recombination calculations.

A successful model should connect the current organization, electromagnetic energy transfer and final bound state within one consistent calculation.

---

## 13. Established results and proposed mechanisms

| Statement | Status |
|---|---|
| Proton and electron possess electric charges and magnetic moments | Measured |
| Their magnetic interactions contribute to hydrogen hyperfine structure | Established |
| Hydrogen exhibits the approximately 1420.4 MHz hyperfine transition | Measured |
| A changing magnetic field induces an electric field | Established |
| Moving electric charge produces current | Established |
| Suitable radial and azimuthal current components can form spiral streamlines | Mathematical result |
| Time-dependent quantum states can produce transient current | Mathematical result |
| Magnetic coupling initiates the proposed spiral current during hydrogen formation | Model hypothesis |
| Electromagnetic feedback contributes to the proposed atomic shell | Model hypothesis |
| Proton–electron radiative recombination can emit a photon | Established |
| The photon marks the proposed organizational transformation | Model interpretation |
| Electron capture and neutron beta decay occur | Established |

This distinction identifies which elements of the proposed mechanism are grounded in measurement, which follow mathematically under stated assumptions, and which form the author's physical interpretation.

---

## 14. Conclusion

References [A], [B] and [C] examine successive levels of the proposed relational model.

Reference [A] describes the manifestation of potential through relations and the mathematical possibility of organized forms.

Reference [B] connects organized energy to the measurable properties of the neutron.

Reference [C] examines whether electromagnetic interactions can organize the motion of charged constituents during the formation of an atom.

Several mathematical and experimental results are directly relevant.

The proton and electron possess measurable magnetic moments.

Their magnetic interaction contributes to the hydrogen hyperfine spectrum.

Faraday's law relates changing magnetic fields to induced electric fields.

The motion of electric charge produces current, and a current containing suitable radial and azimuthal components can form a spiral.

Time-dependent quantum states can possess transient currents that are absent from their corresponding stationary components.

Maxwell's equations describe the feedback between electromagnetic fields and moving charge.

Finally, proton–electron binding can occur through a process in which a photon carries away released energy.

These results provide a mathematical framework for examining the author's proposed sequence:

**MAGNETISM → MOTION → SPIRAL CURRENT → ELECTROMAGNETIC FEEDBACK → ORGANIZED ATOMIC FORM → PHOTON EMISSION.**

The central hypothesis is that changing electromagnetic relations can contribute to a transient spiral current whose feedback participates in the formation of an organized atomic state.

The decisive quantitative investigation is to calculate the time-dependent current during proton–electron binding and determine whether the proposed spiral structure emerges from the dynamics.

The model therefore connects its organizational principle to measurable atomic properties and to explicit equations governing electromagnetic interactions, quantum currents and photon emission.

**THE PRINCIPLE DOES NOT CHANGE. WHAT ENTERS INTO RELATION CHANGES.**

---

## 15. Sources and related references

**[A]** [Mathematical Model of Potential, Relations, Energy and Organization](https://github.com/MeasurableScience/measurable-science/blob/main/References/A-mathematical-model.md)

**[B]** [Neutron Magnetic Moment, Energy and Precession](https://github.com/MeasurableScience/measurable-science/blob/main/References/B-neutron-magnetism-energy-precession.md)

**[8]** [Neutron](https://github.com/MeasurableScience/measurable-science/blob/main/References/008-neutron.md)

**[10]** [Ancient Atomism](https://github.com/MeasurableScience/measurable-science/blob/main/References/010-ancient-atomism.md)

**[11]** [Electron Capture](https://github.com/MeasurableScience/measurable-science/blob/main/References/011-electron-capture.md)

**NIST — CODATA 2022:** [Fundamental Physical Constants](https://physics.nist.gov/constants)

**NIST:** [Atomic Spectra Database](https://physics.nist.gov/asd)

**NIST:** [Atomic Data for Hydrogen](https://physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable1.htm)

**NIST:** [Hydrogen Hyperfine Transition Measurement](https://tf.nist.gov/general/pdf/2060.pdf)

**NRAO:** [Essential Radio Astronomy — Hydrogen 21-cm Line](https://www.cv.nrao.edu/~sransom/web/Ch7.html)

**OpenStax:** [Maxwell's Equations and Electromagnetic Waves](https://openstax.org/books/university-physics-volume-2/pages/16-1-maxwells-equations-and-electromagnetic-waves)

