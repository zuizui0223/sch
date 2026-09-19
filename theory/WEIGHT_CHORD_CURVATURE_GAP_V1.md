# SCH weight-chord curvature-gap theorem v1

## Purpose

Convert concavity of optimized conflict load in functional-weight space into a quantitative three-point prediction. The theorem uses two endpoint weight regimes plus one interior regime to estimate or falsify the amount of conflict curvature along a registered weight-transfer chord.

## Setup

Let

\[
L^*(w)=\min_z\sum_iw_i\ell_i(z)
\]

on a regular weight region, and define

\[
C(w)=-\nabla_w^2L^*(w)\succeq0.
\]

Choose two registered weight vectors `w_0,w_1` and the chord

\[
w_t=(1-t)w_0+t w_1,
\qquad t\in[0,1],
\]

with direction

\[
v=w_1-w_0.
\]

Let

\[
g(t)=L^*(w_t).
\]

Then

\[
-g''(t)=v^TC(w_t)v\ge0.
\]

Assume the directional curvature is bounded on the whole chord:

\[
0\le\alpha\le v^TC(w_t)v\le\beta<\infty.
\]

## Theorem 1 — conflict-load chord bulge

Define the linear endpoint chord

\[
\ell(t)=(1-t)g(0)+t g(1)
\]

and the concavity bulge

\[
J(t)=g(t)-\ell(t).
\]

Then

\[
\boxed{
\frac{\alpha}{2}t(1-t)
\le
J(t)
\le
\frac{\beta}{2}t(1-t).
}
\]

In particular, concavity alone gives `J(t)>=0`.

At the midpoint,

\[
\boxed{
\frac{\alpha}{8}
\le
L^*\!\left(\frac{w_0+w_1}{2}\right)
-\frac{L^*(w_0)+L^*(w_1)}{2}
\le
\frac{\beta}{8}.
}
\]

Thus the midpoint excess above the endpoint average is a direct measure of integrated weight-space conflict curvature.

## Matrix-bound version

If for a positive-semidefinite metric `Q`

\[
\alpha Q\preceq C(w_t)\preceq\beta Q
\]

along the chord, then

\[
\boxed{
\frac{\alpha}{2}t(1-t)v^TQv
\le J(t)\le
\frac{\beta}{2}t(1-t)v^TQv.
}
\]

This makes the prediction invariant to how the chord is parameterized once the weight metric is registered.

## Theorem 2 — three-point curvature audit

Given observed endpoint and interior optimized conflict loads, define

\[
\widehat J(t)
=\widehat L^*(w_t)-[(1-t)\widehat L^*(w_0)+t\widehat L^*(w_1)].
\]

Under the registered curvature bounds, the observation must lie inside the interval above after uncertainty propagation.

Therefore:

- `J<0` rejects concavity on the registered branch;
- `J<alpha t(1-t)/2` rejects the lower curvature bound;
- `J>beta t(1-t)/2` rejects the upper curvature bound.

This provides a direct finite-difference test without estimating the full weight Hessian.

## Corollary — scalar pairwise transfer

For a fixed-total two-function weight transfer, the theorem quantifies the previously proved pairwise concavity result. Three calibrated weight regimes are enough to test whether the observed compromise-load bulge is compatible with a preregistered directional curvature interval.

## Empirical consequence

A graded P/G weighting experiment can use two endpoint regimes and a midpoint regime to test SCH weight curvature before attempting a full multidimensional Hessian recovery.

This is especially useful when the focal system has only one independent relative-weight direction: it cannot identify a multidimensional curvature matrix, but it can still estimate the curvature integrated along that one causal direction.

## Claim ceiling

The theorem requires the same smooth optimum branch and valid curvature bounds over the whole weight chord. Weight interventions that change the loss families, phenotype accessibility or context invalidate the comparison. The result concerns optimized shared conflict, not PAYOFF dynamics.
