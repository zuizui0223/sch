# SCH optimized conflict-load curvature theorem v1

## Purpose

Extend SCH from the location of the shared optimum to the **curvature of the optimized compromise cost** with respect to functional weights.

Let

\[
J(z;w)=\sum_{i=1}^n w_i\ell_i(z),\qquad w_i>0,
\]

where each loss is twice continuously differentiable and the optimized shared state `z*(w)` is unique and regular. Define

\[
L^*(w)=\min_z J(z;w)=J(z^*(w);w)
\]

and

\[
H(w)=\sum_iw_i\ell_i''(z^*)>0.
\]

Losses may be normalized so that `ell_i(theta_i)=0`, but the derivative results below do not require quadratic loss.

## Theorem 1 — function-specific shadow price

By the envelope theorem,

\[
\boxed{
\frac{\partial L^*}{\partial w_j}=\ell_j(z^*)
}
\]

for every function `j`.

Thus the marginal increase in optimized compromise load caused by increasing function `j`'s weight is exactly the residual loss of function `j` at the current compromise.

If losses are normalized at their own optima, this shadow price is non-negative and is strictly positive whenever the current shared optimum differs from `theta_j`.

## Theorem 2 — exact Hessian in weight space

The shared-optimum sensitivity is

\[
\frac{\partial z^*}{\partial w_k}
=-\frac{\ell_k'(z^*)}{H}.
\]

Differentiate the envelope result:

\[
\frac{\partial^2 L^*}{\partial w_j\partial w_k}
=
\ell_j'(z^*)\frac{\partial z^*}{\partial w_k}.
\]

Therefore

\[
\boxed{
\frac{\partial^2 L^*}{\partial w_j\partial w_k}
=-\frac{\ell_j'(z^*)\ell_k'(z^*)}{H}
}
\]

and, writing `g_i=ell_i'(z*)`,

\[
\boxed{
\nabla_w^2L^*=-\frac{gg^T}{H}.
}
\]

The Hessian is negative semidefinite and has rank at most one.

## Corollary 2a — optimized conflict load is concave in functional weights

For any vector `v`,

\[
v^T\nabla_w^2L^*v
=-\frac{(v^Tg)^2}{H}\le0.
\]

Hence

\[
\boxed{L^*(w)\text{ is locally concave in }w}
\]

where the optimum is regular. Globally, the same concavity also follows because `L*(w)` is the pointwise infimum over `z` of functions that are affine in `w`.

Biologically, increasing a functional weight can raise the optimized compromise cost, but the marginal cost is itself changed by the movement of the shared optimum.

## Corollary 2b — cross-weight sign identifies which functions oppose each other at the compromise

If functions `j` and `k` pull the current compromise in opposite directions, then

\[
\ell_j'(z^*)\ell_k'(z^*)<0
\]

and therefore

\[
\boxed{
\frac{\partial^2L^*}{\partial w_j\partial w_k}>0.
}
\]

If both gradients point in the same direction, the cross-partial is negative.

Thus opposite-side functions are identifiable locally not only from opposite optimum-shift directions but also from the sign structure of the optimized-load Hessian.

## Corollary 2c — homogeneity

Because multiplying all weights by `a>0` leaves `z*` unchanged,

\[
L^*(aw)=aL^*(w).
\]

So `L*` is positively homogeneous of degree one in functional weights. Euler's theorem gives

\[
\boxed{
L^*(w)=\sum_jw_j\frac{\partial L^*}{\partial w_j}
=\sum_jw_j\ell_j(z^*).
}
\]

The compromise location depends on **relative** functional weighting, whereas the absolute optimized loss scales with the common weight scale.

## Empirical consequence

If selective interventions can alter several functional demands independently, SCH can estimate more than the sign of optimum movement:

1. the first-order shift of `z*` identifies directional functional pull;
2. the change in optimized conflict load identifies the shadow price `ell_j(z*)`;
3. paired weight perturbations can, in principle, test whether functions lie on opposite sides of the compromise through the cross-curvature sign.

This is a stronger falsifiable structure than a generic statement that several functions influence one trait.

## Claim ceiling

The Hessian formula assumes a common scalar shared coordinate, regular unique optimum, fixed loss functions during the weight perturbation, and positive total curvature. If changing a functional demand changes the loss shape itself, the formula needs additional terms.
