# Ocean Current Analyzer v3.0

V3 keeps the working V2 parser and adds cross-depth physics.

## Install

```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

A virtual environment is safer, but the command above is the direct macOS/Homebrew bypass requested earlier.

## Run

Put all original `.tab` files in the same folder and run:

```bash
python3 analyze_ocean_currents_v3.py . -o results_v3
```

Optional GIF animations:

```bash
python3 analyze_ocean_currents_v3.py . -o results_v3 --animation
```

For faster testing:

```bash
python3 analyze_ocean_currents_v3.py PS137_21-1_AURORA1_CurrentVelocity.tab Y1-1_microcat.tab -o test_v3 --max-depth-series 30
```

## Outputs

- `m2_depth_profiles.csv` — M2 ellipse amplitude, signed minor axis, orientation, wrapped/unwrapped phase and apparent phase gradient.
- `m2_pairwise_coherence_lag.csv` — pairwise M2-band vector coherence and lag between depths.
- `rotary_m2_summary.csv` — CW and CCW M2 power at representative depths.
- `eof_variance_summary.csv` — variance explained by the first five M2-band EOF modes.
- `errors_v3.csv`
- `plots/`
- `ocean_current_v3_report.pdf`

## Interpretation warning

The calculated vertical phase speed is an **apparent phase speed inferred from a linear phase-depth gradient**. It is not automatically a physical vertical group velocity. Large phase wraps, mooring geometry, mixed barotropic/baroclinic signals and noisy bins can make it misleading. Treat it as a diagnostic, not a final physical conclusion.

The PVD is a virtual trajectory obtained by integrating measured Eulerian current and is not the measured path of a real water parcel.
