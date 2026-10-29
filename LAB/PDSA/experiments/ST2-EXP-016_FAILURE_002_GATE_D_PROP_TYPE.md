# ST2-EXP-016 Failure 002 — Gate D Prop/Type distinction

**Exact head:** `94fb171ab7eb65098865624f5dcbf2f4761a8f2d`; **run:** `40971069474`; **job:**
`123787645262`; **classification:** `TECHNICAL_BLOCK`,
not a mathematical counterexample. The prior successful Gate D
head `47c1e6414eff02f661bd5c41fe976e62aad88ecf`
remains immutable historical evidence.

## What failed
The attempt to extend the nine-family research integration package
with *functional comparison data* made a Prop-valued certificate
contain a Type-valued `ConstructiveQuadraticIsomorphism`. Lean
correctly rejected the generated projection and the declarations
previously marked `theorem` for Type-valued results.

## Recovery without factor change
Make the candidate integration package a **Type-valued structure**
instead of `Prop`, and use `def` for its two data-returning
constructors. The mathematical factor, fifteen scalar controls,
nonzero inverse witness proof and required explicit
`CoordinateExtractor` are unchanged. Re-run independent kernel and
declaration checks and retain the failing CI record.

**Why relevant:** BOMA's relation-versus-function firewall requires
actual coordinate extractor data; functional comparison is not merely
a proposition that can be silently inferred from an existential
relation.
