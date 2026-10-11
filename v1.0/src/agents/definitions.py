from dataclasses import dataclass


@dataclass(frozen=True)
class AgentSpec:
    name: str
    objective: str
    tools: tuple[str, ...]
    readable_fields: tuple[str, ...]
    required_tool: str


SPECS = [
    AgentSpec("data_source_agent", "Register provenance; do not imply synthetic data are real.",
              ("register_demo_source",), ("sources", "dataset_metadata"), "register_demo_source"),
    AgentSpec("data_auditor", "Audit chronological development inputs; investigate, never delete.",
              ("audit_development",), ("sources", "data_quality"), "audit_development"),
    AgentSpec("feature_agent", "Build available-at-origin lags and fully document each calculation.",
              ("build_lag_features",), ("data_quality", "feature_metadata"), "build_lag_features"),
    AgentSpec("forecast_agent", "Select registered candidates using chronological unseen validation.",
              ("validate_candidates", "inspect_registries"),
              ("data_quality", "feature_metadata", "forecast_validation_results", "selected_models"),
              "validate_candidates"),
    AgentSpec("regime_agent", "Declare Stage 1 scope; do not invent groups or economic labels.",
              ("record_regime_scope", "inspect_registries"),
              ("feature_metadata", "regime_candidates", "regime_results"), "record_regime_scope"),
    AgentSpec("critic_agent", "Actively inspect evidence; reject flaws or request human judgment.",
              ("inspect_validation",),
              ("sources", "data_quality", "feature_metadata", "forecast_candidates",
               "forecast_validation_results", "selected_models", "regime_results"),
              "inspect_validation"),
    AgentSpec("report_agent", "Render only current approved findings; do no new numerical analysis.",
              ("render_report",), ("approved_findings",), "render_report"),
]
AGENTS = {spec.name: spec for spec in SPECS}
