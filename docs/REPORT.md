# MMA3001 Project report draft — Numerical modelling of vehicle suspension free vibration

**Status:** reproducible computational study; self-selected project requires teaching-team approval. **Authorship:** AI-assisted draft; student must verify, adapt, and personally explain all work.

## 1. Engineering problem
A vehicle suspension reduces vertical oscillation following disturbances. This project studies a simplified one-degree-of-freedom sprung-mass suspension displaced 0.08 m from its equilibrium position and released from rest. The goal is to predict displacement and velocity for five seconds and evaluate whether fourth-order Runge–Kutta (RK4) improves accuracy over explicit Euler at comparable time steps. This is an idealised free-vibration test, **not** a model of a real road bump or a calibrated full vehicle suspension.

## 2. Inputs and outputs
The inputs are effective mass 300 kg, spring stiffness 18,000 N/m, damping 1,500 N s/m, initial displacement 0.08 m, initial velocity 0 m/s, simulation duration 5 s and step sizes 0.2 to 0.0125 s. These values are illustrative assumptions. The solver outputs time (s), displacement (m), and velocity (m/s). Derived outputs are displacement root-mean-square error (RMSE, m), maximum absolute error (m), and approximate runtime (ms). Invalid parameters, time steps, initial conditions, and solver names raise explicit exceptions.

## 3. Computational approach
Newton's second law gives `m*x'' + c*x' + k*x = 0`. Let `y=[x,v]` with `v=x'`. Then `y'=[v,-(c*v+k*x)/m]`. Explicit Euler updates `y[n+1]=y[n]+h*f(t[n],y[n])`. Classical RK4 computes four derivative slopes and combines them with weights 1,2,2,1 divided by 6. Euler is simple and cheap per step but first-order accurate; RK4 is more computationally expensive per step but fourth-order accurate for sufficiently smooth solutions and small step sizes.

For validation, the system is underdamped: `alpha=c/(2m)=2.5 s^-1`, `omega_n=sqrt(k/m)=sqrt(60) rad/s`, and `omega_d=sqrt(omega_n^2-alpha^2)`. The exact displacement is `x(t)=exp(-alpha*t)*(x0*cos(omega_d*t)+((v0+alpha*x0)/omega_d)*sin(omega_d*t))`. Velocity is obtained by differentiating this expression. This provides an independent analytical reference for numerical accuracy, though not experimental evidence that the physical model is realistic.

## 4. Validation and verification
Automated tests verify initial conditions, invalid input handling, exact initial velocity, improved accuracy under time-step refinement, lower RK4 error at the same step size, and non-increasing total mechanical energy under damped RK4 integration at `dt=0.01 s`. All six tests passed in the development environment. The analytical solution was used to calculate displacement RMSE and maximum absolute error at every simulated sample.

At `dt=0.1 s`, Euler displacement RMSE was **0.3070 m** while RK4 RMSE was **9.53e-5 m**. At `dt=0.05 s`, Euler RMSE was **0.00947 m** while RK4 RMSE was **5.34e-6 m**. At `dt=0.2 s`, Euler was unstable, reaching an RMSE of approximately **868 m**: this is a numerical failure, not physical suspension behaviour. RK4 remained accurate at this step size (RMSE approximately **0.00196 m**). The instability highlights the importance of selecting and testing time steps.

## 5. Comparison and optimisation
The comparison varies the integration step while keeping the model and initial conditions fixed. See `results/convergence.csv` and `results/convergence.png`. At `dt=0.05 s`, Euler averaged approximately **0.50 ms** per run versus **2.39 ms** for RK4 on the development machine; runtimes vary with hardware and background load. RK4 needs four derivative evaluations per step, but it delivers much smaller errors here. For an accuracy-oriented simulation, RK4 at `dt=0.05 s` is a reasonable choice; the exact analytical solution is even better for this specific linear free-vibration case, so a numerical method is primarily useful here for teaching and extensibility to more complicated forcing/nonlinear systems. Do not generalise RK4's superiority to every ODE without testing.

## 6. Sensitivity, limitations and lessons
The sensitivity study varies damping between 600, 1,500 and 3,000 N s/m while keeping mass, stiffness and initial conditions fixed (`results/damping_sensitivity.png`). Larger damping changes the decay rate and oscillatory response. The model neglects tyre compliance, unsprung mass, nonlinear dampers, road excitation, pitch/roll, and measured parameter uncertainty. Its validation proves numerical correctness for the chosen ODE, not realistic predictive accuracy for an actual car. A logical extension is a two-degree-of-freedom quarter-car model with measured road input and physical calibration.

## 7. AI use and reflection — complete personally before submission
ChatGPT (GPT-6) assisted substantially with selecting the simulation scope, generating the Python solver and tests, creating graphs, drafting documentation, and structuring the repository. Its outputs were checked by executing the code, running pytest, and comparing solver results with the exact underdamped solution. The student must personally review these results, test additional cases, make and document their own technical decisions, and be able to explain the code and numerical methods in the oral presentation. **Add an accurate first-person account of what you learned, what you changed, mistakes you detected, and which decisions you made independently.** Do not claim independent authorship or checks you did not perform.

## 8. References
- MMA3001 (2026), *Numerical Methods and Machine Learning: Project Brief*, provided unit document.
- MMA3001 (2026), Week 7 learning notebooks: *ODEs and Initial Value Problems*, *Euler's Method*, *Runge–Kutta Methods*, and *Higher Order ODEs*, provided course notes.
- Python, NumPy, Matplotlib, and pytest official documentation (versions and access dates to be added by student).

## Submission and presentation checklist
- Obtain coordinator approval for the self-selected simulation.
- Confirm report formatting and keep the final written submission within 5–10 pages (references/appendices excluded).
- Run the script and tests yourself; inspect plots and make meaningful improvements.
- Generate HTML docs using pdoc; maintain genuine GitHub history with meaningful commits.
- Submit written report through Moodle, repository URL, and zipped clone through Moodle.
- Prepare a five-minute demonstration plus three-minute Q&A, including solver formulas, validation, convergence, stability, limitations, and AI contribution.
