# Pedicularis rex empirical novelty boundary v1

## Purpose

The focal empirical paper must not claim novelty for ecological ideas or
experimental ingredients that already have strong precedents.

The defensible novelty is narrower:

> combine randomized multi-level manipulation of one shared floral coordinate
> with crossed selective mutualist/antagonist states, recover the resulting
> state-specific reproductive optima, and test whether antagonist exposure
> displaces the optimum away from trait states with greater pollination
> performance.

This document is a bounded close-precedent audit, not a global systematic review.

Machine matrix:

```text
empirical/architecture/PEDICULARIS_EMPIRICAL_NOVELTY_MATRIX_V1.csv
scripts/audit_pedicularis_empirical_novelty.py
```

## What is already established

### Conflicting selection on floral traits is not new

Classic and close precedents already show that floral traits can attract or
benefit pollinators while simultaneously increasing exposure to antagonists.

*Polemonium viscosum* is especially strong mechanistically. Galen & Cuba (2001;
doi:10.1111/j.0014-3820.2001.tb01313.x) experimentally altered flower shape:
more tubular flowers reduced ant access but paid a pollination/seed-production
cost. This is direct functional manipulation of a floral trade-off.

*Castilleja linariaefolia* (Cariveau et al. 2004;
doi:10.1111/j.0030-1299.2004.12641.x) used path/SEM decomposition to show
opposing pollination- and seed-predation-mediated selection on calyx length.

*Dalechampia scandens* (Pérez-Barrales et al. 2013;
doi:10.1111/j.1600-0706.2013.20780.x) showed that larger advertising bracts
received more pollen but also more seed-predator eggs, and constructed a
multivariate fitness function from natural trait variation.

Therefore the focal paper must not claim:

```text
first evidence for pollinator-antagonist conflict
first demonstration that attractive flowers pay enemy costs
first floral trait trade-off between pollination and defence.
```

## Consumer-factorial experiments are also not new

Three particularly close precedents already manipulate both ecological agents.

### Gymnadenia conopsea

Sletvold, Moritz & Ågren (2015; doi:10.1890/14-0119.1) manipulated pollination
and herbivory factorially. Pollinators and herbivores caused conflicting
selection on flowering phenology and reinforcing selection on spur length.

This is a very strong precedent for causal separation of mutualist- and
antagonist-mediated selection.

Its focal floral coordinates, however, remain naturally varying phenotypes.
The experiment estimates treatment-specific selection gradients; it does not
randomize one focal z across multiple levels to map four reproductive response
curves and locate bounded state-specific optima.

### Fragaria vesca

Egan et al. (2021; doi:10.1002/evl3.262) used a full factorial manipulation of
pollination and herbivory in woodland strawberry and quantified how the two
agents altered selection on defence and attraction traits. Conflicting
selection occurred on inflorescence density and agent effects were strongly
context dependent.

Again, the consumer manipulation is already factorial. The plant traits used
for selection analysis are naturally varying rather than one randomized
multi-level coordinate whose entire state-specific fitness surface is mapped.

### Trifolium repens

Santangelo, Thompson & Johnson (2019; doi:10.1111/jeb.13392) provides another
strong causal precedent. In an 800-plant common-garden experiment, they crossed
open versus supplemental pollination with ambient versus reduced herbivory
(and a defensive cyanogenesis phenotype) and tested how these treatments
changed selection on reproductive traits.

This removes any remaining basis for calling crossed pollination × herbivory
itself novel. As in the other factorial precedents, however, the focal
reproductive traits were naturally/genotypically varying rather than one shared
coordinate randomized over multiple ordered values for direct recovery of four
bounded state surfaces.

Therefore the focal paper must not claim:

```text
first pollinator x antagonist factorial experiment
first causal partition of pollinator- and herbivore-mediated selection
first demonstration that one agent changes selection imposed by another.
```

## Other close context-manipulation precedents

In *Erysimum mediohispanicum*, Gómez (2003; doi:10.1086/376574) experimentally
excluded ungulate herbivores and showed that the presence of herbivores weakened
or eliminated selection on several floral traits. This demonstrates that enemy
context can strongly alter the realized selection regime.

It does not manipulate pollination as the second crossed treatment, nor
randomize the focal floral coordinate across multiple levels.

In *Eurya japonica*, Tsuji & Ohgushi (2018; doi:10.1002/ece3.3921) combined
artificial floral damage/petal removal with pollination controls. Petal removal
reduced fruit and seed production under natural pollination but not under
artificial pollination, directly demonstrating a florivory-mediated
pollination-performance pathway. This is a close causal precedent for linking
antagonist damage to pollination and reproduction, but it does not randomize one
shared floral coordinate across a multi-level range or recover bounded
consumer-state reproductive optima.

## A close optimum precedent

