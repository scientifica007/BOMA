# ST2-EXP-016 — Independent Study assessment 001 (NO ACT)

**Date:** 2026-10-30  
**Authority:** The owner explicitly authorized **Study only** based on the existing frozen Plan and Do evidence, explicitly excluding Act, PR #33 merge and ST2-EXP-017.  
**Study status:** `STUDY_RECORDED / EVIDENCE_PARTIAL / NO_FINAL_PASS / ACT_NOT_STARTED`  
**Program:** `ST2-RP-001` / `DEPENDENCY_EDGE BOMA-C-R-DEP-001`  
**Original independent Plan freeze:** `212f4f87fe02af13ef8fd2ed487e0bec18841d88`  
**Exact Do evidence HEAD:** `c327135c86c28c34ea2a2fd9376a76c911ae8ce7`, tree `12dd9f88ce652d9284f7be26fd4fc22b5023241a`, **27/27 checks SUCCESS**, zero failed/pending (read on 2026-10-30).  
**Main before this Study record:** `895384b5617763622be4cc2b53fe3bc0686eac62`; protected.  
**PR:** #33 remains Draft; no merge. Current G8 remains disabled.

## Plan — Study decision questions (without new experimental Do)
Assess the already frozen H1–H6 hypotheses against the **actual declared meaning** of all nine accepted C Claim families. Compare the accepted `CA-04` and `CA-17/18/19` contracts, not only corresponding Lean names. Separate the *abstract conditional* 15+1 field proof from the *concrete RBOMA instance* and its order dependency. Preserve negative and failed-attempt evidence. Do **not** weaken the original success condition to obtain PASS.

## Evidence read and exact anchors
- **Frozen Plan** `LAB/PDSA/PDSA-ST2-EXP-016_NORM_ANISOTROPY_FROZEN.md`, plus `LAB/PDSA/plans/ST2-EXP-016/FROZEN_PLAN.json`: H1–H6, nine-Claim requirement, no changed factor except `orderTotal → NormAnisotropy016`.
- **Accepted specification** `LAB/00_ARCHITECTURE/C_ACCEPTANCE_SPECIFICATION.md`: CA-04 (complex field-strength, witness inverse permitted), CA-11 (canonical R-field/algebra isomorphism between candidates), CA-17/18 (ownership and exact verified Claim closure), CA-19 (same selected identity/carrier, commitments and V5 evidence, no circularity).
- **Accepted Claim register** `LAB/20_FORMALIZATION/C_STAGE/C_CLAIM_REGISTER_001.md`: `C-CL-FIELD-001` and `C-CL-INTEGRATION-001` full acceptance roles.
- **Accepted proof sources** `LAB/payloads/lean/CStage/CPairNormInverse001.lean` (`CPairFieldCertificate`: ring, `normNonnegative`, norm nonzero, conjugate product, existential inverse and uniqueness) and `LAB/payloads/lean/CStage/CStageIntegration001.lean` (`CStageIntegrationCertificate`: accepted field, generator, generation, coordinates, nonrealness and selected comparison).
- **Accepted provenance** `LAB/20_FORMALIZATION/C_STAGE/C_CLAIM_CLOSURE_AUDIT_001.md`: accepted `cStageIntegrationCertificate` (nine Claims, 19 producers, zero ownership gaps and undeclared inputs; accepted V5 run `32585583815`).
- **Do abstract proof** `ST2Exp016AlgebraicNormBridge.lean` and `ST2Exp016FieldIntegration.lean`; `ST2_EXP_016_CLAIM_MEANINGS.json`; `ST2_EXP_016_FIELD_INPUTS.txt`.
- **Do external concrete proof** `ST2Exp016ConcreteRBOMA.lean` and distinct concrete manifest; checkpoints `ST2-EXP-016_DO_SEMANTIC_AND_AXIOM_CHECKPOINT_002.md`, `ST2-EXP-016_DO_ABSTRACT_VS_CONCRETE_GATE_E_CHECKPOINT_003.md`.
- **Independent CI at exact Do HEAD:** `27/27 SUCCESS`, including two `verify 016 experimental field and integration candidate`, two `verify 016 concrete RBOMA condition separately`, accepted C integration and 004/011/014/015 regressions, `guard` and interactive governance. These passing checks validate the tested proofs and policies; they do **not** create a formal implication between different certificate types merely by running side by side.

