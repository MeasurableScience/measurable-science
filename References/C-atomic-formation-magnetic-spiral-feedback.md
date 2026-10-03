# Reference [C] — Formation of the Atom: Magnetic Relations, Spiral Electric Current, Electromagnetic Feedback, and Photon Emission

## 1. Purpose and scope

This reference examines the proposed sequence:

**Magnetism → spiral organization of electric current → electromagnetic feedback → stable atomic form → photon emission.**

The central question is not whether a completed hydrogen atom continuously contains an inward or outward radial electric current.

Instead, the question is:

**Can a transient spiral current arise during the formation of a bound proton–electron system, and can electromagnetic feedback contribute to the transition into a stable atomic state?**

The distinction between a formation process and its final state is essential.

A transient radial current may exist during a transformation without remaining present in the final stationary state. However, its existence must be derived from a dynamical model rather than assumed.

Three categories of statements are kept separate throughout this reference:

* **MEASUREMENT:** An experimentally established quantity or phenomenon.
* **MATHEMATICAL RESULT:** A conclusion derived from specified equations and assumptions.
* **HYPOTHESIS:** A proposed physical mechanism not yet established by measurement or calculation.

The proposed *electromagnetic shell* is treated as a model concept. It must not be confused with an experimentally demonstrated, separate plasma membrane surrounding the atom.

---

## 2. Experimental quantities

### 2.1 Fundamental constants

The following rounded values are based on the CODATA 2022 recommended constants.

| Quantity                            | Symbol    | Value                                |
| ----------------------------------- | --------- | ------------------------------------ |
| Elementary charge                   | e         | 1.602176634 × 10^-19 C               |
| Electron mass                       | m_e       | 9.1093837139 × 10^-31 kg             |
| Proton mass                         | m_p       | 1.67262192595 × 10^-27 kg            |
| Electron magnetic moment, magnitude | abs(mu_e) | 9.2847646917 × 10^-24 J/T            |
| Proton magnetic moment              | mu_p      | 1.41060679736 × 10^-26 J/T           |
| Planck constant                     | h         | 6.62607015 × 10^-34 J·s              |
| Reduced Planck constant             | hbar      | h/(2*pi)                             |
| Speed of light                      | c         | 299792458 m/s                        |
| Bohr radius                         | a_0       | approximately 5.291772105 × 10^-11 m |

**Source:**

NIST — CODATA Recommended Values of the Fundamental Physical Constants: 2022

https://physics.nist.gov/constants

https://physics.nist.gov/cuu/pdf/all.pdf

**MEASUREMENT:** Both the proton and the electron possess magnetic moments.

Their magnetic moments can interact, and the interaction affects the energy levels of hydrogen.

This does not establish that the magnetic interaction is the original source of electric charge.

### 2.2 Center of mass

For proton position r_p and electron position r_e:

```text
R = (m_p*r_p + m_e*r_e)/(m_p + m_e)

r = r_e - r_p
```

The reduced mass is:

```text
mu = (m_p*m_e)/(m_p + m_e)
```

The relative coordinate r describes the separation of the particles.

Their individual positions relative to the center of mass are:

```text
r_e - R = (m_p/(m_p + m_e))*r

r_p - R = -(m_e/(m_p + m_e))*r
```

**MATHEMATICAL RESULT:** The proton and electron share a center of mass, but their distances from it are unequal.

A spiral organization of their relative motion would therefore not imply two geometrically identical spirals.

---

## 3. Magnetic relation between proton and electron

### 3.1 Classical magnetic dipole interaction

At separations where the point-dipole approximation is appropriate, the magnetic interaction energy is:

```text
U_mag = (mu_0/(4*pi*r^3)) *
        [mu_p·mu_e
        - 3*(mu_p·r_hat)*(mu_e·r_hat)]
```

Here:

* mu_p and mu_e are magnetic-moment vectors.
* r is their separation.
* r_hat is the unit vector along their separation.
* mu_0 is the vacuum permeability.

The interaction depends on distance and relative orientation.

For fixed orientations:

```text
F_r = -dU_mag/dr

F_r = 3*U_mag/r
```

