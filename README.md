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

The pollinator-antagonist shared-cue problem is the first floral implementation, not the definition of the chapter.

## Scientific target

Let one trait `z` contribute to two functions:

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

one phenotype cannot optimize both functions independently. The shared optimum

```text
zc* = argmax W_shared(z)
```

can therefore represent an integrated compromise.

Balance means **cancellation of opposing marginal gradients**, not equality of raw benefits:

```text
w1 dF1/dz + w2 dF2/dz - dC/dz = 0
```

while the component gradients remain non-zero and oppose one another.

## Analytic bridge to Chapter 2

Under the local quadratic benchmark

```text
L_shared(z)
  = a (z - z1*)^2
  + b (z - z2*)^2,
```

the shared optimum is

```text
zc* = (a z1* + b z2*) / (a + b)
```

and the unavoidable one-dimensional compromise penalty is

```text
L_compromise*
  = [a b / (a + b)] (z1* - z2*)^2.
```

This yields the causal Chapter-1 prediction:

```text
weaken function 2 -> zc* shifts toward z1*
weaken function 1 -> zc* shifts toward z2*.
```

It also yields the Chapter-2 opportunity: a second functional coordinate is potentially favored when the avoided compromise penalty exceeds the extra cost of differentiation.

The derivation is in `docs/SHARED_TO_DIFFERENTIATED_QUADRATIC_BRIDGE_V1.md`.

## Identification programme

SCH separates local conflict identification from compromise-surface identification.

```text
L0  multifunctionality
    the same z affects both functions

L1  functional conflict
    selective interventions recover opposing functional contributions
    on the same z contrast

L2  compromise geometry
    >=3 z levels recover function-specific response curves / optima
    and the total shared-trait optimum

L3  mechanism-resolved balance
    functional interventions identify how the gradients combine

L4  evolutionary maintenance
    heritable variation / repeated selection / experimental evolution

L5  historical architecture
    ancestral integration -> decoupling / specialization reconstructed.
```

The two-level crossed experiment is useful for L1 and part of L3. It does **not** by itself prove an interior compromise.

## Floral implementation

The current floral mapping is

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduced antagonist-mediated loss
shared z   = one floral attraction/display coordinate.
```

For one binary `A` contrast, SCH crosses

```text
A x antagonist x pollinator
```

in eight cells on one common reproductive outcome. Define

```text
d[g,p] = W[1,g,p] - W[0,g,p]
M_A(g) = d[g,1] - d[g,0]
G_A(p) = d[0,p] - d[1,p]
B_A    = d[0,0]
J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

A positive `M_A` and positive `G_A` on the same `A` contrast establish local functional conflict. To establish compromise / balance, extend the experiment across multiple informative `z` levels and recover `z1*`, `z2*`, and `zc*`.

## Real-world evidence role

The PRISMA programme and targeted primary-source audits remain as a **real-world evidence spine**. They do not define the SCH estimand.

They establish that:

- shared floral traits affect multiple functions / receiver classes in nature;
- opposing selection and stabilizing compromise occur in real systems;
- polymorphism and population trajectories respond to changing functional weights;
- component partitioning, conditional gating, and temporal separation provide partial routes toward decoupling;
- complete same-coordinate causal designs are rare.

Current bounded status:

```text
REAL_WORLD_MULTIFUNCTIONALITY_RECOVERED
CASE_LEVEL_COMPROMISE_RECOVERED
LOCAL_SCH_CHANNEL_IDENTIFICATION_NOT_YET_EXECUTED
MULTI_LEVEL_COMPROMISE_SURFACE_NOT_YET_EXECUTED
HISTORICAL_INTEGRATION_TO_MODULARIZATION_NOT_YET_IDENTIFIED.
```

## Current execution systems

*Nicotiana attenuata* remains the strongest same-coordinate floral reality anchor because benzylacetone affects pollinator-mediated reproduction and hawkmoth oviposition. Its main unresolved gate is combined pathway selectivity and the length of the antagonist-to-fitness path.

`Castilleja linariaefolia` remains a promising short-path candidate because pollinator and pre-dispersal seed-predator functions are more separable and antagonist effects map directly to seed fitness, although a clean manipulable shared coordinate still requires validation.

System choice is driven by identifiability, not source count.

## SCH -> BITA

```text
SCH
one shared z
-> opposing functional demands
-> causal compromise / balance

BITA
two partially distinct traits x,y
-> preferential functional loading
-> dimensional release
-> functional differentiation / modularization.
```

The strongest cross-chapter prediction is that adding a function-2 coordinate in BITA should release the function-1 trait toward the `z1*` optimum identified in SCH.

## Canonical reader path

- `manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md` — **canonical Chapter-1 manuscript**
- `docs/SHARED_TRAIT_COMPROMISE_FRAMEWORK_V1.md` — generalized theory and claim ladder
- `docs/SHARED_TO_DIFFERENTIATED_QUADRATIC_BRIDGE_V1.md` — analytic SCH -> BITA bridge
- `docs/SCH_MULTI_LEVEL_COMPROMISE_IDENTIFICATION_V1.md` — multi-level optimum/gradient design
- `docs/SCH_MECHANISM_IDENTIFICATION_DESIGN_V1.md` — two-level crossed mechanism design
- `manuscript/MANUSCRIPT_SHARED_CUE_FRAMEWORK.md` — floral shared-cue implementation and evidence spine
- `docs/CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md` — dissertation-level chapter bridge
- `docs/SCH_NICOTIANA_STAGE0_STAGE1_PILOT_V1.md` — first-choice floral execution contract
- `docs/SCH_SHORT_PATH_CANDIDATE_RANKING_V1.md` — alternative-system search
- `empirical/one_trait_shared_cue/` and `empirical/prisma/` — real-world evidence products.

## Immediate empirical programme

```text
Stage 0  validate one shared z coordinate and selective functional interventions
Stage 1  two-level crossed pilot: identify local opposing functional effects
Stage 2  extend to >=3 z levels: recover F1(z), F2(z), W(z), z1*, z2*, zc*
Stage 3  test causal optimum shifts by weakening each function
Stage 4  test evolutionary maintenance / movement
Stage 5  hand the identified compromise to BITA and test dimensional release.
```

SCH is therefore organized around **the ecology and evolution of compromise under multifunctional trait integration**. The literature demonstrates that the mechanism is biologically real; the decisive chapter result is a causal reconstruction of how multiple functional demands combine on one trait to generate balance.
