# BOMA — Project Handoff / START HERE

BOMA builds a transparent, traceable mathematical architecture from a declared pre-numerical constructional layer toward standard number systems.

Governing method: **PDSA — Plan → Do → Study → Act**. Historical `PDCA` identifiers are provenance only.

## Current accepted spine

As of 2026-08-26:

```text
framework-neutral pre-numerical layer   CALIBRATED
        ↓
N-BLOCK-007                             ACCEPTED N-Core
        ↓
N-ARITH-BLOCK-001                       ACCEPTED N-Arithmetic
        ↓
Z-BLOCK-002                             ACCEPTED Z
        ↓
Q-BLOCK-002                             ACCEPTED Q
        ↓
R-DP-001 SELECTS R-ROUTE-D / Dedekind
        ↓
R-DP-003 SELECTS localized classical CutComparability for Stage I
        ↓
R-BLOCK-001                             ACCEPTED R
        ↓
BOMA-C-R-DEP-001                        exact 16-property C-production boundary
        ↓
C-DP-001 SELECTS C-ROUTE-P
        ↓
C-BLOCK-001
        ↓
C-COMPARE-BLOCK-001                     scalar-generic comparison boundary integrated
        ↓
C-J-001 → C-BLOCK-002
        ↓
CA-20                                   ACCEPTED C
```

The accepted spine is unchanged by Stage-Two research and by the Learning-to-Construction Acts described below.

## Permanent verified alternatives learned through Stage Two

Owner-authorized Learning-to-Construction Acts integrate durable architectural knowledge into the permanent Construction DAG while preserving all experimental provenance.

```text
R-DP-001
   ├── SELECTS R-ROUTE-D / Dedekind → R-BLOCK-001 ACCEPTED
   └── R-ROUTE-C / Cauchy → PERMANENT VERIFIED ALTERNATIVE
                              ↓
                       ST2-EXP-003-R-J-001
                       R-FIELD-ISOMORPHISM / NON-ACCEPTANCE

C-DP-001
   ├── SELECTS C-ROUTE-P → C-BLOCK-001 → C-COMPARE-BLOCK-001
   │                      → C-J-001 → C-BLOCK-002 ACCEPTED
   └── C-ROUTE-Q → PERMANENT VERIFIED ALTERNATIVE
                     ↓
              ST2-EXP-002-PQ-J-001
              R-FIELD-ISOMORPHISM / NON-ACCEPTANCE
```

Permanent graph visibility does **not** mean selection or acceptance.

## C←R production boundary — ST2-EXP-001

`ST2-EXP-001` established the exact mathematical production surface used to rebuild the selected C meaning:

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

Authority: `BOMA-C-R-DEP-001`.

Formal witness:

```text
BOMA.C.StageTwo.NarrowRInterface001.NarrowROrderedFieldCertificate
BOMA.C.StageTwo.NarrowRInterface001.narrowRFromAcceptedProducers
```

The accepted C Lean implementation may still carry a larger bundled R ancestry. That excess is formalization/provenance over-bundling, not mathematical necessity.

## C comparison boundary — ST2-EXP-011

`ST2-EXP-011` established a smaller direct comparison interface at `C-COMPARE-BLOCK-001`:

```text
scalar operations:
  zero / one / neg / add / mul

quadratic coordinate laws:
  coord
  coordinateGeneration / coordinateUnique
  coordinateZero / coordinateOne / coordinateReal / coordinateImag
  coordinateNeg / coordinateAdd / coordinateMul
```

This comparison surface is **not** a replacement for the sixteen-property production surface. They answer different questions.

The accepted RBOMA adapter preserves the existing `Related` meaning definitionally. A native RCBOMA/H6 adapter is verified without H5 `cToD` or selected Dedekind implementation transport. Functional comparison still requires explicit `CoordinateExtractor` data; no global coordinate or inverse selector is introduced.

The experimental `ST2Exp011*.lean` sources remain research-only. The generic factoring is not an implicit replacement of accepted `CQuadraticComparison001`.

## R-DP-003 logical-regime boundary — ST2-EXP-004

`ST2-EXP-004` is closed, passed, merged, and its durable lesson is integrated through `BOMA-ST2-LEARNING-INTEGRATION-003`.

Exact frozen authority:

