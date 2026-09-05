# Chapter 1 to Chapter 2 positioning v2 — balance to differentiation

## Programme-level question

How are conflicting functional demands resolved when they are forced onto one trait coordinate, and when is it advantageous to relax that architectural constraint by separating the functions across partly independent traits?

This document supersedes the old programme-level interpretation in `CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md`. The older file remains useful for the detailed floral `A × D` outcome hierarchy and *Nicotiana* evidence ceiling.

## Chapter 1 — SCH: optimize the shared architecture

SCH holds architecture fixed. Two functions remain coupled to one trait coordinate `z`:

```text
L_S(z) = l1(z) + l2(z)
z*     = argmin_z L_S(z)
L_S*   = L_S(z*)
```

Chapter 1 asks:

1. where is the best shared phenotype `z*`?
2. how does ecological context shift it?
3. how much conflict remains after the best one-axis solution is chosen?
4. which one-axis evolutionary outcomes are actually supported by evidence?

In the matched quadratic baseline,

```text
L_S(z) = w1(z-theta1)^2 + w2(z-theta2)^2

z* = (w1 theta1 + w2 theta2)/(w1+w2)

L_S* = [w1w2/(w1+w2)](theta1-theta2)^2.
```

The programme shorthand **BALANCE** means optimization while functions remain on one shared axis. An interior compromise is the canonical case, but one-axis directional movement, polymorphism or context-dependent shifts remain distinct possible outcomes.

### Floral SCH case

For the current empirical system,

```text
z = A
W(A) = M(A) - G(A) - C(A)
```

where `M` is pollinator-mediated benefit, `G` antagonist-mediated loss and `C` any direct cost retained on the same outcome scale.

A local interior compromise requires

```text
M'(A*) - G'(A*) - C'(A*) = 0
```

with negative local fitness curvature.

Cue sharing is the floral mechanism that makes the same coordinate affect both audiences. It is not the general definition of Chapter 1.

Current evidence supports bounded examples of stabilizing compromise, context-dependent maintenance, population evolutionary change and partial cue decoupling. It does not provide one cross-system estimate of `z*` or `L_S*`, and it does not establish repeated historical shared-cue -> private-cue transitions.

## Chapter 2 — BITA: relax the shared-axis constraint

BITA begins from the Chapter 1 shared solution rather than from a floral defence label.

Allow a larger phenotype space with partly independent axes. Let `R` be the amount of Chapter 1 conflict load recoverable before paying an additional fixed architecture cost `K`.

General Chapter 2 result:

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0  <=>  K < R.
```

For the matched quadratic model,

```text
R = s L_S*
Delta_arch = s L_S* - K,
```

where `s` is the decoupling fraction retained after residual coupling.

Thus Chapter 2 asks:

1. how much of the Chapter 1 conflict load can a larger architecture recover?
2. how incomplete is the separation?
3. does the recovery exceed the cost of the extra architecture?
4. once multiple axes exist, which causal pathway gives the architecture its fitness effect?

### Floral BITA case

The existing `A × D` attraction/defence system is a detailed worked case after multiple axes exist.

```text
Delta_AD W = W11 - W10 - W01 + W00
```

can determine an outcome-level cross-trait interaction but not uniquely allocate its ecological mechanism. The retained identified-set, partial-identification and crossed consumer-intervention framework therefore answers the second-stage mechanism question.

The floral case must not redefine Chapter 2 as “adding defence”. A defence axis is one empirical realization of the more general operation “relax the one-axis architectural constraint”.

## Exact cross-chapter handoff

```text
CHAPTER 1 / SCH
one shared coordinate z
        |
        +--> z*    best shared phenotype
        +--> L_S*  residual shared conflict load
                     |
                     v
CHAPTER 2 / BITA
larger phenotype space x,y
        |
        +--> R     amount of L_S* recovered
        +--> K     extra architecture cost
        +--> Delta_arch = R-K
                     |
                     v
              mechanism identification
```

This makes the sister relationship substantive rather than rhetorical: the output of Chapter 1 is the baseline input of Chapter 2.

## Symmetric claim boundaries

### SCH cannot infer

```text
interior compromise
=> differentiation cannot evolve

one-axis directional change
=> new trait module

partial cue decoupling
=> historical origin of a private cue
```

### BITA cannot infer

```text
positive architecture gain
=> historical transition occurred

structural separation
=> functional independence

positive A x D interaction
=> historical trait splitting
```

### Neither chapter can infer prevalence from case recurrence

Evidence recurrence shows that relevant states or mechanisms occur. It does not estimate how common balance, differentiation or any particular architecture is in nature.

## Why the two chapters are now symmetric

| Chapter dimension | SCH / Chapter 1 | BITA / Chapter 2 |
|---|---|---|
| Fixed object | one shared architecture | shared architecture as baseline |
| What is optimized? | position on the shared axis | architecture with additional axes |
| Core output | `z*`, `L_S*` | `R`, `Delta_arch` |
| Main cost | residual conflict from coupling functions | extra architecture cost `K` + residual coupling |
| Core empirical question | where/how the compromise is maintained or redirected | whether partial decoupling pays and how it works |
| Floral realization | shared cue affecting pollinator and antagonist channels | attraction × defence plus consumer interventions |
| Historical ceiling | shared -> private transition not established | one-axis -> multi-axis origin not established |

## Editorial sequence

The papers should be introduced as one programme:

```text
Chapter 1 / SCH
How do conflicting functions balance while they remain coupled on one trait?

Chapter 2 / BITA
When does relaxing that shared-axis constraint by trait differentiation pay,
and how can the mechanism of the resulting architecture be identified?
```

The papers should not be introduced as:

```text
Chapter 1 = pollination versus antagonism
Chapter 2 = pollination versus defence.
```

Those are empirical implementations, not the general chapter definitions.

## Current empirical asymmetry that remains legitimate

Conceptual symmetry does not mean identical evidence depth.

SCH currently has stronger evidence for heterogeneous evolutionary outcomes of one-trait conflict, including a direct observational stabilizing-compromise case and population evolutionary responses, but weaker direct parameterization of a common `L_S*`.

BITA currently has a cleaner general architecture formula and a mature mechanism-identification framework after multiple axes exist, but no direct historical demonstration that a measured Chapter 1 conflict caused the origin of a second axis.

This is a productive asymmetry in evidence, not a flaw in the chapter logic. The paper pair should state it rather than force the two empirical corpora into artificial equivalence.
