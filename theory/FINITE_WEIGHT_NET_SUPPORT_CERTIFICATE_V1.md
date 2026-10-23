# SCH finite weight-net support certificate v1

## Purpose

Quantify what a **finite** set of functional-weight experiments can guarantee about the positive-weight dual reconstruction of attainable loss geometry.

The complete positive-weight value function reconstructs the closed convex upper attainable set exactly, but no experiment can sample every weight direction. This result turns the angular/directional coverage of a finite weight grid into a uniform bound on unsampled support-inequality error inside a declared bounded loss window.

## Setup

Let the attainable loss set satisfy

\[
Y\subset\mathbb R^n,
\qquad
\|y\|_2\le R_Y
\quad\forall y\in Y.
\]

For unit nonnegative weights

\[
\mathbb S_+^{n-1}
=
\{w\ge0:\|w\|_2=1\},
\]

define

\[
L^*(w)=\min_{y\in Y}w^\top y.
\]

Let `W` be a finite `delta`-net of `S_+`, meaning that for every `w in S_+` there exists `v in W` with

\[
\|w-v\|_2\le\delta.
\]

Define the finite-support outer approximation

\[
U_W=
\bigcap_{v\in W}
\{y:v^\top y\ge L^*(v)\}.
\]

Because the exact upper hull is unbounded upward, evaluate approximation quality inside a preregistered bounded analysis window

\[
\|y\|_2\le R_B.
\]

## Lemma 1 — support-value Lipschitz bound

For any unit nonnegative weights `w,v`,

\[
\boxed{
|L^*(w)-L^*(v)|
\le R_Y\|w-v\|_2.
}
\]

### Proof
Choose a minimizer `y_v` for `v`. Then

\[
L^*(w)-L^*(v)
\le (w-v)^\top y_v
\le R_Y\|w-v\|_2.
\]

Swap `w` and `v` for the reverse inequality.

## Theorem 1 — finite-net support-slack certificate

Take any candidate point

\[
y\in U_W,
\qquad
\|y\|_2\le R_B.
\]

For any unsampled unit positive weight `w`, choose registered `v` with `||w-v||<=delta`. Then

\[
\begin{aligned}
w^\top y
&=v^\top y+(w-v)^\top y\\
&\ge L^*(v)-R_B\delta\\
&\ge L^*(w)-(R_Y+R_B)\delta.
\end{aligned}
\]

Therefore

\[
\boxed{
 w^\top y
\ge
L^*(w)-\varepsilon_W
\quad\forall w\in\mathbb S_+^{n-1},
}
\]

with

\[
\boxed{
\varepsilon_W=(R_Y+R_B)\delta.
}
\]

Thus any bounded candidate satisfying all sampled support half-spaces can violate an unsampled exact positive-weight support inequality by at most `epsilon_W`.

## Corollary 1a — common bounded window

If the analysis window uses the same norm bound as the attainable loss set,

\[
R_B=R_Y=R,
\]

then

\[
\boxed{\varepsilon_W=2R\delta.}
\]

Halving the covering radius halves the worst-case support slack.

## Corollary 1b — monotone design refinement

If `W_2` refines `W_1` and has covering radius

\[
\delta_2\le\delta_1,
\]

then both the geometric outer approximation and its worst-case support-slack bound improve monotonically:

\[
U_{W_2}\subseteq U_{W_1},
\qquad
\varepsilon_{W_2}\le\varepsilon_{W_1}.
\]

This gives a prospective stopping rule based on desired support accuracy rather than an arbitrary number of weight treatments.

## Corollary 1c — required grid resolution

To guarantee support slack at most `tau>0` inside the declared window, it is sufficient to choose a weight grid with

\[
\boxed{
\delta
\le
\frac{\tau}{R_Y+R_B}.
}
\]

The remaining problem is purely geometric: construct a positive-unit-sphere net with that covering radius.

## Why this is not a Hausdorff claim

The upper attainable set is unbounded and the theorem controls **support-inequality slack** inside a bounded analysis window. It does not automatically equal Euclidean Hausdorff distance to the true upper hull. Translating support slack to a Euclidean set-distance bound requires additional regularity/conditioning of the active half-space geometry.

## Empirical consequence

A multi-function SCH generality experiment can preregister:

1. a bounded functional-loss window `R_B` relevant to biological interpretation;
2. a conservative attainable-loss norm bound `R_Y`;
3. a target support slack `tau`;
4. a weight design whose covering radius satisfies the required `delta`.

Then unsampled positive functional demands are not simply ignored: the design has an explicit worst-case geometric error certificate.

## Claim ceiling

The result assumes matched loss coordinates, a common compact attainable loss set while weights vary, valid norm bounds, and a genuine `delta`-net under the declared weight metric. It controls the convexified positive-weight geometry only; unsupported nonconvex Pareto structure and PAYOFF dynamics remain unidentified.
