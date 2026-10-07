# SCH spectral dimension certificate v1

## Purpose

Turn the exact low-rank weight-curvature theorem into a noise-robust falsification rule for the registered shared-coordinate dimension.

Under the regular `d`-dimensional shared-coordinate model,

\[
M=-\nabla_w^2L^*=G^\top H^{-1}G\succeq0,
\qquad
\operatorname{rank}(M)\le d.
\]

Exact rank is fragile to estimation noise, so empirical use requires a perturbation certificate rather than literal zero eigenvalues.

## Setup

Let `M` be the true PSD weight-curvature matrix and let `Mhat` be a symmetric empirical estimate. Assume a registered operator-norm error bound

\[
\|\widehat M-M\|_{\mathrm{op}}\le\varepsilon.
\]

Write ordered eigenvalues

\[
\lambda_1(A)\ge\lambda_2(A)\ge\cdots\ge\lambda_n(A).
\]

## Theorem 1 — dimension-d model implies a spectral ceiling

If the registered shared-coordinate dimension is at most `d`, then

\[
\lambda_{d+1}(M)=0.
\]

Weyl's eigenvalue perturbation inequality gives

\[
|\lambda_k(\widehat M)-\lambda_k(M)|\le\varepsilon.
\]

Therefore every valid dimension-`d` model must satisfy

\[
\boxed{
\lambda_{d+1}(\widehat M)\le\varepsilon.
}
\]

Hence

\[
\boxed{
\lambda_{d+1}(\widehat M)>\varepsilon
\Longrightarrow
\operatorname{rank}(M)>d
}
\]

under the registered error bound.

This is a one-sided falsification certificate: it can reject an underspecified shared-coordinate dimension without requiring exact rank estimation.

## Corollary 1a — certified lower bound on hidden dimension

Define

\[
r_{\rm cert}(\varepsilon)
=
\#\{k:\lambda_k(\widehat M)>\varepsilon\}.
\]

Then

\[
\boxed{
\operatorname{rank}(M)\ge r_{\rm cert}(\varepsilon).
}
\]

Because the exact SCH theorem gives `rank(M)<=d_true`,

\[
\boxed{
d_{\rm true}\ge r_{\rm cert}(\varepsilon).}
\]

Thus the empirical curvature spectrum supplies a conservative lower bound on the number of shared phenotype dimensions required by the data.

## Theorem 2 — best rank-d approximation residual

For a PSD empirical matrix, the Eckart-Young theorem implies that the best rank-`d` approximation in operator norm has residual

\[
\boxed{
\min_{\operatorname{rank}(B)\le d}
\|\widehat M-B\|_{\rm op}
=
\lambda_{d+1}(\widehat M).
}
\]

Therefore `lambda_(d+1)` is not an arbitrary diagnostic: it is the smallest operator-norm perturbation needed to make the observed curvature compatible with rank at most `d`.

In Frobenius norm, the corresponding residual is

\[
\boxed{
\left(\sum_{k>d}\lambda_k(\widehat M)^2\right)^{1/2}.
}
\]

This gives a second, distributed lack-of-fit measure when excess dimension is spread across several weak modes.

## Relation to effective dimension

The continuous effective dimension

\[
d_{\rm eff}
=
\frac{\operatorname{tr}(M)^2}{\operatorname{tr}(M^2)}
\]

summarizes how evenly curvature is distributed among active modes. It is not a substitute for the certified rank lower bound:

- `r_cert` is a thresholded falsification quantity tied to an error guarantee;
- `d_eff` is a continuous concentration index.

Both are invariant to invertible linear reparameterization of the trait coordinate because the exact weight-curvature matrix `M` is invariant.

## Empirical consequence

A multi-function SCH generality experiment can preregister:

1. a symmetric estimate `Mhat` of negative optimized-load curvature in functional-weight space;
2. an operator-error bound `epsilon` from bootstrap, concentration bounds, or an external calibration procedure;
3. the registered shared-coordinate dimension `d`.

Then:

```text
lambda_(d+1)(Mhat) <= epsilon
    compatible with dimension d (not proof)

lambda_(d+1)(Mhat) > epsilon
    dimension d falsified under the registered error bound
```

If the focal biological model claims a single shared scalar axis, the decisive spectral check is simply whether the second curvature eigenvalue exceeds the registered estimation error.

## Claim ceiling

The certificate inherits the assumptions of the exact curvature theorem: a unique regular optimum, fixed loss families under weight perturbation, a common accessible trait coordinate and valid estimation of the optimized-load Hessian. The operator-error bound must be justified prospectively; choosing it after seeing the spectrum destroys the falsification interpretation. A failure of low rank diagnoses model inadequacy or hidden dimensions, not a historical mechanism and not PAYOFF dynamics.
