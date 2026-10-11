"""Typed contracts persisted independently of any LLM conversation."""
from dataclasses import asdict, dataclass, field
from typing import Any, Literal
from datetime import date
import math

Json = dict[str, Any]
AgentName = Literal["data_source_agent", "data_auditor", "feature_agent",
                    "forecast_agent", "regime_agent", "critic_agent", "report_agent"]


@dataclass(frozen=True)
class Observation:
    date: str
    price: float
    available_at: str
    source_id: str = "synthetic"

    def __post_init__(self):
        date.fromisoformat(self.date)
        date.fromisoformat(self.available_at)
        if isinstance(self.price, bool) or not math.isfinite(self.price) or self.price <= 0:
            raise ValueError("Prices must be finite and positive; investigate invalid rows.")


@dataclass(frozen=True)
class SourceRecord:
    source_name: str
    url: str | None
    access_date: str
    frequency: str
    start_date: str
    end_date: str
    variables: list[str]
    publication_lag: str
    vintage_status: str
    license_notes: str
    used_for: str
    synthetic: bool
    transformations: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class HumanReview:
    stage: str
    problem: str
    evidence: Json
    attempts: list[str]
    recommendation: str
    alternatives: list[str]
    consequences: list[str]
    question_for_human: str
    resume_agent: str

    def __post_init__(self):
        if not all((self.stage, self.problem, self.recommendation, self.question_for_human)):
            raise ValueError("Human review must include a problem, evidence and a question.")
        if not self.alternatives or len(self.alternatives) != len(self.consequences):
            raise ValueError("Each review alternative needs a consequence.")


@dataclass(frozen=True)
class CriticReview:
    decision: Literal["approve", "revise", "human_review"]
    target_agent: str | None
    issue: str
    evidence: Json
    required_action: str
    recommendation: str
    question_for_human: str | None = None

    def __post_init__(self):
        if self.decision not in {"approve", "revise", "human_review"}:
            raise ValueError("Invalid critic decision.")
        if self.decision == "revise" and self.target_agent not in {
            "feature_agent", "forecast_agent", "regime_agent"
        }:
            raise ValueError("Critic revision must name a revisable agent.")
        if self.decision != "approve" and not self.issue:
            raise ValueError("Rejection requires an issue.")


@dataclass(frozen=True)
class AgentAction:
    kind: Literal["tool", "finish", "review", "human_review"]
    name: str = ""
    arguments: Json = field(default_factory=dict)
    rationale: str = ""

    def __post_init__(self):
        if self.kind not in {"tool", "finish", "review", "human_review"}:
            raise ValueError("Invalid action type.")
        if not isinstance(self.arguments, dict) or not isinstance(self.rationale, str):
            raise ValueError("Agent arguments must be an object; rationale must be text.")


@dataclass
class WorkflowState:
    run_id: str
    backend: str = "demo"
    schema_version: int = 1
    workflow_status: str = "running"
    current_agent: str = "data_source_agent"
    next_agent: str = "data_source_agent"
    sources: Json = field(default_factory=dict)
    dataset_metadata: Json = field(default_factory=dict)
    data_quality: Json = field(default_factory=dict)
    transformations: list[Json] = field(default_factory=list)
    feature_metadata: Json = field(default_factory=dict)
    feature_dataset: list[Json] = field(default_factory=list)
    feature_catalog: Json = field(default_factory=dict)
    feature_families: Json = field(default_factory=dict)
    target_design: Json = field(default_factory=dict)
    forecast_horizon_design: Json = field(default_factory=dict)
    validation_design: Json = field(default_factory=dict)
    policy_asof_design: Json = field(default_factory=dict)
    regime_feature_design: Json = field(default_factory=dict)
    fold_local_transformations: Json = field(default_factory=dict)
    stage4_decisions: Json = field(default_factory=dict)
    stage4_artifacts: list[Json] = field(default_factory=list)
    model_registry_usage: Json = field(default_factory=dict)
    forecast_design: Json = field(default_factory=dict)
    forecast_selection_record: Json = field(default_factory=dict)
    stage5_decisions: Json = field(default_factory=dict)
    stage5_artifacts: list[Json] = field(default_factory=list)
    forecast_candidates: Json = field(default_factory=dict)
    forecast_validation_results: Json = field(default_factory=dict)
    selected_models: Json = field(default_factory=dict)
    forecast_2025: Json = field(default_factory=dict)
    regime_candidates: Json = field(default_factory=dict)
    regime_results: Json = field(default_factory=dict)
    critic_reviews: list[Json] = field(default_factory=list)
    human_decisions: list[Json] = field(default_factory=list)
    approved_findings: Json = field(default_factory=dict)
    artifacts: list[Json] = field(default_factory=list)
    iteration_counts: dict[str, int] = field(default_factory=dict)
    invocation_counts: dict[str, int] = field(default_factory=dict)
    errors: list[Json] = field(default_factory=list)
    holdout_status: str = "locked"
    holdout_unlocked_at: str | None = None
    freeze_verification: Json = field(default_factory=dict)
    holdout_audit: Json = field(default_factory=dict)
    baseline_holdout_metrics: list[Json] = field(default_factory=list)
    enhanced_holdout_metrics: list[Json] = field(default_factory=list)
    historical_holdout_comparison: list[Json] = field(default_factory=list)
    generalization_findings: Json = field(default_factory=dict)
    stage7_critic_review: Json = field(default_factory=dict)
    stage7_artifacts: list[Json] = field(default_factory=list)
    regime_method_registry: Json = field(default_factory=dict)
    regime_experiment_plan: Json = field(default_factory=dict)
    regime_validation_results: Json = field(default_factory=dict)
    regime_selection_record: Json = field(default_factory=dict)
    regime_numeric_freeze: Json = field(default_factory=dict)
    regime_descriptive_labels: Json = field(default_factory=dict)
    stage8_artifacts: list[Json] = field(default_factory=list)
    revision: int = 0
    approved_revision: int | None = None
    frozen_manifest: Json | None = None
    pending_review: Json | None = None
    steps: int = 0

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        if data.get("schema_version") != 1:
            raise ValueError("Unsupported checkpoint schema.")
        return cls(**data)

    def invalidate_approval(self):
        if self.frozen_manifest:
            raise ValueError("Frozen experiment is closed to further model development.")
        self.revision += 1
        self.approved_revision = None
        self.approved_findings = {}
