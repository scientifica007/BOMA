# ST2-EXP-016 — Owner-directed Do kernel checkpoint (NOT Study/Act)

**Date:** 2026-10-29  
**Authority:** owner wrote explicitly: “أمنحك الإذن في الانطلاق في التنفيذ (مرحلة Do)”.  
**Scope:** independent frozen `ST2-EXP-016` Plan, no additional factor or assumption.  
**Frozen Plan SHA:** `212f4f87fe02af13ef8fd2ed487e0bec18841d88`  
**Do scientific head verified:** `d1ea2b1d64253206cba4c8eb34cfd8cea2e8b24b`  
**Research branch:** `feature/stage-two-st2-exp-016-norm-anisotropy`  
**Lifecycle:** `DO_ACTIVE / GATES_A_B_C_VERIFIED / GATE_D_KERNEL_CANDIDATE_VERIFIED / NOT_STUDY_ACT / NOT_CLOSED`.

## Exact independent verification on scientific head

**Gates A–C:**
- Run: `40971208236` (push) / artifact `12940088702`.
- Artifact SHA256: `ff6ef9302f6480d65a0be0c86a751862c79142385f08377c3afb0eee541786b1`.
- The same earlier checkpoint on `41770de4996fb95f39c438402e44aaaf561d8167`
  passed 15/15 GitHub checks, with separate immutable evidence.
- Exact frozen Plan blobs unchanged; accepted source/manifests unchanged.
- Research scalar certificate consists of 15 exact 004 fields plus **one**
  `NormAnisotropy016`, with proof of norm nonzero and scalar inverse witness.
- Declaration closure at first verified checkpoint: internal 510,
  external boundary 74, dependency edges 5399, unresolved 0,
  unmapped internal 0, internal axioms 0.

**Gate D — research field/integration candidate only:**
- Run `40971208249`, job `123788118231`, artifact `12939809402`.
- Artifact SHA256: `4b8528dc142035198d595f5ca1db2e23d8ead20075c6b0a520367c7c99c6a690`.
- Exact candidate root closure `PROTOTYPE_PASS`: internal **562**,
  external boundary **74**, dependency edges **6007**,
  unresolved **0**, unmapped internal **0**, internal axioms **0**.
- Verified roots:
  `BOMA.C.StageTwo.NormAnisotropy016.fieldCertificate016` and
  `BOMA.C.StageTwo.NormAnisotropy016.nineClaimCandidate016`.
- New research-only source derives pair ring laws, norm-conjugate product,
  complex inverse witness existence and uniqueness from the fixed scalar
  certificate. The comparison layer requires an **explicit pair coordinate
  extractor** and obtains functional comparison for arbitrary conforming
  quadratic presentations, not by global selection.
- The verifier rejects an `.orderTotal` declaration in the actual
  abstract root closure or the `rLE_total_classical` witness, and
  rejects new unresolved/internal axioms.
- All **18/18** applicable GitHub PR/push checks on this exact scientific
  head completed successfully. This measurement is **not** the final
  post-checkpoint-head CI result.

## Nine-family research map (semantic final assessment still OPEN)

| Claim | Experimental Lean root / field | Kernel status | Semantic status |
|---|---|---|---|
| `C-CL-CARRIER-001` | `Pair004`, `pair_ext004` | Verified historical 004 | Fixed control, audit pending |
| `C-CL-REMBED-001` | `cSurvivorCertificate004` embedding fields | Verified historical 004 | Fixed control, audit pending |
| `C-CL-FIELD-001` | `fieldCertificate016` | **NEW KERNEL PASS** | Exact accepted-Claim correspondence pending |
| `C-CL-I-001` | `imag_squared004` | Verified historical 004 | Fixed control, audit pending |
| `C-CL-GEN-001` | `generation004` | Verified historical 004 | Fixed control, audit pending |
| `C-CL-COORDUNIQ-001` | `coordinate_unique004` | Verified historical 004 | Fixed control, audit pending |
| `C-CL-NONREAL-001` | `imag_not_real004` | Verified historical 004 | Fixed control, audit pending |
| `C-CL-COMPARE-001` | `anyQuadraticComparison016`, `explicitFunctionalComparison016` | NEW KERNEL PASS | Fixed 011 meaning, audit pending |
| `C-CL-INTEGRATION-001` | `nineClaimCandidate016` | **NEW KERNEL PASS** | Exact accepted integration Claim audit pending |

The fact that Lean checks a data-containing `Type` certificate is
independent evidence of faithful functional comparison but **does not by
itself establish equivalence of every accepted Claim contract**. Gate
D semantic matching, Gate E logical cost/axiom audit and Gate F exact
final-head regression, followed by Study/Act, remain necessary.

## Failed attempts preserved
- `ST2-EXP-016_FAILURE_001_GATE_D_HELPER_REBIND.md`:
  unknown helper references in run `40970574189`.
- `ST2-EXP-016_FAILURE_002_GATE_D_PROP_TYPE.md`:
  Prop-valued integration package incorrectly contained Type-valued
  functional map in run `40971069474`.
Both were technical blocks repaired within the **same frozen factor**
without deleting the failed run evidence or changing accepted artifacts.

## Owner boundary and source of authority
The original `pre_do_frozen_plan` and its `do_authorized:false`
refer to the exact **pre-Do freeze snapshot**, not the later owner
instruction. The new `owner_directed_do_016` mutable overlay records
the actual current, session-authorized task. The historical G8-specific
`active_experiment` field remains null to preserve fail-closed
autonomy validation and must **not** be read as revoking the later owner
instruction. `OWNER_REQUIRED` continues to mean no autonomy, no
automatic transitions and no automatic merges.

**Next:** finish the exact nine-Claim semantic audit, classify
dependencies and inherited axioms separately for abstract vs concrete
RBOMA, complete exact final-head verification and present Study/Act.
Do not start ST2-EXP-017 or merge this PR automatically.
