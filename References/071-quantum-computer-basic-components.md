# Reference 071 — Basic Components of a Quantum Computer

## Purpose

This reference supports the description of the basic functional
components required for quantum computation.

A quantum computer is built around physical quantum systems called
**qubits**. Computation is performed by preparing quantum states,
manipulating those states through quantum operations, and measuring
the resulting states.

## Basic functional components

### 1. Qubits

Qubits are the fundamental units of quantum information.

Unlike classical bits, which represent either 0 or 1, a qubit can
exist in a quantum superposition of basis states.

### 2. Quantum Processing Unit (QPU)

The QPU is the physical subsystem in which quantum computation takes
place.

It contains the physical qubits and the structures required to operate
and connect them.

IBM describes the QPU as the core component of a quantum computer.

### 3. Quantum operations / gates

Quantum computation requires controlled operations that change the
states of qubits.

Sequences of these operations form quantum circuits.

### 4. Control system

Physical qubits must receive controlled signals in order to prepare
and manipulate their quantum states.

Depending on the qubit technology, these signals may include
microwaves, lasers or electrical voltages.

### 5. Measurement / readout system

The state of the quantum system must ultimately be measured in order
to obtain a result.

Measurement converts information from the quantum system into an
observable classical result.

### 6. Classical control and communication

Modern quantum computers also require classical hardware for sending
instructions to the quantum processor, controlling input and output
signals, receiving measurement results and coordinating subsequent
operations.

### 7. Physical environment for maintaining quantum states

Qubits require physical conditions that allow their quantum states to
remain sufficiently stable and coherent for computation.

The required environment depends on the qubit technology. Examples
include cryogenic systems and vacuum systems.

## Functional summary

At the most basic functional level, quantum computation therefore
requires:

**quantum information carrier → quantum processor → controlled
operations → measurement/readout**

with supporting:

**control → communication → physical stabilization/coherence**

The specific physical implementation can differ between quantum
computing technologies.

## Sources

1. IBM — *What is a QPU (Quantum Processing Unit)?*
   https://www.ibm.com/think/topics/qpu

2. Microsoft Azure Quantum — *What Is Quantum Computing?*
   https://learn.microsoft.com/en-us/azure/quantum/overview-understanding-quantum-computing

3. Microsoft Azure Quantum — *The Qubit in Quantum Computing*
   https://learn.microsoft.com/en-us/azure/quantum/concepts-the-qubit

4. Microsoft Azure Quantum — *Hybrid Quantum Computing Concepts*
   https://learn.microsoft.com/en-us/azure/quantum/hybrid-computing-concepts

## Accessed

26 August 2026