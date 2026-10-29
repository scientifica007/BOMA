# ST2-EXP-016 Failure 001 — Gate D unbound algebraic helper

**Date:** 2026-10-29  
**Head:** `5d39a2ce0e40753abda45976eb05219be701880b`  
**Workflow run:** `40970574189` (push), job `123786000663`  
**Status:** `TECHNICAL_BLOCK / LEAN_UNKNOWN_IDENTIFIER`  
**Not a mathematical counterexample.**

## Do attempt
A research-only Gate D candidate re-derived the Route-P ring laws
from 004's fifteen-property interface and proposed the complex inverse
witness and nine-Claim integration candidate. Its source compilation
reported two `error(lean.unknownIdentifier)` diagnostics at assembled
file lines 9738 and 9782: `neg_zero_from_interface`.

## Diagnosis
The proof transformations retained a historical helper name from
ST2-EXP-001. Under the intentionally narrower 004 assembly the correct,
already verified exact fifteen-property lemma is `neg_zero004`.
No `orderTotal`, extra algebraic assumption or new selector was required.
The source did not reach a passing dependency closure on this attempt.

## Recovery
Replace **only** the two unbound helper references with `neg_zero004`;
preserve this failed run and re-execute the exact-head Gate D Actions
proof. Failure evidence must not be deleted, retroactively classified
as PASS, or used to alter the frozen success criteria.

**Previous verified independent Gates A–C:** run `40970041831`,
artifact `12939647210`, head `41770de4996fb95f39c438402e44aaaf561d8167`.
