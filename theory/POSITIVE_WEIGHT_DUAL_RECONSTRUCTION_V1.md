# SCH positive-weight dual reconstruction theorem v1

## Purpose

Turn the optimized shared-conflict value function

\[
L^*(w)=\min_z\sum_{i=1}^n w_i\ell_i(z)
\]

into a geometric identification result. The theorem states exactly what a sufficiently rich sweep over positive functional weights can reconstruct about the attainable multi-function loss set, and what it can never reconstruct without additional assumptions.

## Setup

Let the attainable loss vectors be

\[
Y=\{\ell(z)=(\ell_1(z),\ldots,\ell_n(z)):z\in Z\}\subset\mathbb R^n.
\]

Assume `Y` is nonempty and compact. Define the closed convex upper hull

\[
U=\overline{\operatorname{conv}(Y)+\mathbb R_+^n}.
\]

For every nonzero positive weight vector `w>=0`, define

\[
L^*(w)=\min_{y\in Y}w^\top y.
\]

## Theorem 1 — convex-upper-hull invariance

For every `w>=0`,

\[
\boxed{L^*(w)=\min_{u\in U}w^\top u.}
\]

Adding a nonnegative vector cannot lower a positive-weight linear functional, and taking a convex hull does not change its minimum. Therefore positive-weight optimization depends only on `U`, not on the detailed nonconvex shape of `Y`.

## Theorem 2 — exact half-space reconstruction

The closed convex upper hull is recovered from the complete positive-weight value function by

\[
\boxed{
U=
\bigcap_{w\in\mathbb R_+^n\setminus\{0\}}
\{y:w^\top y\ge L^*(w)\}.
}
\]

### Proof sketch

Every `u in U` satisfies every inequality by Theorem 1.

Conversely, take `y notin U`. Since `U` is closed and convex, a strict separating hyperplane exists. Because `U+R_+^n=U`, any separating normal with a negative component would make the infimum over `U` equal to minus infinity along the corresponding positive recession direction. Hence a valid separating normal can be chosen in `R_+^n`. That positive normal produces a weight vector `w` with

\[
w^\top y<L^*(w),
\]

so `y` is excluded from the intersection.

## Corollary 2a — finite weight sweeps give an outer approximation

For a finite registered set of functional weights `W`, define

\[
U_W=\bigcap_{w\in W}\{y:w^\top y\ge L^*(w)\}.
\]

Then

\[
\boxed{U\subseteq U_W.}
\]

If `W_1 subset W_2`,

\[
\boxed{U_{W_2}\subseteq U_{W_1}.}
\]

Thus every additional weight treatment can only shrink the admissible convexified loss region. Weight-sweep design becomes a prospective geometric refinement problem.

## Corollary 2b — unsupported nonconvex Pareto structure is not identified

If two attainable sets `Y_1` and `Y_2` have the same closed convex upper hull, then

\[
L_1^*(w)=L_2^*(w)
\quad\text{for every }w\ge0.
\]

Therefore positive weighted-sum experiments cannot distinguish unsupported nonconvex Pareto segments that disappear under convexification.

This sharpens the existing supported-Pareto result:

- positive weights identify supported compromises and the convexified upper attainable set;
- they do **not** identify every biologically attainable efficient phenotype when the attainable loss set is nonconvex.

## Corollary 2c — a direct model falsifier

Suppose a registered collection of weight experiments estimates `L*(w)` and an independently observed phenotype produces loss vector `y_obs`. If

\[
w^\top y_{obs}<L^*(w)
\]

for any correctly matched registered weight `w`, then the observation is incompatible with the claimed common attainable-loss set and value function, beyond uncertainty.

## Empirical interpretation

The theory changes the role of a multi-function weight sweep. It is not only a collection of optimum-shift tests. It incrementally reconstructs the convexified feasible trade-off geometry by supporting half-spaces.

A practical sequence is:

1. choose a prospectively registered set of positive functional weights;
2. estimate the optimized shared fitness/loss at each weight;
3. form the half-space outer approximation `U_W`;
4. add strategically chosen weights where the current outer approximation is widest;
5. reserve independently observed loss vectors as held-out feasibility checks.

## Relation to Chapter-1 universality

Across systems, the universal object can now be compared at three nested levels:

1. optimum shifts under reweighting;
2. low-rank local curvature of `L*(w)`;
3. global convexified attainable-loss geometry reconstructed from positive-weight support values.

Systems may share level 1 while differing at levels 2 or 3.

## Claim ceiling

The exact reconstruction is of the **closed convex upper hull**, not the raw attainable set. It assumes a common attainable phenotype/loss set while functional weights vary and matched loss semantics across the sweep. Positive-weight data alone cannot recover unsupported nonconvex Pareto structure, historical accessibility, or PAYOFF population dynamics.
