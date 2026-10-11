# Housing-agent-system — Final project report

**Stages 1–9 · GVR board · revised-history study · post-holdout prospective analysis**

## 1. Executive Summary

The project delivered a controlled housing research workflow, two immutable 2025 forecast experiments, an honest holdout evaluation, historical regime discovery, and a separate 2030 forecasting exercise. The original nine-series design was not feasible with the validated available data. Human review approved three GVR-board series: apartment, townhouse, and `single_family_mixed`. Acquisition remains closed.

Historical AR improvements failed to generalize to the untouched 2025 holdout. Stage 9 therefore used a new five-year design, not the earlier winner by default. Its central December 2030 estimates and indicative ranges are below. These are forecasts of source-defined nominal CAD benchmarks, not property sale prices, valuations of a specific dwelling, or calibrated conditional expectations.

| Category            | Dec 2025 observed | Selected model  | Dec 2030 central | Increase CAD | Increase % | Annualized % | Historical-error lower | Historical-error upper |
| ------------------- | ----------------- | --------------- | ---------------- | ------------ | ---------- | ------------ | ---------------------- | ---------------------- |
| apartment           | $710,000          | ar3             | $912,000         | $202,000     | 28.4%      | 5.13%        | $745,000               | $1,083,000             |
| townhouse           | $1,056,600        | geometric_drift | $1,445,000       | $388,000     | 36.7%      | 6.46%        | $1,296,000             | $1,655,000             |
| single_family_mixed | $1,887,800        | ridge_trend     | $2,430,000       | $542,000     | 28.7%      | 5.18%        | $2,280,000             | $2,580,000             |

Headline forecasts and bounds are rounded to the nearest $1,000; machine-readable files retain full precision. Increases and rates use unrounded forecasts. Ranges summarize historical errors of selected models, not guaranteed coverage. The analytical origin is December 2025, but the calculation uses a revised snapshot available in **October 2026**. It is not an as-issued December 2025 forecast or a forecast incorporating current 2026 observations.

## 2. Research Objectives

The research asks whether bounded model comparisons can improve over transparent baselines, whether historical gains survive an untouched holdout, and whether reproducible descriptive clusters summarize housing-market dynamics. The final prospective question is the December 2030 benchmark for each approved category. Geography and property definitions constrain every answer. Forecasting evidence and descriptive regime evidence remain separate; there are no causal housing-market claims.

## 3. Agentic System Architecture

Seven roles organize the work: Data Source, Data Auditor, Feature, Forecast, Regime, Critic, and Report. Python dataclasses persist shared state independently of conversational memory. An orchestrator routes explicit actions through role-restricted tools and registries. Tools produce deterministic data transformations, model fits, metrics, manifests and logs. The Critic checks numerical and methodological contracts, routes bounded revisions, and escalates material unresolved choices to persistent human review.

The Stage 1 package supplied retry bounds, review persistence, logging, freeze and holdout guards. Later stages added phase-specific adapters without rebuilding that foundation. Stage 9 extends the existing typed state with a separate `ProspectiveState`; it leaves all 640 pre-existing files unchanged. Its fixed input loader permits compatible 2025 use only through the newly authorized Stage 9 roles. Earlier Forecast/Regime tools retain their original outcome restrictions.

This is authored orchestration executed with deterministic software and Critic checks, **not a live multi-LLM** experiment. The system can express specialized roles and constrained actions without claiming independent language models conducted each stage. Integrity hashes and Python guards are application controls, not an operating-system security sandbox. Stage 9 blocks network connections in its workflow and never invokes acquisition tools.

## 4. Original Research Design

The original aim was monthly history beginning around 2000 for Vancouver and Metro Vancouver across detached, townhouse and apartment properties. The subsequent nine-series specification used GVR board, Vancouver East and Vancouver West, beginning in 2005. The board is not administrative Metro Vancouver; East and West would have been submarkets, not an exact City aggregate. Neither the original geographic panel nor its local detached concept is inferred from the reduced dataset.

## 5. Data Acquisition and Scope Revision

