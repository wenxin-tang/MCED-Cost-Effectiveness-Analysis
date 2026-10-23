# MCED Cost-Effectiveness Simulation

## Research question
How does baseline cancer risk change the cost-effectiveness of annual multi-cancer early detection (MCED) screening?

## What we are building
An individual-based Monte Carlo simulation in Python. It compares two strategies:

1. Usual care
2. Usual care plus annual MCED screening

We run both in lower-risk and higher-risk groups. Then we compare the ICER, which is the extra cost for each extra QALY gained.

## Files

| File | What it is |
|---|---|
| simulation.py | Starter script. Simulates one round of screening and counts true and false positives and negatives. |
| parameters.csv | Model inputs. Values are still being filled in. |
| reference_icers.csv | Results from Raoof et al. (2025). We check our model against these. |
| irr_by_cancer_type.csv | How much more likely each risk group is to get each cancer. |
| data/seer/ | SEER tables for incidence, stage, and survival. |
| DATA_GUIDE.md | Where the data comes from and what every row means. |

## Progress
- [x] Proposal and model outline
- [x] Parameter list
- [x] Starter screening script
- [x] Reference results from Raoof et al. (2025)
- [x] Incidence, stage, and survival tables from SEER
- [ ] Life tables, MCED sensitivity by stage, costs, and utilities
- [ ] Monthly individual-based model
- [ ] Costs, QALYs, and ICERs by risk group
- [ ] Sensitivity analysis and plots

## Run
```
python simulation.py
```

## Main reference
Raoof S, et al. Impact of population cancer risk on the cost-effectiveness of multicancer early detection testing in the United States. Cancer Epidemiol Biomarkers Prev. 2025;34(11):2085-2094. https://doi.org/10.1158/1055-9965.EPI-25-0610
