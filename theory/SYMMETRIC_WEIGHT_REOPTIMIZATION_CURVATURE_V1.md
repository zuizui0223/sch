# SCH symmetric finite reoptimization-curvature theorem v1

## Purpose

Combine forward and reverse finite weight shifts to recover the **full integrated directional conflict curvature** along a weight chord using endpoint quantities only.

The one-way reoptimization relief is a directional Bregman divergence and therefore asymmetric. The sum of the two directions removes that anchoring asymmetry.

## Setup

Let

\[
w_1=w_0+\Delta w
\]

and let optimized conflict load be the concave differentiable function

\[
L^*(w).
\]

Write endpoint residual-loss vectors

\[
r_0=\nabla_wL^*(w_0),
\qquad
r_1=\nabla_wL^*(w_1).
\]

Define forward reoptimization relief

\[
\mathcal R_{01}
=L_0+r_0^\top\Delta w-L_1
\ge0,
\]

and reverse relief

\[
\mathcal R_{10}
=L_1-r_1^\top\Delta w-L_0
\ge0.
\]

The reverse expression uses the no-reoptimization counterfactual anchored at the final optimum while moving weights back from `w_1` to `w_0`.

## Theorem 1 — symmetric endpoint identity

Adding the two directional reliefs cancels the optimized endpoint loads:

\[
\boxed{
\mathcal S_w
:=
\mathcal R_{01}+\mathcal R_{10}
=(r_0-r_1)^\top\Delta w.
}
\]

Because `-L*` is convex, its gradient is monotone, so

\[
\boxed{\mathcal S_w\ge0.}
\]

Thus the finite change in the endpoint residual-loss vector directly measures total integrated conflict curvature along the chord.

## Theorem 2 — full curvature integral

Let

\[
w_t=w_0+t\Delta w,
\qquad
C(w)=-\nabla_w^2L^*(w)\succeq0.
\]

The one-way reliefs satisfy

\[
\mathcal R_{01}
=
\int_0^1(1-t)
\Delta w^\top C(w_t)\Delta w\,dt,
\]

\[
\mathcal R_{10}
=
\int_0^1t
\Delta w^\top C(w_t)\Delta w\,dt.
\]

Therefore

\[
\boxed{
\mathcal S_w
=
\int_0^1
\Delta w^\top C(w_t)\Delta w\,dt.
}
\]

The forward/reverse sum removes the triangular weighting and yields the unweighted line integral of directional conflict curvature.

## Corollary 2a — symmetric effective curvature

For a registered PSD weight metric `Q` with

\[
\Delta w^\top Q\Delta w>0,
\]

define

\[
\boxed{
\bar\kappa_Q
=
\frac{\mathcal S_w}
{\Delta w^\top Q\Delta w}.
}
\]

Then

\[
\boxed{
\bar\kappa_Q
=
\int_0^1
\frac{\Delta w^\top C(w_t)\Delta w}
{\Delta w^\top Q\Delta w}
\,dt.
}
\]

So `bar kappa_Q` is the ordinary chord-average directional curvature, whereas the one-way effective curvature weights the chord toward its starting endpoint.

## Corollary 2b — bounds and constant-curvature case

If normalized directional curvature obeys

\[
\alpha\le\kappa_Q(t)\le\beta,
\]

then

\[
\boxed{
\alpha\le\bar\kappa_Q\le\beta.
}
\]

If curvature is constant along the chord, forward effective curvature, reverse effective curvature and the symmetric average all coincide.

## Theorem 3 — endpoint-only reconstruction

The full chord-average curvature can be computed from endpoint component-loss vectors alone:

\[
\boxed{
\bar\kappa_Q
=
\frac{(r_0-r_1)^\top\Delta w}
{\Delta w^\top Q\Delta w}.
}
\]

Hence an experiment need not directly estimate intermediate curvature if it can recover component residual losses at both optimized endpoints.

## Causal implication

A reversible or matched two-direction weight experiment can test three nested quantities:

1. forward finite reoptimization relief `R_01`;
2. reverse finite reoptimization relief `R_10`;
3. symmetric full-chord curvature `S_w`.

If either directional relief is significantly negative, or if

\[
(r_0-r_1)^\top\Delta w<0,
\]

the registered common-loss concave value-function model is falsified.

Forward and reverse relief need not be equal. Their difference carries information about where curvature is concentrated along the chord.

## Claim ceiling

The result requires the same optimized branch, loss families and feasible shared-phenotype set in both directions. Experimental irreversibility, carryover, acclimation or history dependence means the two directions are no longer evaluations of one static `L*(w)` and should not be forced into this identity. PAYOFF population dynamics are separate.
