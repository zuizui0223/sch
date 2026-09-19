# SCH macroecology — complete current H1 source-axis frontier

## Milestone

All 32 record-level H1 candidates from the current 117-primary-study universe have now been source-audited into explicit source-axis records.

```text
record-level H1 candidates                    32
candidates with source-axis recode            32
missing source-axis recodes                    0
```

This closes the **source-axis coverage** stage for the current P1/H1 universe.

## What source audit changed

The original record-level P1/H1 gate was deliberately permissive. Primary-source inspection subsequently removed six records completely from the H1 trait-axis denominator:

```text
SCHPRISMA-000202  Mitraria
  patch/fragment context, not one shared trait axis

SCHPRISMA-000213  Pulsatilla
  fertilization mixes pollinator and selfing attribution

SCHPRISMA-000214  Costa Rican cloud-forest comparison
  patch context, not one plant trait axis

SCHPRISMA-000233  Haplopappus
  seed-predator outcome not linked to the same odor axis

SCHPRISMA-000253  Vaccinium congeners
  species differ simultaneously in phenology, morphology and breeding system

SCHPRISMA-000287  Camissoniopsis
  mating-system syndrome and floral parasitism covary geographically, but
  florivory is not identified as selection on one shared trait coordinate
```

One further record, SCHPRISMA-000353, is partially downgraded: network centrality is not a plant phenotypic axis, but flower number remains a valid source axis already represented in the Collaea programme.

Thus:

```text
H1 candidate source records with >=1 model axis   26
fully source-downgraded candidate records          6
partially downgraded records                       1
```

## Final source-axis layer for the current H1 candidate universe

Across the 32 candidate records:

```text
source-axis evidence records       57
biological clusters                29
fixed-role source axes             43
role-boundary source axes          14
```

Twenty-one fixed-role source axes across fourteen biological clusters currently have resolved ecological geometry:

```text
CONFLICT / OPPOSITION              9
ALIGNMENT / REINFORCEMENT         3
ONE-SIDED OR NULL                 9
```

One of the resolved conflict axes also carries explicit cancellation.

These are source-axis results, not the independent modeling denominator.

## Canonicalization

Seven source-axis records fail geometry eligibility and are retained only for provenance/H4.

The remaining source records are then merged across papers when they represent the same biological trait coordinate.

```text
57 source-axis evidence records
-> 50 model-eligible/boundary source-axis records
-> 48 canonical biological trait axes
```

Two canonical axes currently have multiple source records:

```text
Gentiana_lutea_color_axis
Collaea_cipoensis_flower_number_axis
```

### Gentiana

The focal-population study resolves reinforcement on the yellow-orange colour axis, whereas the broader multi-population source resolves a one-sided/context-dependent geometry.

The canonical axis is therefore:

```text
Gentiana_lutea_color_axis = CONTEXT_VARIABLE
```

rather than one reinforcement observation plus one one-sided observation.

### Collaea

The 2018 source identifies opposing selection on flower number.

The 2024 network source independently shows that many-flowered individuals are more connected and more visited in a network dominated numerically by antagonists, but does not re-estimate trait-specific opposing selection.

Both sources therefore support one canonical flower-number axis; the later paper is additional ecological context, not independent trait replication.

## Current canonical ecological geometry

After eligibility filtering and cross-source collapse:

```text
canonical trait axes                       48

fixed-role canonical axes                  35
role-boundary canonical axes               13

resolved fixed-role canonical axes         20
  conflict                                  9
  reinforcement                             2
  one-sided / null                          8
  context-variable                          1

unresolved fixed-role canonical axes       15
```

The ratio is still not a prevalence estimate because outcome resolution is incomplete and the current systematic screen is not fully closed.

## New ecological information from the final six records

### Protea aurea

Floral pigmentation attracts differential pollinator behavior, but the color-dependent visitation difference does not translate into fecundity.

Flowers per inflorescence explain more of the fecundity structure, yet surviving seed production is not directly associated with that floral trait.

Both axes therefore strengthen the **one-sided/null** rather than conflict class.

### Tanacetum vulgare

The final published chemodiversity study yields two scale-specific axes:

- individual chemotype;
- plot-level chemodiversity.

Plot-level chemical heterogeneity increases pollinator visitation but not florivore visitation or germination success.

Individual chemotype affects florivore visitation and some pollinator behavior, while germination tracks pollinator visitation rather than florivore visitation.

The key biological result is scale dependence:

```text
individual chemical identity
!=
neighbourhood chemical diversity
```

as ecological selection coordinates.

### Mitraria, Vaccinium and Camissoniopsis

These three records are valuable precisely because source audit prevents false promotion.

They contain real pollination-antagonism biology, but ecological context or correlated syndromes cannot be relabelled as a shared-trait conflict axis.

This is direct empirical support for the SCH claim ceiling.

## Current biological synthesis

The complete source-axis pass supports a stronger formulation than the original Viewpoint boundary:

> **A shared ecological setting does not determine a shared-trait trade-off. Multifunctional geometry emerges only after the focal trait coordinate, local interaction context and consumer functional role are jointly specified.**

The current canonical set contains:

- opposition;
- reinforcement;
- one-sided/null effects;
- context-variable geometry;
- cancellation;
- role-switching consumers;
- intrinsically benefit-cost-coupled consumers.

## Next analysis gate

The broad H1 source search is no longer the bottleneck.

The next tasks are:

1. materialize one canonical-axis ledger rather than source-axis fragments;
2. attach stable trait-domain, antagonist-guild and interaction-timing moderators;
3. separate resolved from unresolved outcomes prospectively;
4. build context cases for H2;
5. use exact/descriptive inference if the resolved cells remain too sparse for a stable multinomial model.

## Claim ceiling

```text
CURRENT_H1_SOURCE_AXIS_COVERAGE = COMPLETE
RECORD_LEVEL_H1_CANDIDATES = 32
SOURCE_AXIS_RECORDS = 57
MODEL_ELIGIBLE_SOURCE_AXIS_RECORDS = 50
CANONICAL_TRAIT_AXES = 48

RESOLVED_FIXED_ROLE_CANONICAL_AXES = 20
UNRESOLVED_FIXED_ROLE_CANONICAL_AXES = 15
ROLE_BOUNDARY_CANONICAL_AXES = 13

CONFLICT_PREVALENCE = NOT_ESTIMATED
H1_MODERATOR_MODEL = NOT_YET_FIT
H2_CONTEXT_MODEL = NOT_YET_FIT
```
