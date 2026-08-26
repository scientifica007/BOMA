#!/usr/bin/env python3
"""Autonomous BOMA research controller.

The controller runs from main, creates/continues deterministic autonomy branches,
uses pull-request exact-head checks as gates, and never performs research writes
directly on main.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import re
import shutil
import sys
from typing import Any

from core import (
    AGENTS,
    EXP_STATE,
    METRICS,
    POLICY,
    PROGRAM_MANIFEST,
    REGISTER,
    RESEARCH_STATE,
    ROOT,
    STATUS,
    GovernanceError,
    accepted_control_paths,
    assert_executor_path_allowed,
    current_head,
    experiment_record,
    git,
    load_json,
    run,
    sanitized_env,
    save_json,
    upsert_runtime_block,
    utc_now,
)
from provider import AIProvider

AUTONOMY_EVIDENCE = ROOT / "LAB/PDSA/autonomy"
EXPERIMENTS = ROOT / "LAB/PDSA/experiments"

CORE_CONTEXT = [
    "LAB/PDSA/AUTONOMY_EXPERIMENT_PROTOCOL_001.md",
    "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_GOVERNANCE_001.md",
    "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_POLICY_001.json",
    "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json",
    "LAB/PDSA/RESEARCH_PROGRAM_ST2_RP_001_R_C_COMPOSITIONALITY_MINIMALITY.md",
    "LAB/PDSA/ST2_RP_001_PROGRAM_MANIFEST_001.json",
    "LAB/PDSA/STATUS.md",
    "LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md",
    "AGENTS.md",
    "LAB/00_ARCHITECTURE/C_R_DEPENDENCY_CONTRACT.md",
    "LAB/00_ARCHITECTURE/CLAIM_REGISTRY.md",
]


def role_system(role: str) -> str:
    common = """You are one logical role inside the active BOMA autonomous mathematical-research experiment.
Return JSON only. Respect the existing owner-authorized ST2-RP-001 program exactly.
Do not ask a human to choose mathematics that is already inside the authorized program.
Do not change SELECTS, accepted exports, acceptance contracts, canonical producers,
the authorized queue, or a Frozen Plan after Do. If a required action exceeds authority,
return OWNER_REQUIRED explicitly. A research PASS is not an acceptance promotion.
Formal proof ancestry is not automatically mathematical necessity. Preserve failure provenance.
Never request, reveal, or write secrets.
"""
    roles = {
        "transition_auditor": """Role: INDEPENDENT TRANSITION-GATE AUDITOR.
Evaluate only the declared transition prerequisites from exact repository evidence.
Return AUTO_CONTINUE only if every declared prerequisite remains satisfied and no
sequence-critical insertion/reordering is required. Otherwise return OWNER_REQUIRED.
""",
        "planner": """Role: EXPERIMENT PLANNER.
Create one immutable, bounded PDSA Plan for the exact queued experiment and its single
authorized changed factor. The Plan must include deterministic verification commands and
explicit success/informative-fail criteria. Do not execute.
""",
        "reviewer": """Role: INDEPENDENT PLAN REVIEWER.
APPROVE only if the Plan changes exactly one authorized scientific factor, preserves all
controls, is mathematically meaningful, has deterministic verification, and does not smuggle
new assumptions, selectors, acceptance changes, or queue changes. Otherwise REVISE.
""",
        "executor": """Role: FROZEN-PLAN EXECUTOR.
Execute only the supplied immutable Plan. Return complete file write/delete operations.
Do not edit the control plane, current-state files, accepted/protected controls, or Frozen Plan.
Do not repair an unexpected defect by changing the Plan or scientific factor.
""",
        "recovery_analyst": """Role: TECHNICAL RECOVERY ANALYST.
Analyze verification/CI failures under the immutable Frozen Plan. You may propose file
operations only for technical/formalization/harness defects that leave the Plan, scientific
factor, assumptions, Claim cone, accepted controls, and success criteria unchanged.
If recovery would cross those boundaries, return OWNER_REQUIRED.
""",
        "study_analyst": """Role: STUDY ANALYST.
Compare Frozen-Plan predictions with exact Do and CI evidence. Classify result as PASS,
INFORMATIVE_FAIL, or OWNER_REQUIRED. Separate mathematical findings from proof/harness
artifacts and state all deviations explicitly.
""",
        "act_analyst": """Role: ACT ANALYST.
Convert Study evidence into bounded durable program knowledge. Assess whether the next
preauthorized transition prerequisites remain meaningful without deciding that next gate.
Do not promote research evidence into acceptance.
""",
        "closure_auditor": """Role: INDEPENDENT LIFECYCLE-CLOSURE AUDITOR.
Authorize CLOSE only when Frozen Plan is unchanged, evidence is exact and sufficient,
Study/Act are complete, no unresolved deviation exists, and no out-of-scope authority is
required. Otherwise return OWNER_REQUIRED.
""",
        "program_synthesizer": """Role: INDEPENDENT PROGRAM SYNTHESIZER.
