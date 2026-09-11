# [117] Pattern Recognition, Learning and Prediction

## Purpose

This reference supports the computational concepts used in the chapter on constellations: pattern recognition, learning from previously observed states, sequence learning, prediction, and quantum machine learning.

It does not claim that constellations are computational structures. That interpretation belongs to the model developed in the book.

The purpose of this reference is narrower: to establish that recognizing patterns, storing relationships between states, and using previous states to predict subsequent ones are well-established computational principles.

## 1. Pattern recognition and machine learning

Machine learning systems can identify structure and patterns in data and use those patterns for classification, inference, and prediction.

In the simplest abstract form, a recognizable input pattern may be represented as:

Ck = P(z1, z2, z3, ... zn)

where individual inputs form a larger pattern that can be treated as a single recognizable state.

The computational distinction used in the book is therefore:

individual input -> pattern -> recognized state

This is a general computational abstraction and does not depend on the physical nature of the inputs.

## 2. Learning relationships between states

If recognizable states occur in a repeated sequence,

C1 -> C2 -> C3 -> ...

a learning system can use previously observed relationships between those states to form an expectation about a subsequent state.

For example:

C1 -> expected C2

If the observed next state corresponds to C2, the learned relationship is supported by the new observation.

If the observed state differs from C2, the difference between the expected and observed result provides new information that can be incorporated into the model or memory.

The general computational chain is therefore:

data -> pattern -> state -> learned relationship -> prediction -> comparison with observation

## 3. Next-state prediction

A concrete modern example is next-token prediction in transformer-based language models.

Li et al. (2024) analyze how a self-attention layer trained for next-token prediction learns relationships within an input sequence and uses the available context to generate the next token.

The important point for the present reference is not language itself, but the more general computational principle:

previous sequence -> learned relationships -> prediction of the next element

This provides a concrete example of a system in which information about previous states is used to predict a subsequent state.

## 4. Quantum machine learning

Quantum machine learning investigates how machine-learning tasks can be implemented using quantum computational systems.

Biamonte et al. (2017) describe quantum machine learning as a field combining quantum computation with machine-learning tasks, including the identification and processing of patterns in data.

Cerezo et al. (2022) review quantum machine-learning methods, including quantum neural networks, classification, learning, and the challenges involved in obtaining useful quantum advantages.

These works establish that pattern recognition and learning are not concepts restricted to conventional classical computers. They are also active subjects of research in quantum computational systems.

This does not establish that a natural physical system performs quantum machine learning. It establishes only that the computational concepts used in the model — patterns, states, learning and prediction — are compatible with established areas of both classical and quantum computation.

## 5. Relation to the model

The model developed in the book proposes the following interpretation:

star -> address

constellation -> pattern of addresses

pattern -> recognizable state

sequence of states -> process

repetition of sequence -> possibility of prediction

or, in compact form:

star -> address -> constellation -> pattern -> state -> prediction

The scientific literature cited below supports the computational principles of pattern recognition, learning from data, sequence processing and prediction.

The additional proposal that stellar patterns perform such a function in a natural computer is the author's hypothesis and is not a conclusion of the cited literature.

## References

Biamonte, J., Wittek, P., Pancotti, N., Rebentrost, P., Wiebe, N., & Lloyd, S. (2017). Quantum machine learning. *Nature*, 549, 195–202. DOI: 10.1038/nature23474.

Cerezo, M., Verdon, G., Huang, H.-Y., Cincio, L., & Coles, P. J. (2022). Challenges and opportunities in quantum machine learning. *Nature Computational Science*, 2, 567–576. DOI: 10.1038/s43588-022-00311-3.

Li, Y., Huang, Y., Ildiz, M. E., Rawat, A. S., & Oymak, S. (2024). Mechanics of Next Token Prediction with Self-Attention. *Proceedings of the 27th International Conference on Artificial Intelligence and Statistics (AISTATS)*, Proceedings of Machine Learning Research, 238, 685–693.