```text
accepted reference  50f3031b8d2657cbe0710e73e5935d997d40e49b
accepted tree       e4842acdf2b08c8db54b45d0798c36ee7565f351
candidate dossier   fd51041857d07cbf8e489c8683a907ea29866b17
Frozen Plan commit  89c9dc9154e7ca469e5c94c177be223205ee9dbd
Final Study/Act      6779d028c49f73757ea838c163d3968a982559fe
exact closed head   1fe760de811ad2b176ead6f420b80ca1aab5ce46
research merge      61adb8589c803e95e1b96ef38902320c8aa5df19
origin              DECISION_POINT / R-DP-003
```

The single changed factor was only the selected F-04 provider:

```text
BOMA.R.DedekindOrderClassical001.cutComparability_classical
BOMA.R.DedekindOrderClassical001.rLE_total_classical
```

The experiment preserved the accepted `LowerCut / CutEquiv / cutSetoid / RBOMA / CutLE / rLE` representation, accepted operation definitions, accepted Q/R/C manifests and sources, and independent logical commitments F-05/F-06/F-07.

### Integrated same-carrier fact

On the unchanged representation:

```text
RTotality ↔ CutComparability
```

where:

```text
RTotality := ∀ x y : RBOMA, rLE x y ∨ rLE y x
CutComparability := ∀ A B : LowerCut, CutLE A B ∨ CutLE B A
```

No unconditional constructive `CutComparability` inhabitant was recovered from the frozen `LowerCut` fields.

Therefore:

```text
conditional CutComparability ≠ constructive recovery
NO F-04 dependency           ≠ fully constructive R
formal dependency            ≠ mathematical necessity
```

F-05 finite membership/bracketing, F-06 positive representative extraction, and F-07 rational density remain separate localized commitments.

### Exact current proof/package impact

Gate A classified the measured declaration roots:

```text
F04_DIRECT             8
F04_TRANSITIVE         7
F04_FREE              22
OTHER_CLASSICAL_ONLY  18
unresolved             0
internal axioms        0
```

Gate B retained `77 / 88` accepted-manifest R source files in the research-only whole-source no-F04 survivor assembly. This is a source-packaging measurement, not an impossibility theorem.

### Downstream C sensitivity

Gate E removed exactly `orderTotal` from the sixteen-property production interface. Seven C Claim families survived:

```text
C-CL-CARRIER-001
C-CL-REMBED-001
C-CL-I-001
C-CL-GEN-001
C-CL-COORDUNIQ-001
C-CL-NONREAL-001
C-CL-COMPARE-001
```

The current proof closures for `C-CL-FIELD-001` and `C-CL-INTEGRATION-001` did not survive; their measured dependency is transitive through the current square/nonnegative → norm → field path. This is current proof-architecture sensitivity, not a theorem that every construction of those meanings mathematically requires total order.

`C-CL-COMPARE-001` survives consistently with the smaller ST2-EXP-011 comparison interface.

A located-cut redesign would change the representation and is only a possible separately authorized future candidate.

## Canonical acceptance remains unchanged

```text
R-DP-001 selected route       R-ROUTE-D / DEDEKIND
R-DP-003 logical regime       localized classical comparability / retained
accepted R integration        R-J-002
accepted R export             R-BLOCK-001
C-DP-001 selected route       C-ROUTE-P
selected C producer           C-BLOCK-001
comparison Claim owner        C-COMPARE-BLOCK-001
accepted C integration        C-J-001
accepted C export             C-BLOCK-002 / CA-20 ACCEPT
```

Permanent alternatives remain non-accepted:

```text
R-ROUTE-C / CAUCHY
  PERMANENT VERIFIED ALTERNATIVE / NON-SELECTED / NOT ACCEPTED
  Junction: ST2-EXP-003-R-J-001

C-ROUTE-Q
  PERMANENT VERIFIED ALTERNATIVE / NON-SELECTED / NOT ACCEPTED
  Junction: ST2-EXP-002-PQ-J-001

H6 Cauchy-native C core
  PERMANENT DOWNSTREAM ROBUSTNESS EVIDENCE / NOT ACCEPTED
```

No new Block, Decision Point, or Junction was created by the ST2-EXP-004 learning integration.

## Learning-to-Construction rule

A successful experiment may, after Study/Act, lifecycle closure, and explicit owner authorization, feed verified knowledge into the permanent Construction DAG by refining a dependency contract or existing unit's dependency/logical classification, retaining verified alternatives or non-acceptance Junctions, exposing invariants, or recording sensitivity/genericity conditions.

But:

```text
permanent DAG visibility ≠ SELECTS
permanent DAG visibility ≠ ACCEPTED EXPORT
successful experiment ≠ automatic acceptance promotion
integrated dependency knowledge ≠ accepted implementation refactor
```