Synthesize the completed ST2-RP-001 evidence after ST2-EXP-017. Do not authorize a fifth
experiment or a new program. Return PROGRAM_COMPLETE only if the four authorized lifecycle
records and program-level synthesis obligations are complete; otherwise OWNER_REQUIRED.
""",
    }
    return common + roles[role]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def read_text(rel: str, limit: int = 14000) -> str:
    path = ROOT / rel
    if not path.is_file():
        return f"[missing: {rel}]"
    try:
        return path.read_text(encoding="utf-8")[:limit]
    except UnicodeDecodeError:
        return f"[binary/unreadable: {rel}]"


def file_tree(limit: int = 500) -> str:
    out: list[str] = []
    for base, dirs, names in os.walk(ROOT):
        base_path = pathlib.Path(base)
        rel_base = base_path.relative_to(ROOT).as_posix()
        dirs[:] = [d for d in dirs if d not in {".git", ".lake", "node_modules", ".venv", "__pycache__"}]
        if rel_base.startswith(".git"):
            continue
        for name in sorted(names):
            rel = (base_path / name).relative_to(ROOT).as_posix()
            if rel.startswith(".autonomy/"):
                continue
            out.append(rel)
            if len(out) >= limit:
                out.append("... tree truncated ...")
                return "\n".join(out)
    return "\n".join(out)


def context(extra: list[str] | None = None) -> str:
    policy = load_json(POLICY)
    sections: list[str] = []
    seen: set[str] = set()
    for rel in CORE_CONTEXT + (extra or []):
        if rel in seen:
            continue
        seen.add(rel)
        sections.append(f"## FILE {rel}\n{read_text(rel)}")
    sections.append("## REPOSITORY TREE\n" + file_tree())
    return "\n\n".join(sections)[: int(policy.get("max_context_characters", 42000))]


def gh(args: list[str], *, check: bool = True) -> dict[str, Any]:
    env = os.environ.copy()
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if not token:
        raise GovernanceError("GH_TOKEN/GITHUB_TOKEN unavailable to autonomous controller")
    env["GH_TOKEN"] = token
    return run(["gh", *args], env=env, timeout=300, check=check)


def gh_json(args: list[str]) -> Any:
    result = gh(args, check=False)
    if result["exit_code"] != 0:
        raise GovernanceError(
            f"gh command failed: {' '.join(args)}\n{result['stdout']}\n{result['stderr']}"
        )
    try:
        return json.loads(result["stdout"] or "null")
    except json.JSONDecodeError as exc:
        raise GovernanceError(f"invalid gh JSON: {result['stdout'][:1000]}") from exc


def return_main() -> str:
    git("fetch", "origin", "main")
    git("checkout", "-B", "main", "origin/main")
    return current_head()


def branch_exists(branch: str) -> bool:
    result = run(["git", "ls-remote", "--exit-code", "--heads", "origin", branch], timeout=120)
    return result["exit_code"] == 0


def checkout_branch(branch: str, *, create: bool = False) -> None:
    return_main()
    if create:
        if branch_exists(branch):
            raise GovernanceError(f"branch already exists: {branch}")
        git("checkout", "-b", branch)
    else:
        git("fetch", "origin", f"{branch}:refs/remotes/origin/{branch}")
        git("checkout", "-B", branch, f"origin/{branch}")


def push_current(branch: str) -> None:
    git("push", "origin", f"HEAD:refs/heads/{branch}")


def commit_all(message: str) -> str:
    assert_working_tree_safe()
    git("add", "-A")
    staged = run(["git", "diff", "--cached", "--quiet"])
    if staged["exit_code"] == 0:
        return current_head()
    git("commit", "-m", message)
    return current_head()


def assert_working_tree_safe() -> None:
    status = git("status", "--porcelain")
    if not status:
        return
    policy = load_json(POLICY)
    protected_prefixes = [str(x) for x in policy.get("protected_prefixes", [])]
    protected_exact = {str(x) for x in policy.get("protected_exact_paths", [])} | accepted_control_paths()
    # Controller-owned state/status files are deliberately allowed.
    controller_owned = {
        "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json",
        "LAB/PDSA/STATUS.md",
        "LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md",
        "AGENTS.md",
    }
    for line in status.splitlines():
        raw = line[3:] if len(line) >= 4 else line
        if " -> " in raw:
            raw = raw.split(" -> ", 1)[1]
        rel = raw.strip()
        if rel.startswith(".autonomy/"):
            raise GovernanceError(f"research branch attempted control-plane change: {rel}")
        if rel.startswith("scripts/boma_autonomy/") or rel.startswith("tests/boma_autonomy/"):
            raise GovernanceError(f"research branch attempted runtime-instrument change: {rel}")
        if rel in protected_exact and rel not in controller_owned:
            raise GovernanceError(f"research branch changed protected accepted/control path: {rel}")
        if any(rel.startswith(prefix) for prefix in protected_prefixes) and rel not in controller_owned:
            # LAB/PDSA/autonomy is controller-owned evidence, not executor-owned.
            if rel.startswith("LAB/PDSA/autonomy/"):
                continue
            raise GovernanceError(f"research branch changed protected prefix: {rel}")


def pr_for_branch(branch: str) -> dict[str, Any] | None:
    data = gh_json([
        "pr", "list", "--head", branch, "--state", "all", "--limit", "5",
        "--json", "number,state,mergedAt,headRefOid,url,title"
    ])
    if not isinstance(data, list) or not data:
        return None
    return data[0]


def ensure_pr(branch: str, title: str, body: str) -> dict[str, Any]:
    existing = pr_for_branch(branch)
    if existing and existing.get("state") == "OPEN":
        return existing
    if existing and existing.get("mergedAt"):
        return existing
    gh(["pr", "create", "--base", "main", "--head", branch, "--title", title, "--body", body])
    created = pr_for_branch(branch)
    if not created:
        raise GovernanceError(f"PR creation not observable for {branch}")
    return created


def pr_check_state(number: int) -> tuple[str, list[dict[str, Any]]]:
    data = gh_json(["pr", "view", str(number), "--json", "statusCheckRollup,headRefOid,state,mergeable"])
    checks = data.get("statusCheckRollup") if isinstance(data, dict) else None
    if not isinstance(checks, list) or not checks:
        return "PENDING", []
    normalized: list[dict[str, Any]] = []
    any_pending = False
    any_fail = False
    for item in checks:
        if not isinstance(item, dict):
            continue
        status = str(item.get("status") or item.get("state") or "").upper()
        conclusion = str(item.get("conclusion") or item.get("state") or "").upper()
        name = item.get("name") or item.get("context") or item.get("workflowName") or "unnamed"
        normalized.append({
            "name": name,
            "status": status,
            "conclusion": conclusion,
            "detailsUrl": item.get("detailsUrl"),
        })
        if status in {"QUEUED", "IN_PROGRESS", "PENDING", "EXPECTED"} or conclusion in {"PENDING", "EXPECTED", ""}:
            if status != "COMPLETED":
                any_pending = True
        if conclusion in {"FAILURE", "ERROR", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "STALE"} or status in {"FAILURE", "ERROR"}:
            any_fail = True
    if any_fail:
        return "FAIL", normalized
    if any_pending:
        return "PENDING", normalized
    return "PASS", normalized


def failed_logs(branch: str, limit: int = 24000) -> str:
    head = git("rev-parse", f"origin/{branch}") if branch_exists(branch) else ""
    data = gh_json([
        "run", "list", "--branch", branch, "--limit", "12",
        "--json", "databaseId,status,conclusion,workflowName,headSha"
    ])
    parts: list[str] = []
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            if head and item.get("headSha") != head:
                continue
            if str(item.get("conclusion")).lower() not in {"failure", "cancelled", "timed_out", "action_required"}:
                continue
            run_id = item.get("databaseId")
            if run_id:
                logs = gh(["run", "view", str(run_id), "--log-failed"], check=False)
                parts.append(
                    f"## {item.get('workflowName')} / run {run_id}\n"
                    + str(logs.get("stdout", ""))
                    + str(logs.get("stderr", ""))
                )
    return "\n\n".join(parts)[:limit]


def assert_main_drift_control_only(branch: str) -> None:
    git("fetch", "origin", "main")
    git("fetch", "origin", f"{branch}:refs/remotes/origin/{branch}")
    base = git("merge-base", "origin/main", f"origin/{branch}")
    changed = git("diff", "--name-only", base, "origin/main")
    invalid = [
        rel for rel in changed.splitlines()
        if rel.strip() and not rel.strip().startswith(".autonomy/")
    ]
    if invalid:
        raise GovernanceError(
            "BASELINE_INVALIDATED_BY_MAIN_CHANGE: non-control-plane main drift while "
            f"{branch} was open: {invalid}"
        )


def merge_pr(number: int, branch: str) -> None:
    assert_main_drift_control_only(branch)
    gh(["pr", "merge", str(number), "--merge", "--delete-branch=false"])


def write_record(path: pathlib.Path, data: dict[str, Any]) -> None:
    if path.exists():
        raise GovernanceError(f"immutable evidence already exists: {path.relative_to(ROOT)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    save_json(path, data)


def update_research_state(state: dict[str, Any], *, note: str) -> None:
    save_json(RESEARCH_STATE, state)
    for path in (STATUS, AGENTS, REGISTER):
        upsert_runtime_block(path, state, note=note)


def apply_operations(operations: Any) -> list[dict[str, str]]:
    if not isinstance(operations, list):
        raise GovernanceError("AI operations must be an array")
    policy = load_json(POLICY)
    if len(operations) > int(policy.get("max_executor_operations", 48)):
        raise GovernanceError("AI returned too many file operations")
    validated: list[tuple[str, str, pathlib.Path, str | None]] = []
    originals: dict[str, bytes | None] = {}
    for op in operations:
        if not isinstance(op, dict):
            raise GovernanceError("operation must be object")
        action = op.get("action")
        rel = op.get("path")
        if action not in {"write", "delete"} or not isinstance(rel, str):
            raise GovernanceError(f"invalid operation: {op!r}")
        target = assert_executor_path_allowed(rel)
        content = op.get("content")
        if action == "write" and not isinstance(content, str):
            raise GovernanceError(f"write requires complete string content: {rel}")
        if rel not in originals:
            originals[rel] = target.read_bytes() if target.exists() and target.is_file() else None
        validated.append((action, rel, target, content if isinstance(content, str) else None))
    applied: list[dict[str, str]] = []
    try:
        for action, rel, target, content in validated:
            if action == "write":
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content or "", encoding="utf-8")
            else:
                if target.exists():
                    if not target.is_file():
                        raise GovernanceError(f"cannot delete directory: {rel}")
                    target.unlink()
            applied.append({"action": action, "path": rel})
        return applied
    except Exception:
        for rel, content in originals.items():
            target = ROOT / rel
            if content is None:
                if target.exists() and target.is_file():
                    target.unlink()
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
        raise


def run_plan_commands(plan: dict[str, Any]) -> dict[str, Any]:
    commands = plan.get("verification_commands")
    if not isinstance(commands, list):
        raise GovernanceError("Frozen Plan lacks verification_commands array")
    max_commands = int(load_json(POLICY).get("max_verification_commands", 20))
    if len(commands) > max_commands:
        raise GovernanceError("Frozen Plan has too many verification commands")
    results = []
    env = sanitized_env()
    for command in commands:
        if not isinstance(command, str) or not command.strip():
            raise GovernanceError("invalid verification command")
        result = run(["bash", "-lc", command], env=env, timeout=1200)
        results.append(result)
    governance = run([sys.executable, "LAB/PDSA/tools/autonomous_research_program_audit.py"], timeout=240)
    architecture = run([sys.executable, "LAB/00_ARCHITECTURE/tools/architecture_consistency_audit.py"], timeout=360)
    results.extend([governance, architecture])

    state = load_json(RESEARCH_STATE)
    protected = sorted(accepted_control_paths())
    for extra in (
        "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json",
        "LAB/PDSA/STATUS.md",
        "LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md",
        "AGENTS.md",
        str(state.get("active_frozen_plan") or ""),
        str(state.get("active_frozen_plan_machine") or ""),
    ):
        if extra and extra not in protected:
            protected.append(extra)
    tamper = run([
        "git", "diff", "--exit-code", "HEAD", "--",
        *protected, ".autonomy", "scripts/boma_autonomy", "tests/boma_autonomy"
    ], timeout=300)
    if tamper["exit_code"] != 0:
        results.append({
            "command": ["protected-working-tree-tamper-check"],
            "exit_code": 99,
            "stdout": tamper["stdout"],
            "stderr": "verification commands modified protected/control-plane files",
        })

    return {
        "passed": all(int(item["exit_code"]) == 0 for item in results),
        "checks": results,
        "verified_at": utc_now(),
        "head_before_commit": current_head(),
    }


def assert_frozen(branch_state: dict[str, Any], exp: str) -> dict[str, Any]:
    frozen_sha = branch_state.get("active_frozen_plan_sha")
    human_rel = branch_state.get("active_frozen_plan")
    machine_rel = branch_state.get("active_frozen_plan_machine")
    if not all(isinstance(x, str) and x for x in (frozen_sha, human_rel, machine_rel)):
        raise GovernanceError("active experiment lacks complete frozen-plan metadata")
    if run(["git", "merge-base", "--is-ancestor", str(frozen_sha), "HEAD"])["exit_code"] != 0:
        raise GovernanceError("Frozen Plan commit is not ancestor of branch head")
    for rel in (human_rel, machine_rel):
        if run(["git", "diff", "--exit-code", str(frozen_sha), "HEAD", "--", str(rel)])["exit_code"] != 0:
            raise GovernanceError(f"Frozen Plan mutated after Do: {rel}")
    plan = load_json(ROOT / str(machine_rel))
    if plan.get("experiment_id") != exp:
        raise GovernanceError("machine Frozen Plan experiment mismatch")
    return plan


def transition_handler(ai: AIProvider, metrics: dict[str, Any]) -> str:
    main_state = load_json(RESEARCH_STATE)
    transition = main_state.get("program_transition", {})
    src = str(transition.get("from_experiment") or "")
    dst = str(transition.get("to_candidate") or "")
    if not src or not dst:
        raise GovernanceError("TRANSITION_GATE lacks source/candidate")
    branch = f"autonomy/transition-{slug(src)}-to-{slug(dst)}"

    if branch_exists(branch):
        pr = pr_for_branch(branch)
        if not pr:
            raise GovernanceError(f"transition branch exists without PR: {branch}")
        if pr.get("mergedAt"):
            return_main()
            return "CONTINUE"
        state, checks = pr_check_state(int(pr["number"]))
        if state == "PENDING":
            return "WAITING_CI"
        if state == "FAIL":
            return recover_nonplan_branch(ai, metrics, branch, pr, checks, kind="transition")
        merge_pr(int(pr["number"]), branch)
        metrics["transition_decisions"] = int(metrics.get("transition_decisions", 0)) + 1
        return_main()
        return "CONTINUE"

    manifest = load_json(PROGRAM_MANIFEST)
    src_rec = experiment_record(manifest, src)
    extra = [
        "LAB/PDSA/BASELINE_INTEGRITY_AUDIT_AUTONOMY_001.md",
        f"LAB/PDSA/experiments/{src}_FINAL_STUDY_ACT_001.md",
        f"LAB/PDSA/experiments/{src}_LIFECYCLE_CLOSURE_001.md",
        f"LAB/PDSA/experiments/{src}_AUTONOMOUS_LIFECYCLE_CLOSURE_001.md",
        f"LAB/PDSA/autonomy/{src}/FINAL_STUDY_001.json",
        f"LAB/PDSA/autonomy/{src}/FINAL_ACT_001.json",
        f"LAB/PDSA/autonomy/{src}/CLOSURE_AUDIT_001.json",
        f"LAB/PDSA/autonomy/{src}/POSTMERGE_SYNC_001.json",
    ]
    prompt = f"""Evaluate only the declared {src} → {dst} transition gate.

