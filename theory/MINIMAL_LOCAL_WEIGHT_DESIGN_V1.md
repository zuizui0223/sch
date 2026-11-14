# SCH minimal local weight-design theorem v1

## Purpose

Translate exposed-loss identification into a minimal local experimental design.

For `n` functional losses, it may appear that identifying the full optimized loss vector requires perturbing every weight independently. Positive homogeneity of the optimized value function removes one degree of freedom: the baseline value itself supplies the missing equation.

## Setup

Let

\[
V(w)=\min_z\sum_{i=1}^n w_i\ell_i(z),
\qquad w\in\mathbb R_{++}^n.
\]

Assume `V` is differentiable at the focal weight `w`, and define the exposed optimized loss vector

\[
g=\nabla_wV(w).
\]

Because scaling all weights by `a>0` scales the objective but does not change the optimizer,

\[
V(aw)=aV(w).
\]

Thus `V` is positively homogeneous of degree one.

## Theorem 1 — Euler equation supplies one loss-space equation

Euler's theorem for differentiable homogeneous functions gives

\[
\boxed{w^\top g=V(w).}
\]

The baseline optimized value therefore provides one exact linear equation in the `n` unknown components of the exposed loss vector.

## Theorem 2 — `n-1` independent relative-weight directional derivatives complete identification

Choose `n-1` perturbation directions

\[
d_1,\ldots,d_{n-1}
\]

such that the `n x n` matrix with rows

\[
w^\top,d_1^\top,\ldots,d_{n-1}^\top
\]

has full rank.

Measure the directional derivatives

\[
s_k=D_{d_k}V(w)=d_k^\top g.
\]

Then `g` is the unique solution of

\[
\boxed{
\begin{bmatrix}
w^\top\\
d_1^\top\\
\vdots\\
d_{n-1}^\top
\end{bmatrix}
g
=
\begin{bmatrix}
V(w)\\
s_1\\
\vdots\\
s_{n-1}
\end{bmatrix}.
}
\]

Hence the full exposed functional-loss vector is locally identified from:

```text
1 baseline optimized value
+ n-1 independent relative-weight response directions.
```

## Corollary 2a — simplex-tangent directions are sufficient

If functional weights are normalized to a simplex, natural relative-weight perturbations satisfy

\[
\mathbf 1^\top d_k=0.
\]

Any basis of this `(n-1)`-dimensional tangent space, together with the positive baseline row `w^T`, has full rank because `w` cannot lie in the zero-sum tangent subspace.

Thus `n-1` independent relative-demand perturbations suffice.

## Theorem 3 — fewer than `n-1` generic relative directions cannot identify all `n` exposed losses

With only `r<n-1` independent directional derivatives plus the Euler equation, the observation matrix has at most rank `r+1<n`.

Therefore its nullspace is nontrivial and multiple exposed loss vectors are compatible with the same local observations.

So, absent additional biological constraints, `n-1` relative directions are generically necessary as well as sufficient.

## Example — three functions

Let

\[
w=(1,1,1),
\qquad
g=(0.2,0.5,1.0).
\]

Then

\[
V=w^\top g=1.7.
\]

Choose

\[
d_1=(1,-1,0),
\qquad
d_2=(0,1,-1).
\]

The directional derivatives are

\[
s_1=-0.3,
\qquad
s_2=-0.5.
\]

The three equations

\[
g_1+g_2+g_3=1.7,
\]

\[
g_1-g_2=-0.3,
\]

\[
g_2-g_3=-0.5
\]

recover exactly

\[
(g_1,g_2,g_3)=(0.2,0.5,1.0).
\]

## Theory -> causal bridge

For a multi-function generality experiment, SCH can now preregister a minimal local design:

1. choose one focal positive weight vector;
2. record its optimized total value;
3. perturb functional demand along `n-1` independent relative directions;
4. estimate directional slopes;
5. reconstruct the exposed component-loss vector;
6. compare that vector with direct component assays and, when the phenotype-to-loss map is injective, reconstruct the optimized phenotype.

This separates **identification treatments** from additional held-out treatments used for curvature, convexity and support-geometry validation.

## Claim ceiling

The result is local and requires differentiability of the static value function at the focal weight. At a support switch, directional derivatives can depend on direction and the exposed object is a face rather than a unique loss vector. Finite differences require a prospectively justified approximation or local model. PAYOFF remains separate.