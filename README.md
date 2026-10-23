# MCED Cost-Effectiveness Simulation

## Research Question

How does baseline cancer risk affect the incremental
cost-effectiveness ratio (ICER) of annual multi-cancer
early detection (MCED) screening?

## Project Overview

We aim to develop an individual-based Monte Carlo
simulation to compare two screening strategies:

1. Usual care
2. Usual care + annual MCED screening

We will compare the cost-effectiveness of these
strategies in lower-risk and higher-risk populations.

## Computational Methods

- Individual-based Monte Carlo simulation
- Monthly state transitions
- Bernoulli random sampling
- Cost-effectiveness analysis (ICER)
- Sensitivity analysis

## Python Libraries

- random
- NumPy
- pandas
- Matplotlib

## Current Progress

- Initial proposal completed
- Simulation framework outlined
- Required model parameters identified
- Parameter template (parameters.csv) created
- Starter screening script (simulation.py) created
- Reference results from Raoof et al. (2025) added (reference_icers.csv)
- Data collection and implementation pending

## Planned Development

1. Collect published model parameters.
2. Implement cancer incidence and progression.
3. Implement annual MCED screening.
4. Calculate costs and QALYs.
5. Compare ICERs across risk groups.
6. Perform sensitivity analysis.
