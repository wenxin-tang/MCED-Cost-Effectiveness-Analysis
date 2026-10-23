# Data Guide

What each file is, where it came from, and what every row means.

## 1. Sources

| Source | Used for |
|---|---|
| Raoof et al. (2025), https://doi.org/10.1158/1055-9965.EPI-25-0610 | Risk groups, incidence ratios, reference ICERs |
| SEER Explorer, November 2024 submission, https://seer.cancer.gov/statistics-network/explorer/archive.html | Incidence, stage, survival |
| Klein et al. (2021), Annals of Oncology | MCED sensitivity and specificity |

Still to collect: life tables (CDC), MCED sensitivity by stage, costs, utilities. Costs and utilities are in the supplement of Raoof et al. (Table S1).

## 2. parameters.csv
Columns: parameter, value, source. One row per model input.

| Row | Meaning |
|---|---|
| baseline_cancer_incidence | Chance of getting cancer in the general population. Comes from the SEER incidence file. |
| high_risk_multiplier | How many times more likely a risk group is to get cancer. See irr_by_cancer_type.csv. |
| cancer_progression_probability | Monthly chance an undiagnosed cancer moves to the next stage. |
| MCED_sensitivity_stage_1 to stage_4 | Chance the test is positive when cancer is present at that stage. Blank for now. |
| MCED_specificity | 0.995. A healthy person tests negative 99.5% of the time. False alarms happen 0.5% of the time. |
| screening_cost | Price of one test. |
| diagnostic_workup_cost | Cost of follow-up after a positive test. |
| treatment_cost | Cost of treatment, by stage. |
| healthy_utility | Quality of life when healthy, from 0 to 1. |
| cancer_utility | Quality of life with cancer, from 0 to 1. |
| background_mortality | Chance of dying from other causes, by age. |
| stage_specific_survival | How long people live after diagnosis, by stage. |
| usual_care_diagnosis_probability | Chance cancer is found without MCED, by stage. |
| discount_rate | Future costs and QALYs count less each year, for example 3%. |

## 3. reference_icers.csv
The answer key from Raoof et al. Table 3. One row per group.

Columns:
- prevalence_pct: share of adults in the group
- all_cause_mortality_hr: how much higher the group's death risk is. 1.42 means 42% higher.
- incremental_cost: extra cost per person from adding MCED
- incremental_qaly: extra QALYs per person from adding MCED
- icer_per_qaly: extra cost divided by extra QALYs. Lower is better value.

| Row | What it says |
|---|---|
| General population | $66,043. The baseline to compare against. |
| Diabetes | $66,010. Diabetes barely raises cancer risk, so it is no better than average. |
| Obesity | $60,245. |
| Ever-smoker | $43,553. |
| First-degree family history | $40,155. The largest group, at 55%. |
| Cancer survivor | $36,774. Mortality HR is blank because the paper gives several values. |
| Heavy alcohol use | $35,515. |
| Current smoker | $26,850. Highest mortality HR, at 1.95. |
| Immunocompromised SOT | $18,013. A very small group, at 0.06%. |
| HCS overall | $544. Extra cost is only $148, so MCED is almost free here. |

Pattern: higher cancer risk gives a lower ICER. This is our hypothesis. The paper's numbers are rounded, so cost divided by QALY will not match the ICER exactly.

## 4. irr_by_cancer_type.csv
From Raoof et al. Table 2. One row per cancer type and one column per risk group.

A value is how many times more likely the group is to get that cancer than the general population. 1 means the same. 2 means double. Below 1 means less likely.

Group rate = general rate times the value. Example: lung cancer at ages 60 to 64 is 128.13 per 100,000 for everyone. For ever-smokers it is 128.13 x 2.13 = about 273.

Columns:
- diabetes_base, diabetes_scenario: two sources the paper tested
- obesity, ever_smoker, current_smoker, first_degree_family_history, immunocompromised_sot
- heavy_alcohol_base, heavy_alcohol_scenario: two sources the paper tested
- hcs_overall, plus low and high range, and five gene groups (brca_like, atm, lynch, mutyh, other). HCS means hereditary cancer syndrome.

