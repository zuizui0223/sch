# SCH finite weight effective-curvature theorem v1

## Purpose

Use the finite weight-reoptimization relief to identify an **integrated directional curvature** along a functional-weight change without estimating the full local Hessian at every intermediate regime.

## Setup

For a registered finite weight chord

\[
w_t=w_0+t\Delta w,
\qquad t\in[0,1],
\]

let

\[
C(w)=-\nabla_w^2L^*(w)\succeq0
\]

be optimized conflict curvature and let the finite reoptimization relief be

\[
\mathcal R_w
=\int_0^1(1-t)
\,\Delta w^\top C(w_t)\Delta w\,dt.
\]

Register a positive-semidefinite weight metric `Q` such that

\[
\Delta w^\top Q\Delta w>0.
\]

Define instantaneous normalized directional curvature

\[
\kappa_Q(t)
=
\frac{\Delta w^\top C(w_t)\Delta w}
{\Delta w^\top Q\Delta w}.
\]

## Definition — finite effective curvature

Define

\[
\boxed{
\kappa_{\rm eff,Q}
=
\frac{2\mathcal R_w}
{\Delta w^\top Q\Delta w}.
}
\]

## Theorem 1 — weighted-average identity

Substituting the relief integral gives

\[
\boxed{
\kappa_{\rm eff,Q}
=
2\int_0^1(1-t)\kappa_Q(t)\,dt.
}
\]

Because

\[
2\int_0^1(1-t)dt=1,
\]

`kappa_eff,Q` is a genuine weighted average of the directional conflict curvature along the chord, with greater weight near the baseline regime.

## Corollary 1a — range identification

If

\[
\kappa_{min}\le\kappa_Q(t)\le\kappa_{max}
\]

on the chord, then

\[
\boxed{
\kappa_{min}
\le
\kappa_{\rm eff,Q}
\le
\kappa_{max}.
}
\]

Thus endpoint quantities cannot identify the full curvature profile, but they identify one exact weighted average of that profile.

## Corollary 1b — constant-curvature recovery

If directional curvature is constant along the registered chord,

\[
\kappa_Q(t)=\kappa_0,
\]

then

\[
\boxed{
\kappa_{\rm eff,Q}=\kappa_0.
}
\]

So a two-endpoint finite weight experiment plus the baseline frozen-phenotype counterfactual is enough to recover the exact directional curvature when the quadratic/constant-curvature model holds.

## Theorem 2 — comparison with midpoint chord curvature

The existing midpoint chord-bulge quantity weights curvature symmetrically around the chord, whereas `kappa_eff,Q` weights it by `2(1-t)` and is anchored at the starting regime.

Therefore comparing the two finite-difference summaries tests whether curvature is approximately constant or systematically changes along the weight shift.

A strong asymmetry between forward and reverse effective curvature is expected when the conflict landscape is nonlinear, because Bregman reoptimization relief is direction-dependent.

## Empirical consequence

A calibrated weight-shift experiment can report

\[
\widehat\kappa_{\rm eff,Q}
=
\frac{2\widehat{\mathcal R}_w}
{\Delta w^\top Q\Delta w}
\]

using only:

- baseline component residual losses;
- the declared weight change;
- final optimized conflict load.

This provides a scalar curvature target even when the experiment lacks the design capacity to reconstruct the full multidimensional weight-curvature matrix.

For the focal two-function design, this is especially useful: one relative-weight direction cannot reveal a multidimensional curvature rank, but it can reveal the integrated curvature along that one causal direction.

## Claim ceiling

`kappa_eff,Q` depends on the registered weight metric and direction. It is not the full Hessian, not a trait-space dimension, and not comparable across experiments using incompatible weight semantics. The identity requires the same regular optimized branch and fixed loss families along the finite chord. PAYOFF dynamics remain outside scope.
