# SCH low-rank weight-curvature identities v1

## Purpose

Turn the d-dimensional weight-curvature theorem into directly falsifiable algebraic signatures.

Let

\[
C(w)=-\nabla_w^2L^*(w)=G^\top H^{-1}G\succeq0
\]

for a shared phenotype coordinate of registered dimension `d`. The previous theorem gives

\[
\operatorname{rank}C\le d.
\]

## Theorem 1 — vanishing minors

Every square minor of `C` of order larger than `d` must vanish. In particular, for any index sets `I,J` with

\[
|I|=|J|=d+1,
\]

we have

\[
\boxed{\det C_{I,J}=0.}
\]

For symmetric principal minors this becomes

\[
\boxed{\det C_{I,I}=0.}
\]

for every `d+1` chosen functional-weight coordinates.

Thus a registered `d`-dimensional common trait predicts polynomial equality constraints on the empirical weight-response curvature matrix.

## Corollary 1a — scalar shared trait

For `d=1`, every 2x2 minor vanishes. Hence for all functions `i,j`,

\[
\boxed{C_{ij}^2=C_{ii}C_{jj}.}
\]

Whenever diagonal terms are positive, the absolute curvature correlation is exactly one:

\[
\frac{|C_{ij}|}{\sqrt{C_{ii}C_{jj}}}=1.
\]

The signs depend on the orientation of the function gradients, but the rank-one magnitude identity does not.

## Theorem 2 — relative-weight nullity

The full weight space has dimension `n`. Since `rank C<=d`,

\[
\dim\ker C\ge n-d.
\]

The common scaling direction `w` is always in the kernel because the first-order condition gives `Gw=0`.

Restrict now to the local fixed-total-weight tangent space

\[
T=\{v:\mathbf1^\top v=0\},
\]

which has dimension `n-1`. The restriction of `C` to `T` still has rank at most `d`, so

\[
\boxed{\dim\ker(C|_T)\ge n-1-d.}
\]

Therefore when the number of manipulated functional demands greatly exceeds the shared-trait dimension, many independent relative-weight perturbations must be second-order flat through phenotype re-optimization.

## Theorem 3 — rank gives a lower bound on hidden shared dimension

If an empirically identified curvature matrix has stable rank `r` after uncertainty and measurement-error correction, any regular common-coordinate SCH model explaining that curvature must satisfy

\[
\boxed{d\ge r.}
\]

This is a one-sided dimension diagnostic. Observing rank 3 falsifies a genuinely scalar or two-dimensional registered shared phenotype model under the theorem assumptions.

The converse does not hold: rank smaller than `d` may arise because function gradients span only a lower-dimensional subspace at the sampled context.

## Empirical consequence

A many-function SCH experiment can estimate local curvature of optimized conflict with respect to controlled relative demands. The theory then predicts a hierarchy:

```text
registered d=1  -> all 2x2 minors vanish
registered d=2  -> all 3x3 minors vanish
registered d=3  -> all 4x4 minors vanish
...
```

This supplies a stronger universal signature than merely observing an intermediate optimum.

## Claim ceiling

These identities require the same regularity assumptions as the d-dimensional weight-curvature theorem: unique local optimum, fixed loss families under weight manipulation, and positive-definite phenotype Hessian. Estimated nonzero minors can also arise from sampling noise, so empirical use requires uncertainty-aware rank testing rather than literal point-estimate determinants. PAYOFF dynamics are unrelated.
