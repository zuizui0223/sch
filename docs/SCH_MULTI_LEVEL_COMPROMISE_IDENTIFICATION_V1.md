# SCH multi-level compromise identification design v1

## Purpose

The binary SCH crossed design identifies local functional conflict. The Chapter-1 headline, however, is **compromise / balance on a multifunctional trait**. That stronger claim requires recovery of the response geometry across multiple values of the shared trait `z`.

This document defines the confirmatory design.

## Core design

Manipulate a shared trait at `K` declared levels,

```text
z1, z2, ..., zK
```

and cross those levels with selective states of the two focal functions or functional environments.

Minimal curvature recovery requires `K >= 3`; `K >= 5` is preferred when feasible because the primary targets are optima and gradients rather than a single linear contrast.

For each `z`, measure the same reproductive outcome under the functional-intervention states required to separate the two pathways.

In the floral pollinator-antagonist implementation:

```text
z = attraction/display intensity
E1 = pollinator pathway suppressed / present
E2 = antagonist pathway suppressed / present.
```

This produces a multi-level extension of the existing `A x G x P` design.

## Primary curves

Estimate three biologically interpretable response curves on one commensurable outcome scale:

```text
F1(z)  function-1 contribution / function-1-only fitness component
F2(z)  function-2 contribution / function-2-only fitness component
W(z)   total fitness under the declared natural combined environment.
```

The exact contrast used to identify `F1` and `F2` depends on the intervention architecture. If the functional channels interact, retain state-specific curves rather than forcing additive decomposition.

For the pollinator-antagonist case, the two-level local contrasts generalize to functions of `z`:

```text
M(z; g) = W(z,g,P=1) - W(z,g,P=0)
G(z; p) = W(z,G=0,p) - W(z,G=1,p).
```

These are reproductive contributions / losses, not visitor counts.

## Optimum targets

Define the function-specific optima on the chosen scale:

```text
z1* = argmax function-1 objective
z2* = argmax function-2 objective
zc* = argmax W(z) under the combined environment.
```

The primary compromise hypothesis is

```text
z1* != z2*
```

with the combined optimum lying away from at least one function-specific optimum because of the other functional demand.

An especially interpretable case is

```text
z1* > zc* > z2*
```

or the reverse ordering, but strict between-ness is not required when direct costs or nonlinear interactions move the combined optimum.

## Causal optimum-shift test

An intermediate phenotype is not sufficient evidence of compromise. The decisive intervention prediction is that changing the weight of one function shifts the total optimum toward the other function's preferred value.

Let

```text
zc*(E2 off) = optimum when function 2 is suppressed
zc*(E1 off) = optimum when function 1 is suppressed.
```

A strong compromise mechanism predicts

```text
zc*(E2 off) moves toward z1*
zc*(E1 off) moves toward z2*.
```

This optimum-shift test is the direct causal signature of a phenotype held between competing functional demands.

## Gradient-balance test

At the combined optimum, estimate the function-specific marginal gradients.

A strong balance result requires

```text
g1(zc*) != 0
g2(zc*) != 0
sign(g1(zc*)) != sign(g2(zc*))
```

while the total gradient is compatible with zero:

```text
gW(zc*) approximately 0.
```

If a direct cost gradient is separately measured, include it explicitly in the balance equation. Do not attribute the entire residual to one function by subtraction.

## Primary estimands

Report at least:

```text
D_opt = z1* - z2*

S1 = zc*(E2 off) - zc*(combined)
S2 = zc*(E1 off) - zc*(combined)

G1c = g1(zc*)
G2c = g2(zc*)
GWc = gW(zc*).
```

The signs of `S1` and `S2` must be interpreted relative to the ordering of `z1*` and `z2*` rather than hard-coded globally.

The optima should be reported with uncertainty distributions / intervals, not as point-estimated peaks alone.

## Curve estimation

The confirmatory analysis should predeclare a limited family of response models appropriate to the data scale.

Acceptable approaches include:

- low-order polynomial response curves when biological shape is simple and the range is narrow;
- monotonic-plus-quadratic models when an interior optimum is expected;
- penalized smooths / GAMs when enough `z` levels and replication exist;
- hierarchical response-surface models when populations / blocks are a substantive level.

Model choice must not be selected solely to manufacture an interior optimum. Compare the predeclared curve family using predictive adequacy and retain shape uncertainty.

## Experimental unit and uncertainty

Randomize `z` at the highest biologically feasible level while preserving:

```text
plant
block / site
night / day
population
flower position
repeated flowers per plant
functional intervention unit.
```

Optimum and gradient uncertainty should be propagated through the fitted hierarchical model or by cluster-respecting bootstrap. Treating flowers from one plant as exchangeable independent replicates is not acceptable.

## Minimum positive Chapter-1 decision

A confirmatory integrated-compromise result requires all of:

```text
C1  same z coordinate influences both functions;
C2  function-specific preferred directions / optima differ;
C3  combined W(z) has a supported optimum over the tested range;
C4  removing / weakening each functional demand shifts the optimum or
    selection gradient toward the other function's preferred state;
C5  function-specific gradients around the combined optimum oppose one another.
```

If only C1-C2 are recovered, report **functional conflict**, not integrated compromise.

If C1-C4 are recovered but the local gradients are too uncertain, report **compromise geometry supported; gradient balance unresolved**.

## Relationship to the binary 8-cell design

The binary design remains the most efficient Stage-1 pilot because it estimates intervention selectivity, channel magnitude, variance and clustering.

The intended sequence is

```text
binary crossed pilot
-> confirm selective functional manipulation
-> estimate mechanism-scale variance
-> choose informative z range
-> multi-level compromise experiment
-> estimate function-specific and combined optima.
```

The binary and multi-level designs therefore answer different layers of the same hypothesis rather than competing with each other.

## Relationship to BITA

The combined Chapter-1 optimum `zc*` is the state that Chapter 2 attempts to release by adding a second trait coordinate.

BITA should ask whether the added coordinate lets the first trait move closer to its function-specific optimum without paying the full cost imposed by the second function.

That makes the most direct cross-chapter prediction:

```text
shared architecture:
    z optimum = compromise zc*

differentiated architecture:
    x optimum shifts toward function-1 optimum
    while y carries more of function-2 demand.
```

This is the empirical bridge from balance to functional differentiation.