Depending on the configuration, the radial magnetic force may be attractive or repulsive.

**MATHEMATICAL RESULT:** A changing magnetic relation can change the interaction energy and the direction or magnitude of the magnetic force.

This establishes a possible radial *force component*, not necessarily a radial *electric-current component*.

A force and a current are different physical quantities.

### 3.2 Order-of-magnitude comparison

At the characteristic hydrogen distance:

```text
r = a_0
```

Define the magnetic interaction scale:

```text
U_mag,scale = (mu_0/(4*pi)) *
              abs(mu_p*mu_e)/a_0^3
```

Using the constants above:

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

The magnetic force scale is approximately 16 million times smaller than the electrostatic force at this distance.

**IMPORTANT LIMITATION:** This comparison uses classical point-dipole approximations. It is not a complete calculation of the quantum magnetic interaction in hydrogen. In particular, the hyperfine interaction includes a contact contribution that cannot be represented by this simple estimate alone.

The calculation nevertheless establishes that the classical magnetic dipole force cannot be substituted for the dominant electrostatic interaction without introducing additional, testable physics.

---

## 4. Direct experimental evidence of the magnetic relation

### 4.1 Hydrogen hyperfine transition

The ground state of hydrogen contains two hyperfine energy configurations associated with the coupled electron and proton spins.

Their energy separation corresponds to the famous 21-centimeter transition:

```text
f_H ≈ 1,420,405,751.8 Hz
```

The energy difference is:

```text
Delta_E = h*f_H

Delta_E ≈ 9.41 × 10^-25 J

Delta_E ≈ 5.87 × 10^-6 eV
```

The corresponding period is:

```text
T = 1/f_H

T ≈ 7.04 × 10^-10 s
```

**MEASUREMENT:** The magnetic interaction between the electron and proton is reflected in a precisely measurable energy separation.

**Source:**

NIST — Measurement of the Unperturbed Hydrogen Hyperfine Transition Frequency

https://tf.nist.gov/general/pdf/2060.pdf

NRAO — Essential Radio Astronomy, Hydrogen 21-cm Line

https://www.cv.nrao.edu/~sransom/web/Ch7.html

### 4.2 What the frequency does and does not establish

The hyperfine frequency is the frequency corresponding to an energy difference.

It is not automatically:

* The mechanical rotation frequency of the proton.
* The mechanical rotation frequency of the electron.
* The frequency of a spiral current.
* The rate at which an atomic shell is formed.

A coherent superposition of hyperfine states can possess a time-dependent relative phase:

```text
Delta_phi(t) = Delta_phi(0) - Delta_E*t/hbar
```

However, the existence of a changing phase does not by itself prove the existence of radial charge transport.

The charge-current density must be calculated separately.

---

## 5. From changing magnetism to an electric field

### 5.1 Faraday's law

Maxwell–Faraday induction is expressed by:

```text
curl(E) = -dB/dt
```

Its integral form is:

```text
closed_integral(E·dl) = -dPhi_B/dt
```

where Phi_B is the magnetic flux through a chosen surface.

**MATHEMATICAL RESULT:** A time-varying magnetic field can produce a circulating electric field.

This is a confirmed physical mechanism.

However, three distinct quantities must not be confused:

```text
Magnetic-field variation
          |
          v
Induced electric field
          |
          v
Possible charge transport
```

The first step follows from Maxwell's equations.

The second requires a physical system containing charged degrees of freedom and a dynamical response.

A changing magnetic field does not automatically create new electric charge.

### 5.2 Charged particles and electromagnetic force

The proton and electron already possess opposite electric charges.

Their interaction with electromagnetic fields can be described, in the classical limit, by the Lorentz force:

```text
F = q*(E + v × B)
```

For the proton:

```text
q_p = +e
```

For the electron:

```text
q_e = -e
```

The force can alter the particles' motion and therefore their associated electric current.

**HYPOTHESIS:** During the formation of a bound atom, changes in the magnetic relation may contribute to a transient organization of electric current.

The proposed organization must be tested against the full electromagnetic interaction, including the dominant electric coupling.

