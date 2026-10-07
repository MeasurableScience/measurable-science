# ADMIN — Functional Tests of Relational Learning, World-Model Adaptation, and Self-Reference

## Purpose of this folder

This folder contains three controlled Python experiments developed for the **Admin** chapter of *Measurable Science*.

The experiments test three successive functional steps proposed in the chapter:

1. Can previous relational experience change the future processing of relations?
2. Can accumulated experience form a predictive model that adapts when a previously learned relation changes?
3. If a future outcome depends partly on the system's own internal state, can including that state in the model improve prediction?

These are three separate tests.

Each experiment tests one step of the proposed functional progression:

**RELATIONAL EXPERIENCE  
→ LEARNING  
→ PREDICTIVE WORLD MODEL  
→ MODEL ADAPTATION  
→ INTERNAL STATE IN THE MODEL  
→ FUNCTIONAL SELF-REFERENCE**

The experiments are deliberately implemented on an ordinary classical computer.

They are not quantum simulations.

They are not physical simulations of the Earth, ionosphere, gyres, magistrale, Black Rock, or any other proposed physical component of the Admin architecture.

Their purpose is narrower:

**to determine whether the proposed functional steps are algorithmically possible under controlled conditions.**

The three Python scripts in this folder therefore test the computational logic of the hypothesis, not the physical existence of the proposed natural machine.


---

# TEST 1 — Relational Learning and Feedback

## Question

The first experiment asks:

**CAN PREVIOUS EXPERIENCE OF A RELATION CHANGE HOW THE SYSTEM PROCESSES THAT RELATION IN THE FUTURE?**

This is the first functional requirement of the proposed architecture.

A system that merely receives signals does not learn.

For learning to occur, previous interactions must leave a state that affects the processing of later interactions.


## Synthetic input

The experiment generates four synthetic signal channels.

The sampling frequency is:

`fs = 128 Hz`

Each observation window lasts:

`8 seconds`

The signals are processed in the frequency band:

`7–9 Hz`

Channels 0 and 1 contain the same 8 Hz carrier with a stable phase offset.

Channel 2 initially also contains the same carrier with a stable phase relationship.

Channel 3 is independent noise and therefore has no intentionally imposed phase locking to the other channels.


## Relational measurement

The signals are band-pass filtered between 7 and 9 Hz.

Their instantaneous phases are extracted using the Hilbert transform.

For every pair of channels the program calculates:

**PLV — Phase Locking Value**

PLV measures the stability of the phase relationship between two signals.

The system therefore does not receive semantic labels describing what the signals represent.

It receives measurable relations between signals.


## Memory

For every channel pair the program stores a learned expected PLV.

The current observation can therefore be compared with the previous state stored in memory.

The difference between the observed relation and the learned relation becomes a prediction error.


## Three-state logic

Each relation can enter one of three functional states:

`0 = REJECT`

`1 = ACCEPT`

`2 = OPEN`

The initial threshold is:

`theta = 0.70`

A previously unknown relation is initially left OPEN.

A sufficiently stable relation that remains above the threshold and remains close to its learned value can become ACCEPTED.

A consistently weak relation can become REJECTED.

A relation that no longer agrees with its previous state can return to OPEN.

The third state therefore provides a simple computational implementation of:

**DO NOT FORCE AN UNKNOWN OR CHANGED RELATION INTO YES OR NO.  
LEAVE IT OPEN FOR FURTHER EXPERIENCE.**


## Learning rule

The expected PLV stored in memory is updated from new observations.

The update rate depends on the current state.

The purpose is not to reproduce a biological or quantum learning mechanism.

It is simply to test whether previous relational experience can alter future classification of the same relation.


## Controlled change

The experiment first presents five stable observation windows.

After that, the phase relation of channel 2 is deliberately disrupted.

Instead of maintaining a stable phase offset, channel 2 receives a phase random walk.

The program is not told:

`CHANNEL 2 HAS CHANGED`

It receives only the new measured relation.

The question is whether the difference between previous experience and the new observation is sufficient to change the system's future processing.


## Feedback

The experiment also contains a simple feedback controller.

