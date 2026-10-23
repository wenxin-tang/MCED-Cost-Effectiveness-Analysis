# Data Sources

Main reference: Raoof S, Kansal AR, Tafazzoli A, Ye W, Morris W, Zou D,
Fendrick AM. Impact of population cancer risk on the cost-effectiveness of
multicancer early detection testing in the United States. Cancer Epidemiol
Biomarkers Prev. 2025;34(11):2085-2094.
https://doi.org/10.1158/1055-9965.EPI-25-0610

## Already in this repo

| File | Contents | Source |
|---|---|---|
| reference_icers.csv | ICER, incremental cost, incremental QALY, prevalence, mortality HR by subpopulation | Raoof 2025, Tables 1 and 3 |
| irr_by_cancer_type.csv | Incidence rate ratios by cancer type for each higher-risk subpopulation | Raoof 2025, Table 2 |
| parameters.csv | MCED specificity (0.995) | Klein 2021; Raoof 2025 |

## Still to collect

| Parameter | Where to get it |
|---|---|
| Incidence by age and stage | SEER*Explorer: https://seer.cancer.gov/statistics-network/explorer/archive.html |
| Stage distribution at diagnosis | SEER*Explorer, Stage Distribution file |
| Survival by stage | SEER*Explorer, Survival files |
| Background mortality | CDC life tables: https://www.cdc.gov/nchs/products/life_tables.htm |
| MCED sensitivity by stage | Klein et al. 2021, Annals of Oncology (CCGA3). News reports give stage I to IV as 16.8%, 40.4%, 77%, 90.1%. Confirm in the paper before using. |
| Costs and utilities | Raoof 2025, Supplementary Table S1 (needs download from the journal site) |
| Gene-level incidence ratios | Raoof 2025, Supplementary Tables S3 and S4 |

## Notes

- Table 2 lists breast cancer separately for HR negative and HR positive, with the same values.
- HCS means hereditary cancer syndrome. "Overall" columns give the mean ratio, and the low and high columns give the reported range.
- The paper's authors are from GRAIL, the company that makes the Galleri test.
