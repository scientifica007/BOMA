#!/usr/bin/env python3
"""Pre-START realistic provider-capacity and response-contract probe; no BOMA research decision."""
from __future__ import annotations

import provider as provider_module
from core import AUTONOMY, EXP_STATE, METRICS, PROGRAM_MANIFEST, GovernanceError, current_head, experiment_record, load_json, save_json, utc_now
from provider import AIProvider

OUT = AUTONOMY / "provider-preflight.json"


def synthetic_evidence(section_count: int, chars_each: int) -> str:
    chunks: list[str] = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for index in range(section_count):
        seed = (alphabet * ((chars_each // len(alphabet)) + 1))[:chars_each]
        chunks.append(
            f"## FILE synthetic/evidence-{index:02d}.txt\n"
            f"SYNTHETIC_NON_RESEARCH_SECTION={index}\n{seed}\n"
        )
    chunks.append("## REPOSITORY TREE\nsynthetic/a\nsynthetic/b\nsynthetic/c\n")
    return "\n".join(chunks)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GovernanceError(message)


def valid_complete_operation(op: object) -> bool:
    if not isinstance(op, dict):
        return False
    if op.get("action") == "delete":
        return isinstance(op.get("path"), str) and set(op).issubset({"action", "path"})
    if op.get("action") == "write":
        return (
            isinstance(op.get("path"), str)
            and isinstance(op.get("content"), str)
            and set(op).issubset({"action", "path", "content"})
        )
    return False


def exercise_planner_manifest_contract() -> None:
    """Exercise the provider-side fixed-field binder without arming research."""
    manifest = load_json(PROGRAM_MANIFEST)
    rec = experiment_record(manifest, "ST2-EXP-015")
    raw = {
        "research_question": "SYNTHETIC_CONTRACT_ONLY",
        "smart_objective": "SYNTHETIC_CONTRACT_ONLY",
        "plan_steps": ["synthetic"],
        "success_criteria": ["synthetic"],
        "verification_commands": ["true"],
        "allowed_recovery_envelope": ["synthetic"],
    }
    original_load = provider_module.load_json

    def synthetic_load(path):
        if path == EXP_STATE:
            return {"armed": True}
        return original_load(path)

    provider_module.load_json = synthetic_load
    try:
        metrics: dict = {}
        bound = provider_module._planner_contract(raw, metrics)
        require(bound.get("experiment_id") == "ST2-EXP-015", "planner contract did not inject experiment_id")
        require(bound.get("single_changed_factor") == rec.get("single_changed_factor"), "planner contract did not inject authorized factor")
        require(bound.get("fixed_controls") == rec.get("fixed_controls"), "planner contract did not inject fixed controls")
        require(bound.get("affected_cone") == rec.get("affected_cone"), "planner contract did not inject affected cone")
        history = metrics.get("planner_pre_review_validation_history")
        require(isinstance(history, list) and history and history[-1].get("contract_passed") is True, "planner contract history missing successful binding")

        conflicting = dict(raw)
        conflicting["single_changed_factor"] = "SYNTHETIC_CONFLICT"
        conflict_metrics: dict = {}
        rejected = provider_module._planner_contract(conflicting, conflict_metrics)
        require(rejected.get("single_changed_factor") == "SYNTHETIC_CONFLICT", "planner contract silently corrected a conflicting factor")
        require(rejected.get("experiment_id") == "__PLANNER_MANIFEST_CONTRACT_CONFLICT__", "planner contract did not force deterministic rejection of a conflict")
        conflict_history = conflict_metrics.get("planner_pre_review_validation_history")
        require(isinstance(conflict_history, list) and "single_changed_factor" in conflict_history[-1].get("conflicting_manifest_fields", []), "planner conflict history not recorded")
    finally:
        provider_module.load_json = original_load


def main() -> int:
    state = load_json(EXP_STATE)
    generation = str(state.get("experiment_generation") or "")
    require(generation == "BOMA-AUTONOMY-008", "provider probe requires Generation 008 bootstrap")

    exercise_planner_manifest_contract()

    metrics = load_json(METRICS)
    ai = AIProvider(metrics)
    evidence = synthetic_evidence(24, 2800)

    qwen = ai.ask_json(
        "transition_auditor",
        "Technical capacity and response-contract probe only. Return JSON only. Do not analyze BOMA or mathematics.",
        "Return exactly this structural shape: "
        "{\"ok\":true,\"kind\":\"BOMA_REALISTIC_QWEN_PREFLIGHT\","
        "\"transition_gate_evaluation\":{\"decision\":\"OWNER_REQUIRED\","
        "\"rationale\":\"SYNTHETIC_CONTRACT_ONLY\"}}. "
        "The decision value is a synthetic schema sentinel, not a BOMA research decision. "
        "The following large marked sections are synthetic padding used only to exercise deterministic capacity compaction.\n\n"
        + evidence,
        max_tokens=3000,
    )
    require(
        qwen.get("ok") is True
        and qwen.get("kind") == "BOMA_REALISTIC_QWEN_PREFLIGHT"
        and qwen.get("decision") == "OWNER_REQUIRED"
        and qwen.get("rationale") == "SYNTHETIC_CONTRACT_ONLY"
        and "transition_gate_evaluation" not in qwen,
        f"Qwen realistic preflight/nested transition contract returned unexpected payload: {qwen!r}",
    )

    gpt = ai.ask_json(
        "planner",
        "Technical capacity probe only. Return JSON only. Do not analyze BOMA or mathematics.",
        "Return exactly an object with ok=true, kind='BOMA_REALISTIC_GPT_PREFLIGHT'. "
        "The following large marked sections are synthetic padding used only to exercise deterministic capacity compaction.\n\n"
        + evidence,
        max_tokens=4500,
    )
    require(
        gpt.get("ok") is True and gpt.get("kind") == "BOMA_REALISTIC_GPT_PREFLIGHT",
        f"GPT realistic preflight returned unexpected payload: {gpt!r}",
    )

    recovery = ai.ask_json(
        "recovery_analyst",
        "Technical recovery response-contract probe only. Return JSON only. Do not analyze BOMA or mathematics.",
        "Return exactly this synthetic schema object and no patch/diff/tool-call aliases: "
        "{\"decision\":\"RECOVER\",\"classification\":\"HARNESS\","
        "\"rationale\":\"SYNTHETIC_CONTRACT_ONLY\",\"operations\":["
        "{\"action\":\"write\",\"path\":\"virtual/recovery-contract.txt\","
        "\"content\":\"SYNTHETIC\\n\"}],\"frozen_plan_unchanged\":true,"
        "\"research_decision_unchanged\":true}. "
        "This is schema simulation only; nothing will be written and no research decision is involved.",
        max_tokens=1500,
    )
    operations = recovery.get("operations")
    require(recovery.get("decision") == "RECOVER", f"recovery contract decision invalid: {recovery!r}")
    require(recovery.get("rationale") == "SYNTHETIC_CONTRACT_ONLY", f"recovery contract rationale invalid: {recovery!r}")
    require(recovery.get("frozen_plan_unchanged") is True, f"recovery frozen-plan flag invalid: {recovery!r}")
    require(recovery.get("research_decision_unchanged") is True, f"recovery research-decision flag invalid: {recovery!r}")
    require(isinstance(operations, list) and len(operations) == 1, f"recovery operations array invalid: {recovery!r}")
    require(valid_complete_operation(operations[0]), f"recovery operation shape invalid: {operations[0]!r}")
    require(operations[0].get("path") == "virtual/recovery-contract.txt", f"recovery path mismatch: {operations[0]!r}")
    require(str(operations[0].get("content", "")) == "SYNTHETIC\n", f"recovery content mismatch: {operations[0]!r}")
    require(not any(key in operations[0] for key in ("type", "file", "patch", "diff")), f"legacy patch-style recovery aliases forbidden: {operations[0]!r}")

    record = {
        "schema": "BOMA-AUTONOMY-PROVIDER-PREFLIGHT-008",
        "experiment_generation": generation,
        "passed": True,
        "head_sha": current_head(),
        "completed_at": utc_now(),
        "synthetic_source_characters": len(evidence),
        "models_exercised": sorted({
            ai.config["models"]["transition_auditor"],
            ai.config["models"]["planner"],
            ai.config["models"]["recovery_analyst"],
        }),
        "production_requested_completion_tokens": {
            "transition_auditor": 3000,
            "planner": 4500,
            "recovery_analyst": 1500,
        },
        "transition_response_contract_exercised": True,
        "transition_response_contract_input_shape": "transition_gate_evaluation.decision",
        "transition_response_contract_canonical_output": "decision=OWNER_REQUIRED / synthetic sentinel only",
        "recovery_operation_contract_exercised": True,
        "recovery_operation_contract_required_shape": "operations[].action/path/content-complete-write-or-delete; patch aliases forbidden",
        "planner_manifest_contract_exercised": True,
        "planner_manifest_contract_behavior": "missing fixed fields injected from authorized manifest; conflicting supplied fields preserved and forced to deterministic pre-review rejection",
        "research_content_read": False,
        "research_decision_made": False,
    }
    save_json(OUT, record)
    print("BOMA Generation-008 realistic AI provider and planner/recovery contract preflight: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
