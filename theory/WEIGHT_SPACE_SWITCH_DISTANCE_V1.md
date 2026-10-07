# SCH weight-space switch-distance theorem v1

## Purpose

Quantify how much functional-demand change is required to switch from one supported compromise state to another.

The normal-cone theorem established that pairwise switch boundaries are hyperplanes in weight space. The present result adds a metric distance and an explicit shortest perturbation. This turns support robustness into a measurable quantity rather than a qualitative statement that one compromise occupies a broad or narrow weight region.

## Setup

Consider two candidate compromise states `a` and `b` with fixed loss vectors

\[
y_a,y_b\in\mathbb R^n.
\]

Define

\[
\Delta=y_b-y_a.
\]

At functional weight `w`, the weighted-value margin favoring state `a` over `b` is

\[
\boxed{
m_{a\succ b}(w)=w^\top\Delta.}
\]

Thus `a` is preferred when `m>0`, `b` is preferred when `m<0`, and their static tie boundary is

\[
\boxed{w^\top\Delta=0.}
\]

Let weight perturbations be measured by a positive-definite metric `Q`:

\[
\|\delta w\|_Q=\sqrt{\delta w^\top Q\delta w}.
\]

## Theorem 1 — unconstrained metric distance to the pairwise switch

Suppose `m=w^T Delta>0`. The minimum metric perturbation satisfying

\[
(w+\delta w)^\top\Delta=0
\]

has distance

\[
\boxed{
d_{ab,Q}(w)
=
\frac{m}{\sqrt{\Delta^\top Q^{-1}\Delta}}.}
\]

The shortest perturbation is

\[
\boxed{
\delta w^*
=-\frac{m}{\Delta^\top Q^{-1}\Delta}Q^{-1}\Delta.
}
\]

This is the standard metric projection onto the pairwise support hyperplane.

## Theorem 2 — relative-weight / simplex-constrained distance

Often functional weights are normalized:

\[
\mathbf 1^\top w=1.
\]

Admissible local perturbations must then satisfy

\[
\mathbf 1^\top\delta w=0.
\]

Let `a=1` denote the all-ones vector and define the metric-tangent component of the switch normal by

\[
\tilde\Delta
=
\Delta-
\frac{a^\top Q^{-1}\Delta}
{a^\top Q^{-1}a}
\,a.
\]

Its squared dual norm is

\[
\boxed{
s_Q^2
=
\Delta^\top Q^{-1}\Delta
-
\frac{(a^\top Q^{-1}\Delta)^2}
{a^\top Q^{-1}a}.}
\]

If `s_Q>0`, the minimum relative-weight distance to the switch is

\[
\boxed{
d_{ab,Q}^{rel}(w)=\frac{m}{s_Q}.}
\]

One shortest tangent perturbation is

\[
\boxed{
\delta w^*
=-\frac{m}{s_Q^2}Q^{-1}\tilde\Delta.
}
\]

It obeys both

\[
\mathbf1^\top\delta w^*=0
\]

and

\[
\Delta^\top\delta w^*=-m.
\]

## Corollary 2a — a pairwise switch may be unreachable by relative weighting

If

\[
s_Q=0,
\]

then the two states differ only in the common-scaling direction as seen from the normalized weight tangent space. Relative-weight changes cannot alter their weighted difference locally.

In that case the pairwise tie is either already present or cannot be reached without leaving the registered normalized-weight manifold / changing the underlying loss vectors.

## Corollary 2b — Euclidean simplex formula

For `Q=I`,

\[
s^2
=
\|\Delta\|_2^2
-
\frac{(\mathbf1^\top\Delta)^2}{n}.
\]

So only the centered component of pairwise loss difference matters for relative functional-demand switching.

## Multi-state support robustness

If state `a` is currently supported against several competitors `b`, its local metric robustness radius is

\[
\boxed{
r_a(w)=\min_{b\ne a}d_{ab,Q}^{rel}(w)}
\]

among competitors with a reachable pairwise boundary and positive current margin.

The competitor attaining the minimum is the nearest support threat in functional-weight space.

Therefore a supported compromise has two distinct properties:

```text
fitness conflict load at current w
weight-space robustness before another compromise becomes optimal
```

A state can have large current conflict but sit close to a support boundary, or small conflict while remaining robust across a broad range of functional demand.

## Theorem 3 — nearest-boundary direction is prospectively testable

The shortest perturbation predicts not just how far the switch lies, but which combination of functional demands should be changed to reach it most efficiently.

If an experiment can perturb relative weights along `delta w*`, the static model predicts a tie at the calculated metric dose. Perturbations orthogonal to the tangent switch normal have zero first-order effect on the pairwise weighted difference.

This creates a focused alternative to exhaustive multi-dimensional weight grids.

## Relation to BALANCE

This result uses the same mathematical idea as metric distance to a status boundary, but the scientific object is different:

- SCH distance: change in **functional weights** required to switch which shared compromise is supported;
- BALANCE distance: change in **environmental context** required to leave the middle-world domain.

The two distances should not be numerically compared unless their metrics are explicitly commensurate, which generally they are not.

## Empirical consequence

For a finite set of candidate supported compromises, a multi-function SCH experiment can report:

1. current pairwise weighted margins;
2. the registered functional-weight metric;
3. nearest support-boundary distance;
4. predicted shortest weight perturbation;
5. observed switch/tie under a targeted validation treatment.

This turns the normal-cone picture into a direct experimental robustness test.

## Claim ceiling

The theorem assumes fixed state loss vectors while weights change and treats support switching as a static weighted-sum problem. It does not apply when the treatment changes the loss functions, feasible phenotype set or fitness semantics. Repeated forward/reverse switches at different weights require an additional history/accessibility model and are not explained by this static distance. PAYOFF dynamics remain separate.