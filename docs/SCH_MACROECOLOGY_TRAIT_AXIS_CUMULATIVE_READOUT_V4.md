# SCH macroecology cumulative trait-axis readout V4

## Current staged ecological layer

Five trait-axis recoding batches now contain:

```text
source records                     26
source-axis records                 48
model-eligible source-axis records       45
canonical trait axes                44
independent biological clusters     24

fixed-role canonical axes           30
consumer-role boundary axes         14
```

After source-level eligibility filtering and cross-source canonicalization, sixteen fixed-role canonical axes across twelve biological clusters are resolved enough to classify:

```text
CONFLICT / OPPOSITION              9
ALIGNMENT / REINFORCEMENT         2
ONE-SIDED OR NULL                 4
CONTEXT-VARIABLE                   1
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
SOURCE_AXIS_RECORDS = 48
MODEL_ELIGIBLE_SOURCE_AXES = 45
CANONICAL_TRAIT_AXES = 44
BIOLOGICAL_CLUSTERS = 24
FIXED_ROLE_CANONICAL_AXES = 30
FIXED_ROLE_RESOLVED_CANONICAL_AXES = 16
FIXED_ROLE_RESOLVED_CLUSTERS = 12

CONFLICT_CANONICAL_AXES = 9
REINFORCEMENT_CANONICAL_AXES = 2
ONE_SIDED_CANONICAL_AXES = 4
CONTEXT_VARIABLE_CANONICAL_AXES = 1

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


## Canonical-axis correction

Source-axis rows are evidence records, not automatically independent biological trait axes.

The first cross-source duplicate identified is the yellow-to-orange flower-colour axis in *Gentiana lutea*. One focal-population source resolves reinforcement, whereas the broader multi-population source resolves a one-sided/context-dependent pattern. The two records are therefore collapsed to:

```text
Gentiana_lutea_color_axis
-> CONTEXT_VARIABLE
```

rather than counted once as reinforcement and once as one-sided geometry.

This correction is now enforced by `SCH_MACROECOLOGY_CANONICAL_AXIS_OVERRIDES_V1.csv` and the canonical-axis builder.


## Eligibility before canonicalization

Three source-axis records are retained for provenance and H4 but are excluded from the H1/H2 canonical trait-axis denominator because source inspection invalidated the proposed functional geometry:

```text
Pulsatilla_000213_stalk_height
  -> function attribution mixes pollination and selfing

CloudForest_000214_patch_display
  -> patch context, not one shared plant trait axis

Haplopappus_000233_odor_blend
  -> seed-predator outcome not linked to the same odor coordinate
```

Thus the current denominator transformation is:

```text
48 source-axis evidence records
-> 45 geometry-eligible/boundary source-axis records
-> 44 canonical biological trait axes
```

The three excluded records remain in the design frontier; they are not biological exclusions from SCH as a programme.
