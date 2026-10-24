# Inputs and outputs — MMA3001 suspension model

| Input | Unit | Valid range and behaviour | Default |
|---|---|---|---|
| method | text | Euler or RK4; otherwise ValueError | required |
| mass | kg | finite >0 | 300 |
| stiffness | N/m | finite >0 | 18000 |
| damping | N s/m | finite >=0 | 1500 |
| initial displacement | m | finite real number | 0.08 |
| initial velocity | m/s | finite real number | 0 |
| duration | s | finite >0 | 5 |
| time step dt | s | finite >0; at most 2 million intervals in updated local package | 0.05 |

Outputs from simulate: time vector (seconds) and state array with columns displacement (metres), velocity (metres per second). Analysis outputs: PNG solver comparison, convergence, damping sensitivity; CSV RMSE (m), maximum displacement error (m), average runtime (ms), number of time points, and sensitivity measurements. All errors are numerical comparisons with an analytical model, **not experimental measurement errors**. Missing external data is not an issue because this is a simulation and does not use the uploaded occupancy or environmental sensor datasets. The full updated local package includes additional parameter and invalid-input tests.

Note: the latest local downloadable ZIP contains updates not yet synchronized to GitHub; use that package as the definitive enhanced draft until the repository is updated.
