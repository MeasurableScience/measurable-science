# Reference 074 — Three-Flavor Neutrinos and Qutrit Encoding

## Purpose

This reference supports two scientific statements used in *Merljiva nauka*:

1. neutrinos occur in three flavor states — electron, muon and tau;
2. a three-flavor neutrino system can be represented in quantum-information processing using a qutrit, a three-level quantum system.

It provides the scientific basis for changing the author's earlier functional mapping:

**neutrino / super-cell → candidate qubit**

to:

**neutrino / super-cell → candidate qutrit**

The assignment of logical meanings such as "accept", "reject" and "remain open / continue learning" to the three states is the author's model and is NOT a claim of the cited literature.

## Scientific basis

### Three neutrino flavors

The three known neutrino flavor states are:

- electron neutrino, νe;
- muon neutrino, νμ;
- tau neutrino, ντ.

Flavor states are related through the PMNS mixing matrix to three neutrino mass eigenstates.

During propagation, a neutrino produced in one flavor state can later be measured as another flavor.

This phenomenon is neutrino oscillation.

### Three-dimensional quantum state space

Because the full flavor description contains three basis states, three-flavor neutrino dynamics can be treated using a three-dimensional quantum state space.

A general qutrit state has three computational basis states:

|0⟩, |1⟩, |2⟩

and may exist in a quantum superposition of those basis states.

### Direct qutrit encoding of neutrino flavor

Nguyen et al. experimentally encoded a three-flavor neutrino in a superconducting qutrit and simulated neutrino oscillations on real quantum hardware.

More recent work has developed qutrit quantum circuits specifically for collective three-flavor neutrino oscillations.

Turro et al. constructed qutrit and qubit circuits for three-flavor collective neutrino dynamics.

Spagnoli et al. provided both qubit and qutrit encodings for all three neutrino flavors and implemented experiments using superconducting quantum hardware.

These works establish that qutrit representation is a physically meaningful quantum-information encoding for the three-flavor neutrino problem.

## Functional consequence for the model

A qutrit differs fundamentally from a qubit.

A qubit has two computational basis states:

|0⟩ and |1⟩.

A qutrit has three:

|0⟩, |1⟩ and |2⟩.

Therefore, if the proposed natural-computer model uses all three neutrino flavor degrees of freedom as its elementary quantum-information unit, the functional analogy is more accurately described as a qutrit than as a qubit.

## Proposed learning logic in the model

The author proposes the following functional interpretation:

0 → reject

1 → accept

2 → remain open / continue learning

This mapping is NOT part of established neutrino physics.

The cited research demonstrates three-flavor neutrino dynamics and qutrit encoding.

It does NOT demonstrate that neutrinos naturally implement this logical rule, that neutrino flavor determines acceptance or rejection of information, or that natural neutrino systems perform learning.

Those claims belong exclusively to the proposed architecture developed in *Merljiva nauka*.

## Important limitation

A computational encoding of neutrino flavors into qutrit states does not by itself demonstrate that an individual neutrino is a naturally operating qutrit computer.

Likewise, the existence of three neutrino flavors does not establish a ternary learning algorithm.

The scientific literature establishes the compatibility between three-flavor neutrino dynamics and qutrit representation.

The computational role assigned to this property is the author's hypothesis.

## Sources

### Nguyen, N. A. et al. (2023)

**Simulating neutrino oscillations on a superconducting qutrit.**

Physical Review D, 108, 023013.

DOI: 10.1103/PhysRevD.108.023013

Demonstrates encoding of a three-flavor neutrino in a superconducting qutrit and simulation of its oscillations using qutrit operations.

### Turro, F., Chernyshev, I. A., Bhaskar, R. & Illa, M. (2025)

**Qutrit and qubit circuits for three-flavor collective neutrino oscillations.**

Physical Review D, 111, 043038.

DOI: 10.1103/PhysRevD.111.043038

Develops quantum circuits for simulating three-flavor neutrino systems using both qutrit and qubit platforms.

### Spagnoli, L. et al. (2025)

**Collective neutrino oscillations in three flavors on qubit and qutrit processors.**

Physical Review D, 111, 103054.

DOI: 10.1103/gjr1-lf8s

Provides qutrit and qubit encodings of all three neutrino flavors and tests them using superconducting quantum hardware.

### Banerjee, S., Alok, A. K., Srikanth, R. & Hiesmayr, B. C. (2015)

**A quantum-information theoretic analysis of three-flavor neutrino oscillations.**

European Physical Journal C, 75, 487.

DOI: 10.1140/epjc/s10052-015-3717-x

Provides a quantum-information treatment of the three-flavor neutrino system and its quantum correlations.

## Accessed

26 August 2026