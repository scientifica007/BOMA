# ARCHITECTURE — Auditable Construction System

## Status

**ACTIVE — Canonical project architecture**

## Purpose

This file defines the permanent engineering architecture of the transparent mathematical construction.

The project is represented as an **auditable dependency graph**, not as a linear sequence of documents.

### Mandatory graph-topology specialization

For the canonical operational interpretation of serial dependencies, horizontal independence, parallel convergence, branching, and branch reconvergence, every human or AI collaborator must also read:

```text
LAB/00_ARCHITECTURE/CONSTRUCTION_TOPOLOGY.md
```

That document is authoritative for graph-topology questions under this architecture. In particular:

```text
construction DAG ≠ forced linear chain
fork ≠ Decision Point by default
meeting ≠ verified Junction by default
reconvergence preserves branch provenance
```

The current program gives particular attention to scientifically meaningful:

```text
split → independent development → verified reconvergence
```

patterns when the mathematics naturally supports them.

This specialization was adopted through:

```text
PDSA-ARCH-001 — Construction Topology Adoption
```

The construction objective is:

```text
declared pre-numerical constructional starting point
        ↓
explicit construction
        ↓
constructed mathematical structure
        ↓
explicit formalization boundary
        ↓
formal realization
        ↓
natural numbers
        ↓
integers → rationals → reals → complex numbers
```

The diagram is a target architecture, not a requirement that every local dependency graph be linear.

## Governing research method

New research work follows:

> **PDSA — Plan, Do, Study, Act**

Historical paths or files containing `PDCA` are legacy provenance only.

The governing correction and methodology record is:

`LAB/BOMA_PDSA_GOVERNANCE_AND_PDCA_LEGACY_CORRECTION_2026-08-18.md`

PDSA produces two linked outputs:

```text
CONSTRUCTION OUTPUT
mathematical units and their dependency graph

LEARNING OUTPUT
errors, successes, corrections, methodological lessons, decision criteria,
and human–AI research learning
```

### Learning-to-Construction integration rule

A verified Learning-Graph result is not required to remain permanently outside
the Construction DAG. When an experiment closes successfully and the owner
explicitly authorizes architectural integration, the **knowledge established by
the experiment** may become permanent Construction-DAG knowledge.

Permitted integration forms include:

```text
refine an existing dependency contract;
preserve a verified non-selected route as a permanent alternative branch;
preserve a verified reconvergence as a permanent Junction;
expose a representation-independent reusable contribution;
record a new sensitivity/reopening/genericity condition.
```

The following implications are forbidden:

```text
permanent DAG visibility ≠ SELECTS
permanent DAG visibility ≠ ACCEPTED EXPORT
verified alternative ≠ canonical producer
successful experiment ≠ automatic acceptance promotion
```

Thus the Construction Graph may contain both the selected canonical route and
verified non-selected alternatives. The Learning Graph continues to preserve
**how** those facts were discovered, including Frozen Plans, failed attempts,
exact evidence, Study/Act decisions, and owner authorization.

If integration changes `SELECTS`, replaces an accepted Block/export, or adds a
new accepted Claim, that requires a separate explicit Decision/acceptance action
and corresponding verification. Architectural learning integration alone has no
such authority.

The first owner-authorized application of this rule is:

`LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_001.md`.

## Canonical unit types

### Brick

The smallest independently reviewable and changeable mathematical construction unit at the declared project granularity.

A Brick must have:

- unique ID;
- explicit inputs;
- explicit construction rule or declared constraint;
- explicit outputs/effect;
- invariants;
- operational status;
- verification status/evidence;
- epistemic status;
- dependencies;
- sensitivity/change impact;
- relevant PDSA provenance when created or changed under the current method.

A Brick's graph orientation does not determine whether it is a Brick. A Brick may be dependency-free, vertically dependent, horizontally independent of sibling units, branch-specific, or one of several contributors to a convergent downstream unit.

### Block

A coherent cluster of Bricks that establishes one higher-level structure.

A Block has:

- input interface;
- internal Bricks or declared internal construction components;
- internal relations;
- output interface;
- acceptance criterion;
- operational and epistemic status;
- PDSA provenance where applicable.

A Block may contain serial or parallel internal structure. Composition must preserve Brick identities and provenance.

### Junction

A **compatibility / convergence gate** where construction paths, representations, interfaces, or constraints must be reconciled before downstream promotion.

A Junction is not the unit used merely to choose among admissible alternatives.

A Junction must record:

- incoming units;
- compatibility condition;
- identification/translation rule where applicable;
- shared output or admitted downstream transition;
- possible conflicts/failure modes;
- verification status;
- operational status;
- epistemic status;
- sensitivity and reopening conditions.

