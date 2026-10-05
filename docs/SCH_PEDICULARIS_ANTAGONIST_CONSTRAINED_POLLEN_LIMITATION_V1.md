# Pedicularis rex antagonist-constrained pollen limitation hypothesis v1

## Biological question

The focal SCH programme asks whether the same floral exsertion axis is pulled
toward greater exposure by pollination and toward greater protection by
pre-dispersal seed predators.

A stronger biological consequence is now testable:

> **Do seed predators constrain floral exsertion below the state favoured by
> pollination, thereby contributing to the maintenance of pollen limitation in
> Pedicularis rex?**

This is related to, but not yet an example of, the
**antagonist-induced adaptive pollen limitation** mechanism formalized by Fitch
& Vandermeer (2021; doi:10.1086/716637).

Machine criterion map:

```text
empirical/architecture/PEDICULARIS_ANTAGONIST_CONSTRAINED_POLLEN_LIMITATION_V1.csv
scripts/audit_pedicularis_antagonist_constrained_pollen_limitation.py
```

## The unexpected focal observation

Sun, Armbruster & Huang (2016; doi:10.1093/aob/mcw097) did not recover only the
expected shared-trait pattern

```text
greater exsertion / wider lower lip
-> more stigmatic pollen
-> more seed predation.
```

In the seven populations retaining plant-level linkage between morphology,
pollination and seed outcomes, the best seed-predation model was:

```text
seed predation
= constant
+ exsertion***
+ lower-lip width*
+ pollen load*
+ population***

AICc = -156.11.
```

Thus higher pollen load remained positively associated with seed predation after
exsertion, lower-lip width and population were retained in the same selected
model.

The source explicitly describes this as unexpected.

This matters because it creates two distinct empirical layers:

```text
Layer A — shared-trait tracking
z -> pollen receipt
z -> predator attack / predation

Layer B — success-risk coupling
higher pollen receipt
<-> higher later seed-predation risk
conditional on measured z-related morphology and population.
```

Layer B is observational. It is not evidence that pollen itself causes attack.

## Why the coupling is biologically interesting

Seed-predator oviposition occurs during flowering, before the eventual seed crop
is available to inspect. The adults therefore cannot simply count the later seed
resource and choose the richest fruit.

The 2016 authors propose that ovipositing adults may use floral information that
predicts future reproductive value, mentioning possibilities such as pollen
odours or unmeasured floral traits associated with pollination success. They
also explicitly state that the mechanism is unclear.

The source additionally warns that the study uses standing phenotypic variation,
so environmental covariance or unmeasured variables could contribute to the
association.

Therefore the admissible interpretation is:

```text
POLLINATION_SUCCESS_ANTAGONIST_RISK_COUPLING = RECOVERED

POLLEN_AS_CAUSAL_PREDATOR_CUE = NOT IDENTIFIED
PREDICTIVE_OVIPOSITION_MECHANISM = HYPOTHESIS
UNMEASURED_QUALITY_OR_PHENOLOGY_CONFOUNDING = POSSIBLE.
```

## Connection to antagonist-induced adaptive pollen limitation

Fitch & Vandermeer (2021) state four requirements for antagonist-induced
adaptive pollen limitation.

### Criterion 1 — correlated attraction of mutualists and antagonists

**Observationally supported in P. rex.**

Greater exsertion and lower-lip width are associated with both greater pollen
receipt and greater seed predation.

The additional pollen-predation association makes the ecological coupling even
stronger, but does not identify its cue.

### Criterion 2 — antagonists respond more strongly than pollinators to increased attraction investment

**Unresolved.**

The 2016 pollen and predation models are on different response scales and were
not designed as a common-scale causal sensitivity comparison. Their
coefficients must not be ranked post hoc as if they measured the same response.

The randomized multi-level z experiment is the appropriate place to compare
prospectively defined standardized response curves.

### Criterion 3 — reduced attraction investment causes pollen limitation

