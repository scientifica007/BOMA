# PDSA — Harmonize live governance after retirement of unattended research
**Date:** 2026-10-29  
**Authority:** `LAB/PDSA/OWNER_DECISION_2026-10-29_INTERACTIVE_PDSA_MODE.md`; owner instruction in the present session.  
**Baseline current main:** `3e8730bd35743a2ff25e13c264dcc4a42076aae7`  
**Type:** governance/control-plane maintenance only. No scientific experiment.

## Plan
Eliminate actionable unattended research authority from `AGENTS.md`,
`LAB/PDSA/STATUS.md`, the live program governance/policy/state, and their
consistency audit. Preserve:
- Existing program queue `014 → 015 → 016 → 017` as research agenda;
- ST2-EXP-015 CLOSED_PASS, ST2-EXP-016 NOT_STARTED / NO_FROZEN_PLAN,
  ST2-EXP-017 conditional, active state OWNER_REQUIRED;
- all accepted mathematics, `SELECTS`, Lean payloads, Claim contracts,
  frozen experimental Plans, and exact-head/CI evidence;
- 2026-08-25 historical program authorization and manifest, including its
  original `routine_merge_authorized: true`, as **historical evidence**
  superseded by the binding 2026-10-29 owner decision.

**Scope:** change five active governance/status files plus the governance audit,
and add this maintenance record. Do not edit `.autonomy/` historical runtime
state, `scripts/boma_autonomy/`, experiment records or accepted math. The
autonomous engine is already disabled manually in GitHub; the runtime is
unarmed. No workflow run or experiment is initiated by this maintenance.

## Do
- Add prominent current execution instructions in AGENTS/STATUS, clearly
  marking superseded 014→015 `current` prose as historical.
- Add binding Section 0 to the program governance document and retain the
  complete earlier governance model as a labelled historical reference.
- Disable automatic action and merge permissions in live program policy.
- Set effective `routine_merge_authorized: false` and owner-directed mode in
  the current program state; preserve its scientific closure and queue.
- Update the fail-closed governance audit so it confirms owner authorization,
  stopped state, empty autonomous actions, and explicitly differentiates the
  historical manifest's 2026-08-25 merge bit from today's revoked authority.

## Study — criteria and evidence
1. JSON policy/state parse; exact queue and scientific frontier unchanged.
2. Only intended governance/control-plane paths changed; no Lean or accepted
   manifests, program manifest, Closed Plans or research artifacts.
3. `python3 LAB/PDSA/tools/autonomous_research_program_audit.py`,
   `python3 scripts/boma_autonomy/validate.py`,
   `python3 -m unittest discover -s tests/boma_autonomy -v`,
   architecture/claim audits and required exact-head PR checks must pass before
   Act approval. A pending/failed check is not a PASS.
4. Confirm no `AUTO_CONTINUE` or routine auto-merge is presented as current
   authority. Retained references must be clearly marked as archived.

## Act — owner decision gate
Create a reviewable PR and **do not auto-merge**. The owner alone decides
whether to merge after reviewing the changed files and CI. No new scientific
experiment, plan, autonomy activation, credential change, branch deletion, or
PR merge is implied by this PDSA maintenance task.

**Remaining separate infrastructure risk:** repository-admin review of unused
`AUTONOMY_GH_TOKEN` / `AI_API_KEY` (never inspect or disclose values),
and further workflow/tooling simplification, require separate owner instructions.
