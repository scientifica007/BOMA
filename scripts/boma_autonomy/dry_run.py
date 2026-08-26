#!/usr/bin/env python3
"""Synthetic pre-START technical PDSA dry run.

This exercises JSON role reliability without reading or changing BOMA research.
"""
from __future__ import annotations

import json
from pathlib import Path

from core import AUTONOMY, EXP_STATE, METRICS, GovernanceError, current_head, load_json, save_json, utc_now
from provider import AIProvider

OUT = AUTONOMY / "prestart-dryrun.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GovernanceError(message)


def main() -> int:
    state = load_json(EXP_STATE)
    generation = str(state.get("experiment_generation") or "")
    require(generation == "BOMA-AUTONOMY-003", "dry run requires Generation 003 bootstrap")

    metrics = load_json(METRICS)
    ai = AIProvider(metrics)

    synthetic = {
        "objective": "Create a synthetic text file virtual/hello.txt containing HELLO and verify exact content.",
        "scope": "synthetic dry run only; no BOMA files exist in this scenario",
    }

    plan = ai.ask_json(
        "planner",
        "Role: synthetic technical planner. Return JSON only. No BOMA research.",
        f"""Plan this synthetic software-only dry run:
{json.dumps(synthetic)}
Return keys smart_objective, single_changed_factor, plan_steps, verification_commands,
success_criteria. verification_commands must be a JSON array.""",
        max_tokens=650,
    )
    require(isinstance(plan.get("plan_steps"), list), "dry-run planner missing plan_steps")
    require(isinstance(plan.get("verification_commands"), list), "dry-run planner missing verification_commands")

    review = ai.ask_json(
        "reviewer",
        "Role: synthetic plan reviewer. Return JSON only. No BOMA research.",
        f"""Review this synthetic plan:
{json.dumps(plan)}
Return {{"decision":"APPROVE"|"REVISE","defects":[]}}.
Approve only if it is bounded, deterministic, and does not mention BOMA research.""",
        max_tokens=450,
    )
    require(review.get("decision") in {"APPROVE", "REVISE"}, "invalid dry-run review decision")
    require(review.get("decision") == "APPROVE", f"synthetic plan not approved: {review}")

    execution = ai.ask_json(
        "executor",
        "Role: synthetic executor. Return JSON only. Do not touch a real repository.",
        """Using the approved synthetic objective, return:
{"status":"EXECUTE","operations":[{"action":"write","path":"virtual/hello.txt","content":"HELLO\n"}],
"deviations":[]}.
This is schema simulation only; nothing will actually be written.""",
        max_tokens=500,
    )
    require(execution.get("status") == "EXECUTE", "dry-run executor status invalid")
    operations = execution.get("operations")
    require(isinstance(operations, list) and len(operations) == 1, "dry-run executor operations invalid")
    op = operations[0]
    require(op.get("action") == "write", "dry-run synthetic action must be write")
    require(op.get("path") == "virtual/hello.txt", "dry-run synthetic path mismatch")
    require(str(op.get("content", "")).strip() == "HELLO", "dry-run synthetic content mismatch")

    study = ai.ask_json(
        "study_analyst",
        "Role: synthetic Study analyst. Return JSON only. No BOMA research.",
        """Synthetic evidence: expected virtual/hello.txt == HELLO; simulated executor produced
exactly that; deterministic simulated verification passed. Return
{"result":"PASS","learning":["..."],"deviations":[]}.""",
        max_tokens=400,
    )
    require(study.get("result") == "PASS", "dry-run Study did not PASS")

    act = ai.ask_json(
        "act_analyst",
        "Role: synthetic Act analyst. Return JSON only. No BOMA research.",
        f"""Synthetic Study:
{json.dumps(study)}
Return {{"close":true,"carry_forward":["technical JSON pipeline works"]}}.""",
        max_tokens=350,
    )
    require(act.get("close") is True, "dry-run Act did not close")

    record = {
        "schema": "BOMA-AUTONOMY-PRESTART-DRYRUN-003",
        "experiment_generation": generation,
        "passed": True,
        "head_sha": current_head(),
        "completed_at": utc_now(),
        "research_content_read": False,
        "research_decision_made": False,
        "roles_exercised": ["planner", "reviewer", "executor", "study_analyst", "act_analyst"],
    }
    save_json(OUT, record)
    print("BOMA Generation-003 pre-START synthetic technical dry run: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
