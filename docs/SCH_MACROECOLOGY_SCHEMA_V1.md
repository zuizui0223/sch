# SCH macroecology schema V1

## Purpose

This layer asks a different question from the SCH identification paper:

> **Under what ecological conditions does multifunctionality become alignment, conflict, context switching, compromise, or cancellation?**

The macroecology layer is comparative and descriptive unless a moderator is experimentally manipulated. It does not replace the SCH L0-L4 promotion ladder and it does not turn heterogeneous literature effects into a universal conflict coefficient.

## Two-level data architecture

SCH macroecology uses two linked tables.

1. **Cluster ledger** — one row per independent biological study programme/system. This protects independence and stores relatively stable biological/design metadata.
2. **Context-case ledger** — one row per cluster x population/year/treatment/consumer regime for studies that provide repeated ecological contexts. This preserves the very switching that a one-row-per-study summary would erase.

The current V1 implementation seeds the cluster ledger from the existing 16-cluster SCH pattern synthesis. It is a schema-validation dataset, not the inferential macroecology sample.

## Outcome axes

The outcomes are deliberately **non-exclusive**. A system can show both conflict and context switching.

Controlled values are `YES`, `NO`, and `UNRESOLVED`.

- `conflict_detected` — opposing function-linked direction/geometry on the declared same or closely bounded trait coordinate under the source-adjudicated claim ceiling.
- `alignment_detected` — multiple functions favor the same direction/state.
- `context_shift_detected` — the effective favored direction, strength, or geometry changes across an ecological context axis.
- `compromise_detected` — an intermediate/hump-shaped combined response is recovered on the focal coordinate.
- `cancellation_detected` — non-zero opposing component effects approximately cancel in the reported net selection/outcome.

A `NO` is used only when the source-adjudicated evidence supports a negative classification. Missing evidence is `UNRESOLVED`, not `NO`.

## Core ecological moderators

Cluster-level fields:

- `trait_domain`: `MORPHOLOGY`, `ORIENTATION`, `CHEMICAL_SIGNAL`, `PHENOLOGY`, `ALLOCATION`, `DISPLAY_STATE`, or `MULTIVARIATE_OR_COMPOSITE`.
- `function_pair_family`: biological pairing such as `MUTUALIST_ANTAGONIST`, `MUTUALIST_ABIOTIC`, `REPRODUCTION_ABIOTIC`, `SEXUAL_FUNCTION`, `SEXUAL_FUNCTION_ANTAGONIST`, or `REPRODUCTIVE_ALLOCATION_ANTAGONIST`.
- `antagonist_involved`: whether a florivore, herbivore, seed predator, grazer, robber, ovipositor, or analogous antagonist is part of the focal pair.
- `abiotic_function_involved`: whether one focal function is abiotic/resource-facing rather than consumer-facing.
- `shared_coordinate_status`: `SAME_COORDINATE`, `COMPOSITE_OR_MULTIVARIATE`, or `NOT_STRICT_SHARED_COORDINATE`.

Context-case fields to add during full recoding:

- population/site;
- year/season;
- treatment or consumer regime;
- pollinator guild/identity;
- antagonist guild/identity;
- antagonist pressure/intensity when reported;
- resource/abiotic state;
- latitude/longitude or study locality when source-supported;
- climatic covariates added only after location provenance is frozen;
- local direction/optimum for each function;
- local combined/net response;
- common-fitness endpoint;
- uncertainty and covariance availability.

## Design moderators

The cluster ledger separately records:

- `trait_manipulated`;
- `consumer_context_manipulated`;
- `common_fitness_endpoint`;
- `multilevel_trait_surface`;
- `spatial_replication`;
- `temporal_replication`.

These fields support an **identification model** distinct from the ecological model: which study designs are capable of promoting claims beyond multifunctionality?

## Sign-independent eligibility rule

The inferential macroecology sample must be built without conditioning inclusion on the observed sign.

A cluster/context is design-eligible when:

1. it is a primary plant study;
2. at least two focal functions are linked to one declared trait coordinate or a prospectively declared bounded coordinate;
3. the study contains enough directional, optimum, or performance information to classify the relation as opposing, aligned, null/one-sided, or unresolved;
4. the biological unit can be assigned to an independent cluster;
5. the outcome is coded even when no conflict is found.

Positive-only inclusion is prohibited for H1-H3 below.

## Registered ecological hypotheses

### H1 — ecological pairing predicts realized conflict geometry

Among sign-independently design-eligible same-coordinate cases:

`conflict_detected ~ antagonist_involved + abiotic_function_involved + trait_domain + function_pair_family`

Primary contrast: mutualist-antagonist versus mutualist-abiotic pairings.

Interpretation ceiling: an association within the screened published evidence universe, not natural prevalence and not a causal antagonist effect unless the moderator itself is experimentally manipulated.

### H2 — consumer-mediated conflict is more context-sensitive

Among systems observed in at least two ecological contexts:

`context_shift_detected ~ antagonist_involved + consumer_context_manipulated + spatial_replication + temporal_replication + trait_domain`

The denominator must be restricted to systems with an actual opportunity to observe switching.

### H3 — opposing components can hide behind weak net selection

For studies reporting commensurate component effects on one outcome scale, define

`cancellation_index = 1 - abs(sum(beta_j)) / sum(abs(beta_j))`

only when the component effects have compatible orientation and scale.

- near 0: reinforcement or little cancellation;
- near 1: strong cancellation.

Do not compute this index across incomparable response constructs or from pooled literature means.

### H4 — design predicts identification ceiling

Use the SCH promotion outcome as an ordinal/design endpoint once all source audits are complete:

`identification_level ~ trait_manipulated + consumer_context_manipulated + common_fitness_endpoint + multilevel_trait_surface`

This is a study-design result, not a biological prevalence result.

## Independence and hierarchy

Repeated populations, years, treatments, or consumer regimes from one programme are context cases nested inside one `cluster_id`. They do not become independent biological replication.

The planned model hierarchy is therefore:

`context case -> biological cluster -> taxon/lineage`

Phylogenetic structure may be added only after taxonomic coverage is large enough and names are source-normalized.

## Geographic extension

Geography is secondary to biological coding. Coordinates are admitted only when supported by the primary source or a traceable study-locality record. Climate extraction is downstream of coordinate validation.

A map, latitude count, or climate association does not by itself identify conflict.

## Current status

```text
SCHEMA = FROZEN_V1
SEED_CLUSTERS = 16
SEED_ROLE = SCHEMA_VALIDATION_ONLY
FULL_MACRO_SAMPLE = NOT_YET_CONSTRUCTED
SIGN_INDEPENDENT_ELIGIBILITY = REQUIRED
NATURAL_PREVALENCE = NOT_ESTIMATED
ECOLOGICAL_MODERATOR_CAUSALITY = NOT_ASSUMED
```

The next data task is to recode the full screened primary-study set into the cluster/context architecture without looking at the desired macroecological result while setting eligibility.
