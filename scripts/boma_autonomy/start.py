#!/usr/bin/env python3
"""Open the BOMA autonomy measurement window exactly once."""
from __future__ import annotations

import datetime as dt
import os
import sys

from core import (
    AUTONOMY,
    EXP_STATE,
    METRICS,
    current_head,
    load_json,
    run,
    save_json,
    start_frontier_errors,
)

DRY_RUN = AUTONOMY / "prestart-dryrun.json"
PREFLIGHT = AUTONOMY / "provider-preflight.json"
COMMISSION = AUTONOMY / "commission.json"


def main() -> int:
    errors = start_frontier_errors()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if os.environ.get("CONFIRM_EXPERIMENT_START") != "YES":
        print("Refusing START without CONFIRM_EXPERIMENT_START=YES", file=sys.stderr)
        return 3
    if not os.environ.get("AI_API_KEY"):
        print("Refusing START: AI_API_KEY unavailable", file=sys.stderr)
        return 4

    state = load_json(EXP_STATE)
    generation = str(state.get("experiment_generation") or "")
    if generation != "BOMA-AUTONOMY-004":
        print("Refusing START: experiment generation is not BOMA-AUTONOMY-004", file=sys.stderr)
        return 5
    if state.get("armed") or state.get("started_at"):
        print("Refusing START: experiment already started", file=sys.stderr)
        return 6
    if state.get("experiment_state") != "BOOTSTRAP":
        print("Refusing START: experiment_state is not BOOTSTRAP", file=sys.stderr)
        return 7

    if not COMMISSION.is_file():
        print("Refusing START: pre-START GitHub commission not recorded", file=sys.stderr)
        return 8
    commission = load_json(COMMISSION)
    if commission.get("passed") is not True:
        print("Refusing START: GitHub commission did not pass", file=sys.stderr)
        return 9
    commission_anchor = commission.get("main_anchor_sha")
    if not isinstance(commission_anchor, str):
        print("Refusing START: invalid commission anchor", file=sys.stderr)
        return 10
    ancestry = run(["git", "merge-base", "--is-ancestor", commission_anchor, "HEAD"])
    if ancestry["exit_code"] != 0:
        print("Refusing START: commission anchor is not an ancestor of current head", file=sys.stderr)
        return 11

    head = current_head()
    if not PREFLIGHT.is_file():
        print("Refusing START: realistic provider preflight not recorded", file=sys.stderr)
        return 12
    preflight = load_json(PREFLIGHT)
    if preflight.get("passed") is not True:
        print("Refusing START: realistic provider preflight did not pass", file=sys.stderr)
        return 13
    if preflight.get("experiment_generation") != generation:
        print("Refusing START: provider preflight belongs to another generation", file=sys.stderr)
        return 14
    if preflight.get("head_sha") != head:
        print("Refusing START: provider preflight head differs from current exact head", file=sys.stderr)
        return 15

    if not DRY_RUN.is_file():
        print("Refusing START: prestart dry run not recorded", file=sys.stderr)
        return 16
    dry = load_json(DRY_RUN)
    if dry.get("passed") is not True:
        print("Refusing START: prestart dry run did not pass", file=sys.stderr)
        return 17
    if dry.get("experiment_generation") != generation:
        print("Refusing START: dry run belongs to another generation", file=sys.stderr)
        return 18
    if dry.get("head_sha") != head:
        print("Refusing START: dry-run head differs from current exact head", file=sys.stderr)
        return 19

    validation = run([sys.executable, "scripts/boma_autonomy/validate.py"], timeout=600)
    if validation["exit_code"] != 0:
        print(validation["stdout"] + validation["stderr"], file=sys.stderr)
        print("Refusing START: runtime validation failed", file=sys.stderr)
        return 20

    now_dt = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    now = now_dt.isoformat()
    policy = load_json(AUTONOMY / "policy.json")
    window_cfg = policy.get("observation_window", {})
    hours = int(state.get("observation_window_hours") or window_cfg.get("default_hours", 168))
    if hours <= 0:
        print("Refusing START: observation_window_hours must be positive", file=sys.stderr)
        return 21
    deadline = (now_dt + dt.timedelta(hours=hours)).isoformat()
    window_id = f"MW-{now_dt.strftime('%Y%m%dT%H%M%SZ')}-{hours}H-G4"

    metrics = load_json(METRICS)
    state["armed"] = True
    state["experiment_state"] = "ACTIVE"
    state["current_stage"] = "READY_TO_EVALUATE_014_TO_015_TRANSITION"
    state["started_at"] = now
    state["finished_at"] = None
    state["observation_window_hours"] = hours
    state["observation_deadline"] = deadline
    state["measurement_window_id"] = window_id
    state["meta_review_due"] = False
    state["start_head_sha"] = head
    state["last_run_at"] = now
    state["last_run_result"] = "EXPERIMENT_STARTED"
    state["infrastructure_status"] = "AVAILABLE"
    state["final_status"] = "NOT_REACHED"
    metrics["started_at"] = now
    metrics["measurement_window_id"] = window_id
    save_json(EXP_STATE, state)
    save_json(METRICS, metrics)
    print(f"BOMA AUTONOMY GENERATION 004 STARTED at {now} on {head}; observation deadline {deadline}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
