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
| data/seer/seer_incidence_by_age.csv | Incidence per 100,000 for ages 50 to 79 in 5-year groups, by cancer type (2018-2022) | SEER*Explorer, Nov 2024 submission |
| data/seer/seer_stage_distribution.csv | Percent of cases by stage (all ages, 50-64, 65+) by cancer type (2013-2022) | SEER*Explorer, Nov 2024 submission |
| data/seer/seer_5yr_relative_survival.csv | 5-year relative survival by stage (all ages, 50-64, 65+) by cancer type (2015-2021) | SEER*Explorer, Nov 2024 submission |

## Still to collect

| Parameter | Where to get it |
|---|---|
| Background mortality | CDC life tables: https://www.cdc.gov/nchs/products/life_tables.htm |
| MCED sensitivity by stage | Klein et al. 2021, Annals of Oncology (CCGA3). News reports give stage I to IV as 16.8%, 40.4%, 77%, 90.1%. Confirm in the paper before using. |
| Costs and utilities | Raoof 2025, Supplementary Table S1 (needs download from the journal site) |
| Gene-level incidence ratios | Raoof 2025, Supplementary Tables S3 and S4 |

## Notes on the SEER files

- Source: SEER Explorer Data Archive, November 2024 SEER Submission (April 2025 Release), https://seer.cancer.gov/statistics-network/explorer/archive.html
- Filters: all races and ethnicities, both sexes, observed (not delay-adjusted) incidence rates, 5-year survival only.
- Breast, ovary, uterus, and cervix are female only. Prostate is male only. Rates for these are per 100,000 of that sex.
- Head and neck is two SEER sites (Oral Cavity and Pharynx, Larynx) and lymphoma is two (Non-Hodgkin, Hodgkin). They are listed separately and not combined.
- The incidence file only gives all-stage rates. For stage-specific incidence, multiply the rate by the percent of cases at each stage.
- The stage and survival files include an In Situ stage for some cancers. Bladder has the most extra rows.
- Survival is relative survival (compared with the general population), not raw survival.

## Other notes

- Table 2 lists breast cancer separately for HR negative and HR positive, with the same values.
- HCS means hereditary cancer syndrome. "Overall" columns give the mean ratio, and the low and high columns give the reported range.
- The paper's authors are from GRAIL, the company that makes the Galleri test.
