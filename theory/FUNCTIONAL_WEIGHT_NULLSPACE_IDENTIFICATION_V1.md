# SCH functional-weight nullspace identification theorem v1

## Purpose

Turn the weight-curvature identity into an additional identifiability result. At a regular shared optimum, the current functional weight vector is not arbitrary relative to the curvature Gram matrix: it must lie in its nullspace.

This creates both a model-consistency test and, in a sufficiently rich geometry, a route to recover relative functional weights from optimized conflict curvature alone.

## Setup

Let

\[
L^*(w)=\min_z\sum_{i=1}^n w_i\ell_i(z),
\qquad w_i>0,
\]

with shared phenotype `z in R^d`, unique regular optimum `z*(w)`, positive-definite combined phenotype Hessian

\[
H=\sum_iw_i\nabla^2\ell_i(z^*)\succ0,
\]

and function-gradient matrix

\[
G=[g_1\;\cdots\;g_n],
\qquad g_i=\nabla\ell_i(z^*).
\]

The optimized conflict-curvature matrix is

\[
C=-\nabla_w^2L^*=G^\top H^{-1}G\succeq0.
\]

The shared-optimum first-order condition is

\[
Gw=\sum_iw_ig_i=0.
\]

## Theorem 1 — current functional weights lie in the curvature nullspace

Multiplying the curvature matrix by the functional-weight vector gives

\[
Cw
=G^\top H^{-1}Gw
=0.
\]

Therefore

\[
\boxed{w\in\ker(C).}
\]

This is an exact local signature under the registered model.

An independently specified functional-weight vector and an estimated curvature matrix must therefore satisfy `C w = 0` up to statistical error.

## Corollary 1a — relative-weight identification when the nullspace is one-dimensional

If

\[
\operatorname{rank}(C)=n-1,
\]

then

\[
\dim\ker(C)=1.
\]

Because the biological weight vector is strictly positive, the unique positive null direction identifies the relative functional weights up to common scale. Under the normalization

\[
\sum_iw_i=1,
\]

we obtain a unique relative-weight vector.

Thus

\[
\boxed{
\operatorname{rank}(C)=n-1
\Rightarrow
\text{relative }w\text{ is identifiable from }C
}
\]

provided the one-dimensional nullspace contains a strictly positive vector.

## Corollary 1b — underidentification when nullity exceeds one

If

\[
\dim\ker(C)>1,
\]

then curvature alone generally does not identify the current functional weights. Multiple weight vectors can satisfy the force-balance constraint encoded by `C`.

Additional information is then required, for example direct functional-weight manipulation or independent component-fitness calibration.

The scalar shared-trait case illustrates this boundary. Since `rank(C)<=1`, more than two functions usually imply a multidimensional nullspace and hence weight underidentification from curvature alone.

## Theorem 2 — rank requirement for weight recovery

The earlier shared-dimension theorem gives

\[
\operatorname{rank}(C)\le d.
\]

For one-dimensional nullspace identification we need `rank(C)=n-1`, so necessarily

\[
\boxed{d\ge n-1.}
\]

Hence recovering all relative functional weights from curvature requires a shared phenotype space rich enough to support `n-1` independent functional-pull directions.

This is distinct from the `d+1` binding-support theorem: one result concerns a sparse worst-case conflict certificate; the present result concerns local recovery of the actual weight balance.

## Theorem 3 — curvature-balance residual as a falsification statistic

Given an estimated curvature matrix `C_hat` and an independently registered normalized weight vector `w_0`, define

\[
r_w=C_{\rm hat}w_0.
\]

Under the exact theory `r_w=0`. A norm such as

\[
\boxed{T_w=\|C_{\rm hat}w_0\|}
\]

is therefore a direct model-checking statistic.

A nonzero residual beyond prospective curvature/weight uncertainty can indicate:

- the functional weights were misspecified;
- the curvature matrix was poorly estimated;
- functional weighting changes the loss families themselves;
- the registered shared coordinate omits moving phenotype dimensions;
- the system is not at the assumed regular shared optimum.

## Empirical consequence

A rich weight-perturbation experiment can now target three nested SCH objects:

1. `rank(C)` -> lower bound on engaged shared phenotype dimension;
2. Gram geometry of functional pulls -> alignment/opposition among functions;
3. `ker(C)` -> force-balance constraints and, when nullity is one, relative functional weights themselves.

For two functions on one shared axis, the curvature matrix can in principle identify the relative weight ratio from its positive null vector. For many functions on a low-dimensional shared trait, the nullspace is intentionally larger and curvature alone should not be overinterpreted as identifying all weights.

## Claim ceiling

The result is local and requires a regular optimum, fixed loss families and the exact optimized-weight curvature identity. Statistical nullspace estimation is sensitive to noise; approximate zero eigenvalues must be handled with prospective error bounds rather than hard algebraic rank calls. The theorem identifies relative functional weights only when the positive null direction is unique. It does not identify historical selection or PAYOFF dynamics.
