# SCH trait-coordinate invariance theorem v1

## Purpose

Show that the weight-space curvature signature of shared-coordinate conflict is not an artifact of how the shared phenotype coordinate is linearly parameterized.

The active d-dimensional theorem gives

\[
\nabla_w^2L^*=-G^\top H^{-1}G,
\]

where `H` is the total phenotype Hessian and the columns of `G` are the function gradients at the optimized shared phenotype. The present result proves that this matrix is exactly invariant under every invertible linear change of trait coordinates.

## Setup

Let the original shared phenotype be

\[
z\in\mathbb R^d
\]

and make an invertible linear reparameterization

\[
\tilde z=A z,
\qquad A\in GL(d).
\]

Write

\[
\tilde\ell_i(\tilde z)=\ell_i(A^{-1}\tilde z).
\]

At the matched optimum, the transformed function gradients and total Hessian are

\[
\tilde g_i=A^{-\top}g_i,
\]

and

\[
\tilde H=A^{-\top}HA^{-1}.
\]

Hence

\[
\tilde H^{-1}=AH^{-1}A^\top.
\]

Collecting transformed gradients as

\[
\tilde G=A^{-\top}G,
\]

gives the transformed weight-curvature matrix.

## Theorem 1 — exact coordinate invariance of optimized conflict curvature

Substitution gives

\[
\tilde G^\top\tilde H^{-1}\tilde G
=
G^\top A^{-1}
(AH^{-1}A^\top)
A^{-\top}G
=
G^\top H^{-1}G.
\]

Therefore

\[
\boxed{
\nabla_w^2\tilde L^*
=
\nabla_w^2L^*.
}
\]

So the complete weight-space Hessian of optimized conflict is invariant to invertible linear reparameterization of the shared trait coordinate.

This is stronger than rank invariance: every entry of the weight-curvature matrix is unchanged when the phenotype coordinate and its Hessian are transformed consistently.

## Corollary 1a — rank and vanishing-minor signatures are coordinate free

Because the matrix itself is invariant,

\[
\operatorname{rank}(-\nabla_w^2L^*)
\]

and every vanishing-minor constraint are invariant as well.

Thus a low-rank empirical signature cannot be created or removed merely by changing from raw trait units to standardized units, rotating a multivariate trait basis, or applying any other invertible linear coordinate transformation.

## Corollary 1b — phenotype sensitivity transforms covariantly

The d-dimensional sensitivity theorem gives

\[
\frac{\partial z^*}{\partial\log w_j}
=-H^{-1}w_jg_j.
\]

In transformed coordinates,

\[
\frac{\partial\tilde z^*}{\partial\log w_j}
=-\tilde H^{-1}w_j\tilde g_j
=-AH^{-1}A^\top w_jA^{-\top}g_j
=A\frac{\partial z^*}{\partial\log w_j}.
\]

Hence

\[
\boxed{
\frac{\partial\tilde z^*}{\partial\log w_j}
=A\frac{\partial z^*}{\partial\log w_j}.
}
\]

The response vector changes coordinates exactly as the trait vector itself should, while the induced weight-space curvature remains invariant.

## Corollary 1c — the hidden-dimension diagnostic is not a units artifact

If observed weight-response curvature robustly has effective rank `r`, then any registered shared-coordinate model with dimension

\[
d<r
\]

fails regardless of the invertible linear trait basis used to describe that model.

This makes the curvature-rank test a coordinate-free falsifier of an underspecified shared phenotype dimension.

## Why this matters for SCH

A multivariate floral or biomechanical trait can be represented in many ways: original measurements, principal-component coordinates, standardized variables, rotated axes, or mechanistic linear combinations. A theory whose dimensionality signature changed under such bookkeeping choices would be fragile.

The present theorem shows that the SCH weight-curvature object

\[
-G^\top H^{-1}G
\]

lives in **functional-weight space**, not trait-coordinate space. The trait basis can change, but the predicted curvature among functional weights does not.

## Empirical consequence

A preregistered multidimensional SCH experiment can report both:

1. phenotype-response vectors in a chosen interpretable trait basis;
2. the coordinate-invariant weight-curvature matrix and its rank/minor diagnostics.

If two analysts use different invertible linear trait bases on the same fitted local model, they should recover the same weight-space curvature matrix within numerical tolerance.

## Claim ceiling

The result covers invertible linear reparameterizations of a fixed regular local shared-coordinate model. Nonlinear coordinate maps require the corresponding differential-geometric treatment and can introduce extra second-derivative terms away from a stationary-point transformation. Changing the phenotype space itself, dropping dimensions, changing loss families, or crossing nonregular optima is not a coordinate change and is outside this theorem. PAYOFF dynamics remain separate.
