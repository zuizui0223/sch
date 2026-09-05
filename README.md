# Shared Cue Hypothesis (SCH) — Chapter 1 / Trait Balance

SCH is the **Chapter 1 / BALANCE** half of the SCH–BITA trait-architecture programme.

```text
SCH / Chapter 1 — BALANCE
multiple functions remain coupled on one trait coordinate z
-> where is the best shared phenotype z*?
-> how much residual conflict remains because the functions must share that axis?

BITA / Chapter 2 — DIFFERENTIATION
allow partly independent trait coordinates
-> how much of the Chapter 1 conflict load can be recovered?
-> does that recovery pay for the extra architecture?
-> what mechanism makes the resulting multi-trait phenotype work?
```

The programme is about **trait trade-offs and architecture**, not specifically pollination versus defence. SCH's most developed empirical case remains floral cue sharing between pollinators and antagonists. BITA's most developed worked case is the mechanism identification of a multi-trait floral phenotype.

## Canonical programme-level Chapter 1 question

> **How do conflicting functions resolve selection while they remain coupled on one trait, and what shared conflict load remains after the best one-axis phenotype is chosen?**

Let one trait coordinate `z` contribute to two functions with loss components `l1(z)` and `l2(z)`:

```text
L_S(z) = l1(z) + l2(z)
z*     = argmin_z L_S(z)
L_S*   = L_S(z*)
```

`z*` is the best phenotype attainable while the functions remain coupled to one coordinate. `L_S*` is the residual shared-axis conflict load on the declared scale.

For the quadratic baseline shared with BITA,

```text
L_S(z) = w1(z-theta1)^2 + w2(z-theta2)^2

z* = (w1 theta1 + w2 theta2)/(w1+w2)

L_S* = [w1 w2/(w1+w2)] (theta1-theta2)^2.
```

This `L_S*` is the exact baseline inherited by BITA Chapter 2. BITA asks how much of it is recoverable after partial differentiation and compares that recovery with the extra architecture cost.

The full cross-chapter contract is `docs/SCH_BITA_SYMMETRY_CONTRACT_V1.md`.

## Floral shared-cue worked case

For one predeclared attraction/display contrast `A`, SCH's existing empirical lane remains:

```text
M_A = change in pollinator-mediated benefit
G_A = change in antagonist-mediated cost
S_A = M_A - G_A
```

and, at the fitness-surface level,

```text
W(A) = M(A) - G(A) - C(A).
```

Cue overlap is one biological mechanism that couples the two functional channels to the same `A` coordinate:

- shared cues can make pollinator benefit and antagonist exposure move together;
- separable cue components can weaken that coupling;
- direct physiological or construction costs remain explicit when they matter.

An interior local floral compromise satisfies

```text
M'(A*) - G'(A*) - C'(A*) = 0
```

with negative local curvature of total fitness.

This is not the BITA two-trait estimand. SCH does not require a second trait `D`, `Delta_AD W`, or BITA's crossed consumer-intervention design.

## Current positive evidence

The current source-audited evidence supports several bounded Chapter 1 outcomes:

- **integrated compromise:** an observational fitness surface in which pollinator and seed-predator selection counteract one another and net selection tends to be stabilizing;
- **context-dependent polymorphism maintenance:** alternative floral displays can be maintained under varying/frequency-dependent selection;
- **population evolutionary change:** antagonist context can redirect population-level or experimental floral evolution;
- **partial cue decoupling:** bouquet component partitioning, conditional emission and temporal receiver separation provide mechanisms that reduce coupling without proving historical origin of a new trait module.

These outcomes are not pooled prevalence estimates and do not yet yield a cross-system estimate of `z*` or `L_S*`.

The current strongest historical bridge is *Ficus*, where resolved pollinator codes, non-pollinator use of receptive odour, temporal separation and phylogenetic structure occur within one radiation. The remaining same-code receiver intersection is still missing, so repeated historical shared-cue -> private-cue evolution remains `NOT_EVALUABLE`, not absent.

## Chapter 1 / Chapter 2 symmetry

The handoff is intentionally exact:

```text
Chapter 1 / SCH
best one-axis state       z*
shared conflict load      L_S*
             |
             v
Chapter 2 / BITA
recoverable loss          R
architecture gain         Delta_arch = R - K
quadratic corollary       R = s L_S*
```

The sister papers therefore separate two questions:

1. **optimization within a fixed shared architecture**;
2. **whether changing the architecture is worth its cost, and how the resulting multi-trait mechanism is identified**.

Strict non-equivalences remain:

```text
interior balance
!= proof that differentiation cannot evolve

one-axis directional change
!= trait differentiation

partial cue decoupling
!= historical origin of a new module

positive multi-trait interaction
!= historical splitting

route/case recurrence
!= prevalence.
```

## Manuscript state

Two manuscript layers are intentionally preserved while the reframe is validated:

- `manuscript/MANUSCRIPT_SHARED_CUE_FRAMEWORK.md` — detailed floral shared-cue evidence manuscript and source-adjudication spine;
- `manuscript/MANUSCRIPT_TRAIT_BALANCE_V1.md` — new general Chapter 1 integration candidate connecting shared-axis balance directly to BITA Chapter 2.

The existing shared-cue manuscript remains the evidence source of truth. The new trait-balance manuscript is the active programme-level integration candidate and must not silently promote evidence beyond the source-specific ceilings.

## Repository map

- `docs/SCH_BITA_SYMMETRY_CONTRACT_V1.md` — exact Chapter 1 -> Chapter 2 mathematical and editorial interface
- `manuscript/MANUSCRIPT_TRAIT_BALANCE_V1.md` — general Chapter 1 integration candidate
- `manuscript/MANUSCRIPT_SHARED_CUE_FRAMEWORK.md` — detailed floral evidence manuscript
- `empirical/one_trait_shared_cue/` — fail-closed coverage, evolutionary outcomes and *Ficus* receiver-gap products
- `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv` — evidence roles and claim ceilings
- `docs/CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md` — biological chapter bridge
- `docs/PUBLICATION_MATERIAL_LEDGER.md` — sections, figures, evidence roles and missing gates
- `scripts/build_one_trait_coverage_audit.py` — deterministic coverage audit builder
- `docs/MIGRATION_RECEIPT.md` — BITA-to-SCH ownership boundary and provenance

## Current status

**Scientific Chapter 1 framing: established. Empirical evidence spine: positive but heterogeneous. General trait-balance manuscript: integration candidate, not yet submission-ready.**

The next paperization gate is not another redefinition of the hypothesis. It is to synchronize the existing floral evidence into the general `z* / L_S*` Chapter 1 structure without pretending that studies lacking a full fitness surface estimated those quantities. In parallel, the historical *Ficus* lane remains a targeted same-code experiment rather than a broad search problem.
