# Finalization recovery — test fixtures only

The lifecycle commit d91b32250f4cdc800f26b728e388902797bf5200 passed all 20 checks.
The subsequent state update correctly clears 015 and exposes 016 as held by the
bounded owner instruction. A second live-state coupling in two existing tests
then surfaced: their assertions concern the 015 planner contract, while their
mock left the current target unbound and the planner correctly selected 016.

Failure 005 records the exact observed expected/actual mismatch. The tests now
supply the already defined 015 prestart fixture and retain the same field-injection
and conflict-rejection assertions. The verifier's protected-test comparison is
updated to an exact Git blob hash; no broad exclusion or test skip is introduced.
The initial repair commit remains an ancestor requirement. All mathematical,
manifest, Plan, workflow, Study/Act and original closure bytes are unchanged.

This is a disclosed technical recovery during finalization, not a retroactive
claim that the changed verification harness was checked at the old closure head.
The earlier closure record's intended no-drift rule remains mandatory for science
and closed evidence; this explicit exception is limited to the test fixture and
its byte pin. It falls under the Frozen Plan's technical CI recovery envelope and
the direct owner's necessary-corrections authorization. Finalization must pass
all exact-head checks afresh before merge. No 016 Plan is authored or frozen.
