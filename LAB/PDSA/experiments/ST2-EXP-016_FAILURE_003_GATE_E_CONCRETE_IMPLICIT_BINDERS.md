# ST2-EXP-016 FAILURE 003 — Gate E concrete RBOMA interface binders

**Date:** 2026-10-30  
**Class:** `TECHNICAL_BLOCK / LEAN_BINDER_ELABORATION`; **NOT** mathematical counterevidence.  
**Failed exact head:** `29bc9bdc614153af0dea788a7159767b43fdbee4`  
**Frozen Plan:** `212f4f87fe02af13ef8fd2ed487e0bec18841d88`  
**Scope:** external concrete-RBOMA instantiation ONLY; not abstract 016 proof roots.

## Observed failures (preserved in GitHub Actions)
- Run [41015369686](https://github.com/scientifica007/BOMA/actions/runs/41015369686), job `123930393685`: FAIL.
- Run [41015362741](https://github.com/scientifica007/BOMA/actions/runs/41015362741), job `123930371070`: FAIL.

Both runs stopped during Lean assembly on two signature mismatches:
`narrowRFromAcceptedProducers.orderTrans` and
`narrowRFromAcceptedProducers.orderAntisymm` carry **implicit**
scalar parameters; `RWithoutOrderTotalCertificate` requires **explicit**
parameters for those two fields. No theorem counterexample was observed.
The independent abstract 016 Gate A–D kernels remained unchanged.

## Bounded recovery
At commit `364eb53491074b9734db5705359f1cbdf858dfad`,
the two structural fields were adapted using explicit lambda binders
that delegate to the exact old proofs. No mathematical assumption, result,
carrier, factor, Frozen Plan, acceptance contract, proof oracle or
`SELECTS` was changed. Re-check the exact corrected head in GitHub
Actions; do not claim the concrete certificate is proved until CI says PASS.

The concrete source is intentionally segregated from the abstract
`NormAnisotropy016` dependency roots because its construction reuses the
selected RBOMA's inherited order and classical resources. It does not
prove global elimination of totality.
