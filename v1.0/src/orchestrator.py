"""The Python application owns routing, mutation, limits, gates, and human resumption."""
import copy
from dataclasses import asdict
import json
from .agents.definitions import AGENTS
from .agents.runtime import invoke
from .config import Config
from .evaluation.forecast_evaluation import freeze_forecast, evaluate_holdout
from .evaluation.leakage_checks import require_report_approval
from .logging.run_logger import RunLogger, timestamp
from .registries import CapabilityRequest
from .routing import DEFAULT_NEXT, require_transition
from .state import HumanReview, CriticReview


class Orchestrator:
    def __init__(self, state, store, backend, config=Config()):
        if backend.name != state.backend:
            raise ValueError("Resume must use the same backend as the persisted run.")
        self.state, self.store, self.backend, self.config = state, store, backend, config
        self.logger = RunLogger(store.root / "outputs/logs", state.run_id)

    def transition(self, target):
        origin = self.state.current_agent
        require_transition(origin, target)
        if target == "report_agent":
            require_report_approval(self.state)
        self.logger.event("transition", source=origin, target=target,
                          summary=f"{origin} -> {target}")
        self.state.next_agent = target
        self.state.current_agent = target
        if target in {"end", "stop"}:
            self.state.workflow_status = "complete" if target == "end" else "stopped"
        self.store.save(self.state)

    def apply_patch(self, agent, tool, patch):
        if not patch:
            return
        changes = {key: copy.deepcopy(value) for key,value in patch.items()}
        analytical = set(changes) - {"artifacts"}
        if analytical:
            self.state.invalidate_approval()
        if agent == "feature_agent":
            self.state.forecast_candidates = {}
            self.state.forecast_validation_results = {}
            self.state.selected_models = {}
            self.state.regime_results = {}
        elif agent == "forecast_agent":
            self.state.regime_results = {}
        for key,value in changes.items():
            if key in {"artifacts", "transformations"}:
                getattr(self.state, key).extend(value)
            else:
                setattr(self.state, key, value)
        self.logger.event("state_patch", agent=agent, tool=tool,
                          changes=changes, revision=self.state.revision,
                          summary=f"Updated {', '.join(changes)}")
        self.store.save(self.state)

    def pause(self, packet: HumanReview):
        require_transition("human_review", packet.resume_agent)
        if packet.resume_agent == "stop":
            raise ValueError("Review must identify a resumable agent.")
        self.state.pending_review = asdict(packet)
        self.state.workflow_status = "waiting_for_human"
        self.logger.event("human_review_requested", packet=asdict(packet), summary=packet.problem)
        self.transition("human_review")

    def generic_review(self, stage, problem, recommendation="Inspect the issue before resuming."):
        return HumanReview(stage, problem, {"revision": self.state.revision},
                           [f"Invocation {self.state.invocation_counts.get(stage, 0)}"],
                           recommendation, ["retry", "stop"],
                           ["Resume the same stage using existing capabilities.", "End this run."],
                           "Retry this stage after correcting the issue, or stop?", stage)

    def handle_critic(self, review: CriticReview):
        self.state.critic_reviews.append({**asdict(review), "revision": self.state.revision,
                                          "timestamp": timestamp()})
        self.logger.event("critic_review", review=asdict(review), revision=self.state.revision,
                          summary=review.decision + ": " + review.issue)
        if review.decision == "revise":
            target = review.target_agent
            count = self.state.iteration_counts.get(target, 0)
            if count >= self.config.max_revisions:
                self.pause(self.generic_review(target, "Maximum automatic revisions reached."))
                return
            self.state.iteration_counts[target] = count + 1
            self.state.approved_revision = None
            self.transition(target)
        elif review.decision == "human_review":
            if review.evidence.get("issues") or not review.evidence.get("human_review_required"):
                target = review.target_agent or "critic_agent"
                self.pause(self.generic_review(target, review.issue, review.recommendation))
                return
            packet = HumanReview(
                "forecasting", review.issue, review.evidence,
                list(self.state.forecast_candidates), review.recommendation,
                ["retain_baseline", "retry", "stop"],
                ["Accept a baseline for the engineering demo; no performance claim.",
                 "Re-run registered analyses; new models still require code registration.",
                 "End this run without a report."],
                review.question_for_human or "How should this workflow proceed?", "critic_agent")
            self.pause(packet)
        else:
            self.state.approved_revision = self.state.revision
            self.store.save(self.state)
            self.transition("report_agent")

    def finalize(self):
        require_report_approval(self.state)
        if self.state.approved_findings:
            return
        freeze_forecast(self.state, self.store, self.config, self.logger)
        evaluation = evaluate_holdout(self.state, self.store, self.config, self.logger)
        self.state.approved_findings = {
            "synthetic": True, "sources": self.state.sources,
            "data_quality": self.state.data_quality, "features": self.state.feature_metadata,
            "validation": self.state.forecast_validation_results,
            "selected_models": self.state.selected_models,
            "forecast": self.state.forecast_2025, "backtest": evaluation,
            "regimes": self.state.regime_results,
            "limitations": ["Stage 1 synthetic fixture; no actual housing-market results.",
                            "No uncertainty estimates, real-data vintages or clustering yet."],
        }
        from .storage import csv_text
        artifacts = [
            self.store.write_output("outputs/tables/feature_dataset.csv", csv_text(self.state.feature_dataset)),
            self.store.write_output("outputs/tables/source_registry.json", json.dumps(self.state.sources, indent=2)),
            self.store.write_output("outputs/tables/validation.json", json.dumps(self.state.forecast_validation_results, indent=2)),
        ]
        self.state.artifacts.extend(artifacts)
        self.logger.event("approved_findings_saved", revision=self.state.revision,
                          summary="Validated analytical evidence plus deterministic final evaluation.")
        self.store.save(self.state)

    def run(self):
        from .acquisition.contracts import require_stage2_closed
        require_stage2_closed(self.state)
        if self.state.workflow_status != "running":
            return self.state
        self.store.verify_inputs()
        while self.state.workflow_status == "running":
            agent = self.state.current_agent
            if self.state.steps >= self.config.max_workflow_steps:
                self.pause(self.generic_review(agent, "Global workflow step budget exhausted."))
                break
            self.state.steps += 1
            self.state.invocation_counts[agent] = self.state.invocation_counts.get(agent, 0) + 1
            self.store.save(self.state)
            try:
                if agent == "report_agent":
                    self.finalize()
                result = invoke(AGENTS[agent], self.backend, self.state, self.store,
                                self.config, self.logger, self.apply_patch)
                if isinstance(result, HumanReview):
                    self.pause(result)
                elif isinstance(result, CriticReview):
                    self.handle_critic(result)
                else:
                    self.transition(DEFAULT_NEXT[agent])
            except Exception as error:
                item = {"agent": agent, "type": type(error).__name__, "message": str(error)}
                self.state.errors.append(item)
                self.logger.event("stage_failed", **item, summary=str(error))
                packet = self.generic_review(agent, str(error))
                if isinstance(error, CapabilityRequest):
                    packet = self.generic_review(agent, str(error),
                                                  "Review and implement the capability before retrying; no auto-install.")
                self.pause(packet)
        return self.state

    def resume(self, choice, justification):
        from .acquisition.contracts import require_stage2_closed
        require_stage2_closed(self.state)
        if self.state.workflow_status != "waiting_for_human" or not self.state.pending_review:
            raise ValueError("No pending human decision.")
        if not justification.strip():
            raise ValueError("A human decision requires a justification.")
        packet = HumanReview(**self.state.pending_review)
        if choice not in packet.alternatives:
            raise ValueError("Decision must match a pending review alternative.")
        if choice == "retain_baseline" and packet.stage != "forecasting":
            raise ValueError("Baseline acceptance only applies to forecasting review.")
        target = "stop" if choice == "stop" else packet.resume_agent
        if choice == "retry" and packet.stage == "forecasting":
            target = "forecast_agent"
        self.state.human_decisions.append({
            "timestamp": timestamp(), "choice": choice, "justification": justification,
            "revision": self.state.revision, "packet": asdict(packet), "resume_agent": target,
        })
        self.logger.event("human_decision", choice=choice, justification=justification,
                          target=target, summary=f"Human chose {choice}: {justification}")
        self.state.pending_review = None
        self.state.workflow_status = "running"
        if self.state.steps >= self.config.max_workflow_steps:
            self.state.steps = 0
        self.transition(target)
        return self.run()
