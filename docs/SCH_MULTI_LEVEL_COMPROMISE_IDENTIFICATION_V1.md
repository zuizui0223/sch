# SCH multi-level compromise identification design v1

## Purpose

The binary SCH crossed design identifies local functional conflict. The Chapter-1 headline, however, is **compromise / balance on a multifunctional trait**. That stronger claim requires recovery of the response geometry across multiple values of the shared trait `z`.

This document defines the confirmatory design and separates theoretical pure-function optima from the state-specific optima that the reproductive experiment directly identifies.

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
P = pollinator pathway suppressed / present
G = antagonist pathway suppressed / present.
```

This produces a multi-level extension of the existing `A x G x P` design.

## Two layers of optimum notation

### Theoretical pure-function optima

The abstract framework may define

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z)
```

for isolated function-specific objectives. These are theory-level quantities.

### Experimentally identified state optima

The crossed reproductive experiment directly identifies state surfaces

```text
W00(z) = W(z,P0,G0)
W10(z) = W(z,P1,G0)
W01(z) = W(z,P0,G1)
W11(z) = W(z,P1,G1)
```

and therefore directly identifies

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

These are **state-specific reproductive optima**, not automatically pure function optima. Direct/background trait consequences remain in the state surfaces unless an independent assay identifies them.

Therefore:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The confirmatory experiment can prove causal compromise using `z_P*`, `z_G*`, `z_C*`, optimum shifts, and component gradients without claiming that pure `z_F1*` and `z_F2*` were point-identified.

## Primary response quantities

For the pollinator-antagonist case, the local contrasts generalize to functions of `z`:

```text
M(z; g) = W(z,g,P=1) - W(z,g,P=0)
G(z; p) = W(z,G=0,p) - W(z,G=1,p).
```

These are reproductive contributions / losses, not visitor counts.

The state surfaces and component contrasts should be reported together. If the functional channels interact, retain state-specific curves rather than forcing additive decomposition.

## Primary experimental optimum targets

The default empirical targets are:

```text
z_P* = pollinator-present / antagonist-suppressed state optimum
z_G* = pollinator-suppressed / antagonist-present state optimum
z_C* = combined P1G1 optimum.
```

The primary empirical conflict hypothesis is

```text
z_P* != z_G*.
```

An especially interpretable case is

```text
z_P* > z_C* > z_G*
```

or the reverse ordering. Strict between-ness is not mandatory because direct costs, baseline reproduction, and P x G interaction can move the combined optimum.

The stronger theoretical statement `z_F1* != z_F2*` requires either an additional identifying assay or a justified mapping from the state-specific optima to the pure functional objectives.

## Causal optimum-shift test

An intermediate phenotype is not sufficient evidence of compromise. The decisive intervention prediction is that changing the weight of one function shifts the total optimum toward the state favored when the competing function is suppressed.

Define

```text
z_C*        = optimum under P1G1
z_P*        = optimum under P1G0
z_G*        = optimum under P0G1.
```

A strong compromise mechanism predicts

```text
remove / weaken antagonism -> optimum shifts from z_C* toward z_P*
remove / weaken pollination -> optimum shifts from z_C* toward z_G*.
```

This is directly identified by the randomized intervention design and does not require identifying pure function optima.

## Gradient-balance test

At the combined optimum, estimate marginal gradients of the causal components.

A strong balance result requires opposite non-zero functional-component gradients, for example:

```text
g_P(z_C*) != 0
g_G(z_C*) != 0
sign(g_P(z_C*)) != sign(g_G(z_C*)).
```

The total `W11` gradient at its fitted interior vertex is zero by construction in a quadratic model and is therefore not an independent test.

If a direct-cost gradient is separately measured, include it explicitly. Do not attribute a residual to `C(z)` or a pure functional objective by subtraction.

## Primary estimands

Report at least:

```text
D_state = z_P* - z_G*

S_Goff = z_P* - z_C*
S_Poff = z_G* - z_C*

G_Pc = pollinator-component gradient at z_C*
G_Gc = antagonist-component gradient at z_C*.
```

If an independent assay additionally identifies pure function objectives, report separately:

```text
D_pure = z_F1* - z_F2*.
```

Do not substitute `D_state` for `D_pure` without an explicit identification argument.

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
C1  same z coordinate influences both focal functional routes;
C2  intervention-defined state optima differ: z_P* != z_G*;
C3  combined W11(z) has a supported interior optimum over the tested range;
C4  removing / weakening each functional demand shifts the optimum toward
    the corresponding single-demand state optimum;
C5  functional-component gradients around z_C* oppose one another.
```

If only C1-C2 are recovered, report **functional conflict**, not integrated compromise.

If C1-C4 are recovered but local component gradients are too uncertain, report **compromise geometry supported; gradient balance unresolved**.

Pure `z_F1*` and `z_F2*` are not part of the minimum empirical positive decision unless separately identified.

## Relationship to the binary 8-cell design

The binary design remains the most efficient Stage-1 pilot because it estimates intervention selectivity, channel magnitude, variance and clustering.

The intended sequence is

```text
binary crossed pilot
-> confirm selective functional manipulation
-> estimate mechanism-scale variance
-> choose informative z range
-> multi-level compromise experiment
-> estimate state-specific and combined optima.
```

The binary and multi-level designs therefore answer different layers of the same hypothesis rather than competing with each other.

## Relationship to the theoretical quadratic bridge

The quadratic bridge using `z_F1*` and `z_F2*` is an idealized theory benchmark. The empirical crossed experiment instead provides `z_P*`, `z_G*`, and `z_C*` by default.

The bridge can be used in two modes:

```text
strict empirical mode:
    use state-specific optimum displacement as the measured compromise geometry;

pure-function mode:
    use z_F1*, z_F2* only after independent direct/background pathways are identified.
```

This distinction prevents a clean theoretical symbol from being mistaken for a directly observed biological estimand.

## Relationship to BITA

The combined Chapter-1 optimum `z_C*` is the state that Chapter 2 attempts to release by adding a second trait coordinate.

The default cross-chapter reference is the directly identified function-1-facing state optimum `z_P*`, not a relabeled pure `z_F1*`.

BITA should ask whether the added coordinate lets the retained first trait move closer to `z_P*` while improving the intended function-2 outcome and total reproductive performance. If SCH separately identifies `z_F1*`, BITA may add that stricter theoretical reference as a second analysis lane.

This is the empirical bridge from balance to functional differentiation.
