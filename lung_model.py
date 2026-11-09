import csv
import random

from Individuals import Individual
from lung_monthly import lung_monthly_incidence, seer_age_group

STAGE_NAMES = {1: "Localized", 2: "Regional", 3: "Distant"}


def age_label(age):
    # the stage and survival files only have these two age groups
    return "Ages 50-64" if age < 65 else "Ages 65+"


def load_stage_mix(csv_path):
    # share of lung cancers found at each stage, by age group
    # unstaged cases are left out and the rest are rescaled to add up to 1
    raw = {}
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if row["model_cancer_type"] != "Lung and bronchus" or row["age_group"] not in ("Ages 50-64", "Ages 65+"):
                continue
            for stage, name in STAGE_NAMES.items():
                if row["stage"] == name:
                    raw.setdefault(row["age_group"], {})[stage] = float(row["percent_of_cases"])
    mix = {}
    for group, shares in raw.items():
        total = sum(shares.values())
        mix[group] = {stage: share / total for stage, share in shares.items()}
    return mix


def load_five_year_survival(csv_path):
    # 5-year relative survival by stage and age group, as a fraction
    survival = {}
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if row["model_cancer_type"] != "Lung and bronchus" or row["age_group"] not in ("Ages 50-64", "Ages 65+"):
                continue
            for stage, name in STAGE_NAMES.items():
                if row["stage"] == name:
                    survival.setdefault(row["age_group"], {})[stage] = float(row["five_year_relative_survival_pct"]) / 100
    return survival


def five_year_to_monthly_death(s5):
    # same idea as annual_to_monthly, over 60 months
    # assumes the same risk every month, which is a simplification
    return 1 - s5 ** (1 / 60)


def background_monthly_death(age):
    # chance of dying from something other than lung cancer
    # todo: use the CDC life table, for now nobody dies of other causes
    return 0.0


def simulate_lung(monthly_onset, stage_mix, survival, n_people=10000, start_age=50, years=20, seed=1):
    random.seed(seed)
    people = [Individual(id=i, age=start_age, sex="Both", is_smoker=False) for i in range(n_people)]
    death_by_stage = {
        group: {stage: five_year_to_monthly_death(s5) for stage, s5 in stages.items()}
        for group, stages in survival.items()
    }

    stage_counts = {1: 0, 2: 0, 3: 0}
    cancer_deaths = 0

    for month in range(years * 12):
        age = start_age + month / 12
        p_onset = monthly_onset[seer_age_group(age)]
        group = age_label(age)
        stages = [1, 2, 3]
        weights = [stage_mix[group][s] for s in stages]

        for person in people:
            if not person.alive:
                continue
            person.age = age

            # other causes of death
            if random.random() < background_monthly_death(age):
                person.alive = False
                continue

            if not person.has_cancer:
                # new lung cancer, pick a stage
                if random.random() < p_onset:
                    person.has_cancer = True
                    person.detected = True
                    person.stage = random.choices(stages, weights)[0]
                    stage_counts[person.stage] += 1
            else:
                # already has cancer, may die of it
                if random.random() < death_by_stage[group][person.stage]:
                    person.alive = False
                    cancer_deaths += 1

    return {
        "cases": sum(stage_counts.values()),
        "by_stage": stage_counts,
        "lung_cancer_deaths": cancer_deaths,
        "alive_at_end": sum(1 for p in people if p.alive),
    }


if __name__ == "__main__":
    incidence_csv = "data/seer/seer_incidence_by_age.csv"
    stage_csv = "data/seer/seer_stage_distribution.csv"
    survival_csv = "data/seer/seer_5yr_relative_survival.csv"

    stage_mix = load_stage_mix(stage_csv)
    survival = load_five_year_survival(survival_csv)

    for label, mult in [("General population", 1.0), ("Current smokers", 3.75)]:
        onset = lung_monthly_incidence(incidence_csv, mult)
        result = simulate_lung(onset, stage_mix, survival)
        print(label)
        print("  lung cancer cases:", result["cases"])
        print("  by stage (localized, regional, distant):", result["by_stage"][1], result["by_stage"][2], result["by_stage"][3])
        print("  died of lung cancer:", result["lung_cancer_deaths"])
        print("  alive after 20 years:", result["alive_at_end"], "of 10000")
