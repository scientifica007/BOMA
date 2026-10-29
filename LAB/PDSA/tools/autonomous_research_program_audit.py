#!/usr/bin/env python3
"""Fail-closed consistency audit for BOMA autonomous research-program governance."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = ROOT / "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_POLICY_001.json"
STATE_PATH = ROOT / "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json"
AGENTS_PATH = ROOT / "AGENTS.md"
STATUS_PATH = ROOT / "LAB/PDSA/STATUS.md"
BASELINE_AUDIT_PATH = ROOT / "LAB/PDSA/BASELINE_INTEGRITY_AUDIT_AUTONOMY_001.md"

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed
        errors.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return {}


policy = load_json(POLICY_PATH)
state = load_json(STATE_PATH)
agents = AGENTS_PATH.read_text(encoding="utf-8")
status = STATUS_PATH.read_text(encoding="utf-8")

require(policy.get("schema") == "BOMA-AUTONOMOUS-RESEARCH-PROGRAM-POLICY-001", "unexpected policy schema")
require(policy.get("default_posture") == "FAIL_CLOSED", "policy must remain FAIL_CLOSED")
require(policy.get("program_authorization_required") is True, "program authorization must be required")
require(policy.get("active_program_created_by_policy") is False, "policy must not activate a program implicitly")

allowed_states = policy.get("allowed_states")
require(isinstance(allowed_states, list) and len(allowed_states) > 0, "allowed_states must be a non-empty list")
current_state = state.get("state")
require(current_state in (allowed_states or []), f"state {current_state!r} is not policy-authorized")
require(state.get("safety", {}).get("fail_closed") is True, "state must preserve fail_closed=true")
require(state.get("safety", {}).get("ambiguous_authority_means") == "OWNER_REQUIRED", "ambiguous authority must mean OWNER_REQUIRED")
require(state.get("safety", {}).get("main_research_writes_allowed") is False, "autonomous research writes to main must remain false")
require(isinstance(state.get("routine_merge_authorized"), bool), "routine_merge_authorized must be boolean")

queue = state.get("authorized_experiment_queue")

if current_state == "NO_ACTIVE_PROGRAM":
    require(state.get("active_program_id") is None, "NO_ACTIVE_PROGRAM cannot have active_program_id")
    require(state.get("owner_authorization_record") is None, "NO_ACTIVE_PROGRAM cannot have owner authorization")
    require(state.get("program_manifest") in (None, ""), "NO_ACTIVE_PROGRAM cannot have program manifest")
    require(state.get("program_baseline_main_sha") is None, "NO_ACTIVE_PROGRAM cannot have baseline sha")
    require(queue == [], "NO_ACTIVE_PROGRAM queue must be empty")
    require(state.get("active_experiment") is None, "NO_ACTIVE_PROGRAM cannot have active experiment")
    require(state.get("routine_merge_authorized") is False, "NO_ACTIVE_PROGRAM cannot authorize routine merge")
else:
    program_id = state.get("active_program_id")
    auth_rel = state.get("owner_authorization_record")
    manifest_rel = state.get("program_manifest")
    require(bool(program_id), "active state requires active_program_id")
    require(bool(auth_rel), "active state requires owner authorization record")
    require(bool(manifest_rel), "active state requires machine-readable program manifest")
    baseline = state.get("program_baseline_main_sha")
    require(isinstance(baseline, str) and re.fullmatch(r"[0-9a-f]{40}", baseline) is not None, "active state requires exact 40-hex baseline main sha")
    require(isinstance(queue, list) and len(queue) > 0, "active state requires non-empty authorized experiment queue")
    if isinstance(queue, list):
        require(len(queue) == len(set(queue)), "authorized experiment queue contains duplicate IDs")
    cursor = state.get("queue_cursor")
    require(isinstance(cursor, int) and isinstance(queue, list) and 0 <= cursor < len(queue), "active state requires a valid queue_cursor")

    auth = ""
    if isinstance(auth_rel, str):
        auth_path = ROOT / auth_rel
        require(auth_path.exists(), f"owner authorization record does not exist: {auth_rel}")
        if auth_path.exists():
            auth = auth_path.read_text(encoding="utf-8")
            require("OWNER_AUTHORIZED" in auth, "authorization record must state OWNER_AUTHORIZED")
            require(str(program_id) in auth, "authorization record must name active_program_id")
            for experiment_id in queue if isinstance(queue, list) else []:
                require(experiment_id in auth, f"authorization record missing queued experiment {experiment_id}")
            if state.get("routine_merge_authorized") is True:
                require("routine_merge_authorized: true" in auth, "routine merge requires explicit true in authorization record")
                require("no SELECTS change" in auth, "routine merge authorization must preserve SELECTS firewall")

    manifest: dict = {}
    if isinstance(manifest_rel, str):
        manifest_path = ROOT / manifest_rel
        require(manifest_path.exists(), f"program manifest does not exist: {manifest_rel}")
        if manifest_path.exists():
            manifest = load_json(manifest_path)
            require(manifest.get("schema") == "BOMA-STAGE-TWO-RESEARCH-PROGRAM-MANIFEST-001", "unexpected active program manifest schema")
            require(manifest.get("program_id") == program_id, "manifest program_id must match active state")
            require(manifest.get("status") == "OWNER_AUTHORIZED", "manifest must be OWNER_AUTHORIZED")
            require(manifest.get("baseline_main_sha") == baseline, "manifest baseline must match state baseline")
            require(manifest.get("queue_order") == queue, "manifest queue must exactly match authorized state queue")
            require(manifest.get("fail_closed") is True, "manifest must preserve fail_closed=true")
            require(manifest.get("routine_merge_authorized") == state.get("routine_merge_authorized"), "manifest/state routine merge authority mismatch")
            experiments = manifest.get("experiments")
            require(isinstance(experiments, list) and len(experiments) == len(queue), "manifest experiment records must cover queue exactly")
            if isinstance(experiments, list) and isinstance(queue, list):
                manifest_ids = [item.get("experiment_id") for item in experiments if isinstance(item, dict)]
                require(manifest_ids == queue, "manifest experiment order must exactly match state queue")
                for item in experiments:
                    if isinstance(item, dict):
                        require(item.get("origin_kind") in {"BRICK", "BLOCK", "DECISION_POINT", "DEPENDENCY_EDGE", "CLAIM", "SUPPORTING_LEMMA"}, f"invalid origin kind for {item.get('experiment_id')}")
                        require(bool(item.get("origin_id")), f"missing typed origin id for {item.get('experiment_id')}")
                        require(bool(item.get("single_changed_factor")), f"missing single changed factor for {item.get('experiment_id')}")

    require(str(program_id) in status, "STATUS.md must name the active research program")
    require(str(current_state) in status, "STATUS.md must name the current autonomous state")
    if isinstance(queue, list) and queue:
        require(queue[state.get("queue_cursor", 0)] in status, "STATUS.md must expose the current authorized queue frontier")

if current_state == "TRANSITION_GATE":
    transition = state.get("program_transition")
    require(isinstance(transition, dict), "TRANSITION_GATE requires program_transition object")
    transition = transition if isinstance(transition, dict) else {}
    from_experiment = transition.get("from_experiment")
    to_candidate = transition.get("to_candidate")
    require(state.get("active_experiment") is None, "TRANSITION_GATE cannot have an active experiment")
    require(state.get("active_experiment_branch") is None, "TRANSITION_GATE cannot have an active experiment branch")
    require(state.get("active_frozen_plan") is None, "TRANSITION_GATE cannot have an active Frozen Plan")
    require(state.get("active_frozen_plan_sha") is None, "TRANSITION_GATE cannot have an active Frozen Plan SHA")
    require(transition.get("transition_decision_recorded") is False, "TRANSITION_GATE baseline must not pre-record a transition decision")
    require(isinstance(queue, list) and from_experiment in queue, "TRANSITION_GATE from_experiment must be in authorized queue")
    require(isinstance(queue, list) and to_candidate in queue, "TRANSITION_GATE to_candidate must be in authorized queue")
    if isinstance(queue, list) and from_experiment in queue and to_candidate in queue:
        from_index = queue.index(from_experiment)
        to_index = queue.index(to_candidate)
        require(to_index == from_index + 1, "TRANSITION_GATE candidate must be the immediate next authorized queue entry")
        require(state.get("queue_cursor") == from_index, "TRANSITION_GATE queue_cursor must remain on the completed source experiment until decision")
    sync_sha = state.get("synchronized_main_sha")
    require(isinstance(sync_sha, str) and re.fullmatch(r"[0-9a-f]{40}", sync_sha) is not None, "TRANSITION_GATE requires synchronized_main_sha")
    baseline_rel = state.get("baseline_integrity_audit")
    require(baseline_rel == "LAB/PDSA/BASELINE_INTEGRITY_AUDIT_AUTONOMY_001.md", "unexpected baseline_integrity_audit path")
    require(BASELINE_AUDIT_PATH.exists(), "TRANSITION_GATE baseline integrity audit file is missing")
    require(str(from_experiment) in status and str(to_candidate) in status, "STATUS.md must expose both sides of the transition gate")

if current_state == "OWNER_REQUIRED":
    require(bool(state.get("owner_required_reason")), "OWNER_REQUIRED must record a reason")

required_agent_markers = [
    "AUTONOMOUS_RESEARCH_PROGRAM_GOVERNANCE_001.md",
    "AUTONOMOUS_RESEARCH_PROGRAM_POLICY_001.json",
    "AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json",
    "BASELINE_INTEGRITY_AUDIT_AUTONOMY_001.md",
    "AMBIGUOUS AUTHORITY",
    "OWNER_REQUIRED",
]
for marker in required_agent_markers:
    require(marker in agents, f"AGENTS.md missing autonomous-governance marker: {marker}")

required_status_markers = [
    "AUTONOMOUS RESEARCH PROGRAM",
    "ST2-EXP-004",
    "ST2-EXP-014",
]
for marker in required_status_markers:
    require(marker in status, f"STATUS.md missing autonomous-governance marker: {marker}")

if errors:
    print("BOMA autonomous research-program audit: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("BOMA autonomous research-program audit: PASS")
print(f"state={current_state}")
print(f"active_program_id={state.get('active_program_id')}")
print(f"queue_size={len(state.get('authorized_experiment_queue', []))}")
print(f"queue_cursor={state.get('queue_cursor')}")
print(f"routine_merge_authorized={state.get('routine_merge_authorized')}")
