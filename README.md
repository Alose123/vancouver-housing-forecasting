# Vancouver Housing Forecasting

Research repository for a versioned Greater Vancouver housing forecasting and market-regime project.

## Versions

- **[v1.0](v1.0/README.md)** — completed GVR board-level benchmark-price study: data governance, chronological forecasting, untouched 2025 holdout evaluation, historical regime discovery, and a separate post-holdout 2030 forecasting exercise.
- **[v2.0](v2.0/README.md)** — planned expansion focused first on richer data: broader geography × property-type panels, vintage-aware inputs, additional market fundamentals, probabilistic/ensemble forecasting, and more analytical agent discretion under the same hard leakage controls.

Version 1.0 is intentionally preserved as a baseline rather than rewritten as Version 2 evolves.

## Public-release note

The public repository does **not** redistribute restricted third-party housing source files or the bulky generated run artifacts from the private research package. Version 1.0 publishes the final report, methodology, public-release notices, and a readable core implementation snapshot. A complete sanitized source bundle (excluding restricted third-party data and bulky generated outputs) is prepared separately because the connected GitHub writer cannot directly transfer local binary archives. See the Version 1.0 third-party/public-data notices for details.

## Core Version 1 lesson

A historically superior model is not necessarily a superior future model. Autoregressive models improved historical validation for apartments and townhouses, but the simpler naive baseline performed substantially better on the untouched 2025 holdout. Version 2 is therefore designed around a stronger question: **what additional information genuinely improves forecasting beyond persistence?**
