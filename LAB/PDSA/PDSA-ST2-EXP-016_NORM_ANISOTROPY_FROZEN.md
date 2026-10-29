# PDSA-ST2-EXP-016 — Frozen independent Plan: algebraic norm anisotropy

**Program:** `ST2-RP-001` / experiment 3 of 4  
**Status in this freeze commit:** `PLAN FROZEN / NO DO / OWNER_REQUIRED`  
**Date:** 2026-10-29  
**Owner authority:** explicit owner approval to **prepare and freeze** 016, **without beginning Do**, following explicit acceptance of the three scientific decisions recorded in `LAB/PDSA/drafts/ST2-EXP-016_OWNER_REVIEW_DECISION_2026-10-29_AR.md`.  
**Frozen reference main:** `e03ea85528aa98cb86562a1d00e57ca5c06323fa`  
**Freeze branch:** `planning/st2-exp-016-frozen-plan-2026-10-29`  
**Machine twin:** `LAB/PDSA/plans/ST2-EXP-016/FROZEN_PLAN.json`  
**Typed origin:** `DEPENDENCY_EDGE / BOMA-C-R-DEP-001`  
**Existing comparison draft:** `LAB/PDSA/drafts/ST2-EXP-016_PLAN_REVIEW_DRAFT_2026-10-29_AR.md`  
**Execution authority:** `OWNER_DIRECTED_INTERACTIVE_PDSA` under `LAB/PDSA/INTERACTIVE_PDSA_EXECUTION_GOVERNANCE_2026_10_29.md`.

# PLAN — FROZEN; NO EXPERIMENTAL DO

## 1. Research question and bounded objective
Can the two C Claim families whose present proof did not survive the removal
of `orderTotal` in ST2-EXP-004 — `C-CL-FIELD-001` and
`C-CL-INTEGRATION-001` — be recovered by replacing **only** that scalar
production-interface field with one explicitly frozen non-order algebraic
norm-nondegeneracy condition, while preserving the other fifteen production
fields, selected Route-P quadratic meaning, and all nine accepted C Claim
meanings?

The output is a measured research-only sufficiency result or an evidenced
failure under this exact interface. No minimality/necessity theorem, global
removal of order/Choice, generic K[i], acceptance promotion, or route change
is within scope.

## 2. Exact frozen factor — one condition, one change
The program manifest fixes the factor name:
`PRODUCTION_ORDERTOTAL_TO_ONE_EXACT_FROZEN_NON_ORDER_ALGEBRAIC_NONDEGENERACY_CONDITION`.

Freeze the **only replacement assumption** as:

```text
NormAnisotropy016:
  ∀ a b : RBOMA,
    rAdd (rMulCandidate a a) (rMulCandidate b b) = rZero
      → a = rZero ∧ b = rZero
```

The same frozen `RBOMA` carrier, `rZero`, `rAdd`,
`rMulCandidate`, and equality are used. This is one two-variable
predicate, not two independently chosen conditions. `-1` nonsquare and
polynomial irreducibility are **not** additional assumptions in 016.
No later replacement, strengthening, simplification, or second algebraic
assumption can be introduced without a new owner decision and new Plan.

**Direct experimental comparator:** the exact fifteen-field
`RWithoutOrderTotalCertificate` of
`LAB/payloads/lean/CStage/ST2Exp004WithoutOrderTotalCConsumers.lean`.
Create a new research-only fifteen-plus-one certificate, not a modification
of that historical source or the accepted sixteen-field interface.

## 3. Frozen controls and deliberately excluded second factors
- `RBOMA` selected Dedekind real producer and unchanged scalar operations,
  equality, `rLE`, and the **other fifteen** ST2-EXP-001 properties.
  Preserve the exact signatures; do not quietly alter `orderMulNonneg` or
  remove another order-related field.
- Fixed complex **Route P** ordered-pair carrier and equality,
  component definitions, embedding, `i²=-1`, generation/coordinate
  uniqueness, nonrealness, conjugate, `N(a+bi)=a²+b²`, and witness-only
  nonzero inverse semantics.
- The same nine accepted C Claim **meanings**, plus comparison logic from
  ST2-EXP-011 and the relation/function firewall with an explicit
  `CoordinateExtractor`. No existential witness becomes a global selector.
- Fixed accepted Q/R/C sources, manifests, `R-DP-001 SELECTS Dedekind`,
  `C-DP-001 SELECTS Route P`, `R-BLOCK-001`,
  `C-BLOCK-002 / CA-20`, `C-J-001`, accepted contracts, all previously
  frozen Plans, exact closure artifacts and the historical research program
  manifest and 2026-08-25 authority.