Fitch & Vandermeer (2021; doi:10.1086/716637) is especially important for
bounding the novelty claim. In *Odontonema cuspidatum*, experimental floral
arrays varied flower number to measure pollinator and nectar-robber responses,
and the field/experimental programme recovered an optimum flower number under
antagonist-induced pollen limitation.

Thus neither multi-level manipulation of a pollinator-attraction trait nor
estimation of an ecological optimum under pollinator-antagonist conflict is, by
itself, the P. rex novelty.

The remaining difference is causal architecture. *Odontonema* does not
selectively cross pollinator and antagonist states around the same randomized
trait to recover separate reproductive surfaces and ask whether removing the
antagonist **moves the optimum**.

## A close optimum-displacement precedent

The idea that antagonist context can move a floral optimum is also not unique to
the P. rex programme. Wise & Hebert (2010; doi:10.1890/09-1373.1) found in
*Solanum carolinense* that selection on floral-sex ratio changed with natural
flower/fruit herbivory: under low herbivory the fitted optimum was near 29%
male flowers, whereas increasing herbivory shifted the pattern toward an
optimum at 0% male flowers.

This is a genuine context-dependent optimum-displacement precedent. It is not
the same causal design as P. rex: herbivory was not selectively randomized as a
G state, pollination was not crossed as P, and the focal floral coordinate was
not randomized across a registered multi-level surface.

Therefore **enemy-associated movement of a floral optimum is not itself the
novelty claim**.

## The bounded gap

Across the close precedents audited here, individual ingredients exist:

```text
shared floral conflict                         YES
direct floral phenotype manipulation           YES
multi-level attraction-trait manipulation       YES
ecological optimum under mutualist-antagonist conflict YES
antagonist-associated floral optimum displacement YES
selective enemy-context manipulation           YES
factorial pollination x herbivory              YES
selection-gradient decomposition               YES
nonlinear floral fitness surfaces              YES
```

What is not recovered in the audited close mutualist-antagonist examples is
their joint use in one design:

```text
randomized multi-level shared trait z
x
selective P state
x
selective G state
->
W00(z), W10(z), W01(z), W11(z)
->
bounded state-specific reproductive optima
->
direct test of antagonist-induced optimum displacement.
```

That joint design/estimand combination is the defensible novelty boundary.

## Why optimum displacement is different from a selection-gradient difference

A treatment-dependent linear selection gradient says that the local slope of
fitness with phenotype differs between ecological contexts.

The focal P. rex result asks a stronger geometric question:

```text
where is the reproductive maximum in each ecological state,
and how far does that maximum move when the antagonist is removed?
```

If:

```text
z_predator_free > z_predator_exposed
```

and randomized higher z also improves pollen receipt, then enemy pressure has
not merely changed a regression coefficient. It has displaced the realized
reproductive optimum away from a region of trait space with better pollination
performance.

That is the central empirical contribution.

## What a positive W1/W2 result would add

A positive outcome does not replace the older literature; it closes a different
link.

Earlier studies establish:

```text
pollinators and enemies can prefer the same floral cues;
their selection can oppose;
consumer manipulations can change selection gradients;
a manipulated attraction trait can have an inferred optimum under
pollinator-antagonist conflict;
an antagonist gradient can coincide with displacement of a floral optimum.
```

The focal causal experiment would add:

```text
antagonist state
-> displacement of a bounded reproductive optimum
-> displacement toward a region with lower measured pollination performance.
```

W1 further shows that the displacement also moves toward lower initial seed
set. W2 supports the pollen-receipt cost but not that stronger pre-predation
reproductive step.

## Why null worlds remain informative relative to the literature

The predeclared W3-W5 outcomes distinguish several alternatives already
suggested by the precedent literature.

- W3: enemies move the optimum, but not along the expected pollen-performance
  gradient. Antagonist effects operate through another pathway.
- W4: exsertion improves pollination, but enemies do not move the optimum.
  Functional conflict need not translate into enemy-induced adaptive-surface
  displacement.
- W5: neither link is recovered in the focal context.

These outcomes matter because factorial-selection studies already show that
consumer effects can be additive, context dependent, or absent. The P. rex
experiment tests which of those possibilities actually changes the location of
the reproductive optimum.

## Permitted novelty language

Use:

> Among the close floral mutualist-antagonist precedents audited here,
> factorial consumer manipulations already exist, but we found no example that
> combines randomized multi-level manipulation of one shared floral coordinate
> with crossed selective consumer states to recover state-specific reproductive
> optima and test antagonist-induced optimum displacement.

Do not use:

```text
the first pollinator-antagonist experiment
the first factorial test of mutualists and enemies
the first demonstration of conflicting floral selection
the first study ever to show enemy-induced optimum displacement
```

The last statement would require a dedicated systematic novelty search well
beyond this bounded close-precedent audit.
