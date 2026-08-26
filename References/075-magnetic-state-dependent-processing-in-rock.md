# Reference 075 — Magnetic-State-Dependent Electrical Response and Remanence Modification in Rock

## Purpose

This reference supports the physical mechanisms used in *Merljiva nauka* for the proposed central processing node.

Specifically, it documents that:

1. magnetite can exhibit an electrical response dependent on magnetization and its orientation relative to electric current;
2. magnetic minerals and igneous/volcanic rocks can change their remanent magnetic state under mechanical stress and other physical excitation;
3. some stress-induced changes in remanent magnetization can remain after the applied stress is removed;
4. therefore a magnetic material can possess a previous physical state that influences its response and can itself be modified by later physical conditions.

These observations provide physical ingredients for the author's proposed functional sequence:

**stored magnetic state + new input → state-dependent response → modified stored state**

The cited literature does NOT demonstrate that a natural volcanic structure functions as a CPU or performs computation.

## 1. Magnetic state can influence electrical response

Magnetite (Fe3O4) is both magnetic and electrically conductive.

Experiments on epitaxial magnetite have measured anisotropic magnetoresistance (AMR) and the planar Hall effect (PHE).

The measured electrical resistivity depends on the relative orientation of:

- electric current;
- magnetization;
- crystallographic axes;
- applied magnetic field.

Therefore the electrical transport properties of magnetite are not completely independent of its magnetic state.

A simplified functional representation is:

**ρ = ρ(M, J, B, T, crystal orientation, ...)**

where:

- ρ is electrical resistivity;
- M is magnetization;
- J is current density;
- B is magnetic field.

This establishes the narrower material principle required by the model:

**magnetic state can affect electrical response.**

## 2. Stress can modify remanent magnetization

Magnetite-bearing rocks are magnetostrictive and their magnetic properties can respond to mechanical stress.

Laboratory experiments on igneous rocks have demonstrated piezo-remanent magnetization and stress-induced changes of existing remanent magnetization.

Nagata and Carleton experimentally studied igneous rocks in weak magnetic fields under uniaxial compression comparable to crustal stresses.

Domen demonstrated that applied pressure can change both the direction and intensity of remanent magnetization.

Pozzi measured the effects of compressive and tensile stresses on natural remanent and induced magnetizations in volcanic rocks from Mount Etna.

Hamano progressively compressed natural rock samples and measured changes of natural remanent magnetization. At 100 bar, measured changes in NRM intensity ranged from approximately 0.4% to 47.7%, depending on the sample.

These experiments demonstrate that an already magnetized natural rock can change its magnetic state in response to later physical conditions.

## 3. Some magnetic changes are irreversible

Stress effects on remanent magnetization are not necessarily completely reversible.

Experiments have observed permanent changes remaining after stress cycles.

This distinction is important for the proposed architecture because a purely reversible response would function only as a temporary state modulation.

An irreversible or partially irreversible change provides a possible physical route by which an interaction can alter the state encountered by subsequent interactions.

This can be represented abstractly as:

**M(t) → physical interaction → M(t+1)**

with:

**M(t+1) ≠ M(t)**

under appropriate conditions.

## 4. Volcanic rocks contain relevant magnetic carriers

Magnetic studies of volcanic rocks identify magnetite and titanomagnetite as major carriers of natural remanent magnetization.

Studies of volcanites from Lipari and Vulcano found remanent magnetization to exceed induced magnetization in most investigated lithologies and identified titanomagnetite as the primary magnetic carrier.

Studies of volcanic rocks in New Zealand likewise measure substantial natural remanence and magnetic susceptibility.

Therefore the magnetic phenomena used in the proposed model are not restricted to synthetic magnetic devices; related magnetic carriers occur naturally in volcanic rocks.

## Functional interpretation in the model

Reference [72] establishes:

**magnetic volcanic rock → long-lived remanent storage**

Reference [75] adds two further material properties:

**stored magnetic state → can influence electrical response**

and

