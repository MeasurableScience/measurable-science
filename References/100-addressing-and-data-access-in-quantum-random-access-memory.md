# Reference 100 — Addressing and Data Access in Quantum Random-Access Memory

## Purpose

This reference supports the statement that random-access memory requires an addressing mechanism through which particular memory locations can be selected and their stored information accessed.

The same fundamental addressing principle appears in both classical random-access memory and quantum random-access memory (QRAM).

## Quantum Random-Access Memory

Wang et al. describe the addressing principle explicitly:

- each memory location is identified by a distinct binary address;
- an address is supplied as the input during a memory query;
- the memory element associated with that address is retrieved;
- classical RAM uses classical routing hardware to reach the selected memory location;
- QRAM uses quantum routing mechanisms to direct quantum information toward the intended memory location.

The important architectural principle is therefore:

**stored information must remain addressable if the system is to retrieve a particular memory element.**

### Source

Wang, Y., Alexeev, Y., Jiang, L., Chong, F. T., et al. (2024).

"Fundamental causal bounds of quantum random access memories."

npj Quantum Information, 10, Article 71.

DOI: 10.1038/s41534-024-00848-3

## Experimental Random-Access Quantum Memory

An experimental implementation reported by Jiang et al. realized a random-access quantum memory containing 105 qubits carried by 210 memory cells.

The experiment demonstrated:

- many separate memory cells;
- individual addressing of qubits stored in those cells;
- programmable write-in;
- programmable readout;
- retrieval in arbitrary programmable order.

This provides an experimental example of quantum information being stored in a system containing individually addressable memory locations.

### Source

Jiang, N., Chang, W., Pu, Y.-F., et al. (2019).

"Experimental realization of 105-qubit random access quantum memory."

npj Quantum Information, 5, Article 28.

DOI: 10.1038/s41534-019-0144-0

## Relevance to the model

These papers do not imply that natural celestial systems constitute computer memory.

They establish the narrower computer-science principle used in the book:

**as a memory system contains increasing amounts of stored information, individual memory locations must remain identifiable and accessible through an addressing mechanism.**

In the model developed in *Measurable Science*, the plasma firmament is proposed as the working memory of the natural computer, while stable celestial reference points are investigated as possible addressing and reference structures within that memory system.

That final identification is a hypothesis of the model, not a conclusion of the cited QRAM research.