The system identified historical-vintage problems and rejected unsafe stitching of incompatible releases. It escalated the issue; the human approved current/revised history and prohibited publisher contact. Legitimate public routes were investigated and exact historical chart tooltips were identified, but a complete numerical nine-series panel was not acquired and validated. An access-control boundary was encountered and the blocked backend route was stopped, without bypass or workaround. Holdout isolation was retained through the original model development.

The human then terminated further acquisition: `data_acquisition_status = closed_by_human_decision`, `complete_nine_series_history = not_obtained`, and `original_scope_feasible = false`. The original Stage 2 nine-series exit condition did not pass. A repository-only feasibility review supported a reduced board-level scope, which the human approved. Approval changed the research scope; it did not create missing observations. This record demonstrates critic escalation and human governance as substantive project outcomes.

The retained source is CREA MLS HPI Greater Vancouver board, non-seasonally-adjusted benchmark prices from the already-downloaded September 2026 snapshot, with recorded vintage/access date October 7, 2026. Source evidence and licensing notes remain in `data/source_registry.json` and the preserved Stage 2 reports. No new source was sought in Stage 9. Benchmark prices describe source-defined representative homes; arithmetic sale means and medians vary with transaction mix, while HPI is an index. Those measures were not substituted for one another.

## 6. Final Dataset

The original development panel contains 239 months per category, January 2005–November 2024: 717 rows. November was the last eligible housing reference month for the simulated December 31, 2024 decision. The separate compatible 2025 evaluation file contains 36 rows, January–December 2025. Policy rate is the only validated external dataset: 300 monthly month-end target overnight rates, January 2000–December 2024. It is neither a mortgage rate nor Bank Rate and was not extended.

The new Stage 9 panel contains 252 months per category, January 2005–December 2025: 756 rows. It combines the unchanged 717 development rows, exactly three December 2024 CREA rows already present in quarantine, and the 36 same-snapshot evaluation rows. All 717 overlapping CREA rows in quarantine were compared field-for-field. Source ID, vintage, geography, category, currency, benchmark measure and seasonal adjustment match. Other quarantine rows, including local detached observations, are excluded. No interpolation, averaging, relabelling, vintage stitching or source-value change is used.

`single_family_mixed` retains the source's mixed single-family definition and is not relabelled detached. Category labels are continuous, but benchmark attributes and represented composition need not be invariant. Existing documentation records the 2022 methodology change to rolling five-year benchmark attributes and annual historical recalculation. Revision hindsight remains in the entire analysis; chronological reference-month controls cannot remove it.

## 7. Stage 3 Data Quality

The approved 717-row development panel had no missing months, invalid rows or duplicate series-month keys. Cleaning changed zero values. All 69 statistical anomaly flags were retained because no source error was confirmed. Statistical extremes can be economically real or affected by revision; they are not automatic deletion instructions. Ten preserved apartment/townhouse vintage comparisons established revision risk, but did not support reconstructing a full original-vintage panel or quantifying regime-boundary changes.

## 8. Stage 4 Feature and Experiment Design

The inventory contained 24 candidate features arranged into History, Trend, State, Policy and Cross-category families. Housing and peer features use only the reference-month prefix. Policy joins use recorded knowledge dates; later policy observations cannot enter earlier decisions. Structural warmup remains blank, never imputed. Learned preprocessing, target corrections and tuning must be fold-local.

Historical forecast validation used expanding windows with at least 120 raw months and 90 eligible supervised examples. The original decision used November 2024 housing, an internally predicted December bridge, and January–December 2025 horizons 2–13. Eight annual and 36 quarterly origins were fixed. A separate regime feature design excluded raw price/HPI levels: five primary features, optionally eight extended features. The three categories share time and are not independent stacked samples.

## 9. Stage 5 Baseline Experiment

Only naive and seasonal naive were executable in the original registry. Both were compared honestly; unimplemented learned models were not represented as fitted. Naive won for every category. Annual-origin MAEs were $43,993 for apartments, $65,268 for townhouses and $123,578 for mixed single-family, versus seasonal-naive $60,798, $92,921 and $175,470. The first immutable forecast freeze contains 36 2025 benchmark predictions. Freezing did not authorize outcome access.

## 10. Stage 6 Enhanced Experiment