SOURCE MANIFEST RECORD:
{json.dumps(src_rec, ensure_ascii=False, indent=2)}

CURRENT TRANSITION STATE:
{json.dumps(main_state, ensure_ascii=False, indent=2)}

REPOSITORY EVIDENCE:
{context(extra)}

Return:
{{
 "decision":"AUTO_CONTINUE"|"OWNER_REQUIRED",
 "prerequisite_assessment":[{{"requirement":"...","satisfied":true|false,"evidence":"..."}}],
 "sequence_critical_prerequisite_discovered":false,
 "rationale":"...",
 "owner_required_reason":null|"..."
}}
"""
    decision = ai.ask_json("transition_auditor", role_system("transition_auditor"), prompt, max_tokens=3000)
    if decision.get("decision") not in {"AUTO_CONTINUE", "OWNER_REQUIRED"}:
        raise GovernanceError(f"invalid transition decision: {decision!r}")

    checkout_branch(branch, create=True)
    record_path = EXPERIMENTS / f"{src}_TO_{dst}_AUTONOMOUS_TRANSITION_001.json"
    write_record(record_path, {
        "schema": "BOMA-AUTONOMOUS-TRANSITION-RECORD-001",
        "from": src,
        "to": dst,
        "evaluated_from_main": main_state.get("synchronized_main_sha") or git("rev-parse", "main"),
        "decision": decision,
        "recorded_at": utc_now(),
    })
    new_state = load_json(RESEARCH_STATE)
    if decision["decision"] == "AUTO_CONTINUE":
        queue = new_state["authorized_experiment_queue"]
        new_state["state"] = "PREPARING_EXPERIMENT"
        new_state["queue_cursor"] = queue.index(dst)
        new_state["active_experiment"] = None
        new_state["active_experiment_branch"] = None
        new_state["active_frozen_plan"] = None
        new_state["active_frozen_plan_machine"] = None
        new_state["active_frozen_plan_sha"] = None
        new_state["active_experiment_frozen_reference_sha"] = None
        new_state["owner_required_reason"] = None
        new_state["program_transition"]["transition_decision_recorded"] = True
        new_state["program_transition"]["last_transition_decision"] = "AUTO_CONTINUE"
        frontier = new_state["current_stage_two_frontier"]
        frontier["next_experiment"] = dst
        frontier["next_experiment_status"] = "OWNER_AUTHORIZED / TRANSITION_PASSED / NOT_STARTED"
        frontier["activation_authorized_by_this_state"] = True
        new_state["next_legal_action"] = f"CREATE_INDEPENDENT_{dst}_BRANCH_AND_FREEZE_PLAN_BEFORE_DO"
        note = f"Autonomous transition gate {src}→{dst}: AUTO_CONTINUE; {dst} not started."
    else:
        reason = decision.get("owner_required_reason") or decision.get("rationale") or "transition gate requires owner"
        new_state["state"] = "OWNER_REQUIRED"
        new_state["owner_required_reason"] = str(reason)
        new_state["program_transition"]["transition_decision_recorded"] = True
        new_state["program_transition"]["last_transition_decision"] = "OWNER_REQUIRED"
        new_state["next_legal_action"] = "STOP / OWNER_REQUIRED"
        metrics["owner_required_stops"] = int(metrics.get("owner_required_stops", 0)) + 1
        note = f"Autonomous transition gate {src}→{dst}: OWNER_REQUIRED."
    update_research_state(new_state, note=note)
    commit_all(f"autonomy: record {src} to {dst} transition gate")
    push_current(branch)
    ensure_pr(
        branch,
        f"Autonomy: evaluate {src} → {dst} transition",
        "Autonomous transition-gate record under the already owner-authorized ST2-RP-001 program. "
        "No new queue authority, acceptance promotion, or mathematical implementation is introduced.",
    )
    return_main()
    return "WAITING_CI"


def render_plan_md(plan: dict[str, Any]) -> str:
    return (
        f"# {plan['experiment_id']} — Autonomous Frozen PDSA Plan\n\n"
        f"**Research question:** {plan.get('research_question','')}  \n"
        f"**SMART objective:** {plan.get('smart_objective','')}  \n"
        f"**Single changed factor:** `{plan.get('single_changed_factor','')}`\n\n"
        "## Fixed controls\n\n"
        + "\n".join(f"- `{x}`" for x in plan.get("fixed_controls", []))
        + "\n\n## Affected cone\n\n"
        + "\n".join(f"- `{x}`" for x in plan.get("affected_cone", []))
        + "\n\n## Plan steps\n\n"
        + "\n".join(f"{i+1}. {x}" for i, x in enumerate(plan.get("plan_steps", [])))
        + "\n\n## Success / informative-fail criteria\n\n"
        + "\n".join(f"- {x}" for x in plan.get("success_criteria", []))
        + "\n\n## Deterministic verification commands\n\n```text\n"
        + "\n".join(plan.get("verification_commands", []))
        + "\n```\n\n## Recovery envelope\n\n"
        + "\n".join(f"- {x}" for x in plan.get("allowed_recovery_envelope", []))
        + "\n\nThis Plan is immutable after its freeze commit. A later technical recovery may "
          "not change this file, its machine JSON twin, the single changed factor, "
          "assumptions, success criteria, or Claim cone.\n"
    )


def planning_handler(ai: AIProvider, metrics: dict[str, Any]) -> str:
    main_state = load_json(RESEARCH_STATE)
    queue = main_state.get("authorized_experiment_queue", [])
    cursor = int(main_state.get("queue_cursor", -1))
    if cursor < 0 or cursor >= len(queue):
        raise GovernanceError("invalid queue cursor in PREPARING_EXPERIMENT")
    exp = str(queue[cursor])
    branch = f"autonomy/{slug(exp)}"

    if branch_exists(branch):
        checkout_branch(branch)
        branch_state = load_json(RESEARCH_STATE)
        stage = branch_state.get("state")
        if branch_state.get("active_experiment") not in {None, exp}:
            raise GovernanceError("existing experiment branch has mismatched active experiment")
        return branch_stage_handler(ai, metrics, branch, exp, branch_state)

    manifest = load_json(PROGRAM_MANIFEST)
    rec = experiment_record(manifest, exp)
    base_context = context()
    revision_notes: list[str] = []
    approved: dict[str, Any] | None = None
    review_history: list[dict[str, Any]] = []
    max_revisions = int(load_json(POLICY).get("max_plan_revisions", 2))

    for attempt in range(max_revisions + 1):
        plan = ai.ask_json(
            "planner",
            role_system("planner"),
            f"""Prepare the immutable Frozen Plan for the exact queued experiment.

