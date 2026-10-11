"""Only these transitions can be executed, regardless of LLM text."""
ALLOWED_TRANSITIONS = {
    "data_source_agent": {"data_auditor", "human_review"},
    "data_auditor": {"feature_agent", "human_review"},
    "feature_agent": {"forecast_agent", "human_review"},
    "forecast_agent": {"regime_agent", "critic_agent", "human_review"},
    "regime_agent": {"critic_agent", "human_review"},
    "critic_agent": {"feature_agent", "forecast_agent", "regime_agent",
                     "report_agent", "human_review"},
    "human_review": {"data_source_agent", "data_auditor", "feature_agent",
                     "forecast_agent", "regime_agent", "critic_agent", "report_agent", "stop"},
    "report_agent": {"end", "human_review"},
    "end": set(), "stop": set(),
}
DEFAULT_NEXT = {
    "data_source_agent": "data_auditor", "data_auditor": "feature_agent",
    "feature_agent": "forecast_agent", "forecast_agent": "regime_agent",
    "regime_agent": "critic_agent", "report_agent": "end",
}


def require_transition(source: str, target: str):
    if target not in ALLOWED_TRANSITIONS.get(source, set()):
        raise ValueError(f"Forbidden transition: {source} -> {target}")
