# Shared-to-differentiated quadratic bridge v1

## Purpose

This note gives the simplest analytic bridge between Chapter 1 / SCH and Chapter 2 / BITA. It is not a universal law of trait evolution. It is a local quadratic benchmark showing how a one-dimensional multifunctional compromise can create a potential benefit for later functional differentiation.

The notation in this document is deliberately **theory-level**. It must not be confused with the state-specific optima directly recovered by the crossed experiment.

## Theory-level function optima

Let one phenotype `z` serve two idealized functions with pure function-specific optima

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z).
```

Near those optima, write the fitness loss from functional mismatch as

```text
L_shared(z)
  = a (z - z_F1*)^2
  + b (z - z_F2*)^2
```

with `a > 0` and `b > 0` describing the local strengths of the two functional demands.

The idealized shared optimum is

```text
z_C,theory* = (a z_F1* + b z_F2*) / (a + b).
```

The minimum unavoidable mismatch loss under the one-dimensional architecture is

```text
L_compromise,theory*
  = [a b / (a + b)] (z_F1* - z_F2*)^2.
```

This quantity rises with the separation between pure function optima and with the joint strength of the two demands.

If either function has negligible weight (`a -> 0` or `b -> 0`), the theoretical compromise penalty vanishes because the shared optimum can move toward the remaining pure function optimum.

## Causal theory prediction

The formula yields a simple theoretical intervention prediction.

If function 2 is removed from the idealized loss,

```text
b -> 0
=> z_C,theory* -> z_F1*.
```

If function 1 is removed,

```text
a -> 0
=> z_C,theory* -> z_F2*.
```

This is the conceptual origin of the empirical optimum-shift test.

## What the crossed experiment directly identifies

The empirical `z x P x G` experiment does not generally identify `z_F1*` and `z_F2*` because every reproductive state can still contain consumer-independent/direct trait effects and other baseline processes.

It directly identifies:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

Therefore:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The empirical causal signature is:

```text
remove antagonism -> z_C* shifts toward z_P*
remove pollination -> z_C* shifts toward z_G*
```

plus opposing causal component gradients near `z_C*`.

This state-specific geometry is sufficient for the contemporary compromise claim. Pure function optima require an additional identifying assay for direct/background pathways.

## Chapter 2: two differentiated traits

Now consider two partially distinct coordinates `x` and `y`:

```text
function 1 <- x
function 2 <- y.
```

Under the idealized fully differentiated theory benchmark,

```text
L_diff(x,y)
  = a (x - z_F1*)^2
  + b (y - z_F2*)^2
  + K,
```

where `K` is the added construction, developmental, genetic, regulatory, or ecological cost of maintaining the differentiated architecture.

If `x` and `y` can be tuned independently, the ideal theoretical optimum is

```text
x* = z_F1*
y* = z_F2*
```

and the maximum theoretical advantage over the one-dimensional architecture is

```text
Delta_mod,theory
  = [a b / (a + b)] (z_F1* - z_F2*)^2 - K.
```

Differentiation is theoretically favored when

```text
K < [a b / (a + b)] (z_F1* - z_F2*)^2.
```

This is a design benchmark, not an automatically identified empirical quantity.

## Empirical BITA default

The default empirical Chapter-2 question should use the directly identified SCH reference:

```text
Does adding / increasing y move x* toward z_P*?
```

where `z_P*` is the function-1-facing state optimum identified by SCH.

Only if SCH independently identifies the pure objective `F1(z)` may BITA upgrade the reference to:

```text
Does x* move toward z_F1*?
```

The two analyses should be reported separately rather than silently equated.

## Partial rather than complete modularity

Real traits will rarely have perfectly diagonal functional loading. Cross-loading, shared development, pleiotropy and consumer-context dependence reduce the attainable release below the ideal benchmark.

In the floral implementation, the BITA `A x D x antagonist x pollinator` four-way term is one empirical diagnostic of this residual coupling.

Accordingly, the empirical hierarchy is:

```text
one shared coordinate
-> state-specific causal compromise geometry
-> second coordinate appears
-> preferential functional loading
-> release toward the SCH state-specific reference
-> mechanism-resolved differentiation
-> historical modularization only with transition evidence.
```

## Mapping to the floral implementation

```text
function 1 = pollinator-mediated reproductive gain
function 2 = avoidance / reduction of antagonist-mediated loss

Chapter 1 shared z = one attraction/display coordinate
Chapter 2 x       = attraction coordinate A
Chapter 2 y       = antagonist-reducing coordinate D.
```

The two-level SCH 8-cell design identifies local opposing functional effects around a declared `z` contrast. A multi-level `z` design identifies `z_P*`, `z_G*`, and `z_C*` directly. BITA then asks whether adding `D` shifts the preferred `A` state toward `z_P*` and improves the common reproductive outcome.

## What this benchmark does and does not establish

It establishes:

- a transparent theoretical meaning of one-dimensional compromise;
- a causal optimum-shift prediction;
- an explicit theoretical threshold at which extra trait dimensionality can be valuable;
- a common mathematical bridge between the two chapters.

It does not establish:

- that natural fitness surfaces are globally quadratic;
- that the experiment directly identifies pure `z_F1*` or `z_F2*`;
- that two observed traits are developmentally or evolutionarily independent;
- that an extant two-trait state evolved by splitting an ancestral shared trait;
- that `K = 0`;
- that empirical `Delta_mod` is identified without commensurable shared and differentiated fitness scales.

The quadratic model is therefore a theory benchmark and experimental design guide, not a shortcut around empirical identification.
