# Version 1.0 — Limitations and Future Directions

The central weakness of Version 1.0 is **the amount and structure of data**. The project has sophisticated orchestration and validation relative to the amount of independent statistical information available to it.

## Limitations

### 1. Small effective time-series sample

The development table has 717 housing rows, but this is only 239 monthly observations for each of three co-moving property categories.

The three categories share the same dates and market environment, so 717 stacked rows are not equivalent to 717 independent observations. Flexible ML, hyperparameter search, regime analysis, and repeated model comparison all reuse the same limited history.

### 2. Aggregate benchmarks hide property-level heterogeneity

Version 1 models MLS HPI **benchmark prices**, not raw monthly transaction averages. That is useful for market-level analysis because it reduces composition effects, but it cannot directly learn how individual sale prices vary with size, age, bedrooms, exact location, lot/building attributes, or quality.

### 3. Narrow geography/category coverage

The validated final scope contains only GVR board apartment, townhouse, and `single_family_mixed`. There is no exact City of Vancouver, Vancouver East/West, administrative Metro Vancouver, or exact detached-only inference.

### 4. Revised history, not real-time vintages

Historical values come from a later revised snapshot. Reference-date leakage is controlled, but a historical backtest uses the current revised view of the past rather than necessarily the values analysts actually saw at that time.

### 5. Only one untouched holdout year

2025 is a genuine untouched future test, but it is still only one market path with 12 serially dependent months per category. The AR failure is strong evidence about **this holdout**, not proof that AR is always inferior to naive forecasting.

### 6. Model-selection uncertainty

Historical AR improvements of roughly 25% for apartment/townhouse reversed strongly in 2025. This demonstrates that model rankings can be unstable across market conditions and that a small validation history can reward relationships that do not persist.

### 7. Limited external explanatory information

Mortgage rates, listings, inventory, sales, supply, employment/income, population, and other demand/supply measures are absent from the final predictive models. Only historical policy rates were fully validated as an external candidate.

### 8. No fully probabilistic forecasting

The project evaluates point forecasts. It does not produce calibrated probability distributions or validated prediction intervals.

### 9. Descriptive, specification-sensitive regimes

The two-state K-means regimes are descriptive summaries rather than proven latent economic states. Apartment assignments are materially sensitive to feature specification and sample endpoint.

### 10. No causal identification

Forecast coefficients, policy associations, and regime membership are predictive/descriptive. They do not identify causal effects.

### 11. Bounded agent autonomy

The project implements specialized roles, shared state, routing, restricted tools, Critic review, and escalation, but many analytical choices are predeclared through stage contracts, registries, validation origins, and thresholds. That makes the system a tightly orchestrated agentic workflow rather than a fully autonomous multi-agent scientist.

This trade-off was intentional: hard restrictions protected against leakage and irreproducible search, but some restrictions also reduced the agents' freedom to formulate new analytical paths.

### 12. Public reproducibility is licensing-constrained

The private package preserves source material and generated outputs. Some housing material is not treated as openly redistributable, so the public GitHub release intentionally excludes those bytes.

## Future directions

The highest-value improvement is **more informative data, not a more complicated model on the same small sample**.

### Priority 1 — expand cross-sectional housing data

Build a source-consistent panel:

`month × geography × property type`

A target of roughly 15–30 local areas across multiple property types would make panel/hierarchical forecasting much more meaningful while preserving the Version 1 market-level question.

### Priority 2 — add transaction-level modelling as a separate layer

If a legally usable transaction-level dataset becomes available, a later version could model:

`transaction price ~ size + age + bedrooms + property type + location + time + ...`

Thousands of transactions would greatly improve cross-sectional learning and allow hedonic/ML property valuation. They would **not**, however, create thousands of independent observations of the market's macro time evolution; the number of calendar periods would still be limited.

### Priority 3 — real-time/vintage-aware data

Track `reference_month`, `release_date`, `vintage_date`, and `available_at` so historical backtests reconstruct what was actually knowable at each origin.

### Priority 4 — economically justified predictors

Add mortgage rates, sales, inventory, listings, starts/completions, permits, employment/income, and demographic variables only when publication timing and historical definitions are defensible.

### Priority 5 — hierarchical/panel and ensemble models

Use broader data to compare common market factors with local effects, and evaluate ensembles instead of forcing a single historical winner. Short-, medium-, and long-horizon forecasts should not be assumed to share one optimal model.

### Priority 6 — probabilistic forecasts

Once the dataset is richer, evaluate approaches such as quantile forecasting and time-aware conformal prediction. Report empirical coverage/calibration, not only point error.

### Priority 7 — more analytical agent discretion

Keep hard guardrails fixed:

- no holdout leakage;
- chronological validation;
- source integrity;
- deterministic/reproducible tool execution;
- bounded computation/retries;
- Critic review;
- approval for major capability changes.

Give agents more discretion over:

- which registered models merit testing;
- which diagnostics to run;
- which feature hypotheses to propose;
- whether the current registry appears inadequate;
- whether a new method should be proposed for approval.

### Priority 8 — preserve future observations

Keep Version 1 and future Version 2 forecasts frozen and evaluate them prospectively as new observations arrive instead of repeatedly retuning and calling the same period an untouched test.

## Proposed Version 2 research question

> **How much incremental forecast accuracy can richer local-market, property-level and economic information provide beyond a simple persistence forecast of Greater Vancouver housing prices, and how stable is that improvement across horizons and market conditions?**

The guiding lesson from Version 1 is: **complexity alone did not reliably beat persistence. Version 2 should first add useful information, then add modelling complexity.**
