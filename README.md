# Shared Trait Compromise / SCH

SCH is Chapter 1 of a trait-architecture programme paired with [BITA](https://github.com/zuizui0223/bita).

```text
Chapter 1 / SCH
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/

Chapter 2 / BITA
shared compromise
      ↓
function 1 ---> trait x
function 2 ---> trait y
      ↓
functional differentiation / modularization
```

The general SCH question is:

> **What happens when two fitness-relevant functions are forced to use the same phenotypic coordinate?**

The pollinator-antagonist shared-cue problem remains the primary floral implementation, but it is now treated as one realization of a more general multifunctionality problem rather than the definition of the chapter.

## Scientific target

Let one trait `z` contribute to two functional components:

```text
F1(z)
F2(z)
```

with total fitness

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z).
```

If the function-specific optima differ,

```text
z1* != z2*,
```

a single phenotype cannot optimize both functions independently. The shared-trait optimum

```text
zc* = argmax W_shared(z)
```

can therefore represent an integrated compromise.

The strongest balance claim is about **opposing marginal gradients**, not equal raw benefits. Near an interior compromise,

```text
w1 dF1/dz + w2 dF2/dz - dC/dz = 0
```

while the function-specific gradients can remain non-zero and oppose one another. Net selection near zero can therefore mask strong functional conflict.

The generalized framework is frozen in `docs/SHARED_TRAIT_COMPROMISE_FRAMEWORK_V1.md`.

## Identification programme

SCH now separates local conflict identification from compromise-surface identification.

```text
L0  multifunctionality
    the same z affects both functions

L1  functional conflict
    selective interventions recover opposing functional contributions
    on the same z contrast

L2  compromise geometry
    >=3 z levels recover distinct functional response curves / optima
    and the total shared-trait optimum

L3  mechanism-resolved balance
    crossed functional interventions identify how the gradients combine

L4  evolutionary maintenance
    heritable variation / repeated selection / experimental evolution

L5  historical architecture
    ancestral integration -> decoupling / specialization reconstructed
```

The current two-level crossed design remains valuable for L1 and part of L3. It does **not** by itself prove an interior compromise; that requires a multi-level or continuous `z` experiment.

## Pollinator-antagonist realization

The current floral implementation maps the general architecture as

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduced antagonist-mediated loss
shared z   = one floral attraction/display coordinate
```

so that

```text
W(z) = M(z) - G(z) - C(z).
```

For one binary attraction/display contrast, the registered experiment crosses

```text
A x antagonist x pollinator
```

in an 8-cell selective-intervention design on one common reproductive outcome. Write

```text
d[g,p] = W[1,g,p] - W[0,g,p].
```

Then identify

```text
M_A(g) = d[g,1] - d[g,0]
         pollinator-mediated contribution

G_A(p) = d[0,p] - d[1,p]
         antagonist-mediated loss

B_A    = d[0,0]
         consumer-independent remainder

J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0]
         channel-dependence diagnostic.
```

A positive `M_A` and positive `G_A` on the same `A` contrast establish local functional conflict. To establish **compromise / balance**, the next extension is to repeat the crossed functional design over at least three informative `A`/`z` levels and recover the pollinator, antagonist and total-fitness response curves.

## What the literature evidence does

The PRISMA programme, targeted primary-source audits and evolutionary-outcome audit remain in SCH as a **real-world evidence spine**. Their role is secondary to the identifying experiment.

They provide four kinds of grounding:

- **mechanism reality:** shared floral traits affect multiple functions / receiver classes in nature;
- **compromise reality:** opposing selection, stabilizing compromise, polymorphism and population shifts are documented;
- **design-gap evidence:** both functions and a common fitness outcome are rarely manipulated on the same trait coordinate;
- **historical extension:** systems such as *Ficus* identify candidate routes from integrated to more separable architectures.

The frozen systematic cohort contains 868 records. Through V20, 405 have title/abstract decisions, 117 primary studies are included, and two studies satisfy the strict linked measurement architecture. Those counts are not the SCH estimand and are not prevalence estimates.

Current bounded status:

```text
REAL_WORLD_MULTIFUNCTIONALITY_RECOVERED
REAL_WORLD_COMPROMISE_AND_DECOUPLING_OUTCOMES_RECOVERED
LOCAL_SCH_CHANNEL_IDENTIFICATION_NOT_YET_EXECUTED
MULTI_LEVEL_COMPROMISE_SURFACE_NOT_YET_EXECUTED
HISTORICAL_INTEGRATION_TO_MODULARIZATION_NOT_YET_IDENTIFIED
```

## Current execution systems

*Nicotiana attenuata* remains the strongest same-coordinate floral system for the pollinator-antagonist realization because benzylacetone (BA) affects pollinator-mediated reproduction and hawkmoth oviposition on the same programme-level axis. Existing pollen-loading and egg-removal methods also provide intervention components.

Its current gate is **combined pathway selectivity**: the pollination and antagonist pathways must be perturbed without moving the BA coordinate or contaminating the other functional channel. The relevant contracts are:

- `docs/SCH_NICOTIANA_STAGE0_STAGE1_PILOT_V1.md`
- `docs/SCH_NICOTIANA_STAGE0_PRIMARY_SOURCE_RECOVERY_V1.md`
- `docs/SCH_NICOTIANA_COMBINED_SELECTIVITY_PILOT_V1.md`

A parallel short-path search is retained because the best system for L0 same-coordinate reality need not be the easiest system for L2 compromise geometry. Systems with distinct pollinator and seed-predator guilds and a short antagonist-to-seed-loss path may be superior for the full compromise experiment.

## SCH -> BITA

The sister projects now answer one general evolutionary sequence.

```text
Chapter 1 — SCH
one trait dimension z
multiple functional demands
-> identify conflict and integrated compromise

Chapter 2 — BITA
increase trait dimensionality to x and y
-> test whether functions become more independently tunable
-> identify functional differentiation / modularization
```

In the current floral special case:

```text
SCH:   shared attraction/display coordinate under pollination and antagonism
BITA:  attraction trait A + antagonist-reducing trait D
```

BITA therefore no longer means merely “add defence.” It is the operational two-trait test of whether a second coordinate can release a compromise identified in Chapter 1.

## Repository map

- `docs/SHARED_TRAIT_COMPROMISE_FRAMEWORK_V1.md` — generalized Chapter-1 theory and evidence ladder
- `docs/SCH_MECHANISM_IDENTIFICATION_DESIGN_V1.md` — two-level crossed mechanism-identification contract
- `docs/CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md` — dissertation-level bridge to functional differentiation
- `docs/SCH_NICOTIANA_STAGE0_STAGE1_PILOT_V1.md` — first-choice floral execution contract
- `docs/SCH_NICOTIANA_STAGE0_PRIMARY_SOURCE_RECOVERY_V1.md` — primary-source recovery of Nicotiana Stage-0 gates
- `docs/SCH_NICOTIANA_COMBINED_SELECTIVITY_PILOT_V1.md` — combined pathway go/no-go pilot
- `docs/SCH_SHORT_PATH_CANDIDATE_RANKING_V1.md` — alternative-system search for short function-to-fitness paths
- `empirical/one_trait_shared_cue/` — source adjudications, evolutionary outcomes and historical extensions
- `empirical/prisma/frozen_v2/` — immutable systematic denominator
- `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv` — evidence roles and claim ceilings

## Immediate empirical programme

```text
Stage 0  validate one shared z coordinate and selective functional interventions
Stage 1  two-level crossed pilot: identify local opposing functional effects
Stage 2  extend to >=3 z levels: recover F1(z), F2(z), W(z), z1*, z2*, zc*
Stage 3  confirm balance by testing opposing gradients around zc*
Stage 4  test evolutionary maintenance / movement
Stage 5  hand the identified compromise to BITA and test dimensional release
```

SCH is therefore now organized around **the ecology and evolution of compromise under multifunctional trait integration**. The pollinator-antagonist literature demonstrates that the mechanism is real; the decisive chapter result is an experiment showing how two functional demands combine on one trait to generate a compromise surface.