# BOMA autonomy bootstrap log

## 2026-08-26 — Runtime installation

The autonomy runtime was installed **before valid START**.

Bootstrap anchor before runtime installation:

`8344d8fab5b2e02568cdc41126701da1d1b58ae7`

Research baseline at installation:

- `ST2-RP-001 = OWNER_AUTHORIZED`
- `ST2-EXP-014 = CLOSED / PASS / exact closure verified / routine merged`
- BOMA state = `TRANSITION_GATE`
- transition = `ST2-EXP-014 → ST2-EXP-015`
- `ST2-EXP-015 = AUTHORIZED / QUEUED / NOT STARTED`
- no 015 branch
- no 015 Frozen Plan

No API credential is stored in this repository. A provider key is required only
for explicit preflight/dry-run/START and later active wakes.

This bootstrap does not decide the 014→015 transition gate and does not execute
a research PDSA cycle.

## 2026-08-26 — Outer observation-window rule confirmed

Before valid START, the autonomy experiment is configured to support a bounded
outer observation window around many inner autonomous BOMA PDSA cycles.

Current bootstrap default:

- observation window: `168 hours` (7 days);
- schedule: wake-up mechanism only, currently every 6 hours;
- human mode while the window is open: `READ_ONLY`;
- research writes: fork only (`scientifica007/BOMA`);
- upstream/original BOMA repository: never a write target;
- at the first wake on or after the deadline: pause before new research work and
  persist `PAUSED_FOR_META_REVIEW`;
- a later continuation requires a new measurement window rather than silently
  altering the measured run.

The duration is a bootstrap parameter and may be changed before valid START
without making a mathematical decision. No valid START has occurred yet.

## 2026-08-26 — Post-installer cleanup integrity

The temporary one-shot bootstrap installer/carrier and payload chunks were
removed after runtime installation. The only changes after the successful
runtime/governance validation head `a001eddac77065445986811b71db8f21e750d1fa`
were deletions of those temporary bootstrap transport files. No installed
`.autonomy`, `scripts/boma_autonomy`, `tests/boma_autonomy`, permanent workflow,
or BOMA research file was changed by that cleanup.

This log update is pre-START control-plane documentation and is intended to
trigger a fresh governance/runtime validation on the current `main` head.

## 2026-08-26 — Generation 002 technical stop

Generation 002 reached a valid START at `2026-08-26T20:41:22+00:00` and then
failed closed on its first research wake before any transition decision was
recorded, before any `ST2-EXP-015` Frozen Plan was created, and before any
research file was changed.

The failure was technical rather than mathematical:

- the transition evidence packet expected autonomy-era JSON artifacts for
  `ST2-EXP-014`, although 014 had completed before the autonomy runtime existed;
- the transition auditor returned the recognized semantic value
  `OWNER_REQUIRED` under the key `audit_result` rather than the contracted key
  `decision`, and the controller rejected the schema mismatch fail-closed.

The complete Generation 002 Meta-Study is preserved in
`.autonomy/meta-study-generation-002.json`. Measurement counters at the stop
remained `HRIC = 0`, `HIIC = 0`; no 014→015 decision was accepted.

## 2026-08-26 — Generation 003 Meta-PDSA bootstrap

Generation 003 is a pre-START technical repair generation only. Its frozen
Meta-Plan is `.autonomy/meta-plan-generation-003.json`.

The repair adds a provenance-preserving historical compatibility layer for the
already completed `ST2-EXP-014`, narrowly canonicalizes the single observed
transition-response key alias, and extends the synthetic provider preflight to
exercise that response contract. It does not evaluate the 014→015 gate and does
not change any mathematical factor, queue order, SELECTS edge, accepted export,
or acceptance contract.

Generation 002 commission/preflight/dry-run evidence is invalidated. Generation
003 must complete a fresh post-merge commission, exact-head provider preflight,
synthetic dry run, and valid START before research autonomy resumes.
