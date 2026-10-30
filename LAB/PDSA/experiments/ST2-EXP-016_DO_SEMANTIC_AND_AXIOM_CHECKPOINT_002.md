# ST2-EXP-016 — Do checkpoint 002: explicit Claim meanings and inherited axiom cost

**Recorded:** 2026-10-30  
**Lifecycle:** `DO_ACTIVE / KERNEL_RESEARCH_CHECKPOINT / NOT_STUDY_ACT / NOT_CLOSED`  
**Frozen Plan (immutable):** `212f4f87fe02af13ef8fd2ed487e0bec18841d88`  
**Main baseline for owner-authorized Do:** `895384b5617763622be4cc2b53fe3bc0686eac62`  
**Verified exact Do source head before this record:** `c0bfd11e6b00ecbb46c884917ef87cb3b1c34cbd`  
**Research branch:** `feature/stage-two-st2-exp-016-norm-anisotropy`  
**Authority:** owner-directed interactive PDSA, Do authorized; no merge or 017 authorization.

## Plan and fixed scientific control
The Plan's single changed factor is *only*
`NarrowROrderedFieldCertificate.orderTotal` replaced with
`NormAnisotropy016`:
`a²+b²=0 → a=0 ∧ b=0` on the same `RBOMA` carrier.
The other fifteen scalar properties, C Route P, the nine accepted Claim
**meanings**, all accepted Q/R/C sources, manifests, `SELECTS`,
all historical Plans and evidence remain fixed. G8 stays disabled.

## Do — exact new work after the first 016 kernel checkpoint
1. Added `NineClaimMeaningCertificate016` and root
   `nineClaimMeaningCertificate016` to the **research-only**
   `ST2Exp016FieldIntegration.lean`. The explicit typed certificate now
   exposes separate obligations for all nine Claim families, instead
   of relying solely on the earlier generic `nineClaimCandidate016`
   wrapper. It explicitly includes scalar/pair nontriviality,
   embedding preservation, field laws, norm-based nonzero inverse witness
   existence/uniqueness, `i²=-1`, generation, unique coordinates,
   nonrealness, comparison and extractor-conditional functional isomorphism.
   This is a research certificate and does **not** modify or re-export CA-20.
2. Added `LAB/20_FORMALIZATION/C_STAGE/ST2_EXP_016_CLAIM_MEANINGS.json`,
   a typed nine-Claim inventory whose `closed_acceptance_contract`
   remains `false`. Added the new proof root to Gate D's exact
   declaration-closure workflow, rather than accepting a source-text
   assertion as proof.
3. Added the read-only `st2_exp_016_gate_e_axioms.py` checker, called
   inside the verification-only Gate D workflow. This independently
   assembles the fixed 016 manifest, runs Lean `#print axioms` on
   `normBridgeCertificate016`, `fieldCertificate016` and
   `nineClaimMeaningCertificate016`, rejects unexpected axioms, and
   writes an artifact report. It does not instantiate the new condition
   on concrete `RBOMA` or promote experimental meaning to acceptance.
4. The exact head `c0bfd11e6b00ecbb46c884917ef87cb3b1c34cbd`
   passed **25/25 GitHub checks** with no failures or pending checks,
   including the experimental 016 kernel jobs, independent accepted C
   verification, historic 004/011/014/015 CI, program governance and
   `guard`. This is a verified Do head, **not** the final lifecycle
   verified head after this bookkeeping record.

## Measured kernel logical cost
Verification-only workflow run `41014288423`, job `123926974192`,
artifact `12959211038`,
artifact SHA-256:
`04606f0c54642bda936f32c37d839a772c497e74d931b1deee2367ed5a61708e`.

Independent run `41014282907`, job `123926956455`,
artifact `12958702745`,
artifact SHA-256:
`3ab35dbdc3043b765737457e06ba274f117e4aff93d41ec2ba92c67a5d8037c6`.

Both exact job logs explicitly report the following inherited axiom set
for **each of the three tested abstract roots**:

```text
Classical.choice
Quot.sound
propext
```

No unexpected axiom was accepted; the declaration audit on the 016 roots
remained `PROTOTYPE_PASS`, with no unresolved dependencies and no
internal axioms. The checker still forbids an `.orderTotal` declaration
or `rLE_total_classical` witness in the abstract field/integration
dependency closure. This does **not** establish absence of all
order-related assumptions: the fixed fifteen-field scalar interface
still includes ordered laws, notably `orderMulNonneg`, and the
concrete Dedekind real implementation has inherited classical costs.

## Traceable Claim inventory — research, not acceptance promotion
| Accepted Claim | Research witness |
| --- | --- |
| `C-CL-CARRIER-001` | `carrierExt` |
| `C-CL-REMBED-001` | `embeddingInjective/Zero/One/Neg/Add/Mul` |
| `C-CL-FIELD-001` | `scalarNontrivial`, `pairNontrivial`, `field` |
| `C-CL-I-001` | `generatorSquared` |
| `C-CL-GEN-001` | `realGeneration` |
| `C-CL-COORDUNIQ-001` | `coordinateUnique` |
| `C-CL-NONREAL-001` | `imaginaryNotReal` |
| `C-CL-COMPARE-001` | `comparison`, `functionalComparison` (explicit extractor) |
| `C-CL-INTEGRATION-001` | `nineClaimMeaningCertificate016` (experimental assembly) |

The accepted integration is based on `CStageIntegrationCertificate`,
which also contains inherited implementation-level auxiliary structures.
The research `normNonnegative` auxiliary is deliberately *not*
restored by simply assuming orderTotal. Whether the accepted
CA-04/CA-19 semantic requirements are all exactly discharged by
this replacement still requires a separate **semantic equivalence
assessment**; Lean's successful typing of the nine fields alone
is not an acceptance or minimality proof.

## Work still open — no Study/Act verdict now
- Detailed crosswalk between original accepted CA-04/CA-19 meaning and
  the research field/integration roots, including the treatment of
  `normNonnegative`; no silent contract weakening.
- Separate provenance and logical-cost measurement for a *concrete*
  `RBOMA` instantiation of `NormAnisotropy016`, distinct from the
  abstract conditional theorem.
- Gate F final-head proof of frozen-file hashes, regressions and full CI
  after all Do evidence, then future H1–H6 Study / owner Act and lifecycle
  closure if authorized in a later task.

**Do checkpoint only:** no `CLOSED_PASS`, no accepted C change,
no global elimination-of-order claim, no automatic PR merge, no
autonomous restart and no start of `ST2-EXP-017`.
