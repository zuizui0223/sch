# SCH weight-polytope vertex certificate v1

## Purpose

Use concavity of the optimized shared-axis conflict value to certify an entire convex region of functional-weight uncertainty from finitely many extreme weight combinations.

This is the high-dimensional analogue of the one-dimensional chord result: if the admissible weight set is a polytope, the smallest optimized conflict over that whole set occurs at a vertex.

## Setup

Let

\[
L^*(w)=\min_z\sum_i w_i\ell_i(z)
\]

for nonnegative functional weights `w` in a declared convex weight domain. As established previously, `L*` is concave in `w` because it is the pointwise minimum of linear functions of `w`.

Let the admissible functional-weight uncertainty set be a compact polytope

\[
\mathcal W=\operatorname{conv}\{v_1,\ldots,v_M\}.
\]

Weights may be normalized to a simplex or may live in another affine slice; only convexity of the declared set is needed.

## Theorem 1 — minimum optimized conflict occurs at a weight-polytope vertex

Every `w in W` can be written

\[
w=\sum_{j=1}^M\alpha_jv_j,
\qquad
\alpha_j\ge0,
\qquad
\sum_j\alpha_j=1.
\]

Concavity gives

\[
L^*(w)
\ge
\sum_j\alpha_jL^*(v_j)
\ge
\min_jL^*(v_j).
\]

Because every vertex itself belongs to `W`,

\[
\boxed{
\min_{w\in\mathcal W}L^*(w)
=
\min_{v\in\operatorname{Vert}(\mathcal W)}L^*(v).
}
\]

Thus no hidden interior functional-weight combination can have lower optimized conflict than all registered extreme combinations.

## Corollary 1a — robust positive-conflict certificate

If every vertex satisfies

\[
L^*(v_j)\ge\delta>0,
\]

then every admissible weight vector satisfies

\[
\boxed{L^*(w)\ge\delta\quad\forall w\in\mathcal W.}
\]

So positive shared-axis conflict is certified over the entire declared weight uncertainty region by a finite set of vertex experiments.

This is stronger than checking a few interior weights without geometric coverage.

## Corollary 1b — interval-valued vertex receipts

If each vertex value is only partially identified,

\[
L^*(v_j)\in[L_j^-,L_j^+],
\]

then

\[
\boxed{
\inf_{w\in\mathcal W}L^*(w)
\ge
\min_jL_j^-.
}
\]

Hence a strictly positive minimum lower endpoint gives a fail-closed robust-conflict certificate across the entire polytope.

## Theorem 2 — interior low values falsify the registered static concavity model

Suppose all vertex values are estimated on one common fitness scale and a directly measured interior weight `w` yields

\[
L^*(w)<\sum_j\alpha_jL^*(v_j)
\]

for a known convex representation

\[
w=\sum_j\alpha_jv_j,
\]

beyond uncertainty. This violates concavity of the registered static value function.

At least one assumption must fail:

- functional weights changed the component-loss families rather than only their coefficients;
- feasible shared phenotypes changed across treatments;
- contexts or fitness scales were mismatched;
- the reported optimized values were not comparable maxima/minima of the same shared-coordinate problem.

This turns interior validation points into a direct model audit rather than additional vertices needed for the certificate.

## Corollary 2a — experimental division of labor

A prospective SCH design can separate contexts into:

```text
vertex treatments     -> certify the full admissible weight region
interior hold-outs    -> test concavity / common-model validity
```

For a simplex of `n` normalized weight coordinates, the naive vertices correspond to extreme functional emphasis. Biological restrictions can instead define a smaller feasible weight polytope whose vertices remain experimentally meaningful.

## Relation to the minimax result

The weight-simplex minimax theorem asks where **maximum** unavoidable conflict occurs over weights. A concave function can attain that maximum in the interior.

The present theorem asks where **minimum** conflict occurs over a convex uncertainty region. Concavity forces that minimum to the boundary and, for a polytope, to a vertex.

Therefore the two results are complementary:

```text
maximum conflict over weights   -> potentially interior minimax weighting
minimum conflict over polytope  -> vertex certificate
```

## Empirical consequence

If environmental or ecological uncertainty changes relative functional demands within a registered convex range, Chapter 1 need not densely sample every possible weighting to establish persistent shared conflict. Measuring all admissible vertices on the same causal fitness scale is mathematically sufficient under the static SCH model.

An interior treatment is then most valuable as a held-out test of the concavity prediction.

## Claim ceiling

The certificate concerns the optimized static conflict value `L*`, not an arbitrary empirical proxy. It requires a common feasible phenotype set and fixed loss families while weights vary. If treatments alter component functions, accessibility or fitness semantics, vertex interpolation is invalid. It does not establish population dynamics or PAYOFF stability.