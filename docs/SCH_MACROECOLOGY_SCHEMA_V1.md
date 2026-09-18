# SCH macroecology schema V1

## Purpose

This layer asks a different question from the SCH identification paper:

> **Under what ecological conditions does multifunctionality become alignment, conflict, context switching, compromise, or cancellation?**

The macroecology layer is comparative and descriptive unless a moderator is experimentally manipulated. It does not replace the SCH L0-L4 promotion ladder and it does not turn heterogeneous literature effects into a universal conflict coefficient.

## Three-level data architecture

SCH macroecology uses three linked biological levels.

1. **Cluster ledger** — one row per independent biological study programme/system. This protects replication and stores programme-level metadata.
2. **Trait-axis ledger** — one row per cluster x declared trait coordinate. This is the primary unit for conflict/alignment geometry. A single study may therefore contribute several trait axes without becoming several independent clusters.
3. **Context-case ledger** — one row per trait axis x population/year/treatment/consumer regime when repeated ecological contexts are available. This preserves switching without inflating independent replication.

This third level is necessary because one study can contain opposite ecological geometry on different traits. For example, the existing *Gymnadenia* evidence contains conflicting agent-mediated selection on flowering phenology but reinforcing selection on spur length. Collapsing both into one cluster-level binary outcome would erase that biological result.

The current 16-cluster seed remains a schema-validation summary inherited from the legacy pattern synthesis. Inferential H1-H3 will use trait-axis and context-case records while clustering uncertainty at the biological-cluster level.

## Outcome axes

The outcomes are deliberately **non-exclusive**. A system can show both conflict and context switching.

Controlled values are `YES`, `NO`, and `UNRESOLVED`.

- `conflict_detected` — opposing function-linked direction/geometry on the declared same or closely bounded trait coordinate under the source-adjudicated claim ceiling.
- `alignment_detected` — multiple functions favor the same direction/state.
- `context_shift_detected` — the effective favored direction, strength, or geometry changes across an ecological context axis.
- `compromise_detected` — an intermediate/hump-shaped combined response is recovered on the focal coordinate.
- `cancellation_detected` — non-zero opposing component effects approximately cancel in the reported net selection/outcome.
- `one_sided_or_null_detected` — one focal functional route is directional while the other is null/unresolved on the declared coordinate, so the case is neither conflict nor alignment.

A `NO` is used only when the source-adjudicated evidence supports a negative classification. Missing evidence is `UNRESOLVED`, not `NO`.

## Core ecological moderators

Trait-axis fields:

- `trait_axis_id`: stable identifier nested inside `cluster_id`.
- `trait_domain`: `MORPHOLOGY`, `ORIENTATION`, `CHEMICAL_SIGNAL`, `REWARD`, `PHENOLOGY`, `ALLOCATION`, `DISPLAY_STATE`, or `MULTIVARIATE_OR_COMPOSITE`.
- `function_pair_family`: biological pairing such as `MUTUALIST_ANTAGONIST`, `MUTUALIST_ABIOTIC`, `REPRODUCTION_ABIOTIC`, `SEXUAL_FUNCTION`, `SEXUAL_FUNCTION_ANTAGONIST`, or `REPRODUCTIVE_ALLOCATION_ANTAGONIST`.
- `antagonist_involved`: whether a florivore, herbivore, seed predator, grazer, robber, ovipositor, or analogous antagonist is part of the focal pair.
- `abiotic_function_involved`: whether one focal function is abiotic/resource-facing rather than consumer-facing.
- `shared_coordinate_status`: `SAME_COORDINATE`, `COMPOSITE_OR_MULTIVARIATE`, or `NOT_STRICT_SHARED_COORDINATE`.
- `antagonist_role_status`: `NET_ANTAGONISTIC`, `ROLE_DEPENDENT`, `BENEFIT_COST_COUPLED`, or `UNRESOLVED`. `ROLE_DEPENDENT` means the same visitor changes functional role across morphology/context; `BENEFIT_COST_COUPLED` means pollination benefit and exploitative/damaging activity are intrinsically linked within a visit or life cycle. Neither is forced into the fixed-antagonist H1 stratum.

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

