# SCH functional-weight criticality v1

## Purpose

SCH has no intrinsic shared-versus-differentiated phase transition while the architecture is fixed to one trait coordinate. Changing the weight of a focal function moves the shared optimum continuously.

However, once the BITA decoupling fraction and architecture cost are imported, the common architecture boundary can be projected onto a Chapter-1 ecological weight.

Let

```text
a = weight of function 1
b = context-dependent weight of function 2
lambda = residual coupling of the differentiated architecture
d = |theta1-theta2|
K = added architecture cost.
```

Then

```text
L_S*(b) = a b d^2/(a+b)

s(b) = a b/[a b + lambda(a+b)]

R(b) = s(b)L_S*(b)
     = a^2 b^2 d^2/
       [(a+b){a b + lambda(a+b)}].
```

The projected Chapter-1 critical condition is

```text
R(b_crit)=K.
```

## A finite BALANCE-only domain is generic

For `K>0`, conflict starts as soon as the second function has nonzero weight and the preferred states differ, but the architecture switch occurs only after the recoverable loss reaches `K`.

Therefore a finite interval can exist in which

```text
conflict is real
+
compromise is real
+
differentiation still does not pay.
```

This is the ecological-weight version of the previously derived load gap

```text
0 < L_S* < K/s.
```

## Increasing functional pressure has a ceiling

For `b>0` and `d>0`, `R(b)` increases monotonically, but

```text
R_infinity = a^2 d^2/(a+lambda).
```

Hence:

```text
K > R_infinity
-> BALANCE remains the higher-fitness architecture for every finite b.

K = R_infinity
-> the boundary is approached only at b -> infinity.

0 < K < R_infinity
-> a unique finite b_crit exists.

K = 0
-> the projected architecture threshold collapses onto conflict onset.
```

Thus stronger ecological antagonism does not guarantee trait differentiation. High architecture cost or residual coupling can remove the differentiated domain entirely.

## Finite critical weight

Define

```text
A = a^2 d^2 - K(a+lambda).
```

When `A>0`,

```text
b_crit
 = a { K(a+2lambda)
       + sqrt[K^2(a+2lambda)^2 + 4K lambda A] }
   / (2A).
```

The registered script `scripts/analyze_chapter1_functional_weight_threshold.py` computes this threshold and fails closed when no finite crossing exists.

## Biological use

A natural environmental variable such as seed-predator pressure is not automatically identical to `b`. The empirical programme must either:

1. estimate context-specific functional weights directly, or
2. preregister a calibration `b(e)` from the environmental control axis `e`.

Only then can the model translate a biological context into a predicted architecture critical context.

## Relationship to BITA

The same threshold is read oppositely by the two chapters:

```text
SCH: how strong must the second functional demand become before the one-axis compromise is too costly?

BITA: at the observed shared conflict, how much decoupling and how little added cost are required for the differentiated architecture to win?
```

They are two coordinate projections of the same `R-K=0` surface, not two independent theoretical phase boundaries.

## Claim ceiling

This result assumes the quadratic bridge and fixed `a`, `lambda`, `d`, and `K` while `b` changes. If environmental change also alters coupling, architecture cost, functional optima, or the fitness mapping, the observed critical context can shift away from this one-parameter prediction. That deviation is the empirical parallel-world question registered in BITA.