**Source:**

OpenStax — Maxwell's Equations and Electromagnetic Waves

https://openstax.org/books/university-physics-volume-2/pages/16-1-maxwells-equations-and-electromagnetic-waves

---

## 6. What exactly is a spiral electric current?

### 6.1 Current density

For a classical distribution of charge:

```text
J = rho*v
```

where rho is charge density and v is velocity.

For a quantum particle, charge-current density is obtained from its wavefunction and electromagnetic coupling.

A current is a spatial flow of charge. It does not require that an electron be represented as a tiny classical sphere following a sharply defined trajectory.

This distinction is important for the proposed atomic model.

### 6.2 Spiral geometry

In cylindrical coordinates:

```text
J = J_r*r_hat + J_phi*phi_hat + J_z*z_hat
```

A current with nonzero radial and azimuthal components can have spiral flow lines in a plane.

For a planar flow:

```text
dr/dphi = r*(J_r/J_phi)
```

For example, if:

```text
J_r/J_phi = k
```

with constant k, then:

```text
dr/dphi = k*r
```

and integration gives:

```text
r(phi) = r_0*exp(k*(phi - phi_0))
```

This is a logarithmic spiral.

**MATHEMATICAL RESULT:** A radial current component combined with an azimuthal current component can produce a spiral current pattern.

**LIMITATION:** This is a geometrical result. It does not demonstrate that the proton–electron interaction generates the required components.

### 6.3 Charge conservation

Any proposed current must satisfy:

```text
d(rho)/dt + div(J) = 0
```

This is the continuity equation.

For a stationary, spherically symmetric bound charge distribution, a persistent net radial flux through a closed sphere is incompatible with a constant enclosed charge.

A transient radial current, however, is not excluded.

It must be accompanied by an appropriate time dependence of the charge distribution or by compensating local flows.

**This distinction is central to the proposed model: the current during formation need not equal the current in the final stationary state.**

---

## 7. Quantum test: the final state versus the formation process

### 7.1 Stationary hydrogen ground state

The spatial wavefunction of the hydrogen 1s state is approximately:

```text
psi_1s(r) = exp(-r/a)/(sqrt(pi)*a^(3/2))
```

where a includes the reduced-mass correction.

The orbital probability-current density is:

```text
j = (hbar/mu)*Im(psi*grad(psi))
```

For a real stationary 1s spatial wavefunction:

```text
j_orbital = 0
```

The associated orbital charge current is also zero.

Spin-dependent magnetization currents are a separate contribution and can possess azimuthal structure.

**MATHEMATICAL RESULT:** A stationary 1s spatial wavefunction does not contain a persistent radial orbital probability current.

**CRITICAL INTERPRETATION:** This does not establish that radial currents are absent during the earlier, time-dependent process of forming the atom.

A stationary state and a transition into that state are different physical situations.

### 7.2 A concrete example of transient quantum current

Consider a coherent superposition of two spatial hydrogen states:

```text
Psi(r,t) =
    a*psi_1s(r)*exp(-i*E_1*t/hbar)
  + b*psi_2p(r)*exp(-i*E_2*t/hbar)
```

Here a and b are complex amplitudes.

For simplicity, choose real spatial orbitals and temporarily omit spin and vector-potential contributions.

The probability-current density is:

```text
j = (hbar/mu)*Im(Psi*grad(Psi))
```

The individual stationary orbitals contribute no current in this simplified real-orbital representation.

The interference terms give:

```text
j = (hbar/mu)*
    Im[a_conj*b*exp(-i*(E_2-E_1)*t/hbar)]
    *
    [psi_1s*grad(psi_2p)
     - psi_2p*grad(psi_1s)]
```

This expression is generally nonzero.

Because the spatial orbitals have different angular and radial dependence, the interference current can contain local radial and angular components.

**MATHEMATICAL RESULT:** Time-dependent quantum superpositions can produce local charge transport that is absent in their individual stationary components.

This provides a concrete demonstration that the absence of a radial current in the final 1s state does not prohibit radial current during a transition.