A separate registry added linear regression, Ridge, recursive AR log returns, Random Forest and gradient boosting using installed implementations. SARIMA was unavailable because no approved installed implementation had been established; no substitute was silently named SARIMA. Twelve bounded candidate configurations used chronological outer validation and training-only inner tuning. Early folds used predeclared defaults where inner histories were insufficient.

AR reduced annual historical MAE to $32,655 for apartments and $48,675 for townhouses, about 26% below naive. Final fitted orders were AR(1) and AR(3), respectively. The mixed category retained naive: its numerically best learned candidate did not satisfy the stability rules. Smaller tree-model training errors did not establish better forecast generalization. A second immutable 36-row forecast freeze preserved these selections separately from Stage 5.

## 11. Stage 7 Untouched 2025 Holdout

Both forecast freezes were verified before authorized analytical evaluation. Same-snapshot source categories were chosen before decoding outcomes. The chronology remains Stage 5/6 freeze → Stage 7 evaluation → Stage 9 post-holdout model.

| Category            | Experiment | 2025 MAE | 2025 RMSE | Bias: forecast − actual |
| ------------------- | ---------- | -------- | --------- | ----------------------- |
| apartment           | Baseline   | $18,067  | $22,845   | $12,417                 |
| townhouse           | Baseline   | $27,325  | $33,311   | $27,325                 |
| single_family_mixed | Baseline   | $39,908  | $50,751   | $25,658                 |
| apartment           | Enhanced   | $31,302  | $41,473   | $27,990                 |
| townhouse           | Enhanced   | $89,155  | $98,681   | $89,155                 |
| single_family_mixed | Enhanced   | $39,908  | $50,751   | $25,658                 |

Historically superior AR models **failed to generalize** to 2025. Apartment MAE was about 73% worse than the baseline, and townhouse MAE about 226% worse. Mixed forecasts were identical across experiments. Every category/experiment's largest error occurred in December, horizon 13. AR paths rose while the observed endpoints fell. These are negative out-of-sample findings, not reasons to edit the original models retrospectively. There is one untouched target year, with dependent monthly errors, not twelve independent replications per category.

## 12. Stage 8 Regime Discovery

Stage 8 used only pre-2025 information: 227 eligible months per category, January 2006–November 2024, following feature warmup. Primary features were 12-month growth, three-month momentum, six-month log-return volatility, historical drawdown and three-month acceleration. The extension added cross-category growth dispersion and two policy features.

K-means, diagonal-covariance Gaussian mixtures and Ward hierarchical clustering were compared across K=2–6, both feature sets, and all categories: 90 configurations. There were 1,155 fitted input records. Seed, contiguous-block deletion, prefix, scaling and feature sensitivity were assessed. Numeric characterizations were frozen before descriptive names were added.

Primary solutions were K-means K=2 in every category: **Lower-growth adjustment** and **Higher-growth expansion**. Median annual growth in the two groups was −0.67% versus 10.82% for apartments, 1.25% versus 12.99% for townhouses, and −1.16% versus 14.16% for mixed single-family. Adjustment is not synonymous with contraction: the townhouse median is positive.

Median episode duration was nine months for apartments and 12.5 months for the other categories. Apartment expansion lasted 55 months from January 2014 to July 2018; townhouse expansion lasted 52 months from March 2014 to June 2018. The mixed adjustment episode lasted 40 months from August 2017 to November 2020. These are descriptive partitions, not externally identified recessions or causes.

Separation was modest: silhouette scores approximately 0.27–0.30. Block-refit agreement was generally high, but apartment specification sensitivity was material: its extended solution selected four clusters and agreement with the primary partition was only about 0.09 ARI. The earliest apartment prefix comparison was about 0.23 ARI despite much stronger later-prefix results. One apartment singleton episode was retained and a report-only correction documented it. Regimes are context in Stage 9, not predictors. No claim is made that regime awareness would have improved the original holdout forecast.

## 13. Stage 9 Prospective 2030 Forecast

### Registration and temporal design

This is **post-holdout prospective analysis**. The full 2025 housing path is now authorized for the final refit. The plan and implementation hashes were saved before any Stage 9 model fit. Annual year-end origins 2014–2020 yield endpoints December 2019–December 2025, with 120–192 monthly training observations. Final refits use 252 months through December 2025. Every fit receives only its training prefix, and all future 60-month targets are excluded from that fit. Final endpoint is December 2030.

