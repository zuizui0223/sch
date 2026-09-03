# Shared traits, opposing functions, and the evolution of compromise

## Abstract

A single phenotype often performs more than one ecological function. When those functions favor different trait values, evolution along one shared coordinate cannot optimize them independently. We formalize this problem as a **shared-trait compromise**: two functional surfaces act on one trait `z`, their function-specific optima differ, and the realized optimum is maintained where opposing marginal fitness gradients balance. This framing separates three questions that are often conflated: whether one trait affects multiple functions, whether those functions impose conflicting selection, and whether the observed phenotype is causally maintained as a compromise. We develop two linked identification designs. A local crossed-intervention design identifies the opposing functional contributions of one declared trait contrast; in the floral implementation this is an `A x antagonist x pollinator` eight-cell experiment. A multi-level trait design then estimates the function-specific optima `z1*` and `z2*`, the combined optimum `zc*`, and the predicted movement of `zc*` when either functional demand is experimentally weakened. Under a local quadratic benchmark, the unavoidable fitness penalty of a one-dimensional architecture is `[ab/(a+b)](z1*-z2*)^2`, directly linking the strength of functional conflict to the potential value of later trait differentiation. Existing floral studies provide real-world evidence for the required biological ingredients: shared or jointly exposed traits affect mutualists and antagonists, stabilizing compromise and context-dependent maintenance occur, and interaction regimes redirect evolutionary trajectories. They rarely provide the complete same-coordinate intervention needed to identify the mechanism in one system. SCH therefore treats the literature as ecological grounding and uses explicit experiments to test why multifunctionality produces balance. Chapter 2 / BITA asks the complementary question: when does an additional trait dimension release that compromise through functional differentiation or modularization?

## 1. The general problem

Traits are often multifunctional. A floral scent may recruit a pollinator and expose a plant to an antagonist; a structural element may support reproduction while also protecting tissue; a chemical compound may mediate attraction, defence, communication, or physiology. The important evolutionary problem is not simply that one trait has several effects. It is that **the same coordinate can be required to satisfy functions with different preferred states**.

Let one shared trait be `z`. Define two function-specific fitness components, `F1(z)` and `F2(z)`, with function-specific optima

```text
z1* = argmax F1(z)
z2* = argmax F2(z).
```

When

```text
z1* != z2*,
```

one value of `z` cannot simultaneously maximize both functions. If total fitness is

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z),
```

the combined optimum `zc*` is a compromise whenever it lies away from at least one function-specific optimum because the opposing functional gradients cancel there.

The central Chapter-1 question is therefore:

> **Does multifunctionality constrain evolution because different functions pull one shared trait toward different optima, and is the realized phenotype causally maintained by that balance?**

This is broader than the floral pollinator-antagonist case. The floral system is the first operational implementation because it offers clear functional interventions and a direct bridge to Chapter 2.

## 2. What counts as compromise

An intermediate phenotype is not sufficient evidence of compromise. Three nested conditions are required.

### 2.1 Multifunctionality

The same declared trait coordinate must affect both functions:

```text
z -> function 1
z -> function 2.
```

### 2.2 Functional conflict

The two functions must prefer different regions of trait space:

```text
z1* != z2*.
```

Equivalently, at the combined optimum the marginal contributions of the two functions should point in opposing directions.

### 2.3 Balance

At the realized combined optimum,

```text
w1 F1'(zc*) + w2 F2'(zc*) - C'(zc*) = 0,
```

while at least two component gradients remain non-zero and oppose one another. Thus **balance means cancellation of selection gradients, not equality of raw benefits or costs**.

The strongest evidence is causal: experimentally weakening function 2 should shift the optimum toward `z1*`, whereas weakening function 1 should shift it toward `z2*`.

## 3. A local quadratic benchmark

Near the two function-specific optima, write the mismatch loss as

```text
L_shared(z)
  = a (z - z1*)^2
  + b (z - z2*)^2,
```

with `a,b > 0`.

Then

```text
zc* = (a z1* + b z2*) / (a + b)
```

and the minimum unavoidable mismatch loss is

```text
L_compromise*
  = [a b / (a + b)] (z1* - z2*)^2.
