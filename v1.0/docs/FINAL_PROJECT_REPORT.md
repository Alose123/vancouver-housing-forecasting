# Housing-agent-system — Final project report

**Stages 1–8 · GVR board · revised-history study**

## 1. Executive Summary

The project delivered a controlled housing research workflow, two immutable 2025 forecast experiments, an untouched holdout evaluation, and historical market-regime discovery.

The original nine-series design was not feasible with the validated available data. The final approved analytical scope contains three Greater Vancouver REALTORS (GVR) board-level series:

- `apartment`
- `townhouse`
- `single_family_mixed`

The main development panel contains **717 rows = 239 months × 3 categories**, January 2005–November 2024. These are not 717 independent market observations: there are only 239 monthly dates per category, and the categories co-move.

Historical validation initially favored autoregressive models for apartments and townhouses, but those models **failed to generalize to the untouched 2025 holdout**. The simple naive baseline was materially more accurate in 2025.

A separate historical regime analysis compared 90 clustering configurations. The primary results were descriptive two-state K-means partitions characterized as **Lower-growth adjustment** and **Higher-growth expansion**. Separation was modest and apartment regime boundaries were materially specification-sensitive.

The main research lesson is therefore not that one complex model reliably predicts Vancouver housing. It is that disciplined validation, strong baselines, leakage controls, and honest preservation of negative results are essential when working with a small dependent time-series sample.

## 2. Research Objectives

Version 1 asks three main questions:

1. Can bounded statistical and machine-learning models improve on transparent housing-price baselines?
2. Do historical validation gains survive a genuinely untouched future period?
3. Can reproducible descriptive clustering summarize recurring housing-market conditions without imposing predefined boom/crisis labels?

Forecasting and regime analysis are treated separately. The project does not make causal claims about housing prices.

## 3. Agentic System Architecture

Seven specialized roles organize the workflow:

- Data Source
- Data Auditor
- Feature
- Forecast
- Regime
- Critic
- Report

Python dataclasses persist shared state independently of conversational memory. An orchestrator controls explicit transitions through role-restricted tools and registries. Deterministic tools perform data transformations, model fitting, metrics, hashes, manifests, and validation checks.

The Critic independently checks numerical and methodological contracts, requests bounded revisions when a correctable issue is found, and escalates material unresolved choices for review.

This is an **authored, bounded agentic workflow with deterministic execution and Critic checks**. It is not presented as a live autonomous multi-LLM research system.

## 4. Original Research Design

The original aim was a much broader monthly housing panel covering Vancouver / Greater Vancouver and multiple property categories.

The later nine-series specification targeted:

- GVR board
- Vancouver East
- Vancouver West

across:

- detached
- townhouse
- apartment

with monthly history beginning in 2005.

That panel could not be validated under the accepted data-access and source-consistency rules.

## 5. Data Acquisition and Scope Revision

The system identified historical-vintage problems and rejected unsafe stitching of incompatible releases.

A strict pre-cutoff historical series could not be established from the available public material without relying on source combinations that were not methodologically defensible. Publisher contact was considered. It was declined. The study therefore moved to an explicitly **retrospective revised-history design**.

Further acquisition was later terminated after legitimate public routes had been explored and an access-control boundary had been encountered. The blocked backend route was not retried or bypassed.

A repository-only feasibility review then supported a reduced board-level scope. That reduced scope was approved. This changed the research question; it did not create missing observations.

The retained housing source is a later revised CREA MLS HPI Greater Vancouver board snapshot. Version 1 therefore controls reference-time leakage but does **not** reconstruct the exact vintage an analyst would have seen at every historical forecast date.

## 6. Final Dataset

### Housing development panel

The forecasting-development panel contains:

- January 2005–November 2024
- 239 months per category
- 3 categories
- 717 rows total

Categories:

- apartment
- townhouse
- `single_family_mixed`

`single_family_mixed` retains the source-defined mixed single-family concept and is **not** relabelled detached.

### 2025 holdout

The protected evaluation file contains:

- January–December 2025
- 12 observations per category
- 36 rows total

These outcomes remained inaccessible through model development and selection and were opened only after the Stage 5 and Stage 6 forecasts had been frozen.

### External data

The Bank of Canada policy-rate series was the only validated external candidate. It contains 300 monthly settings from January 2000–December 2024.

It is treated as a policy-rate series, not a mortgage rate, monthly average, or Bank Rate substitute.

## 7. Stage 3 — Data Quality

The approved 717-row development panel had:

- 0 missing months
- 0 invalid rows
- 0 duplicate series-month keys
- 0 conflicting duplicate groups
- 0 source price/HPI values modified

Sixty-nine statistical anomaly flags were investigated and retained because no source error was confirmed. Statistical extremeness was not treated as sufficient reason for deletion, clipping, smoothing, or imputation.

The audit preserved source timing/vintage metadata and explicitly documented that later historical revisions can affect earlier benchmark values.

## 8. Stage 4 — Feature and Experiment Design

Stage 4 defined the experiment before modelling.

The feature inventory contained 24 candidate variables grouped into:

- History
- Trend
- State
- Policy
- Cross-category

Housing and peer features used only historical prefixes available before their future targets. Policy features used as-of timing based on recorded knowledge dates rather than naive calendar-month joins.

The validation design used expanding chronological windows rather than random train/test splits.

Learned preprocessing—such as scaling or other fitted transformations—was required to be fit inside training folds only.

A separate regime feature design excluded raw price/HPI levels to reduce the risk that clustering merely separated early low-price years from later high-price years.

## 9. Stage 5 — Baseline Forecast Experiment

The first executable registry contained only:

- naive
- seasonal naive

Both were evaluated honestly; unimplemented learned models were not represented as tested.

The naive model won for every category.

Historical annual-origin MAE:

| Category | Naive MAE | Seasonal-naive MAE |
|---|---:|---:|
| Apartment | $43,993 | $60,798 |
| Townhouse | $65,268 | $92,921 |
| Mixed single-family | $123,578 | $175,470 |

The Stage 5 forecast was frozen before any 2025 outcome access.

## 10. Stage 6 — Enhanced Forecast Experiment

A separate controlled registry added:

- ordinary linear regression
- Ridge regression
- recursive autoregression on log returns
- Random Forest
- gradient boosting

SARIMA was not implemented because no approved installed implementation was available; the project did not silently substitute another method and call it SARIMA.

Historical validation suggested:

- AR(1) for apartments
- AR(3) for townhouses
- naive for mixed single-family

Historical MAE fell to approximately:

- **$32,655** for apartments
- **$48,675** for townhouses

which was about 25–26% lower than naive for those two categories.

The mixed category retained naive because the numerically best learned alternative did not satisfy the predeclared stability rules.

The Stage 6 enhanced 2025 forecasts were then frozen independently of Stage 5.

## 11. Stage 7 — Untouched 2025 Holdout

Both frozen forecast artifacts and their hashes were verified before actual 2025 outcomes were opened.

Final 2025 results:

| Category | Experiment | MAE | RMSE | Bias: forecast − actual |
|---|---|---:|---:|---:|
| Apartment | Naive baseline | $18,067 | $22,845 | +$12,417 |
| Townhouse | Naive baseline | $27,325 | $33,311 | +$27,325 |
| Mixed single-family | Naive baseline | $39,908 | $50,751 | +$25,658 |
| Apartment | Enhanced AR | $31,302 | $41,473 | +$27,990 |
| Townhouse | Enhanced AR | $89,155 | $98,681 | +$89,155 |
| Mixed single-family | Enhanced | $39,908 | $50,751 | +$25,658 |

The historical model ranking did **not** generalize.

Relative to naive:

- apartment enhanced MAE deteriorated by about **73%**
- townhouse enhanced MAE deteriorated by about **226%**
- mixed single-family was identical because both experiments used naive

The enhanced AR paths rose while the observed endpoints fell, producing substantial overprediction.

This does not prove that AR models are universally inferior. It shows that their historical advantage was not robust to the particular untouched 2025 market path.

## 12. Stage 8 — Historical Regime Discovery

Stage 8 used pre-2025 information only.

After feature warmup, each category had 227 usable months from January 2006–November 2024.

Primary features:

- YoY price growth
- 3-month momentum
- 6-month log-return volatility
- historical drawdown
- 3-month acceleration

Candidate methods:

- K-means
- diagonal-covariance Gaussian mixture models
- Ward hierarchical clustering

Each was evaluated across K=2–6 for primary and extended feature sets, producing **90 candidate configurations**.

The primary selected solution was **K-means with K=2** for each category.

Numerical profiles were frozen before descriptive labels were assigned.

The two descriptive labels were:

- **Lower-growth adjustment**
- **Higher-growth expansion**

Median YoY growth by category:

| Category | Lower-growth adjustment | Higher-growth expansion |
|---|---:|---:|
| Apartment | -0.67% | 10.82% |
| Townhouse | 1.25% | 12.99% |
| Mixed single-family | -1.16% | 14.16% |