These are reference-month origins, not assertions that a December release was already available on December 31. The calculation is a retrospective revised-vintage exercise using a December 2025 information endpoint, performed in October 2026. It does not ingest observed 2026 housing even though such dates precede execution. The original holdout is now consumed; Stage 9 selection scores are not a new untouched test.

### Candidates and selection

Seven fixed candidates were fitted: flat naive; full-history geometric drift; CAD linear trend; log-linear trend with training-only smearing retransformation; Ridge CAD trend with alpha 12 on fold-standardized time; and registered recursive log-return AR(1) and AR(3). The drift is the mean monthly log change from January 2005 to the origin, not a model selected solely because historical CAGR is positive. AR uses the preserved Stage 6 fitting capability with a separately authorized 60-month recursion.

Trees were considered and rejected before fitting: standard tree models predict from learned target regions and do not naturally extrapolate long-run time trends. A new recursive construction would introduce unsupported design choices, while direct 60-month labels would leave few independent examples. No neural networks, external packages or added economic variables were used. None of the candidates needs unknown 2026–2030 policy values.

Primary selection uses five-year endpoint MAE in CAD, separately by category. Within **5%** of the lowest eligible MAE, the predeclared simpler model wins. Non-naive candidates must beat naive in at least four origins, remain no worse under every leave-one-origin-out MAE comparison, and pass percentage-error and error-concentration limits. All historical and final fits must have finite positive paths, implied five-year annual growth within −15% to +25%, and a first-month price ratio within 0.8–1.2. AR spectral radius must be below 0.999. These are transparent design thresholds, not statistical significance or proof of economic plausibility.

| Category            | Model           | Endpoint MAE | Endpoint RMSE | Endpoint MAPE | Signed bias | Wins vs naive | Monthly path MAE |
| ------------------- | --------------- | ------------ | ------------- | ------------- | ----------- | ------------- | ---------------- |
| apartment           | ar3             | $110,115     | $127,248      | 15.98%        | $51,510     | 5/7           | $74,221          |
| townhouse           | geometric_drift | $82,923      | $98,308       | 8.92%         | $5,968      | 7/7           | $89,369          |
| single_family_mixed | ridge_trend     | $83,590      | $94,875       | 4.64%         | $8,282      | 7/7           | $154,550         |

The apartment log-linear candidate had lower endpoint MAE but failed the predeclared first-month discontinuity rule at the final origin: about +20.9%. Linear and Ridge apartment trends failed at a historical origin. Among eligible candidates, AR(3) won. Its MAE was $110,115; AR(1), at $115,743, narrowly missed the 5% band ending near $115,621. A modestly different tolerance could change that choice. We did not retune the threshold after seeing this result.

Townhouse geometric drift had the lowest endpoint MAE and was simpler than the near-tied AR(3). For mixed single-family, Ridge improved on the simpler linear trend enough to lie outside the simplicity tie. Its endpoint MAPE of about 4.64% is encouraging within these historical origins but should not be read as expected 2030 accuracy. Its monthly-path MAE was about $154,550, worse than its endpoint MAE, so endpoint success does not establish smooth-path accuracy. The unanchored trend also starts above the last observed price; it is not silently rebased or smoothed.

All candidates and failures remain visible:

| Category            | Candidate        | Endpoint MAE | Eligible | Exclusion                                                                                                     |
| ------------------- | ---------------- | ------------ | -------- | ------------------------------------------------------------------------------------------------------------- |
| apartment           | naive            | $155,086     | True     | —                                                                                                             |
| apartment           | geometric_drift  | $119,217     | True     | —                                                                                                             |
| apartment           | linear_trend     | $108,391     | False    | extrapolation_gate                                                                                            |
| apartment           | log_linear_trend | $93,903      | False    | extrapolation_gate                                                                                            |
| apartment           | ridge_trend      | $118,575     | False    | extrapolation_gate                                                                                            |
| apartment           | ar1              | $115,743     | True     | —                                                                                                             |
| apartment           | ar3              | $110,115     | True     | —                                                                                                             |
| townhouse           | naive            | $281,000     | True     | —                                                                                                             |
| townhouse           | geometric_drift  | $82,923      | True     | —                                                                                                             |
| townhouse           | linear_trend     | $199,779     | True     | —                                                                                                             |
| townhouse           | log_linear_trend | $119,553     | True     | —                                                                                                             |
| townhouse           | ridge_trend      | $221,344     | True     | —                                                                                                             |
| townhouse           | ar1              | $87,315      | True     | —                                                                                                             |
| townhouse           | ar3              | $83,287      | True     | —                                                                                                             |
| single_family_mixed | naive            | $317,971     | True     | —                                                                                                             |
| single_family_mixed | geometric_drift  | $408,502     | False    | fewer_than_four_origin_wins;leave_one_origin_out_not_stable_vs_naive;percentage_error_gate                    |
| single_family_mixed | linear_trend     | $97,476      | True     | —                                                                                                             |
| single_family_mixed | log_linear_trend | $539,167     | False    | extrapolation_gate;fewer_than_four_origin_wins;leave_one_origin_out_not_stable_vs_naive;percentage_error_gate |
| single_family_mixed | ridge_trend      | $83,590      | True     | —                                                                                                             |
| single_family_mixed | ar1              | $336,228     | False    | leave_one_origin_out_not_stable_vs_naive;percentage_error_gate                                                |
| single_family_mixed | ar3              | $364,645     | False    | fewer_than_four_origin_wins;leave_one_origin_out_not_stable_vs_naive;percentage_error_gate                    |

There were 168 fits, zero fit exceptions, 147 five-year endpoint predictions and 8,820 monthly backtest predictions. There are only **seven overlapping** five-year origins per category/model. Annual origins reduce redundancy but do not eliminate overlapping economic conditions. Categories co-move. Candidate selection and range construction use the same historical errors and can be optimistic; there is no third independent holdout. Choosing different models by category is permitted, but no per-horizon model selection was performed.

### Growth benchmarks, scenarios and uncertainty

The 20-year benchmark is exactly December 2005–December 2025; 10- and 5-year benchmarks end at the same date. These are descriptive reference rates, not automatically selected forecasts.

| Category            | 20-year CAGR | 10-year CAGR | 5-year CAGR |
| ------------------- | ------------ | ------------ | ----------- |
| apartment           | 5.41%        | 5.51%        | 2.83%       |
| townhouse           | 6.22%        | 6.67%        | 5.23%       |
| single_family_mixed | 6.02%        | 2.79%        | 3.46%       |

For each forecast horizon, the selected model's seven historical log errors, log(actual/forecast), provide empirical 10th and 90th quantiles. The forecast is multiplied by the exponentiated corrections, extending the lower/upper corrections to include zero so that the displayed band contains its central path. This is a **historical-error-based forecast range**, **not a formal 95% prediction interval** or a calibrated 80% interval. It does not quantify all parameter, revision, model-selection, shock or regime-change risk. Horizon-specific historical errors can produce irregular or narrowing bands; these are retained, not cosmetically smoothed into a claim of increasing calibrated variance.

The models provide central point estimates. Log-return compounding is not automatically an unbiased conditional mean. The log-linear candidate's smearing factor is learned within each training fold; no future residuals enter its fit. The requested “expected” benchmark is therefore interpreted as the selected central model projection, not a mathematically established expected-value estimand.

Fixed nominal-growth scenarios use the observed rolling 60-month CAGR distribution: its 10th, median and 90th percentiles, rounded to 0.5 percentage point. There are 192 overlapping windows per category. They describe historical experience, not scenario probabilities. No probability is assigned and no future policy assumption is hidden.

| Category            | Scenario       | Annual nominal rate | December 2030 scenario |
| ------------------- | -------------- | ------------------- | ---------------------- |
| apartment           | low_growth     | 2.0%                | $784,000               |
| apartment           | central_growth | 5.0%                | $906,000               |
| apartment           | high_growth    | 11.0%               | $1,196,000             |
| townhouse           | low_growth     | 3.0%                | $1,225,000             |
| townhouse           | central_growth | 7.0%                | $1,482,000             |
| townhouse           | high_growth    | 10.5%               | $1,741,000             |
| single_family_mixed | low_growth     | 2.5%                | $2,136,000             |
| single_family_mixed | central_growth | 7.0%                | $2,648,000             |
| single_family_mixed | high_growth    | 10.0%               | $3,040,000             |

