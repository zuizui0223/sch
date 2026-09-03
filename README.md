# Shared Cue Hypothesis (SCH)

SCH is the one-trait mechanism chapter paired with [BITA](https://github.com/zuizui0223/bita). The programme asks one sequence:

```text
SCH:  why does one floral attraction/display coordinate become conflicted?
BITA: can a distinct defence coordinate release that conflict?
```

The central SCH contribution is now **mechanism identification**, not a literature review. Existing literature is retained as real-world evidence that the proposed routes, conflicts and evolutionary consequences actually occur in nature, and as a map of which identifying measurements are usually missing.

## Scientific target

For one predeclared attraction/display manipulation `A`, SCH asks whether pollinators increase the reproductive value of `A` while antagonists decrease the reproductive value of that **same coordinate**.

The core experiment is a crossed

```text
A x antagonist x pollinator
```

**8-cell selective-intervention design** on one common plant reproductive outcome.

Write the attraction effect in each consumer state as

```text
d[g,p] = W[1,g,p] - W[0,g,p].
```

Then identify:

```text
M_A(g) = d[g,1] - d[g,0]
         pollinator-mediated contribution

G_A(p) = d[0,p] - d[1,p]
         antagonist-mediated loss

B_A    = d[0,0]
         consumer-independent remainder

J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0]
         channel-dependence diagnostic
```

A positive `M_A` means pollinator access makes attraction more reproductively beneficial. A positive `G_A` means antagonist access erodes that benefit. `B_A` is not automatically a physiological/construction cost; it remains unallocated unless an independent assay identifies it.

The strongest contemporary shared-cue result therefore requires both:

1. **informational overlap** — the same sensory/display coordinate of `A` is used by both receiver classes; and
2. **functional conflict** — selective intervention shows pollinator-mediated gain and antagonist-mediated loss on that same `A` contrast.

The mechanism and inference contract is frozen in `docs/SCH_MECHANISM_IDENTIFICATION_DESIGN_V1.md`.

## Constraint result to be tested

Under natural pollinator access,

```text
G_A(1) = d[0,1] - d[1,1].
```

If `G_A(1) > 0`, antagonist presence flattens the attraction-fitness effect relative to an antagonist-free state. Stronger outcomes are predeclared separately:

```text
constraint attenuation:              0 < d[1,1] < d[0,1]
constraint release by antagonist removal: d[1,1] <= 0 < d[0,1]
strict sign reversal:                    d[1,1] < 0 < d[0,1]
```

These are reproductive mechanism claims. They do not by themselves establish historical evolution of a private cue.

## Role of the literature evidence

The PRISMA programme, targeted primary-source audits and evolutionary-outcome audit remain in SCH, but their role is now explicitly secondary to the identification framework.

They provide four kinds of grounding:

- **route reality:** attraction/display traits affect pollinators and antagonists in real systems;
- **outcome reality:** compromise, polymorphism, population change and partial cue decoupling are documented evolutionary outcomes;
- **design-gap evidence:** manipulation, both consumer channels and a common reproductive outcome are rarely measured together;
- **historical extension:** systems such as *Ficus* locate candidate shared/private transitions that can be tested only after matched receiver states are measured on the same cue coordinate.

The frozen systematic cohort currently contains 868 records. Through V20, 405 have title/abstract decisions, 117 primary studies are included, and two studies satisfy the strict linked measurement architecture. Those counts are **not the main SCH estimand and are not prevalence estimates**. They show that the mechanism components are biologically real while complete identification remains rare.

## Current positive evidence

The source spine already supports several bounded ecological conclusions:

- floral attraction/display coordinates can influence both mutualist and antagonist routes;
- opposing biotic effects can produce an integrated compromise;
- context-dependent selection can maintain alternative phenotypes;
- antagonists can redirect population-level floral evolution;
- bouquet partitioning, conditional emission and temporal separation can partially decouple receiver effects.

What remains unproven is the stronger historical claim that dual-audience selection repeatedly transformed an ancestral shared cue into a pollinator-private cue or distinct audience-specialized lineages. *Ficus* remains `COMPOSITE_NEAR_L4`, not `DIRECT_L4`.

Thus the current status is:

```text
REAL_WORLD_MECHANISM_COMPONENTS_RECOVERED
COMPLETE_SCH_CHANNEL_IDENTIFICATION_NOT_YET_EXECUTED
HISTORICAL_SHARED_TO_PRIVATE_TRANSITION_NOT_YET_IDENTIFIED
```

## SCH -> BITA

SCH and BITA now form an explicit experimental ladder.

```text
Chapter 1 — SCH
A x antagonist x pollinator
8 cells
-> identify the one-trait dual-audience conflict

Chapter 2 — BITA
A x D x antagonist x pollinator
16 cells
-> test whether a distinct defence coordinate releases the conflict
   and allocate antagonist relief, pollinator interference and joint cost
```

SCH therefore establishes **why attraction is constrained**. BITA asks **whether and why defence provides an escape route**.

## Repository map

- `docs/SCH_MECHANISM_IDENTIFICATION_DESIGN_V1.md` — canonical 8-cell mechanism-identification contract
- `manuscript/MANUSCRIPT_SHARED_CUE_FRAMEWORK.md` — mechanism-first paper concept and evidence grounding
- `docs/CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md` — SCH Chapter 1 -> BITA Chapter 2 research programme
- `empirical/one_trait_shared_cue/` — source adjudications, evolutionary outcomes and historical extensions
- `empirical/prisma/frozen_v2/` — immutable 868-record systematic denominator
- `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv` — evidence roles and claim ceilings
- `docs/PUBLICATION_MATERIAL_LEDGER.md` — mechanism-first publication material and remaining gates
- `scripts/build_one_trait_coverage_audit.py` — deterministic legacy/coverage audit builder
- `docs/MIGRATION_RECEIPT.md` — BITA-to-SCH ownership boundary and provenance

## Immediate empirical programme

```text
Stage 0  validate one A coordinate and paired receiver access
Stage 1  pilot A x antagonist x pollinator and estimate channel-scale variance
Stage 2  re-power and execute the confirmatory 8-cell experiment
Stage 3  independently assay the consumer-free remainder / direct cost
Stage 4  extend to multiple A levels, populations or experimental evolution
```

Literature-derived visitor effects must not be used as substitutes for channel-scale pilot effects when powering the confirmatory mechanism experiment.

## Status

SCH is now organized as a **mechanism-first empirical programme with a real-world evidence spine**. The systematic review remains useful and should continue, but it no longer determines the scientific identity of the project. The decisive future result is a same-coordinate, selective-intervention decomposition of pollinator gain, antagonist loss and their realized effect on attraction fitness; BITA then tests whether an added defence coordinate releases that identified conflict.
