# C ← R DEPENDENCY CONTRACT — Production Surface, Comparison Boundary, and orderTotal Sensitivity

**Document ID:** `BOMA-C-R-DEP-001`  
**Status:** **ACTIVE — CANONICAL C PRODUCTION R→C MATHEMATICAL SURFACE / ST2-EXP-001 + ST2-EXP-011 + ST2-EXP-004 LESSONS INTEGRATED**  
**Date:** 2026-08-25  
**C specification:** `BOMA-C-ACCEPT-001`  
**Upstream selected export:** `R-BLOCK-001`  
**Narrow production-interface experiment:** `ST2-EXP-001 / CLOSED / PASS`  
**Comparison-interface experiment:** `ST2-EXP-011 / CLOSED / PASS / LESSON INTEGRATED`  
**orderTotal sensitivity experiment:** `ST2-EXP-004 / CLOSED / PASS / LESSON INTEGRATED`  
**Accepted C:** `C-BLOCK-001` selected producer; `C-BLOCK-002 / CA-20 ACCEPT`  
**Architecture integration authorities:** `BOMA-ST2-LEARNING-INTEGRATION-001`, `BOMA-ST2-LEARNING-INTEGRATION-002`, `BOMA-ST2-LEARNING-INTEGRATION-003`.

## 1. Purpose

Define the **mathematical production interface** that C consumes from R, separately from:

1. the larger historical formal package carried by accepted implementation assemblies;
2. the narrower scalar/coordinate interface consumed by the quadratic comparison Block; and
3. measured sensitivity of current C proof closures to one production field, `orderTotal`.

The governing distinctions are:

```text
selected R producer = R-BLOCK-001 / Dedekind
!=
Dedekind representation internals are premises of C
```

```text
C production mathematical dependency
!=
whole accepted R integration bundle
```

```text
C production dependency
!=
C quadratic-comparison dependency
```

```text
failure of a current proof closure after removing one field
!=
mathematical necessity in every construction
```

## 2. Canonical C production mathematical dependency surface — ST2-EXP-001

`ST2-EXP-001` established that the selected C Claim meaning survives when the whole accepted `RStageIntegrationCertificate` is replaced by exactly these sixteen properties:

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

This sixteen-field surface remains the canonical **production mathematical dependency contract** of `BOMA-C-R-DEP-001`. `ST2-EXP-004` did not shrink or rewrite this accepted contract.

**Scope clarification (owner-authorized 2026-10-28):** these sixteen properties
form a verified sufficient interface for the tested construction. Neither their
direct use by that proof nor the reduction from a twenty-five-field bundle
proves that they are an independent or mathematically minimal axiom set.
Minimality would require a separately stated comparison class and supporting
evidence. This clarification changes no interface field, accepted producer,
Claim meaning, or authorized scientific factor in ST2-RP-001.

Formal witness:

```text
BOMA.C.StageTwo.NarrowRInterface001.NarrowROrderedFieldCertificate
BOMA.C.StageTwo.NarrowRInterface001.narrowRFromAcceptedProducers
```

Source:

`LAB/payloads/lean/CStage/ST2Exp001NarrowRInterface.lean`.

The certificate is assembled directly from accepted R producers rather than by projecting the oversized accepted-R integration certificate.

## 3. Quadratic comparison uses a different, narrower surface — ST2-EXP-011

`ST2-EXP-011` studied the scalar hard-wiring inside the existing `C-COMPARE-BLOCK-001` only.

Exact declaration closure established that the direct comparison proof consumes scalar operations:

```text
zero
one
neg
add
mul
```

plus the quadratic presentation's explicit coordinate interface:

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

This second surface is authoritative inside:

```text
C-COMPARE-BLOCK-001 / C-CL-COMPARE-001
```

and is **not** a replacement definition of `BOMA-C-R-DEP-001`.

Canonical classification:

```text
PRODUCTION C mathematical dependency
  authority = BOMA-C-R-DEP-001
  surface   = exact sixteen properties

QUADRATIC COMPARISON dependency
  authority = C-COMPARE-BLOCK-001
  surface   = zero/one/neg/add/mul + explicit coordinate laws
```

The comparison proof does not directly require scalar order, completeness, density, Archimedean properties, a general field-law bundle, or scalar inverse-existence/uniqueness fields. Its inverse-witness theorem transports a supplied witness rather than selecting one.