MANIFEST EXPERIMENT RECORD:
{json.dumps(rec, ensure_ascii=False, indent=2)}

PRIOR REVIEW DEFECTS:
{json.dumps(revision_notes, ensure_ascii=False)}

REPOSITORY CONTEXT:
{base_context}

Return exactly these keys:
experiment_id, research_question, smart_objective, single_changed_factor,
fixed_controls, affected_cone, plan_steps, success_criteria,
verification_commands, allowed_recovery_envelope, expected_files.
verification_commands must be deterministic shell commands that return zero when
the planned PASS or planned informative-fail condition is correctly evidenced.
""",
            max_tokens=4500,
        )
        if plan.get("experiment_id") != exp:
            revision_notes = [f"experiment_id must equal {exp}"]
            continue
        if plan.get("single_changed_factor") != rec.get("single_changed_factor"):
            revision_notes = ["single_changed_factor must exactly match the authorized manifest literal"]
            continue
        plan_controls = plan.get("fixed_controls")
        if not isinstance(plan_controls, list) or not set(map(str, rec.get("fixed_controls", []))).issubset(set(map(str, plan_controls))):
            revision_notes = ["fixed_controls must include every control declared by the authorized manifest"]
            continue
        for key in ("fixed_controls", "affected_cone", "plan_steps", "success_criteria", "verification_commands", "allowed_recovery_envelope"):
            if not isinstance(plan.get(key), list) or not plan.get(key):
                revision_notes = [f"{key} must be a non-empty array"]
                break
        else:
            review = ai.ask_json(
                "reviewer",
                role_system("reviewer"),
                f"""Review this proposed Plan against the exact manifest authority.

MANIFEST:
{json.dumps(rec, ensure_ascii=False, indent=2)}

PROPOSED PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

Return:
{{"decision":"APPROVE"|"REVISE","defects":[],"scope_assessment":"...","verification_assessment":"..."}}.
""",
                max_tokens=2600,
            )
            review_history.append(review)
            if review.get("decision") == "APPROVE":
                approved = plan
                break
            if review.get("decision") != "REVISE":
                raise GovernanceError(f"invalid reviewer decision: {review!r}")
            defects = review.get("defects", [])
            revision_notes = [str(x) for x in defects] if isinstance(defects, list) else [str(defects)]
            metrics["plan_revisions"] = int(metrics.get("plan_revisions", 0)) + 1
            continue

    if approved is None:
        raise GovernanceError(f"autonomous Plan failed review for {exp}: {review_history!r}")

    baseline = current_head()
    checkout_branch(branch, create=True)
    plan_dir = AUTONOMY_EVIDENCE / exp
    plan_dir.mkdir(parents=True, exist_ok=True)
    machine_path = plan_dir / "FROZEN_PLAN.json"
    human_rel = f"LAB/PDSA/PDSA-{exp}_AUTONOMOUS.md"
    human_path = ROOT / human_rel
    origin_path = plan_dir / "BRANCH_ORIGIN_001.json"
    save_json(machine_path, approved)
    human_path.write_text(render_plan_md(approved), encoding="utf-8")
    save_json(origin_path, {
        "schema": "BOMA-AUTONOMOUS-BRANCH-ORIGIN-001",
        "experiment_id": exp,
        "origin_kind": rec.get("origin_kind"),
        "origin_id": rec.get("origin_id"),
        "single_changed_factor": rec.get("single_changed_factor"),
        "frozen_reference_main_sha": baseline,
        "branch": branch,
        "created_at": utc_now(),
    })

    git("add", str(machine_path.relative_to(ROOT)), human_rel, str(origin_path.relative_to(ROOT)))
    git("commit", "-m", f"autonomy: freeze {exp} Plan")
    frozen_commit = current_head()

    state = load_json(RESEARCH_STATE)
    state["state"] = "PLAN_FROZEN"
    state["active_experiment"] = exp
    state["active_experiment_branch"] = branch
    state["active_frozen_plan"] = human_rel
    state["active_frozen_plan_machine"] = str(machine_path.relative_to(ROOT))
    state["active_frozen_plan_sha"] = frozen_commit
    state["active_experiment_frozen_reference_sha"] = baseline
    state["active_experiment_origin_record"] = str(origin_path.relative_to(ROOT))
    state["owner_required_reason"] = None
    frontier = state["current_stage_two_frontier"]
    frontier["active_experiment"] = exp
    frontier["active_experiment_status"] = "PLAN_FROZEN / DO_NOT_MUTATE_PLAN"
    frontier["next_experiment"] = exp
    frontier["next_experiment_status"] = "ACTIVE / PLAN_FROZEN"
    state["next_legal_action"] = f"EXECUTE_IMMUTABLE_{exp}_FROZEN_PLAN"
    update_research_state(state, note=f"{exp} autonomous Plan frozen at {frozen_commit}; Do not yet executed.")
    commit_all(f"autonomy: record {exp} frozen Plan authority")
    push_current(branch)
    ensure_pr(
        branch,
        f"{exp}: autonomous research lifecycle",
        f"Autonomous execution of already owner-authorized `{exp}` under `ST2-RP-001`. "
        f"Frozen Plan commit: `{frozen_commit}`. The PR remains open through Do, exact verification, Study/Act, and lifecycle closure.",
    )
    metrics["plans_frozen"] = int(metrics.get("plans_frozen", 0)) + 1
    return_main()
    return "CONTINUE"


def ask_executor(ai: AIProvider, plan: dict[str, Any], exp: str) -> dict[str, Any]:
    prompt = f"""Execute only this immutable Frozen Plan.

PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

REPOSITORY CONTEXT:
{context()}

