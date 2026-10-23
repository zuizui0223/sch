# SCH Pareto normal-cone support-region theorem v1

## Purpose

Characterize the set of functional weights for which one particular compromise phenotype remains optimal.

The key result is geometric and strongly falsifiable: under a fixed attainable loss set, the weight region supporting a given phenotype is convex. Therefore the same compromise cannot be uniquely optimal at two endpoints of a straight weight path, lose optimality in the middle, and then reappear at the other endpoint.

## Setup

Let a feasible phenotype `z_a` have loss vector

\[
y_a=\boldsymbol\ell(z_a)\in\mathbb R^n.
\]

For positive/nonnegative weights `w`, `z_a` is a weighted-sum optimum when

\[
w^\top y_a\le w^\top\boldsymbol\ell(z)
\quad\text{for every feasible }z.
\]

Define its support region

\[
\mathcal W_a
=
\left\{w:
 w^\top(y_a-\boldsymbol\ell(z))\le0
 \text{ for all feasible }z
\right\}.
\]

## Theorem 1 — the support region is a convex cone

For every competitor `z`, the inequality

\[
w^\top(y_a-\boldsymbol\ell(z))\le0
\]

defines a closed half-space through the origin in weight space. The intersection of half-spaces is convex. Therefore

\[
\boxed{\mathcal W_a\text{ is a convex cone}.}
\]

If weights are normalized, e.g.

\[
\sum_iw_i=1,\qquad w_i\ge0,
\]

then the supported region inside the simplex is convex.

For a finite candidate set of loss vectors, it is a convex polytope/polyhedral cone.

## Corollary 1a — chord persistence of an optimal compromise

If `z_a` is optimal at both `w_0` and `w_1`, then for every

\[
w_t=(1-t)w_0+tw_1,
\qquad 0\le t\le1,
\]

we have

\[
\boxed{z_a\text{ remains optimal at }w_t.}
\]

Proof: both endpoints lie in the convex support region `W_a`, so the entire chord lies in `W_a`.

This permits ties with other phenotypes along the chord, but `z_a` cannot become strictly suboptimal at an interior point.

## Corollary 1b — no support re-entry along a straight weight path

Under the same fixed static loss geometry, a pattern

```text
z_a uniquely optimal
-> z_b uniquely optimal
-> z_a uniquely optimal
```

along a straight interpolation of functional weights is impossible.

Such re-entry requires at least one assumption to fail:

- the loss vectors themselves changed with the weight treatment;
- the feasible phenotype set changed;
- contexts/fitness semantics changed;
- the path in effective weight space was not actually straight;
- estimation uncertainty obscured ties.

This is a static SCH no-reentry result in **weight space**, distinct from BALANCE environmental no-reentry and PAYOFF history dynamics.

## Theorem 2 — pairwise switching boundaries are hyperplanes

For two candidate compromise states with loss vectors `y_a` and `y_b`, their weighted values tie when

\[
\boxed{w^\top(y_a-y_b)=0.}
\]

Thus the pairwise switching boundary is a hyperplane through the origin; inside a normalized weight simplex it becomes an affine codimension-one slice.

For two functions, writing the weight ratio as

\[
r=\frac{w_1}{w_2},
\]

a nondegenerate switch obeys

\[
\boxed{
r_c
=-\frac{y_{a2}-y_{b2}}{y_{a1}-y_{b1}}.}
\]

So an experimentally observed critical functional-weight ratio can identify a ratio of loss differences between the two supported states.

## Theorem 3 — support regions are normal cones of the lower loss hull

In loss space, a supported Pareto point minimizes a linear functional `w^T y`. The set of supporting weights is the normal cone to the lower convex hull of the attainable loss set at that point.

Hence weight-space geometry and Pareto geometry are dual:

```text
face / point on supported Pareto frontier
<->
normal cone of functional weights selecting it
```

A broad support cone means the compromise is robust to functional-demand changes. A narrow cone means small relative-weight changes switch the selected compromise.

## Corollary — kinks versus hysteresis

Crossing from one support cone to another can produce a sharp switch in the optimum even in a completely static system. Forward and reverse weight sweeps must nevertheless cross the same static boundary when the state/loss geometry is unchanged.

Therefore a switch is not hysteresis by itself. A reproducible forward/reverse boundary discrepancy requires an additional mechanism beyond this static normal-cone geometry.

## Empirical consequence

A multi-weight SCH experiment can preregister:

1. candidate compromise loss vectors or fitted states;
2. predicted pairwise hyperplanes in weight space;
3. held-out weight treatments inside predicted support regions;
4. a no-reentry audit along straight relative-weight paths.

This is stronger than asking only whether the optimum moves in the expected direction.

## Claim ceiling

The support-region theorem assumes a fixed attainable loss set and linear weighting of those losses. It does not apply if changing ecological demand changes the loss functions, trait accessibility, or fitness scale. Exact phenotype identity can also be too strict for continuously varying optima; in that case the theorem applies to a registered discrete state or local supported face rather than arbitrary measurement noise. PAYOFF invasion and evolutionary history remain separate.