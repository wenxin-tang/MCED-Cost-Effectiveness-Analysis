"""Read and validate the MCED model's category,parameter,value,source CSV.

Usage from Python (place this file beside parameters.csv)::

    from parameter_loader import load_parameters, require_parameters
    params = load_parameters()
    require_parameters(params, ["population_size", "MCED_specificity"])

Blank values remain None; no clinical assumptions or stage mappings are added.
Run ``python parameter_loader.py`` to report missing inputs, or add
``--require MCED_specificity screening_interval_months`` to check a subset.
Only the Python standard library is required.
"""

import argparse
import csv
import math
from pathlib import Path


class ParameterError(ValueError):
    """A model input is missing, malformed, or outside its allowed range."""


# These scalar inputs have explicit meanings in the current parameters.csv.
# Stage-specific mortality/cost/utility tables need a separate table format;
# this loader deliberately does not interpret lists packed into a CSV cell.
POSITIVE_INTEGERS = {
    "population_size", "simulation_years", "screening_interval_months"
}
PROBABILITIES = {
    "baseline_cancer_incidence", "cancer_progression_probability",
    "usual_care_diagnosis_probability", "MCED_specificity",
    "MCED_sensitivity_stage_1", "MCED_sensitivity_stage_2",
    "MCED_sensitivity_stage_3", "MCED_sensitivity_stage_4",
    "background_mortality", "cancer_mortality_by_stage",
    "healthy_utility", "cancer_utility_by_stage", "discount_rate",
}
NONNEGATIVE = {
    "starting_age", "high_risk_multiplier", "screening_cost",
    "diagnostic_workup_cost", "treatment_cost_by_stage",
}


def load_parameters(csv_path=None):
    """Return {parameter_name: int | float | None} without altering the CSV.

    The default path is relative to this module, not the working directory.
    Unknown parameter names are accepted as finite numeric inputs so that
    teammates can extend the CSV. Only names listed above receive range checks.
    OSError is raised for unreadable files; ParameterError for invalid content.
    """
    path = Path(csv_path) if csv_path is not None else Path(__file__).with_name("parameters.csv")
    parameters = {}
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle, strict=True)
            expected = {"category", "parameter", "value", "source"}
            if (reader.fieldnames is None or len(reader.fieldnames) != 4
                    or set(reader.fieldnames) != expected):
                raise ParameterError(f"{path}: expected columns category,parameter,value,source")
            for row in reader:
                location = f"{path}: line {reader.line_num}"
                if None in row or any(value is None for value in row.values()):
                    raise ParameterError(f"{location}: expected exactly four fields")
                name = row["parameter"].strip()
                if not name:
                    raise ParameterError(f"{location}: parameter name is empty")
                if name in parameters:
                    raise ParameterError(f"{location}: duplicate parameter {name!r}")
                raw = row["value"].strip()
                if not raw:
                    parameters[name] = None
                    continue
                try:
                    value = float(raw)
                except ValueError as exc:
                    raise ParameterError(f"{location}: {name} must be one numeric value, got {raw!r}") from exc
                if not math.isfinite(value):
                    raise ParameterError(f"{location}: {name} must be finite")
                if name in POSITIVE_INTEGERS:
                    if value <= 0 or not value.is_integer():
                        raise ParameterError(f"{location}: {name} must be a positive integer")
                    value = int(value)
                elif name in PROBABILITIES and not 0 <= value <= 1:
                    raise ParameterError(f"{location}: {name} must be between 0 and 1 (use 0.995, not 99.5)")
                elif name in NONNEGATIVE and value < 0:
                    raise ParameterError(f"{location}: {name} must be nonnegative")
                parameters[name] = value
    except csv.Error as exc:
        raise ParameterError(f"{path}: invalid CSV: {exc}") from exc
    if not parameters:
        raise ParameterError(f"{path}: no parameter rows found")
    return parameters


def require_parameters(parameters, required_names):
    """Raise ParameterError if any required name is absent or blank.

    Call after load_parameters and before running the corresponding model arm.
    """
    missing = sorted({name for name in required_names if parameters.get(name) is None})
    if missing:
        raise ParameterError("Missing required parameters: " + ", ".join(missing))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", nargs="?", help="Defaults to parameters.csv beside this file")
    parser.add_argument("--require", nargs="+", metavar="NAME", help="Check only these inputs for missing values; default: all inputs")
    args = parser.parse_args()
    try:
        parameters = load_parameters(args.csv_path)
        missing = [name for name, value in parameters.items() if value is None]
        print(f"Loaded {len(parameters)} parameters; {len(parameters) - len(missing)} filled, {len(missing)} blank.")
        require_parameters(parameters, args.require if args.require is not None else parameters)
    except (OSError, ParameterError) as exc:
        parser.exit(1, f"Parameter check failed: {exc}\n")
    print("All required parameters are available and valid.")


if __name__ == "__main__":
    main()
