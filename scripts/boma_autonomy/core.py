"""Core safety and repository helpers for the BOMA autonomy runtime."""
from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import subprocess
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[2]
AUTONOMY = ROOT / ".autonomy"
EXP_STATE = AUTONOMY / "state.json"
METRICS = AUTONOMY / "metrics.json"
PROVIDER = AUTONOMY / "provider.json"
POLICY = AUTONOMY / "policy.json"
RESEARCH_STATE = ROOT / "LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json"
PROGRAM_MANIFEST = ROOT / "LAB/PDSA/ST2_RP_001_PROGRAM_MANIFEST_001.json"
STATUS = ROOT / "LAB/PDSA/STATUS.md"
AGENTS = ROOT / "AGENTS.md"
REGISTER = ROOT / "LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md"
PROTOCOL = ROOT / "LAB/PDSA/AUTONOMY_EXPERIMENT_PROTOCOL_001.md"

RUNTIME_BEGIN = "<!-- BOMA_AUTONOMY_RUNTIME_STATE_BEGIN -->"
RUNTIME_END = "<!-- BOMA_AUTONOMY_RUNTIME_STATE_END -->"


class GovernanceError(RuntimeError):
    pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GovernanceError(f"cannot read JSON {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise GovernanceError(f"JSON root must be object: {path.relative_to(ROOT)}")
    return data


def save_json(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def run(
    command: list[str],
    *,
    cwd: pathlib.Path | None = None,
    timeout: int = 900,
    check: bool = False,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd or ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        payload = {"command": command, "exit_code": 127, "stdout": "", "stderr": str(exc)}
        if check:
            raise GovernanceError(str(payload)) from exc
        return payload
    except subprocess.TimeoutExpired as exc:
        payload = {"command": command, "exit_code": 124, "stdout": "", "stderr": str(exc)}
        if check:
            raise GovernanceError(str(payload)) from exc
        return payload
    payload = {
        "command": command,
        "exit_code": result.returncode,
        "stdout": result.stdout[-12000:],
        "stderr": result.stderr[-12000:],
    }
    if check and result.returncode != 0:
        raise GovernanceError(
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"{payload['stdout']}\n{payload['stderr']}"
        )
    return payload


def git(*args: str, check: bool = True, cwd: pathlib.Path | None = None) -> str:
    result = run(["git", *args], cwd=cwd, check=check, timeout=300)
    return str(result["stdout"]).strip()


def current_head() -> str:
    return git("rev-parse", "HEAD")


def sanitized_env() -> dict[str, str]:
    policy = load_json(POLICY)
    fragments = [str(x).upper() for x in policy.get("forbidden_secret_name_fragments", [])]
    clean: dict[str, str] = {}
    for key, value in os.environ.items():
        upper = key.upper()
        if key in {"GITHUB_TOKEN", "GH_TOKEN", "ACTIONS_RUNTIME_TOKEN"}:
            continue
        if any(fragment in upper for fragment in fragments):
            continue
        clean[key] = value
    return clean


def accepted_control_paths() -> set[str]:
    policy = load_json(POLICY)
    result = {str(p) for p in policy.get("protected_exact_paths", [])}
    for manifest_rel in policy.get("accepted_manifests", []):
        rel = str(manifest_rel)
        result.add(rel)
        manifest = ROOT / rel
        if not manifest.is_file():
            continue
        for raw in manifest.read_text(encoding="utf-8").splitlines():
            src = raw.strip()
            if src and not src.startswith("#"):
                result.add(src)
    return result


def assert_executor_path_allowed(rel: str) -> pathlib.Path:
    if not rel or rel.startswith("/") or "\\" in rel:
        raise GovernanceError(f"invalid executor path: {rel!r}")
    pure = pathlib.PurePosixPath(rel)
    if ".." in pure.parts:
        raise GovernanceError(f"path traversal denied: {rel}")
    policy = load_json(POLICY)
    if rel in accepted_control_paths():
        raise GovernanceError(f"accepted/protected path denied: {rel}")
    for prefix in policy.get("protected_prefixes", []):
        if rel.startswith(str(prefix)):
            raise GovernanceError(f"autonomy control path denied: {rel}")
    if rel in {
        ".github/workflows/boma-autonomous-engine.yml",
        ".github/workflows/boma-autonomy-experiment-guard.yml",
    }:
        raise GovernanceError(f"runtime workflow denied: {rel}")
    target = ROOT / rel
    try:
        target.resolve().relative_to(ROOT.resolve())
    except ValueError as exc:
        raise GovernanceError(f"path escapes repository: {rel}") from exc
    return target


def render_runtime_state(state: dict[str, Any], *, note: str = "") -> str:
    frontier = state.get("current_stage_two_frontier", {})
    transition = state.get("program_transition", {})
    lines = [
        RUNTIME_BEGIN,
        "### Autonomous runtime current-state marker",
        "",
        "This block is maintained by the autonomous runtime and supersedes older",
        "current-frontier prose below it when the two disagree. Historical records",
        "remain immutable evidence of their own time.",
        "",
        "```text",
        f"STATE: {state.get('state')}",
        f"PROGRAM: {state.get('active_program_id')}",
        f"QUEUE_CURSOR: {state.get('queue_cursor')}",
        f"ACTIVE_EXPERIMENT: {state.get('active_experiment')}",
        f"LATEST_COMPLETED: {frontier.get('latest_completed_experiment')}",
        f"NEXT_EXPERIMENT: {frontier.get('next_experiment')}",
        f"TRANSITION_FROM: {transition.get('from_experiment')}",
        f"TRANSITION_CANDIDATE: {transition.get('to_candidate')}",
        f"TRANSITION_DECISION_RECORDED: {transition.get('transition_decision_recorded')}",
        f"NEXT_LEGAL_ACTION: {state.get('next_legal_action')}",
        "```",
    ]
    if note:
        lines.extend(["", f"Runtime note: {note}"])
    lines.extend([RUNTIME_END, ""])
    return "\n".join(lines)


def upsert_runtime_block(path: pathlib.Path, state: dict[str, Any], *, note: str = "") -> None:
    text = path.read_text(encoding="utf-8")
    block = render_runtime_state(state, note=note)
    if RUNTIME_BEGIN in text and RUNTIME_END in text:
        before, rest = text.split(RUNTIME_BEGIN, 1)
        _, after = rest.split(RUNTIME_END, 1)
        text = before.rstrip() + "\n\n" + block + after.lstrip("\n")
    else:
        first_newline = text.find("\n")
        if first_newline >= 0:
            text = text[: first_newline + 1] + "\n" + block + "\n" + text[first_newline + 1 :]
        else:
            text = text + "\n\n" + block
    path.write_text(text, encoding="utf-8")


def experiment_record(manifest: dict[str, Any], experiment_id: str) -> dict[str, Any]:
    for item in manifest.get("experiments", []):
        if isinstance(item, dict) and item.get("experiment_id") == experiment_id:
            return item
    raise GovernanceError(f"experiment not in active manifest: {experiment_id}")


def bootstrap_errors() -> list[str]:
    errors: list[str] = []
    required = [
        EXP_STATE,
        METRICS,
        PROVIDER,
        POLICY,
        RESEARCH_STATE,
        PROGRAM_MANIFEST,
        STATUS,
        AGENTS,
        REGISTER,
        PROTOCOL,
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
    if errors:
        return errors

    try:
        e = load_json(EXP_STATE)
        r = load_json(RESEARCH_STATE)
        m = load_json(PROGRAM_MANIFEST)
        p = load_json(POLICY)
    except GovernanceError as exc:
        return [str(exc)]

    if e.get("schema") != "BOMA-AUTONOMY-EXPERIMENT-STATE-001":
        errors.append("unexpected autonomy experiment state schema")
    if e.get("experiment_state") not in {"BOOTSTRAP", "ACTIVE", "FINISHED", "STOPPED", "PAUSED_FOR_META_REVIEW"}:
        errors.append("invalid autonomy experiment_state")
    if p.get("fail_closed") is not True:
        errors.append("runtime policy must remain fail_closed=true")
    expected_repo = p.get("allowed_repository")
    actual_repo = os.environ.get("GITHUB_REPOSITORY")
    if actual_repo and expected_repo and actual_repo != expected_repo:
        errors.append(f"runtime bound to {expected_repo}, not {actual_repo}")
    if r.get("active_program_id") != "ST2-RP-001":
        errors.append("active BOMA program must be ST2-RP-001")
    if m.get("program_id") != "ST2-RP-001" or m.get("status") != "OWNER_AUTHORIZED":
        errors.append("program manifest must remain owner-authorized ST2-RP-001")
    if r.get("authorized_experiment_queue") != m.get("queue_order"):
        errors.append("research-state queue must match manifest queue")
    if not r.get("safety", {}).get("fail_closed"):
        errors.append("BOMA research state must remain fail-closed")
    if r.get("safety", {}).get("main_research_writes_allowed") is not False:
        errors.append("main research writes must remain forbidden")
    return errors


def start_frontier_errors() -> list[str]:
    errors = bootstrap_errors()
    if errors:
        return errors
    r = load_json(RESEARCH_STATE)
    p = load_json(POLICY)
    if r.get("state") != p.get("required_start_research_state"):
        errors.append(f"START requires research state {p.get('required_start_research_state')}")
    if r.get("active_experiment") is not None:
        errors.append("START requires no active research experiment")
    transition = r.get("program_transition", {})
    if transition.get("from_experiment") != p.get("required_start_transition_from"):
        errors.append("unexpected START transition source")
    if transition.get("to_candidate") != p.get("required_start_transition_candidate"):
        errors.append("unexpected START transition candidate")
    if transition.get("transition_decision_recorded") is not False:
        errors.append("014→015 decision must remain unrecorded before START")
    frontier = r.get("current_stage_two_frontier", {})
    if frontier.get("next_experiment") != "ST2-EXP-015":
        errors.append("START requires ST2-EXP-015 as next authorized candidate")
    if r.get("active_frozen_plan") is not None:
        errors.append("START requires no active Frozen Plan")
    return errors
