# SCH exposed-phenotype identification theorem v1

## Purpose

Close the gap between what a positive functional-weight sweep identifies in loss space and when that information is sufficient to identify the optimized shared phenotype itself.

The observational-equivalence theorem established that complete positive-weight data identify the convex upper attainable loss geometry, not a unique latent phenotype map. This result gives a sharp sufficient condition for recovering phenotype identity at a supported regular optimum.

## Setup

Let the shared phenotype be `z` in a registered phenotype domain `Z`, with functional-loss map

\[
y:Z\to\mathbb R^n,
\qquad
y(z)=(\ell_1(z),\ldots,\ell_n(z)).
\]

For positive weights `w`, define

\[
V(w)=\min_{z\in Z} w^\top y(z).
\]

Assume `V` is differentiable at the focal weight `w` and the minimizing loss vector is unique.

## Theorem 1 — exposed loss vector is identified by the value-function gradient

By the envelope theorem / support-function result,

\[
\boxed{\nabla_w V(w)=y(z^*(w)).}
\]

Thus a sufficiently smooth local weight-response surface identifies the complete functional-loss vector of the optimized shared phenotype.

This statement is coordinate-free in phenotype space: it identifies the point in **loss space** even if the biological parameterization of `z` is changed.

## Theorem 2 — phenotype identification under an injective loss map

Suppose the registered loss map `y(z)` is injective on a set `Z_0` known to contain the optimizer.

Then the exposed loss vector uniquely determines the phenotype:

\[
\boxed{
z^*(w)=y^{-1}(\nabla_wV(w)).
}
\]

Therefore complete local weight-response information plus a known injective phenotype-to-loss map is sufficient for local optimized-phenotype identification.

## Corollary 2a — known inverse on a restricted biological branch is enough

Global injectivity is not necessary. If biology independently restricts the optimizer to a branch `Z_0` on which `y` is one-to-one, the same inverse result holds on that branch.

This is relevant when a physical trait coordinate has symmetries or repeated loss vectors globally but only one branch is developmentally accessible.

## Theorem 3 — noninjective loss maps preserve phenotype non-identifiability

If two distinct phenotypes satisfy

\[
z_a\neq z_b,
\qquad
y(z_a)=y(z_b),
\]

then no experiment whose observable is only the optimized functional-loss vector can distinguish `z_a` from `z_b` at that loss point.

Even exact knowledge of

\[
V(w),\quad \nabla V(w),\quad \nabla^2V(w)
\]

cannot resolve phenotype identity solely through the loss map if both phenotypes generate the same local loss-space observables.

Direct phenotype measurement or an additional phenotype-sensitive observable is required.

## Example — two quadratic functions

Let

\[
\ell_1(z)=z^2,
\qquad
\ell_2(z)=(z-2)^2.
\]

Then

\[
z^*(w)=\frac{2w_2}{w_1+w_2}
\]

and

\[
V(w)=\frac{4w_1w_2}{w_1+w_2}.
\]

Its gradient is

\[
\frac{\partial V}{\partial w_1}
=\left(z^*\right)^2,
\qquad
\frac{\partial V}{\partial w_2}
=\left(z^*-2\right)^2,
\]

exactly the two functional losses.

Moreover

\[
\ell_1(z)-\ell_2(z)=4z-4,
\]

so the pair of losses is injective in `z` and

\[
\boxed{
z^*=\frac{\ell_1-\ell_2+4}{4}.}
\]

Thus the optimizer can be reconstructed from the gradient of the weight-value function in this registered model.

## Theory -> causal bridge

This result separates two experimental roles:

```text
weight perturbation response
    -> identifies exposed functional-loss vector
trait calibration / direct phenotype measurement
    -> establishes or tests the phenotype-to-loss map
both together, when injective
    -> identify optimized shared phenotype
```

So a weight sweep can become genuinely phenotype-identifying, but only after the causal programme supplies the map linking phenotype to component losses.

## Falsifiable implication

If a registered injective loss map predicts

\[
z_{pred}=y^{-1}(\nabla V(w))
\]

but the directly measured optimized phenotype differs beyond uncertainty, at least one assumption fails: the value surface is not static, the gradient estimate is wrong, the loss map changed with weights, or the registered common-coordinate model is inadequate.

## Claim ceiling

The result is local to weights where the value function has a unique exposed loss vector and requires a validated injective loss map on the admissible phenotype set. It identifies the current optimized phenotype, not historical evolution or population dynamics. PAYOFF remains separate.