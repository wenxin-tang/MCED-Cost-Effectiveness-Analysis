from model import calculate_screening_results

results = calculate_screening_results(
    population=10000,
    cancer_risk=0.01,
    sensitivity=0.80,
    specificity=0.95
)

print(results)
