# SCH theory -> causal predictions v2

## Purpose

Translate the current SCH mathematical results into prospectively measurable causal signatures without changing the existing Pedicularis full-surface gate.

The theory layer is now richer than the focal two-function experiment. This document separates:

1. signatures that the focal Pedicularis route can test now;
2. signatures requiring a later multi-function or multidimensional generality system.

No unexecuted biological result is promoted here.

---

## A. Focal Pedicularis causal layer

The primary design remains

```text
P0 qualified multilevel z manipulation
x P pollination-weight manipulation
x G independent seed-predator manipulation
-> same-context fitness surface
```

with primary fitness on the registered common scale.

### A1. Optimum-shift sign

For two strict-convex functions with distinct optima, increasing the relative weight of one function must move the optimized shared coordinate toward that function's optimum.

Causal readout:

- estimate state-specific `z*` under P/G weighting interventions;
- test the preregistered direction of movement rather than only whether optima differ.

Failure modes:

- no directional shift beyond uncertainty;
- shift in the wrong direction;
- manipulation changes the loss family or other phenotype dimensions rather than only the registered function weight.

### A2. Positive shared-axis conflict load

The focal surface must still recover a bounded positive `L` on the common fitness scale.

Curvature bounds can additionally convert measured function-optimum separation into a nonquadratic theoretical bracket for `L`.

A direct causal budget outside that bracket is a model audit trigger, not a reason to redefine the bracket post hoc.

### A3. Pairwise fixed-total weighting

If P/G manipulations can approximate a fixed-total transfer of functional importance, optimized conflict load is predicted to be concave along that transfer path.

An interior maximum occurs where residual functional losses are equal.

This is optional for the focal causal proof; it is a stronger theory test if the manipulation supports a calibrated weight path.

---

## B. Multi-function generality layer

The following signatures require more than the focal two-function Pedicularis surface and should not be claimed from it.

### B1. Weight-space curvature matrix

For a registered shared phenotype dimension `d`, estimate local optimized conflict over multiple independent functional-weight perturbations and recover

\[
M=-\nabla_w^2L^*.
\]

Theory predicts

\[
M\succeq0,
\qquad
\operatorname{rank}(M)\le d.
\]

Equivalent exact signatures include vanishing `(d+1)x(d+1)` minors.

### B2. Trait-coordinate invariance

Fit the same local shared-coordinate model in two preregistered invertibly related trait bases.

After transforming gradient/Hessian objects consistently, the recovered weight-curvature matrix must agree:

\[
\tilde M=M.
\]

This tests whether the low-rank signature is a genuine functional-weight object rather than an arbitrary trait-unit artifact.

### B3. Effective conflict dimension

For PSD `M`, report

\[
d_{eff}=\frac{\operatorname{tr}(M)^2}{\operatorname{tr}(M^2)}.
\]

Under the model,

\[
d_{eff}\le\operatorname{rank}(M)\le d.
\]

Use bootstrap/posterior draws rather than a point estimate alone.

Interpretation:

- `d_eff` near one: one conflict direction dominates locally;
- `d_eff>1` robustly: a one-dimensional shared-coordinate model is inadequate;
- `d_eff` is not a count of genes or historical modules.

### B4. Noise-robust spectral dimension certificate

Exact zero eigenvalues are not expected from estimated curvature matrices. Therefore preregister an operator-norm error bound

\[
\|\widehat M-M\|_{op}\le\varepsilon
\]

independently of the observed spectrum.

For a registered shared-coordinate dimension `d`, theory requires

\[
\lambda_{d+1}(\widehat M)\le\varepsilon.
\]

Thus

\[
\boxed{
\lambda_{d+1}(\widehat M)>\varepsilon
\Rightarrow
\text{dimension }d\text{ rejected under the registered error bound.}
}
\]

Report the conservative lower bound

\[
r_{cert}(\varepsilon)
=\#\{k:\lambda_k(\widehat M)>\varepsilon\}.
\]

Then the shared-coordinate model must have dimension at least `r_cert` if the regular curvature assumptions hold.

This is stronger than visual scree-plot interpretation because the rejection threshold is tied to a prospective perturbation guarantee. A dimension not rejected is only compatible, not proven.

### B5. d+1 binding-function certificate

At the global worst-case functional weighting, there exists a certificate supported on at most `d+1` binding functions.

For equal-curvature quadratic surfaces this reduces to the minimum-enclosing-ball geometry of function-specific optima.

A comparative multi-function system can therefore ask not only how many functions exist, but how many actually define the worst shared compromise.

### B6. Weight-perturbation design capacity

Before interpreting a low empirical curvature rank, audit whether the experiment had enough independent relative-weight directions to reveal the registered dimension.

Let `n` be the number of independently weightable functions and `q` the number of linearly independent fixed-total relative-weight perturbation directions. For projected curvature

\[
C=V^\top M V,
\]

theory gives

\[
\operatorname{rank}(C)\le\min(d,q).
\]

Therefore a design can only have capacity to recover `d` shared-coordinate curvature dimensions if

\[
\boxed{q\ge d}
\]

and, because the relative-weight simplex has dimension `n-1`, also

\[
\boxed{n\ge d+1.}
\]

These are necessary, not sufficient, conditions. Full local recovery additionally requires the manipulated directions to span phenotype-gradient space:

\[
\operatorname{rank}(GV)=d.
\]

A low-rank result from a design with `q<d` must therefore be labeled insufficient design capacity rather than evidence that the phenotype is low-dimensional.

Prospective reporting should include:

```text
number of independently manipulable functions n
independent relative-weight directions q
target shared-coordinate dimension d
maximum detectable curvature dimension min(n-1,q)
capacity classification
```

The focal two-function Pedicularis design has at most one independent relative-weight direction, so it is suitable for the Chapter-1 conflict proof but cannot identify a genuinely two-dimensional weight-curvature geometry. The multidimensional dimension programme belongs to later generality systems with at least `d+1` independently manipulable functions.

---

## C. Promotion ladder

```text
SCH-T
mathematical shared-coordinate predictions

SCH-C
causal weight manipulation moves z* as predicted
+ positive bounded L on one fitness scale

SCH-G1
same signatures recur in an independent floral system

SCH-G2
weight-curvature/dimension signatures recur in a cross-domain shared-coordinate system
```

PAYOFF invasion, ESS or coexistence results cannot promote any stage in this ladder.

## D. Minimum evidence statement

The current mathematics permits stronger predictions than the present focal data can test. Until the Pedicularis full surface is executed, the correct status remains:

```text
THEORY OPERATIONAL
CAUSAL ANALYZERS READY
FOCAL BIOLOGICAL CAUSAL RECEIPT PENDING
```

The multidimensional curvature/dimension programme belongs primarily to later generality tests unless a focal system with enough independently manipulable functions is developed.