Scenario ranges can extend beyond historical-error bands because they answer a different sensitivity question. Neither set is a hard bound on 2030 prices. Full candidate forecast sensitivity, including rejected candidates identified as such, is retained in `forecast_model_sensitivity.csv`.

### Monthly paths and annual endpoints

| Year end | apartment | townhouse  | single_family_mixed |
| -------- | --------- | ---------- | ------------------- |
| 2026     | $735,000  | $1,125,000 | $2,139,000          |
| 2027     | $776,000  | $1,197,000 | $2,212,000          |
| 2028     | $819,000  | $1,275,000 | $2,285,000          |
| 2029     | $864,000  | $1,357,000 | $2,357,000          |
| 2030     | $912,000  | $1,445,000 | $2,430,000          |



The dotted boundary marks December 2025. Solid lines are observations; dashed lines are projections. Shading is the historical-error-based range. Mixed single-family's first forecast month reflects the fitted trend level, not a known January 2026 observation.



## 14. Key Findings

**Empirical facts:** the compatible repository history is complete for three board-level categories; the original nine-series panel was not obtained; 2025 holdout errors are preserved; the final combined panel contains 756 unchanged observations.

**Modelling evidence:** naive beat seasonal naive; enhanced AR improved earlier validation but lost on 2025; five-year validation selected different category-specific models; primary regime solutions were two-state K-means. These conclusions are conditional on the registered samples, rules and revised data.

**Interpretation:** persistence and growth contain useful descriptive information, but validation improvements do not ensure generalization. Regime partitions summarize recurring feature patterns without demonstrating latent economic states.

**Limitations:** small dependent samples, model-selection uncertainty, changing benchmark attributes, and lack of real-time vintage reconstruction constrain precision. A 2030 point estimate alone would conceal material uncertainty.

## 15. What Failed and Why

The original geographic/category scope was infeasible under the accepted public access routes. A strict pre-cutoff historical vintage could not be established within the authorized scope; publisher contact was unwanted and unsafe stitching was rejected. These were research-design limitations, not missing-data problems to solve by interpolation.

Historical AR advantages failed on the untouched year. More complex tree models did not automatically improve forecasting. Some trend models produced unacceptable first-month jumps despite attractive endpoint scores. Regime boundaries, particularly apartments under extended features and early prefixes, were not perfectly stable. These negative results are retained because hiding them would overstate predictive and orchestration success.

## 16. Agentic-AI Contributions

Deterministic software handled validation keys, feature timing, fits, arithmetic, hashes, state persistence and guard checks. Authored agent decisions organized the search, documented source definitions, proposed bounded experiments and interpreted evidence. Critic logic independently reconstructed numerical results, enforced fixed rules and exposed report inconsistencies. Human decisions approved geographic/vintage scope changes, terminated acquisition, authorized holdout evaluation and authorized each later analytical objective.

Stage 9's Critic reconstructs all 168 fits through independent numerical formulas, checks forecast arithmetic, compares selection rules, and verifies all earlier files. This is independent computational checking within the same project, not an external review or proof of model validity. The portfolio describes implemented orchestration rather than autonomous multi-LLM discovery.

## 17. Limitations

Version 1 is constrained more by the **amount and structure of information** than by the sophistication of its modelling code. The 717-row development panel contains only 239 monthly dates per category, and the three categories co-move; the final panel contains 252 dates per category through December 2025. These rows should not be interpreted as hundreds of independent market experiments. This small effective sample limits flexible ML, hyperparameter search, regime identification and especially long-horizon model comparison. The Stage 9 five-year experiment has only seven overlapping annual origins per category/model, so model rankings and empirical forecast ranges remain uncertain.

Only 2025 was a genuinely untouched outcome year. Its 12 monthly targets per category are serially dependent and represent one future market path. The result that naive beat the historically selected AR models is therefore strong evidence about **this holdout**, but not proof that naive forecasting is universally superior.

