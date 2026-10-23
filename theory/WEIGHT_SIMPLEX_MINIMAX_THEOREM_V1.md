# SCH weight-simplex minimax theorem v1

## Purpose

Characterize the **largest possible optimized shared-coordinate conflict load** over all relative functional weightings, without assuming quadratic loss.

Let `Z` be a convex trait interval and let each normalized function loss

\[
\ell_i(z)\ge 0,
\qquad \min_z\ell_i(z)=0,
\]

be continuous and convex. Let relative functional weights lie on the simplex

\[
\Delta_n=\{w_i\ge0,\;\sum_iw_i=1\}.
\]

Define

\[
L^*(w)=\min_{z\in Z}\sum_i w_i\ell_i(z).
\]

Assume the usual compactness/coercivity conditions needed for the minima and minimax interchange.

## Theorem 1 — worst weighting equals best worst-function compromise

Because

\[
f(w,z)=\sum_iw_i\ell_i(z)
\]

is linear in `w` and convex in `z`, the convex-concave minimax theorem gives

\[
\boxed{
\max_{w\in\Delta_n}L^*(w)
=
\min_{z\in Z}\max_i\ell_i(z)
}.
\]

Thus the largest conflict load attainable by changing **relative function importance** is exactly the smallest worst-function residual loss achievable on the shared axis.

This turns the SCH weight problem into a minimax compromise problem.

## Theorem 2 — KKT equal-loss condition on the active weight support

Suppose `L*` is differentiable at a maximizing weight vector `w*`, with shared optimum `z*`. By the envelope theorem,

\[
\frac{\partial L^*}{\partial w_i}=\ell_i(z^*).
\]

At a simplex maximum, feasible pairwise weight transfers imply:

- if `w_i*>0` and `w_j*>0`, then
  \[
  \boxed{\ell_i(z^*)=\ell_j(z^*)};
  \]
- if `w_k*=0` and `w_i*>0`, then
  \[
  \boxed{\ell_k(z^*)\le\ell_i(z^*)}.
  \]

So all functions that receive positive weight in a conflict-maximizing mixture have equal residual loss, while excluded functions are no worse off at that shared phenotype.

## Corollary 2a — active residual loss equals the maximum conflict load

Because weights sum to one,

\[
L^*(w^*)=\sum_iw_i^*\ell_i(z^*).
\]

If every active function has the same residual loss `C`, then

\[
\boxed{L^*(w^*)=C}.
\]

Combining with Theorem 1,

\[
\boxed{
C
=
\max_wL^*(w)
=
\min_z\max_i\ell_i(z)
}.
\]

The worst ecological weighting therefore selects a shared phenotype that equalizes the binding functional losses.

## Corollary 2b — two-function case

With two distinct strictly convex losses, the simplex maximum is interior. Hence the maximizing weighting satisfies

\[
\boxed{\ell_1(z^*)=\ell_2(z^*)}.
\]

For symmetric quadratic losses around two optima this reduces to equal weighting and the midpoint phenotype, but equality of residual losses rather than arithmetic symmetry is the general statement.

## Three-function example

For

\[
\ell_1=(z+1)^2,
\qquad
\ell_2=z^2,
\qquad
\ell_3=(z-1)^2,
\]

the minimax shared phenotype is `z*=0` with worst residual loss `1`.

A maximizing weight vector is

\[
w^*=(1/2,0,1/2),
\]

so the active extreme functions each incur loss `1`, while the central function has residual loss `0` and therefore need not receive weight in the conflict-maximizing mixture.

This shows why the maximum-conflict weighting need not have full support when several functions are present.

## Empirical interpretation

Across environments that redistribute relative functional importance, SCH predicts more than directional optimum shifts:

1. the optimized conflict load is concave in the weight vector;
2. there is a globally worst relative weighting on the simplex;
3. at that worst weighting, the binding functions have equal residual fitness loss on the common outcome scale.

A sufficiently rich factorial experiment can therefore ask whether estimated conflict load across function-weight treatments approaches the predicted equal-loss configuration.

## Claim ceiling

This is a theorem about the declared shared-coordinate optimization problem. It does not imply that natural environments explore the full weight simplex, that functional weights are independently manipulable, or that the conflict-maximizing weighting is evolutionarily realized. PAYOFF invasion dynamics remain separate.
