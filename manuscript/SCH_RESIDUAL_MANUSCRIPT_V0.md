# Causal identification of functional conflict in multifunctional traits

## Abstract

Traits often contribute to multiple biological functions, but multifunctionality alone does not establish functional conflict. A single phenotypic coordinate may affect two functions while both favor the same state, while state-specific reproductive optima can differ from the pure-function optima assumed by theory. We develop an identification framework that separates these cases. Crossed manipulation of a focal trait with selective functional interventions reconstructs context-specific fitness surfaces and identifies whether opposing functional geometry exists. Component contrasts then provide an optional promotion gate from contextual optima to empirical pure-function optima when those component optima are stable across the state of the other function. Failure of that gate is informative: it implies context-dependent functional geometry rather than a failed experiment. The framework turns a common verbal claim—one trait serves two functions—into a falsifiable causal programme for determining whether those functions genuinely compete along a shared phenotypic coordinate.

## 1. Introduction

Multifunctional traits are often described as trade-off traits. That inference is unsafe. The fact that one phenotype contributes to two fitness-relevant processes establishes multifunctionality, not opposition. A trade-off requires causal evidence that improving one functional contribution moves fitness in a direction that conflicts with improvement of the other on the same phenotypic coordinate.

A second identification problem follows. Experiments commonly estimate the optimum phenotype in a pollinator-present state, an antagonist-present state, or a combined state. These are state-specific reproductive optima. They are not automatically the pure-function optima used in theoretical compromise models because direct phenotype effects and residual background channels can remain in every ecological state.

We therefore separate three questions: whether two functions use the same trait, whether they impose opposing causal geometry on that trait, and whether context-specific component optima are stable enough to be interpreted as pure-function optima.

## 2. Identification framework

Let `z` be a focal trait and let `P` and `G` denote two selectively manipulable ecological functions or channels. The crossed design estimates

```text
W00(z), W10(z), W01(z), W11(z).
```

The direct state-specific optima are

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

These quantities reconstruct contextual compromise geometry but do not, by default, identify pure-function optima.

Define component contrasts

```text
M_G0(z)=W10(z)-W00(z)
M_G1(z)=W11(z)-W01(z)
H_P0(z)=W01(z)-W00(z)
H_P1(z)=W11(z)-W10(z).
```

A function-specific optimum may be promoted to an empirical pure-function optimum only if its component optimum is stable across the state of the other function under a prospectively frozen equivalence criterion, with interior-optimum and uncertainty support.

## 3. Falsifiable outcomes

The framework distinguishes at least four outcomes:

1. multifunctionality without conflict;
2. opposing contextual geometry with an interior compromise;
3. context-stable component optima that support empirical pure-function promotion;
4. context-dependent component optima that block the promotion while retaining a valid contextual-conflict result.

The fourth outcome is scientifically meaningful because it shows that the functional landscape itself changes with ecological context.

## 4. Empirical implementation

The primary execution system is a conflict-qualified Dalechampia population or season. The staged programme is:

```text
population qualification
-> reversible multi-level z manipulation
-> selective functional-state validation
-> 5 z x 2 P x 2 G experiment
-> contextual compromise reconstruction
-> optional component-optimum promotion.
```

The key empirical requirement is one common reproductive fitness scale across all crossed states.

## 5. Discussion

The framework shifts the burden of proof from demonstrating that one trait participates in two functions to demonstrating that the two functions impose opposing causal geometry on one shared coordinate. It also prevents a second common overreach: relabeling ecological state optima as pure-function optima without identifying function-specific causal components.

The resulting claim is narrower but stronger. A valid experiment can establish contextual functional conflict even when pure-function promotion fails. Conversely, multifunctionality alone remains insufficient evidence of a trade-off.

## Scope after SLK integration

This paper does not own the later architecture chain `L -> Phi=sL-K -> evolutionary outcomes`. Once a valid conflict budget `L` is identified, that cross-architecture hierarchy is handed to SLK. The present paper owns the causal identification problem that makes such a handoff legitimate.