**LIMITATION:** A 1s–2p superposition is not itself a calculation of proton–electron capture. Nor does this example demonstrate that the current has the particular spiral geometry predicted by the model.

The next step must therefore address the actual formation dynamics.

---

## 8. The proposed spiral during atom formation

The model predicts the following sequence:

```text
Changing magnetic relation
            |
            v
Time-dependent electromagnetic interaction
            |
            v
Radial and azimuthal current components
            |
            v
Transient spiral organization
            |
            v
Electromagnetic feedback
            |
            v
Bound atomic state
```

The third step is the decisive unverified prediction.

### 8.1 Formation-stage hypothesis

Let the electric current during formation be:

```text
J(r,t) = J_r(r,t)*r_hat
       + J_phi(r,t)*phi_hat
       + J_z(r,t)*z_hat
```

The model predicts that there is a finite time interval during which:

```text
J_r != 0

J_phi != 0
```

and their spatial organization produces a spiral flow pattern.

It further predicts that the radial component may diminish as the system approaches a stationary bound state.

These statements are **HYPOTHESES**, not consequences already derived from the known magnetic moments.

### 8.2 The role of relative phase

A changing phase may alter interference terms in a quantum current.

However, not every phase difference is physically observable.

A global phase has no observable effect. A relative phase between coherently superposed states can affect observables.

The model must specify:

1. Which physical states possess the relative phase.
2. How the magnetic interaction changes that phase.
3. How the changing phase enters the spatial charge-current density.
4. Whether the resulting current possesses both radial and azimuthal components.

Without these steps, a changing magnetic phase cannot be identified with a spiral current.

### 8.3 Why the magnetic interaction must be isolated

A calculation showing spiral motion under the complete electromagnetic force would not, by itself, establish that magnetism initiated the process.

To test that specific hypothesis, the magnetic contribution must be separated from the electric contribution.

One possible comparison is:

```text
Model A:
Electric interaction + radiation

Model B:
Electric interaction + magnetic dipole/spin coupling + radiation
```

The difference between their predicted current fields can reveal the effect of magnetic coupling.

Both models must respect conservation laws and the physical constraints of their approximations.

---

## 9. Electromagnetic feedback

### 9.1 Maxwell–Ampère equation

The magnetic field is related to current and the changing electric field:

```text
curl(B) = mu_0*J
        + mu_0*epsilon_0*dE/dt
```

Together with Faraday's law:

```text
curl(E) = -dB/dt
```

this establishes mutual electromagnetic coupling.

A changing current can alter the magnetic field, and the resulting fields can act back on charged matter.

**MATHEMATICAL RESULT:** Electromagnetic feedback is permitted by the established field equations.

But the existence of feedback does not guarantee that the resulting configuration is stable.

### 9.2 Electromagnetic energy

The classical electromagnetic energy density is:

```text
u_EM = 0.5*epsilon_0*E^2
     + B^2/(2*mu_0)
```

The electromagnetic energy flux is described by the Poynting vector:

```text
S = (1/mu_0)*(E × B)
```

Poynting's theorem is:

```text
d(u_EM)/dt + div(S) = -J·E
```

This equation relates:

* Changes in electromagnetic-field energy.
* Energy transported by the field.
* Energy exchanged between the field and charged matter.

**MATHEMATICAL RESULT:** Electromagnetic fields and charged matter can exchange energy.

### 9.3 Feedback and stability

The proposed electromagnetic shell is a hypothesis about the organization of the final atomic form.

To establish its physical validity, the model must provide:

* A mathematical definition of the shell.
* Its spatial charge and current distributions.
* Its energy.
* Its response to perturbations.
* A stability criterion.
* At least one observable prediction that differs from standard atomic physics.

A self-consistent field configuration is not automatically a stable one.

In established quantum mechanics, the stability of hydrogen is described by its bound-state energy spectrum and quantum dynamics.

The proposed feedback mechanism must reproduce those observations before it can be considered an alternative explanation.

---

## 10. Formation of hydrogen and photon emission

### 10.1 Radiative recombination

An electron and proton can form neutral hydrogen through radiative recombination:

```text
p + e^- -> H + gamma
```

The photon carries away energy and momentum.

This is an established atomic process.

**MEASUREMENT:** Hydrogen has a discrete energy spectrum, and transitions involving photon emission and absorption are observed.

**Sources:**

NIST — Atomic Data for Hydrogen

https://www.physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable1.htm

NIST — Atomic Spectra Database

https://physics.nist.gov/asd

### 10.2 Energy conservation

Let:

```text
K_i = initial relative kinetic energy

E_bind = binding energy of the final state

E_recoil = recoil kinetic energy of the hydrogen atom
```

Then, in the initial center-of-mass frame and neglecting small corrections:

```text
E_gamma = K_i + E_bind - E_recoil
```

For capture into the hydrogen ground state:

```text
E_bind ≈ 13.5984 eV
```

For negligible initial relative kinetic energy, the emitted photon energy is close to the ground-state binding energy, with a small recoil correction.

However, the capture probability depends on the available initial and final states and the relevant transition selection rules.

The reaction equation is an energy-accounting description, not a claim that every electron–proton encounter produces a hydrogen atom.

### 10.3 Photon emission as a signature of transformation

The model proposes:

**The photon is the observable manifestation of successful transformation into a stable electromagnetic form.**

This is a model interpretation.

The established physical result is narrower:

**Radiative capture and atomic transitions can produce photons whose energies correspond to differences between initial and final states.**

Photon emission does not, by itself, prove the formation of a separate electromagnetic shell.

The model's proposed shell must be independently defined and tested.

---

## 11. Does the spiral disappear after stabilization?

This question requires a precise distinction.

The model does not require:

```text
J_r(final) = J_r(formation)
```

Instead, it proposes:

```text
During formation:
J_r(t) may be nonzero.

After stabilization:
The stationary state may have zero net radial current.
```

This is mathematically compatible with the distinction between transient and stationary quantum states.

But compatibility is not proof.

**MATHEMATICAL RESULT:** Transient charge currents can exist in time-dependent quantum states even when the final stationary state has no radial orbital current.

**HYPOTHESIS:** A particular spiral current is responsible for the organization and stabilization of the hydrogen atom.

The hypothesis remains unconfirmed until the relevant current distribution is obtained from a dynamical calculation.

---

## 12. Electron capture, neutron decay, and the proposed transformation chain

### 12.1 Electron capture

In an energetically allowed nuclear electron-capture process:

```text
p + e^- -> n + nu_e
```

This equation represents the local weak-interaction conversion of a proton and electron into a neutron and an electron neutrino.

In an actual nucleus, the complete reaction must include the parent and daughter nuclei, and energy conservation must be satisfied.

An isolated, stationary proton cannot simply capture a free electron to produce a neutron and neutrino without sufficient available energy.

**Source:**

[11] Electron Capture

https://github.com/MeasurableScience/measurable-science/blob/main/References/011-electron-capture.md

### 12.2 Free-neutron beta decay

A free neutron can decay according to:

```text
n -> p + e^- + anti_nu_e
```

This process is experimentally established.

The electron and antineutrino are produced through the weak interaction during the decay; they are not evidence that a neutron is a preassembled proton–electron–antineutrino system.

### 12.3 Interpretation of the proposed chain

The model proposes:

```text
NEUTRINO -> NEUTRON -> ATOM
```

The known reactions do not establish this as a literal sequence of particle construction.

In particular:

* A neutron is not known to be constructed from a neutrino.
* Free-neutron decay does not automatically create an atom.
* The production of a proton and electron does provide particles that can subsequently participate in hydrogen formation.
* Electron capture and neutron beta decay are weak-interaction processes, distinct from electromagnetic atomic binding.

**HYPOTHESIS:** The recurrence of neutrinos and nucleons in these transformations may reflect a deeper organizational principle.

This interpretation is not established by the reactions alone.

---

## 13. Required numerical test of the proposed mechanism

The decisive test must examine the formation process, not merely the completed atom.

### 13.1 Initial state

Specify an initially unbound proton–electron system with:

```text
Initial relative separation: r_0

Initial relative momentum: p_0

Electron spin state: s_e

Proton spin state: s_p

Initial orbital angular momentum: L_0

Initial electromagnetic state: EM_0
```

These are necessary initial conditions, not adjustable values to be selected after seeing the result.

### 13.2 Physical model

A first nonrelativistic quantum approximation may be written schematically as:

```text
H = H_kinetic
  + H_Coulomb
  + H_spin_orbit
  + H_spin_spin
  + H_other_relativistic_corrections
  + H_radiation
```

The electromagnetic interaction must be introduced consistently, avoiding double-counting magnetic terms already represented by the Hamiltonian.

For radiative capture, the photon field must be included. A closed two-particle Schrödinger calculation cannot by itself represent spontaneous emission into the electromagnetic radiation field.

### 13.3 Dynamical evolution

The state evolves according to:

```text
i*hbar*dPsi/dt = H*Psi
```

From the evolving state, calculate:

```text
rho(r,t) = charge density

J(r,t) = charge-current density
```

The current should include the appropriate orbital and spin contributions for the selected approximation.

### 13.4 Current decomposition

Calculate:

```text
J_r(r,t)

J_phi(r,t)

J_z(r,t)
```

Do not insert a spiral shape into the initial conditions or numerical algorithm unless it is explicitly being tested as a separate imposed-condition experiment.

A useful local diagnostic is:

```text
Q(r,t) = abs(J_r*J_phi)
```

A nonzero Q identifies regions with simultaneous radial and azimuthal components.

However, **Q > 0 is not sufficient to prove a coherent spiral structure**. The current field must also be examined through its streamlines or integral curves, continuity, and time evolution.

### 13.5 Magnetic contribution

Run a controlled comparison:

```text
Case 1:
Reference electromagnetic model.

Case 2:
Same model with the relevant magnetic spin couplings
included or varied consistently.
```

Then compare:

```text
Delta_J = J_case2 - J_case1
```

The objective is to determine whether magnetic coupling produces a distinctive radial–azimuthal current organization.

### 13.6 Feedback and energy accounting

Calculate:

```text
E_matter(t)

E_field(t)

E_radiation(t)
```

Check energy conservation:

```text
E_initial = E_final + E_emitted
```

with all recoil and other relevant terms included.

A proposed stable shell must correspond to a well-defined final state and satisfy the appropriate stability conditions.

### 13.7 Photon prediction

Determine:

```text
Photon energy

Photon emission probability

Angular distribution

Polarization

Dependence on initial spin configuration
```

A distinctive model prediction should be compared with established hydrogen recombination theory and experimental spectra.

### 13.8 Falsification criteria

The proposed mechanism would lack support if:

1. No relevant spiral current emerges from the specified initial state.
2. The apparent spiral exists only when imposed numerically.
3. Magnetic coupling does not produce the predicted contribution.
4. The proposed stable shell cannot satisfy conservation and stability requirements.
5. Predicted photon energies or transition probabilities contradict established observations.

A positive result would require more than finding a spiral-shaped plot. It would require a reproducible dynamical mechanism and agreement with measurements.

**The program must not know the result.**

---

## 14. Evidence matrix

| Statement                                                                       | Status               |
| ------------------------------------------------------------------------------- | -------------------- |
| Proton and electron have magnetic moments                                       | MEASUREMENT          |
| Their magnetic interaction affects hydrogen energy levels                       | MEASUREMENT          |
| Hydrogen exhibits the approximately 1420.4 MHz hyperfine transition             | MEASUREMENT          |
| A changing magnetic field can induce an electric field                          | ESTABLISHED PHYSICS  |
| Moving electric charge constitutes electric current                             | ESTABLISHED PHYSICS  |
| Radial and azimuthal current components can form spiral flow lines              | MATHEMATICAL RESULT  |
| Time-dependent quantum states can contain transient charge currents             | MATHEMATICAL RESULT  |
| The final hydrogen 1s spatial state has zero radial orbital current             | MATHEMATICAL RESULT  |
| Magnetic coupling generates a specific spiral current during hydrogen formation | UNTESTED HYPOTHESIS  |
| Electromagnetic feedback can couple field dynamics and charge motion            | ESTABLISHED PHYSICS  |
| The proposed feedback creates a separate stable electromagnetic shell           | UNTESTED HYPOTHESIS  |
| Proton and electron can form hydrogen through radiative recombination           | ESTABLISHED PHYSICS  |
| The emitted photon marks formation of the proposed shell                        | MODEL INTERPRETATION |
| Electron capture and neutron beta decay occur                                   | MEASUREMENT          |
| Neutrino → neutron → atom is a literal particle-construction chain              | NOT ESTABLISHED      |