A Junction may reconcile branches that arose from a Decision Point or combine parallel non-alternative contributions. A visual meeting of paths is not sufficient evidence of convergence.

### Decision Point

An explicit architectural unit recording a **non-derived selection problem** between two or more admissible methodological, foundational, representational, logical, or formalization alternatives.

A Decision Point exists when the project must choose a route and the choice is not already forced by a proved compatibility/derivability result.

A Decision Point must record:

- unique ID;
- incoming dependencies and the question requiring a choice;
- admissible options/branches with distinct identities or explicit option IDs;
- `ALTERNATIVE_TO` relations where applicable;
- evaluation criteria;
- new commitments introduced by each option;
- current operational status (`OPEN`, `RESOLVED / SELECTED`, etc.);
- selected option if resolved;
- epistemic status of the selection, normally `DECLARED CHOICE`, `METHODOLOGICAL CHOICE`, or `FORMALIZATION-DEPENDENT` rather than `DERIVED`;
- rationale and PDSA evidence;
- downstream consequences;
- reopening/sensitivity conditions;
- preservation status of non-selected alternatives.

A selected option does not become mathematically necessary merely because it is the canonical route.

### Configuration

A mathematical or constructional object produced by one or more construction units.

A document describing a configuration is not the configuration itself.

## Canonical graph relations

Only these graph relations are admitted unless the architecture is explicitly revised:

```text
DEPENDS_ON
COMPOSES
REFINES
VERIFIES
CONSTRAINS
ALTERNATIVE_TO
MEETS_AT
REPRESENTS
BRANCHES_TO
SELECTS
```

### Decision relations

```text
DecisionPoint --BRANCHES_TO--> Option
DecisionPoint --SELECTS-----> SelectedOption
```

`SELECTS` records a project choice. It must never be interpreted as `DERIVES`.

Non-selected options remain traceable and may later become verified permanent
alternative branches without becoming selected.

### Topology interpretation

The same relation vocabulary may participate in different graph topologies:

```text
serial dependency
horizontal independence
parallel convergence
Decision Point branching
exploratory branching
verified reconvergence through Junctions
permanent verified alternative branches learned through PDSA
```

The detailed rules and fork taxonomy are defined by `CONSTRUCTION_TOPOLOGY.md`.

## Operational status

Operational status records where a unit is in the active project lifecycle and graph. Typical values include:

```text
ACTIVE
OPEN
RESOLVED / SELECTED
PASS / RESOLVED
CONDITIONAL / PENDING
RESERVED
REJECTED
ARCHIVED
```

Operational status answers questions such as:

- Is the unit currently part of the active graph?
- Is it blocked at a gate?
- Is it an unresolved Decision Point?
- Has an option been selected for the canonical route?
- Is its identity only reserved for future work?
- Has it been rejected or archived?

## Verification levels

```text
V0  idea
V1  explicit construction
V2  local verification
V3  dependency-compatible verification
V4  cross-path verification
V5  formal verification under selected regime
```

Verification level is not the same as operational or epistemic status.

## Epistemic status

Epistemic status records **how the content is justified**, independently of whether the unit is operationally active.

Every active unit or explicit subclaim must declare, where applicable, one of:

```text
CONSTRUCTED
DERIVED
DECLARED CHOICE
METHODOLOGICAL CHOICE
FORMALIZATION-DEPENDENT
PENDING
REJECTED
```

A declared additional constraint can be operationally ACTIVE while epistemically a DECLARED CHOICE until/unless a later proof reclassifies its current-path role.

A Decision Point selection is normally not a theorem; its status must remain a choice unless necessity is independently proved.

## Status-separation invariant

The following dimensions must not be collapsed:

```text
Operational Status
Verification Status / Evidence
Epistemic Status
```

Historical example:

```text
TCT-BR-009
Earlier state under incomplete ≈:
  Operational Status = ACTIVE
  Epistemic Status   = DECLARED CHOICE — ADDITIONAL CONSTRAINT

Current path after BR-010 / PDSA-TCT-004:
  Operational Status = ACTIVE
  Epistemic Status   = DERIVED UNDER TCT-BR-010
```

The earlier state remains provenance rather than being rewritten away.

## Sensitivity rule

Every Brick and every high-impact Block/Junction/Decision Point must answer:

```text
If this unit or selection changes:

What remains valid upstream?
Which descendants require retesting?
Which sibling/alternative units may become active or incompatible?
Which Junctions must be reopened?
Which Decision Points must be reconsidered?
Which PDSA results or learning claims must be revisited?
```

For reconvergent structures, sensitivity analysis must also identify whether a change invalidates only one branch, the Junction proof, or the shared downstream contribution.

## Architectural invariants

