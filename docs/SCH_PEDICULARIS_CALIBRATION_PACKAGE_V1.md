# SCH Pedicularis calibration package contract v1

## Purpose

This contract defines the complete nonconfirmatory field packet required before
CAL-A/B target freezing and CAL-C planning.

The package contains five biological data bundles plus one cohort registry:

```text
1  CAL-A same-flower repeatability
2  CAL-A exploratory P0 graded-z manipulation
3  CAL-B exploratory P1 supplementation
4  CAL-B exploratory G barrier-effect/selectivity pilot
5  CAL-B natural G event-time pilot
6  calibration/confirmatory cohort registry.
```

All six inputs must refer to the same population and season.

## Required role mapping

```text
repeatability rows -> CAL_A
P0 exploratory    -> CAL_A
P1 exploratory    -> CAL_B_P1
G exploratory     -> CAL_B_G
G event-time       -> CAL_B_G_TIMING.
```

Calibration rows must be:

```text
threshold_basis_eligible = YES
confirmatory_eligible    = NO.
```

## Allowed within-calibration reuse

Same-flower repeatability is intended to measure the same CAL-A flowers before
or as part of the P0 calibration programme.

Therefore:

```text
repeatability flower IDs must be a subset of P0 CAL_A flower IDs.
```

This is the only cross-file flower overlap explicitly allowed by the package
builder.

P0, P1, G effect and G event-time flower IDs must be mutually disjoint.
The event-time cohort is not a relabelled subset of the barrier experiment.

## Confirmatory separation

The cohort registry remains the authority for calibration vs confirmatory
eligibility. A calibration flower cannot later become:

```text
CONFIRMATORY_P0
CONFIRMATORY_P1
CONFIRMATORY_G
FULL_SURFACE.
```

Plant-level overlap is reported by the registry validator. Flower-level
outcome reuse is prohibited.

## Templates

```text
empirical/architecture/PEDICULARIS_CALIBRATION_COHORT_TEMPLATE_V1.csv
empirical/architecture/PEDICULARIS_CAL_A_REPEATABILITY_TEMPLATE_V1.csv
empirical/architecture/PEDICULARIS_STAGE_P0_EXSERTION_TEMPLATE_V1.csv
empirical/architecture/PEDICULARIS_POLLINATION_WEIGHT_TEMPLATE_V1.csv
empirical/architecture/PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V4.csv
empirical/architecture/PEDICULARIS_G_EVENT_TIME_PILOT_TEMPLATE_V1.csv
empirical/architecture/PEDICULARIS_G_EVENT_TIME_PILOT_CONFIG_TEMPLATE_V1.json.
```

## Build

Run:

```bash
python scripts/build_pedicularis_calibration_package.py \
  <cohort_registry.csv> \
  <cal_a_repeatability.csv> \
  <cal_a_p0.csv> \
  <cal_b_p1.csv> \
  <cal_b_g.csv> \
  --g-timing-config <g_event_time_config.json> \
  --g-timing <g_event_time.csv> \
  --repeatability-out <repeatability_summary.json> \
  --calibration-out <calibration_summary.json> \
  --receipt-out <calibration_package_receipt.json>
```

The package builder:

- validates the entire cohort registry;
- checks every data flower is registered in the correct role;
- checks all inputs share one population and season;
- permits repeatability-within-P0 overlap only;
- rejects other cross-lane flower reuse, including G effect vs G event-time;
- requires prospectively frozen event definitions for pollination completion,
  predator attack and ovary swelling;
- requires at least one observed pollination-complete sentinel and one observed
  attack/swelling constraint onset before declaring the package target-freeze ready;
- builds the same-flower repeatability summary;
- builds the threshold-free P0/P1/G/G_TIMING calibration summary.

## Positive package receipt

A valid package has:

```text
receipt_schema_version = SCH_PEDICULARIS_CALIBRATION_PACKAGE_V1
status = PEDICULARIS_CALIBRATION_PACKAGE_READY_FOR_TARGET_FREEZE.
```

It unlocks:

```text
materialize_and_freeze_CAL_A_targets
materialize_and_freeze_CAL_B_targets
materialize_CAL_C_pilot_SD_provenance.
```

## Sequence after package completion

```text
calibration package
  -> CAL-A 20 target freeze
  -> CAL-B 7 target freeze
  -> CAL-A + CAL-B fill CAL-C 25 boundaries
  -> prospectively freeze 25 assumed true values + CAL-C planning assumptions
  -> CAL-C returns 8 sample-size gates
  -> exact F0 assembly 5 + 20 + 7 + 8 = 40
  -> collect separate confirmatory P0/P1/G rows.
```

## Claim ceiling

A positive package receipt establishes only calibration-data integrity and
role/context separation.

It does not select thresholds, choose assumed true effects, set sample size,
validate P0/P1/G, or establish causal compromise.
