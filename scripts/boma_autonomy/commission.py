#!/usr/bin/env python3
"""Pre-START GitHub write/PR plumbing commission test.

Creates a temporary control-plane-only branch and PR, then closes/deletes it.
No BOMA research content or decision is changed.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import time

from core import AUTONOMY, EXP_STATE, ROOT, current_head, load_json, run, save_json, start_frontier_errors, utc_now

OUT = AUTONOMY / "commission.json"


def gh(args: list[str], *, check: bool = True) -> dict:
    env = os.environ.copy()
    token = env.get("GH_TOKEN") or env.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN/GITHUB_TOKEN unavailable")
    env["GH_TOKEN"] = token
    return run(["gh", *args], env=env, timeout=180, check=check)


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
        run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"], check=True)

        created = gh([
            "pr", "create", "--base", "main", "--head", branch,
            "--title", "Autonomy pre-START commission probe",
            "--body", "Synthetic control-plane plumbing test only. No BOMA research decision or content change."
        ])
        view = gh([
            "pr", "view", branch, "--json", "number,state,headRefName,baseRefName,url"
        ])
        data = json.loads(view["stdout"])
        pr_number = int(data["number"])
        if data.get("state") != "OPEN" or data.get("headRefName") != branch or data.get("baseRefName") != "main":
            raise RuntimeError(f"unexpected commission PR state: {data}")
        gh(["pr", "close", str(pr_number), "--delete-branch"])
        passed = True
    except Exception as exc:
        error = str(exc)
    finally:
        run(["git", "reset", "--hard"], check=False)
        run(["git", "checkout", "main"], check=False)
        run(["git", "fetch", "origin", "main"], check=False)
        run(["git", "reset", "--hard", "origin/main"], check=False)
        if branch:
            run(["git", "push", "origin", "--delete", branch], check=False)

    record = {
        "schema": "BOMA-AUTONOMY-COMMISSION-001",
        "passed": passed,
        "main_anchor_sha": anchor,
        "branch_push": passed,
        "pull_request_create": passed,
        "pull_request_close": passed,
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
    print(f"BOMA autonomy commission: PASS (temporary PR #{pr_number})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