---

## 15. Scientific sources

**[C1] NIST — CODATA Recommended Values of the Fundamental Physical Constants: 2022**

Fundamental masses, magnetic moments, charges, and physical constants.

https://physics.nist.gov/constants

https://physics.nist.gov/cuu/pdf/all.pdf

**[C2] NIST — Measurement of the Unperturbed Hydrogen Hyperfine Transition Frequency**

Experimental determination of the hydrogen ground-state hyperfine transition.

https://tf.nist.gov/general/pdf/2060.pdf

**[C3] National Radio Astronomy Observatory — Essential Radio Astronomy, Chapter 7**

Hydrogen 21-centimeter line and its magnetic origin.

https://www.cv.nrao.edu/~sransom/web/Ch7.html

**[C4] OpenStax — Maxwell's Equations and Electromagnetic Waves**

Faraday induction, Maxwell–Ampère law, and electromagnetic coupling.

https://openstax.org/books/university-physics-volume-2/pages/16-1-maxwells-equations-and-electromagnetic-waves

**[C5] NIST — Atomic Data for Hydrogen**

Hydrogen energy levels and ionization energy.

https://www.physics.nist.gov/PhysRefData/Handbook/Tables/hydrogentable1.htm

**[C6] NIST — Atomic Spectra Database**

Measured and evaluated atomic spectra and transitions.

https://physics.nist.gov/asd

**[C7] Measurable Science — Mathematical Model [A]**

The author's relational-energy and organized-form framework.

https://github.com/MeasurableScience/measurable-science/blob/main/References/A-mathematical-model.md

**[C8] Measurable Science — Neutron Magnetism, Energy and Precession [B]**

The author's preceding comparison between neutron magnetic moment, energy splitting, and precession.

https://github.com/MeasurableScience/measurable-science/blob/main/References/B-neutron-magnetism-energy-precession.md

**[C9] Measurable Science — Neutron [8]**

Neutron properties, mass, and related scientific discussion.

https://github.com/MeasurableScience/measurable-science/blob/main/References/008-neutron.md

**[C10] Measurable Science — Electron Capture [11]**

Electron capture and its interpretation in the author's transformation sequence.

https://github.com/MeasurableScience/measurable-science/blob/main/References/011-electron-capture.md

---

## 16. Conclusion

The experimentally established foundation is clear:

The proton and electron have magnetic moments and electric charges. Their magnetic interaction produces measurable changes in hydrogen's energy spectrum. Time-dependent electromagnetic fields interact with electric currents, and proton–electron binding can occur with photon emission.

Mathematics also establishes that transient quantum charge currents can exist during a transition even when the final stationary state has no radial orbital current.

The proposed additional mechanism is more specific:

**A changing magnetic relation organizes a transient spiral electric current; that current participates in electromagnetic feedback; the feedback contributes to the formation of a stable atomic structure; photon emission accompanies the completed transformation.**

This mechanism is not yet derived from the established proton–electron dynamics.

The decisive test is therefore the calculation of the time-dependent charge-current field during radiative hydrogen formation, including magnetic coupling and radiation, without imposing a spiral in advance.

A verified spiral contribution would support part of the proposed organizational mechanism. Demonstrating that it causes stabilization would require an additional dynamical and experimental test.

The absence of persistent radial current in the completed atom does not, by itself, disprove a transient formation-stage current.

**The formation process and the completed form must be investigated separately.**

**The principle does not change. What enters into relation changes.**
