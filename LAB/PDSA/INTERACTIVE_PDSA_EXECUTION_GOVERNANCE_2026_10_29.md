# BOMA Interactive PDSA Execution Governance — 2026-10-29

**Status:** CURRENT / OWNER-DIRECTED / FAIL-CLOSED
**Authority:** `LAB/PDSA/OWNER_DECISION_2026-10-29_INTERACTIVE_PDSA_MODE.md` (PR #26)
**Policy:** `LAB/PDSA/INTERACTIVE_PDSA_EXECUTION_POLICY_2026_10_29.json`

## Binding authority
The owner revoked unattended Agents, autonomous research, scheduled research
wakes, automatic experiment transitions, technical recovery without current
task authorization, and autonomous PR merges. All changes require a
specific owner instruction in the current interactive session.

This document supersedes the *execution* provisions of the historical
`AUTONOMOUS_RESEARCH_PROGRAM_GOVERNANCE_001.md` and old program policy.
Those historical files remain byte-identical because ST2-EXP-015 frozen
verification pins their original bytes. They retain scientific and decision
provenance but **not current operational authority**.

The 2026-08-25 ST2-RP-001 Manifest and its
`routine_merge_authorized: true` value are historical authorization
evidence, not current permission. Likewise, the backward-compatible
`routine_merge_authorized: true` field in current program state exists
only to preserve frozen verification. Read the later
`effective_execution_authority.routine_merge_authorized: false` field
and this policy for binding current execution decisions.

## Mandatory PDSA in each owner-instructed task
1. **Plan:** read actual GitHub current main; fix task authorization, typed
   architectural origin, single changed factor for scientific research,
   controls, affected claims, success/failure criteria and evidence strategy.
   Freeze each scientific experiment's independent Plan before Do.
2. **Do:** use a separate branch within the authorized task; no research
   changes directly on main. Preserve accepted R/C producers and `SELECTS`,
   formal proofs, contracts, closed evidence and Frozen Plans.
3. **Study:** require independent exact-head CI/Lean verification, dependency
   and axiom evidence, failure logs, controls and provenance. Distinguish
   mathematical informative failure from technical failures.
4. **Act:** record learning and recommendations. Only the owner authorizes
   the next task, experiment, selection/acceptance change or PR merge.
   Successful research is not automatic acceptance promotion.

Verification-only GitHub Actions are allowed; unattended scientific judgment,
research execution, scheduling and merges are prohibited. Ambiguous authority
means OWNER_REQUIRED and no research-changing action.

## Current research frontier
ST2-RP-001 queue 014 → 015 → 016 → 017 remains research agenda, not
blanket execution consent. ST2-EXP-015 is CLOSED_PASS (PR #25).
ST2-EXP-016 is NOT_STARTED / NO_FROZEN_PLAN, scientific prerequisites MET,
but requires new owner instruction. ST2-EXP-017 is contingent upon 016.
State remains OWNER_REQUIRED; G8 is unarmed and its Workflow was manually
disabled. The accepted Dedekind R and C Route P selections remain unchanged.

**Fail-closed invariants:** NO SESSION INSTRUCTION → NO NEW TASK;
NO OWNER MERGE APPROVAL → NO MERGE; NO AUTONOMOUS CONTINUATION.