```

This formula gives a transparent interpretation of constraint. The compromise penalty increases as the functional optima diverge and as both functional demands become strong. If one demand becomes negligible, the penalty vanishes because the shared trait can move toward the remaining optimum.

The same result produces the Chapter-2 prediction. If the two functions later gain partially independent coordinates `x` and `y`, the maximum ideal benefit of differentiation over the one-dimensional state is

```text
Delta_mod
  = [a b / (a + b)] (z1* - z2*)^2 - K,
```

where `K` is the extra cost of the differentiated architecture. Functional differentiation is favored in this benchmark when the avoided compromise loss exceeds that added cost.

The derivation and claim boundary are frozen in `docs/SHARED_TO_DIFFERENTIATED_QUADRATIC_BRIDGE_V1.md`.

## 4. Two complementary SCH experiments

SCH separates **local mechanism identification** from **fitness-surface identification**.

### 4.1 Local crossed intervention

In the floral implementation, the shared trait is one attraction/display coordinate `A`, and the two functions are pollinator-mediated reproductive gain and avoidance of antagonist-mediated reproductive loss. Cross

```text
A x antagonist x pollinator
```

in eight cells on one common reproductive outcome `W`.

Define

```text
d[g,p] = W[1,g,p] - W[0,g,p]
M_A(g) = d[g,1] - d[g,0]
G_A(p) = d[0,p] - d[1,p]
B_A    = d[0,0]
J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

A positive `M_A` identifies a pollinator-mediated contribution to the reproductive value of the same trait contrast; a positive `G_A` identifies an antagonist-mediated erosion of that value. `J_A` diagnoses context dependence between the two channels. `B_A` remains an unallocated consumer-independent remainder unless an independent assay gives it a narrower biological interpretation.

This experiment shows **why a local trait contrast is conflicted**. It does not by itself locate the full compromise optimum.

### 4.2 Multi-level `z` experiment

To identify compromise geometry, manipulate at least three and preferably five or more levels of the same `z` coordinate and estimate, under selective functional conditions:

```text
F1(z)
F2(z)
W_shared(z).
```

Recover

```text
z1*, z2*, zc*.
```

Then test the causal optimum-shift predictions:

```text
weaken function 2 -> zc* shifts toward z1*
weaken function 1 -> zc* shifts toward z2*.
```

This design distinguishes a true multifunctional compromise from an arbitrary intermediate phenotype, a monotonic endpoint, or a phenotype maintained by an unmeasured third process.

The full contract is `docs/SCH_MULTI_LEVEL_COMPROMISE_IDENTIFICATION_V1.md`.

## 5. The floral implementation as a mechanistic example

The current floral mapping is

```text
function 1 = pollinator-mediated reproductive gain
function 2 = avoidance / reduction of antagonist-mediated loss
shared trait z = floral attraction/display coordinate A.
```

A shared cue is one especially clear route to multifunctionality: pollinators and antagonists use the same sensory or display coordinate. Informational overlap alone is not enough. The stronger claim is that the two receivers make opposing causal contributions to the reproductive value of that coordinate.

This implementation motivates the eight-cell SCH design, but the general framework also accommodates other multifunctional traits in which the two functions are not defined by different receiver guilds.

## 6. Real-world evidence for Chapter 1

The literature is used as a **reality check on the mechanism**, not as the primary estimator of the chapter's causal quantities.

### 6.1 Integrated compromise

Pérez-Barrales et al. recover a one-trait observational fitness surface in which larger showy bracts increase pollination opportunity but also seed-predator exposure; antagonist selection counteracts pollinator selection and net selection tends toward stabilizing selection. This is the clearest existing case-level match to the shared-trait compromise geometry.

Theis & Adler supply the negative side of the same logic experimentally: increasing floral fragrance increases florivore attraction and reduces seed production without a detected pollinator-attraction gain. This does not locate the full optimum but demonstrates that increasing one display can move the plant away from a beneficial balance.

### 6.2 Context-dependent balance and polymorphism

The `Primula farinosa` studies show that opposing mutualist-antagonist selection need not maintain one continuous intermediate phenotype. Frequency-dependent selection and spatially varying pollinator-versus-grazer regimes can maintain or change alternative display morphs. Long-term manipulations link those functional weights to microevolutionary frequency change.

### 6.3 Experimental evolutionary redirection

