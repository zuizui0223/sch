# SCH pairwise functional-weight transfer theorem v1

## Purpose

Characterize what happens when total functional importance is held fixed but weight is transferred between two functions.

Start from

\[
L^*(w)=\min_z\sum_iw_i\ell_i(z)
\]

with the regular unique shared optimum `z*(w)` and positive total curvature

\[
H=\sum_iw_i\ell_i''(z^*)>0.
\]

Choose functions `j` and `k`. Along a feasible transfer path,

\[
w_j(t)=w_j+t,
\qquad
w_k(t)=w_k-t,
\]

while every other weight remains fixed. Total weight is unchanged.

Define

\[
F(t)=L^*(w(t)).
\]

## Theorem 1 — first derivative is the residual-loss contrast

By the envelope theorem,

\[
\boxed{
F'(t)=\ell_j(z^*)-\ell_k(z^*).
}
\]

Thus transferring a small amount of importance from function `k` to function `j` raises optimized compromise load exactly when function `j` currently suffers the larger residual loss at the shared optimum.

This gives a direct interpretation of the weight-transfer gradient: it compares **unresolved functional losses**, not raw function weights.

## Theorem 2 — fixed-total-weight transfer is concave

Differentiate the first-order condition along `t`:

\[
H\frac{dz^*}{dt}
+\ell_j'(z^*)-\ell_k'(z^*)=0.
\]

Therefore

\[
\frac{dz^*}{dt}
=-\frac{\ell_j'(z^*)-\ell_k'(z^*)}{H}.
\]

Differentiate `F'`:

\[
F''(t)
=
[\ell_j'(z^*)-\ell_k'(z^*)]\frac{dz^*}{dt}.
\]

Hence

\[
\boxed{
F''(t)
=-\frac{[\ell_j'(z^*)-\ell_k'(z^*)]^2}{H}
\le0.
}
\]

So optimized compromise load is concave along every pairwise weight-transfer direction that preserves total weight.

It is strictly concave whenever the two functions have different local gradients at the compromise.

## Corollary 2a — equal residual losses define the interior maximum

Any interior stationary point satisfies

\[
F'(t)=0
\]

and therefore

\[
\boxed{
\ell_j(z^*)=\ell_k(z^*).
}
\]

Because `F` is concave, such an interior stationary point is the global maximum of optimized compromise load along that transfer path.

Thus the largest compromise burden produced by redistributing a fixed total amount of importance between two functions occurs where their residual losses are equal, provided that equal-loss point is feasible and interior.

This is an **equal-residual-loss maximum**, not a claim that the biological system chooses weights to maximize conflict.

## Corollary 2b — if no equal-loss point is feasible, the maximum lies at a transfer boundary

If

\[
\ell_j(z^*)-\ell_k(z^*)
\]

never changes sign over the feasible transfer range, `F` is monotone there and its maximum occurs at one endpoint.

## Quadratic special case

For

\[
\ell_i(z)=\frac12(z-\theta_i)^2
\]

with two functions and fixed total weight `W=w_1+w_2`,

\[
L^*=\frac12\frac{w_1w_2}{W}(\theta_1-\theta_2)^2.
\]

The fixed-total transfer curve is a concave quadratic and is maximized at

\[
w_1=w_2=W/2,
\]

where the shared optimum is the midpoint and the two residual losses are equal.

## Empirical consequence

A system in which two functional demands can be titrated while approximately holding their total contribution fixed predicts:

1. a concave optimized-load response to pairwise weight transfer;
2. a sign change of the first derivative when residual functional losses cross;
3. maximum conflict burden near equal residual losses, not necessarily near equal raw treatment intensity if the loss shapes differ.

This creates a stronger experimental target for SCH than merely comparing two endpoint environments.

## Claim ceiling

The result concerns a counterfactual functional-weight path with fixed loss shapes and a regular scalar compromise optimum. It does not imply that natural selection adjusts functional weights to maximize compromise load, and it is not a PAYOFF game result.