If the mean prediction error becomes sufficiently large, the selection threshold for the next observation is temporarily reduced.

The feedback is bounded and smoothed to prevent uncontrolled instability.

This implements a minimal closed loop:

**RELATION  
→ MEMORY  
→ PREDICTION ERROR  
→ FEEDBACK  
→ CHANGED CONDITIONS FOR THE NEXT PROCESSING STEP**


## Test conditions

The script automatically checks that:

- a stable relation becomes accepted;
- the stable control pair remains strongly phase locked;
- the relation that will later be disrupted was strongly phase locked before the intervention;
- the intervention produces a detectable prediction error;
- the prediction error activates feedback.


## Result

The predefined checks pass.

The experiment demonstrates that a classical algorithm can retain previous relational experience and use it to change the future processing of a relation.

The result supports the limited statement:

**PREVIOUS EXPERIENCE CAN ALGORITHMICALLY CHANGE THE FUTURE PROCESSING OF RELATIONS.**


## What Test 1 does not prove

The experiment does not prove that natural gyres calculate PLV.

It does not prove that the proposed natural system uses this three-state rule.

It does not prove quantum computation.

It does not prove consciousness.

It establishes only the algorithmic feasibility of the first functional step.


---

# TEST 2 — Building and Adapting a World Model

## Question

The second experiment asks a stronger question:

**CAN EXPERIENCE FORM A MODEL THAT PREDICTS FUTURE STATES, AND CAN PREDICTION ERROR MODIFY THAT MODEL AFTER THE WORLD CHANGES?**

The tested cycle is:

**EXPERIENCE  
→ PATTERN / MODEL  
→ PREDICTION  
→ UNEXPECTED CHANGE  
→ PREDICTION ERROR  
→ MODEL CHANGE  
→ IMPROVED FUTURE PREDICTION**


## Synthetic world

The experiment contains:

`900 time steps`

and:

`12 synthetic signals`

The signals deliberately contain different forms of structure.

They include periodic relations, combinations of multiple rhythms, drift, relations dependent on other signals, an autoregressive process, and weakly predictable signals.

The world generator knows the mathematical rules that produce these signals.

The processors do not.

They receive only the numerical observations delivered through the simulated transmission channels.


## Three processors

The same synthetic world is presented to three processors.

### Processor A — LEARNING

Learns before and after the intervention.

### Processor B — NEVER_LEARN

Never updates its model.

### Processor C — FREEZE_AT_CHANGE

Learns in exactly the same way as A before the intervention.

At the moment of intervention its model is frozen.

This creates the most important causal control in the experiment.

Immediately before the intervention:

**A and C have the same history and the same model.**

After the intervention there is only one intended difference:

**A is allowed to adapt.  
C is not.**


## Prediction before observation

At every time step the processors must make their prediction before receiving the current observation.

The order is therefore:

**1. Predict  
2. Receive observation  
3. Measure prediction error  
4. Update the model, if learning is allowed**

This prevents the current observation from leaking into the prediction that is supposedly being tested.


## Intervention

At:

`step = 480`

the transmission regime of:

`channel = 3`

is changed.

The new transmission parameters are:

`gain = 0.55`

`offset = 0.28`

`delay = 2`

This is not simply the addition of random noise.

The channel changes from one deterministic transmission regime to another.

The experiment therefore does not assume that a changed signal must automatically become worse or noisier.

It asks whether the relationship between the learned model and the arriving observation has changed.


## Counterfactual control

The experiment also preserves a counterfactual signal:

**what the channel would have transmitted if the intervention had never occurred.**

The processors never see this signal.

It is used only after the experiment for evaluation.

This makes it possible to distinguish the effect of the intervention from ordinary prediction error.


## Predefined criteria

The pass/fail conditions are defined before evaluating the result.

Among other requirements:

- A and C must be numerically identical before the intervention;
- the intervention must actually change the transmitted signal;
- learning before the intervention must outperform the never-learning control;
- the adaptive model must outperform the frozen identical model after the intervention;
- late adaptation must retain a predefined advantage over the frozen model.

The script is allowed to fail.

