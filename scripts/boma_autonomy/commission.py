#!/usr/bin/env python3
"""Pre-START GitHub write/PR/CI plumbing commission test.

Creates a temporary control-plane-only branch and PR, proves that the dedicated
autonomy exact-head guard is triggered and succeeds without human approval, then
closes/deletes the probe. Before the probe it also quarantines stale runtime
research branches left by earlier stopped Meta-PDSA generations so a new generation
cannot inherit a closed PR/branch by deterministic-name collision. No BOMA research
content or decision is changed.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

from core import AUTONOMY, EXP_STATE, ROOT, current_head, load_json, run, save_json, start_frontier_errors, utc_now

OUT = AUTONOMY / "commission.json"
GUARD_WORKFLOW = "BOMA Autonomy Exact-Head Guard 001"
CI_TIMEOUT_SECONDS = 180
CI_POLL_SECONDS = 5
TERMINAL_FAILURES = {
    "failure",
    "cancelled",
    "timed_out",
    "action_required",
    "stale",
    "startup_failure",
}
RUNTIME_RESEARCH_BRANCH_PREFIXES = (
    "autonomy/transition-",
    "autonomy/st2-exp-",
    "autonomy/postmerge-",
)
RUNTIME_RESEARCH_BRANCH_EXACT = {
    "autonomy/st2-rp-001-program-synthesis",
}


def gh(args: list[str], *, check: bool = True) -> dict:
    env = os.environ.copy()
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN/GITHUB_TOKEN unavailable")
    env["GH_TOKEN"] = token
    return run(["gh", *args], env=env, timeout=180, check=check)


def gh_json(args: list[str]):
    result = gh(args, check=False)
    if result["exit_code"] != 0:
        raise RuntimeError(
            f"gh command failed ({result['exit_code']}): gh {' '.join(args)}\n"
            f"{result.get('stdout', '')}\n{result.get('stderr', '')}"
        )
    try:
        return json.loads(result.get("stdout") or "null")
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid gh JSON: {result.get('stdout', '')[:1000]}") from exc


def is_runtime_research_branch(branch: str) -> bool:
    return branch in RUNTIME_RESEARCH_BRANCH_EXACT or any(
        branch.startswith(prefix) for prefix in RUNTIME_RESEARCH_BRANCH_PREFIXES
    )


def archive_branch_name(generation: str, branch: str) -> str:
    generation_slug = re.sub(r"[^a-z0-9]+", "-", generation.lower()).strip("-")
    suffix = branch[len("autonomy/") :] if branch.startswith("autonomy/") else branch
    return f"archive/{generation_slug}/prestart/{suffix}"


def remote_runtime_research_branches() -> list[tuple[str, str]]:
    result = run(["git", "ls-remote", "--heads", "origin"], timeout=120, check=True)
    found: list[tuple[str, str]] = []
    for raw in str(result.get("stdout") or "").splitlines():
        parts = raw.split()
        if len(parts) != 2 or not parts[1].startswith("refs/heads/"):
            continue
        branch = parts[1][len("refs/heads/") :]
        if is_runtime_research_branch(branch):
            found.append((branch, parts[0]))
    return sorted(found)


def pull_requests_for_branch(branch: str) -> list[dict]:
    data = gh_json([
        "pr", "list", "--head", branch, "--state", "all", "--limit", "10",
        "--json", "number,state,mergedAt,headRefName,headRefOid,url,title",
    ])
    return data if isinstance(data, list) else []


def quarantine_stale_runtime_branches(generation: str) -> list[dict]:
    """Archive prior-generation runtime refs before the new measurement window.

    Only branches used by the autonomous research runtime are considered. An open PR
    is never renamed/deleted automatically; that is ambiguous authority and fails
    commission closed. Closed/merged historical PRs remain immutable GitHub evidence,
    while the exact branch head is preserved under an archive ref before the live
    deterministic branch name is removed.
    """
    archived: list[dict] = []
    for branch, sha in remote_runtime_research_branches():
        prs = pull_requests_for_branch(branch)
        if any(str(pr.get("state") or "").upper() == "OPEN" for pr in prs):
            raise RuntimeError(
                f"stale runtime research branch has an open PR and cannot be quarantined automatically: {branch}"
            )

        archive = archive_branch_name(generation, branch)
        existing = run(
            ["git", "ls-remote", "--heads", "origin", f"refs/heads/{archive}"],
            timeout=120,
            check=True,
        )
        existing_lines = str(existing.get("stdout") or "").splitlines()
        if existing_lines:
            existing_sha = existing_lines[0].split()[0]
            if existing_sha != sha:
                raise RuntimeError(
                    f"archive ref collision for {branch}: {archive} points to {existing_sha}, expected {sha}"
                )
        else:
            run(["git", "push", "origin", f"{sha}:refs/heads/{archive}"], timeout=180, check=True)

        run(["git", "push", "origin", "--delete", branch], timeout=180, check=True)
        verify = run(
            ["git", "ls-remote", "--heads", "origin", f"refs/heads/{branch}"],
            timeout=120,
            check=True,
        )
        if str(verify.get("stdout") or "").strip():
            raise RuntimeError(f"runtime branch quarantine failed; source ref still exists: {branch}")

        archived.append({
            "source_branch": branch,
            "source_head_sha": sha,
            "archive_branch": archive,
            "pull_requests": prs,
            "research_content_rewritten": False,
            "research_decision_changed": False,
        })

    return archived


def wait_for_guard_ci(branch: str, probe_head_sha: str) -> dict:
    """Require the PR-triggered exact-head guard to appear and finish SUCCESS."""
    deadline = time.monotonic() + CI_TIMEOUT_SECONDS
    last_seen = None
    while time.monotonic() < deadline:
        runs = gh_json([
            "run", "list",
            "--branch", branch,
            "--event", "pull_request",
            "--limit", "40",
            "--json", "databaseId,status,conclusion,workflowName,headSha,url",
        ])
        if isinstance(runs, list):
            candidates = [
                item for item in runs
                if isinstance(item, dict)
                and item.get("workflowName") == GUARD_WORKFLOW
                and item.get("headSha") == probe_head_sha
            ]
            if candidates:
                run_info = candidates[0]
                last_seen = run_info
                status = str(run_info.get("status") or "").lower()
                conclusion = str(run_info.get("conclusion") or "").lower()
                if conclusion == "success" and status == "completed":
                    return run_info
                if conclusion in TERMINAL_FAILURES:
                    raise RuntimeError(
                        f"commission PR guard did not run successfully: {run_info}"
                    )
        time.sleep(CI_POLL_SECONDS)

    if last_seen:
        raise RuntimeError(
            f"commission PR guard did not reach SUCCESS within {CI_TIMEOUT_SECONDS}s: {last_seen}"
        )
    raise RuntimeError(
        f"commission PR never triggered {GUARD_WORKFLOW!r} within {CI_TIMEOUT_SECONDS}s; "
        "autonomous PR-to-CI plumbing is not commissioned"
    )


def main() -> int:
    state = load_json(EXP_STATE)
    if state.get("armed") or state.get("experiment_state") != "BOOTSTRAP":
        print("Commission test is pre-START only", file=sys.stderr)
        return 2
    errors = start_frontier_errors()
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 3
    if not os.environ.get("GITHUB_REPOSITORY"):
        print("GITHUB_REPOSITORY unavailable", file=sys.stderr)
        return 4

    generation = str(state.get("experiment_generation") or "")
    anchor = current_head()
    suffix = str(int(time.time()))
    branch = f"autonomy/commission-probe-{suffix}"
    probe_rel = "LAB/PDSA/autonomy-commission-probe.txt"
    probe = ROOT / probe_rel
    pr_number = None
    probe_head_sha = None
    guard_run = None
    branch_push = False
    pull_request_create = False
    pull_request_ci = False
    pull_request_close = False
    passed = False
    error = None
    stale_branch_archives: list[dict] = []

    try:
        stale_branch_archives = quarantine_stale_runtime_branches(generation)
        remaining = remote_runtime_research_branches()
        if remaining:
            raise RuntimeError(f"runtime research branches remain after quarantine: {remaining}")

        run(["git", "checkout", "-b", branch], check=True)
        probe.write_text(
            "Synthetic pre-START autonomy commission probe. No research content.\n",
            encoding="utf-8",
        )
        run(["git", "add", probe_rel], check=True)
        run(["git", "commit", "-m", "autonomy: synthetic pre-START commission probe"], check=True)
        probe_head_sha = current_head()
        run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"], check=True)
        branch_push = True

        gh([
            "pr", "create", "--base", "main", "--head", branch,
            "--title", "Autonomy pre-START commission probe",
            "--body", "Synthetic control-plane plumbing test only. No BOMA research decision or content change."
        ])
        view = gh_json([
            "pr", "view", branch, "--json", "number,state,headRefName,headRefOid,baseRefName,url"
        ])
        pr_number = int(view["number"])
        if (
            view.get("state") != "OPEN"
            or view.get("headRefName") != branch
            or view.get("baseRefName") != "main"
            or view.get("headRefOid") != probe_head_sha
        ):
            raise RuntimeError(f"unexpected commission PR state: {view}")
        pull_request_create = True

        guard_run = wait_for_guard_ci(branch, probe_head_sha)
        pull_request_ci = True

        gh(["pr", "close", str(pr_number)])
        pull_request_close = True
        passed = True
    except Exception as exc:
        error = str(exc)
    finally:
        if pr_number is not None and not pull_request_close:
            close_result = gh(["pr", "close", str(pr_number)], check=False)
            pull_request_close = close_result.get("exit_code") == 0
        run(["git", "reset", "--hard"], check=False)
        run(["git", "checkout", "main"], check=False)
        run(["git", "fetch", "origin", "main"], check=False)
        run(["git", "reset", "--hard", "origin/main"], check=False)
        if branch:
            run(["git", "push", "origin", "--delete", branch], check=False)

    record = {
        "schema": "BOMA-AUTONOMY-COMMISSION-003",
        "experiment_generation": generation,
        "passed": passed,
        "main_anchor_sha": anchor,
        "probe_head_sha": probe_head_sha,
        "branch_push": branch_push,
        "pull_request_create": pull_request_create,
        "pull_request_ci": pull_request_ci,
        "guard_workflow": GUARD_WORKFLOW,
        "guard_workflow_run": guard_run,
        "pull_request_close": pull_request_close,
        "temporary_pr_number": pr_number,
        "stale_runtime_branch_quarantine_exercised": True,
        "stale_branch_archives": stale_branch_archives,
        "research_content_changed": False,
        "research_decision_made": False,
        "completed_at": utc_now(),
        "error": error,
    }
    save_json(OUT, record)
    if not passed:
        print(f"BOMA autonomy commission: FAIL — {error}", file=sys.stderr)
        return 5
    print(
        f"BOMA autonomy commission: PASS (archived {len(stale_branch_archives)} stale runtime branch(es); "
        f"temporary PR #{pr_number}; {GUARD_WORKFLOW} SUCCESS)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
