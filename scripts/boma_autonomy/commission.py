#!/usr/bin/env python3
"""Pre-START GitHub write/PR/CI plumbing commission test.

Creates a temporary control-plane-only branch and PR, proves that the dedicated
autonomy exact-head guard is triggered and succeeds without human approval, then
closes/deletes the probe. No BOMA research content or decision is changed.
"""
from __future__ import annotations

import json
import os
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

    try:
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
        "schema": "BOMA-AUTONOMY-COMMISSION-002",
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
        f"BOMA autonomy commission: PASS (temporary PR #{pr_number}; "
        f"{GUARD_WORKFLOW} SUCCESS)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