These are relative descriptive states, not recession/boom ground truth.

Silhouette values were modest, approximately 0.27–0.30. Stability was generally good under repeated fits and block perturbations, but apartment assignments were materially sensitive to the expanded feature specification and earlier sample endpoints.

No regime-aware forecasting model was fitted.

## 13. Key Findings

### Empirical findings

- The validated Version 1 housing panel is complete for three board-level categories but small in effective time-series size.
- Naive forecasting beat seasonal naive historically.
- Historical AR improvements for apartment and townhouse did not survive the untouched 2025 holdout.
- Tree-based models could fit training data more aggressively without delivering clearly superior historical generalization.
- Historical housing dynamics can be summarized by persistent higher-growth and lower-growth clusters, but the boundaries are not perfectly stable.

### Methodological finding

The strongest lesson is:

> **Historical model superiority must survive genuinely unused future data.**

Cross-validation is evidence, not proof of future superiority.

## 14. What Failed and Why

Several negative results are intentionally preserved.

The original nine-series geographic/category scope was infeasible under the accepted public-access and consistency requirements.

A strict historical vintage was not established. Publisher contact was considered; it was declined, and unsafe stitching was rejected.

Historically selected AR models failed badly relative to naive in the untouched 2025 year.

More flexible tree models did not automatically translate lower training error into better generalization.

Regime solutions, particularly apartments, were sensitive to feature specification.

These failures are part of the research result rather than defects to conceal.

## 15. Agentic-AI Contribution

The project demonstrates an orchestration framework rather than unconstrained autonomous research.

Deterministic software handled:

- validation keys
- timing rules
- transformations
- model fitting
- metrics
- hashes
- state persistence
- access guards

Agent-style roles organized bounded analytical decisions and interpretation.

Critic logic independently reconstructed numerical results and enforced fixed methodological rules.

Material scope/capability decisions were handled through explicit review rather than silently changed by the workflow.

The resulting system is best described as a **tightly orchestrated agentic research workflow with deterministic tools and human-in-the-loop governance**.

## 16. Limitations

The largest limitation is **the amount and structure of data**.

The 717 development rows correspond to only 239 monthly dates for each of three co-moving categories. This is a small effective sample for flexible ML, repeated hyperparameter search, regime analysis, and robust model-ranking conclusions.

Other major limitations are:

- only one untouched holdout year;
- later-revised history rather than real-time vintage data;
- narrow board-level geography;
- no exact detached-only series;
- aggregate benchmark data rather than transaction-level property observations;
- limited external economic/supply-demand predictors;
- no calibrated probabilistic forecasts;
- descriptive rather than causal regime interpretation;
- model-selection uncertainty;
- bounded agent autonomy;
- public reproducibility constrained by third-party redistribution rights.

See [Limitations and Future Directions](LIMITATIONS_AND_FUTURE_DIRECTIONS.md) for the expanded discussion.

## 17. Future Directions

The highest-value Version 2 improvement is **more informative data before more sophisticated modelling**.

Priorities are:

1. expand to a broader `month × geography × property type` panel;
2. add transaction-level / hedonic modelling if a legally usable dataset becomes available;
3. reconstruct real-time/vintage-aware historical inputs;
4. add economically justified variables such as mortgage rates, sales, inventory, listings, supply, income/employment, and population;
5. evaluate hierarchical/panel and ensemble models;
6. introduce probabilistic forecasts with calibration tests;
7. give analytical agents more discretion while preserving hard leakage and governance constraints;
8. preserve future periods as genuine prospective evaluations.

The proposed Version 2 question is:

> **How much incremental forecast accuracy can richer local-market, property-level and economic information provide beyond a simple persistence forecast of Greater Vancouver housing prices, and how stable is that improvement across horizons and market conditions?**

## 18. Reproducibility

The private project preserves source registry information, stage states, logs, tests, frozen forecasts, manifests, and numerical checks.

The public repository intentionally excludes third-party source bytes that are not treated as openly redistributable.

Stage test counts progressed through:

- Stage 1: 36
- Stage 2: 72
- Stage 3: 96
- Stage 4: 128
- Stage 5: 156
- Stage 6: 184
- Stage 7: 220
- Stage 8: **252**

These tests validate implementation and methodological controls; they do not certify forecasting accuracy.

## 19. Completion

**252/252 tests passed through Stage 8.**

Version 1.0 ends with the untouched 2025 holdout evaluation and historical regime discovery. No prospective price prediction is included in the public Version 1 project.