Return one of:
{{"status":"NEED_CONTEXT","read_files":["path", ...]}}
or
{{"status":"EXECUTE","summary":"...","operations":[
{{"action":"write","path":"relative/path","content":"COMPLETE UTF-8 CONTENT"}},
{{"action":"delete","path":"relative/path"}}
],"deviations":[],"expected_evidence":[]}}.
"""
    response = ai.ask_json("executor", role_system("executor"), prompt, max_tokens=6500)
    if response.get("status") != "NEED_CONTEXT":
        return response
    requested = response.get("read_files")
    if not isinstance(requested, list):
        raise GovernanceError("NEED_CONTEXT requires read_files")
    limit = int(load_json(POLICY).get("max_executor_read_files", 18))
    clean = [
        str(rel) for rel in requested[:limit]
        if isinstance(rel, str) and (ROOT / rel).is_file() and not str(rel).startswith(".autonomy/")
    ]
    return ai.ask_json(
        "executor",
        role_system("executor"),
        f"""Execute the immutable Plan now. Requested files are included below.

PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

EXTENDED CONTEXT:
{context(clean)}

Return status EXECUTE with complete file operations, deviations, and expected_evidence.
""",
        max_tokens=7000,
    )


def branch_stage_handler(
    ai: AIProvider,
    metrics: dict[str, Any],
    branch: str,
    exp: str,
    state: dict[str, Any],
) -> str:
    stage = str(state.get("state"))
    if stage == "PLAN_FROZEN":
        return execute_do(ai, metrics, branch, exp, state)
    if stage in {"WAITING_CI", "RECOVERY_ALLOWED"}:
        return wait_or_recover(ai, metrics, branch, exp, state)
    if stage == "CLOSING":
        return close_when_exact(ai, metrics, branch, exp, state)
    if stage == "OWNER_REQUIRED":
        return_main()
        return "OWNER_REQUIRED"
    raise GovernanceError(f"unhandled branch research state {stage} for {exp}")


def execute_do(
    ai: AIProvider,
    metrics: dict[str, Any],
    branch: str,
    exp: str,
    state: dict[str, Any],
) -> str:
    plan = assert_frozen(state, exp)
    response = ask_executor(ai, plan, exp)
    if response.get("status") != "EXECUTE":
        raise GovernanceError(f"executor did not return EXECUTE: {response!r}")
    applied = apply_operations(response.get("operations"))
    assert_frozen(state, exp)
    verification = run_plan_commands(plan)
    evidence_dir = AUTONOMY_EVIDENCE / exp
    write_record(evidence_dir / "DO_EXECUTION_001.json", {
        "schema": "BOMA-AUTONOMOUS-DO-EVIDENCE-001",
        "experiment_id": exp,
        "executor_summary": response.get("summary"),
        "operations": applied,
        "deviations": response.get("deviations", []),
        "expected_evidence": response.get("expected_evidence", []),
        "verification": verification,
        "recorded_at": utc_now(),
    })
    state = load_json(RESEARCH_STATE)
    state["state"] = "WAITING_CI" if verification["passed"] else "RECOVERY_ALLOWED"
    state["active_work_head_before_ci_state_commit"] = current_head()
    state["waiting_on"] = "EXACT_PULL_REQUEST_CHECKS" if verification["passed"] else "AUTONOMOUS_TECHNICAL_RECOVERY"
    frontier = state["current_stage_two_frontier"]
    frontier["active_experiment_status"] = state["state"]
    state["next_legal_action"] = (
        "WAIT_FOR_EXACT_PR_CHECKS"
        if verification["passed"]
        else "DIAGNOSE_AND_RECOVER_WITHIN_IMMUTABLE_FROZEN_PLAN"
    )
    update_research_state(state, note=f"{exp} Do executed; local deterministic verification passed={verification['passed']}.")
    commit_all(f"autonomy: execute {exp} frozen Plan")
    push_current(branch)
    metrics["executor_runs"] = int(metrics.get("executor_runs", 0)) + 1
    if not verification["passed"]:
        metrics["verification_failures"] = int(metrics.get("verification_failures", 0)) + 1
    return_main()
    return "WAITING_CI" if verification["passed"] else "CONTINUE"


def wait_or_recover(
    ai: AIProvider,
    metrics: dict[str, Any],
    branch: str,
    exp: str,
    branch_state: dict[str, Any],
) -> str:
    pr = pr_for_branch(branch)
    if not pr or pr.get("state") != "OPEN":
        raise GovernanceError(f"active experiment branch lacks open PR: {branch}")
    check_state, checks = pr_check_state(int(pr["number"]))
    if branch_state.get("state") == "WAITING_CI" and check_state == "PASS":
        checkout_branch(branch)
        return study_act_close(ai, metrics, branch, exp, load_json(RESEARCH_STATE), checks)
    if check_state == "PENDING" and branch_state.get("state") == "WAITING_CI":
        return_main()
        return "WAITING_CI"
    return recover_experiment(ai, metrics, branch, exp, branch_state, pr, checks)


def recover_experiment(
    ai: AIProvider,
    metrics: dict[str, Any],
    branch: str,
    exp: str,
    branch_state: dict[str, Any],
    pr: dict[str, Any],
    checks: list[dict[str, Any]],
) -> str:
    checkout_branch(branch)
    plan = assert_frozen(load_json(RESEARCH_STATE), exp)
    evidence_dir = AUTONOMY_EVIDENCE / exp
    attempts = sorted(evidence_dir.glob("RECOVERY_*.json"))
    max_attempts = int(load_json(POLICY).get("max_recovery_attempts_per_head", 4))
    if len(attempts) >= max_attempts:
        state = load_json(RESEARCH_STATE)
        state["state"] = "OWNER_REQUIRED"
        state["owner_required_reason"] = "AUTONOMOUS_TECHNICAL_RECOVERY_LIMIT_REACHED"
        state["next_legal_action"] = "STOP / OWNER_REQUIRED"
        update_research_state(state, note=f"{exp} autonomous technical recovery limit reached.")
        commit_all(f"autonomy: stop {exp} after recovery limit")
        push_current(branch)
        metrics["owner_required_stops"] = int(metrics.get("owner_required_stops", 0)) + 1
        return_main()
        return "OWNER_REQUIRED"

    logs = failed_logs(branch)
    latest_do = read_text(str((evidence_dir / "DO_EXECUTION_001.json").relative_to(ROOT)))
    response = ai.ask_json(
        "recovery_analyst",
        role_system("recovery_analyst"),
        f"""Diagnose this exact {exp} failure under the immutable Frozen Plan.

FROZEN PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

CHECK SUMMARY:
{json.dumps(checks, ensure_ascii=False, indent=2)}

FAILED LOGS:
{logs}

DO EVIDENCE:
{latest_do}

Return:
{{
 "decision":"RECOVER"|"OWNER_REQUIRED",
 "classification":"TECHNICAL_FORMALIZATION"|"HARNESS"|"INFRASTRUCTURE"|"OUT_OF_SCOPE",
 "rationale":"...",
 "operations":[complete write/delete operations],
 "frozen_plan_unchanged":true
}}.
RECOVER is legal only if no Plan/factor/assumption/Claim-cone/success-criterion change is needed.
""",
        max_tokens=6000,
    )
    if response.get("decision") == "OWNER_REQUIRED":
        state = load_json(RESEARCH_STATE)
        state["state"] = "OWNER_REQUIRED"
        state["owner_required_reason"] = str(response.get("rationale") or "recovery requires out-of-scope change")
        state["next_legal_action"] = "STOP / OWNER_REQUIRED"
        update_research_state(state, note=f"{exp} recovery analyst set OWNER_REQUIRED.")
        idx = len(attempts) + 1
        write_record(evidence_dir / f"RECOVERY_{idx:03d}.json", {
            "decision": response,
            "checks": checks,
            "recorded_at": utc_now(),
        })
        commit_all(f"autonomy: record {exp} owner-required recovery boundary")
        push_current(branch)
        metrics["owner_required_stops"] = int(metrics.get("owner_required_stops", 0)) + 1
        return_main()
        return "OWNER_REQUIRED"
    if response.get("decision") != "RECOVER" or response.get("frozen_plan_unchanged") is not True:
        raise GovernanceError(f"invalid recovery decision: {response!r}")

    applied = apply_operations(response.get("operations"))
    assert_frozen(load_json(RESEARCH_STATE), exp)
    verification = run_plan_commands(plan)
    idx = len(attempts) + 1
    write_record(evidence_dir / f"RECOVERY_{idx:03d}.json", {
        "schema": "BOMA-AUTONOMOUS-RECOVERY-EVIDENCE-001",
        "experiment_id": exp,
        "decision": response,
        "applied_operations": applied,
        "prior_checks": checks,
        "post_recovery_verification": verification,
        "recorded_at": utc_now(),
    })
    state = load_json(RESEARCH_STATE)
    state["state"] = "WAITING_CI" if verification["passed"] else "RECOVERY_ALLOWED"
    state["waiting_on"] = "EXACT_PULL_REQUEST_CHECKS" if verification["passed"] else "FURTHER_AUTONOMOUS_TECHNICAL_RECOVERY"
    state["next_legal_action"] = "WAIT_FOR_EXACT_PR_CHECKS" if verification["passed"] else "CONTINUE_TECHNICAL_RECOVERY"
    update_research_state(state, note=f"{exp} technical recovery #{idx}; local verification passed={verification['passed']}.")
    commit_all(f"autonomy: recover {exp} within Frozen Plan")
    push_current(branch)
    metrics["technical_recovery_attempts"] = int(metrics.get("technical_recovery_attempts", 0)) + 1
    if not verification["passed"]:
        metrics["verification_failures"] = int(metrics.get("verification_failures", 0)) + 1
    return_main()
    return "CONTINUE"


def recover_nonplan_branch(
    ai: AIProvider,
    metrics: dict[str, Any],
    branch: str,
    pr: dict[str, Any],
    checks: list[dict[str, Any]],
    *,
    kind: str,
) -> str:
    checkout_branch(branch)
    logs = failed_logs(branch)
    response = ai.ask_json(
        "recovery_analyst",
        role_system("recovery_analyst"),
        f"""Recover a technical CI/governance failure on an autonomy {kind} branch.
