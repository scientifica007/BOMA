# AGENTS.md — BOMA continuation rules

<!-- BOMA_AUTONOMY_RUNTIME_STATE_BEGIN -->
### Autonomous runtime current-state marker

This block is maintained by the autonomous runtime and supersedes older
current-frontier prose below it when the two disagree. Historical records
remain immutable evidence of their own time.

```text
STATE: PREPARING_EXPERIMENT
PROGRAM: ST2-RP-001
QUEUE_CURSOR: 1
ACTIVE_EXPERIMENT: None
LATEST_COMPLETED: ST2-EXP-014
NEXT_EXPERIMENT: ST2-EXP-015
TRANSITION_FROM: ST2-EXP-014
TRANSITION_CANDIDATE: ST2-EXP-015
TRANSITION_DECISION_RECORDED: True
NEXT_LEGAL_ACTION: CREATE_INDEPENDENT_ST2-EXP-015_BRANCH_AND_FREEZE_PLAN_BEFORE_DO
```

Runtime note: Autonomous transition gate ST2-EXP-014→ST2-EXP-015: AUTO_CONTINUE; ST2-EXP-015 not started.
<!-- BOMA_AUTONOMY_RUNTIME_STATE_END -->


Mandatory for AI agents and other automated collaborators.

## 1. Read current state before acting

Read, in order:

```text
README.md
LAB/PDSA/STATUS.md
LAB/PDSA/BASELINE_INTEGRITY_AUDIT_AUTONOMY_001.md
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_GOVERNANCE_001.md
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_POLICY_001.json
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json
LAB/PDSA/RESEARCH_PROGRAM_ST2_RP_001_R_C_COMPOSITIONALITY_MINIMALITY.md
LAB/PDSA/ST2_RP_001_PROGRAM_MANIFEST_001.json
LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md
LAB/PDSA/STAGE_TWO_BRANCH_ORIGIN_LEDGER_001.json
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_003.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_002.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_001.md
LAB/PDSA/PDSA-ST2-EXP-004_R_TOTAL_ORDER_LOGICAL_REGIME.md
LAB/PDSA/experiments/ST2-EXP-004_FINAL_STUDY_ACT_001.md
LAB/PDSA/experiments/ST2-EXP-004_LIFECYCLE_CLOSURE_001.md
LAB/PDSA/experiments/ST2-EXP-014_FINAL_STUDY_ACT_001.md
LAB/PDSA/experiments/ST2-EXP-014_LIFECYCLE_CLOSURE_001.md
LAB/00_ARCHITECTURE/GRAPH.md
LAB/00_ARCHITECTURE/REGISTRY.md
LAB/00_ARCHITECTURE/R_DAG.md
LAB/10_CONSTRUCTION/decisions/R-DP-003/UNIT.md
LAB/00_ARCHITECTURE/C_R_DEPENDENCY_CONTRACT.md
LAB/10_CONSTRUCTION/blocks/C-COMPARE-BLOCK-001/UNIT.md
LAB/00_ARCHITECTURE/views/CONSTRUCTION_DAG_VIEW.md
LAB/00_ARCHITECTURE/views/LEARNING_GRAPH_VIEW.md
```

If a later program supersedes `ST2-RP-001`, follow the exact active-program
paths named by `AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json` rather than assuming
these two current paths remain active forever.

Historical records preserve provenance; they do not override later synchronized current-state authorities.

## 2. Current structural state

```text
Pre-numerical layer   CALIBRATED
N-Core                N-BLOCK-007 ACCEPTED
N-Arithmetic          N-ARITH-BLOCK-001 ACCEPTED
Z                     Z-BLOCK-002 ACCEPTED
Q                     Q-BLOCK-002 ACCEPTED
R                     R-DP-001 SELECTS Dedekind / R-BLOCK-001 ACCEPTED
R logical regime      R-DP-003 SELECTS localized classical CutComparability
R learned boundary    RTotality ↔ CutComparability / ST2-EXP-004 INTEGRATED
R alternative         R-ROUTE-C / Cauchy PERMANENT VERIFIED / NON-SELECTED
R alt Junction        ST2-EXP-003-R-J-001 / NON-ACCEPTANCE
C production R→C      BOMA-C-R-DEP-001 / exact sixteen-property surface
C                     C-DP-001 SELECTS C-ROUTE-P / C-BLOCK-002 / CA-20 ACCEPTED
C comparison          C-COMPARE-BLOCK-001 / five scalar ops + coordinate laws
C alternative         C-ROUTE-Q PERMANENT VERIFIED / NON-SELECTED
C alt Junction        ST2-EXP-002-PQ-J-001 / NON-ACCEPTANCE
ST2-EXP-001..004+011  CLOSED / PASS / VERIFIED LESSONS INTEGRATED
ST2-EXP-014           CLOSED / PASS / EXACT CLOSURE VERIFIED / ROUTINE MERGED
ACTIVE EXPERIMENT     NONE
AUTONOMOUS PROGRAM    ST2-RP-001 / OWNER_AUTHORIZED
ACTIVE STATE          TRANSITION_GATE
AUTHORIZED QUEUE      ST2-EXP-014 → ST2-EXP-015 → ST2-EXP-016 → ST2-EXP-017
TRANSITION            ST2-EXP-014 → ST2-EXP-015 / DECISION NOT YET RECORDED
NEXT CANDIDATE        ST2-EXP-015 / AUTHORIZED / QUEUED / NOT STARTED
015 BRANCH            NONE
015 FROZEN PLAN       NONE
SYNCHRONIZED MAIN     2a6c38af70e596c840ef2db4733421bde38f3ee5
ROUTINE MERGE         TRUE / EXACT PROGRAM-SCOPE GATES ONLY
REQUIRED NEXT ACT     re-read synchronized main → evaluate 014→015 transition gate
```

