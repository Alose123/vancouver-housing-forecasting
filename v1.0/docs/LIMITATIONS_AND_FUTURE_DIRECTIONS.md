# Version 1.0 — Limitations and Future Directions

The central weakness of Version 1.0 is **the amount and structure of data**. The project has sophisticated orchestration and validation relative to the amount of independent statistical information available to it.

## Limitations

### 1. Small effective time-series sample

The original development table has 717 housing rows, but this is only 239 monthly observations for each of three co-moving property categories. The final post-holdout panel has 252 monthly observations per category through December 2025.

The three categories share the same dates and market environment, so 717 or 756 stacked rows are not equivalent to that many independent observations. Flexible ML, hyperparameter search, regime analysis and five-year forecasting all reuse the same limited history.

The Stage 9 five-year experiment is especially constrained: only seven annual five-year origins exist per category/model, and those windows overlap.

### 2. Aggregate benchmarks hide property-level heterogeneity

Version 1 models MLS HPI **benchmark prices**, not raw monthly transaction averages. That is useful for market-level analysis because it reduces composition effects, but it cannot directly learn how individual sale prices vary with size, age, bedrooms, exact location, lot/building attributes or quality.

### 3. Narrow geography/category coverage

The validated final scope contains only GVR board apartment, townhouse and `single_family_mixed`. There is no exact City of Vancouver, Vancouver East/West, administrative Metro Vancouver or exact detached-only inference.

### 4. Revised history, not real-time vintages

Historical values come from a later revised snapshot. Reference-date leakage is controlled, but a 2018 backtest uses the current revised view of 2018 rather than necessarily the values analysts actually saw in 2018.

### 5. Only one untouched holdout year

2025 is a genuine untouched future test, but it is still only one market path with 12 serially dependent months per category. The AR failure is strong evidence about 2025, not proof that AR is always inferior to naive forecasting.

### 6. Model-selection uncertainty

Historical AR improvements of roughly 25% for apartment/townhouse reversed strongly in 2025. This demonstrates that model rankings can be unstable across market conditions and that a small validation history can reward relationships that do not persist.

### 7. Long-horizon evidence is weak

The 2030 experiment uses seven overlapping five-year historical origins. Central projections and empirical ranges are therefore useful research outputs, not precise expected values or calibrated guarantees.

### 8. Limited external explanatory information

Mortgage rates, listings, inventory, sales, supply, employment/income, population and other demand/supply measures are absent from the final predictive models. Only historical policy rates were fully validated as an external candidate.

### 9. No fully probabilistic forecasting

The project reports point forecasts and historical-error-based ranges. Those ranges are not validated probability intervals.

### 10. Descriptive, specification-sensitive regimes

The two-state K-means regimes are descriptive summaries rather than proven latent economic states. Apartment assignments are materially sensitive to feature specification and sample endpoint.

### 11. No causal identification

Forecast coefficients, policy associations and regime membership are predictive/descriptive. They do not identify causal effects.

### 12. Bounded agent autonomy

The project implements specialized roles, shared state, routing, restricted tools, Critic review and human escalation, but many analytical choices are predeclared through stage contracts, registries, validation origins and thresholds. That makes the system a tightly orchestrated agentic workflow rather than a fully autonomous multi-agent scientist.

### 13. Public reproducibility is licensing-constrained

The private package preserves source material and generated outputs. Some housing material is not treated as openly redistributable, so the public GitHub release intentionally excludes those bytes.

## Future directions

### Priority 1 — expand cross-sectional housing data

Build a source-consistent panel:

`month × geography × property type`

A target of roughly 15–30 local areas across multiple property types would make panel/hierarchical forecasting much more meaningful while preserving the Version 1 market-level question.

### Priority 2 — real-time/vintage-aware data

Track `reference_month`, `release_date`, `vintage_date` and `available_at` so historical backtests reconstruct what was actually knowable at each origin.

### Priority 3 — economically justified predictors

Add mortgage rates, sales, inventory, listings, starts/completions, permits, employment/income and demographic variables only when publication timing and historical definitions are defensible.

### Priority 4 — hierarchical/panel and ensemble models

Use broader data to compare common market factors with local effects, and evaluate ensembles instead of forcing a single historical winner.

### Priority 5 — probabilistic forecasts

Add quantile or time-aware conformal forecasts with explicit historical coverage/calibration diagnostics.

### Priority 6 — transaction-level/hedonic modelling

If a legally usable transaction dataset becomes available, add a separate property-level valuation layer. Thousands of transactions would greatly improve cross-sectional learning, but would not by themselves create thousands of independent macro time observations.

### Priority 7 — more analytical agent discretion

Keep hard guardrails such as leakage prevention and chronological validation, but let agents decide more of the scientific search path: diagnostics, candidate models, feature hypotheses and proposals for new methods.

### Priority 8 — preserve future observations

Keep Version 1/Version 2 predictions frozen and evaluate them prospectively as new years arrive.

## Proposed Version 2 research question

> **How much incremental forecast accuracy can richer local-market, property-level and economic information provide beyond a simple persistence forecast of Greater Vancouver housing prices, and how stable is that improvement across horizons and market conditions?**

The guiding lesson from Version 1 is: **complexity alone did not reliably beat persistence. Version 2 should first add useful information, then add modelling complexity.**