The history is a later-revised snapshot; reference chronology is controlled but original-vintage availability is not reconstructed. Historical backtests therefore contain revision hindsight relative to the information analysts actually had at earlier dates. Changing benchmark attributes and annual historical recalculation can also affect earlier observations.

Geographic and property coverage is narrow. No exact City of Vancouver, Vancouver East/West, administrative Metro Vancouver or exact local detached inference is supported. The source-defined benchmark is useful for market-level analysis but compresses underlying transaction heterogeneity; Version 1 cannot learn individual-property effects such as size, age, bedrooms, lot size or exact location.

External explanatory coverage is limited to historical policy rates, and the final models use no future external predictors. Mortgage rates, sales, inventory, listings, supply, income, employment and demographic variables are absent. There is no causal identification. Forecast coefficients, regime membership and policy associations must not be interpreted as causal effects.

Uncertainty is also limited. Stage 9 reports central projections and historical-error-based ranges rather than fully calibrated probabilistic forecasts. Five-year ranges based on seven selected-model errors may be too narrow under structural change. The model registry, eligibility gates and simplicity thresholds are research-design choices that can affect selection, especially apartment AR order.

The regime results are descriptive rather than proof of latent economic states. Separation is modest and apartment assignments are materially specification-sensitive.

The agent architecture is also deliberately bounded. Specialized roles, shared state, routing and Critic review are implemented, but many scientific choices are constrained by predefined stage contracts, registries, validation origins and thresholds. This improves control and reproducibility while limiting autonomous analytical search.

Finally, full public byte-for-byte reproduction is constrained by third-party licensing. The private research package preserves restricted source material and full generated outputs, but the public repository should not redistribute material without clear publication rights.

## 18. Future Directions

The highest-value improvement is **more informative data, not a more complicated model on the same small sample**.

### 18.1 Expand the geography × property-type panel

Version 2 should first expand the dataset to a monthly panel such as:

`month × geography × property type`

A panel spanning many municipalities/submarkets and housing categories would let models learn both common GVR dynamics and local differences. It still would not create hundreds of independent time periods, but it would provide much richer cross-sectional structure for hierarchical/panel forecasting.

### 18.2 Add transaction-level modelling as a separate layer

Version 1 uses MLS HPI benchmark prices, not simple arithmetic transaction averages. That is useful for market-level analysis because it reduces transaction-composition effects, but one benchmark compresses potentially thousands of sales into a single monthly market measure.

If legally usable transaction-level data become available, a later version could model:

`transaction price ~ size + age + bedrooms + property type + location + time + ...`

This would support hedonic/ML property valuation and potentially a quality-adjusted local index. Thousands of monthly sales would materially improve cross-sectional learning, although they would not become thousands of independent observations of the market's macro time evolution.

### 18.3 Reconstruct real-time data vintages

Future records should distinguish reference month, release date, vintage date and availability so historical forecasts use values genuinely available at each forecast origin rather than the current revised view of the past.

A stronger data contract would include fields such as:

- `reference_month`
- `release_date`
- `vintage_date`
- `available_at`
- `benchmark_price`

### 18.4 Add economically justified predictors

Candidate information families include mortgage rates, sales, inventory, new listings, sales-to-active-listings ratios, starts/completions, permits, employment/income and population. Their value should be judged by **incremental out-of-sample accuracy beyond persistence**, not by in-sample fit.

### 18.5 Use panel/hierarchical and ensemble forecasting

Version 1 showed that winner-take-all historical model selection can be fragile. Future work should evaluate:

- hierarchical/panel models;
- simple and performance-weighted forecast combinations;
- horizon-specific designs;
- time-varying parameters/structural-break handling;
- mandatory naive/drift baselines.

Short-, medium- and five-year horizons should not be assumed to share one optimal model.

### 18.6 Add probabilistic forecasts

Once the dataset is richer, evaluate methods such as time-aware conformal prediction and quantile forecasting. Report empirical coverage/calibration, not only point error. Historical-error bands from a handful of long-horizon cases should not be presented as fully calibrated probability intervals.

### 18.7 Make the agent layer more genuinely autonomous—selectively

Keep hard methodological constraints fixed:

- no holdout leakage;
- chronological validation;
- source integrity;
- deterministic/reproducible tool execution;
- bounded computation/retries;
- Critic review;
- human approval for major capability changes.

