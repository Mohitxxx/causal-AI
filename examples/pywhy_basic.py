"""Minimal causal inference example using pywhy/dowhy."""
from dowhy import CausalModel
import pandas as pd


def main() -> None:
    # Synthetic data with a confounder (U) affecting treatment (T) and outcome (Y)
    data = pd.DataFrame(
        {
            "U": [0, 1, 0, 1, 0, 1, 0, 1],
            "T": [0, 1, 0, 1, 1, 1, 0, 0],
            "Y": [1.0, 3.1, 1.2, 3.0, 2.8, 3.2, 1.1, 0.9],
        }
    )

    model = CausalModel(
        data=data,
        treatment="T",
        outcome="Y",
        common_causes=["U"],
    )

    identified_estimand = model.identify_effect()
    estimate = model.estimate_effect(
        identified_estimand,
        method_name="backdoor.linear_regression",
    )

    print("Estimated causal effect of T on Y:", estimate.value)


if __name__ == "__main__":
    main()
