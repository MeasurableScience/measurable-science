# 06 – Directors and Emitters

This section contains the comparative analysis of several locations that, according to the proposed model described in the book, may represent either **emitters** or **directors** within the natural field system.

The objective is not to prove the model, but to provide the complete datasets, processing scripts, and results so that anyone can independently verify the analysis or contribute additional measurements.

---

# Locations

The current dataset includes recordings from:

- Rtanj (Serbia)
- Glaveja (Serbia)
- Blagotin (Serbia)
- Mauao (New Zealand)
- Otanewainuku (New Zealand)

These locations were selected because repeated field measurements revealed stable phase-coherent frequency bands that warranted further investigation.

---

# Data Processing

All recordings were processed using the analysis scripts included in this repository.

The workflow is fully transparent:

1. normalize recordings into a common format;
2. identify phase-coherent frequency bands using the PLV carrier detector;
3. calculate the integrated energy within each detected frequency band;
4. remove redundant overlapping bands using objective criteria;
5. rank the remaining bands by integrated energy.

The complete processing script is included in this repository and performs the same procedure for every location without manual adjustment. :contentReference[oaicite:0]{index=0}

---

# Why only the Top 3 bands?

Many frequency bands can be detected within a recording.

Instead of selecting frequencies manually, the analysis objectively ranks all detected bands according to their integrated energy.

Only the three strongest non-overlapping bands are presented for comparison.

The complete measurements remain available for anyone wishing to perform additional analyses.

---

# Preliminary Observations

Although the investigated locations are separated by thousands of kilometers, several recurring characteristics appear:

- similar dominant frequency regions;
- similar vertical (Z-axis) energy contribution;
- similar processing modes selected by the PLV detector;
- comparable energetic hierarchy between the strongest channels.

Some locations exhibit very similar frequency structures, while others show distinctive characteristics.

For example, Rtanj displays a strong band near **4.3 Hz**, which differs from the dominant structures observed at several other sites.

Rather than weakening the model, these differences may indicate that individual locations perform different functions within the proposed system.

Whether this interpretation is correct remains an open research question.

---

# Comparative Figures

The generated figures illustrate:

- comparison of the three strongest energy bands for every location;
- relative dominance of the strongest channels;
- frequency ranges occupied by the detected energetic structures.

Unlike a CSV table that lists only the central frequency, these figures show the entire frequency interval occupied by each energetic channel, making similarities and differences between locations much easier to evaluate.

---

# Open Research

This repository intentionally includes:

- raw recordings;
- processing scripts;
- generated CSV files;
- comparison figures.

The purpose is not to ask anyone to accept the interpretation presented in the accompanying book.

Instead, the goal is to encourage independent measurements, independent analysis, and open discussion.

If researchers obtain recordings from additional locations using compatible sensors, the same scripts can be executed without modification, allowing the database of investigated sites to grow over time.

Every additional measurement helps evaluate whether these recurring frequency structures represent reproducible natural phenomena or merely local effects.

---

# Carrier Coupling Analysis

In addition to identifying the strongest energetic channels, an experimental analysis was performed to investigate whether these channels exhibit temporal coupling with the frequency region commonly associated with the first Schumann resonance.

Several complementary methods were applied, including:

- envelope coherence analysis;
- sliding-window coherence stability;
- transfer function comparison between energetic channels and the Schumann frequency band.

The purpose of these analyses is not to demonstrate a physical mechanism, but to determine whether recurring statistical relationships exist between the strongest local energetic bands and the Schumann frequency region.

Across the investigated locations, moderate and relatively stable envelope coherence was observed, while transfer-function estimates remained of the same order of magnitude despite the large geographical separation of the measurement sites.

These observations alone do not demonstrate causal coupling. However, they provide additional evidence that the detected energetic structures deserve further investigation and motivate future synchronized measurements performed simultaneously at multiple locations.

---

# Comparative Figures

The generated figures illustrate:

- comparison of the three strongest energy bands for every location;
- relative dominance of the strongest channels;
- frequency ranges occupied by the detected energetic structures;
- envelope coherence with the Schumann frequency band;
- temporal stability of the observed coherence;
- transfer-function comparison across measurement sites.

Unlike a CSV table that lists only the central frequency, these figures show the entire frequency interval occupied by each energetic channel, making similarities and differences between locations much easier to evaluate.