**Required components are present; the causal chain is unresolved.**

The focal programme indicates pollen limitation, and greater exsertion predicts
greater pollen receipt. But the observational geographic study does not show
that seed-predator selection caused reduced exsertion, nor that such reduction
caused the existing pollen limitation.

### Criterion 4 — reduced attraction investment increases total fitness under antagonism

**Unresolved until the causal combined optimum is identified.**

Seed predators reduce final viable seed production and oppose
pollinator-mediated selection on exsertion. That is conflicting selection, but
it is not yet a bounded causal fitness optimum demonstrating that a lower-z
state maximizes total fitness when antagonists are present.

## Causal SCH predictions

The corrected P. rex `z x P x G` experiment can test the missing causal chain
without redefining its primary SCH estimands.

The strongest directional prediction is:

```text
z_P* = optimum under natural pollination + predator exclusion
z_C* = optimum under natural pollination + predator exposure

antagonist-constrained-pollination prediction:

z_P* > z_C*.
```

This should not be described as predator removal directly increasing pollen
receipt within the same flower. G is deliberately qualified so it does not
contaminate pollination.

Instead the causal chain is:

```text
predator exposure
-> changes the reproductive fitness surface over randomized z
-> lowers the favoured exsertion state

and independently

randomized higher z
-> increases pollen receipt / initial seed set.
```

The biological consequence is that the exsertion state favoured in the absence
of seed predators should provide more pollination service than the lower state
favoured when predators are present.

## Natural phenotype alignment

Stage P0 includes a sham/natural-exsertion level. This provides an additional
descriptive check after the causal surface is fitted:

```text
is realized natural/sham exsertion closer to z_C* than to z_P*?
```

If so, the contemporary phenotype is consistent with the combined
mutualist-antagonist optimum rather than the predator-free pollination optimum.

This is supporting evidence only. A one-season alignment does not demonstrate
historical evolutionary adaptation or genetic response.

## Success-risk coupling prediction for the field programme

The current event-time and full-surface designs already preserve the variables
needed for a prospective test:

```text
randomized / realized z
plant block
pollen receipt
initial seed set
early antagonist attack
later seed predation
population / season context.
```

A replicated positive association between pollination success and antagonist
risk after randomized z is controlled would strengthen the success-risk
coupling result.

It still would not prove that pollen is the cue. Cue identity requires a
separate chemical/phenological/reward assay.

## Falsifiers

The antagonist-constrained pollen-limitation hypothesis is weakened or rejected
for the tested context if:

```text
predator removal does not shift the fitness optimum toward greater exsertion;

randomized greater exsertion does not increase pollen receipt or initial seed set;

the combined predator-exposed optimum is not lower than the predator-excluded
natural-pollination optimum;

or the apparent historical pollen-predation coupling disappears once randomized
z and prospectively measured local state are controlled.
```

A negative result remains informative: P. rex could still exhibit genuine
functional conflict without that conflict being responsible for its pollen
limitation.

## Claim ceiling

Current evidence supports:

```text
SHARED_POLLINATOR_ANTAGONIST_TRACKING              RECOVERED
POLLEN_LIMITATION_STATE                            RECOVERED
POLLINATION_SUCCESS_ANTAGONIST_RISK_COUPLING       RECOVERED_OBSERVATIONALLY
ANTAGONIST_CONSTRAINED_POLLEN_LIMITATION           CAUSAL_HYPOTHESIS
ADAPTIVE_POLLEN_LIMITATION                         NOT IDENTIFIED
PREDICTIVE_SEED_PREDATOR_CUE                       NOT IDENTIFIED
POLLEN_ODOR_AS_CAUSAL_CUE                          NOT IDENTIFIED
```

The value of this hypothesis is that it converts the Pedicularis full surface
from a generic demonstration of compromise into a direct ecological question:
whether enemy-mediated selection can keep a pollinator-dependent flower below
its pollination-favoured trait state.
