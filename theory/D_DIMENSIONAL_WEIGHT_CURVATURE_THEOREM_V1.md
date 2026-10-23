# SCH d-dimensional weight-curvature theorem v1

## Purpose

Generalize the scalar weight-sensitivity and rank-one conflict-load Hessian to a shared phenotype coordinate

\[
z\in\mathbb R^d.
\]

The result shows that even when many functional weights vary, the local second-order geometry of optimized conflict caused by phenotype movement has rank at most the dimension of the shared trait space.

## Setup

Let

\[
J(z;w)=\sum_{i=1}^n w_i\ell_i(z),
\qquad w_i>0,
\]

where each `ell_i` is twice continuously differentiable and convex on the relevant region.

Assume the optimized shared phenotype `z*(w)` is unique and the total phenotype Hessian

\[
H
=
\sum_iw_i\nabla^2\ell_i(z^*)
\]

is positive definite.

Define the function-gradient columns

\[
g_i=\nabla\ell_i(z^*)\in\mathbb R^d
\]

and collect them in

\[
G=[g_1\;g_2\;\cdots\;g_n]\in\mathbb R^{d\times n}.
\]

The first-order condition is

\[
\sum_iw_i g_i=0.
\]

## Theorem 1 — vector phenotype sensitivity to log functional weight

Differentiate the first-order condition with respect to `log w_j`:

\[
H\frac{\partial z^*}{\partial\log w_j}
+w_jg_j=0.
\]

Therefore

\[
\boxed{
\frac{\partial z^*}{\partial\log w_j}
=-H^{-1}w_jg_j.
}
\]

So the response to up-weighting one function is the negative function gradient transformed by the inverse curvature of the combined shared-fitness landscape.

Unlike the scalar case, “toward the function optimum” is now a vector statement mediated by the local Hessian geometry rather than a simple sign rule.

## Theorem 2 — exact weight-space Hessian of optimized conflict load

Define

\[
L^*(w)=J(z^*(w);w).
\]

The envelope theorem gives

\[
\frac{\partial L^*}{\partial w_i}=\ell_i(z^*).
\]

Differentiate with respect to `w_j`. Since

\[
\frac{\partial z^*}{\partial w_j}=-H^{-1}g_j,
\]

we obtain

\[
\boxed{
\frac{\partial^2L^*}{\partial w_i\partial w_j}
=-g_i^\top H^{-1}g_j.
}
\]

In matrix form,

\[
\boxed{
\nabla_w^2L^*
=-G^\top H^{-1}G.
}
\]

This is negative semidefinite because for any weight perturbation vector `v`,

\[
v^\top\nabla_w^2L^*v
=-(Gv)^\top H^{-1}(Gv)
\le0.
\]

Thus optimized conflict load remains concave in functional weights in arbitrary shared-coordinate dimension.

## Theorem 3 — curvature rank is at most shared-trait dimension

Because

\[
\operatorname{rank}(G^\top H^{-1}G)
\le
\operatorname{rank}(G)
\le d,
\]

we have

\[
\boxed{
\operatorname{rank}(-\nabla_w^2L^*)\le d.
}
\]

Therefore at most `d` independent combinations of functional-weight perturbations generate nonzero second-order curvature through movement of the optimized shared phenotype.

For the scalar SCH model (`d=1`), this reduces to the previously derived rank-one Hessian.

## Corollary 3a — local flat weight directions

If a perturbation `v` satisfies

\[
Gv=0,
\]

then

\[
v^\top\nabla_w^2L^*v=0.
\]

Such a weight redistribution has no second-order effect on optimized conflict load through phenotype movement at the current context.

This does not imply no first-order change in `L*`; the first-order term is set by residual losses. It means the local **curvature correction from re-optimizing the shared phenotype** vanishes in that direction.

## Corollary 3b — only relative weights move the phenotype

The common-scaling direction `v=w` obeys

\[
Gw=\sum_iw_ig_i=0
\]

by the first-order condition.

Thus multiplying all functional weights together remains a phenotype-flat direction in any dimension.

## Quadratic special case

For

\[
\ell_i(z)=\frac12(z-\theta_i)^\top Q_i(z-\theta_i),
\qquad Q_i\succ0,
\]

we have

\[
g_i=Q_i(z^*-\theta_i),
\qquad
H=\sum_iw_iQ_i.
\]

The formulas above become exact global differential identities wherever weights remain positive.

## Empirical consequence

For a multidimensional shared trait module, experimentally perturbing many functional demands need not require estimating an unconstrained `n x n` curvature matrix. The theory predicts a low-rank structure:

\[
-\nabla_w^2L^*
\]

should have effective rank no larger than the dimension of the common phenotype coordinate under the model.

If empirical weight-response curvature robustly requires rank greater than the registered shared-coordinate dimension, then at least one of the following is wrong:

- the assumed trait dimension is too small;
- functional weighting changes the loss families themselves;
- additional hidden phenotype coordinates are moving;
- the local common-coordinate model is inadequate.

This turns curvature rank into a possible diagnostic for hidden dimensionality.

## Claim ceiling

The rank statement is local and assumes a unique regular optimum with positive-definite combined Hessian. Boundaries, nonconvex optima, weight-dependent loss functions and changing phenotype accessibility can break the formula. It does not identify historical evolution or PAYOFF dynamics.
