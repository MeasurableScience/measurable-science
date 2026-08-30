# Reference 096 — Quantum Control and Phase Synchronization

## Purpose

This reference documents the physical and engineering basis for precise electromagnetic control and synchronization in superconducting quantum processors.

The relevant established facts are:

1. superconducting qubits are commonly controlled using microwave electromagnetic pulses;
2. qubit operations depend on precisely controlled microwave frequency, phase, amplitude and pulse duration;
3. phase stability is essential because microwave phase determines the rotation axis of the qubit state;
4. amplitude and pulse duration determine the magnitude of the induced qubit rotation;
5. multichannel quantum-control systems require phase-coherent and stable microwave control;
6. differences introduced by cables, mixers, amplifiers and individual signal paths can be characterized and compensated by calibration.

These engineering principles provide the technical basis for the statement that physically non-identical control channels can nevertheless operate coherently when referenced, calibrated and synchronized.

---

## 1. Microwave control of superconducting qubits

Superconducting qubits, including transmon qubits, are commonly manipulated using resonant microwave electromagnetic pulses.

A microwave drive near the qubit transition frequency produces coherent transitions between quantum states.

Single-qubit XY gates can therefore be implemented by applying controlled microwave pulses to the qubit.

### Source

Krantz P., Kjaergaard M., Yan F., Orlando T. P., Gustavsson S., Oliver W. D.

**A Quantum Engineer's Guide to Superconducting Qubits.**

Applied Physics Reviews. 2019;6:021318.

DOI:
https://doi.org/10.1063/1.5089550

---

## 2. Frequency, phase, amplitude and duration carry different control functions

A microwave control pulse is not defined merely by whether electromagnetic energy is present.

Its frequency, phase, amplitude and temporal envelope determine the resulting operation on the qubit.

For resonant microwave control:

- microwave frequency determines resonance and the rotating reference frame;
- microwave phase determines the rotation axis in the XY plane of the Bloch sphere;
- microwave amplitude determines the Rabi frequency;
- pulse amplitude together with pulse duration determines the rotation angle.

Therefore precise quantum control requires precise control of both the electromagnetic waveform and its timing.

### Source

Kjaergaard M., Schwartz M. E., Braumüller J., Krantz P., Wang J. I.-J., Gustavsson S., Oliver W. D.

**Superconducting Qubits: Current State of Play.**

Annual Review of Condensed Matter Physics. 2020;11:369–395.

DOI:
https://doi.org/10.1146/annurev-conmatphys-031119-050605

See also:

Rizvi N. R. et al.

**A Survey of Microwave-Implemented Superconducting Qubit Control and Readout Circuits.**

IEEE Transactions on Quantum Engineering. 2026;7:1–52.

DOI:
https://doi.org/10.1109/TQE.2026.3659400

---

## 3. Phase is a physical control parameter

The phase of the microwave carrier determines the axis around which the qubit state rotates in the XY plane.

A phase difference of 90 degrees between two otherwise equivalent microwave drives corresponds to orthogonal X and Y control axes.

Consequently, uncontrolled phase differences produce control errors.

Modern superconducting-qubit control systems therefore require low phase noise and stable phase relationships between microwave signals.

### Source

Rizvi N. R. et al.

**A Survey of Microwave-Implemented Superconducting Qubit Control and Readout Circuits.**

IEEE Transactions on Quantum Engineering. 2026;7:1–52.

DOI:
https://doi.org/10.1109/TQE.2026.3659400

The review specifically discusses the requirement for low-phase-noise local oscillators and short-term phase coherence across channels in multi-qubit systems.

---

## 4. Multichannel phase coherence

A quantum processor contains multiple microwave control and readout channels.

For coherent operations, these channels cannot be allowed to develop arbitrary independent phases.

Quantum-control hardware therefore uses stable frequency generation, local oscillators, phase-locked references, direct digital synthesis and synchronized waveform generation.

The relevant requirement is not that every physical channel be identical.

The requirement is that their timing, frequency and phase relationships be sufficiently known and controlled for the intended quantum operation.

This distinction is important:

**physical equality of channels is not required for coherent synchronization.**

What is required is a stable reference together with calibration of channel-dependent differences.

### Source

Rizvi N. R. et al.

**A Survey of Microwave-Implemented Superconducting Qubit Control and Readout Circuits.**

IEEE Transactions on Quantum Engineering. 2026;7:1–52.

DOI:
https://doi.org/10.1109/TQE.2026.3659400

---

## 5. Channel differences can be measured and compensated

Real microwave-control paths are not identical.

Cables, mixers, amplifiers, filters and other components introduce:

- propagation delays;
- amplitude distortion;
- phase offsets;
- frequency-dependent transfer functions;
- mixer imbalance;
- dispersion.

High-fidelity quantum control therefore requires calibration of the complete microwave path.

Measurements of amplitude and phase transfer functions can be used to characterize these distortions and correct the generated control pulses.

### Source

Schuster D. I. et al. / related superconducting microwave-control literature summarized in:

Rizvi N. R. et al.

**A Survey of Microwave-Implemented Superconducting Qubit Control and Readout Circuits.**

IEEE Transactions on Quantum Engineering. 2026;7:1–52.

DOI:
https://doi.org/10.1109/TQE.2026.3659400

See also:

**Amplitude and frequency sensing of microwave fields with a superconducting transmon qudit.**

npj Quantum Information. 2020;6:57.

DOI:
https://doi.org/10.1038/s41534-020-00287-w

The experiment demonstrates characterization of microwave transfer functions at the qubit and discusses pulse correction for high-fidelity superconducting quantum gates.

---

## 6. Experimental multichannel phase stability

The importance of channel-to-channel phase stability can also be measured directly.

Modern multichannel superconducting-qubit controllers monitor and stabilize microwave outputs against amplitude and phase drift.

A multichannel controller reported simultaneous monitoring of 15 microwave output channels and measured phase deviations of approximately 0.35–0.44 degrees over 24 hours.

The authors explicitly evaluated the effect of phase misalignment and amplitude instability on quantum-gate fidelity.

This demonstrates that phase alignment between physical microwave channels is a measurable engineering parameter of quantum-control hardware.

### Source

**Microwave output stabilization of a qubit controller via device-level temperature control.**

2026.

PMID:
41891775

https://pubmed.ncbi.nlm.nih.gov/41891775/

---

## 7. Technical summary

The experimentally established engineering chain can therefore be summarized as:

**stable electromagnetic reference  
→ controlled microwave frequency and phase  
→ measurement/calibration of channel-dependent errors  
→ compensation  
→ phase-coherent control channels**

The individual physical channels do not need to have identical construction, propagation delay or transfer characteristics.

Their differences can be measured and compensated relative to common stable timing and phase references.

---

## Relevance to the model

This reference establishes only the engineering principles used in real superconducting quantum-control systems.

It supports the statements that:

- superconducting qubits can be controlled by microwave electromagnetic signals;
- frequency, phase, amplitude and duration are essential control parameters;
- stable phase relationships are required;
- multiple non-identical physical channels can be calibrated and operated coherently relative to common references.

It does not establish that natural oceanic, atmospheric or geological structures constitute a quantum computer.

The proposed correspondence between these engineering principles and the four magistrales of the model is therefore a model hypothesis.