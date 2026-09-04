# Shared-trait compromise framework v1

## Core biological question

SCH is Chapter 1 of a broader trait-architecture programme:

> **What happens when two fitness-relevant functions are forced to use the same phenotypic coordinate?**

```text
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/
```

A floral cue used by pollinators and antagonists is one empirical realization. The chapter-level claim is more general: multifunctionality can constrain evolution when functional demands pull the same trait in different directions.

## Theory-level shared-coordinate model

Let:

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z).
```

Pure function-specific optima are:

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z).
```

The integration problem exists when:

```text
z_F1* != z_F2*.
```

These are theory-level quantities. They are not automatically the optima directly identified by the reproductive crossed experiment.

## What the empirical experiment identifies

In the floral crossed design:

```text
W00(z) = P0G0
W10(z) = P1G0
W01(z) = P0G1
W11(z) = P1G1.
```

The directly identified state-specific optima are:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

Because direct/background trait effects can remain in all reproductive states:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

Pure function optima require an additional identifying assay or restriction.

## What “balance” means

Balance is not equality of raw benefits, visitor numbers, or function values. The relevant quantity is the marginal reproductive gradient.

A strong empirical compromise result requires:

```text
z_P* != z_G*
W11(z) has a supported interior z_C*
G off -> z_C* shifts toward z_P*
P off -> z_C* shifts toward z_G*
functional-component gradients near z_C* oppose one another.
```

Thus net selection near zero can reflect strong opposing demands rather than absence of selection.

## Empirical identification ladder

```text
L0  multifunctionality
    the same manipulated z affects both focal routes

L1  functional conflict
    selective manipulations show opposing local contributions

L2  state-specific compromise geometry
    multi-level z x P x G recovers z_P*, z_G*, z_C*

L3  mechanism-resolved balance
    functional-component gradients and interactions explain the balance

L4  evolutionary maintenance
    heritable variation / repeated selection / experimental evolution

L5  historical architecture
    ancestral integration and later differentiation reconstructed.
```

Evidence is not promoted up this ladder by interpretation alone.

## Why the binary design remains useful

The existing:

```text
A x antagonist x pollinator
```

8-cell experiment identifies L1 and part of L3 for one declared two-level trait contrast.

It cannot by itself prove an interior compromise because two trait values do not recover response-surface geometry.

The revised sequence is:

```text
Stage 1  two-level crossed intervention
         identify local opposing contributions

Stage 2  multi-level z x P x G
         recover z_P*, z_G*, z_C*

Stage 3  confirm causal compromise
         test opposite optimum shifts and component gradients

Stage 4  evolutionary extension.
```

At least three informative `z` levels are mathematically required; five or more are preferred.

## Pollinator-antagonist realization

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduction of antagonist-mediated loss
shared z   = floral attraction/display coordinate.
```

The local decomposition remains:

```text
M(z;g) = W(z,g,P=1) - W(z,g,P=0)
G(z;p) = W(z,G=0,p) - W(z,G=1,p).
```

The multi-level experiment then asks whether those routes generate distinct state optima and a stable combined optimum.

## What counts as a positive Chapter-1 result

The strongest contemporary result is the conjunction:

```text
1. the same z causally contributes to both focal routes;
2. z_P* and z_G* differ;
3. the combined W11 surface has an interior z_C*;
4. removing each demand shifts z_C* toward the corresponding state optimum;
5. functional-component gradients near z_C* oppose one another.
```

This identifies **multifunctional compromise** without requiring pure function optima to be point-identified.

## Optional pure-function lane

If direct/background consequences `C(z)` are independently measured or otherwise identified, SCH may additionally estimate:

```text
z_F1*
z_F2*.
```

This is a stronger theory-facing result and is reported separately from `z_P*` and `z_G*`.

## Bridge to Chapter 2

Default empirical bridge:

```text
SCH: z_P*, z_G*, z_C*
BITA: add x,y and test whether x* moves toward z_P*.
```

Optional stricter bridge:

```text
SCH independently identifies z_F1*
BITA additionally tests release toward z_F1*.
```

State-specific release and pure-function release are not silently conflated.

## Claim boundary

A contemporary two-trait architecture does not prove that an ancestral shared trait historically split into two descendants. SCH and BITA can establish contemporary functional differentiation experimentally. Historical modularization requires phylogenetic, developmental, or genetic evidence for an ancestral integrated state and a derived increase in functional independence.
