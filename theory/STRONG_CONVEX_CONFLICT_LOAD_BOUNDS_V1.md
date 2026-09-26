# SCH strong-convex conflict-load bounds v1

## Purpose

Convert function-optimum separation into quantitative lower and upper bounds on the shared compromise load without assuming exactly quadratic losses.

Let

\[
L^*(w)=\min_z\sum_{i=1}^n w_i\ell_i(z),
\qquad w_i>0,
\]

where each loss has unique minimizer `theta_i` and is normalized by

\[
\ell_i(\theta_i)=0,
\qquad
\ell_i'(\theta_i)=0.
\]

Assume that on the trait interval containing all relevant optima and the shared optimum,

\[
0<m_i\le \ell_i''(z)\le M_i<\infty.
\]

## Theorem 1 — function-wise quadratic envelopes

Strong convexity and smoothness imply

\[
\frac{m_i}{2}(z-\theta_i)^2
\le
\ell_i(z)
\le
\frac{M_i}{2}(z-\theta_i)^2.
\]

Define effective lower and upper curvature weights

\[
a_i=w_i m_i,
\qquad
b_i=w_i M_i,
\]

and totals

\[
A=\sum_i a_i,
\qquad
B=\sum_i b_i.
\]

## Theorem 2 — pairwise-disagreement bracket for optimized conflict load

Because the actual summed loss is bounded pointwise by the two quadratic envelopes,

\[
\min_z \frac12\sum_i a_i(z-\theta_i)^2
\le
L^*(w)
\le
\min_z \frac12\sum_i b_i(z-\theta_i)^2.
\]

Using the weighted-variance identity,

\[
\min_z\frac12\sum_i a_i(z-\theta_i)^2
=
\frac{1}{2A}\sum_{i<j}a_i a_j(\theta_i-\theta_j)^2,
\]

and analogously for `b_i`. Therefore

\[
\boxed{
\frac{1}{2A}\sum_{i<j}a_i a_j(\theta_i-\theta_j)^2
\le
L^*(w)
\le
\frac{1}{2B}\sum_{i<j}b_i b_j(\theta_i-\theta_j)^2.
}
\]

This is a nonquadratic quantitative bracket based only on function-specific optimum separation, functional weights, and curvature bounds.

## Corollary 2a — common curvature bounds

If every function satisfies the same bounds

\[
m\le\ell_i''(z)\le M,
\]

then

\[
\boxed{
\frac{m}{2W}
\sum_{i<j}w_iw_j(\theta_i-\theta_j)^2
\le
L^*(w)
\le
\frac{M}{2W}
\sum_{i<j}w_iw_j(\theta_i-\theta_j)^2
}
\]

with

\[
W=\sum_iw_i.
\]

Thus the familiar weighted pairwise-disagreement expression survives beyond quadratic loss as a curvature-scaled bracket.

## Corollary 2b — two-function bound

For two functions,

\[
\boxed{
\frac{a_1a_2}{2(a_1+a_2)}(\theta_1-\theta_2)^2
\le L^*
\le
\frac{b_1b_2}{2(b_1+b_2)}(\theta_1-\theta_2)^2.
}
\]

Large optimum separation must therefore generate a nontrivial shared compromise load whenever both functions retain positive curvature and positive weight.

## Corollary 2c — exact quadratic recovery

If

\[
\ell_i(z)=\frac{q_i}{2}(z-\theta_i)^2,
\]

then `m_i=M_i=q_i`, lower and upper bounds coincide, and the pairwise expression is exact.

## Why this matters for SCH

The strict-convex theorem established that distinct function optima imply positive conflict load. The present result adds magnitude control:

- optimum separation sets the geometric scale of unavoidable conflict;
- curvature determines how costly a given separation is;
- functional weights determine which pairwise disagreements dominate the total load.

This creates an empirical route in which function-specific surfaces need not be perfectly quadratic. Conservative curvature bounds can still translate measured optimum separation into a bound on the conflict budget.

## Empirical consequence

If experimental component-fitness surfaces provide:

```text
function-specific optimum estimates theta_i
relative functional weights w_i
conservative curvature intervals [m_i,M_i]
```

then SCH can report a preregistered interval for the theoretical shared-axis conflict load even before adopting a parametric quadratic model.

A directly estimated causal conflict budget that lies far outside this curvature bracket would indicate at least one mismatch among:

- the assumed common coordinate;
- curvature bounds;
- functional weighting;
- component-loss definition;
- context matching.

## Claim ceiling

The bounds require valid curvature bounds over the relevant trait interval. They do not hold globally if losses become nonconvex or if the shared optimum leaves the interval on which `m_i` and `M_i` were established.
