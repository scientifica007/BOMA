# ST2-EXP-016 — Do checkpoint 003: abstract/concrete boundary and logical cost

**Recorded:** 2026-10-30  
**Program:** `ST2-RP-001`; **typed origin:** `DEPENDENCY_EDGE / BOMA-C-R-DEP-001`  
**Status:** `DO_VERIFIED_CHECKPOINT / NOT_STUDY_ACT / NOT_CLOSED`  
**Owner permission:** execute ST2-EXP-016 Do only, no auto merge, no 017  
**Immutable Frozen Plan commit:** `212f4f87fe02af13ef8fd2ed487e0bec18841d88`  
**Exact verified concrete scientific head:** `3a63e7f84d9c9b6fa1f1820ea050a2aa88dd7c95`  
**Research PR:** #33 (`feature/stage-two-st2-exp-016-norm-anisotropy`).

## Plan: preserve the factor and distinguish its proof boundaries
One single replacement only:
`orderTotal → NormAnisotropy016`,
`∀a b : RBOMA, a²+b²=0 → a=0 ∧ b=0`.
The other fifteen fields, RBOMA, selected Route P, the accepted nine Claim
*meanings*, previously accepted sources and Frozen Plans remain unchanged.
The abstract 016 certificate may assume exactly this one algebraic
condition, while an external, segregated audit may show that the actual
selected RBOMA satisfies it by using inherited classical order proofs.
These are **different mathematical dependency questions**.

## Do: newly verified external concrete instance
- `LAB/payloads/lean/CStage/ST2Exp016ConcreteRBOMA.lean` defines
  `concreteFifteen016` by projecting the exact fifteen fixed fields
  from the historical real certificate, then proves
  `concreteNormAnisotropy016` using the existing narrowed
  real-square/nonnegative-sum lemmas. Its `concreteAnisotropyCertificate016`
  directly inhabits the **same** one-condition interface; the
  `concreteFieldWitness016` obtains the witness-field result from
  the separate abstract 016 theorem.
- The **external** compilation manifest
  `LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_CONCRETE_RBOMA_INPUTS.txt`
  includes the selected-real and historical narrow-interface sources.
  It is *not* interchangeable with the independent abstract
  `ST2_EXP_016_FIELD_INPUTS.txt` manifest.
- New verification-only workflow `boma-st2-exp-016-concrete-rboma.yml`
  checks the exact freeze ancestry, Lean kernel closure, declaration
  dependency graph and inherited axioms, with read-only Actions
  permissions and no credentials or autonomous engine dispatch.

## Study-boundary evidence acquired during Do (no final Study verdict)

| Measurement | Abstract 016 | External concrete RBOMA 016 |
| --- | --- | --- |
| Proof object | `nineClaimMeaningCertificate016`, `fieldCertificate016` | `concreteNormAnisotropy016`, `concreteFieldWitness016` |
| Premises | exact fifteen fields + one norm anisotropy condition | historical selected RBOMA and its ordered real proofs |
| Uses `.orderTotal` or `rLE_total_classical` in measured root closure | **NO** | **YES** (including `BOMA.R.DedekindOrderClassical001.rLE_total_classical`) |
| Inherited Lean axioms in `#print axioms` | `propext, Quot.sound, Classical.choice` | `propext, Quot.sound, Classical.choice` |
| Internal axioms or unresolved declaration dependencies | 0 | 0 |
| Scope | conditional algebraic sufficiency | original concrete real model satisfies new algebraic condition |

The direct concrete dependency closure reports **692 internal declarations,
76 external boundary declarations, 8,454 dependency edges, 0 unresolved,
0 unmapped internal after recorded 58 generated-source inferences, 0
internal axioms**. Thus, the construction of the concrete witness
**retains order dependence**; only the segregated abstract consumer proof
avoids the `orderTotal` projection. No global logical independence,
minimality or constructivity assertion is made.

The explicit nine-Claim certificate introduced in checkpoint 002 is
kernel-checked, including nontriviality, field laws, existential inverse,
generation and comparison with explicit extractors. **The final exact
accepted CA-04/CA-19 semantic fidelity judgment and the role of auxiliary
`normNonnegative` remain for later Study; no automatic promotion.**

## Exact evidence
At head `3a63e7f84d9c9b6fa1f1820ea050a2aa88dd7c95`, the full
applicable GitHub CI set completed **26/26 PASS**, with no failed/pending
checks. Concrete audit was independently completed twice:

- Run [41015869708](https://github.com/scientifica007/BOMA/actions/runs/41015869708),
  job `123931946515`, artifact `12959855443`,
  ZIP SHA-256 `81407a42ad8778e5be4ec639f058e1669de32f67db3e0bb6b1dd1868cd5edc52`.
- Run [41015865316](https://github.com/scientifica007/BOMA/actions/runs/41015865316),
  job `123931931845`, artifact `12959204037`,
  ZIP SHA-256 `0eb964ae153e9efdb15f09de5f1ac450cbae97d607d14c2ca8b4a0dd4984011e`.

**Preserved technical failure:** earlier first concrete
attempt `29bc9bdc614153af0dea788a7159767b43fdbee4`
failed in runs `41015369686` and `41015362741` because the two
historic order proof fields had implicit binders while the 004 certificate
expected explicit binders. `ST2-EXP-016_FAILURE_003_GATE_E_CONCRETE_IMPLICIT_BINDERS.md`
records it; corrected with explicit lambdas at
`364eb53491074b9734db5705359f1cbdf858dfad`
without any scientific-factor change.

## Do boundary: what this checkpoint does NOT do
- This is **not** the H1–H6 Study verdict or Act authorization.
- Does not change C acceptance `SELECTS`, `CA-20`, `C-J-001`,
  accepted C/R/Q Lean sources, or historical Frozen Plans.
- Does not claim `CLOSED_PASS`, automatically merge PR #33, start 017,
  re-enable G8 or schedule research.
- The later final Study should crosswalk the accepted integration semantics
  exactly, classify `normNonnegative`, the measured two closure boundaries,
  and confirm the post-checkpoint-head exact CI before any closure decision.

**Lifecycle remains `OWNER_REQUIRED / 016_DO_ACTIVE / NOT_CLOSED`.**
