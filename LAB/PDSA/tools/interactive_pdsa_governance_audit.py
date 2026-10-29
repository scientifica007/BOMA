#!/usr/bin/env python3
"""Verify active interactive governance while preserving frozen historical controls."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PREFIX = ROOT / "LAB/PDSA"
POLICY = PREFIX / "INTERACTIVE_PDSA_EXECUTION_POLICY_2026_10_29.json"
STATE = PREFIX / "AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json"
MANIFEST = PREFIX / "ST2_RP_001_PROGRAM_MANIFEST_001.json"
DECISION = "LAB/PDSA/OWNER_DECISION_2026-10-29_INTERACTIVE_PDSA_MODE.md"
GOVERNANCE = "LAB/PDSA/INTERACTIVE_PDSA_EXECUTION_GOVERNANCE_2026_10_29.md"

def main() -> int:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    effective = state.get("effective_execution_authority", {})
    errs = []
    def req(ok: bool, message: str) -> None:
        if not ok:
            errs.append(message)

    mode = "OWNER_DIRECTED_INTERACTIVE_PDSA"
    req(policy.get("schema") == "BOMA-INTERACTIVE-PDSA-EXECUTION-POLICY-001", "unexpected schema")
    req(policy.get("execution_mode") == mode and effective.get("mode") == mode, "execution mode disagreement")
    req(policy.get("owner_decision_record") == DECISION and effective.get("owner_decision_record") == DECISION, "owner decision mismatch")
    req((ROOT / DECISION).is_file() and (ROOT / GOVERNANCE).is_file(), "missing owner authority")
    req(policy.get("fail_closed") is True, "not fail-closed")
    req(state.get("state") == "OWNER_REQUIRED" and state.get("safety", {}).get("fail_closed") is True, "owner stop lost")
    req(state.get("active_experiment") is None and state.get("active_frozen_plan") is None, "research experiment active")
    req(state.get("current_stage_two_frontier", {}).get("latest_completed_experiment") == "ST2-EXP-015", "closure changed")
    req(state.get("current_stage_two_frontier", {}).get("next_experiment") == "ST2-EXP-016", "next experiment changed")
    req(state.get("authorized_experiment_queue") == manifest.get("queue_order") == ["ST2-EXP-014","ST2-EXP-015","ST2-EXP-016","ST2-EXP-017"], "agenda changed")
    req(manifest.get("routine_merge_authorized") is True and state.get("routine_merge_authorized") is True, "pinned historical merge provenance changed")
    for key in ("autonomous_research_enabled","unattended_continuation_enabled","routine_merge_authorized"):
        req(policy.get(key) is False and effective.get(key) is False, "unauthorized operational permission: " + key)
    req(policy.get("autonomous_actions_when_authorized") == [], "autonomous actions not empty")
    req(policy.get("scheduled_continuation", {}).get("enabled") is False, "scheduled autonomy enabled")
    req(effective.get("new_task_requires_explicit_owner_session_instruction") is True, "owner session approval missing")
    req(effective.get("new_experiment_requires_explicit_owner_session_instruction") is True, "research start approval missing")
    req(effective.get("merge_requires_explicit_owner_approval") is True, "merge approval missing")
    req(policy.get("verification_only_github_actions_allowed") is True, "CI permission missing")
    for path in (ROOT / "AGENTS.md", PREFIX / "STATUS.md"):
        text = path.read_text(encoding="utf-8")
        req(DECISION in text and GOVERNANCE in text and POLICY.name in text, "missing current authority link in " + path.name)
    runtime = json.loads((ROOT / ".autonomy/state.json").read_text(encoding="utf-8"))
    req(runtime.get("armed") is False, "G8 unexpectedly armed")
    if errs:
        print("BOMA interactive PDSA governance: FAIL")
        for e in errs: print("- " + e)
        return 1
    print("BOMA interactive PDSA governance: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
