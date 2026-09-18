# SCH macroecology cumulative trait-axis readout V4

## Current staged ecological layer

Five trait-axis recoding batches now contain:

```text
source records                     26
independent biological clusters   24
trait axes                         48

fixed-role axes                    34
consumer-role boundary axes        14
```

Seventeen fixed-role axes across twelve biological clusters are resolved enough to classify:

```text
CONFLICT / OPPOSITION              9
ALIGNMENT / REINFORCEMENT         3
ONE-SIDED OR NULL                 5
```

These counts describe the staged recode, not prevalence in nature or the final systematic sample.

## Contrast cases now span the full SCH geometry

### Reinforcement can itself be context dependent

In *Caryopteris divaricata*, shorter corolla tubes experience:

```text
less nectar robbing
more legitimate visitation
more seed production
```

when robbers are present.

However, when robbing is prevented, tube-length differences in legitimate visitation and seed production disappear.

Thus the realized alignment toward shorter tubes is itself antagonist-context dependent. Because bumblebee visitors can switch between legitimate and robbing behavior, the system is retained in the `ROLE_DEPENDENT` boundary stratum rather than the fixed-role H1 set.

### One-sided selection can dominate a factorial mutualist-antagonist experiment

In *Trifolium repens*:

- herbivores weaken selection for increased inflorescence production;
- herbivores weaken selection on flower size among acyanogenic plants;
- pollinators show no independent selection effect on those two axes.

Both axes therefore enter the fixed-role ledger as one-sided/null geometry rather than conflict.

Flowering time remains unresolved because the pollinator effect is defence-genotype dependent and the matched herbivore direction is not frozen at the current extraction level.

### Robbing behavior does not imply plant-fitness antagonism

In sesame, many pollinating bee species also rob nectar and robbing frequency depends strongly on corolla length, resource availability, flowering phase and time of day.

Yet robbing does not significantly reduce fruit or seed set in the source study.

The sesame axes are therefore retained as `ROLE_DEPENDENT` boundary cases rather than being assigned a negative antagonist sign merely because visits are classified as robbery.

### Shared floral trait bundles need not share one ecological axis

In *Polygala vayredae*, nectar reward is strongly linked to legitimate pollination, while flower size is associated with robbing frequency in one population.

The paper proposes robber-mediated negative selection on floral phenotype, but the two response routes are not source-resolved on the same individual trait axis.

Flower-size and nectar-reward axes therefore remain unresolved rather than being promoted to conflict.

## Why these negative and boundary cases matter

The enlarged staged set demonstrates that apparent pollinator-antagonist multifunctionality can resolve into at least five biologically different structures:

```text
1. conflict / opposition
2. reinforcement / alignment
3. one-sided or null geometry
4. role-dependent consumer behavior
5. benefit-cost-coupled consumer interactions
```

These structures cannot be collapsed into one "trade-off" variable without losing the ecology.

## Context dependence is layered

Context shifts now appear through several distinct mechanisms:

- antagonist abundance or removal;
- plant defence genotype;
- population or geographic interaction regime;
- trait identity within the same plant system;
- consumer role switching;
- reward state and floral access geometry.

The registered H2 analysis will therefore need context-case decomposition rather than a single binary "context dependent" label.

## Current ecological statement

> **Multifunctionality produces a family of ecological geometries, not a universal compromise. Which geometry is realized depends on the focal trait axis, ecological context and functional role of the interacting consumers.**

This statement is now supported by source-adjudicated positive, negative and boundary cases, but general frequency and moderator effects remain unestimated.

## Claim ceiling

```text
TRAIT_AXES_RECODED = 48
BIOLOGICAL_CLUSTERS = 24
FIXED_ROLE_RESOLVED_AXES = 17
FIXED_ROLE_RESOLVED_CLUSTERS = 12

CONFLICT_AXES = 9
REINFORCEMENT_AXES = 3
ONE_SIDED_AXES = 5

CONSUMER_ROLE_BOUNDARY_AXES = 14
ROLE_DEPENDENT_AXES = 9
BENEFIT_COST_COUPLED_AXES = 5

RESOLVED_CONTEXT_SHIFT_AXES = 7
CANCELLATION_AXES = 1

CONFLICT_PREVALENCE = NOT_ESTIMATED
H1_H2_H3_MODELS = NOT_FIT
FULL_MACRO_INFERENCE = CLOSED
```

Next: finish the remaining multi-axis P1 records, consolidate overlapping programmes into source-to-axis mappings, and then freeze the independent trait-axis denominator before model fitting.