**later physical interaction → can alter magnetic state**

Together these permit the author to investigate the abstract physical sequence:

**M_t + X_t → R_t → M_(t+1)**

where:

- M_t = pre-existing magnetic state;
- X_t = new physical/electromagnetic input;
- R_t = state-dependent physical response;
- M_(t+1) = resulting magnetic state.

This is analogous to state-dependent processing.

The analogy does NOT establish digital computation, software execution, semantic comparison, addressing, or conscious information processing.

## Important limitation

The anisotropic magnetoresistance and planar Hall measurements cited here were performed on controlled magnetite samples or thin films.

They do NOT establish that bulk volcanic rock exhibits the same magnitude or useful form of magnetoresistive response at geological scale.

Similarly, piezomagnetic and piezo-remanent experiments establish changes in natural-rock magnetization under stress, but do NOT demonstrate deliberate writing of encoded computer data.

The scientific sources establish physical component mechanisms.

The interpretation of those mechanisms as:

**READ → PROCESS → WRITE**

inside the proposed natural-computer architecture is the author's hypothesis.

## Sources

### Naftalis, N., Kaplan, A., Schultz, M., Vaz, C. A. F., Moyer, J. A., Ahn, C. H. & Klein, L. (2011)

**Field-dependent anisotropic magnetoresistance and planar Hall effect in epitaxial magnetite thin films.**

Physical Review B, 84, 094441.

DOI: 10.1103/PhysRevB.84.094441

Experimental measurements of longitudinal and transverse resistivity in Fe3O4 showing dependence on magnetization/current orientation and applied field.

### Nagata, T. & Carleton, B. J. (1969)

**Notes on Piezo-remanent Magnetization of Igneous Rocks II.**

Journal of Geomagnetism and Geoelectricity, 21, 427–445.

DOI: 10.5636/jgg.21.427

Experimental demonstration of piezo-remanent magnetization in igneous rocks under weak magnetic fields and uniaxial compression.

### Domen, H. (1962)

**Piezo-Remanent Magnetism in Rock and Its Field Evidence.**

Journal of Geomagnetism and Geoelectricity, 13, 66–72.

DOI: 10.5636/jgg.13.66

Demonstrates changes in intensity and direction of remanent magnetization caused by uniaxial pressure.

### Pozzi, J.-P. (1977)

**Effects of stresses on magnetic properties of volcanic rocks.**

Physics of the Earth and Planetary Interiors, 14, 77–85.

DOI: 10.1016/0031-9201(77)90047-4

Experimental study of compressive and tensile stress effects on natural remanent and induced magnetization in volcanic rocks from Mount Etna.

### Hamano, Y. (1983)

**Experiments on the Stress Sensitivity of Natural Remanent Magnetization.**

Journal of Geomagnetism and Geoelectricity, 35, 155–172.

DOI: 10.5636/jgg.35.155

Reports measured changes in natural remanent magnetization during progressive uniaxial compression of rock samples.

### Stacey, F. D. (1958)

**Effect of stress on the remanent magnetism of magnetite-bearing rocks.**

Journal of Geophysical Research, 63, 361–368.

DOI: 10.1029/JZ063i002p00361

Establishes strong stress sensitivity of remanent magnetization in magnetite-bearing rocks.

### Zanella, E. & Lanza, R. (1994)

**Remanent and induced magnetization in the volcanites of Lipari and Vulcano (Aeolian Islands).**

Annals of Geophysics.

DOI: 10.4401/ag-4163

Measurements on natural volcanic lithologies identify titanomagnetite as the major magnetic carrier and document substantial remanent magnetization.

### Cox, A. (1971)

**Remanent magnetization and susceptibility of late Cenozoic rocks from New Zealand.**

New Zealand Journal of Geology and Geophysics, 14, 192–207.

DOI: 10.1080/00288306.1971.10422470

Measurements of remanence and magnetic susceptibility from 176 volcanic-rock samples from 22 North Island formations.

## Accessed

26 August 2026