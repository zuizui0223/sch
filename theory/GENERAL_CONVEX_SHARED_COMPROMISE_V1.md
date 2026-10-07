# SCH general convex shared-compromise theorem v1

## Setup

Let two biological functions act on one shared scalar trait `z` through losses

```text
ell1(z), ell2(z)
```

with positive weights `w1,w2`.

Assume:

1. each `ell_i` is differentiable and strictly convex on an interval containing both optima;
2. each has a unique minimizer `theta_i`;
3. `theta1 < theta2`;
4. `w1,w2 > 0`.

Define the shared loss

```text
F(z)=w1 ell1(z)+w2 ell2(z).
```

## Proposition 1 — unique interior compromise

`F` is strictly convex, so it has at most one minimizer. Because

```text
F'(theta1)=w2 ell2'(theta1) < 0
F'(theta2)=w1 ell1'(theta2) > 0,
```

continuity of `F'` implies a unique root

```text
theta1 < z* < theta2.
```

Thus the shared optimum lies strictly between the function-specific optima whenever those optima differ.

This result does not require quadratic losses.

## Proposition 2 — positive compromise load

Define the general shared compromise load

```text
L_general
= min_z [w1 ell1(z)+w2 ell2(z)]
  - [w1 min_z ell1(z)+w2 min_z ell2(z)].
```

Because `theta1 != theta2`, no single `z` simultaneously attains both separate minima. Therefore

```text
L_general > 0.
```

If `theta1=theta2`, the same point minimizes both functions and `L_general=0`.

## Proposition 3 — directional weight response

Add the stronger regularity assumption that both losses are twice differentiable with positive second derivative in the relevant interval.

Let

```text
r = w1/w2.
```

The first-order condition is

```text
r ell1'(z*) + ell2'(z*) = 0.
```

Implicit differentiation gives

```text
dz*/dr
= -ell1'(z*) / [r ell1''(z*) + ell2''(z*)].
```

Since `theta1 < z* < theta2`, strict convexity gives `ell1'(z*)>0`; the denominator is positive. Hence

```text
dz*/dr < 0.
```

Increasing the relative weight of function 1 moves the shared optimum toward `theta1`. By symmetry, increasing the relative weight of function 2 moves it toward `theta2`.

## Empirical consequence

SCH's causal test is therefore not tied to parabolic fitness curves. Under a broad strictly convex one-axis class, selective changes in functional weight predict **directional optimum movement on the same trait coordinate**.

This is exactly why the empirical `z x P x G` surface is decisive: it can test the directional comparative-static signature rather than merely fit a quadratic curve.

## Claim ceiling

This is a mathematical statement conditional on convex single-coordinate losses. It does not establish that natural biological fitness surfaces are globally convex, that the manipulations change only the intended weights, or that a measured state-specific optimum is automatically a pure-function optimum.
