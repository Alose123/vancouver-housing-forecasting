# Vancouver Housing Forecasting — Version 1.0

Version 1.0 is the completed research prototype for **Greater Vancouver REALTORS (GVR) board-level housing forecasting and historical market-regime analysis**.

The project is intentionally presented as a research and engineering prototype rather than a production forecasting service. It combines deterministic Python orchestration, seven specialized analytical roles, typed shared state, restricted tools, model registries, Critic checks, human-in-the-loop decisions, chronological validation, immutable forecast freezes, and reproducibility tests.

## Headline results

- Final approved housing scope: GVR board, `apartment`, `townhouse`, and `single_family_mixed`.
- Core pre-2025 development panel: **717 rows = 239 months × 3 categories** (January 2005–November 2024). These are not 717 independent time observations; there are only 239 monthly dates per category.
- Final post-holdout panel: **756 rows = 252 months × 3 categories** through December 2025.
- Historical validation initially favored autoregressive models for apartments and townhouses, but those models **failed to generalize to the untouched 2025 holdout**. The simple naive baseline performed materially better in 2025.
- Historical regime analysis compared 90 configurations and retained descriptive two-state K-means solutions: **Higher-growth expansion** and **Lower-growth adjustment**, with important specification sensitivity—especially for apartments.
- A separate post-holdout five-year experiment produced December 2030 central benchmark projections of approximately **$912k apartments**, **$1.445M townhouses**, and **$2.430M mixed single-family**, with explicit historical-error ranges and substantial uncertainty.
- Final validation: **288/288 tests passed** in the completed private research package.

## What Version 1 demonstrates

The strongest contribution is not a claim of highly accurate housing prediction. It is the end-to-end research process:

1. data provenance and scope validation;
2. refusal to stitch incompatible historical vintages;
3. explicit human review when the original data scope became infeasible;
4. leakage-safe feature timing and chronological validation;
5. baseline and learned-model comparison;
6. forecast freezing before holdout access;
7. honest preservation of negative out-of-sample results;
8. descriptive regime discovery with stability checks;
9. deterministic Critic verification and persistent audit logs.

The project uses authored agent roles and bounded decision logic. It is **not presented as a live autonomous multi-LLM research system**.

## Public release contents

The public Version 1 release contains the methodology and a sanitized source-code archive. Restricted third-party raw housing files, source PDFs and large generated run artifacts are intentionally omitted from the public repository.

- [Final project report](docs/FINAL_PROJECT_REPORT.md)
- [Limitations and future directions](docs/LIMITATIONS_AND_FUTURE_DIRECTIONS.md)
- [Public data notice](docs/PUBLIC_DATA_NOTICE.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)
- [Sanitized source archive instructions](archive/README.md)

## Versioning

- **v1.0** — completed aggregate benchmark-price forecasting, untouched 2025 holdout evaluation, regime analysis, and post-holdout 2030 forecasting.
- **v2.0 (planned)** — expanded geographic/property panel, richer time-aware predictors, real-time data vintages where feasible, probabilistic/ensemble forecasts, and greater analytical agent discretion while retaining hard leakage and governance guardrails.

## Scope warning

`single_family_mixed` is the source-defined mixed single-family category and must not be relabelled as detached. GVR board territory is not the same thing as administrative Metro Vancouver, and Version 1 does not support exact Vancouver East/West or City-of-Vancouver conclusions.
