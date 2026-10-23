def calculate_screening_results(
    population,
    cancer_risk,
    sensitivity,
    specificity
):
    cancer_cases = population * cancer_risk
    healthy_people = population - cancer_cases

    true_positives = cancer_cases * sensitivity
    false_negatives = cancer_cases * (1 - sensitivity)

    false_positives = healthy_people * (1 - specificity)
    true_negatives = healthy_people * specificity

    return {
        "TP": true_positives,
        "FN": false_negatives,
        "FP": false_positives,
        "TN": true_negatives
    }
