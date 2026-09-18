# SCH macroecology expansion protocol V1

## Objective

Convert the existing SCH literature infrastructure into a comparative ecological layer without weakening the identification rules of the main paper.

The immediate macroecology question is restricted to the sampling frame that SCH already owns:

> **Within plant pollinator-antagonist systems, which ecological and design features are associated with opposition, context switching, compromise, or cancellation on multifunctional floral traits?**

Cross-domain comparison against abiotic multifunctionality is deferred to a separately registered matched search.

## Existing source base

The frozen PRISMA V2 cohort contains 868 records identified by pollinator-antagonist search queries.

At the current V20 screening state:

```text
frozen denominator                868
title/abstract screened           405
retained for full text            277
full-text included primary        117
full-text excluded                131
current full-text undecided        29
title/abstract unscreened         463
```

The 117 currently included primary studies form an **interim recoding queue**, not the final macroecology denominator.

## Stage A — automatic queue construction

`scripts/build_sch_macroecology_primary_candidates.py` merges the frozen candidate registry with every versioned screening overlay and exports all current `screen_fulltext == INCLUDE` records together with a machine-readable receipt.

The queue copies source metadata and leaves all macroecology judgments blank. This prevents screening decisions from being silently converted into ecological outcomes.

Required blank-at-entry fields include:

```text
cluster_id
trait_domain
function_pair_family
antagonist_guild
pollinator_guild
shared_coordinate_status
context_axes_present
conflict_detected
alignment_detected
context_shift_detected
compromise_detected
cancellation_detected
macro_design_eligible
macro_eligibility_reason
coding_status
coding_note
```

## Stage B — blind design eligibility

Eligibility is adjudicated before coding the desired ecological sign.

Order:

1. verify primary study;
2. identify the focal trait coordinate;
3. determine whether at least two focal functions can be linked to that coordinate;
4. determine whether direction/optimum/performance information is sufficient for a geometry classification;
5. assign independent biological cluster;
6. only then code opposition/alignment/context outcomes.

Required eligibility outcomes:

- `ELIGIBLE_SAME_COORDINATE`
- `ELIGIBLE_BOUNDED_COORDINATE`
- `INELIGIBLE_MULTIVARIATE_UNRESOLVED`
- `INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY`
- `INELIGIBLE_NOT_PRIMARY`
- `UNRESOLVED_SOURCE`

No study is excluded because its result is null, aligned, one-sided, or contrary to SCH.

## Stage C — cluster and context decomposition

One `cluster_id` represents an independent biological programme/system.

Repeated observations become context cases rather than independent clusters:

```text
cluster
  -> population/site
  -> year/season
  -> treatment/consumer regime
  -> local ecological geometry
```

The context-case table is used whenever a source reports multiple populations, years, guilds, or treatments. This is required for the context-switch analysis.

## Stage D — ecological coding

### Antagonist guild

Prospective top-level classes:

- `FLORIVORE_HERBIVORE`
- `SEED_PREDATOR`
- `NECTAR_LARCENIST`
- `OVIPOSITOR_BROOD_EXPLOITER`
- `GRAZER_VERTEBRATE`
- `MULTIPLE_ANTAGONISTS`
- `OTHER`
- `UNRESOLVED`

### Interaction timing

- `SIMULTANEOUS_OR_OVERLAPPING`
- `SEQUENTIAL_LIFE_HISTORY_FILTER`
- `TEMPORALLY_SEPARATED`
- `UNRESOLVED`

### Trait domain

Use the controlled V1 classes in `SCH_MACROECOLOGY_SCHEMA_V1.md`. Composite/multivariate traits remain visible and are not silently promoted to same-coordinate cases.

## Stage E — registered analyses

### Analysis 1: conflict geometry

Primary unit: independent cluster, using only sign-independently eligible same/bounded-coordinate systems.

Candidate model:

```text
conflict_detected
~ antagonist_guild
+ trait_domain
+ interaction_timing
+ pollinator_guild
+ common_fitness_endpoint
```

If binary event/non-event counts are too sparse for stable regression, report exact/descriptive estimates with uncertainty rather than forcing a multivariable model.

### Analysis 2: context switching

Primary unit: context cases nested within clusters that contain at least two observable ecological contexts.

Candidate model:

```text
context_shift
~ antagonist_pressure_or_identity
+ pollinator_identity
+ spatial_context
+ temporal_context
+ trait_domain
+ (1 | cluster_id)
```

A system with only one observed context is not a negative for switching.

### Analysis 3: cancellation

Restrict to studies where opposing components are expressed on the same outcome scale with compatible orientation.

```text
cancellation_index
= 1 - |sum(beta_j)| / sum(|beta_j|)
```

Missing covariance is retained as missing. Cancellation magnitude is descriptive unless valid uncertainty can be propagated.

### Analysis 4: identification ceiling

Model whether design structure predicts the highest SCH claim that can be licensed.

Predictors:

- focal trait manipulated;
- consumer context manipulated;
- common reproductive endpoint;
- multilevel trait surface;
- repeated ecological context;
- uncertainty/covariance completeness.

This is a methods/ecology interface result and should be kept separate from the biological moderator models.

## Stage F — geography and climate

Only after study-locality provenance is frozen:

1. normalize locality;
2. recover coordinates from source-supported location text;
3. retain provenance;
4. attach climate variables;
5. test geographic/climatic moderators conditionally on the screened study universe.

Do not infer coordinates from species ranges when the study locality is not known.

## Cross-domain comparator protocol

The present 868-record cohort cannot estimate a mutualist-antagonist versus mutualist-abiotic contrast because its search strategy was built around antagonists.

A later comparator search must therefore:

1. reuse the same floral-trait concept families;
2. replace the antagonist concept block with prospectively declared abiotic/function blocks such as rain protection, water economy, thermal protection, or mechanical protection;
3. freeze its own denominator;
4. use the same sign-independent eligibility and cluster rules;
5. include a sampling-frame indicator in any merged comparison.

Until then, Abelia and Platycodon remain valid negative/specificity examples but not an unbiased comparison denominator.

## Promotion gate to manuscript result

No macroecology claim is promoted into the SCH Viewpoint until all of the following are true:

```text
FROZEN_868_SCREEN_COMPLETE
FULLTEXT_DECISIONS_COMPLETE
INDEPENDENCE_CLUSTERING_COMPLETE
SIGN_INDEPENDENT_MACRO_ELIGIBILITY_COMPLETE
CONTEXT_CASE_DECOMPOSITION_COMPLETE
SOURCE_VERIFICATION_COMPLETE
MODEL_SPECIFICATION_FROZEN
```

Before that point, seed and interim queue summaries are development readouts only.

## Current implementation status

```text
SCHEMA_V1                         READY
16_CLUSTER_SEED                  READY
NONEXCLUSIVE_OUTCOME_AXES        READY
CONTEXT_CASE_TEMPLATE            READY
117_PRIMARY_CANDIDATE_BUILDER    READY
INFERENTIAL_MACRO_SAMPLE         NOT_READY
CROSS_DOMAIN_COMPARATOR          NOT_STARTED
```
