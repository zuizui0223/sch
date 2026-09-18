# SCH macroecology P1 manual-gate frontier V1

## Scope

The sign-blind machine pretriage identified 47 current primary-study records with:

```text
pollinator response
+ antagonist response
+ common reproductive outcome
```

These 47 records have now all passed through manual source-level design adjudication.

No ecological outcome sign was used to determine the design gate.

## Complete P1 gate

```text
machine P1 records                    47
manually gated P1 records             47
missing manual gates                   0
```

Geometry status:

```text
ELIGIBLE_SAME_COORDINATE              10
ELIGIBLE_BOUNDED_COORDINATE           22
BOUNDARY_BENEFIT_COST_COUPLED          1
INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY    7
INELIGIBLE_MULTIVARIATE_UNRESOLVED     5
UNRESOLVED_SOURCE                      2
```

Therefore the current record-level H1 candidate frontier is:

```text
H1 geometry candidate records = 32
```

This is a record count, not an independent biological-cluster count.

## H2 context frontier

Twenty of the 47 P1 records contain a repeated ecological context that is usable enough to proceed toward context-case decomposition.

```text
H2 repeated-context candidate records = 20
```

Repeated contexts include populations, sites, disturbance regimes, consumer assemblages, common-garden provenance contrasts, and other source-declared ecological settings.

## Trait-axis decomposition is now the main bottleneck

The 47 P1 records are not equivalent to 47 trait axes.

```text
SPLIT_REQUIRED = 25
SINGLE_AXIS    = 17
NO_AXIS_PROMOTION / H4-only = 4
SPLIT_FOR_H4  = 1
```

Thus more than half of the P1 records require explicit separation into trait axes before conflict/alignment outcomes can be analyzed.

This is not a nuisance detail. It is a biological result of the literature architecture: many studies report “floral phenotype”, “display”, or “trait bundle” while different traits can experience different ecological geometry.

## Why 47 P1 records shrink to 32 H1 candidates

Having both consumer responses and a common reproductive outcome is necessary but not sufficient.

The 15 non-H1 P1 records fail or stop for distinct reasons:

- the two functional routes do not actually respond to the same declared trait coordinate;
- several trait dimensions are bundled and cannot yet be separated;
- the source does not contain enough trait-level detail;
- one interaction is benefit-cost coupled rather than a fixed mutualist-antagonist pair.

These are precisely the inference failures SCH was designed to make visible.

## Relationship to the full 117-study universe

Current workflow:

```text
117 primary includes
  ↓ sign-blind machine pretriage
47 P1: both responses + common fitness
  ↓ complete manual source gate
32 record-level H1 geometry candidates
  ↓ trait-axis decomposition + programme clustering
final independent trait-axis sample
  ↓ context-case decomposition
registered H1/H2/H3 models
```

The other 70 primary-study records remain informative for the H4 design audit and for boundary analyses. They are not discarded.

## Immediate next step

The next high-value operation is no longer broad study screening.

It is:

1. split the 32 H1 candidate records into declared trait axes;
2. cluster overlapping papers into independent biological programmes;
3. create repeated context cases where supported;
4. only then code conflict, alignment, one-sided/null, cancellation, and role boundaries.

## Claim ceiling

```text
P1_MANUAL_GATE = COMPLETE
P1_RECORDS = 47
H1_RECORD_LEVEL_CANDIDATES = 32
H2_CONTEXT_CANDIDATE_RECORDS = 20
TRAIT_AXIS_SPLIT_REQUIRED_RECORDS = 25

INDEPENDENT_H1_CLUSTER_N = NOT_YET_ESTIMATED
CONFLICT_PREVALENCE = NOT_ESTIMATED
H1_H2_H3_MODELS = NOT_FIT
FULL_MACRO_INFERENCE = CLOSED
```
