# causal-AI

Causal AI focuses on understanding cause-and-effect relationships rather than relying solely on correlations. Building systems with causal reasoning improves decision-making, supports robust generalization under distribution shifts, and enables more trustworthy explanations for model behavior.

This repository is a starting point for documenting and implementing causal AI techniques, experiments, and resources.

## Quick start (PyWhy/DoWhy)

The example below uses the PyWhy ecosystem (DoWhy) to estimate a causal effect with a simple backdoor adjustment. Install dependencies with:

```bash
pip install dowhy pandas
```

Run the example:

```bash
python examples/pywhy_basic.py
```

Key snippet (see the full script in `examples/pywhy_basic.py`):

```python
from dowhy import CausalModel
import pandas as pd

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
```
