# Shared-trait compromise framework v1

## Core biological question

SCH is Chapter 1 of a broader trait-architecture programme. Its general question is not restricted to pollination versus antagonism:

> **What happens when two fitness-relevant functions are forced to use the same phenotypic coordinate?**

The canonical architecture is

```text
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/
```

A floral cue used by pollinators and antagonists is one empirical realization of this architecture. The chapter-level claim is more general: multifunctionality can constrain evolution when the functions favor different values of the same trait.

## Shared-coordinate model

Let one trait `z` contribute to two fitness-relevant functional components,

```text
F1(z)
F2(z)
```

and let any direct construction, physiological or allocation cost be `C(z)`. On a declared fitness scale,

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z).
```

The weights `w1` and `w2` represent the reproductive consequences of the two functions on the chosen scale; they are not assumed equal.

Define the function-specific optima

```text
z1* = argmax F1(z)
z2* = argmax F2(z)
```

or, when each function contains its own cost term, the corresponding function-specific fitness optima.

The integration problem exists when

```text
z1* != z2*.
```

A single trait cannot then sit at both optima simultaneously. The realized shared-trait optimum is

```text
zc* = argmax W_shared(z).
```

When `zc*` lies away from both function-specific optima, the phenotype is an **integrated compromise**.

## What “balance” means

Balance is not equality of raw benefits, visitor numbers or function values. The relevant quantity is the marginal fitness gradient.

At an interior shared optimum,

```text
w1 dF1/dz + w2 dF2/dz - dC/dz = 0.
```

A strong compromise result requires that the underlying functional gradients are not themselves both zero. In the simplest two-function case,

```text
sign(dF1/dz) != sign(dF2/dz)
```

near the shared optimum, with both gradients meaningfully non-zero before they cancel on the total-fitness scale.

Thus

```text
net selection approximately zero
```

does **not** mean “nothing is selecting on the trait.” It can mean that strong opposing functional demands are balanced on the same phenotype.

## Empirical identification ladder

SCH now separates five contemporary levels before any historical claim.

```text
L0  multifunctionality
    the same manipulated z affects both functions

L1  functional conflict
    selective functional manipulations show opposing marginal effects
    on the reproductive value of the same z contrast

L2  compromise geometry
    >=3 declared z levels or a continuous manipulation recover
    distinct function-specific response curves / optima and a shared optimum

L3  mechanism-resolved balance
    function-specific interventions across z identify how the opposing
    gradients combine and whether their interaction is state-dependent

L4  evolutionary maintenance
    heritable variation, repeated selection or experimental evolution
    shows persistence / movement around the compromise geometry

L5  historical architecture
    ancestral integration and later decoupling or specialization are
    reconstructed rather than inferred from extant correlations alone
```

Evidence must not be promoted up this ladder by interpretation alone.

## Why the current binary SCH design remains useful

The existing

```text
z x function-1 environment x function-2 environment
```

binary design is the correct local identification design for L1 and part of L3. In the pollinator-antagonist realization this is the registered

```text
A x antagonist x pollinator
```

8-cell experiment.

For one two-level `z` contrast, it can identify whether function 1 makes the contrast more beneficial while function 2 makes it less beneficial. It cannot by itself prove an interior evolutionary compromise because two `z` values do not reconstruct the shape of the fitness surface.

Accordingly the revised empirical programme is:

```text
Stage 1  two-level crossed intervention
         identify local opposing functional contributions

Stage 2  multi-level z experiment
         recover F1(z), F2(z) and W(z)
         estimate z1*, z2* and zc*

Stage 3  confirm compromise / balance
         test opposing gradients around zc* with compatible uncertainty

Stage 4  evolutionary extension
         test maintenance, population shifts or experimental evolution
```

At least three informative `z` levels are required for a minimal curvature test; more levels are preferable when the trait can be manipulated continuously.

## Pollinator-antagonist realization

The existing SCH floral programme becomes a high-information realization of the general framework.

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduction of antagonist-mediated loss
shared z   = one floral attraction/display coordinate
```

For the current notation,

```text
W(z) = M(z) - G(z) - C(z).
```

If stronger floral display increases `M(z)` but also increases `G(z)`, the two functional demands can favor different values of the same `z`. The 8-cell design identifies the opposing local contributions; a multi-level `z` design is needed to establish the compromise surface itself.

The literature layer remains valuable because it shows that all parts of this geometry occur in nature: same-coordinate receiver use, opposing selection, stabilizing compromise, polymorphism, population change and partial cue decoupling. It is real-world grounding, not the chapter's final identifying experiment.

## What counts as a positive Chapter-1 result

The strongest contemporary Chapter-1 result is not merely

```text
function 1 responds to z
function 2 responds to z.
```

It is the conjunction

```text
1. the same z coordinate causally contributes to both functions;
2. the functions favor different movement along z;
3. the total fitness surface has a realized optimum that reflects their
   opposing marginal contributions;
4. selective intervention shows that removing one function shifts the
   optimum or selection gradient in the predicted direction.
```

This identifies **multifunctional compromise**.

## Bridge to Chapter 2

Chapter 1 establishes the constraint created by functional integration. Chapter 2 asks whether that constraint can be relaxed by increasing trait dimensionality:

```text
Chapter 1 / SCH
function 1 ---\
               >--- z ---> compromise
function 2 ---/

Chapter 2 / BITA
function 1 ---> x
function 2 ---> y
               |
               +--> functional differentiation / modularization
```

The chapter transition is therefore

> **from compromise under one shared coordinate to functional differentiation across partially independent coordinates.**

The existing attraction-defence implementation is one special case: attraction `A` can serve primarily the pollination function while a distinct defence-associated trait `D` can serve antagonist reduction.

## Claim boundary

A contemporary two-trait architecture does not by itself prove that an ancestral shared trait historically split into two descendant traits. SCH and BITA can establish **functional differentiation as an escape architecture** with experiments. The stronger term **historical modularization** requires phylogenetic, developmental or genetic evidence for an ancestral integrated state and a derived increase in functional independence.
