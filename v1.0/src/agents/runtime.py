"""Permission-filtered views and one common bounded agent/tool loop."""
from dataclasses import asdict
import copy
from ..config import HARD_CONSTRAINTS
from ..state import CriticReview, HumanReview
from ..tools.registry import TOOLS, execute_tool


def agent_view(spec, state):
    from ..acquisition.contracts import require_stage2_closed
    require_stage2_closed(state)
    if spec.name == "report_agent":
        from ..evaluation.leakage_checks import require_report_approval
        require_report_approval(state)
    return {
        "objective": spec.objective, "required_tool": spec.required_tool,
        "cutoff": "2024-12-31", "synthetic_demo": True,
        "hard_constraints": list(HARD_CONSTRAINTS),
        "iteration_count": state.iteration_counts.get(spec.name, 0),
        "revision": state.revision,
        "state": {field: copy.deepcopy(getattr(state, field)) for field in spec.readable_fields},
        "latest_critique": copy.deepcopy(state.critic_reviews[-1])
                           if state.critic_reviews and spec.name != "report_agent" else None,
    }


def invoke(spec, backend, state, store, config, logger, apply_patch):
    from ..acquisition.contracts import require_stage2_closed
    require_stage2_closed(state)
    view = agent_view(spec, state)
    tools = [{"name": name, "description": TOOLS[name].description,
              "parameters": TOOLS[name].parameters} for name in spec.tools]
    logger.event("agent_started", agent=spec.name, objective=spec.objective,
                 input_summary={"fields": list(view["state"]), "revision": state.revision})
    history = []
    for turn in range(config.max_agent_turns):
        action = backend.next_action(spec, view, history, tools)
        logger.event("agent_action", agent=spec.name, action=asdict(action),
                     backend=backend.name, provider_metadata=getattr(backend, "response_metadata", {}))
        if action.kind == "human_review":
            return HumanReview(**action.arguments)
        if action.kind == "tool":
            logger.event("tool_started", agent=spec.name, tool=action.name,
                         arguments=action.arguments, rationale=action.rationale)
            try:
                result = execute_tool(spec.name, action.name, action.arguments, state, store, config)
            except Exception as error:
                logger.event("tool_failed", agent=spec.name, tool=action.name,
                             error_type=type(error).__name__, summary=str(error))
                raise
            apply_patch(spec.name, action.name, result.patch)
            logger.event("tool_completed", agent=spec.name, tool=action.name,
                         result=result.payload, patch_fields=list(result.patch), validation="pass")
            history.append({"name": action.name, "payload": result.payload,
                            "call_id": getattr(backend, "last_call_id", f"demo-{turn}")})
            view = agent_view(spec, state)
            continue
        if not any(item["name"] == spec.required_tool for item in history):
            raise ValueError("Agent tried to finish without its required deterministic evidence.")
        if spec.name == "critic_agent":
            if action.kind != "review":
                raise ValueError("Critic must return a structured review.")
            review = CriticReview(**action.arguments)
            evidence = next(item["payload"] for item in reversed(history)
                            if item["name"] == "inspect_validation")
            if review.decision == "approve" and (evidence["issues"] or evidence["human_review_required"]):
                raise ValueError("Critic cannot approve known violations or unresolved human review.")
            return review
        if action.kind != "finish":
            raise ValueError("Only the critic may submit a critic review.")
        return None
    raise RuntimeError("Agent tool-turn budget exhausted; human review required.")
