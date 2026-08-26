#!/usr/bin/env python3
"""Exact-head guard for autonomy-created BOMA pull requests."""
from __future__ import annotations

import json
import pathlib
import sys

from core import (
    POLICY,
    PROGRAM_MANIFEST,
    RESEARCH_STATE,
    ROOT,
    accepted_control_paths,
    git,
    load_json,
    run,
    sanitized_env,
    utc_now,
)

OUT = pathlib.Path("/tmp/boma-autonomy-guard.json")


def fail(message: str, evidence: dict) -> int:
    evidence["passed"] = False
    evidence.setdefault("errors", []).append(message)
    evidence["completed_at"] = utc_now()
    OUT.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"BOMA autonomy exact-head guard: FAIL — {message}", file=sys.stderr)
    return 1


def main() -> int:
    state = load_json(RESEARCH_STATE)
    manifest = load_json(PROGRAM_MANIFEST)
    policy = load_json(POLICY)
    evidence: dict = {
        "schema": "BOMA-AUTONOMY-GUARD-EVIDENCE-001",
        "head": git("rev-parse", "HEAD"),
        "research_state": state.get("state"),
        "active_experiment": state.get("active_experiment"),
        "checks": [],
        "errors": [],
    }

    if state.get("active_program_id") != manifest.get("program_id"):
        return fail("active program/manifest mismatch", evidence)
    if state.get("authorized_experiment_queue") != manifest.get("queue_order"):
        return fail("queue mismatch", evidence)

    active = state.get("active_experiment")
    frozen_rel = state.get("active_frozen_plan")
    frozen_machine_rel = state.get("active_frozen_plan_machine")
    frozen_sha = state.get("active_frozen_plan_sha")
    baseline = state.get("active_experiment_frozen_reference_sha")

    if active is not None:
        if not all(isinstance(x, str) and x for x in (frozen_rel, frozen_machine_rel, frozen_sha, baseline)):
            return fail("active experiment lacks frozen plan/reference metadata", evidence)
        plan_path = ROOT / str(frozen_rel)
        if not plan_path.is_file():
            return fail(f"frozen plan missing: {frozen_rel}", evidence)

        ancestor = run(["git", "merge-base", "--is-ancestor", str(frozen_sha), "HEAD"])
        if ancestor["exit_code"] != 0:
            return fail("frozen Plan commit is not an ancestor of exact head", evidence)

        frozen_diff = run([
            "git", "diff", "--exit-code", str(frozen_sha), "HEAD", "--",
            str(frozen_rel), str(frozen_machine_rel)
        ])
        if frozen_diff["exit_code"] != 0:
            return fail("Frozen Plan or machine Plan changed after freeze", evidence)
        evidence["checks"].append({"name": "frozen_plan_immutable", "passed": True})

        controller_owned = {
            "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json",
            "LAB/PDSA/STATUS.md",
            "LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md",
            "AGENTS.md",
        }
        control_paths = sorted(
            p for p in accepted_control_paths()
            if p not in controller_owned and (ROOT / p).exists()
        )
        if control_paths:
            controls = run(
                ["git", "diff", "--exit-code", str(baseline), "HEAD", "--", *control_paths],
                timeout=300,
            )
            if controls["exit_code"] != 0:
                return fail("accepted/protected control changed on research branch", evidence)
        evidence["checks"].append({"name": "accepted_controls_immutable", "passed": True})

        machine_plan = ROOT / "LAB/PDSA/autonomy" / str(active) / "FROZEN_PLAN.json"
        if not machine_plan.is_file():
            return fail(f"machine Frozen Plan missing: {machine_plan.relative_to(ROOT)}", evidence)
        plan = load_json(machine_plan)
        if plan.get("experiment_id") != active:
            return fail("machine Frozen Plan experiment id mismatch", evidence)
        commands = plan.get("verification_commands")
        if not isinstance(commands, list):
            return fail("Frozen Plan verification_commands must be an array", evidence)
        max_commands = int(policy.get("max_verification_commands", 20))
        if len(commands) > max_commands:
            return fail("too many Frozen Plan verification commands", evidence)

        command_evidence = []
        env = sanitized_env()
        for command in commands:
            if not isinstance(command, str) or not command.strip():
                return fail("invalid empty/non-string verification command", evidence)
            result = run(
                ["bash", "-lc", command],
                timeout=1200,
                env=env,
            )
            command_evidence.append(result)
            if result["exit_code"] != 0:
                evidence["verification_commands"] = command_evidence
                return fail(f"verification command failed: {command}", evidence)
        evidence["verification_commands"] = command_evidence
        tamper = run([
            "git", "diff", "--exit-code", "HEAD", "--",
            *sorted(accepted_control_paths()),
            str(frozen_rel), str(frozen_machine_rel),
            ".autonomy", "scripts/boma_autonomy", "tests/boma_autonomy"
        ], timeout=300)
        if tamper["exit_code"] != 0:
            return fail("verification commands modified protected/control-plane files", evidence)
        evidence["checks"].append({"name": "frozen_plan_verification_commands", "passed": True})

    evidence["passed"] = True
    evidence["completed_at"] = utc_now()
    OUT.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print("BOMA autonomy exact-head guard: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