| Row | What stands out |
|---|---|
| Lung and bronchus | Smoking drives it: ever-smoker 2.13, current smoker 3.75. Diabetes and obesity have no effect. |
| Colon and rectum | Gene groups: Lynch 9.12, MUTYH 56.41, other 9.67. Other groups are small, from 1.05 to 1.82. |
| Pancreas | Diabetes 1.58. Gene groups: other 11.58, ATM 5.16. |
| Liver and bile duct | Alcohol 1.85, family history 1.87, diabetes 1.62. Transplant 3.02. |
| Breast HR negative | Gene groups: other 4.49, BRCA-like 3.71, ATM 2.15. Alcohol 1.44. |
| Esophagus | Family history 2.24, current smoker 2.20, transplant 2.64. Diabetes has no effect. |
| Head and neck | Alcohol 3.20 and 3.34. Transplant 6.83. Current smoker 2.81. |
| Stomach | Other gene group 23.99. Obesity 1.36. |
| Ovarian | Gene groups: BRCA-like 9.87, Lynch 9.87. Overall 8.22. |
| Kidney and renal pelvis | Transplant 6.08. Heavy alcohol is below 1 at 0.88. |
| Prostate | Diabetes is below 1 at 0.87. Gene groups are low. |
| Breast HR positive | Same values as HR negative. |
| Lymphoma | Transplant 9.13 is the highest. Alcohol is below 1 at 0.83. |
| Anus | Transplant 4.5. Family history 1.55. |
| Uterus | Lynch 12.30, other 4.19. Obesity 1.53. |
| Bladder | Current smoker 2.12, transplant 2.7. Ever-smoker 1.61. |
| Cervix | Transplant 3.31. Family history 1.60. |
| Urothelial | The paper assumes the same as bladder. |
| Other | All 1. No data. |

## 5. data/seer/
One row is one cancer type and one age group, and sometimes one stage.

Filters: all races and ethnicities, both sexes, observed incidence rates, 5-year survival only.
Breast, ovary, uterus, and cervix are female only. Prostate is male only.
Head and neck is two SEER sites (Oral Cavity and Pharynx, Larynx). Lymphoma is two (Non-Hodgkin, Hodgkin). They are listed separately.

### seer_incidence_by_age.csv
Columns: model_cancer_type, seer_site, years, sex, stage, age_group, rate_per_100k, number_of_cases.
There are 6 age groups (50-54 up to 75-79) for each cancer type. Years are 2018-2022.

Example: lung at 50-54 is 28.97 per 100,000, from 13,836 cases.
To use it, divide by 100,000 to get a yearly chance (0.00029). Then convert to a monthly chance with 1 - (1 - p)^(1/12), which is about 0.0000241.

### seer_stage_distribution.csv
Columns: model_cancer_type, seer_site, years, sex, age_group, stage, percent_of_cases, number_of_cases.
Age groups are all ages, 50-64, and 65+. Years are 2013-2022.
Each group of stages adds up to 100%.

Example: lung, all ages. Localized 24.96%, Regional 20.60%, Distant 47.37%, Unstaged 7.06%.

### seer_5yr_relative_survival.csv
Columns: model_cancer_type, seer_site, years, sex, age_group, stage, five_year_relative_survival_pct, number_of_cases.
Years are 2015-2021.
Relative survival compares cancer patients with people of the same age without cancer.

Example: lung localized is 64.70%. Lung distant is 9.69%. This is why finding cancer early matters.

## 6. Watch out for
- SEER has three stage levels (Localized, Regional, Distant). The MCED test reports stage I to IV. We need a rule to match them.
- The incidence file only has all-stage rates. For stage-specific incidence, multiply the rate by the stage percent.
- MCED sensitivity by stage is blank. News reports give 16.8%, 40.4%, 77%, and 90.1% for stage I to IV. Check the Klein paper before using them.
- The authors of Raoof et al. work for GRAIL, the company that makes the Galleri test.