1. No unit may silently replace another unit.
2. Alternatives receive distinct IDs or explicit versioned revisions when identity is intentionally preserved.
3. A Junction may not hide an unresolved incompatibility.
4. A Decision Point may not present a selected option as a derived necessity without proof.
5. A pending result cannot become accepted because a downstream document exists.
6. Historical material is preserved when scientifically relevant.
7. Geometry or visualization is a representation unless explicitly promoted to mathematical structure.
8. Numerical concepts are not used as hidden premises in the pre-numerical object layer.
9. The pre-numerical layer is not metatheory-free; its meta-level resources must be declared.
10. Construction is distinguished from numerical/algebraic interpretation.
11. Operational status, verification status, and epistemic status remain distinct.
12. Scientifically relevant failures and corrections remain traceable through PDSA learning records.
13. AI-generated content never becomes canonical solely because it is fluent or plausible; appropriate verification and human research authority remain explicit.
14. Non-selected Decision Point options remain traceable for later branch comparison unless explicitly rejected for a documented reason.
15. Repository or document order must not be treated as mathematical dependency order.
16. Independent horizontal units must not be forced into false dependencies for presentation convenience.
17. A fork must be classified before it is represented as a Decision Point.
18. Reconvergence requires explicit evidence and an appropriate Junction/compatibility record.
19. Reconvergence does not erase branch provenance or imply identical construction histories.
20. Same reusable certified contribution may have multiple distinct producer paths, provided their convergence/translation is explicitly verified.
21. A successful experiment may refine the permanent Construction DAG only through an explicit Study/Act classification and owner-authorized integration action.
22. Integrating verified knowledge does not by itself promote a producer, change `SELECTS`, or change an accepted export.
23. A verified non-selected route may remain permanently visible in the Construction DAG with its distinct evidence and provenance.
24. When a successful experiment demonstrates a smaller sufficient dependency interface, the architectural dependency contract should record that verified sufficient surface even if legacy implementation bundles remain larger. A measured proof-dependency surface does not by itself establish mathematical minimality or independence of its fields. Any minimality claim must state its comparison class and carry separate evidence that justifies that stronger claim.

The 2026-10-28 owner-authorized clarification is recorded in
`LAB/PDSA/reviews/BOMA_MATHEMATICAL_AUDIT_CORRECTIONS_2026-10-28.md`.
Historical experiment and integration records retain their original wording;
their measured dependency results must be read at the scope actually verified.

## Repository structure

Current canonical structure:

```text
LAB/
├── 00_ARCHITECTURE/
├── 10_CONSTRUCTION/
│   ├── blocks/
│   ├── bricks/
│   ├── junctions/
│   ├── decisions/
│   └── experiments/
├── 20_FORMALIZATION/
└── 90_ARCHIVE/
```

The PDSA research-process record is maintained separately under:

```text
LAB/PDSA/
```

Repository-level handoff/discovery files:

```text
README.md
AGENTS.md
```

`00_ARCHITECTURE` defines the active construction system.

`10_CONSTRUCTION` contains active construction units, gates, and explicit Decision Points.

`20_FORMALIZATION` contains explicit formal realizations.

`90_ARCHIVE` contains historical or superseded material when migrated there intentionally.

`PDSA` records cumulative research cycles and learning. A PDSA record is not itself automatically a canonical mathematical unit.

## Authority rule

The sequence of documents is only a **view** of the construction graph.

The canonical graph and unit identities are authoritative for mathematical construction status.

`LAB/00_ARCHITECTURE/CONSTRUCTION_TOPOLOGY.md` is authoritative for the operational interpretation of serial/parallel/fork/reconvergence topology.

PDSA cycle records are authoritative for the recorded research process and learning associated with those cycles, subject to later additive correction rather than silent rewriting.

## PDSA-N-002 architectural revision note

The explicit `Decision Point` unit type and `BRANCHES_TO` / `SELECTS` relations were added when the project reached its first major formal-realization choice.

This restores a core BOMA concept to the canonical engineering architecture rather than hiding formalization choices inside narrative text.

## PDSA-ARCH-001 architectural revision note

`PDSA-ARCH-001 — Construction Topology Adoption` consolidated prior Brick/Block/DAG/branch learning into the explicit canonical topology rules in:

```text
LAB/00_ARCHITECTURE/CONSTRUCTION_TOPOLOGY.md
```

It also established `README.md` and `AGENTS.md` as mandatory repository-level handoff entry points.

## BOMA-ST2-LEARNING-INTEGRATION-001 architectural revision note

Owner-authorized integration of `ST2-EXP-001..003` established that successful
experiment knowledge may become permanent Construction-DAG knowledge without
rewriting Decision selection or accepted exports. The authoritative Act is:

`LAB/PDSA/STAGE_TWO_SUCCESSFUL_EXPERIMENTS_ARCHITECTURE_INTEGRATION_001.md`.