Give agents more discretion over:

- which registered models merit testing;
- which diagnostics to run;
- which feature hypotheses to propose;
- whether the current registry appears inadequate;
- whether a new method such as SARIMA/state-space modelling should be proposed for human approval.

A useful Version 2 experiment would compare deterministic/scripted policies with live LLM agents under identical tool/state contracts, measuring reproducibility, decision quality, unnecessary tool use, cost, failure rate and Critic interventions.

### 18.8 Preserve future years as genuine prospective tests

Do not repeatedly retune frozen models and then call later observations untouched tests. Preserve Version 1 and Version 2 forecasts and evaluate them prospectively as 2026+ observations accumulate.

### Version 2 research question

> **How much incremental forecast accuracy can richer local-market, property-level and economic information provide beyond a simple persistence forecast of Greater Vancouver housing prices, and how stable is that improvement across horizons and market conditions?**

## 19. Reproducibility

The complete source registry, raw files, prior decisions, stage states, logs, tests and immutable forecasts remain in the project. Stage 9 preserves every one of the 640 pre-existing files by hash. `post_holdout_provenance.json` records the exact join and source hashes; `pre_fit_registration.json` binds the registered plan and code before fitting. Fit traces preserve training counts, hashes, coefficients/scalers and extrapolation diagnostics. CSV outputs retain unrounded values.

`scripts/run_stage9.py` is create-once and refuses to overwrite this experiment. `scripts/test_final_project.py` runs regressions in a disposable copy, keeping prior evaluation logs unchanged. `scripts/finalize_stage9.py` checks the final Critic and all tests, writes `stage9_validation.json` and `stage9_exit_criteria.json`, and seals the final manifest. `scripts/inspect_stage9.py` verifies completion read-only. The final validation appendix records the executed counts; no success is inferred merely from generating this report.

Stage 1–8 test counts progressed through 36, 72, 96, 128, 156, 184, 220 and 252 passing tests. The final-stage suite adds chronology, prefix mutation, category, range, arithmetic, acquisition and preservation checks. These tests validate implementation and controls; they cannot certify the future forecast.

## 20. Conclusion

The central forecasting lesson is that historical model superiority must survive a genuinely unused outcome period, and the original AR improvement did not. Descriptive housing regimes were reproducible enough to be useful context but sensitive enough to require restrained interpretation. A separately authorized long-horizon experiment produces reviewable 2030 benchmarks with explicit uncertainty, without rewriting the earlier result. The research system's contribution is a transparent chain of evidence, constrained tools, critical checks and human decisions. This is the final project stage; there is no automatic Stage 10.

## Portfolio-ready project summary

I implemented a Python research system for GVR-board housing-market analysis, with seven specialized agent roles, typed shared state, explicit routing, restricted tools, and versioned model registries. The project combined authored agent workflows with deterministic execution and Critic checks; it was not a live multi-LLM deployment.

Human-in-the-loop decisions shaped the research scope. When a complete nine-series dataset could not be validated through acceptable public routes, acquisition stopped and the study retained three source-defined board-level categories. Historical revisions, access boundaries, and category definitions were documented rather than concealed.

I built chronological time-series validation, fold-local preprocessing, immutable forecast manifests, and guarded holdout evaluation. Linear, regularized, autoregressive, and tree-based methods were compared against simple baselines. Models that improved historical validation nevertheless lost to naive forecasts on the untouched 2025 holdout, providing a concrete lesson about generalization.

The project also compared historical clustering methods, tested temporal stability, and froze numeric regimes before assigning descriptive labels. A separately authorized post-holdout experiment then produced five-year benchmark forecasts, empirical error ranges, and transparent growth scenarios.

Reproducibility rests on preserved source files, hashes, persistent state, execution logs, independent numerical checks, and regression tests. The result is a research prototype demonstrating orchestration and methodological controls, not production deployment or causal evidence about housing markets.

## Final validation and completion

**288/288 tests passed**: all 252 prior tests plus 36 Stage 9 tests, with zero skips. The final Critic approves. All 640 pre-existing files remain unchanged. Stage 9 exit criteria pass. Project complete; no Stage 10, additional acquisition or forecast optimization is authorized.