## Study — hypothesis dispositions

| Frozen hypothesis | Study assessment | Reason and exact limit |
| --- | --- | --- |
| **H1** seven control Claims retained | **CONFIRMED for the 004 research interface** | `RWithoutOrderTotalCertificate` retains 15 fields; `cSurvivorCertificate004` is included in the new `NormBridgeCertificate016.sevenControls`; the 004 historical gate and independent 016 A–C checks pass. This is a control result; **not** a new accepted source. |
| **H2** single-condition norm bridge | **CONFIRMED** | `normZeroCoordinates016`, `normNonzero016`, `normScalarInverseExists016` and `mulConj016` verified. No second frozen condition or selected complex field oracle was added. |
| **H3** existential field witness closure | **CONFIRMED for research mathematical field-strength** | `FieldCertificate016` contains commutative ring laws, `normNonzero`, conjugate product, nonzero existential inverse and uniqueness. `NineClaimMeaningCertificate016` also includes scalar and complex nontriviality. No globally chosen inverse is introduced. |
| **H4** unweakened nine-Claim accepted integration | **PARTIAL — FINAL SEMANTIC BRIDGE UNPROVEN** | Nine *research* obligations were typechecked, but the independent `Pair004` and accepted `CBOMA` are **distinct Lean record types**, and the `ComparisonInterface011.QuadraticPresentation` and accepted `QuadraticFieldPresentation` have different formal contract shapes. No verified exact adapter or equivalence connects the 016 field/integration certificates to all existing `CA-04 / CA-11 / CA-17 / CA-18 / CA-19` obligations, including Junction/provenance and V5 obligations. The JSON research mapping explicitly says `closed_acceptance_contract:false`. |
| **H5** measured order-dependency separation | **CONFIRMED WITH BOUNDED INTERPRETATION** | Actual abstract 016 root closure rejects `.orderTotal` and `rLE_total_classical`. External concrete RBOMA proof closure **does include** `BOMA.R.DedekindOrderClassical001.rLE_total_classical`. Both abstract/concrete `#print axioms` report exactly `propext`, `Quot.sound`, `Classical.choice`. Other **order-related laws remain** among the 15 fixed fields (e.g. `orderMulNonneg`). This supports replacement of one *projection*, not mathematical minimality or global constructive/order independence. |
| **H6** provenance, frozen constraints and lifecycle | **PARTIAL FOR COMPLETE LIFECYCLE; VERIFIED FOR DO PROVENANCE** | Frozen Plan/twin/origin Git blob SHAs unchanged after the freeze; accepted source/SELECTS unchanged; failures kept. Exact Do head passed 27/27. This new Study commit requires its own CI; Act and experiment lifecycle closure are excluded by current owner scope. No claim of completed H6 lifecycle or `CLOSED_PASS`. |

**Aggregate verdict:** `PARTIAL / STUDY_COMPLETE_AS_ASSESSMENT / EXPERIMENT_NOT_CLOSED`. No frozen hypothesis is refuted by a mathematical counterexample. H4 is *insufficiently demonstrated*, **not disproven**. Hence the predeclared all-H1–H6 PASS condition **is not met**.

## Claim-level CA-04 / CA-19 semantic crosswalk
| Accepted Claim | 016 research evidence | Study classification |
| --- | --- | --- |
| `C-CL-CARRIER-001` | `Pair004`, `carrierExt` | **Research meaning represented**; separate accepted `CBOMA` adapter not verified |
| `C-CL-REMBED-001` | injectivity + zero/one/neg/add/mul preservation fields | **Research meaning represented** |
| `C-CL-FIELD-001` | `FieldCertificate016`, nontriviality, inverse existence/uniqueness | **CA-04 core mathematical strength verified**, but direct equivalence to selected `CPairFieldCertificate` type unproven |
| `C-CL-I-001` | `generatorSquared` | **Research meaning represented** |
| `C-CL-GEN-001` | `realGeneration` | **Research meaning represented** |
| `C-CL-COORDUNIQ-001` | `coordinateUnique` | **Research meaning represented** |
| `C-CL-NONREAL-001` | `imaginaryNotReal` | **Research meaning represented** |
| `C-CL-COMPARE-001` | 011 relation + extractor-conditional functional comparison | **Research meaning represented**; exact bridge between generic 011 presentation and accepted field-strength presentation not verified |
| `C-CL-INTEGRATION-001` | `nineClaimMeaningCertificate016` | **Research aggregation verified; full CA-17/18/19 governance and selected Junction equivalence not established** |

