# Verification, validation and alternatives

## What is checked?
Verification: explicit Euler and classical RK4 solve m*x''+c*x'+k*x=0. The exact underdamped analytical solution is the numerical reference. RMSE and maximum absolute displacement error have units of metres.

Physical validation: **not established**. No measured car or suspension-rig response is available. A published MIT OCW example (m=500 kg, k=50000 N/m, c=2000 N s/m) is a parameter plausibility example, not experimental validation.

## Acceptance criteria
- RK4 displacement RMSE at dt=0.05 s below 0.001 m.
- Errors decrease when dt is reduced from 0.1 to 0.05 s for both solvers.
- RK4 observed convergence order close to four.
- For sufficiently small dt, damped mechanical energy does not increase.
- Invalid inputs rejected; unstable Euler case identified and reported.

## Observed baseline results
| Method | dt (s) | displacement RMSE (m) |
|---|---:|---:|
| Euler | 0.20 | 868.4159 |
| Euler | 0.10 | 0.307020 |
| Euler | 0.05 | 0.00947156 |
| RK4 | 0.20 | 0.00195787 |
| RK4 | 0.10 | 0.0000953454 |
| RK4 | 0.05 | 0.00000533992 |

Euler at dt=0.2 s is unstable and its very large error is not physical. Euler at dt=0.1 s is also outside the asymptotic stability region, despite its much smaller finite-horizon error. The enhanced local package includes 11 automated tests; the GitHub tests should be updated to match that package.

## Alternatives
Euler: simple, one derivative evaluation per step, inaccurate or unstable at coarse step. RK4: four derivative evaluations per step, much better accuracy at matched step. Exact solution: best when available for this linear underdamped model; not a general solver for forced or nonlinear systems. Adaptive Runge–Kutta is a credible future comparison, not an implemented solver.

## Limits
The numerical reference and simulation share physical assumptions. A real vehicle comparison requires measured displacement/acceleration and parameter identification on independent data. Re-run all timings on your own computer before submission.