Multigeneration experiments in `Brassica rapa` show that adding antagonism changes pollinator-driven evolutionary trajectories. This is broader than the strict shared-cue case, but it supports the general prediction that changing functional weights moves the evolutionary endpoint.

These cases establish that shared-function conflict and balance are real ecological phenomena. They do not replace the direct `z1*`, `z2*`, `zc*` identification experiment.

## 7. Current floral execution programme

The current system-selection work has two roles.

`Nicotiana attenuata` is the strongest same-coordinate reality anchor. Primary-source recovery shows that benzylacetone affects pollinator-mediated reproduction and hawkmoth oviposition on the same attraction axis, and established pollen-loading and egg-removal methods provide components of a selective intervention. Its key remaining gate is combined pollinator/antagonist selectivity and a short enough antagonist-to-fitness pathway.

`Castilleja linariaefolia` is a promising short-path candidate because pollinator and pre-dispersal seed-predator functions are more separable and antagonist effects map directly onto seed fitness, although a clean manipulable shared `z` coordinate still requires recovery and validation.

System choice is therefore driven by identifiability, not by familiarity or source count.

## 8. Literature programme and claim boundary

The frozen systematic cohort contains 868 records. Through V20, 405 records have title/abstract decisions and 117 primary studies are included. Only two studies satisfy the strict linked measurement architecture requiring a manipulated focal trait, both consumer responses, and a common reproductive outcome. These counts are not natural prevalence and are not the SCH estimand.

Their scientific role is to show that:

1. the constituent functional routes recur in nature;
2. compromise, polymorphism, evolutionary redirection, and partial decoupling occur;
3. the complete identifying experiment is rare.

The systematic screen therefore motivates and grounds the causal design rather than defining the paper as a literature review.

## 9. From compromise to differentiation

Chapter 1 ends with a constraint:

```text
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/
```

Chapter 2 asks what happens when the architecture gains another dimension:

```text
shared compromise
      ↓
function 1 -> trait x
function 2 -> trait y
      ↓
functional differentiation / modularization.
```

The strongest cross-chapter prediction is not merely that `x` and `y` both exist. It is that adding a function-2 coordinate should release `x` from the function-2 demand, shifting the optimum of `x` toward the function-1 optimum identified in SCH.

Contemporary functional differentiation is distinct from historical modularization. Demonstrating preferential loading and functional release in extant traits does not prove that an ancestral shared trait split into two descendant traits.

## 10. Main predictions

1. A genuinely multifunctional shared trait affects both declared functions.
2. The function-specific optima differ: `z1* != z2*`.
3. The combined optimum lies between or otherwise away from the function-specific optima because opposing marginal gradients balance.
4. Weakening one functional demand shifts the combined optimum toward the other function's preferred value.
5. The size of the compromise penalty increases with functional-optimum separation and the joint strength of both demands.
6. Systems with larger compromise penalties should have greater potential fitness benefit from an additional, preferentially loaded trait dimension, conditional on the added cost of differentiation.
7. Partial modularity should leave detectable residual cross-loading or context dependence.

## 11. Current claim ceiling

The current evidence supports the positive statement that multifunctional floral traits experience real opposing ecological demands and that case-level compromise, context-dependent maintenance, evolutionary redirection, and partial decoupling occur in nature. What is not yet available is one complete experiment that identifies both function-specific optima, the combined optimum, and the causal optimum shifts on the same trait coordinate.

The current conceptual status is therefore

```text
MULTIFUNCTIONAL_CONFLICT_REALITY_RECOVERED
CASE_LEVEL_COMPROMISE_RECOVERED
COMPLETE_CAUSAL_COMPROMISE_IDENTIFICATION_NOT_YET_EXECUTED.
```

## 12. Conclusion

Multifunctionality can constrain evolution even when every component process is individually adaptive. The constraint arises because multiple functions are forced to share one coordinate. SCH turns that intuition into an identifiable problem: estimate the functional optima, identify the opposing causal contributions, and test whether changing functional weights moves the shared optimum. This makes compromise a measurable property of trait architecture rather than a verbal description of an intermediate phenotype. The same quantities then generate a direct Chapter-2 prediction: the greater the loss imposed by one-dimensional sharing, the greater the potential value of functional differentiation, provided the costs and residual coupling of a more modular architecture do not erase the gain.
