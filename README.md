# MMA3001 — Vehicle suspension numerical simulation

A **self-selected simulation proposal (requires unit coordinator approval)** for a simplified quarter-car suspension's free vibration. Compares explicit Euler and classical RK4 against an exact analytical solution of a damped mass–spring system.

## Engineering model

`m*x'' + c*x' + k*x = 0`, where `x` is vertical displacement relative to equilibrium (m), `m` is effective sprung mass (kg), `c` is damping (N s/m), and `k` is spring stiffness (N/m). Assumes linear suspension, constant parameters, no tyre dynamics, no road forcing after release, and one degree of freedom. Initial displacement represents an idealised disturbance and release, **not a physically resolved road-bump profile**.

Defaults: `m=300 kg`, `k=18000 N/m`, `c=1500 N s/m`, `x(0)=0.08 m`, `v(0)=0 m/s`, 5 seconds. These are illustrative assumptions, **not values calibrated to the uploaded sensor datasets**.

## Reproduce

Requires Python 3.10+.

```bash
python -m pip install -r requirements.txt
python src/run_analysis.py
python -m pytest -q tests
python -m pdoc src/suspension.py src/run_analysis.py -o docs/html
```

Outputs: `results/solver_comparison.png`, `results/convergence.png`, `results/damping_sensitivity.png`, `results/convergence.csv`, `results/sensitivity.csv`. HTML documentation generated in `docs/html/`.

## Input/output contracts

`simulate(method, p, initial, duration, dt)` accepts `method` as `Euler` or `RK4`, a validated `Parameters` object, a finite 2-element initial state `[m, m/s]`, a positive duration (s), and positive maximum time step (s). Returns time vector (s) and two-column state `[displacement (m), velocity (m/s)]`. Invalid method, parameter, step, duration, or state raises `ValueError`. No external dataset is required.

## Verification and limits

Exact solution for underdamped free vibration, RMSE and max absolute displacement error, convergence on step refinement, energy decay test, and damping sensitivity. Timing is environment-dependent. No experimental validation or suspension hardware calibration is claimed. RK4 has four derivative evaluations per step; Euler has one. Explicit methods may become unstable at excessive step sizes.

## Project assessment notes

See `docs/REPORT.md` for the report draft, model assumptions, result interpretation, and AI disclosure template. Verify the results and write your own personal AI reflection before submitting. Upload to your own GitHub repository with meaningful commits, and submit its URL and a zipped clone as required by the brief.

## Data provenance

This simulation does **not** use the environmental or occupancy sensor ZIP files. It follows the simulation option in the project brief, rather than implying that those datasets describe vehicle suspensions.