Historical proposed IDs `ST2-EXP-005..013` remain candidate history and are not
implicitly authorized or repurposed.

## 3. Authority distinction and fail-closed posture

Two execution-authority mechanisms exist and must not be conflated:

```text
A. specific direct owner authorization for an experiment or bounded maintenance Act
B. exact scope of an OWNER_AUTHORIZED autonomous research program
```

The current autonomous-program machine state is:

```text
state = TRANSITION_GATE
active_program_id = ST2-RP-001
authorized_experiment_queue = [ST2-EXP-014, ST2-EXP-015, ST2-EXP-016, ST2-EXP-017]
queue_cursor = 0
active_experiment = null
transition_from = ST2-EXP-014
transition_candidate = ST2-EXP-015
transition_decision_recorded = false
synchronized_main_sha = 2a6c38af70e596c840ef2db4733421bde38f3ee5
routine_merge_authorized = true
```

Program authority is bounded by:

```text
LAB/PDSA/RESEARCH_PROGRAM_ST2_RP_001_R_C_COMPOSITIONALITY_MINIMALITY.md
LAB/PDSA/ST2_RP_001_PROGRAM_MANIFEST_001.json
```

The autonomous program policy remains fail-closed:

```text
AMBIGUOUS AUTHORITY => OWNER_REQUIRED
```

Queue reordering, a sequence-critical new prerequisite, Frozen-Plan factor
change, out-of-scope assumption, SELECTS/acceptance/canonical change, or an
unresolved authority conflict requires `OWNER_REQUIRED` before the change.

## 4. Learning-to-Construction rule

A successful experiment may, after Study/Act and lifecycle closure, and only under applicable owner authority, be integrated into the permanent Construction DAG as **verified knowledge**.

Allowed integration includes:

```text
refine dependency contract
refine an existing Block or Decision Point's dependency/logical classification
retain permanent verified alternative branch
retain permanent verified non-acceptance Junction
expose representation-independent invariant
record sensitivity/genericity condition
```

Never infer:

```text
permanent DAG visibility = SELECTS
permanent DAG visibility = accepted export
verified alternative = canonical producer
successful experiment = automatic promotion
integrated dependency knowledge = accepted implementation refactor
shared generic interface = Junction
formal proof ancestry = mathematical necessity
```

`ST2-RP-001` grants conditional routine merge authority only for program-scope
research/lifecycle records and verified-knowledge integration satisfying its
exact gates. It does not authorize accepted-source replacement, SELECTS change,
acceptance promotion, or acceptance-contract revision.

## 5. Exact C-production R→C mathematical dependency rule

`ST2-EXP-001` established the canonical **production** mathematical surface of `BOMA-C-R-DEP-001`:

```text
orderTrans
orderAntisymm
orderTotal
nontrivial
addComm
addAssoc
addZeroLeft
addInverseRight
addTranslateOrderIff
negOrderReversing
mulComm
mulAssoc
mulOneLeft
distribRight
orderMulNonneg
inverseExists
```

Formal witness:

```text
BOMA.C.StageTwo.NarrowRInterface001.NarrowROrderedFieldCertificate
BOMA.C.StageTwo.NarrowRInterface001.narrowRFromAcceptedProducers
```

Do not confuse accepted-source formal ancestry with mathematical necessity.

`ST2-EXP-016` is authorized to test replacement of exactly `orderTotal` by one
exact algebraic nondegeneracy condition selected before Do and frozen in that
experiment's independent Plan. Until 016 supplies evidence, the sixteen-field
surface remains the current production authority.

