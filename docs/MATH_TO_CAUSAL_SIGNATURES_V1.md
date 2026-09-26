# SCH math -> causal signatures v1

## Purpose

Freeze the experimentally testable consequences of the current SCH mathematics. A biological system is not promoted because it merely resembles a compromise. The causal programme must reproduce registered responses to selective functional-weight interventions.

## Signature S1 — directional optimum response

For function `j`,

\[
\frac{\partial z^*}{\partial\log w_j}
=-H^{-1}w_jg_j
\]

in the multidimensional form. In the scalar strict-convex case the sign must point toward function `j`'s optimum.

**Test:** selectively strengthen function `j` while holding the trait coordinate and other loss families fixed enough for the registered local model.

**Failure:** optimum moves robustly opposite the predicted direction.

## Signature S2 — common weight scaling does not move the optimum

A proportional multiplication of all functional weights leaves the optimized shared phenotype unchanged.

**Test:** where a common multiplicative intensity manipulation is biologically meaningful, separate total fitness-scale change from relative-weight change.

**Failure:** common scaling systematically moves `z*` after accounting for changes in the loss families themselves.

## Signature S3 — cross-weight reciprocity

Optimized residual losses obey

\[
\frac{\partial r_i}{\partial w_j}
=
\frac{\partial r_j}{\partial w_i}.
\]

For multiplicative weight manipulations use the corresponding scaled log-weight relation.

**Test:** independently perturb functions `i` and `j` in both directions and estimate reciprocal cross-responses.

**Failure:** the two cross-effects differ beyond a preregistered equivalence tolerance under a context in which the same smooth optimum branch should apply.

## Signature S4 — low-rank curvature

Let

\[
C=-\nabla_w^2L^*.
\]

A registered `d`-dimensional shared phenotype predicts

\[
\operatorname{rank}C\le d,
\]

so all `(d+1)x(d+1)` minors vanish in the population model.

**Test:** use at least `d+1` independent relative functional-weight contrasts and estimate the curvature matrix with uncertainty.

**Failure:** robust effective rank above the registered shared-trait dimension.

## Signature S5 — functional-pull Gram geometry

The same curvature matrix is the Gram matrix of whitened functional gradients:

\[
C_{ij}=\tilde g_i^T\tilde g_j.
\]

Therefore

\[
\cos\phi_{ij}=C_{ij}/\sqrt{C_{ii}C_{jj}}.
\]

**Test:** compare the curvature-derived functional alignment/opposition pattern with independent component-surface gradient estimates when available.

**Failure:** the inferred Gram geometry and independently measured component geometry are incompatible after accounting for uncertainty and the shared Hessian metric.

## Signature S6 — worst-case binding support

For a shared coordinate in `R^d`, the global minimax conflict has a certificate using at most `d+1` binding functions.

**Test:** in a many-function system, identify the functions whose residual losses bind at the experimentally approximated minimax weighting.

**Failure:** no subset of at most `d+1` functions can satisfy the registered minimax/KKT balance under the assumed `d`-dimensional common coordinate.

## Signature S7 — curvature-nullspace weight balance

The current functional-weight vector must satisfy

\[
\boxed{Cw=0.}
\]

because the shared optimum force-balance condition gives `Gw=0` and `C=G^T H^-1 G`.

**Test:** register an independently calibrated relative-weight vector `w_0`, estimate `C` from graded weight perturbations, and evaluate a prospective residual norm such as

\[
T_w=\|\widehat C w_0\|.
\]

**Failure:** the residual remains larger than the preregistered curvature/weight uncertainty. This is a direct audit of the common-coordinate/fixed-loss-family model.

If `ker(C)` is one-dimensional and its unique direction is strictly positive, normalize that null vector to sum to one and compare it with independently measured relative functional weights. Under this condition the theory predicts that relative weights are identifiable from curvature geometry itself.

If nullity exceeds one, the correct conclusion is **weight underidentification from curvature**, not an arbitrary selected weight vector.

## Signature S8 — three-level weight-chord curvature gap

For a preregistered weight chord

\[
w_t=(1-t)w_0+t w_1,
\]

let `v=w_1-w_0` and suppose the directional conflict curvature satisfies

\[
\alpha\le v^TC(w_t)v\le\beta
\]

throughout the chord. Then the optimized conflict-load bulge above endpoint interpolation obeys

\[
\boxed{
\frac{\alpha}{2}t(1-t)
\le
L^*(w_t)-[(1-t)L^*(w_0)+tL^*(w_1)]
\le
\frac{\beta}{2}t(1-t).
}
\]

**Test:** use two calibrated endpoint weight regimes plus a preregistered midpoint/interior regime. At `t=1/2`, the bulge must lie in `[alpha/8,beta/8]` when the curvature bounds are directional; include the registered metric factor when matrix bounds are used.

**Failure:** a negative bulge rejects concavity; a bulge outside the registered interval rejects the corresponding curvature bound or common smooth optimum branch.

This is useful even when only one independent P/G weight-transfer direction is experimentally available, because it tests integrated curvature without pretending to recover a full multidimensional Hessian.

## Pedicularis use

The current focal `z x P x G` surface directly addresses S1 for two functional weights and the positive conflict load. S3-S8 require additional independently varied functional demands or replicated graded P/G intensities; they are stronger extensions, not hidden requirements for the first two-function causal receipt.

For exactly two functions on one shared axis, S7 is in principle identifiable because a rank-one `2 x 2` curvature matrix has a one-dimensional nullspace. In practice this requires enough graded P/G weighting information to estimate the curvature robustly. S8 is a lower-burden extension: three calibrated weight levels along one relative-weight direction are enough for the finite-difference curvature audit.

## Promotion rule

A positive SCH causal claim requires the primary registered surface and conflict load. The higher-order signatures strengthen the claim from **one detected conflict** toward a general shared-coordinate mechanism. They must never be inferred merely from observational covariation.

PAYOFF invasion/coexistence remains outside this document.
