# Vancouver Housing Forecasting

**Headline finding:** Autoregressive models improved historical validation for apartments and townhouses, but naive forecasts were more accurate on the untouched 2025 holdout. Apartment holdout MAE was $31,302 for AR versus $18,067 for naive; townhouse MAE was $89,155 versus $27,325.

Research repository for a versioned Greater Vancouver housing forecasting and market-regime project.

## Versions

- **[v1.0](v1.0/README.md)** — completed GVR board-level benchmark-price study: data governance, chronological forecasting, untouched 2025 holdout evaluation, and historical regime discovery.
- **[v2.0](v2.0/README.md)** — planned expansion focused first on richer data: broader geography × property-type panels, vintage-aware inputs, additional market fundamentals, probabilistic/ensemble forecasting, and more analytical agent discretion under the same hard leakage controls.

Version 1.0 is intentionally preserved as a baseline rather than rewritten as Version 2 evolves.

## Public-release note

The public repository does **not** redistribute restricted third-party housing source files or bulky generated run artifacts from the private research package. Version 1.0 publishes the final report, methodology, public-release notices, and a readable core implementation snapshot. See the Version 1.0 third-party/public-data notices for details.

## Research direction

Version 2 asks what additional information genuinely improves forecasting beyond persistence.