- 014's Cauchy P and 015's Cauchy Q / Dedekind×Cauchy P/Q
  square are **external fixed corroborating evidence**, never native
  implementation inputs or additional changed factors for 016.
- No use of accepted Route-P field/integration implementation as a proof
  oracle for the **new** field/integration roots. Established statements
  may serve only as comparison targets.

**Assistant's operational authority is not changed by freezing a Plan**:
the G8 engine remains disabled; `OWNER_REQUIRED`, no unattended work,
no automatic transition or merge, and no automatic start of 017.

## 4. Prior exact evidence frozen as controls
- **004 / Gate E** (`LAB/PDSA/experiments/ST2-EXP-004_GATE_E_C_SENSITIVITY_001.md`):
  seven of nine C Claim families survived the fifteen-field interface;
  `C-CL-FIELD-001` and `C-CL-INTEGRATION-001` did not close by the
  existing square-nonnegative→norm→inverse-witness proof path. This is
  proof-path dependence, not mathematical impossibility.
- **011** (`LAB/PDSA/experiments/ST2-EXP-011_FINAL_STUDY_ACT_001.md`):
  `C-CL-COMPARE-001` depends on scalar arithmetic and explicit coordinate
  presentation/extractors, not total order or a global inverse selector.
- **014** (`LAB/PDSA/experiments/ST2-EXP-014_FINAL_STUDY_ACT_001.md`):
  nine Claim meanings closed over independent Cauchy scalar Route P,
  retaining native/external boundaries.
- **015** (`LAB/PDSA/experiments/ST2-EXP-015_FINAL_STUDY_ACT_001.md`,
  `LAB/PDSA/experiments/ST2-EXP-015_TO_ST2-EXP-016_BOUNDARY_ASSESSMENT_001.json`):
  Q and the four-corner square closed; 015 retained orderTotal. The
  015→016 scientific prerequisites were `MET`; owner instruction
  to freeze 016 is now separately explicit.
- **Authoritative architecture:** `LAB/00_ARCHITECTURE/C_R_DEPENDENCY_CONTRACT.md`,
  `LAB/PDSA/ST2_RP_001_PROGRAM_MANIFEST_001.json`, the current
  interactive governance and the two merged 016 review documents.

## 5. The nine-Claim frozen meaning matrix
**Two target recoveries:** `C-CL-FIELD-001`,
`C-CL-INTEGRATION-001`.

**Seven exact controls:**
```text
C-CL-CARRIER-001
C-CL-REMBED-001
C-CL-I-001
C-CL-GEN-001
C-CL-COORDUNIQ-001
C-CL-NONREAL-001
C-CL-COMPARE-001
```

Every row receives exact proof roots, source boundaries, verified declaration
closure, inherited axioms and semantic correspondence to the accepted
contract. Missing or weakened meanings do not count as success.

## 6. Auxiliary-certificate rule: normNonnegative
`CPairFieldCertificate.normNonnegative` and the Q analogue are
auxiliary fields in historical implementations. They are **not a new ninth-
or tenth-family C Claim**, but Gate A must audit whether any accepted
field/Claim export semantically relies on their meaning.

A new 016 research-only field certificate may reorganize or omit an
auxiliary **proof-structure field** only if it preserves the full
`C-CL-FIELD-001` and `C-CL-INTEGRATION-001` meaning and the other
seven Claims. It may not delete or weaken an accepted promise. If a
semantic dependency on nonnegativity turns out indispensable to an
accepted Claim, the experiment stops `OWNER_REQUIRED`. A silent
contract change is explicitly forbidden.

## 7. Frozen hypotheses H1–H6
**H1: Seven-family control fidelity.** Each survivor of 004 remains
available under the fifteen fixed properties and does not depend on the
new factor or a hidden `orderTotal` projection.

**H2: Algebraic norm bridge.** From the single
`NormAnisotropy016` condition, derive
`N(z)=0 → (z.re=0 ∧ z.im=0)` and
`z≠0 → N(z)≠0`, and
`z * conj(z) = embed(N(z))`, without deriving square nonnegativity
from totality or importing a selected complex-field oracle.

**H3: Field closure.** Using the preserved scalar
`inverseExists` witness field, establish the existence and uniqueness
of a nonzero complex inverse witness using the algebraic norm and
conjugate; recover the field Claim meaning without a chosen global
inverse function.

**H4: Integration.** Assemble all nine C Claim families including
`C-CL-INTEGRATION-001` with the unchanged explicit-coordinate
comparison semantics and fixed accepted-meaning contract.

