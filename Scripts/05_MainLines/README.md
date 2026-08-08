# Cappadocia Corridor Investigation

This directory contains one of the most interesting measurements collected during the **Measurable Science** project.

Unlike most locations investigated so far, the objective here was **not** to search for the carrier commonly observed near **7.8 Hz**.

The location was selected because, according to the model described in the accompanying book, it should lie close to the region between two neighboring carrier structures.

The complete recording used for this analysis is available on Google Drive.

Recording:

https://drive.google.com/file/d/11J2pyxG9mH2vXLDfLnFNU4uI9zzFyalI/view?usp=drive_link

The recording exceeds GitHub's file size limit by more than five times and therefore cannot be included directly in this repository.

---

# Blind Carrier Discovery

The recording was first analyzed using the **Blind Beauty Detector** included in this repository.

Unlike traditional FFT peak detection, this script searches the entire selected frequency range for organized phase-coherent structures without assuming where the carrier should exist.

The results were very different from the majority of measurements collected during this project.

Across more than one thousand recordings performed at different locations, a clearly organized carrier has consistently been detected somewhere within approximately **7.8 ± 0.5 Hz**.

Depending on the location, the strongest carrier may appear near **7.3 Hz**, **7.8 Hz** or **8.3 Hz**, but an organized carrier is normally present within this frequency region.

At this location that behavior was absent.

Instead, the analysis revealed:

- no significant organized carrier near **7.8 Hz**;
- a dominant coherent band between approximately **1.1 and 1.7 Hz**;
- the strongest resonance centered near **1.6 Hz**.

This immediately suggested that the field at this location behaves differently from the majority of measured sites.

---

# Carrier Characterization

The strongest detected resonance was then analyzed using the **Carrier Characterization** script.

The carrier was refined to approximately **1.400 Hz** and characterized using band-pass filtering, Hilbert transform and three-dimensional covariance analysis.

The measured properties were:

- dominant frequency approximately **1.4 Hz**;
- nearly vertical principal oscillation axis (**83°** elevation);
- approximately **58.7%** of the measured energy contained in the vertical component;
- flattened rotating elliptical geometry;
- continuous phase variation over time;
- continuous azimuth variation over time;
- only mild phase stabilization during the highest-energy intervals.

These measurements describe a field that is both highly dynamic and predominantly vertical.

---

# Interpretation

Within the model proposed in the accompanying book, these observations are consistent with the expected behavior of a region located between two neighboring rotating standing-wave carriers.

If two neighboring carriers rotate while maintaining standing-wave structure, the region between them is expected to be dominated by a dynamic channel rather than by another localized carrier.

Such a channel would be expected to exhibit:

- the absence of a strong local carrier near **7.8 Hz**;
- a dominant lower-frequency organized resonance;
- strong vertical energy concentration;
- continuous rotation of phase and oscillation direction.

The measurements obtained at this location are consistent with these expectations.

This interpretation remains a working hypothesis that should be tested through additional measurements at other locations predicted by the same model.

---

# Historical Observation

One aspect of this location deserves further investigation.

Cappadocia contains one of the world's largest concentrations of ancient monasteries, churches and underground religious complexes.

Whether this historical distribution is unrelated to the measured field characteristics or reflects properties of the local environment cannot be determined from these measurements alone.

However, the coincidence makes the location particularly interesting for future investigation.

---

# Reproducibility

The normalized dataset, analysis scripts and generated reports are included in this repository.

Anyone can repeat the complete analysis, modify the processing parameters or compare these results with measurements acquired at other locations.

Independent verification is strongly encouraged.