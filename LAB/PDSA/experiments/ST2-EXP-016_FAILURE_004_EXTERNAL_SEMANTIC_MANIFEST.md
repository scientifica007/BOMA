# ST2-EXP-016 FAILURE 004 — external semantic bridge manifest omission

**Date:** 2026-10-30  
**Head:** `c32987a5fd02f1c4f5a42fc661732bc73d1fef68`.  
**Failed exact Actions runs:** [41024586871](https://github.com/scientifica007/BOMA/actions/runs/41024586871), job `123959567655`; [41024579583](https://github.com/scientifica007/BOMA/actions/runs/41024579583), job `123959543632`.  
**Classification:** `TECHNICAL_BLOCK / MISSING_HISTORICAL_NARROW_SOURCE_IN_EXTERNAL_MANIFEST`. **Not a mathematical counterexample**.

The first external bridge manifest combined accepted C sources and the four abstract 016 dependencies plus `ST2Exp016ConcreteRBOMA.lean`, but omitted `ST2Exp001NarrowRInterface.lean`, `ST2Exp001NarrowPairCore.lean`, and `ST2Exp001NarrowPairNormInverse.lean` and related historical narrow files. Lean first reported unknown namespaces `NarrowRInterface001`, `NarrowPairCore001`, `NarrowPairNormInverse001` then unresolved historical projection names. The bridge's mathematical question was not resolved by those failed assemblies.

**Bounded repair:** at `bd97b0c7841af83cd5119be87be2c953b3a6072c` the independent **external-only** manifest was rebuilt from the already verified concrete 016 manifest, with the new bridge last, preserving 107 unique source paths. No accepted source, 016 factor, Frozen Plan, research abstract source, new axiom or selector changed. New bridge exact-head Lean CI subsequently passed. The unsuccessful runs remain immutable evidence.

**Governance:** no Act, merge, acceptance promotion, 017 or autonomous engine restart.