This branch does not authorize any new mathematical factor.

CHECKS:
{json.dumps(checks, ensure_ascii=False, indent=2)}

FAILED LOGS:
{logs}

Return:
{{"decision":"RECOVER"|"OWNER_REQUIRED","rationale":"...","operations":[complete operations],
"research_decision_unchanged":true}}.
Do not change the already recorded transition/closure result merely to make CI green.
""",
        max_tokens=5000,
    )
    if response.get("decision") != "RECOVER" or response.get("research_decision_unchanged") is not True:
        return_main()
        raise GovernanceError(f"non-plan recovery requires owner or invalid response: {response!r}")
    applied = apply_operations(response.get("operations"))
    record_dir = AUTONOMY_EVIDENCE / "_runtime_recovery"
    record_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(record_dir.glob(f"{slug(branch)}-*.json"))
    write_record(record_dir / f"{slug(branch)}-{len(existing)+1:03d}.json", {
        "kind": kind,
        "branch": branch,
        "checks": checks,
        "decision": response,
        "applied_operations": applied,
        "recorded_at": utc_now(),
    })
    commit_all(f"autonomy: recover {kind} CI without changing research decision")
    push_current(branch)
    metrics["technical_recovery_attempts"] = int(metrics.get("technical_recovery_attempts", 0)) + 1
    return_main()
    return "WAITING_CI"


def study_act_close(
    ai: AIProvider,
    metrics: dict[str, Any],
    branch: str,
    exp: str,
    state: dict[str, Any],
    checks: list[dict[str, Any]],
) -> str:
    plan = assert_frozen(state, exp)
    evidence_dir = AUTONOMY_EVIDENCE / exp
    evidence_text = []
    for path in sorted(evidence_dir.glob("*.json")):
        evidence_text.append(f"## {path.name}\n{path.read_text(encoding='utf-8')[:10000]}")
    study = ai.ask_json(
        "study_analyst",
        role_system("study_analyst"),
        f"""Study the completed exact-head evidence for {exp}.

FROZEN PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

PR CHECKS:
{json.dumps(checks, ensure_ascii=False, indent=2)}

EXECUTION/RECOVERY EVIDENCE:
{chr(10).join(evidence_text)[:30000]}

Return:
{{
 "result":"PASS"|"INFORMATIVE_FAIL"|"OWNER_REQUIRED",
 "expected_vs_observed":[],
 "mathematical_findings":[],
 "formalization_findings":[],
 "deviations":[],
 "transition_prerequisite_observations":[],
 "owner_required_reason":null|"..."
}}.
""",
        max_tokens=5000,
    )
    if study.get("result") not in {"PASS", "INFORMATIVE_FAIL", "OWNER_REQUIRED"}:
        raise GovernanceError(f"invalid Study result: {study!r}")
    if study["result"] == "OWNER_REQUIRED":
        state = load_json(RESEARCH_STATE)
        state["state"] = "OWNER_REQUIRED"
        state["owner_required_reason"] = str(study.get("owner_required_reason") or "Study found owner-required boundary")
        state["next_legal_action"] = "STOP / OWNER_REQUIRED"
        write_record(evidence_dir / "FINAL_STUDY_001.json", study)
        update_research_state(state, note=f"{exp} Study set OWNER_REQUIRED.")
        commit_all(f"autonomy: study {exp} and stop owner-required")
        push_current(branch)
        metrics["owner_required_stops"] = int(metrics.get("owner_required_stops", 0)) + 1
        return_main()
        return "OWNER_REQUIRED"

    act = ai.ask_json(
        "act_analyst",
        role_system("act_analyst"),
        f"""Act on this completed Study for {exp} without deciding the next transition gate.

FROZEN PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

STUDY:
{json.dumps(study, ensure_ascii=False, indent=2)}

Return:
{{
 "durable_program_knowledge":[],
 "research_only_disposition":[],
 "candidate_future_work":[],
 "next_predeclared_transition_still_assessable":true|false,
 "acceptance_effect":"NONE"
}}.
""",
        max_tokens=3600,
    )
    if act.get("acceptance_effect") != "NONE":
        raise GovernanceError("Act attempted acceptance effect outside program authority")

    closure = ai.ask_json(
        "closure_auditor",
        role_system("closure_auditor"),
        f"""Audit lifecycle closure for {exp}.

PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

STUDY:
{json.dumps(study, ensure_ascii=False, indent=2)}

ACT:
{json.dumps(act, ensure_ascii=False, indent=2)}

EXACT PR CHECKS:
{json.dumps(checks, ensure_ascii=False, indent=2)}

