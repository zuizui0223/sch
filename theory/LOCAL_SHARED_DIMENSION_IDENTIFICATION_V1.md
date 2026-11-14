# SCH local shared-dimension identification theorem v1

## Purpose

Sharpen the low-rank weight-curvature result from an upper bound into an exact rank identity for the locally engaged functional-gradient subspace.

The result clarifies exactly when the dimension of a shared trait module can be identified from optimized conflict curvature.

## Setup

For a regular shared optimum in `R^d`, define

\[
C=-\nabla_w^2L^*=G^\top H^{-1}G,
\]

where

\[
G=[g_1\;\cdots\;g_n]\in\mathbb R^{d\times n},
\qquad
H\succ0.
\]

## Theorem 1 — exact rank identity

Because `H` is positive definite it has an invertible square root. Write

\[
C=(H^{-1/2}G)^\top(H^{-1/2}G).
\]

For any matrix `A`,

\[
\operatorname{rank}(A^\top A)=\operatorname{rank}(A).
\]

Since multiplication by invertible `H^{-1/2}` does not change rank,

\[
\boxed{
\operatorname{rank}(C)
=
\operatorname{rank}(G).
}
\]

Thus the curvature rank is exactly the dimension of the linear span of the active function gradients at the current shared optimum.

## Corollary 1a — exact local identification of shared dimension under spanning

If the active function gradients span the whole registered shared-trait space,

\[
\operatorname{rank}(G)=d,
\]

then

\[
\boxed{
\operatorname{rank}(-\nabla_w^2L^*)=d.
}
\]

Hence under the regular common-coordinate model and a gradient-spanning intervention set, the local shared-trait dimension is identified by the curvature rank.

## Corollary 1b — rank deficiency has a precise meaning

If

\[
\operatorname{rank}(C)=r<d,
\]

then the manipulated functions locally engage only an `r`-dimensional subspace of the registered phenotype space.

This does **not** prove the phenotype is intrinsically `r`-dimensional. It means the current function-gradient set fails to excite the remaining directions.

Thus low curvature rank can arise from either:

- a genuinely low-dimensional shared phenotype;
- a higher-dimensional phenotype with locally redundant functional gradients.

## Theorem 2 — minimum number of independent functional perturbations

To identify dimension `d` from curvature rank, at least `d` linearly independent function-gradient directions are required. Since the common scaling direction in weight space is phenotype-flat, practical identification also requires enough independently varied relative functional weights to expose those directions.

A necessary design condition is therefore

\[
\boxed{n-1\ge d}
\]

for `n` independently weighted functions under a fixed-total-weight design.

This condition is not sufficient by itself: the corresponding gradients must actually span `R^d`.

## Theorem 3 — rank stability across contexts distinguishes dimension from engagement

Suppose the registered phenotype dimension is constant across contexts but the gradient span changes. Then curvature rank may vary with context even though the phenotype dimension does not.

Conversely, if rank `d` is repeatedly recovered across sufficiently different contexts and function-weight perturbations, this supports—but does not by itself prove—the claim that the full `d`-dimensional module is functionally engaged.

Thus the universal object for comparative SCH is not a single rank estimate but the relationship

\[
\boxed{
\text{curvature rank}
=
\text{locally engaged shared-functional dimension}.
}
\]

## Empirical consequence

A many-function causal SCH experiment can prospectively test:

1. the low-rank minor constraints;
2. the recovered curvature rank `r`;
3. whether independent component-gradient estimates span the same `r`-dimensional subspace;
4. whether additional functional perturbations raise rank, indicating previously unexcited shared dimensions.

This creates a direct route from comparative statics to latent trait-dimensionality diagnostics.

## Claim ceiling

The theorem is local and requires a unique regular optimum, positive-definite combined phenotype Hessian, and functional-weight interventions that do not alter the loss families themselves. Statistical rank estimation requires uncertainty treatment. Rank identifies the active gradient span, and equals the full trait dimension only under the explicit spanning condition. PAYOFF dynamics are separate.
