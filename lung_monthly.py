import csv
import random

from Individuals import Individual


def annual_to_monthly(p_annual):
    # yearly chance -> monthly chance
    return 1 - (1 - p_annual) ** (1 / 12)


def lung_monthly_incidence(csv_path, risk_multiplier=1.0):
    # monthly chance of lung cancer for each SEER age group
    # risk_multiplier is 1 for everyone, or the value from irr_by_cancer_type.csv (current smoker = 3.75)
    monthly = {}
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if row["model_cancer_type"] == "Lung and bronchus" and row["stage"] == "All Stages":
                p_annual = float(row["rate_per_100k"]) / 100000 * risk_multiplier
                monthly[row["age_group"]] = annual_to_monthly(p_annual)
    return monthly


def seer_age_group(age):
    # 50-54, 55-59, ... 75-79 (80 and older uses 75-79)
    start = min(int(age) // 5 * 5, 75)
    return f"{start}-{start + 4}"


def simulate_lung_onset(monthly, n_people=10000, start_age=50, years=20, seed=1):
    # every month each healthy person has a chance of getting lung cancer
    # no deaths and no stages here, just counting who gets it
    random.seed(seed)
    people = [Individual(id=i, age=start_age, sex="Both", is_smoker=False) for i in range(n_people)]

    for month in range(years * 12):
        age = start_age + month / 12
        p = monthly[seer_age_group(age)]
        for person in people:
            person.age = age
            if not person.has_cancer and random.random() < p:
                person.has_cancer = True

    return sum(1 for person in people if person.has_cancer)


def expected_share(monthly, start_age=50, years=20):
    # what we should get: 1 - chance of never getting lung cancer
    never = 1.0
    for month in range(years * 12):
        age = start_age + month / 12
        never *= 1 - monthly[seer_age_group(age)]
    return 1 - never


if __name__ == "__main__":
    path = "data/seer/seer_incidence_by_age.csv"

    for label, mult in [("General population", 1.0), ("Current smokers", 3.75)]:
        monthly = lung_monthly_incidence(path, mult)
        cases = simulate_lung_onset(monthly)
        print(label)
        print("  simulated lung cancer cases out of 10,000:", cases)
        print("  expected:", round(expected_share(monthly) * 10000))