Return:
{{
 "decision":"CLOSE"|"OWNER_REQUIRED",
 "frozen_plan_unchanged":true|false,
 "exact_evidence_complete":true|false,
 "unresolved_deviations":[],
 "acceptance_promotion":"NONE",
 "rationale":"..."
}}.
""",
        max_tokens=3200,
    )
    if closure.get("decision") != "CLOSE":
        state = load_json(RESEARCH_STATE)
        state["state"] = "OWNER_REQUIRED"
        state["owner_required_reason"] = str(closure.get("rationale") or "closure auditor refused closure")
        state["next_legal_action"] = "STOP / OWNER_REQUIRED"
        write_record(evidence_dir / "FINAL_STUDY_001.json", study)
        write_record(evidence_dir / "FINAL_ACT_001.json", act)
        write_record(evidence_dir / "CLOSURE_AUDIT_001.json", closure)
        update_research_state(state, note=f"{exp} closure auditor set OWNER_REQUIRED.")
        commit_all(f"autonomy: record {exp} closure owner-required")
        push_current(branch)
        metrics["owner_required_stops"] = int(metrics.get("owner_required_stops", 0)) + 1
        return_main()
        return "OWNER_REQUIRED"
    if closure.get("frozen_plan_unchanged") is not True or closure.get("exact_evidence_complete") is not True:
        raise GovernanceError("closure auditor CLOSE lacks exact/frozen confirmations")
    if closure.get("acceptance_promotion") != "NONE":
        raise GovernanceError("closure auditor attempted acceptance promotion")
    unresolved = closure.get("unresolved_deviations")
    if isinstance(unresolved, list) and unresolved:
        raise GovernanceError("closure auditor CLOSE has unresolved deviations")

    write_record(evidence_dir / "FINAL_STUDY_001.json", study)
    write_record(evidence_dir / "FINAL_ACT_001.json", act)
    write_record(evidence_dir / "CLOSURE_AUDIT_001.json", closure)
    closure_md = ROOT / "LAB/PDSA/experiments" / f"{exp}_AUTONOMOUS_LIFECYCLE_CLOSURE_001.md"
    closure_md.write_text(
        f"# {exp} — Autonomous Lifecycle Closure 001\n\n"
        f"**Study result:** `{study['result']}`  \n"
        f"**Frozen Plan commit:** `{state.get('active_frozen_plan_sha')}`  \n"
        f"**Acceptance effect:** `NONE`.\n\n"
        "This lifecycle is `CLOSED` only when the exact commit containing this record "
        "passes all required pull-request checks and is routine-merged without content drift.\n\n"
        "## Closure audit\n\n```json\n"
        + json.dumps(closure, ensure_ascii=False, indent=2)
        + "\n```\n\n## Study\n\n```json\n"
        + json.dumps(study, ensure_ascii=False, indent=2)
        + "\n```\n\n## Act\n\n```json\n"
        + json.dumps(act, ensure_ascii=False, indent=2)
        + "\n```\n",
        encoding="utf-8",
    )
    state = load_json(RESEARCH_STATE)
    state["state"] = "CLOSING"
    state["last_experiment_result"] = study["result"]
    state["waiting_on"] = "EXACT_CLOSURE_HEAD_PR_CHECKS"
    state["next_legal_action"] = f"WAIT_FOR_EXACT_{exp}_CLOSURE_HEAD_THEN_ROUTINE_MERGE"
    state["current_stage_two_frontier"]["active_experiment_status"] = f"CLOSING / {study['result']} / EXACT_CI_PENDING"
    update_research_state(state, note=f"{exp} Study/Act complete; lifecycle closure awaits exact closure-head CI.")
    commit_all(f"autonomy: close {exp} pending exact closure-head verification")
    push_current(branch)
    return_main()
    return "WAITING_CI"


def close_when_exact(
    ai: AIProvider,
    metrics: dict[str, Any],
    branch: str,
    exp: str,
    state: dict[str, Any],
) -> str:
    pr = pr_for_branch(branch)
    if not pr:
        raise GovernanceError(f"CLOSING branch lacks PR: {branch}")
    if pr.get("mergedAt"):
        return_main()
        return "CONTINUE"
    check_state, checks = pr_check_state(int(pr["number"]))
    if check_state == "PENDING":
        return_main()
        return "WAITING_CI"
    if check_state == "FAIL":
        return recover_nonplan_branch(ai, metrics, branch, pr, checks, kind=f"{exp}-closure")
    merge_pr(int(pr["number"]), branch)
    metrics["routine_merges"] = int(metrics.get("routine_merges", 0)) + 1
    return_main()
    return "CONTINUE"


def main_closing_handler(ai: AIProvider, metrics: dict[str, Any]) -> str:
    state = load_json(RESEARCH_STATE)
    exp = state.get("active_experiment")
    if not isinstance(exp, str) or not exp:
        raise GovernanceError("main CLOSING state lacks active experiment")
    branch = f"autonomy/postmerge-{slug(exp)}-sync"
    if branch_exists(branch):
        pr = pr_for_branch(branch)
        if not pr:
            raise GovernanceError("postmerge sync branch lacks PR")
        if pr.get("mergedAt"):
            return_main()
            return "CONTINUE"
        check_state, checks = pr_check_state(int(pr["number"]))
        if check_state == "PENDING":
            return "WAITING_CI"
        if check_state == "FAIL":
            return recover_nonplan_branch(ai, metrics, branch, pr, checks, kind=f"{exp}-postmerge-sync")
        merge_pr(int(pr["number"]), branch)
        return_main()
        return "CONTINUE"

    merge_head = current_head()
    checkout_branch(branch, create=True)
    state = load_json(RESEARCH_STATE)
    queue = state["authorized_experiment_queue"]
    idx = queue.index(exp)
    result = state.get("last_experiment_result")
    state["synchronized_main_sha"] = merge_head
    state["active_experiment"] = None
    state["active_experiment_branch"] = None
    state["active_frozen_plan"] = None
    state["active_frozen_plan_machine"] = None
    state["active_frozen_plan_sha"] = None
    state["active_experiment_frozen_reference_sha"] = None
    state["active_experiment_origin_record"] = None
    state["active_work_head_before_ci_state_commit"] = None
    frontier = state["current_stage_two_frontier"]
    frontier["active_experiment"] = None
    frontier["active_experiment_status"] = "NONE / POSTMERGE_SYNCHRONIZED"
    frontier["latest_completed_experiment"] = exp
    frontier["latest_completed_status"] = f"CLOSED / {result} / EXACT_HEAD_VERIFIED / ROUTINE_MERGED"

    if idx == len(queue) - 1:
        state["state"] = "ACT"
        state["waiting_on"] = "PROGRAM_LEVEL_SYNTHESIS"
        state["program_transition"] = {
            "from_experiment": exp,
            "to_candidate": None,
            "queue_order_immutable_without_owner": True,
            "informative_fail_may_transition_if_prerequisites_hold": True,
            "sequence_critical_discovery_means": "OWNER_REQUIRED",
            "program_completion_requires_program_level_synthesis": True,
            "transition_decision_recorded": True,
            "last_transition_decision": "PROGRAM_SYNTHESIS_REQUIRED",
        }
        frontier["next_experiment"] = None
        frontier["next_experiment_status"] = "NO_FIFTH_EXPERIMENT_AUTHORIZED"
        frontier["activation_authorized_by_this_state"] = False
        state["next_legal_action"] = "RUN_ST2_RP_001_PROGRAM_LEVEL_SYNTHESIS"
        note = f"{exp} routine-merged; program-level synthesis required before PROGRAM_COMPLETE."
    else:
        nxt = queue[idx + 1]
        state["state"] = "TRANSITION_GATE"
        state["waiting_on"] = f"{exp}_TO_{nxt}_TRANSITION_GATE"
        state["program_transition"] = {
            "from_experiment": exp,
            "to_candidate": nxt,
            "queue_order_immutable_without_owner": True,
            "informative_fail_may_transition_if_prerequisites_hold": True,
            "sequence_critical_discovery_means": "OWNER_REQUIRED",
            "program_completion_requires_program_level_synthesis": True,
            "transition_decision_recorded": False,
        }
        frontier["next_experiment"] = nxt
        frontier["next_experiment_status"] = "OWNER_AUTHORIZED / QUEUED / TRANSITION_GATE_PENDING"
        frontier["activation_authorized_by_this_state"] = False
        state["next_legal_action"] = f"EVALUATE_{exp}_TO_{nxt}_TRANSITION_GATE_ONLY"
        note = f"{exp} routine-merged and synchronized; next decision is {exp}→{nxt} transition gate."

    sync_record = AUTONOMY_EVIDENCE / exp / "POSTMERGE_SYNC_001.json"
    if not sync_record.exists():
        write_record(sync_record, {
            "schema": "BOMA-AUTONOMOUS-POSTMERGE-SYNC-001",
            "experiment_id": exp,
            "merged_main_sha": merge_head,
            "result": result,
            "new_state": state["state"],
            "recorded_at": utc_now(),
        })
    update_research_state(state, note=note)
    commit_all(f"autonomy: synchronize postmerge state after {exp}")
    push_current(branch)
    ensure_pr(
        branch,
        f"Autonomy: synchronize postmerge state after {exp}",
        "Administrative lifecycle synchronization after an exact verified routine merge. "
        "This PR makes no new mathematical transition decision.",
    )
    return_main()
    return "WAITING_CI"


def program_synthesis_handler(ai: AIProvider, metrics: dict[str, Any]) -> str:
    branch = "autonomy/st2-rp-001-program-synthesis"
    if branch_exists(branch):
        pr = pr_for_branch(branch)
        if not pr:
            raise GovernanceError("program synthesis branch lacks PR")
        if pr.get("mergedAt"):
            return_main()
            return "CONTINUE"
        state, checks = pr_check_state(int(pr["number"]))
        if state == "PENDING":
            return "WAITING_CI"
        if state == "FAIL":
            return recover_nonplan_branch(ai, metrics, branch, pr, checks, kind="program-synthesis")
        merge_pr(int(pr["number"]), branch)
        metrics["program_syntheses"] = int(metrics.get("program_syntheses", 0)) + 1
        return_main()
        return "CONTINUE"

    synth_sources = []
    for exp_dir in sorted(AUTONOMY_EVIDENCE.glob("ST2-EXP-*")):
        if not exp_dir.is_dir():
            continue
        for name in ("FINAL_STUDY_001.json", "FINAL_ACT_001.json", "CLOSURE_AUDIT_001.json", "POSTMERGE_SYNC_001.json"):
            path = exp_dir / name
            if path.is_file():
                synth_sources.append(f"## {exp_dir.name}/{name}\n{path.read_text(encoding='utf-8')[:9000]}")
    response = ai.ask_json(
        "program_synthesizer",
        role_system("program_synthesizer"),
        f"""Perform the required ST2-RP-001 program-level synthesis after experiment 017.

