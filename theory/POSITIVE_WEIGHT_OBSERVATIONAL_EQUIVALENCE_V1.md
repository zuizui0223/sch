# SCH positive-weight observational-equivalence theorem v1

## Purpose

State exactly what can and cannot be identified from an arbitrarily rich set of positive functional-weight experiments.

The existing positive-weight dual-reconstruction result shows that the optimized value function reconstructs the closed convex upper attainable loss set. The present result turns that statement into an **observational-equivalence theorem** and separates three objects:

1. the positive-weight value function;
2. the convex upper attainable loss geometry identified by that value function;
3. the underlying nonconvex phenotype-to-loss map, which need not be identified.

## Setup

Let `Y` be the attainable functional-loss set in `R^n`, with losses oriented so smaller is better. For strictly positive functional weights

\[
w\in\mathbb R_{++}^n,
\]

define the optimized shared-axis value function

\[
V_Y(w)=\inf_{y\in Y} w^\top y.
\]

Define the closed convex upper completion

\[
U_Y
=\operatorname{cl}\bigl(\operatorname{conv}(Y)+\mathbb R_+^n\bigr).
\]

Assume the regularity conditions already registered for positive-weight dual reconstruction, so that

\[
U_Y
=\bigcap_{w>0}
\{y:w^\top y\ge V_Y(w)\}.
\]

## Theorem 1 — complete positive-weight observational equivalence

For two attainable loss sets `Y` and `Z`, the following are equivalent:

\[
\boxed{
V_Y(w)=V_Z(w)
\quad\text{for every }w\in\mathbb R_{++}^n
}
\]

and

\[
\boxed{
U_Y=U_Z.
}
\]

### Proof

If the value functions are equal for every positive weight, their support-half-space intersections are identical, hence `U_Y=U_Z` by the dual-reconstruction theorem.

Conversely, replacing `Y` by its convex upper completion does not change any positive-weight infimum. Therefore equal convex upper completions imply identical positive-weight value functions.

Thus the complete positive-weight experiment identifies an **equivalence class** of latent attainable sets: all sets having the same closed convex upper completion.

## Corollary 1a — unsupported nonconvex structure is observationally silent

If `Y` and `Z` differ only by phenotype states that do not alter

\[
\operatorname{cl}(\operatorname{conv}(Y)+\mathbb R_+^n),
\]

then no positive weighted-sum experiment can distinguish them, even with infinitely many noiseless weight treatments.

This includes hidden nonconvex dents, unsupported Pareto states and redundant dominated states that do not change the convex upper completion.

Therefore failure to recover such states is a structural non-identifiability, not merely a sampling problem.

## Theorem 2 — exposed loss vector from the derivative of the value function

Suppose `U_Y` is closed and convex and `V_Y` is differentiable at a positive weight `w`.

Let

\[
F(w)=\operatorname*{arg\,min}_{y\in U_Y}w^\top y
\]

be the exposed minimizing face.

For the concave value function `V_Y`, the superdifferential at `w` equals the exposed face:

\[
\partial^+V_Y(w)=F(w).
\]

Hence differentiability implies that the exposed face is a singleton and

\[
\boxed{
\nabla_w V_Y(w)=y^*(w),
}
\]

where `y*(w)` is the unique exposed optimized loss vector.

So a sufficiently smooth weight-response surface identifies the **optimized functional-loss vector** at that weight directly from the value-function gradient.

## Corollary 2a — nondifferentiability identifies a face, not a unique phenotype

At a weight where several distinct loss vectors tie,

\[
F(w)
\]

contains more than one point and `V_Y` is generally nondifferentiable.

The observable object is then the exposed face or its uncertainty set, not a unique causal phenotype state.

A switch in optimized phenotype can therefore appear as a kink in weight space while the value function remains continuous.

## Theorem 3 — finite weight designs identify only an outer set

For a finite registered design

\[
W_m=\{w_1,\ldots,w_m\},
\]

define

\[
P_m
=\bigcap_{k=1}^m
\{y:w_k^\top y\ge V_Y(w_k)\}.
\]

Then

\[
\boxed{
U_Y\subseteq P_m.
}
\]

and adding new positive weights can only shrink the outer approximation:

\[
P_{m+1}\subseteq P_m.
\]

Two latent systems with equal values on the finite design are observationally equivalent **for that design** even if their complete positive-weight value functions differ elsewhere.

Thus finite-design equivalence is weaker than global positive-weight equivalence.

## Empirical consequence

SCH now has a clean identification hierarchy:

```text
finite positive-weight responses
        -> outer support approximation
complete positive-weight value function
        -> exact closed convex upper attainable loss set
trait/manipulation measurements beyond weighted sums
        -> needed for unsupported nonconvex states and mechanistic phenotype identity
```

This gives a direct reason to keep the causal trait-manipulation layer separate from the later weight-sweep generality layer. Weight experiments can recover the convexified functional conflict geometry extremely well, but they cannot by themselves prove the unique latent phenotype map that generated it.

## Falsifiable signatures

Under the registered common attainable-set model:

- repeated positive-weight experiments that produce incompatible support half-spaces falsify a common static `Y`;
- a smooth value function predicts a unique exposed optimized loss vector equal to its weight gradient;
- a kink predicts a non-singleton exposed loss face or a support switch;
- two proposed mechanistic models that imply the same `U_Y` are observationally indistinguishable by positive weighted sums alone.

## Claim ceiling

The equivalence theorem inherits the assumptions of positive-weight dual reconstruction. It identifies the convex upper loss geometry, not historical evolution, latent developmental coordinates, or unsupported nonconvex Pareto structure. The derivative result concerns optimized loss vectors; it does not by itself identify a unique biological phenotype if multiple phenotypes map to the same loss vector. PAYOFF population dynamics remain outside SCH.