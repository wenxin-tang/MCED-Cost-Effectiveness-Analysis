import pandas as pd
import random

# Load parameters from CSV
df = pd.read_csv("data/mced_parameters.csv")
params = dict(zip(df["parameter"], df["value"]))

def mced_test(has_cancer, stage=None):
    """Simulate a positive or negative MCED test result."""

    if not has_cancer:
        return random.random() < (1 - params["specificity"])

    if stage not in (1, 2, 3, 4):
        raise ValueError("Cancer stage must be 1, 2, 3, or 4")

    sensitivity = params[f"sensitivity_stage_{stage}"]
    return random.random() < sensitivity

# Example: test 1000 patients with Stage I lung cancer
results = [mced_test(True, 1) for _ in range(1000)]

print("Stage I detection rate:", sum(results) / len(results))
