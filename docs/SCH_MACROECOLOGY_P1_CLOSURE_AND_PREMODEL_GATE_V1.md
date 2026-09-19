# SCH macroecology — complete P1 source-axis closure and premodel gate

## Milestone

The current high-priority P1 universe is now closed at source level.

```text
current primary-study inclusions                 117
P1: both audience responses + common fitness     47
record-level H1 candidates after manual gate     32
H1 candidates source-audited                     32 / 32
missing source-axis recodes                       0
```

The source audit generated 56 source-axis evidence records.

Seven source axes fail the geometry gate after primary-source inspection. The remaining 49 source-axis records are either model-eligible fixed-role axes or explicit consumer-role boundary axes.

## Record-level fate after source audit

Among the 32 record-level H1 candidates:

```text
retains >=1 fixed-role trait axis     19 records
role-boundary only                     7 records
fully downgraded                       6 records
```

Fully downgraded records remain in the H4 design audit. They are not deleted from the evidence programme.

The six full downgrades are:

- `SCHPRISMA-000202` — habitat fragmentation changes reproduction and robbing, but not through one shared plant trait axis;
- `SCHPRISMA-000213` — fertilization combines pollinator-mediated and selfing contributions;
- `SCHPRISMA-000214` — patch context is not a plant trait coordinate;
- `SCHPRISMA-000233` — seed-predator outcomes are not linked to the same floral odor coordinate;
- `SCHPRISMA-000253` — congeners differ simultaneously in phenology, morphology and breeding system;
- `SCHPRISMA-000287` — corolla width covaries with selfing and florivory, but pollinator and florivore causal contributions are not separable on the axis.

## Canonical-axis correction

Source-axis records are provenance. They are not automatically independent biological axes.

The complete P1 transformation is now:

```text
56 source-axis evidence records
-> 49 geometry-eligible / role-boundary source-axis records
-> 47 canonical biological trait axes
```

Two canonical axes currently have multiple source records:

- `Gentiana_lutea_color_axis`
- `Collaea_000312_flower_number`

Both become `CONTEXT_VARIABLE` because their source-specific ecological geometries differ. They are not counted twice.

## Canonical ecological geometry

Current 47-axis table:

```text
fixed-role canonical axes           34
role-boundary canonical axes        13

fixed-role resolved                 19
  conflict                           8
  reinforcement                      2
  one-sided / null                   7
  context-variable                   2

fixed-role unresolved               15
```

The resolved categories are descriptive only.

The important empirical result is the recurrence of several distinct realized geometries within the same pollinator-antagonist discovery frame.

## New final-batch corrections

### Mitraria coccinea

Edges and gaps alter flower production, fruit set and nectar robbing, and robbing reduces reproduction. However, the source does not estimate pollinator and robber responses to flower production as one trait coordinate.

Result: source-level H1 downgrade; retained as ecological-context/H4 evidence.

### Protea aurea

Bird pollinators spend more time on white morphs, but the behavioral difference has no apparent fecundity consequence. Realized fecundity is not directly associated with color.

Result: pigmentation enters as one-sided/null geometry.

Flower number is biologically important but its positive reproductive route is not isolated as pollinator-mediated selection, so that separate axis is downgraded for function attribution.

### Camissoniopsis cheiranthifolia

Small-flowered/selfing populations experience reduced pollen limitation and less florivory across the range. Within populations, however, florivores do not generally prefer larger flowers. The source interprets reduced florivory as more likely a consequence of mating-system differentiation than its selective cause.

Result: strong macroecological covariation, but no direct pollinator-versus-florivore geometry on corolla width.

### Tanacetum vulgare

The final Functional Ecology publication resolves two scales of chemodiversity.

Individual chemotype:
- florivore visitation differs significantly;
- overall pollinator response is weak/context specific;
- germination is affected by chemotype but not by florivore visits.

Plot chemodiversity:
- heterogeneous plots receive more pollinator visits;
- florivore visits do not respond to plot type;
- germination correlates with pollinator visits.

Both are retained as one-sided/null ecological geometry rather than conflict.

### Collaea cipoensis

The 2018 selection study identifies conflict on flower number.

The 2024 network study finds that many-flowered plants become more central mainly because of antagonistic visitors, while increased centrality does not translate into higher reproductive success.

These are the same biological flower-number axis under different study contexts.

Result:

```text
Collaea flower-number axis
-> CONTEXT_VARIABLE
```

rather than one conflict observation plus one independent second axis.

## Canonical model table

`data/SCH_MACROECOLOGY_CANONICAL_AXIS_TABLE_V1.csv` is now the modeling surface.

It stores one row per canonical axis with:

- biological cluster;
- trait domain;
- function pair;
- consumer-role status;
- source provenance;
- source-specific geometry classes;
- canonical geometry;
- context evidence;
- manipulation structure;
- H1 static eligibility;
- H2 context priority.

Current trait-domain coverage:

```text
MORPHOLOGY       30
CHEMICAL_SIGNAL   4
REWARD            4
DISPLAY_STATE     4
VISUAL_SIGNAL     3
PHENOLOGY         2
```

## Premodel gate

### H1 — static ecological geometry

```text
eligible canonical axes     17
independent clusters        13

conflict                    8 axes / 7 clusters
reinforcement               2 axes / 2 clusters
one-sided/null              7 axes / 5 clusters
```

A full multinomial H1 model remains fail-closed because the reinforcement category is too sparse for a stable multivariable fit.

Binary conflict-versus-other analysis is allowed only as exploratory work while the systematic recode is incomplete.

### H2 — ecological context switching

```text
context-priority axes       30
context-priority clusters   14
```

This is the strongest next macroecological route, but the context-case table has not yet been materialized. H2 therefore remains closed until population/year/treatment cases are split explicitly.

### H3 — cancellation

One canonical axis currently has an explicit directional cancellation signature: flowering phenology in *Gymnadenia conopsea*.

H3 remains closed pending numerical component-effect and covariance recovery.

### H4 — design frontier

The current 117 primary-study universe is already suitable for descriptive design-gap analysis.

Final systematic frequencies remain closed until the frozen screening universe is completed.

## Current ecological statement

> **Multifunctionality produces a family of ecological geometries rather than a universal compromise. Realized geometry is assembled at canonical trait axis × ecological context × consumer role.**

The statement is now supported not only by conflict examples but by reinforcement, one-sided/null effects, context-variable axes, consumer-role boundaries, and explicit source-level failures of apparent conflict candidates.

## Next priority

The highest information-value next step is:

```text
30 H2 context-priority canonical axes
-> materialize population/year/treatment context cases
-> distinguish true geometry switching from repeated static geometry
-> freeze H2 denominator
-> only then fit the hierarchical context-switch model
```

In parallel, the 15 unresolved fixed-role canonical axes should be source-mined because resolving even a few reinforcement/null cases would materially improve H1 category balance.
