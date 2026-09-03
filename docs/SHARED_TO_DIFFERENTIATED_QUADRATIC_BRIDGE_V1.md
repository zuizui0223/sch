# Shared-to-differentiated quadratic bridge v1

## Purpose

This note gives the simplest analytic bridge between Chapter 1 / SCH and Chapter 2 / BITA. It is not a universal law of trait evolution. It is a local quadratic benchmark showing exactly how a one-dimensional multifunctional compromise creates a potential benefit for later functional differentiation.

## Chapter 1: one shared trait

Let one phenotype `z` serve two functions with function-specific optima `z1*` and `z2*`. Near those optima, write the fitness loss from functional mismatch as

```text
L_shared(z)
  = a (z - z1*)^2
  + b (z - z2*)^2
```

with `a > 0` and `b > 0` describing the local strengths of the two functional demands.

The shared optimum is

```text
zc* = (a z1* + b z2*) / (a + b).
```

Thus `zc*` lies between the two function-specific optima whenever `z1* != z2*`.

The minimum unavoidable mismatch loss under the one-dimensional architecture is

```text
L_compromise*
  = [a b / (a + b)] (z1* - z2*)^2.
```

This is the key Chapter-1 quantity. The cost of sharing one coordinate rises with:

1. the squared distance between the function-specific optima; and
2. the joint strength of the two demands.

If either function has negligible weight (`a -> 0` or `b -> 0`), the compromise penalty vanishes because the shared optimum can move to the remaining function's preferred state.

## Causal optimum-shift prediction

The formula yields a direct intervention prediction.

If function 2 is experimentally removed or strongly weakened,

```text
b -> 0
=> zc* -> z1*.
```

If function 1 is removed or weakened,

```text
a -> 0
=> zc* -> z2*.
```

This is why SCH should not define compromise only by an intermediate phenotype. The stronger causal test is that changing functional weights moves the optimum in the predicted direction.

## Chapter 2: two differentiated traits

Now let the two functions be carried by partially distinct coordinates `x` and `y`:

```text
function 1 <- x
function 2 <- y.
```

Under the idealized fully differentiated benchmark,

```text
L_diff(x,y)
  = a (x - z1*)^2
  + b (y - z2*)^2
  + K,
```

where `K` is the extra construction, developmental, genetic, regulatory, or ecological cost of maintaining the differentiated architecture relative to the shared architecture.

If `x` and `y` can be tuned independently, the differentiated optimum is

```text
x* = z1*
y* = z2*
```

and the mismatch part of the loss vanishes.

The maximum fitness advantage of ideal differentiation over the shared architecture is therefore

```text
Delta_mod
  = [a b / (a + b)] (z1* - z2*)^2 - K.
```

Differentiation is favored in this benchmark when

```text
K < [a b / (a + b)] (z1* - z2*)^2.
```

This inequality is the simplest analytic statement of the SCH -> BITA logic:

```text
larger multifunctional conflict
        -> larger one-axis compromise penalty
        -> greater potential value of an extra trait dimension,
           provided modularization costs do not erase that gain.
```

## Partial rather than complete modularity

Real traits will rarely have perfectly diagonal functional loading. Let

```text
x -> function 1 strongly, function 2 weakly
y -> function 2 strongly, function 1 weakly.
```

Cross-loading, shared development, pleiotropy and consumer-context dependence reduce the attainable release below the ideal `Delta_mod` above. In the floral implementation, the BITA `A x D x antagonist x pollinator` four-way term is one empirical diagnostic of this residual coupling.

Accordingly, the empirical hierarchy is:

```text
one shared coordinate
-> measurable compromise penalty
-> second coordinate appears
-> preferential functional loading
-> partial or complete dimensional release
-> historical modularization only with transition evidence.
```

## Mapping to the floral implementation

The current plant example maps as follows:

```text
function 1 = pollinator-mediated reproductive gain
function 2 = avoidance / reduction of antagonist-mediated loss

Chapter 1 shared z = one attraction/display coordinate exposed to both functions
Chapter 2 x       = attraction coordinate A
Chapter 2 y       = antagonist-reducing coordinate D.
```

The two-level SCH 8-cell design identifies the local opposing functional effects around a declared `z` contrast. A multi-level `z` design is needed to estimate `z1*`, `z2*` and `zc*` directly. BITA then asks whether adding `D` shifts the preferred `A` state toward the pollination optimum and improves the common reproductive outcome.

## What this benchmark does and does not establish

It establishes:

- a transparent quantitative meaning of one-dimensional compromise;
- a causal optimum-shift prediction for Chapter 1;
- an explicit threshold at which the potential benefit of differentiation exceeds its extra cost;
- a common mathematical bridge between the two chapters.

It does not establish:

- that natural fitness surfaces are globally quadratic;
- that two observed traits are developmentally or evolutionarily independent;
- that an extant two-trait state evolved by splitting an ancestral shared trait;
- that `K = 0`;
- that the attraction-defence implementation is the only biological realization.

The quadratic model is therefore a local benchmark and experimental design guide, not a claim that all multifunctional systems follow one global fitness function.
