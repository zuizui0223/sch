# SCH polyhedral facet-complete weight design theorem v1

## Purpose

Identify when a **finite** positive-weight experiment can reconstruct the convexified attainable-loss geometry exactly, not merely approximately.

The positive-weight dual reconstruction theorem says that every supporting weight direction contributes one half-space. The finite-net theorem quantifies approximation error for general curved boundaries. The present theorem gives the exact finite case: when the convex upper attainable set is polyhedral, one support measurement per irredundant lower facet is sufficient and, under the stated representation, necessary.

## Setup

Let

\[
U=\overline{\operatorname{conv}(Y)+\mathbb R_+^n}
\]

be a full-dimensional closed convex upper polyhedron with irredundant facet representation

\[
\boxed{
U=
\bigcap_{k=1}^q
\{y:a_k^\top y\ge b_k\},
}
\]

where every facet normal satisfies

\[
a_k\in\mathbb R_+^n\setminus\{0\}.
\]

Normalize

\[
w_k=\frac{a_k}{\|a_k\|_2}.
\]

Because the kth inequality is supporting,

\[
L^*(w_k)
=
\min_{y\in U}w_k^\top y
=
\frac{b_k}{\|a_k\|_2}.
\]

## Theorem 1 — facet-complete exact reconstruction

Measure the optimized shared loss at the q normalized facet directions

\[
W_F=\{w_1,\ldots,w_q\}.
\]

The reconstructed support intersection is

\[
\begin{aligned}
U_{W_F}
&=
\bigcap_{k=1}^q
\{y:w_k^\top y\ge L^*(w_k)\}\\
&=
\bigcap_{k=1}^q
\{y:a_k^\top y\ge b_k\}\\
&=U.
\end{aligned}
\]

Therefore

\[
\boxed{
q\text{ facet-normal weight treatments are sufficient for exact reconstruction.}
}
\]

## Theorem 2 — irredundant facet count is a lower bound

Because the facet representation is irredundant, removing any facet-defining inequality strictly enlarges the intersection.

Each exact positive-weight support measurement contributes one supporting half-space. A full-dimensional polyhedron with `q` irredundant facets cannot be represented by fewer than `q` half-spaces.

Hence any exact finite support reconstruction of this polyhedron requires at least

\[
\boxed{q}
\]

facet-defining supporting inequalities.

Thus, in the ideal polyhedral case, the minimum exact support-measurement count equals the number of irredundant lower facets.

## Corollary 2a — omitted facet gives a direct held-out failure region

If facet `k` is omitted, define

\[
U_{-k}=\bigcap_{j\ne k}\{y:a_j^\top y\ge b_j\}.
\]

Irredundancy guarantees

\[
U\subsetneq U_{-k}.
\]

Therefore there exists at least one candidate loss vector that passes every retained weight constraint but violates the omitted facet.

This supplies a natural held-out test: estimate the omitted weight after fitting the other facets and ask whether the predicted outer geometry excludes the held-out violating region.

## Corollary 2b — redundant weights add validation, not identification

Once all q facet normals have been measured exactly, any additional positive-weight measurement produces a support half-space already implied by `U`.

Such extra weights cannot change the exact reconstructed polyhedron under the model. Their role becomes:

- measurement replication;
- curvature/nonpolyhedrality diagnostics;
- context-stability checks;
- detection of an omitted facet or changing attainable-loss set.

## Example — two-function piecewise-linear trade-off

For

\[
U=
\{(y_1,y_2):
 y_1\ge0,
 y_2\ge0,
 y_1+y_2\ge1\},
\]

there are three irredundant lower facets with normals

\[
e_1,
\quad e_2,
\quad (1,1).
\]

The three corresponding weight treatments reconstruct `U` exactly.

If the `(1,1)` treatment is omitted, `(0,0)` falsely survives the remaining constraints. If the `e_1` facet is omitted, points with negative first-coordinate loss can falsely survive the other two constraints.

## Relation to finite-net theory

There are now two finite-design regimes:

1. **polyhedral exact regime** — one treatment per irredundant facet gives zero support error;
2. **general curved regime** — a finite `delta`-net gives a quantitative support-slack bound but exact recovery generally requires infinitely many directions.

This makes the geometry itself determine the experimental burden.

## Empirical consequence

If a multi-function system is plausibly piecewise-linear/polyhedral after convexification, the theory suggests an adaptive strategy:

1. estimate candidate facet normals from pilot/support data;
2. prospectively register the candidate irredundant facets;
3. measure one optimized treatment per facet normal;
4. reserve extra/intermediate weights as held-out tests of polyhedrality;
5. reject the finite-facet model if held-out support values cut the reconstructed region.

## Claim ceiling

Exact finite reconstruction requires the convex upper attainable set itself to be polyhedral over the declared loss domain, all relevant lower facets to have admissible nonnegative normals, and support values to be known on a common matched loss scale. Biological attainable geometry can be nonpolyhedral or nonstationary, in which case the finite-net approximation theorem rather than the exact facet count applies. PAYOFF dynamics remain separate.