**H5: Measured dependency effect.** The abstract 016 proof roots and
their actual declaration closure must not consume an `.orderTotal`
interface field or a disguised theorem requiring that field. Separately
inventory any inherited order or classical dependence introduced while
building a concrete `RBOMA` instance of the single predicate. Do not
equate absence of an interface projection with global logical
independence, minimality or constructive real arithmetic.

**H6: Provenance and governance.** The Plan/twin are immutable after
the freeze SHA; exact single-factor and fixed-control checks, full
independent verification/CI, unchanged selected sources and historical
closure, honest failure records and owner-only Act/merge are satisfied.

## 8. Exact post-freeze execution gates (not invoked by this commit)
**Gate A — authority/baseline/semantic inventory.**
Verify freeze SHA ancestor, byte-identical Plan and machine twin,
freeze baseline, historical 004/011/014/015 closures and nine-Claim
matrix. Record the `normNonnegative` semantic classification before
research payload work. If a mismatch changes factor/controls, stop.

**Gate B — seven Claim controls.**
Reconfirm 004's seven-family certificate on precisely the fifteen
properties, with source and declaration evidence. No missing Claim may
be silently reclassified as a target.

**Gate C — new norm bridge.**
In an isolated 016 research-only namespace implement the fifteen-plus-one
certificate and `NormAnisotropy016`-based norm nonzero and conjugate
product proofs. No `orderTotal`, new field hypothesis, sign split, or
second changed factor.

**Gate D — field/integration.**
Construct nonzero inverse *witness* proofs, inverse uniqueness, and
nine-Claim research integration; preserve the explicit 011 extractor
and the accepted mathematical semantics.

**Gate E — source/declaration/logic audit.**
Record independent research manifest and selected roots, full
declaration closures, `#print axioms`, inherited
`propext`/`Quot.sound`/`Classical.choice` if present, rejected
internal axioms, sorry/admit/unsafe, undeclared dependencies,
forbidden `Classical.choose` and orderTotal ancestry. Classify
the concrete RBOMA instance separately from the abstract 016 result.

**Gate F — exact-head verification.**
Use repository-pinned Lean toolchain (currently 4.32.1),
architectural/Claim and 004/011/014/015 historical regressions,
interactive policy audits, frozen-file byte-hashes, exact run/job/
attempt/artifact IDs and SHA-256 evidence. Output generated artifacts
outside protected mathematical inputs. Do not dispatch G8.

**Gate G — Study/Act/lifecycle.**
State CONFIRMED / REFUTED / PARTIAL / BLOCKED for every H1–H6,
nine Claim rows and dependency/axiom measurements. Preserve all
material failures, classify mathematical INFORMATIVE FAIL versus
tooling TECHNICAL_BLOCK, record exact tree/commit identity and
owner-approved PR lifecycle. No automatic 017.

## 9. Predeclared success, failure, and recovery rules
**PASS** only if H1–H6 are confirmed with an unweakened nine-Claim
comparison, both target recoveries, a genuine abstract norm-based
inverse witness, no hidden `orderTotal` in the abstract root closure,
no extra unapproved assumptions, and exact-head verification.

**INFORMATIVE FAIL** requires a reproducible mathematical
counterexample/incompatibility/necessary second-factor observation
under the frozen semantics. An unproved Lean goal, timeout, missing
declaration, unrelated failure, or incomplete proof is a
`TECHNICAL_BLOCK`, not disproof.

Permitted recovery: namespace/import/unfolding/proof-script repairs,
manifest path and ordering repairs, false-positive dependency audit
correction, infra/download retry, all without altering the factor,
controls, Claims or Frozen Plan. Every substantive unsuccessful attempt
is evidence. **OWNER_REQUIRED** for any change of assumption,
representation, scalar producer, accepted meaning, acceptance
contract, additional logical principle, unapproved selector,
sequence-critical prerequisite, or inability to preserve H1–H6.

## 10. Relation to 017 and owner boundary
016's PASS, if achieved, is **not** authority to start or freeze
ST2-EXP-017. The transition requires separately verified evidence of
the precise abstract algebraic interface sufficient for a later K[i]
question, not just a proof specializing an ordered RBOMA. Any
remaining ordering assumptions must be openly classified. If 016
does not supply the required interface, stop and refer the next
scientific decision to the owner. After program closure at 017,
the owner has separately directed a deliberate pause for BOMA
architectural synthesis before any new research program.

**NO DO AUTHORIZATION:** this freeze only fixes a Plan. The owner must
separately approve beginning Do after the freeze record and PR review.
No research files, Lean declarations, new 016 witness, or experiment
activation are allowed by this freeze commit.
