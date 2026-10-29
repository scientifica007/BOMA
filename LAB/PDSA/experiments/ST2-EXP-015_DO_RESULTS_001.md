# ST2-EXP-015 Do results — native Q, native P/Q and external square

**Date:** 29 October 2026  
**Status:** mathematical gates locally verified; exact-head CI and Study/Act pending  
**Frozen Plan:** `1bd27f622753558fb622436d2e27560462ea1771`  
**Frozen baseline:** `575ce175ebc024a33d5c3e7925779b2b8ae9921f`

Gate B was committed at `1a07ebfde2521e32923db0696cd5cd44d935cc83` before
Gate C. The unchanged native-Q source hashes are preserved in its local record.
Gate C was verified afresh on 29 October before the external Gate-D assembly.
The fixed scientific factor and all accepted mathematics remain unchanged.

| Assembly | Sources | Root | Internal declarations | External boundary | Edges |
|---|---:|---|---:|---:|---:|
| Native Q full | 78 | QPresentation015.nativeQFullCertificate | 745 | 80 | 8219 |
| Native Q field | 78 | QQuotientField015.qFieldCertificateFromCauchyR | 663 | 80 | 7471 |
| Native P/Q | 82 | NativePQ015.nativePQJunctionCertificate | 994 | 82 | 11121 |
| External square | 145 | RouteSquare015.routeSquareCertificate | 1793 | 83 | 21391 |

All four measured closures have zero internal axioms, unresolved declarations
and unmapped internal declarations after generated-source inference. The new
verification command regenerates these counts rather than accepting this table
as evidence. Native Q excludes H6/P, H5 and Dedekind at source and declaration
levels. Native P/Q excludes H5 and Dedekind. Only the external square admits H5.

## Four corners and map meaning

| Scalar producer | Route P | Route Q |
|---|---|---|
| Dedekind RBOMA | unchanged accepted CBOMA | unchanged verified 002 quotient |
| Cauchy RCBOMA | unchanged H6/014 CCBOMA | new independently verified 015 quotient |

The native horizontal maps use the unchanged 011 semantics and explicit pair
projections / quotient normalization. Both directions preserve zero, one,
negation, addition, multiplication, scalar embedding, I and supplied inverse
witnesses. The Dedekind horizontal maps are definitionally the retained 002 maps.

The vertical pair maps apply the existing H5 scalar maps to both coordinates.
The vertical quotient maps have explicit coefficient formulas using H5 and
quotient normalization. They are implemented externally through the already
verified horizontal comparisons; they do not establish either native field.
Both vertical directions have verified operation preservation and mutual inverses.

For every native P value z:

`dPToQ (pCToD z) = qCToD (pToQ z)`.

For every Dedekind Q value z:

`pDToC (dQToP z) = qToP (qDToC z)`.

The combined root bundles all preservation and inverse obligations as well as
these square equations. Mere coordinate agreement is not used in place of a
field comparison. Vertical maps change the concrete scalar realization through
H5; they are not linear maps over a single unchanged concrete scalar carrier.

## Verification and recovery scope

`st2_exp_015_verify.py` checks immutable human/machine Plans, baseline controls,
source hashes, exact manifest boundaries, all four kernel/dependency closures,
axioms, nine Claim roots, historical regressions, the six-stage transparency
matrix, architecture/program audits and all 30 governance tests.

The only baseline change outside the four current-state marker files is the
necessary test-harness correction pinned at
`927d78044e3521067709eea5dc306c2ca95cfbc1`; the verifier requires its exact bytes.
Runtime implementation, policy and G8 state are unchanged. Failures 001–004 and
the interruption/reconstruction limit are documented separately.

This is not Study/Act or lifecycle closure. Exact-head GitHub evidence is still
required before either can be completed.
