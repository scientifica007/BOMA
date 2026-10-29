# AUTONOMOUS_RESEARCH_PROGRAM_GOVERNANCE_001 — Owner-Authorized Sequential Research

**Document ID:** `BOMA-ARP-GOV-001`  
**Status:** `PROPOSED GOVERNANCE / NO ACTIVE PROGRAM CREATED BY THIS DOCUMENT`  
**Date:** `2026-08-25`  
**Method:** PDSA — Plan → Do → Study → Act  
**Default safety posture:** `FAIL-CLOSED`

## 1. Purpose

BOMA may execute a pre-authorized sequence of controlled experiments without
requiring repeated owner approval for routine execution, recovery, closure, or
transition between experiments.

The owner authorizes the **research program**. The autonomous collaborator then
executes only what that program explicitly authorizes.

```text
OWNER AUTHORIZES RESEARCH PROGRAM
        ↓
E1 → transition gate → E2 → transition gate → E3 → ...
        ↓
continue while authority and scientific ordering remain valid
```

If evidence requires a material change to the authorized program, execution
stops rather than improvising.

```text
ambiguity / scope change / ordering change / new prerequisite
        ↓
OWNER_REQUIRED
```

## 2. Authority hierarchy

This governance does not weaken existing mathematical, architectural, Claim,
acceptance, provenance, or exact-head verification rules.

An autonomous research program is an **execution authority**, not a new source
of mathematical truth.

For current-state interpretation, the repository source-of-truth order remains
controlling. For autonomous execution specifically, additionally read:

```text
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_POLICY_001.json
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json
active program authorization record, if any
active experiment Frozen Plan, if any
```

If these sources disagree and the conflict cannot be resolved by an explicit
higher-priority repository authority, set `OWNER_REQUIRED`.

## 3. Program-level authorization

The owner may explicitly authorize a finite or bounded research program
containing an ordered experiment queue.

A valid authorization must declare at least:

```text
program_id
status = OWNER_AUTHORIZED
owner_authorization_record
baseline_main_sha
ordered_experiment_queue
per-experiment intended change point
program invariants
program non-goals
transition policy
routine merge authority, if any
stop conditions
completion condition
```

Authorization of a program counts as prior authorization to prepare and execute
the experiments listed in that program **only while their declared order and
prerequisites remain scientifically valid**.

Program authorization does not authorize:

```text
inventing a replacement program
silently reordering experiments
inserting a sequence-critical experiment
changing a Frozen Plan after Do begins
changing the single experimental factor
changing SELECTS
promoting an accepted export
rewriting an acceptance contract
adding an undeclared foundational/logical commitment
silently weakening exact verification
```

## 4. Experiment independence remains mandatory

Program-level authorization does not create one giant mutable Plan.

Each experiment still requires:

```text
re-read synchronized current main
verify exact baseline
exact typed architectural origin
one changed factor / fixed controls
affected Claim cone
independent immutable Frozen Plan
separate branch
Do
exact verification
Study
Act
lifecycle closure
```

The next experiment must be frozen from the then-current authorized baseline,
not copied mechanically from the previous experiment's branch state.

## 5. Autonomous experiment lifecycle

Within an authorized program, an agent may autonomously perform routine
lifecycle actions covered by the program:

```text
PREPARE
→ FREEZE_PLAN
→ DO
→ VERIFY
→ STUDY
→ ACT
→ CLOSE
→ TRANSITION_GATE
→ NEXT_EXPERIMENT
```

A mathematical hypothesis may close as either:

```text
CLOSED / PASS
CLOSED / INFORMATIVE FAIL
```

An informative mathematical failure is not itself an execution failure. After
closure, evaluate whether the next experiment remains valid.

## 6. Transition gate

Before starting the next queued experiment, verify all applicable conditions:

```text
previous experiment lifecycle is closed
required exact-head evidence is complete
all preserved provenance is recorded
current main is synchronized and re-read
no unresolved CI/governance failure remains
next experiment is explicitly present in the authorized queue
next experiment prerequisites still hold
its intended single changed factor remains meaningful
its baseline has not been invalidated
no newly discovered prerequisite must precede it
no authorized experiment must be reordered
no undeclared foundational/logical commitment is now required
no canonical/acceptance decision outside program authority is required
```

