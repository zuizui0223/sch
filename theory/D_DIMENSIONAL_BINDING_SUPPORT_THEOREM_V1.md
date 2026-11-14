# SCH d-dimensional binding-support theorem v1

## Purpose

Generalize the scalar binding-pair result to a shared trait coordinate of dimension `d`.

The result identifies how many functional constraints are required to certify the **globally worst shared-coordinate compromise** when the common phenotype is vector-valued.

## Setup

Let the shared trait be

\[
z\in Z\subset\mathbb R^d,
\]

where `Z` is convex. Function `i` has a normalized convex differentiable loss

\[
\ell_i(z)\ge0,
\qquad \min_{z\in Z}\ell_i(z)=0.
\]

Relative weights lie on the simplex

\[
\Delta_n=\{w_i\ge0,\;\sum_iw_i=1\}.
\]

Define

\[
L^*(w)=\min_{z\in Z}\sum_iw_i\ell_i(z).
\]

Under the same compactness/coercivity and minimax assumptions as the scalar weight-simplex theorem,

\[
C^*
=
\max_{w\in\Delta_n}L^*(w)
=
\min_{z\in Z}\max_i\ell_i(z).
\]

Let `z^dagger` be an interior minimizer of the right-hand side and let

\[
A(z^\dagger)=\{i:\ell_i(z^\dagger)=C^*\}
\]

be the active set.

## Theorem 1 — active gradients contain zero

For the convex envelope

\[
h(z)=\max_i\ell_i(z),
\]

interior optimality gives

\[
0\in\partial h(z^\dagger).
\]

With differentiable component losses,

\[
\partial h(z^\dagger)
=
\operatorname{conv}\{\nabla\ell_i(z^\dagger): i\in A(z^\dagger)\}.
\]

Hence

\[
\boxed{
0\in
\operatorname{conv}\{\nabla\ell_i(z^\dagger): i\in A(z^\dagger)\}.
}
\]

## Theorem 2 — at most d+1 binding functions are sufficient

By Caratheodory's theorem, any point in the convex hull of vectors in `R^d` can be represented as a convex combination of at most `d+1` of them.

Therefore there exist active indices

\[
i_1,\ldots,i_m,
\qquad m\le d+1,
\]

and nonnegative weights `alpha_r` summing to one such that

\[
\sum_{r=1}^m
\alpha_r\nabla\ell_{i_r}(z^\dagger)=0.
\]

Construct a functional-weight vector supported only on those indices:

\[
w_{i_r}=\alpha_r,
\qquad w_k=0\text{ otherwise}.
\]

The weighted loss is convex and has gradient zero at `z^dagger`, so `z^dagger` is a global minimizer. Since every selected function is active,

\[
\ell_{i_r}(z^\dagger)=C^*.
\]

Thus

\[
L^*(w)
=
\sum_r\alpha_rC^*
=C^*.
\]

Therefore

\[
\boxed{
\text{there exists a globally conflict-maximizing weighting with support}\le d+1.
}
\]

The scalar binding-pair theorem is exactly the `d=1` case.

## Tightness in two dimensions

Take three equal-curvature quadratic losses centered at the vertices of an equilateral triangle of circumradius one:

\[
\theta_1=(1,0),
\]

\[
\theta_2=(-1/2,\sqrt3/2),
\]

\[
\theta_3=(-1/2,-\sqrt3/2),
\]

with

\[
\ell_i(z)=\|z-\theta_i\|_2^2.
\]

The minimax phenotype is the origin and all three residual losses equal one. Equal weights give

\[
C^*=1.
\]

Any two vertices are separated by distance `sqrt(3)`. A two-function quadratic compromise has maximum optimized loss

\[
\frac{(\sqrt3)^2}{4}=\frac34<1.
\]

Therefore no two-function support reaches the global three-function conflict maximum.

So in dimension two, `d+1=3` binding functions can be genuinely necessary.

## Corollary — quadratic geometric interpretation

For equal-curvature quadratic losses

\[
\ell_i(z)=\|z-\theta_i\|^2,
\]

the minimax formulation becomes the minimum-enclosing-ball problem for the function-specific optima `theta_i`.

The globally worst shared-coordinate conflict load is the squared radius of that minimum enclosing ball, and a certificate requires at most `d+1` boundary points.

Thus SCH worst-case conflict geometry connects directly to the support geometry of the function-optimum cloud.

## Empirical interpretation

This extension distinguishes:

- **scalar shared traits**: a binding pair can certify worst-case conflict;
- **d-dimensional shared trait modules**: up to `d+1` binding functional demands may be required.

If a measured shared phenotype is inherently multidimensional, forcing it into a scalar score can hide the number and identity of binding functions. Conversely, if a low-dimensional latent trait coordinate is empirically justified, the theorem supplies an upper bound on the number of functional constraints required to explain its worst-case compromise.

## Claim ceiling

The result assumes a common convex `d`-dimensional shared phenotype space and the minimax conditions stated above. It does not imply that actual ecological weights equal the worst-case weights, nor that every multifunctional phenotype admits a low-dimensional common coordinate. Nonconvex accessibility and historical evolution are outside this theorem.
