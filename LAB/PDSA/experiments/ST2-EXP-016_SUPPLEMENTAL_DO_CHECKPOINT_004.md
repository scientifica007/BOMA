# ST2-EXP-016 — Supplemental Do checkpoint 004: exact accepted semantic bridge (NO ACT)

**Date:** 2026-10-30  
**Authority:** explicit owner authorization for a **bounded supplemental Do**, exclusively to address the accepted semantic gaps found by `ST2-EXP-016_STUDY_ASSESSMENT_001.md`.  
**Lifecycle:** `SUPPLEMENTAL_DO_RESEARCH_PROOF_VERIFIED / STUDY_REASSESSMENT_REQUIRED / NOT_CLOSED`.  
**Scientific source head before this administrative record:** `e84fb8b36dd05ff03191e1bf1a8b7c1b50d9c2e3`.  
**Frozen Plan immutable at:** `212f4f87fe02af13ef8fd2ed487e0bec18841d88`.  
**Research PR:** #33, Draft, unmerged; accepted `main` unchanged; G8 disabled; no 017.

## Plan/control retention
The only changed mathematical input remains the exact frozen `orderTotal → NormAnisotropy016` condition on the **same RBOMA**:
`a²+b²=0 → a=0 ∧ b=0`.
All other fifteen fields, Route P, accepted Claim meanings, `SELECTS`, accepted R/C/Q Lean sources, historical Plan/Do/Study/Act, and prior verification remain unchanged. This is a **follow-up Do**, *not* a new Frozen Plan, new scalar hypothesis or silently altered 016 objective.

## Do — independently typechecked external compatibility evidence
`LAB/payloads/lean/CStage/ST2Exp016AcceptedSemanticBridge.lean`
is a **separate external assembly**, not part of the abstract 016 root:
1. `toSelected016` and `fromSelected016` give explicitly proven mutually inverse maps between distinct Lean structures `Pair004` and accepted `CBOMA`. Their zero, one, imaginary generator, real embedding, negation, addition, multiplication, conjugation and norm correspond by checked equalities. This closes the **carrier/operation identification** gap, not by incorrectly asserting definitional type equality.
2. `selectedFieldCompatibility016` **inhabits the exact accepted `CPairFieldCertificate` type**. Its nonzero complex inverse existence/uniqueness and norm bridge are transported from the independently proved 016 `FieldCertificate016`; it does **not** call the accepted `cPairFieldCertificateFromAcceptedR` or accepted `c_inverse_exists` as a field oracle. It retains the historical accepted **ring core** only as a fixed pre-existing seven-Claim control.
3. The selected `normNonnegative` **auxiliary** is reconstructed separately as `selectedNormNonnegativeExternal016` from the historical accepted **R order interface** and nonnegative-square argument. This does **not** follow from 15+1 alone and is **not** smuggled into the abstract 016 field root. Thus the exact old certificate *type* is constructible for the original ordered RBOMA, but an unconditional 15+1-to-old-full-type equivalence for arbitrary models is not claimed.
4. `researchAcceptedPresentation016` directly inhabits the **original** `QuadraticFieldPresentation R` signature using new research field laws and fixed 004 controls. `researchExactComparison016` and `researchExactFunctionalComparison016` use coordinate relations and an **explicit extractor**; no global Choice selector is inferred from existential comparison.
5. `selectedIntegrationCompatibility016` inhabits the exact accepted `CStageIntegrationCertificate` *type* with 016-derived field witnesses and transferred generator, generation, uniqueness and nonrealness. `concreteAcceptedIntegrationCompatibility016` instantiates this result at the original RBOMA using the separate concrete `NormAnisotropy016` witness. This is a **research semantic compatibility package**, not replacement of accepted `cStageIntegrationCertificate` or issuance of a new `C-J-001`.
6. The original `selectedPresentation` occurs deliberately as the **fixed comparison TARGET** for the exact accepted integration type. Its original proof term contains the historical `c_inverse_exists` dependency. The external integration root therefore retains that historical ancestry **only through its comparison target**. The new *abstract 016* field/integration roots and the new **external selected field root** do **not** use that C inverse as a proof oracle. Absence of such historical ancestry for the external full integration root would be a **false claim**.