The criteria are not changed after seeing the result in order to force a successful outcome.


## Result

On the changed channel during the final evaluation:

`Adaptive model A MSE = 0.003580`

`Frozen model C MSE = 0.038209`

The adaptive model therefore has:

**90.63% LOWER ERROR**

than the model that had the same history and the same learned state before the intervention but was not allowed to adapt afterward.

Across the whole modeled world, the learned system also retains a substantial advantage over the processor that never learned.

All:

**7 / 7 predefined criteria passed.**


## Interpretation

The important comparison is not simply between a "smart" and a "dumb" processor.

The strongest comparison is between A and C.

They are deliberately identical immediately before the intervention.

Their behavior diverges only because one system is allowed to use new prediction error to modify its model while the other is frozen.

The experiment therefore supports the limited functional statement:

**PREVIOUS EXPERIENCE CAN FORM A PREDICTIVE MODEL, AND PREDICTION ERROR CAN BE USED TO ADAPT THAT MODEL AFTER A RELATION CHANGES.**

Or, in compact form:

**EXPERIENCE  
→ MODEL  
→ PREDICTION  
→ ERROR  
→ MODEL ADAPTATION**


## What Test 2 does not prove

The experiment does not prove that the proposed natural machine contains these exact algorithms.

It does not prove the physical existence of gyres or magistrale as computational components.

It does not prove consciousness.

It demonstrates that the proposed functional cycle of experience, prediction, error, and adaptation is algorithmically possible.


---

# TEST 3 — Functional Self-Reference

## Question

The third experiment asks:

**CAN A SYSTEM PREDICT THE FUTURE MORE ACCURATELY IF ITS MODEL INCLUDES ITS OWN INTERNAL STATE?**

The comparison is:

`MODEL A: Y(t+1) = f(X_t)`

`MODEL B: Y(t+1) = f(X_t, M_t)`

where:

`X_t = external state`

`M_t = internal state of the system`

`Y(t+1) = future outcome to be predicted`


## Experimental design

The experiment contains:

`6000 time steps`

The training interval is:

`0–3999`

The blind test interval is:

`4000–5999`

The final test data are not used for learning.


## External world

The external input is generated from multiple oscillatory components plus noise.

This prevents the external state from being a trivial constant variable.


## Internal state

The internal state is not an arbitrary label.

It has its own dynamics.

It depends on:

- its previous internal state;
- external input;
- a small internal noise component.

The principal parameters are:

`STATE_MEMORY = 0.92`

`STATE_INPUT_COUPLING = 0.16`

`STATE_NOISE = 0.04`

The internal state therefore has memory.

Two similar external inputs can encounter the system in different internal states.


## Hidden future law

The synthetic world's generator is deliberately constructed so that the future outcome depends on both the external state and the internal state.

The true internal-state contribution is controlled by:

`TRUE_SELF_EFFECT = 0.75`

The future outcome also contains an interaction between external and internal state.

The models do not receive the generator formula.

They must infer predictive relationships only from the training data.


## Three models

Three models are compared.

### Model A — EXTERNAL ONLY

Uses only the external state:

`X_t`

### Model B — SELF STATE

Uses:

`X_t + M_t`

### Model C — SHUFFLED SELF

Uses the same number and type of variables as B, but the internal states are deliberately paired with the wrong events during training.

This control is essential.

If B outperforms A alone, the improvement could in principle result merely from giving B additional variables.

Model C tests that possibility.

It receives the additional internal-state variable, but the meaningful relationship between internal state and event has been destroyed.

Therefore, if:

`B < A`

and:

`B < C`

in prediction error, the advantage cannot be explained simply by adding another input column.

The correctly corresponding internal state must contain useful predictive information.


## Prediction model

All models use the same general regression method.

Model A is also given nonlinear functions of the external variable so that B does not win merely because A has been artificially restricted to an excessively weak model.

The models are trained only on the training interval.

Their parameters are then frozen for the blind final test.


## Main results

The blind-test results are:

| Model | MSE | MAE |
|---|---:|---:|
| A — External only | 0.20813445 | 0.37285870 |
| B — Correct self state | **0.00684981** | **0.06650734** |
| C — Shuffled self | 0.21009852 | 0.37519345 |