## 4. `orderTotal` sensitivity — ST2-EXP-004

`ST2-EXP-004` held the other fifteen ST2-EXP-001 production fields fixed and removed **exactly**:

```text
orderTotal
```

from the research alternative interface.

Seven accepted C Claim families survived the measured alternative:

```text
C-CL-CARRIER-001
C-CL-REMBED-001
C-CL-I-001
C-CL-GEN-001
C-CL-COORDUNIQ-001
C-CL-NONREAL-001
C-CL-COMPARE-001
```

The current proof closures for:

```text
C-CL-FIELD-001
C-CL-INTEGRATION-001
```

did not survive. Their measured dependence is transitive through the current:

```text
square/nonnegative → norm → field
```

proof path.

This is a **current proof-architecture sensitivity result**. It does not establish that every mathematical realization of these C meanings requires total order, and it does not authorize removal of `orderTotal` from the canonical sixteen-property production contract.

The survival of `C-CL-COMPARE-001` independently supports the separation between the sixteen-property production boundary and the smaller ST2-EXP-011 comparison boundary.

## 5. Upstream logical provenance of `orderTotal`

In the selected accepted R producer, `orderTotal` is discharged through `R-DP-003`:

```text
constructive rLE partial-order core
+
localized classical F-04 CutComparability witness
+
constructive totality-from-CutComparability bridge
```

`ST2-EXP-004` established on the unchanged accepted Dedekind representation:

```text
RTotality ↔ CutComparability
```

No unconditional constructive `CutComparability` was recovered from the frozen `LowerCut` fields.

Independent localized commitments remain:

```text
F-05 finite membership / bracketing
F-06 positive representative extraction
F-07 rational density
```

Therefore:

```text
NO F-04 dependency ≠ fully constructive R
formal ancestry ≠ mathematical necessity
```

These upstream facts explain current provenance of `orderTotal`; they do not enlarge the C production contract beyond its sixteen mathematical fields.

## 6. Why the production/comparison/sensitivity distinction matters

The comparison layer answers a narrower question than production of the whole C structure. Therefore its smaller closure cannot be extrapolated into:

```text
"C as a whole needs only zero/one/neg/add/mul"
```

Conversely, the larger sixteen-property production surface cannot be projected onto `C-COMPARE-BLOCK-001` as mathematical necessity merely because the accepted formal implementation has those declarations available upstream.

The Gate-E non-survival of current field/integration proof closures also cannot be promoted into a universal necessity claim.

Dependency architecture follows the measured consumer proof closure at each boundary while keeping accepted contracts and proof provenance distinct.

## 7. Accepted semantics and formal provenance

The existing accepted comparison implementation remains built in the selected `RBOMA / RStageIntegrationCertificate` environment. `ST2-EXP-011` verified a forgetful/generic factoring and proved its accepted relation semantics are definitionally preserved (`related_iff_accepted` by `rfl`).

Therefore:

```text
accepted C Claim meaning              unchanged
accepted CQuadraticComparison001      unchanged
accepted Q/R/C manifests              unchanged
canonical production R→C contract     unchanged
comparison dependency classification  refined
orderTotal sensitivity                recorded as current proof evidence
```

The experimental ST2-EXP-001/011/004 Lean sources remain research-only. A later accepted source refactor would be a separate controlled change.

## 8. Claim-family interpretation of the production surface

The sixteen production properties sit inside accepted R Claim families including:

```text
R-CL-NONTRIV-001
R-CL-ADD-001
R-CL-MUL-001
R-CL-INV-001
R-CL-FIELD-001
R-CL-ORDER-001
R-CL-INTEGRATION-001
```

The following accepted R properties are not mathematical dependencies of the selected C **production** core contract:

```text
R-CL-COMP-001      Dedekind LUB completeness
R-CL-DENSITY-001   Q density in R
R-CL-ARCH-001      Archimedean characterization
R-CL-QEMBED-001    explicit Q embedding, as a direct C requirement
```

They remain valid accepted R properties and may remain in formal ancestry.

The direct comparison Claim remains classified separately:

```text
C-CL-COMPARE-001
  → scalar operations + explicit quadratic coordinate laws
```

## 9. Explicitly prohibited implicit representation dependencies

No C construction may silently treat the following as mathematical premises merely because the selected R producer uses them:

```text
LowerCut
CutEquiv
cutSetoid
principal-cut internals
Dedekind union LUB witness
cut membership search / bracketing
positive/negative-part multiplication implementation
Dedekind reciprocal implementation
route-local proof machinery used only to establish accepted R Claims
```

`RBOMA` remains the selected accepted formal carrier. The prohibition concerns consuming hidden representation history rather than exported mathematical interfaces.

## 10. Route-neutral and alternative-producer evidence

`ST2-EXP-003` established an independent Cauchy real producer and explicit field/order isomorphism with selected Dedekind R. H6 rebuilt seven selected C core meanings natively over Cauchy R.

`ST2-EXP-011` then showed that the H6/RCBOMA research producer can instantiate the generic quadratic comparison interface without H5 `cToD` or selected Dedekind implementation transport.

`ST2-EXP-004` adds a different robustness/sensitivity fact: comparison survives removal of the production `orderTotal` field while the current field/integration proof closures do not.

None of this makes Cauchy R selected or accepted.

## 11. Mathematical dependency versus current formal closure

```text
CANONICAL C PRODUCTION MATHEMATICAL SURFACE
  = sixteen properties from ST2-EXP-001

CANONICAL C COMPARISON MATHEMATICAL SURFACE
  = zero/one/neg/add/mul + coordinate laws from ST2-EXP-011

CURRENT orderTotal SENSITIVITY
  = seven C Claim families survive;
    current field/integration proof closures do not

CURRENT ACCEPTED C FORMALIZATION
  = accepted historical sources/manifests whose actual ancestry may be larger
```

Extra bundled ancestry is formalization/provenance over-bundling, not a license to enlarge mathematical necessity.

## 12. Reopening rule

Reopen the **production** `BOMA-C-R-DEP-001` contract only under a separate controlled act if acceptance changes, a newly accepted C production Claim requires a property outside the sixteen fields, or a future controlled experiment establishes and authorizes a different production contract.

Reopen the **comparison** boundary if `C-CL-COMPARE-001` changes meaning, a comparison theorem consumes a new scalar property, a global selector is proposed, or a future accepted source refactor fails to preserve accepted `Related` semantics.

Formal bundling changes alone do not automatically change either mathematical contract.

## 13. Provenance and evidence

```text
ST2-EXP-001
  production dependency experiment
  CLOSED / PASS / V5 32593045224
  integrated by BOMA-ST2-LEARNING-INTEGRATION-001

ST2-EXP-011
  C-COMPARE-BLOCK-001 scalar/interface experiment
  CLOSED / PASS
  final lifecycle-closed head 632a7134f26daf9dd781e3546804941f429a4246
  merged by 72394878854aa69e865d17567959bec1daa70e6d
  integrated by BOMA-ST2-LEARNING-INTEGRATION-002

ST2-EXP-004
  R-DP-003 F-04 logical-regime / downstream orderTotal sensitivity experiment
  CLOSED / PASS / EXACT F-04 IMPACT CLASSIFIED
  final exact research head 1fe760de811ad2b176ead6f420b80ca1aab5ce46
  research merge 61adb8589c803e95e1b96ef38902320c8aa5df19
  integrated by BOMA-ST2-LEARNING-INTEGRATION-003
```

Architecture integration records:

```text
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_001.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_002.md
LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_003.md
```

## 14. Current boundary summary

```text
upstream selected R export          R-BLOCK-001 / Dedekind
R-DP-003 logical regime             localized classical comparability / retained
C production R→C dependency         exact sixteen-property interface
orderTotal sensitivity              7 C Claim families survive / current field+integration closures do not
comparison scalar dependency        zero/one/neg/add/mul + coordinate laws
comparison Claim owner              C-COMPARE-BLOCK-001
selected C route                    C-ROUTE-P
selected C producer                 C-BLOCK-001
accepted C integration              C-J-001
accepted C export                   C-BLOCK-002 / CA-20
ST2-EXP-001                         CLOSED / PASS / production lesson integrated
ST2-EXP-011                         CLOSED / PASS / comparison lesson integrated
ST2-EXP-004                         CLOSED / PASS / logical/sensitivity lesson integrated
active experiment                   NONE
next experiment                     NOT AUTHORIZED
required next act                   STOP / OWNER AUTHORIZATION REQUIRED
```
