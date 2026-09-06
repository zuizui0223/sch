# SCH weight-perturbation design capacity theorem v1

## Purpose

Translate the low-rank weight-curvature theorem into a prospective requirement on the number and geometry of functional-weight manipulations.

The exact theory gives

\[
M=-\nabla_w^2L^*=G^\top H^{-1}G,
\qquad
\operatorname{rank}(M)\le d,
\]

where `d` is the dimension of the shared phenotype coordinate.

An experiment observes curvature only along the weight-perturbation directions it actually manipulates. This theorem states what dimensional information such a design can and cannot recover.

## Setup

Let `n` be the number of functional weights. Let

\[
V=[v_1\;\cdots\;v_q]\in\mathbb R^{n\times q}
\]

collect `q` linearly independent experimental weight-perturbation directions.

The curvature visible to the experiment is the projected matrix

\[
C=V^\top M V.
\]

When total weight is fixed, the columns of `V` lie in the relative-weight tangent space, which has dimension at most `n-1`.

## Theorem 1 — projected curvature rank bound

Matrix-rank inequalities give

\[
\boxed{
\operatorname{rank}(C)
\le
\min\{\operatorname{rank}(M),\operatorname{rank}(V)\}
\le
\min\{d,q\}.
}
\]

Thus an experiment with only `q` independent weight directions cannot reveal more than `q` active shared-coordinate curvature dimensions, even if the true phenotype has higher dimension.

## Corollary 1a — certified lower dimension from the experimental subspace

If the projected curvature has rank `r`, then

\[
\boxed{d\ge r.}
\]

With estimation error, the spectral certificate should be applied to `C` rather than literal rank, yielding a conservative lower bound on dimension visible inside the manipulated weight subspace.

## Theorem 2 — necessary design capacity for full local dimension recovery

To have any possibility of recovering `d` independent curvature modes, both conditions are necessary:

\[
\boxed{q\ge d}
\]

and

\[
\boxed{n-1\ge d.}
\]

Therefore

\[
\boxed{n\ge d+1}
\]

functional weights are necessary for a fixed-total relative-weight design to have capacity to identify `d` shared-coordinate curvature dimensions.

This is a design-capacity statement, not a sufficiency statement. The functional gradients must also span the phenotype directions being claimed.

## Theorem 3 — full-rank projected curvature criterion

If

\[
\operatorname{rank}(GV)=d,
\]

then

\[
C=V^\top G^\top H^{-1}GV
\]

has rank `d` because `H^{-1}` is positive definite on phenotype space.

Hence

\[
\boxed{
\operatorname{rank}(GV)=d
\Longrightarrow
\operatorname{rank}(C)=d.
}
\]

This gives the local sufficiency condition: the manipulated weight directions must move the weighted combination of functional gradients through all registered shared-coordinate directions.

## Corollary 3a — redundant weight perturbations

If a new perturbation direction lies in the span of existing directions after mapping through `G`, it adds no new phenotype-curvature dimension even if it is algebraically independent in raw weight space.

Therefore biological design should maximize **functional-gradient diversity**, not merely the number of nominal treatment contrasts.

## Relation to common scaling

The common-scaling direction `w` satisfies

\[
Gw=0
\]

at the optimum and is phenotype-flat. Including common scaling as one of the nominal manipulations therefore does not increase the rank capacity for shared-coordinate identification.

## Empirical consequence

Before a multi-function SCH generality experiment, report:

1. number of independently manipulable functions `n`;
2. number of independent relative-weight directions `q`;
3. registered shared-coordinate dimension `d` to be tested;
4. whether `q>=d` and `n>=d+1`;
5. after pilot data, whether estimated functional-gradient responses suggest `GV` spans the proposed dimension.

A design with `q<d` should be labeled

```text
INSUFFICIENT_WEIGHT_DIRECTION_CAPACITY_FOR_DIMENSION_d
```

rather than treating a low empirical rank as support for a low-dimensional phenotype.

## Claim ceiling

The theorem concerns local identifiability of the SCH curvature signature. It assumes the regular common-coordinate model and fixed loss families under weight perturbation. Having enough design capacity does not guarantee statistical power or gradient spanning, and failure to recover dimension `d` under a low-capacity design cannot falsify `d`. The result does not concern historical modularity or PAYOFF dynamics.
