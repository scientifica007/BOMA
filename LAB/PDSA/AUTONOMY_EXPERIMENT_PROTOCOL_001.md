# BOMA Autonomous Research Experiment Protocol 001

**Status:** PRE-START / BOOTSTRAP  
**Measurement target:** autonomous execution of the already owner-authorized `ST2-RP-001` research program from the synchronized post-`ST2-EXP-014` frontier.  
**Research baseline before engine installation:** `8344d8fab5b2e02568cdc41126701da1d1b58ae7`.

## 1. Experimental question

Can an AI-controlled research runtime continue BOMA from the synchronized
`ST2-EXP-014 → ST2-EXP-015` transition gate through the remaining authorized
program, preserving BOMA governance, exact evidence, immutable Frozen Plans,
formal verification, failure provenance, and routine-merge gates, without human
research-development intervention after a valid START?

This is an experiment on the autonomy mechanism. It is not an authorization to
change the mathematical scope of `ST2-RP-001`.

## 2. Measurement boundary

Before valid START, bootstrap work may install, validate, repair, or replace the
autonomy runtime. Such work is not counted as a human research intervention
because the measurement window has not opened.

A valid START opens the measurement window. After that point:

```text
HRIC = Human Research Intervention Count
HIIC = Human Infrastructure Intervention Count
```

Target:

```text
HRIC = 0
```

A human research intervention includes directing a proof, selecting a lemma,
choosing a mathematical replacement condition, changing a Frozen Plan, telling
the runtime which research result to prefer, reordering/inserting an experiment,
or otherwise supplying development guidance that the autonomous program was
supposed to decide inside its authority.

A human infrastructure intervention is limited to external operational failures
such as unavailable provider credentials, GitHub Actions failure external to
repository logic, account/quota failure, or equivalent infrastructure. Any such
intervention after START must be recorded and increments `HIIC`.

Read-only observation does not increment either metric.

## 3. Valid START

START is valid only when all of the following hold on the same exact checked-out
`main` head:

1. the synchronized BOMA research state is still the post-014 `TRANSITION_GATE`;
2. `ST2-EXP-015` has not started and has no Frozen Plan;
3. BOMA autonomous-governance audit passes;
4. autonomy-runtime validation and tests pass;
5. a pre-START commission probe has successfully tested Git branch push and pull-request creation/closure using the GitHub Actions token;
6. an AI-provider preflight passes with the configured provider;
7. a synthetic technical dry run exercises the AI JSON roles without making a
   BOMA research decision or editing BOMA research content;
8. the dry-run record names the exact START head and reports `passed=true`;
9. the experiment state is explicitly transitioned from `BOOTSTRAP` to `ACTIVE`
   with a UTC timestamp.

If any condition fails, START is invalid and the measurement window remains
closed.

## 4. Separation of authority

The runtime has no authority beyond the existing owner-authorized program:

```text
ST2-RP-001
ST2-EXP-014 → ST2-EXP-015 → ST2-EXP-016 → ST2-EXP-017
```

The runtime may evaluate declared transition gates, prepare and freeze each
remaining Plan, execute within the Frozen Plan, recover from technical defects
inside the declared recovery envelope, verify, Study, Act, close, routine-merge,
and continue when the existing program says `AUTO_CONTINUE`.

It may not silently:

- change queue order;
- insert a sequence-critical experiment;
- modify a Frozen Plan after Do;
- change more than the authorized single scientific factor;
- add an out-of-scope foundational or logical principle;
- change `SELECTS`, accepted exports, canonical producers, or acceptance
  contracts;
- reinterpret a research PASS as acceptance promotion.

Any such need sets `OWNER_REQUIRED` and stops autonomous research.

## 5. Git and exact-evidence discipline

Research work is never performed directly on `main`.

The runtime uses deterministic `autonomy/*` branches and pull requests. A Frozen
Plan is committed before Do. The exact Plan commit is recorded and the Plan must
remain byte-identical thereafter.

A research/lifecycle branch may be merged only when:

- the exact current branch head has completed required checks successfully;
- the Frozen Plan remains unchanged;
- required deterministic Plan verification passes;
- BOMA governance and architecture audits pass;
- Study/Act and lifecycle closure are complete where applicable;
- no unresolved deviation or `OWNER_REQUIRED` condition exists.

Post-merge state synchronization is administrative lifecycle work and occurs in a
separate `autonomy/postmerge-*` branch. It does not itself decide the next
transition gate.

## 6. Control plane

`.autonomy/` is the experiment control plane. It is not BOMA mathematical
content. The research executor cannot edit it.

The controller may persist measurement state and metrics on `main`. These
control-plane commits do not constitute research decisions and must not modify
BOMA mathematical or governance content.

While an autonomy research PR is open, `main` may therefore advance only through
`.autonomy/` control-plane commits. Immediately before any routine merge the
controller must prove that every `main` change since the branch merge-base is
inside `.autonomy/`. Any non-control-plane drift means
`BASELINE_INVALIDATED_BY_MAIN_CHANGE` and must fail closed. For exact-evidence
purposes, "no post-verification research-content drift" excludes this explicitly
separated measurement control plane but excludes nothing in BOMA research,
governance, architecture, Lean, or lifecycle content.

The authoritative BOMA program state remains:

`LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json`.

## 7. Scheduled continuation

Scheduled execution is only a wake-up mechanism. The clock does not determine
scientific progression.

Each wake continues from exact repository/PR evidence until it reaches an
external wait state such as pending CI, `OWNER_REQUIRED`, or
`PROGRAM_COMPLETE`.

## 8. Outer observation window / Meta-PDSA checkpoint

The autonomous BOMA runtime may execute many inner PDSA research cycles without
human research intervention while an outer observation window is open. The
default pre-START window is 168 hours (7 days), but the duration is a bootstrap
parameter and may be changed before valid START without changing mathematics.

During an open observation window:

- scheduled wakes continue to advance the authorized research program;
- human activity is read-only observation only;
- no human mathematical suggestion, plan repair, proof hint, queue change, or
  experiment-selection guidance is permitted;
- the upstream/original BOMA repository is never a write target; all autonomous
  branches, pull requests, merges, and control-plane commits are confined to the
  experimental fork named by runtime policy;
- `HRIC` must remain zero for a clean no-human-research-intervention run.

At the first scheduled wake at or after the deadline, the controller pauses
**before starting new research work**, persists `PAUSED_FOR_META_REVIEW`, and
leaves the repository as a stable observation snapshot. This pause is
pre-authorized before START and therefore is not a human intervention.

A later continuation, if desired, must open a new measurement window. Any
change to the autonomy engine based on the Meta-Study belongs to a later
Meta-PDSA generation rather than being silently introduced into the measured
window.

## 9. End condition

The experiment reaches its intended endpoint when `ST2-RP-001` reaches
`PROGRAM_COMPLETE` after `ST2-EXP-017` lifecycle closure and program-level
synthesis, or when the program legitimately stops at `OWNER_REQUIRED`.

A stop is not automatically a failed autonomy experiment. Final Meta-Study must
classify why the stop occurred and report HRIC, HIIC, autonomous recovery
attempts, exact evidence, and any governance deviations.
