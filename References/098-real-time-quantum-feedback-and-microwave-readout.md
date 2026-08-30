# Reference 098 — Real-Time Quantum Feedback and Microwave Readout

## Purpose

This reference documents the experimental basis of microwave readout and real-time feedback control in superconducting quantum systems.

The relevant established facts are:

1. superconducting qubits can be measured through microwave readout resonators;
2. the state of a qubit changes the response of the readout system;
3. information about the qubit state can be extracted from the amplitude and/or phase of the microwave readout signal;
4. the measured signal can be amplified and processed by classical electronics;
5. the measurement result can be used in real time to determine a corrective action;
6. a conditional microwave control pulse can then be applied to the qubit;
7. real-time feedback has experimentally been used to stabilize superconducting qubit states and dynamics.

The essential control structure is therefore:

control
→ quantum system
→ measurement
→ classical processing
→ corrective control
→ quantum system

---

## 1. Microwave readout of superconducting qubits

Superconducting qubits are commonly coupled to microwave resonators for dispersive readout.

In the dispersive regime, the qubit state modifies the effective resonance characteristics of the coupled resonator.

A microwave probe signal is sent to the readout resonator.

The outgoing microwave signal consequently contains information about the state of the qubit.

The information can be encoded in measurable changes of the phase and amplitude of the transmitted or reflected microwave field.

### Source

Krantz P., Kjaergaard M., Yan F., Orlando T. P., Gustavsson S., Oliver W. D.

**A Quantum Engineer's Guide to Superconducting Qubits.**

Applied Physics Reviews. 2019;6:021318.

DOI:
https://doi.org/10.1063/1.5089550

---

## 2. Measurement signal and state discrimination

The microwave signal leaving the readout resonator is amplified and converted into a form that can be processed by classical electronics.

The measured quadratures of the microwave field contain information about the qubit state.

From these measurements the control system can distinguish between possible qubit states with a finite measurement fidelity.

The measurement therefore converts information stored in the quantum system into a classical signal that can be used by the control electronics.

In simplified form:

qubit state
→ resonator response
→ microwave output
→ amplification
→ signal processing
→ state estimate

### Source

Kjaergaard M., Schwartz M. E., Braumüller J., Krantz P., Wang J. I.-J., Gustavsson S., Oliver W. D.

**Superconducting Qubits: Current State of Play.**

Annual Review of Condensed Matter Physics. 2020;11:369–395.

DOI:
https://doi.org/10.1146/annurev-conmatphys-031119-050605

---

## 3. Real-time quantum feedback

Measurement does not have to be the final operation.

The measurement result can be processed while the experiment is running and used to determine a subsequent control operation.

This creates a feedback loop:

measurement
→ state estimate
→ decision
→ conditional control operation
→ new quantum state

Such measurement-based feedback has been experimentally demonstrated with superconducting qubits.

### Primary experimental source

Vijay R., Macklin C., Slichter D. H., Weber S. J., Murch K. W., Naik R., Korotkov A. N., Siddiqi I.

**Stabilizing Rabi oscillations in a superconducting qubit using quantum feedback.**

Nature. 2012;490:77–80.

DOI:
https://doi.org/10.1038/nature11505

In this experiment a superconducting qubit was continuously monitored through a microwave cavity.

The weak measurement signal was amplified and processed in real time.

The resulting estimate of the qubit evolution was used to generate feedback that corrected deviations and stabilized the qubit's Rabi oscillations.

This is a direct experimental realization of a closed quantum feedback loop.

---

## 4. Measurement → processing → correction

A measurement-based quantum feedback system contains two distinct physical functions:

### Measurement

The system must obtain information about the present quantum state.

For superconducting qubits this can be performed using microwave readout through a resonator.

### Correction

The measured information is processed by classical control electronics.

Depending on the result, a conditional control pulse can be generated and applied to the qubit.

The correction energy is supplied by the control hardware; it does not need to originate from the readout signal itself.

Therefore the readout channel and the corrective-control channel perform different functions even though both may use microwave electromagnetic signals.

---

## 5. Conditional microwave correction

Real-time control systems can convert a qubit measurement into a conditional gate.

A simplified implementation is:

microwave readout pulse
→ readout resonator
→ state-dependent microwave response
→ amplification
→ digitization
→ real-time logic
→ conditional microwave pulse
→ qubit

The corrective pulse may, for example, implement a π rotation when the measured state indicates that such a correction is required.

This architecture is also used in active reset and quantum-error-correction experiments.

### Experimental source

Ristè D., van Leeuwen J. G., Ku H.-S., Lehnert K. W., DiCarlo L.

**Initialization by Measurement of a Superconducting Quantum Bit Circuit.**

Physical Review Letters. 2012;109:050507.

DOI:
https://doi.org/10.1103/PhysRevLett.109.050507

The experiment demonstrated measurement-based initialization in which the result of a qubit measurement was used to conditionally apply a microwave π pulse.

---

## 6. Feedback for quantum error correction

The same general principle extends from stabilization of a single qubit to quantum error correction.

Information about the quantum system is extracted through measurements.

The measurement outcomes are processed to identify errors or deviations.

A controller can then determine and apply an appropriate corrective operation.

Thus the general closed-loop architecture is:

quantum state
→ measurement
→ error information
→ classical decoding or decision
→ corrective operation
→ quantum state

The feedback path therefore provides information required to determine whether and how the quantum system should be corrected.

---

## 7. Synchronization and feedback are different functions

A stable control system can require both:

**reference/control**

and

**measurement/feedback.**

They should not be confused.

A synchronization reference establishes the timing and phase basis used by the control system.

A feedback path determines how the controlled system actually responded and provides information required for subsequent correction.

In engineering terms:

reference
→ defines desired timing/control basis

feedback
→ measures actual response

comparison/processing
→ determines deviation

correction
→ modifies subsequent control

Therefore a feedback sensor does not need to perform the same physical function or provide the same power as the primary control source.

Its essential requirement is sufficient sensitivity and precision to extract the information required by the controller.

---

## 8. Technical summary

The experimentally demonstrated chain can be summarized as:

**microwave control
→ superconducting qubit
→ state-dependent microwave readout
→ amplification
→ real-time processing
→ conditional corrective microwave control
→ superconducting qubit**

Real-time measurement-based feedback has been experimentally demonstrated in superconducting quantum systems.

Vijay et al. demonstrated continuous monitoring and feedback stabilization of Rabi oscillations.

Ristè et al. demonstrated measurement followed by conditional microwave control for qubit initialization.

These experiments establish that measurement and corrective control can form a physical closed feedback loop around a superconducting quantum system.

---

## Relevance to the model

This reference establishes only the engineering and experimental principles of microwave readout and real-time feedback in superconducting quantum systems.

It supports the statements in the book that:

- a superconducting qubit can be read through a microwave resonator;
- its state changes the microwave readout response;
- amplitude and phase can carry information about that state;
- the signal can be processed in real time;
- the resulting information can determine a corrective microwave operation;
- real-time quantum feedback has experimentally been used to stabilize superconducting qubit dynamics.

It does not establish the proposed identification of any natural or celestial structure with a quantum feedback device.

The interpretation of the second "eye" as a readout/feedback element belongs to the model.