Relative to Model A, Model B reduces MSE by:

**96.71%**

Relative to the shuffled-self control, Model B reduces MSE by:

**96.74%**

The improvement is also present in MAE:

**82.16% lower MAE than Model A.**


## Permutation control

A second independent control tests whether the correct correspondence between internal state and event is important.

Model B remains frozen.

The internal-state values in the test set are randomly permuted between events while the external input and target outcome remain unchanged.

This is repeated:

`1000 times`

Nothing is retrained.

If the correctly aligned internal state contains meaningful predictive information, destroying that alignment should increase prediction error.

The result is:

`Correct self-state MSE = 0.00684981`

`Median permuted MSE = 0.78438316`

`p = 0.000999`

The correctly aligned internal state therefore strongly outperforms randomly mismatched internal states.


## Predefined criteria

Five success criteria were specified in advance.

They require:

1. B to outperform A by the predefined minimum MSE margin.
2. B to outperform the shuffled-self control.
3. The advantage to remain present using MAE.
4. The permutation test to satisfy the predefined significance threshold.
5. Correctly aligned internal state to outperform the permuted-state distribution.

All:

**5 / 5 predefined criteria passed.**


## Interpretation

The experiment demonstrates a narrow but important computational property.

When the future state of the synthetic world depends partly on the current internal state of the predicting system, information about that internal state can improve prediction.

The system's own state therefore becomes a variable inside its model of the future.

This is what is meant here by:

**FUNCTIONAL SELF-REFERENCE.**

The result supports the statement:

**IF A FUTURE OUTCOME DEPENDS ON THE STATE OF THE MACHINE ITSELF, THE MACHINE'S OWN STATE CAN BECOME INFORMATION REQUIRED FOR BETTER PREDICTION.**


## What Test 3 does not prove

This is not a test of subjective consciousness.

It does not demonstrate awareness.

It does not demonstrate the statement:

**"I EXIST."**

It does not establish that a natural system identifies itself as an individual entity.

The experiment tests only a minimal functional step:

**the state of the system performing the prediction can become a useful variable in its own predictive model.**


---

# Combined Result

The three scripts test three different stages.

They should not be interpreted as three repetitions of the same experiment.

### Test 1

**PREVIOUS EXPERIENCE  
→ CHANGED FUTURE PROCESSING**

The system can retain relational history and allow that history to affect future processing.

### Test 2

**EXPERIENCE  
→ MODEL  
→ PREDICTION  
→ ERROR  
→ ADAPTATION**

Experience can form a predictive model, and prediction error can be used to modify that model after the environment changes.

### Test 3

**EXTERNAL STATE + INTERNAL STATE  
→ IMPROVED FUTURE PREDICTION**

When future outcomes depend on the system's internal state, that state can become useful information inside the predictive model.


# Overall conclusion

Taken together, the experiments demonstrate the algorithmic feasibility of the following progression:

**RELATIONS  
→ MEMORY OF RELATIONS  
→ LEARNING FROM RELATIONS  
→ PREDICTIVE MODEL  
→ ERROR-DRIVEN ADAPTATION  
→ INTERNAL STATE ENTERS THE MODEL  
→ FUNCTIONAL SELF-REFERENCE**

All three steps can be implemented and tested on a classical computer.

This is the result established by the simulations.

The simulations do **not** establish that the proposed natural architecture physically exists.

They do **not** establish that the Earth is a quantum computer.

They do **not** establish that neutrinos perform the proposed three-state logic.

They do **not** establish that gyres perform relational computation.

They do **not** establish that the Black Rock functions as a processor.

And they do **not** establish consciousness.

They establish something narrower and testable:

**THE THREE FUNCTIONAL STEPS REQUIRED BY THE PROPOSED ADMIN ARCHITECTURE ARE ALGORITHMICALLY POSSIBLE IN CONTROLLED CLASSICAL SIMULATIONS.**

The transition from functional self-reference to consciousness remains a separate hypothesis.

It is not a result of these three computational tests.