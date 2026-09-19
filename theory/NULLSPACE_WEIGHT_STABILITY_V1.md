# SCH nullspace-weight stability theorem v1

## Purpose

Add a noise-robust stability bound to curvature-nullspace weight identification. Exact algebra says that a one-dimensional curvature nullspace identifies relative functional weights. The present result says when that identification is numerically/statistically stable.

## Setup

Let the true optimized conflict-curvature matrix be symmetric positive semidefinite,

\[
C\succeq0,
\]

with a simple zero eigenvalue

\[
\lambda_1(C)=0
\]

and next eigenvalue

\[
\lambda_2(C)=\gamma>0.
\]

Let the normalized true functional-weight direction be the positive unit null vector `w`, so

\[
Cw=0.
\]

Let an estimated symmetric curvature matrix satisfy a prospective operator-norm error bound

\[
\|\widehat C-C\|_{op}\le\varepsilon.
\]

Assume

\[
\varepsilon<\gamma/2.
\]

Let `w_hat` be the unit eigenvector of `C_hat` associated with its smallest eigenvalue, oriented to have positive inner product with `w`.

## Theorem 1 — null-direction angular stability

Weyl's inequality gives

\[
\lambda_2(\widehat C)\ge\gamma-\varepsilon.
\]

The true zero eigenspace is therefore separated from the unwanted estimated eigenspace by at least `gamma-epsilon`.

A Davis-Kahan sin-theta bound yields

\[
\boxed{
\sin\angle(\widehat w,w)
\le
\frac{\varepsilon}{\gamma-\varepsilon}.
}
\]

Hence the curvature-derived weight direction is stable when the nullspace spectral gap is large relative to the curvature estimation error.

The requirement `epsilon < gamma/2` guarantees both separation and a nontrivial bound below one.

## Corollary 1a — instability near an additional hidden null direction

As

\[
\gamma\downarrow0,
\]

the bound deteriorates. This is not merely a numerical nuisance: it means the data are approaching a geometry with nullity greater than one, where relative functional weights cease to be identifiable from curvature alone.

Thus the same spectral gap controls both:

- algebraic uniqueness of the force-balance direction;
- statistical stability of its recovery.

## Corollary 1b — estimated-gap fail-closed rule

The true gap `gamma` is unknown. Weyl also gives

\[
\gamma
\ge
\widehat\lambda_2-\varepsilon.
\]

A conservative sufficient condition for stable one-dimensional nullspace recovery is therefore

\[
\widehat\lambda_2>3\varepsilon,
\]

which implies the true `gamma>2 epsilon`.

Under this condition one may substitute the conservative gap lower bound

\[
\gamma_L=\widehat\lambda_2-\varepsilon
\]

into

\[
\boxed{
\sin\theta
\le
\frac{\varepsilon}{\gamma_L-\varepsilon}
=
\frac{\varepsilon}{\widehat\lambda_2-2\varepsilon}.
}
\]

If `lambda2_hat <= 3 epsilon`, the correct status is **NULLSPACE_WEIGHT_DIRECTION_UNSTABLE_OR_UNRESOLVED**, not a precise relative-weight estimate.

## Theorem 2 — relationship to the dimension certificate

The earlier spectral dimension certificate counts eigenvalues above the operator-error floor. The present theorem uses the **smallest positive** curvature mode as a conditioning quantity.

These answer different questions:

- large higher eigenvalues can reject an underspecified shared dimension;
- a large smallest-positive eigenvalue stabilizes recovery of the unique null weight direction.

A curvature matrix can have the correct rank yet still yield unstable weights if its smallest positive eigenvalue is close to the estimation error.

## Empirical consequence

A multi-level functional-weight experiment that claims curvature-based relative weights should report:

```text
smallest two estimated curvature eigenvalues
prospective operator-norm error bound epsilon
one-dimensional-nullspace compatibility
estimated spectral-gap lower bound
sin-angle upper bound for the weight direction
```

Only after this conditioning audit should the positive estimated null vector be normalized to the simplex and interpreted biologically.

## Claim ceiling

The theorem controls the angle of the null direction under symmetric operator-norm perturbation. It does not by itself convert that angle into componentwise confidence intervals on simplex weights; those depend on the true weight vector's distance from the simplex boundary. The result assumes a simple true null eigenvalue and the same regular shared-coordinate model used by the exact curvature identity. PAYOFF dynamics remain separate.
