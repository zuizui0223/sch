# SCH finite weight reoptimization-relief theorem v1

## Purpose

Turn concavity of optimized shared-axis conflict in functional-weight space into an exact finite-change decomposition.

The question is not only how the optimum moves when functional weights change, but how much conflict is **relieved by re-optimizing the shared phenotype** after a finite weight shift.

## Setup

Let

\[
L^*(w)=\min_z J(z;w),
\qquad
J(z;w)=\sum_i w_i\ell_i(z),
\]

on a regular convex weight region. Let

\[
w_0\to w_1=w_0+\Delta w
\]

be a registered finite functional-weight change, and write

\[
z_0=z^*(w_0),
\qquad
L_0=L^*(w_0),
\qquad
L_1=L^*(w_1).
\]

Define the baseline residual-loss vector

\[
r_0=(\ell_1(z_0),\ldots,\ell_n(z_0))
=\nabla_w L^*(w_0)
\]

by the envelope theorem.

## Definition — no-reoptimization counterfactual

If the functional weights changed from `w_0` to `w_1` but the phenotype were held at the old optimum `z_0`, the new load would be

\[
J(z_0;w_1)
=
L_0+r_0^\top\Delta w.
\]

Define the finite **reoptimization relief**

\[
\boxed{
\mathcal R_w(w_0\to w_1)
=
J(z_0;w_1)-L_1
=
L_0+r_0^\top\Delta w-L_1.
}
\]

This is measured in the same fitness-loss units as `L*`.

## Theorem 1 — reoptimization relief is nonnegative

Because `L_1` is the minimum of `J(z;w_1)`,

\[
L_1\le J(z_0;w_1).
\]

Therefore

\[
\boxed{\mathcal R_w\ge0.}
\]

Equivalently, because `L*` is concave in `w`,

\[
L^*(w_1)
\le
L^*(w_0)+\nabla L^*(w_0)^\top(w_1-w_0).
\]

Thus `R_w` is exactly the tangent gap of the concave optimized-load value function.

## Theorem 2 — exact curvature integral

Let

\[
w_t=w_0+t\Delta w,
\qquad t\in[0,1],
\]

and define the positive-semidefinite weight-curvature matrix

\[
C(w)=-\nabla_w^2L^*(w)\succeq0.
\]

For

\[
g(t)=L^*(w_t),
\]

we have

\[
-g''(t)=\Delta w^\top C(w_t)\Delta w.
\]

Taylor's theorem with integral remainder gives

\[
\boxed{
\mathcal R_w
=
\int_0^1(1-t)
\,\Delta w^\top C(w_t)\Delta w\,dt.
}
\]

So finite reoptimization relief is accumulated weight-space conflict curvature along the actual weight-change chord.

## Corollary 2a — curvature bounds

If on the whole chord

\[
0\le\alpha
\le
\Delta w^\top C(w_t)\Delta w
\le\beta,
\]

then

\[
\boxed{
\frac{\alpha}{2}
\le
\mathcal R_w
\le
\frac{\beta}{2}.
}
\]

More generally, if

\[
\alpha Q\preceq C(w_t)\preceq\beta Q
\]

for a registered positive-semidefinite weight metric `Q`, then

\[
\boxed{
\frac{\alpha}{2}\Delta w^\top Q\Delta w
\le
\mathcal R_w
\le
\frac{\beta}{2}\Delta w^\top Q\Delta w.
}
\]

## Corollary 2b — zero-relief criterion

If

\[
C(w_t)\Delta w=0
\]

for all `t` on the chord, then

\[
\boxed{\mathcal R_w=0.}
\]

The old optimum then loses no load relative to the newly optimized phenotype along this weight change.

For a common scaling of all weights, the phenotype remains fixed, so after accounting for the trivial scaling of total load there is no phenotype-reoptimization relief.

## Bregman form

Because `-L*` is convex,

\[
\boxed{
\mathcal R_w
=D_{-L^*}(w_1,w_0)
}
\]

is the Bregman divergence of the convex function `-L*` from `w_0` to `w_1`.

This makes the asymmetry explicit:

\[
\mathcal R_w(w_0\to w_1)
\neq
\mathcal R_w(w_1\to w_0)
\]

in general, because the no-reoptimization counterfactual is anchored at the starting optimum.

## Relation to the chord-bulge theorem

The existing weight-chord theorem compares an interior optimized load with the linear interpolation of **two optimized endpoints**.

The present theorem compares the final optimized load with a different counterfactual:

```text
same final functional weights
but phenotype frozen at the initial optimum
```

Therefore the two quantities answer different questions:

- chord bulge: how concave is the optimized value function between two endpoints?
- reoptimization relief: how much did phenotype movement rescue after this finite weight change?

## Empirical consequence

A causal weight-shift experiment can estimate `R_w` without reconstructing the full Hessian if it has:

1. baseline component-loss surfaces, giving `z_0` and residual losses `r_0`;
2. a registered finite weight change `Delta w`;
3. the re-estimated optimized conflict load `L_1` after the weight change.

Then

\[
\widehat{\mathcal R}_w
=
\widehat L_0+
\widehat r_0^\top\Delta w-
\widehat L_1.
\]

A significantly negative value after uncertainty propagation rejects at least one of the registered assumptions: common loss families, correct functional-weight mapping, same phenotype-accessibility set, or successful optimization/surface recovery.

## Claim ceiling

The theorem assumes the same loss families and feasible shared-phenotype space before and after the weight intervention. If changing ecological demand also changes the functions themselves, accessibility, or fitness semantics, `R_w` is not a pure reoptimization quantity. The result is static SCH geometry and does not concern PAYOFF invasion dynamics.