## Exact independent dependency boundaries — Do measurements
Verification-only workflow:
`.github/workflows/boma-st2-exp-016-accepted-bridge.yml`,
using manifest
`LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_ACCEPTED_BRIDGE_INPUTS.txt`
and checker `LAB/00_ARCHITECTURE/tools/st2_exp_016_semantic_boundary_audit.py`.

| Root closure | Internal declarations | External leaves | Edges | Unresolved / unmapped / internal axioms |
| --- | ---: | ---: | ---: | ---: |
| `selectedFieldCompatibility016` only | 571 | 75 | 6,151 | 0 / 0 / 0 |
| `selectedIntegrationCompatibility016` only | 972 | 77 | 11,540 | 0 / 0 / 0 |
| Six exact external adapter roots, joint | 1,053 | 77 | 12,222 | 0 / 0 / 0 |

Exact `#print axioms` on the external selected field, selected integration and concrete selected integration roots reports the same inherited set on **each**: `Classical.choice`, `Quot.sound`, `propext`. **No new internal axioms.**
The separate source/declaration checker asserts that neither accepted `cPairFieldCertificateFromAcceptedR` nor accepted `cStageIntegrationCertificate` appears as a proof oracle in these measured closures. The **field-only** root excludes accepted `c_inverse_exists`. The external comparison/integration root **does include** it through fixed `selectedPresentation`; concrete specialization also reaches `rLE_total_classical`. The checker records these facts instead of concealing them.

**Two independent successful bridge verifier runs:**
- [run 41025332718](https://github.com/scientifica007/BOMA/actions/runs/41025332718), job `123961986516`, artifact `12963945382`, artifact ZIP SHA-256 `8ddd4e151fc9d37710ae53f5e4f4f392e91010a237eed0ccafc2481a9579ad1e`.
- [run 41025340797](https://github.com/scientifica007/BOMA/actions/runs/41025340797), job `123962011902`, artifact `12963526023`, artifact ZIP SHA-256 `45c992ebb245577c4c21b4d83bfcf8314ced907634d5c238c8dd8aa3bbddd5df`.

At source head `e84fb8b36dd05ff03191e1bf1a8b7c1b50d9c2e3`, all new targeted bridge CI checks passed. The original entire-applicable-checks CI set is independently rechecked on every new commit; the final bookkeeping head (this record) requires an additional exact-head read before declaring it fully green.

## Failures preserved, bounded recovery
Initial bridge assembly at `c32987a5fd02f1c4f5a42fc661732bc73d1fef68` failed runs `41024586871` and `41024579583` because its external manifest omitted the historical narrow 001 proof sources required by `ST2Exp016ConcreteRBOMA.lean`. Corrected at `bd97b0c7841af83cd5119be87be2c953b3a6072c` by using the previously approved concrete manifest with the bridge file appended. See `ST2-EXP-016_FAILURE_004_EXTERNAL_SEMANTIC_MANIFEST.md`. No new hypothesis or mathematical modification was required.

## Study/Act boundary — what this new Do does NOT decide
The earlier owner-authorized Study (`ST2-EXP-016_STUDY_ASSESSMENT_001.md`) was **PARTIAL** on evidence available at its own exact head. It remains historical evidence and is **not silently rewritten or overruled** by this additional Do.

The present Do fills major mathematical **type-level semantic compatibility** gaps. It does **not** independently certify every administrative `CA-17/18/19` acceptance provenance/Claim-ownership/V5 Junction gate, and does not eliminate all historical order dependencies. A new owner-authorized **Study reassessment** must classify H4/H6 under the frozen success criteria, explicitly including fixed selected comparison ancestry, `normNonnegative` and the new external accepted-type proof. No automatic H4 PASS.

**NO ACT / NO CLOSED_PASS / NO PR MERGE / NO ACCEPTANCE PROMOTION / NO 017 / NO G8.**