PROGRAM AUTHORITY:
{read_text('LAB/PDSA/RESEARCH_PROGRAM_ST2_RP_001_R_C_COMPOSITIONALITY_MINIMALITY.md', 18000)}

AUTONOMOUS PROGRAM EVIDENCE:
{chr(10).join(synth_sources)[:45000]}

Return:
{{
 "decision":"PROGRAM_COMPLETE"|"OWNER_REQUIRED",
 "program_findings":[],
 "cross_experiment_synthesis":[],
 "limits":[],
 "acceptance_effect":"NONE",
 "fifth_experiment_authorized":false,
 "owner_required_reason":null|"..."
}}.
""",
        max_tokens=5500,
    )
    if response.get("decision") not in {"PROGRAM_COMPLETE", "OWNER_REQUIRED"}:
        raise GovernanceError("invalid program synthesis decision")
    if response.get("acceptance_effect") != "NONE" or response.get("fifth_experiment_authorized") is not False:
        raise GovernanceError("program synthesis attempted unauthorized acceptance/new experiment")

    checkout_branch(branch, create=True)
    synthesis_path = ROOT / "LAB/PDSA/ST2_RP_001_AUTONOMOUS_PROGRAM_SYNTHESIS_001.md"
    synthesis_path.write_text(
        "# ST2-RP-001 — Autonomous Program Synthesis 001\n\n```json\n"
        + json.dumps(response, ensure_ascii=False, indent=2)
        + "\n```\n\nNo fifth experiment or new research program is authorized by this synthesis.\n",
        encoding="utf-8",
    )
    state = load_json(RESEARCH_STATE)
    if response["decision"] == "PROGRAM_COMPLETE":
        state["state"] = "PROGRAM_COMPLETE"
        state["owner_required_reason"] = None
        state["waiting_on"] = None
        state["next_legal_action"] = "STOP / PROGRAM_COMPLETE / NO_FIFTH_EXPERIMENT_AUTHORIZED"
        note = "ST2-RP-001 autonomous program synthesis complete; no fifth experiment authorized."
    else:
        state["state"] = "OWNER_REQUIRED"
        state["owner_required_reason"] = str(response.get("owner_required_reason") or "program synthesis requires owner")
        state["next_legal_action"] = "STOP / OWNER_REQUIRED"
        metrics["owner_required_stops"] = int(metrics.get("owner_required_stops", 0)) + 1
        note = "ST2-RP-001 program synthesis set OWNER_REQUIRED."
    update_research_state(state, note=note)
    commit_all("autonomy: synthesize ST2-RP-001 program")
    push_current(branch)
    ensure_pr(
        branch,
        "Autonomy: ST2-RP-001 program-level synthesis",
        "Required program-level synthesis after ST2-EXP-017. No fifth experiment is authorized.",
    )
    return_main()
    return "WAITING_CI"


def dispatch(ai: AIProvider, metrics: dict[str, Any]) -> str:
    state = load_json(RESEARCH_STATE)
    stage = str(state.get("state"))
    if stage == "TRANSITION_GATE":
        return transition_handler(ai, metrics)
    if stage == "PREPARING_EXPERIMENT":
        return planning_handler(ai, metrics)
    if stage == "CLOSING":
        return main_closing_handler(ai, metrics)
    if stage == "ACT" and state.get("active_experiment") is None:
        return program_synthesis_handler(ai, metrics)
    if stage == "PROGRAM_COMPLETE":
        return "PROGRAM_COMPLETE"
    if stage == "OWNER_REQUIRED":
        return "OWNER_REQUIRED"
    # If main reflects a state that should live only on an open experiment branch,
    # discover/continue that deterministic branch.
    active = state.get("active_experiment")
    if isinstance(active, str) and active:
        branch = str(state.get("active_experiment_branch") or f"autonomy/{slug(active)}")
        if branch_exists(branch):
            checkout_branch(branch)
            return branch_stage_handler(ai, metrics, branch, active, load_json(RESEARCH_STATE))
    raise GovernanceError(f"unhandled main BOMA research state: {stage}")


def main() -> int:
    exp_state = load_json(EXP_STATE)
    metrics = load_json(METRICS)
    if not exp_state.get("armed") or exp_state.get("experiment_state") != "ACTIVE":
        print("BOMA autonomy controller: experiment not ACTIVE; no research action")
        return 0

    deadline_raw = exp_state.get("observation_deadline")
    if isinstance(deadline_raw, str) and deadline_raw:
        try:
            deadline = dt.datetime.fromisoformat(deadline_raw)
            if deadline.tzinfo is None:
                raise ValueError("deadline must be timezone-aware")
        except ValueError as exc:
            raise GovernanceError(f"invalid observation_deadline: {deadline_raw}") from exc
        now = dt.datetime.now(dt.timezone.utc)
        if now >= deadline:
            exp_state["experiment_state"] = "PAUSED_FOR_META_REVIEW"
            exp_state["current_stage"] = "META_REVIEW_DUE"
            exp_state["meta_review_due"] = True
            exp_state["last_run_at"] = utc_now()
            exp_state["last_run_result"] = "OBSERVATION_WINDOW_COMPLETE"
            metrics["observation_pauses"] = int(metrics.get("observation_pauses", 0)) + 1
            save_json(EXP_STATE, exp_state)
            save_json(METRICS, metrics)
            print("BOMA autonomy observation window complete; paused before new research wake")
            return 0
    if shutil.which("gh") is None:
        raise GovernanceError("GitHub CLI 'gh' is required on runner")

    return_main()
    exp_state["current_wake"] = int(exp_state.get("current_wake", 0)) + 1
    exp_state["current_stage"] = "AUTONOMOUS_RESEARCH_WAKE"
    exp_state["last_run_at"] = utc_now()
    metrics["wakes_started"] = int(metrics.get("wakes_started", 0)) + 1
    ai = AIProvider(metrics, persist_metrics=False)

    outcome = "NO_ACTION"
    try:
        # Continue within one wake until an external wait/stop, bounded to avoid loops.
        for _ in range(8):
            return_main()
            outcome = dispatch(ai, metrics)
            if outcome in {"WAITING_CI", "OWNER_REQUIRED", "PROGRAM_COMPLETE"}:
                break
            if outcome != "CONTINUE":
                break
        return_main()
        research_state = load_json(RESEARCH_STATE)
        if research_state.get("state") == "PROGRAM_COMPLETE":
            exp_state["experiment_state"] = "FINISHED"
            exp_state["current_stage"] = "PROGRAM_COMPLETE"
            exp_state["finished_at"] = utc_now()
            exp_state["final_status"] = "PROGRAM_COMPLETE"
            outcome = "PROGRAM_COMPLETE"
        elif research_state.get("state") == "OWNER_REQUIRED":
            exp_state["experiment_state"] = "STOPPED"
            exp_state["current_stage"] = "OWNER_REQUIRED"
            exp_state["finished_at"] = utc_now()
            exp_state["final_status"] = "OWNER_REQUIRED"
            outcome = "OWNER_REQUIRED"
        else:
            exp_state["current_stage"] = str(research_state.get("state"))
        exp_state["last_run_result"] = outcome
        print(f"BOMA autonomy wake completed: {outcome}")
        return 0
    except Exception as exc:
        try:
            return_main()
        except Exception:
            pass
        exp_state["current_stage"] = "CONTROLLER_ERROR"
        exp_state["last_run_result"] = f"CONTROLLER_ERROR: {type(exc).__name__}: {exc}"
        raise
    finally:
        metrics["wakes_completed"] = int(metrics.get("wakes_completed", 0)) + 1
        metrics["human_research_interventions"] = int(exp_state.get("human_research_interventions", 0))
        metrics["human_infrastructure_interventions"] = int(exp_state.get("human_infrastructure_interventions", 0))
        save_json(EXP_STATE, exp_state)
        save_json(METRICS, metrics)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GovernanceError as exc:
        print(f"BOMA AUTONOMY GOVERNANCE ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
