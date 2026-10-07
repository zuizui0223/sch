# SCH functional-gradient Gram identification theorem v1

## Purpose

Show that the optimized conflict-curvature matrix contains not only dimensionality information, but the full pairwise geometry of function gradients after whitening by the shared-landscape curvature.

This gives SCH a geometric object that can be compared across systems even when the original trait coordinates differ.

## Setup

At a regular shared optimum, define

\[
C=-\nabla_w^2L^*=G^\top H^{-1}G,
\]

where

\[
G=[g_1\;\cdots\;g_n],
\qquad
g_i=\nabla\ell_i(z^*),
\qquad
H\succ0.
\]

Define whitened functional gradients

\[
\tilde g_i=H^{-1/2}g_i.
\]

Then

\[
\boxed{C_{ij}=\tilde g_i^\top\tilde g_j.}
\]

Thus `C` is exactly the Gram matrix of the whitened function-gradient vectors.

## Theorem 1 — pairwise gradient norms and angles are encoded in curvature

The diagonal entries satisfy

\[
\boxed{C_{ii}=\|\tilde g_i\|^2.}
\]

For nonzero gradients, define the whitened angle `phi_ij` by

\[
\cos\phi_{ij}
=
\frac{\tilde g_i^\top\tilde g_j}
{\|\tilde g_i\|\|\tilde g_j\|}.
\]

Then

\[
\boxed{
\cos\phi_{ij}
=
\frac{C_{ij}}{\sqrt{C_{ii}C_{jj}}}.
}
\]

Therefore optimized weight-curvature directly determines whether two functions locally pull the shared phenotype in aligned, orthogonal or opposed directions in the curvature-normalized phenotype geometry.

## Interpretation of signs

- `C_ij>0`: whitened function gradients point partly in the same direction;
- `C_ij=0`: they are locally orthogonal in the `H^-1` metric;
- `C_ij<0`: they oppose one another along at least one shared direction.

The scalar shared-trait case is extreme: every nonzero gradient pair has

\[
|\cos\phi_{ij}|=1.
\]

## Theorem 2 — Gram geometry is identifiable up to orthogonal transformation

A positive-semidefinite Gram matrix determines any set of generating vectors up to an orthogonal transformation on their span.

Hence if `C` is identified, the configuration

\[
\{\tilde g_i\}
\]

is identified up to a common rotation/reflection in the engaged shared-trait subspace.

This is exactly the appropriate invariance: the original phenotype axes can be relabeled or rotated without changing the functional geometry.

## Corollary 2a — comparative geometry without homologous raw coordinates

Two biological systems may use different trait coordinates but share the same normalized functional-conflict geometry if their curvature Gram matrices agree after matching function labels and scale conventions.

Thus a possible generality target is not raw trait equality, but recurrence of patterns such as:

```text
strongly opposed function pair
third function nearly orthogonal
one weakly engaged function
```

in the whitened gradient geometry.

## Theorem 3 — distances between functional pulls

The squared distance between whitened gradients is

\[
\|\tilde g_i-\tilde g_j\|^2
=
C_{ii}+C_{jj}-2C_{ij}.
\]

Therefore

\[
\boxed{
D_{ij}^2=C_{ii}+C_{jj}-2C_{ij}
}
\]

is identified from conflict curvature alone.

Large `D_ij` means the two functions exert locally different pulls after accounting for the stiffness of the shared phenotype landscape.

## Theorem 4 — centered geometry under common scaling

Because

\[
Gw=0,
\]

the weighted barycenter of whitened gradients is zero:

\[
\boxed{
\sum_iw_i\tilde g_i=0.
}
\]

Thus the active function-gradient configuration is automatically centered at the shared optimum's force-balance condition.

The shared phenotype is locally optimal precisely where the weighted functional pulls balance to zero.

## Empirical consequence

A sufficiently rich functional-weight intervention can in principle recover:

1. curvature rank -> engaged shared dimension;
2. diagonal curvature -> strength of each whitened functional pull;
3. off-diagonal curvature -> pairwise alignment/opposition;
4. Gram distances -> relative separation among functional pulls.

This turns SCH from a one-dimensional compromise story into a coordinate-invariant local geometry of multifunctional conflict.

## Claim ceiling

The geometry is local and whitened by the combined phenotype Hessian. It identifies `H^-1/2 g_i`, not the raw gradients `g_i` or the biological trait axes separately unless `H` is independently known. Statistical estimation must enforce or regularize positive-semidefinite low-rank structure rather than interpret noisy unconstrained Hessian entries literally. PAYOFF dynamics remain separate.
