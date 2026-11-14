# SCH general n-function shared-axis theorem v1

## Purpose

Extend the one-coordinate compromise result beyond two functions and beyond quadratic loss.

Let one shared trait coordinate be `z`. Function `i` contributes a twice continuously differentiable loss

\[
\ell_i(z),
\]

with positive weight `w_i>0`. Assume each `\ell_i` is strictly convex with a unique minimizer `theta_i`, and define

\[
J(z;w)=\sum_{i=1}^n w_i\ell_i(z).
\]

Assume positive curvature on the relevant interval,

\[
H(z;w)=\sum_i w_i\ell_i''(z)>0.
\]

## Theorem 1 — unique shared optimum lies in the function-optimum hull

`J` is strictly convex, hence has a unique minimizer `z*(w)` satisfying

\[
\sum_i w_i\ell_i'(z^*)=0.
\]

Let

\[
\theta_{\min}=\min_i\theta_i,
\qquad
\theta_{\max}=\max_i\theta_i.
\]

If not all `theta_i` are equal, then

\[
\boxed{\theta_{\min}<z^*<\theta_{\max}}.
\]

Reason: for `z<=theta_min`, every derivative is non-positive and at least one is strictly negative; for `z>=theta_max`, every derivative is non-negative and at least one is strictly positive. The unique zero of the summed derivative must lie strictly between the extremes.

Thus a shared coordinate cannot optimize outside the convex hull of the function-specific optima under these assumptions.

## Theorem 2 — exact weight sensitivity

Differentiate the first-order condition with respect to `log w_j`:

\[
0
=
\frac{d}{d\log w_j}
\left[\sum_i w_i\ell_i'(z^*)\right].
\]

This gives

\[
\boxed{
\frac{\partial z^*}{\partial\log w_j}
=
-\frac{w_j\ell_j'(z^*)}{H(z^*;w)}
}.
\]

Because strict convexity implies

\[
\operatorname{sign}\ell_j'(z^*)
=
\operatorname{sign}(z^*-\theta_j),
\]

we obtain

\[
\boxed{
\operatorname{sign}
\left(
\frac{\partial z^*}{\partial\log w_j}
\right)
=
\operatorname{sign}(\theta_j-z^*)
}.
\]

So increasing the relative importance of one function moves the shared optimum toward that function's own optimum. This is the n-function, nonquadratic version of the SCH directional intervention prediction.

## Corollary 2a — common rescaling of all weights does nothing

Summing the log-weight sensitivities gives

\[
\sum_j
\frac{\partial z^*}{\partial\log w_j}
=
-\frac{\sum_jw_j\ell_j'(z^*)}{H}
=0.
\]

Hence multiplying every weight by the same positive constant changes the scale of total loss but not the compromise location.

The identifiable object is therefore **relative functional weighting**, not absolute multiplication of all functions by the same factor.

## Corollary 2b — local sensitivity magnitude

The response to function `j` is larger when

- its current weighted gradient `|w_j ell_j'(z*)|` is large;
- total curvature `H` is small.

Thus shallow compromise landscapes are more environmentally labile than steep ones even at the same optimum ordering.

## Theorem 3 — positive compromise load

Normalize each function loss so that

\[
\ell_i(\theta_i)=0.
\]

Define the optimized shared loss

\[
L_n^*(w)=\min_z\sum_iw_i\ell_i(z).
\]

Then

\[
\boxed{L_n^*(w)\ge0},
\]

with equality if and only if all positively weighted functions share a common minimizer. Therefore, with distinct unique optima,

\[
\boxed{L_n^*(w)>0}.
\]

This is the general shared-coordinate conflict load. The quadratic weighted pairwise-disagreement identity is a special case, not the definition.

## Empirical consequence

For a natural environmental axis `e` that changes one functional weight while leaving the loss family fixed locally, SCH predicts a directional optimum shift toward the corresponding function-specific optimum. With multiple independently manipulable functions, the vector of observed optimum responses should respect the sign rule above.

Failure of that sign rule after selective intervention is evidence against the registered shared-axis mechanism, unless the intervention also changes `ell_i`, other function weights, or the trait coordinate itself.

## Claim ceiling

This theorem establishes geometry and comparative statics conditional on strict convexity, unique function optima, and a common scalar coordinate. It does not establish those assumptions biologically, does not prove historical adaptation, and does not imply PAYOFF invasion dynamics.