The Learning Graph continues to preserve how every integrated fact was learned.

Integration authorities:

```text
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_001.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_002.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_003.md
```

## Current Stage-Two lifecycle

```text
ST2-EXP-001  CLOSED / PASS / lesson integrated
ST2-EXP-002  CLOSED / PASS / lesson integrated
ST2-EXP-003  CLOSED / PASS / lesson integrated
ST2-EXP-011  CLOSED / PASS / lesson integrated
ST2-EXP-004  CLOSED / PASS / lesson integrated
ST2-EXP-014  CLOSED / PASS / exact closure verified / routine merged
AUTONOMOUS RESEARCH PROGRAM = ST2-RP-001 / OWNER_AUTHORIZED
ACTIVE EXPERIMENT = NONE
ACTIVE STATE = TRANSITION_GATE
TRANSITION UNDER EVALUATION = ST2-EXP-014 → ST2-EXP-015
NEXT AUTHORIZED CANDIDATE = ST2-EXP-015 / QUEUED / NOT STARTED
ST2-EXP-015 BRANCH = NONE
ST2-EXP-015 FROZEN PLAN = NONE
SYNCHRONIZED PRE-AUTONOMY MAIN = 2a6c38af70e596c840ef2db4733421bde38f3ee5
REQUIRED NEXT ACT = RE-READ SYNCHRONIZED MAIN → EVALUATE 014→015 TRANSITION GATE
```

The ST2-EXP-004 and ST2-EXP-014 Frozen Plans remain immutable historical authorities. The baseline synchronization records no new mathematical result and does not pre-authorize a transition-gate outcome.

## Source-of-truth order

When current-state documents disagree, use this order unless a later explicit governance record supersedes it:

1. `LAB/PDSA/STATUS.md`
2. `LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_GOVERNANCE_001.md`
3. `LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_POLICY_001.json`
4. `LAB/PDSA/AUTONOMOUS_RESEARCH_PROGRAM_STATE_001.json` for autonomous-program state
5. active owner-authorized program record named by state
6. active program manifest named by state
7. `LAB/PDSA/STAGE_TWO_BRANCH_EXPERIMENT_REGISTER_001.md`
8. `LAB/PDSA/STAGE_TWO_BRANCH_ORIGIN_LEDGER_001.json`
9. `LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_003.md`
10. immutable experiment Plans / Study-Act / lifecycle / failures for experiment history
11. earlier integration authorities 002 and 001
12. `LAB/00_ARCHITECTURE/ARCHITECTURE.md` / `CONSTRUCTION_TOPOLOGY.md`
13. `LAB/00_ARCHITECTURE/REGISTRY.md` / `GRAPH.md`
14. relevant DAG / Decision / Block / acceptance / Claim records and exact evidence
15. onboarding summaries such as this README and `AGENTS.md`

Historical documents remain valid records of their own state at their own date; they do not override a later synchronized current-state authority. The old top-level frontier markers in `STAGE_TWO_BRANCH_ORIGIN_LEDGER_001.json` remain historical post-004 metadata and do not override the later owner-authorized program/state.

## Mandatory reading order

Before canonical work or before proposing any later research cycle, read:

```text
README.md
AGENTS.md
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
LAB/00_ARCHITECTURE/GRAPH.md
LAB/00_ARCHITECTURE/REGISTRY.md
LAB/00_ARCHITECTURE/R_DAG.md
LAB/10_CONSTRUCTION/decisions/R-DP-003/UNIT.md
LAB/00_ARCHITECTURE/C_R_DEPENDENCY_CONTRACT.md
LAB/10_CONSTRUCTION/blocks/C-COMPARE-BLOCK-001/UNIT.md
LAB/00_ARCHITECTURE/views/CONSTRUCTION_DAG_VIEW.md
LAB/00_ARCHITECTURE/views/LEARNING_GRAPH_VIEW.md
```

## Do not linearize BOMA

The construction is a DAG. Valid topology includes vertical dependency, horizontal independence, parallel contributors, Decision Point branches, permanent verified alternatives, and split → independent development → verified reconvergence.

Key invariants:

```text
fork ≠ Decision Point by default
meeting ≠ verified Junction by default
SELECTS ≠ DERIVES
reconvergence preserves provenance
verified alternative ≠ accepted export
successful experiment ≠ promotion
formal provenance ≠ mathematical necessity
```