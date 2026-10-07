# SCH forward-reverse curvature-localization theorem v1

## Purpose

Use the **asymmetry** between forward and reverse finite weight-reoptimization relief to determine where directional conflict curvature is concentrated along a weight chord.

The symmetric forward+reverse sum recovers total chord-integrated curvature. The difference between the two directions adds localization information.

## Setup

Along

\[
w_t=w_0+t\Delta w,
\qquad t\in[0,1],
\]

define directional conflict curvature

\[
\kappa(t)
=\Delta w^\top C(w_t)\Delta w
\ge0,
\qquad
C=-\nabla_w^2L^*\succeq0.
\]

The forward and reverse reoptimization reliefs are

\[
\mathcal R_{01}
=\int_0^1(1-t)\kappa(t)dt,
\]

\[
\mathcal R_{10}
=\int_0^1t\kappa(t)dt.
\]

## Theorem 1 — asymmetry identity

Subtracting gives

\[
\boxed{
\mathcal R_{01}-\mathcal R_{10}
=\int_0^1(1-2t)\kappa(t)dt.
}
\]

Pairing points `t` and `1-t`,

\[
\boxed{
\mathcal R_{01}-\mathcal R_{10}
=
\int_0^{1/2}(1-2t)
[\kappa(t)-\kappa(1-t)]dt.
}
\]

Thus the sign of the forward/reverse difference reveals which half of the chord carries more directional curvature.

## Corollary 1a — monotone-curvature sign test

If `kappa(t)` is non-increasing along the forward path, then for `t<=1/2`,

\[
\kappa(t)\ge\kappa(1-t),
\]

so

\[
\boxed{
\mathcal R_{01}\ge\mathcal R_{10}.
}
\]

If `kappa(t)` is non-decreasing,

\[
\boxed{
\mathcal R_{01}\le\mathcal R_{10}.
}
\]

Constant directional curvature gives equality.

These are sufficient sign predictions; equality can also occur for nonconstant curvature arranged symmetrically around the chord midpoint.

## Definition — curvature localization index

When total symmetric relief is positive, define

\[
\boxed{
A_\kappa
=
\frac{\mathcal R_{01}-\mathcal R_{10}}
{\mathcal R_{01}+\mathcal R_{10}}.
}
\]

Because both directional reliefs are nonnegative,

\[
\boxed{-1\le A_\kappa\le1.}
\]

Interpretation:

- `A_kappa>0`: curvature is weighted more strongly toward the `w_0` side of the chord;
- `A_kappa<0`: curvature is weighted more strongly toward the `w_1` side;
- `A_kappa=0`: no directional localization is detected by this first antisymmetric moment.

This index is not evolutionary direction or irreversibility. It is a static curvature-localization statistic of one optimized value function.

## Theorem 2 — first moment of normalized curvature

Let total chord curvature be

\[
S=\mathcal R_{01}+\mathcal R_{10}
=\int_0^1\kappa(t)dt>0
\]

and define the curvature-weighted mean position

\[
\bar t_\kappa
=
\frac{\int_0^1t\kappa(t)dt}
{\int_0^1\kappa(t)dt}.
\]

Since the numerator is `R_10`,

\[
\boxed{
\bar t_\kappa
=
\frac{\mathcal R_{10}}
{\mathcal R_{01}+\mathcal R_{10}}.
}
\]

Therefore

\[
\boxed{
A_\kappa=1-2\bar t_\kappa.
}
\]

Forward and reverse endpoint experiments thus identify the **first spatial moment of directional curvature along the weight chord** without observing intermediate regimes.

## Empirical consequence

A matched reversible weight experiment can estimate:

```text
R_01       forward finite reoptimization relief
R_10       reverse finite reoptimization relief
S          total chord-integrated curvature
A_kappa    curvature localization index
bar t      curvature-weighted mean chord position
```

A preregistered hypothesis that curvature weakens as function `j` is up-weighted predicts `R_01 >= R_10` in that direction.

If forward and reverse interventions produce different underlying biological states because of carryover or history dependence, the static identity is invalid; that failure should be reported rather than interpreted as curvature localization.

## Claim ceiling

The result assumes both directions evaluate the same static optimized-load function `L*(w)`, with identical loss families and feasible phenotype space. The monotonicity sign rule requires monotone directional curvature along the chord. `A_kappa` localizes curvature mathematically and is not a historical or PAYOFF hysteresis measure.
