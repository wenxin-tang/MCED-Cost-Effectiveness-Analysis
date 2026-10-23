import random


def simulate_screening(
    population_size,
    cancer_prevalence,
    sensitivity,
    specificity
):
    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for _ in range(population_size):

        has_cancer = random.random() < cancer_prevalence

        if has_cancer:
            test_positive = random.random() < sensitivity

            if test_positive:
                true_positive += 1
            else:
                false_negative += 1

        else:
            test_positive = random.random() < (1 - specificity)

            if test_positive:
                false_positive += 1
            else:
                true_negative += 1

    return {
        "TP": true_positive,
        "FP": false_positive,
        "TN": true_negative,
        "FN": false_negative
    }


if __name__ == "__main__":

    results = simulate_screening(
        population_size=10000,
        cancer_prevalence=0.01,
        sensitivity=0.75,
        specificity=0.99
    )

    print(results)