**Do not infer** that a new research structural field of the same *name* automatically proves its accepted counterpart. The absence of a Lean adapter is an evidence gap; it is not mathematical evidence that the two rank-two constructions are inequivalent.

### normNonnegative — the exact auxiliary issue
The accepted `CPairFieldCertificate` includes `normNonnegative : ∀ z, rLE rZero (cNorm z)`. The accepted **CA-04 prose** explicitly requires commutative-field-strength behavior with an inverse witness interface; it does *not* separately list nonnegative norm as an acceptance Claim family. Consequently, it is reasonable to classify `normNonnegative` as an **implementation-certificate auxiliary**, rather than inventing a tenth C Claim or silently making it a new algebraic assumption.

However the *selected certificate type* and the accepted `CStageIntegrationCertificate.field` **do contain the field**, whereas `FieldCertificate016` deliberately omits it. Therefore **direct certificate-type equivalence is not shown**. Study has neither introduced a new axiom to recover it nor silently declared it unnecessary for all acceptance/provenance obligations. A later owner-authorized targeted Do could provide a kernel-verified semantic bridge, potentially using a concrete external-RBOMA result **without importing that result into the abstract conditional 016 root**. That proposal is NOT executed by this Study.

### comparison and integration boundary
Accepted `CA-11` and `CStageIntegrationCertificate` quantify over `QuadraticFieldPresentation rStageIntegrationCertificate`. The research `NineClaimMeaningCertificate016` quantifies instead over the narrower `ComparisonInterface011.QuadraticPresentation scalarOps004`. Both support coordinate-preserving relational and extractor-conditional functional comparison, but no exact formal translation from the accepted class of field presentations into the 011 class is verified in this branch. In addition, `CA-19` calls for selected-carrier integration, declaration-ownership/provenance, absence of circularity and exact V5 evidence. A typechecked research nine-Claim packet does not itself implement the accepted Junction `C-J-001` or replace its V5 governance evidence.

## Dependency, axioms and negative evidence
- **External concrete RBOMA** measured declaration closure: **692 internal**, **76 external boundary**, **8,454 edges**, **0 unresolved**, **0 unmapped**, **0 internal axioms**.
- **Abstract field/meaning roots:** orderTotal projection and concrete `rLE_total_classical` absent from measured abstract root ancestry; inherited Lean axioms remain `propext`, `Quot.sound`, `Classical.choice`. Concretizing on RBOMA uses inherited classical order — openly reported rather than hidden.
- **Failures retained as technical blocks, not mathematical refutation:**
  - Gate D missing helper `neg_zero_from_interface` — run `40970574189` (`ST2-EXP-016_FAILURE_001_GATE_D_HELPER_REBIND.md`).
  - Gate D Prop/Type functional isomorphism mismatch — run `40971069474` (`ST2-EXP-016_FAILURE_002_GATE_D_PROP_TYPE.md`).
  - External concrete certificate implicit/explicit order binder mismatch — runs `41015369686` and `41015362741` (`ST2-EXP-016_FAILURE_003_GATE_E_CONCRETE_IMPLICIT_BINDERS.md`).
All were corrected within the existing frozen mathematical factor; failed runs remain evidence.

## Study recommendation only — not Act
**Do not label 016 `CLOSED_PASS`, merge PR #33, modify `SELECTS`, or start 017 under this Study.** The owner can later direct a **separately authorized, narrow Do continuation on the same frozen factor** to establish formal carrier/operation/field-presentation adapters and a claim-by-claim CA-04/CA-19 semantic/provenance crosswalk, with exact-head CI and no accepted-source edit. Alternatively the owner can later authorize Act to record a **PARTIAL** scientific outcome and stop. **Neither choice is authorized or executed here**.

The program's full `H1..H6` PASS threshold remains unchanged. The prior 015 closure is unaffected. This study record is not a new Frozen Plan, counterexample, accepted C producer, Act decision, routine merge authorization or 017 transition.
