# SCH binding-pair reduction theorem v1

## Purpose

Show that even when many functions share one scalar trait axis, the **globally worst relative functional weighting can always be represented by at most two binding functions** under the declared convex minimax assumptions.

This is a dimension-specific result for a one-dimensional shared coordinate.

## Setup

Use the normalized convex losses and weight simplex from the weight-simplex minimax theorem:

\[
L^*(w)=\min_z\sum_{i=1}^n w_i\ell_i(z),
\qquad
w\in\Delta_n,
\]

and

\[
C^*
=
\max_{w\in\Delta_n}L^*(w)
=
\min_z\max_i\ell_i(z).
\]

Let

\[
z^\dagger\in\operatorname*{arg\,min}_z\max_i\ell_i(z)
\]

be an interior minimax phenotype and define the active set

\[
A(z^\dagger)=\{i:\ell_i(z^\dagger)=C^*\}.
\]

Assume the losses are differentiable at `z^dagger` and `C*>0`.

## Theorem 1 — active gradients straddle zero

The pointwise maximum

\[
h(z)=\max_i\ell_i(z)
\]

is convex. At an interior minimizer,

\[
0\in\partial h(z^\dagger).
\]

For differentiable component losses,

\[
\partial h(z^\dagger)
=
\operatorname{conv}\{\ell_i'(z^\dagger):i\in A(z^\dagger)\}.
\]

Therefore

\[
\boxed{
0\in
\operatorname{conv}\{\ell_i'(z^\dagger):i\in A(z^\dagger)\}.
}
\]

Because the gradient space is one-dimensional, there exist active functions `i,j` with

\[
\ell_i'(z^\dagger)\le0\le\ell_j'(z^\dagger)
\]

whose two gradients already contain zero in their convex hull.

## Theorem 2 — two active functions suffice to realize the global maximum conflict

Choose `alpha in [0,1]` such that

\[
\alpha\ell_i'(z^\dagger)
+(1-\alpha)\ell_j'(z^\dagger)=0.
\]

Define a weight vector supported only on these two functions:

\[
w_i=\alpha,
\qquad
w_j=1-\alpha,
\qquad
w_k=0\;(k\notin\{i,j\}).
\]

The weighted objective is convex and has first derivative zero at `z^dagger`, so `z^dagger` is its global minimizer. Since both functions are active,

\[
\ell_i(z^\dagger)
=
\ell_j(z^\dagger)
=C^*.
\]

Hence

\[
L^*(w)
=
\alpha C^*+(1-\alpha)C^*
=C^*.
\]

Therefore

\[
\boxed{
\text{there exists a globally conflict-maximizing }w^*
\text{ with support size at most }2.
}
\]

When `C*>0` and every individual loss is normalized to zero at its own minimum, the nondegenerate interior case requires two binding functions rather than one.

## Interpretation

The result does **not** say that only two biological functions matter in an organism. It says that on a one-dimensional shared trait axis, the worst achievable compromise over all relative weightings can be certified by a pair of binding functional constraints.

Additional functions can:

- alter which pair is binding;
- create ties with more than two active functions;
- matter strongly away from the global maximum-conflict weighting;
- change the landscape if their loss families themselves change.

But there always exists a two-function support that realizes the same global maximum conflict load.

## Corollary — quadratic ordered optima

For equal-curvature quadratic losses

\[
\ell_i(z)=(z-\theta_i)^2,
\]

the global minimax phenotype is the midpoint of the extreme optima,

\[
z^\dagger
=
\frac{\theta_{\min}+\theta_{\max}}{2},
\]

and the maximum conflict load is

\[
\boxed{
C^*
=
\frac{(\theta_{\max}-\theta_{\min})^2}{4}.
}
\]

A maximizing weighting puts one half of the weight on each extreme function; all intermediate-optimum functions are nonbinding for this worst-case certificate.

## Empirical consequence

For many-function systems, SCH can separate two questions:

1. **actual ecological weighting** — all functions may matter and must be estimated;
2. **worst-case shared-axis conflict capacity** — can be bounded or certified by identifying the binding pair on the shared coordinate.

This suggests a practical screening strategy for high-dimensional multifunctionality: first identify candidate extreme/binding functions, then test whether the full weight structure changes the observed causal compromise away from that worst-case pair.

## Claim ceiling

The support-reduction theorem uses a scalar trait coordinate and convex minimax geometry. In a `d`-dimensional shared coordinate, Caratheodory-type logic would generally require up to `d+1` binding gradients rather than two. Nonconvex landscapes, boundary optima, inaccessible trait regions or changing loss families require separate treatment.
