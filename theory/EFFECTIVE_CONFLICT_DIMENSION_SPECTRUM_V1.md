# SCH effective conflict-dimension spectrum v1

## Purpose

Turn the exact low-rank weight-curvature theorem into a continuous, coordinate-invariant dimension diagnostic that is less brittle than a hard numerical rank cutoff.

The d-dimensional SCH theorem gives the positive-semidefinite weight-curvature matrix

\[
M
:=-\nabla_w^2L^*
=G^\top H^{-1}G
\succeq0,
\]

with

\[
\operatorname{rank}(M)\le d.
\]

When `M` is estimated with uncertainty, deciding whether a small eigenvalue is exactly zero can be unstable. The present result uses the spectrum continuously.

## Setup

Let the positive eigenvalues of `M` be

\[
\lambda_1,\ldots,\lambda_r>0,
\qquad r=\operatorname{rank}(M).
\]

Define the effective conflict dimension

\[
\boxed{
 d_{\rm eff}
 =
 \frac{(\sum_{a=1}^r\lambda_a)^2}
 {\sum_{a=1}^r\lambda_a^2}
}
\]

when `M` is nonzero, and define `d_eff=0` when `M=0`.

This is the participation ratio of the nonzero weight-curvature spectrum.

## Theorem 1 — effective dimension is bounded by true curvature rank

Cauchy-Schwarz gives

\[
\left(\sum_{a=1}^r\lambda_a\right)^2
\le
r\sum_{a=1}^r\lambda_a^2.
\]

Therefore

\[
\boxed{
1\le d_{\rm eff}\le r\le d
}
\]

for nonzero curvature.

Hence, under the exact registered SCH model,

\[
\boxed{
 d\ge\lceil d_{\rm eff}\rceil.
}
\]

A measured effective dimension above one therefore rules out a genuinely one-dimensional shared-coordinate model, provided estimation uncertainty cannot account for the excess.

## Corollary 1a — equality condition

The upper equality

\[
d_{\rm eff}=r
\]

holds exactly when all nonzero eigenvalues are equal.

Thus `d_eff` is close to rank when conflict curvature is spread evenly across the engaged trait directions, but falls toward one when a single direction dominates the response.

This distinguishes:

```text
number of mathematically engaged directions   rank(M)
how evenly conflict curvature occupies them   d_eff
```

## Theorem 2 — no eigendecomposition is required

Because `M` is symmetric,

\[
\operatorname{tr}(M)=\sum_a\lambda_a
\]

and

\[
\operatorname{tr}(M^2)
=\sum_a\lambda_a^2
=\sum_{i,j}M_{ij}^2.
\]

Therefore

\[
\boxed{
 d_{\rm eff}
 =
 \frac{\operatorname{tr}(M)^2}
 {\operatorname{tr}(M^2)}
}
\]

for `M!=0`.

The diagnostic can be computed directly from the fitted weight-curvature matrix.

## Corollary 2a — coordinate invariance

The trait-coordinate invariance theorem showed that `M` itself is unchanged under every invertible linear reparameterization of the shared phenotype coordinate.

Therefore its eigenvalues, rank, trace, Frobenius norm and

\[
\boxed{d_{\rm eff}}
\]

are all exactly invariant to such trait-coordinate changes.

## Theorem 3 — whitened-gradient interpretation

Let

\[
U=H^{-1/2}G.
\]

Then

\[
M=U^\top U.
\]

The nonzero eigenvalues of `M` equal the nonzero eigenvalues of

\[
UU^\top.
\]

Hence `d_eff` measures the effective dimensionality of the function-gradient cloud after whitening by the curvature of the combined shared-fitness landscape.

It is not simply the number of measured traits. It is the number of trait directions that are **functionally engaged in the local conflict geometry**.

## Empirical consequence

For a multi-function experiment with enough independent demand perturbations to estimate `M`, SCH can preregister:

1. exact low-rank/minor tests for a proposed integer dimension `d`;
2. `d_eff` as a continuous descriptive diagnostic;
3. uncertainty intervals for `d_eff` from bootstrap or posterior draws of `M`.

A useful pattern is:

```text
hard rank uncertain because of small eigenvalues
but d_eff robustly > 1
```

which provides evidence against a single engaged conflict direction without requiring a brittle zero-eigenvalue decision.

## Claim ceiling

For a noisy empirical matrix that is not exactly positive semidefinite, `d_eff` should not be computed after silently discarding negative eigenvalues. The estimation model, PSD projection if any, and uncertainty propagation must be registered. `d_eff` is a local functional-conflict dimension under the shared-coordinate model, not a count of historical genetic modules or PAYOFF strategies.
