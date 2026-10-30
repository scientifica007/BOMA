# ST2-EXP-016 — Failure 005: generated coordinate provenance (TECHNICAL_BLOCK)

**Date:** 2026-10-30. **Owner scope:** bounded third Do only.  
**Classification:** `TECHNICAL_BLOCK / GENERATED_SOURCE_RANGE_ATTRIBUTION`; NOT a mathematical counterexample, accepted C inverse leakage, or an unproved Lean theorem.

Two independent dedicated verifier jobs initially failed at scientific head `2338a937f4b485d7df2dc9ac133caf6d600af66b`:
- [run 41034988899](https://github.com/scientifica007/BOMA/actions/runs/41034988899), job 123993526140;
- [run 41034982793](https://github.com/scientifica007/BOMA/actions/runs/41034982793), job 123993504451.

The Lean declaration extractor reported `PROTOTYPE_PASS`, zero unresolved names and zero internal axioms, but the separate strict research provenance checker rejected ten unmapped generated source ranges. A diagnostic retry at `e2a16ba` exposed the count; at `63108ef` it identified precisely `BOMA.C.QuadraticComparison001.selectedPresentation._proof_1..10`; at `005a468` the dependency edge showed `researchSelectedPresentation016 → selectedPresentation._proof_1` and classified these as fixed historical coordinate proof helpers. They are sourced from `LAB/payloads/lean/CStage/CQuadraticComparison001.lean`, **not** an 016-owned proof source. Existing accepted C `c_inverse_exists`, full `selectedPresentation`, old accepted field-certificate producer and old integration producer remain disallowed in the four root closures.

Resolution at `a4a17e01df02be241bb36dee2769aa89ce5a5341`: the dedicated research checker explicitly accounts for precisely those ten generated coordinate helpers by source and identity, while refusing any additional unmapped name and continuing to reject accepted inverse/field/integration oracles. Two independent CI checks then passed; failed attempts remain durable evidence. No frozen scientific condition or accepted source changed. This is a **bounded provenance classification**, not evidence that the entire package is source-independent or newly CA-17/18/19 accepted. No Study/Act/merge/017 authorized.