## 6. Exact C comparison dependency rule — ST2-EXP-011

The integrated direct comparison scalar operations are:

```text
zero
one
neg
add
mul
```

with explicit quadratic coordinate laws:

```text
coord
coordinateGeneration
coordinateUnique
coordinateZero
coordinateOne
coordinateReal
coordinateImag
coordinateNeg
coordinateAdd
coordinateMul
```

This comparison closure is not the whole C-production closure. The accepted `CQuadraticComparison001` source has not been replaced by the experimental generic source.

## 7. Relation/function firewall

For quadratic comparison:

```text
relation totality + uniqueness
!=
chosen functional comparison
```

An actual comparison function requires explicit `CoordinateExtractor` data. Never introduce a global coordinate selector or inverse selector merely for convenience.

## 8. R-DP-003 logical-regime rule — ST2-EXP-004 integrated

`R-DP-003` remains resolved and selected as:

```text
constructive rLE partial-order core
+
localized classical F-04 witness of CutComparability
+
constructive totality-from-CutComparability bridge
```

The exact ST2-EXP-004 frozen authority remains historical and immutable:

```text
accepted reference  50f3031b8d2657cbe0710e73e5935d997d40e49b
accepted tree       e4842acdf2b08c8db54b45d0798c36ee7565f351
Frozen Plan commit  89c9dc9154e7ca469e5c94c177be223205ee9dbd
Frozen Plan blob    1bd97aebb7e36ed5f7647ce29461c9c24b3cc9ba
Final Study/Act      6779d028c49f73757ea838c163d3968a982559fe
exact closed head   1fe760de811ad2b176ead6f420b80ca1aab5ce46
research merge      61adb8589c803e95e1b96ef38902320c8aa5df19
integration         BOMA-ST2-LEARNING-INTEGRATION-003
```

The integrated same-carrier boundary is:

```text
RTotality ↔ CutComparability
```

No unconditional constructive `CutComparability` was recovered from the frozen `LowerCut` fields.

The current measured F-04 declaration impact is:

```text
F04_DIRECT             8
F04_TRANSITIVE         7
F04_FREE              22
OTHER_CLASSICAL_ONLY  18
```

Gate B's `77 / 88` result is whole-source survivor/packaging evidence, not a theorem of mathematical necessity.

Independent controls remain:

```text
F-05 finite membership / bracketing
F-06 positive representative extraction
F-07 rational density
```

Therefore always preserve:

```text
NO F-04 dependency ≠ fully constructive R
conditional CutComparability ≠ constructive recovery
failure to recover totality ≠ impossibility theorem
formal declaration ancestry ≠ mathematical necessity
whole-source elaboration dependency ≠ theorem dependency
```

A located-cut redesign changes the representation and is outside `ST2-RP-001`.
Record it only as a future candidate unless separately owner-authorized.

## 9. ST2-EXP-004 downstream C sensitivity rule

Gate E removed exactly `orderTotal` from the ST2-EXP-001 sixteen-property production interface.

Surviving accepted C Claim families:

```text
C-CL-CARRIER-001
C-CL-REMBED-001
C-CL-I-001
C-CL-GEN-001
C-CL-COORDUNIQ-001
C-CL-NONREAL-001
C-CL-COMPARE-001
```

The current proof closures for `C-CL-FIELD-001` and `C-CL-INTEGRATION-001` did not survive; measured dependence is transitive through the current square/nonnegative → norm → field path. Do not state this as mathematical necessity.

`C-CL-COMPARE-001` remains governed by the smaller ST2-EXP-011 comparison interface.

## 10. Decision / alternative discipline

### R

```text
R-DP-001 SELECTS R-ROUTE-D / Dedekind
R-BLOCK-001 is accepted
R-ROUTE-C / Cauchy is permanent verified alternative
ST2-EXP-003-R-J-001 is permanent verified non-acceptance Junction
R-DP-003 SELECTS localized classical comparability for Stage I
ST2-EXP-004 refines R-DP-003 knowledge; it does not replace the Decision Point
```

### C

```text
C-DP-001 SELECTS C-ROUTE-P
C-BLOCK-001 is selected producer
C-COMPARE-BLOCK-001 owns C-CL-COMPARE-001
C-J-001 is accepted integration Junction
C-BLOCK-002 / CA-20 is accepted export
C-ROUTE-Q is permanent verified alternative
ST2-EXP-002-PQ-J-001 is permanent verified non-acceptance Junction
```

Program experiments 014–017 test robustness/minimality/generalization while
these selected/accepted facts remain controls.

## 11. Stage-Two lifecycle rule

Closed and integrated/retained:

```text
ST2-EXP-001
ST2-EXP-002
ST2-EXP-003
ST2-EXP-011
ST2-EXP-004
ST2-EXP-014 / CLOSED PASS / research-only evidence retained
```

Current program:

```text
ST2-RP-001 OWNER_AUTHORIZED / TRANSITION_GATE
queue: 014 → 015 → 016 → 017
active experiment: NONE
latest completed: ST2-EXP-014 / CLOSED PASS / exact closure verified / routine merged
transition: 014 → 015 / decision not yet recorded
next candidate: ST2-EXP-015 / AUTHORIZED / QUEUED / NOT STARTED
```

Historical closure is monotone evidence. Never mutate closed Frozen Plan, Study/Act, failure, run, artifact, merge, or lifecycle records.

Each new queued experiment gets a separately frozen Plan from then-current
synchronized main. Do not freeze 015–017 in advance.

## 12. Accepted-source firewall

Do not change without a separate explicit accepted architectural decision:

```text
accepted Q/R/C manifests or their manifest-listed mathematical sources
R-DP-001 selection
R-DP-003 Stage-I logical-regime selection
R-BLOCK-001 accepted export
current BOMA-C-R-DEP-001 production authority except as research-only test under 016
C-DP-001 selection
C-J-001
C-BLOCK-002 / CA-20
```

Program-scope research may construct independent research producers/interfaces
and compare them against these controls. A PASS is not automatic promotion.

## 13. Status authority

When current-state documents conflict, prefer:

```text
LAB/PDSA/STATUS.md
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_GOVERNANCE_001.md
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_POLICY_001.json
LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json for autonomous-program state only
active owner-authorized program record named by state
active program machine manifest named by state
LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md
LAB/PDSA/STAGE_TWO_BRANCH_ORIGIN_LEDGER_001.json
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_003.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_002.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_001.md
relevant architecture / DAG / Decision / Block / acceptance / Claim records
claim-level exact evidence
README.md / AGENTS.md
historical checkpoints
```

The autonomous state/program files govern execution scope; they may not rewrite mathematical or architectural facts.

The old top-level stop markers in `STAGE_TWO_BRANCH_ORIGIN_LEDGER_001.json` were
correct at the completed 004 frontier. When they conflict with the later
explicit `ST2-RP-001` authorization or the synchronized post-014 state, treat
them as historical current-frontier metadata; do not mutate closed experiment
origin records. New experiment typed origins are carried by the active program
manifest and must enter permanent origin records as each experiment is
independently frozen.

## 14. Verification rules

Historical ST2-EXP-004 and ST2-EXP-014 evidence remains immutable and must
continue to verify as historical closure. Do not reinterpret historical
`NO_ACTIVE_PROGRAM` or `CLOSING` sentinels as current state after their later
authorized transitions completed.

For the synchronized pre-autonomy baseline verify:

```text
program authorization baseline == 1fac73b24b9b2e0db9dafc95e1944267aa9040da
synchronized post-014 main == 2a6c38af70e596c840ef2db4733421bde38f3ee5
014 exact closure head == 19cc6541457b3e8c58ea4607198d2474cd293dc9
014 exact V5 / lifecycle / governance checks == PASS
014 routine merge == COMPLETE with no tree drift
state == TRANSITION_GATE
active_program_id == ST2-RP-001
queue == [014,015,016,017] exactly and without duplicates
active_experiment == null
015 branch == none
015 Frozen Plan == none
transition decision 014→015 == not yet recorded
routine merge authority == true in authorization + state + manifest
accepted selections/exports unchanged
no research decision is made by baseline synchronization itself
```

Pinned Lean toolchain for historical experiment evidence:

```text
leanprover/lean4:v4.32.1
Lake packages: none
```

## 15. GitHub continuation rule

Do not conduct experiment work on `main`.

Current legal sequence:

```text
re-read synchronized main 2a6c38af70e596c840ef2db4733421bde38f3ee5
→ evaluate exact ST2-EXP-014 → ST2-EXP-015 transition gate
→ AUTO_CONTINUE only if every declared gate remains valid
→ create independent ST2-EXP-015 branch
→ freeze immutable 015 Plan before Do
→ execute/verify/Study/Act/close 015
→ evaluate exact 015→016 transition gate
```

The same pattern applies at every program transition. Routine merge authority is
active only within exact `ST2-RP-001` scope and gates.

Do not:

```text
work directly on main
start or freeze 015 before the 014→015 transition gate is positively recorded
start 016 before 015 lifecycle closure + transition gate
start 017 without the exact sufficient algebraic interface required from 016
insert/reorder a sequence-critical experiment
change a Frozen Plan after Do
promote selected/accepted/canonical mathematics under routine merge authority
```

Any such need sets `OWNER_REQUIRED`.