## Sampling-frame rule

The existing frozen 868-record PRISMA V2 cohort was retrieved with pollinator-antagonist queries. It is therefore an appropriate discovery frame for **pollinator-antagonist macroecology**, but it is not an unbiased frame for comparing antagonist systems against abiotic multifunctionality such as rain protection or water economy.

V1 therefore separates two lanes:

1. **Primary macro lane — pollinator-antagonist systems.** Complete the frozen 868-record screen, then recode all design-eligible primary systems without conditioning on sign.
2. **Cross-domain comparator lane — later, separate protocol.** Any formal mutualist-antagonist versus mutualist-abiotic comparison requires a prospectively registered matched search with comparable trait/function eligibility. The current two abiotic negative controls remain specificity examples, not the denominator for H1.

## Sign-independent eligibility rule

Within the declared sampling lane, the inferential macroecology sample must be built without conditioning inclusion on the observed sign.

A trait axis/context is design-eligible when:

1. it is a primary plant study;
2. at least two focal functions are linked to one declared trait coordinate or a prospectively declared bounded coordinate;
3. the trait coordinate is split into a separate `trait_axis_id` when another trait in the same study shows a different ecological geometry;
4. the study contains enough directional, optimum, or performance information to classify the relation as opposing, aligned, null/one-sided, or unresolved;
5. the biological unit can be assigned to an independent cluster;
6. the outcome is coded even when no conflict is found.

Positive-only inclusion is prohibited for H1-H3 below.

Eligibility is analysis-specific rather than one omnibus flag:

- `geometry_eligibility` — can this trait axis enter H1 conflict/alignment analysis?
- `context_switch_eligibility` — are at least two comparable ecological contexts observed for this trait axis?
- `cancellation_eligibility` — are component effects commensurate enough to define the H3 cancellation index?
- `design_audit_eligible` — can the study enter H4 as evidence about which design features raise or limit the SCH identification ceiling?

A study may therefore be ineligible for H1 while remaining informative for H4. Shared-receiver studies lacking a common reproductive endpoint are a key example.

## Registered ecological hypotheses

### H1 — ecological structure within pollinator-antagonist systems predicts opposition

Among sign-independently design-eligible same-coordinate cases from the frozen pollinator-antagonist sampling frame:

`conflict_detected ~ antagonist_guild + trait_domain + interaction_timing + pollinator_guild + common_fitness_endpoint`

Where sample size permits, antagonist guild is resolved as florivory/herbivory, seed predation, nectar larceny, oviposition/brood exploitation, grazing, or other prospectively frozen classes. The primary fixed-role H1 excludes `ROLE_DEPENDENT` and `BENEFIT_COST_COUPLED` cases; both are retained as ecological boundary strata rather than recoded as antagonistic by name alone.

Interpretation ceiling: an association within the screened published pollinator-antagonist evidence universe, not natural prevalence and not a causal antagonist effect unless the moderator itself is experimentally manipulated.

A later cross-domain H1b may compare mutualist-antagonist with mutualist-abiotic systems only after the matched comparator search is registered and completed.

### H2 — conflict geometry changes across ecological context

Among systems observed in at least two ecological contexts:

`context_shift_detected ~ antagonist_pressure_or_identity + pollinator_identity + spatial_replication + temporal_replication + trait_domain`

The denominator must be restricted to systems with an actual opportunity to observe switching. Experimental and observational context changes are coded separately.

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

Multiple trait coordinates from one programme are nested trait axes, and repeated populations, years, treatments, or consumer regimes are context cases nested inside those axes. Neither operation creates new independent biological clusters.

The planned hierarchy is therefore:

`context case -> trait axis -> biological cluster -> taxon/lineage`

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

The next data task is to complete/recode the frozen pollinator-antagonist screen into the cluster/trait-axis/context architecture without looking at the desired macroecological result while setting eligibility. The current 117 included primary studies can be coded prospectively as an interim build, but inferential H1-H4 remain closed until the frozen screen and full-text decisions are complete. Cross-domain mutualist-abiotic comparison requires a separate matched search and is not licensed by the 868-record cohort.
