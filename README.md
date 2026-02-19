# Causal AI Production Pipeline Template

This repository provides a practical, end-to-end production pipeline that combines:

- **Technical, code-first causal methods** (in the spirit of Aleksander Molak and *Causal Inference and Discovery in Python*).
- **Business, governance, and ROI framing** (in the spirit of Judith S. Hurwitz and *Causal Artificial Intelligence*).

Use this template across marketing, product, healthcare, and operations settings.

## Pipeline Overview

1. **Business framing & decision design**
2. **Causal problem specification & assumptions**
3. **Data inventory & engineering**
4. **Causal discovery + expert constraints**
5. **Modeling & estimation**
6. **Validation & refutation**
7. **Policy learning & decisioning**
8. **Deployment, monitoring & governance**
9. **Post-deployment learning loop**

---

## 1) Business Framing & Decision Design

Turn a vague problem into a decision-ready objective.

- Define the decision rule (what action follows a positive prediction).
- Select a primary KPI (incremental revenue, readmission reduction, conversion lift, etc.).
- Quantify constraints: budget, compliance, fairness, and operational limits.
- Set unit of decisioning (user, cohort, geo, time window).
- Decide validation path (A/B test or phased rollout).

**Example decision artifact:**

> Target users with predicted uplift > 3% for campaign X; expected net value = uplift × average transaction value − action cost.

---

## 2) Causal Problem Specification & Assumptions

Define the estimand and encode assumptions in a DAG/SCM.

- Create an initial graph with domain experts.
- Specify estimand: ATE, ATT, or CATE.
- Explicitly record assumptions (e.g., no unobserved confounding, positivity, SUTVA).
- Identify valid controls and forbidden controls (colliders/descendants).

**Example estimand:**

`P(Y | do(T=1)) - P(Y | do(T=0))`

---

## 3) Data Inventory & Engineering

Build a reliable, compliant data foundation.

- Catalog tables, keys, time columns, treatment/outcome mappings.
- Track data lineage, freshness, and delay windows.
- Enforce privacy and governance standards.
- Create feature definitions aligned with causal assumptions.

Outputs include production schema, ETL contracts, and train/validation/holdout splits.

---

## 4) Causal Discovery + Expert Knowledge

When the graph is uncertain, use discovery as **hypothesis generation**, not truth.

- Run methods like PC, GES, or LiNGAM.
- Add expert edge constraints (required/forbidden links).
- Re-run and compare candidate structures.
- Validate with robustness checks before operational use.

---

## 5) Modeling & Estimation

Practical stack:

- **Identification:** DoWhy
- **Estimation:** EconML (DML, doubly robust, meta-learners), causal forests
- **Heterogeneity:** CATE modeling for policy targeting

### Minimal DoWhy + EconML example

```python
import pandas as pd
from dowhy import CausalModel
from econml.metalearners import XLearner
from sklearn.ensemble import RandomForestRegressor


df = pd.read_csv("data.csv")

graph = "digraph { BrowsingScore -> AdExposure; BrowsingScore -> Purchase; AdExposure -> Purchase }"

model = CausalModel(
    data=df,
    treatment="AdExposure",
    outcome="Purchase",
    graph=graph,
)

estimand = model.identify_effect()

X = df[[c for c in df.columns if c.startswith("cov_")]]
T = df["AdExposure"].values
Y = df["Purchase"].values

xl = XLearner(
    models=RandomForestRegressor(),
    propensity_model=RandomForestRegressor(),
)
xl.fit(Y, T, X=X)
cate = xl.effect(X)
```

---

## 6) Validation & Refutation

Build confidence through stress tests and sensitivity checks.

- Placebo/permutation treatment checks.
- Random common cause stability checks.
- Negative controls.
- Sensitivity analysis for hidden confounding.
- Cross-estimator agreement (IPW, DML, causal forest, etc.).

```python
refute = model.refute_estimate(estimand, estimate, method_name="placebo_treatment")
print(refute)
```

Deliver to stakeholders: effect size with CI, sensitivity summary, and expected ROI.

---

## 7) Policy Learning & Decisioning

Translate CATE into operational policy.

- Threshold policy: action if `cate(x) > threshold`.
- Constrained optimization: maximize value under budget/fairness constraints.
- Direct policy learning where appropriate.

```python
df["cate"] = cate
threshold = 0.03
targets = df[df["cate"] > threshold]["user_id"].tolist()
```

---

## 8) Deployment, Monitoring & Governance

Operationalize safely and transparently.

- CI/CD for data + model artifacts.
- Monitoring:
  - business outcomes (incremental lift, profitability)
  - model drift (covariates, treatment propensity, CATE shifts)
  - online holdouts for causal validity
- Governance:
  - documented DAG and assumptions
  - privacy controls and audit logs
  - fairness impact monitoring
- Scheduled retraining and periodic validation experiments.

---

## 9) Post-Deployment Learning Loop

- Maintain continuous holdout evaluation.
- Run targeted RCTs in uncertain/high-value cohorts.
- Fuse observational and experimental data for ongoing refinement.

---

## One-Page Mini Project Example

**Problem:** increase monthly subscriptions via targeted email.

1. Business economics: revenue per subscription ₹500, email cost ₹5, break-even uplift ≈ 1.0%.
2. Causal setup: `Treatment=email_send`, `Outcome=purchase_30d`, confounders include recency and behavior.
3. DAG review with analytics + product.
4. Estimation with DML + causal forest.
5. Validation via refuters + randomized holdout.
6. Policy: target users with uplift > 1.5% until budget cap.
7. Deploy daily batch and monitor weekly net uplift.
8. Recalibrate monthly with small RCT.

---

## Go/No-Go Checklist

- [ ] Decision and KPI owner approved
- [ ] DAG and assumptions documented
- [ ] Data contract and quality checks in place
- [ ] Estimand identified and at least two estimators selected
- [ ] Refutation and sensitivity plan defined
- [ ] Validation experiment budget allocated
- [ ] Monitoring and rollback playbook completed

## Communication Artifacts

- Executive decision brief: action, ROI, risk
- Technical appendix: DAG, estimand, estimators, refutation output
- Operations playbook: targeting rules, cadence, compliance/fairness controls