If all pass: `AUTO_CONTINUE`.

If any material condition fails or is ambiguous: `OWNER_REQUIRED`.

## 7. New research discoveries

Classify newly discovered experiment ideas in two classes.

### 7.1 Non-sequence-critical discovery

If the discovery is interesting but does not affect the validity or order of the
active program:

```text
record candidate under FUTURE_EXPERIMENT_CANDIDATE_PROTOCOL_001
status = CANDIDATE / NOT AUTHORIZED
continue current program
```

### 7.2 Sequence-critical discovery

If evidence indicates that a new experiment must be inserted before a queued
experiment, or that the approved order should change:

```text
record evidence and candidate dossier
set state = OWNER_REQUIRED
state exact proposed insertion/reordering
stop before modifying the approved queue
```

An agent may recommend a revised sequence but may not enact it without owner
authorization.

## 8. Recovery envelope

Technical and formalization failures that do not alter the Frozen Plan may be
diagnosed, documented, corrected, re-verified, and continued autonomously.

Examples include:

```text
namespace/qualification errors
proof-script goal-state errors
manifest/path mistakes
CI false positives
scoping errors
wrapper/unfolding errors
non-mathematical configuration defects
```

Recovery becomes `OWNER_REQUIRED` if correction would require:

```text
new mathematical assumption
new logical principle outside the Plan
changed experimental factor
changed success/failure criterion
expanded affected Claim cone with material architectural effect
accepted-source reinterpretation outside authorization
program reordering or insertion of a prerequisite experiment
```

## 9. Routine merge authority

Routine merge authority is **opt-in per owner-authorized research program**.
It is false unless the program record explicitly enables it.

Even when enabled, autonomous merge is allowed only when every declared gate is
satisfied, including exact verified head and required regressions.

Routine merge authority never by itself authorizes:

```text
SELECTS changes
acceptance promotion
acceptance-contract changes
canonical producer replacement
foundational commitment changes
logical regime changes beyond the experiment's declared scope
```

Such effects require an explicit owner authorization boundary in the program or
an `OWNER_REQUIRED` stop.

## 10. Stop conditions

Set `OWNER_REQUIRED` and make no further research-changing writes when any of
the following occurs:

1. The authorized queue should be reordered.
2. A new experiment must precede the next authorized experiment.
3. A Frozen Plan must change after Do begins.
4. The single changed factor must change.
5. A new foundational or logical assumption is required outside scope.
6. A canonical selection, accepted export, or acceptance contract requires a
   decision outside explicit program authority.
7. Repository authorities conflict materially.
8. Exact verification evidence cannot be classified safely.
9. Current main changed in a way that invalidates the active baseline or next
   experiment prerequisites.
10. The agent cannot determine whether an action is authorized.

The final rule is:

```text
AMBIGUOUS AUTHORITY => OWNER_REQUIRED
```

## 11. State machine

Allowed high-level states:

```text
NO_ACTIVE_PROGRAM
PROGRAM_READY
PREPARING_EXPERIMENT
PLAN_FROZEN
DO
WAITING_CI
RECOVERY_ALLOWED
STUDY
ACT
CLOSING
TRANSITION_GATE
PROGRAM_COMPLETE
OWNER_REQUIRED
```

`OWNER_REQUIRED` is terminal for autonomous research-changing actions until a
new explicit owner authorization updates the program/state.

## 12. Scheduled continuation semantics

A scheduled ChatGPT continuation is a wake-up mechanism, not the scientific
clock.

At each wake-up, the agent should execute all currently ready and authorized
work until reaching a genuine blocking gate such as:

```text
WAITING_CI
OWNER_REQUIRED
PROGRAM_COMPLETE
```

It should not stop merely because one small subtask finished.

## 13. No implicit activation

This governance document creates a capability only.

At introduction:

```text
ACTIVE AUTONOMOUS RESEARCH PROGRAM = NONE
ST2-EXP-004 = NOT ACTIVE
NO EXPERIMENT QUEUE IS OWNER-AUTHORIZED BY THIS DOCUMENT
```

A separate owner-approved program record is required before autonomous research
execution begins.
