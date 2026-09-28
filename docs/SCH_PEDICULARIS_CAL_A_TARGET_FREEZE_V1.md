# SCH Pedicularis CAL-A target-freeze contract v1

## Purpose

CAL-A defines the 20 separation/equivalence targets that guard P0/P1/G
selectivity before confirmatory data are interpreted.

The workflow keeps three layers distinct:

```text
pilot-observed variation
same-flower measurement noise
prospectively chosen biological margin/separation.
```

No layer is automatically substituted for another.

## Step 1 — materialize pilot and repeatability context

Template:

```text
empirical/architecture/PEDICULARIS_CAL_A_TARGET_TEMPLATE_V1.csv
```

Run:

```bash
python scripts/materialize_pedicularis_cal_a_observed.py \
  <calibration_summary.json> \
  <repeatability_summary.json> \
  empirical/architecture/PEDICULARIS_CAL_A_TARGET_TEMPLATE_V1.csv \
  <cal_a_targets_observed.csv> \
  --receipt <cal_a_observed_receipt.json>
```

This materializes all 20 pilot distributions and, where available, the q95
same-flower measurement-noise quantity from CAL-A repeatability.

Current coverage:

```text
20 CAL-A targets total
13 with direct measurement-noise q95
 7 without a directly matched repeatability metric.
```

The target fields remain unresolved.

## Step 2 — choose target separation/margins prospectively

The 20 targets contain:

```text
P0   1 minimum realized-z separation + 7 upper tolerances
P1   6 upper selectivity tolerances
G    6 upper selectivity tolerances.
```

A target must have an explicit biological/method basis. Pilot q95 and
measurement-noise q95 are supporting context, not automatic cutoffs.

For a gate with a direct repeatability metric, the target must be strictly
larger than the recorded measurement-noise q95. This is only a necessary
measurement-resolution floor; it is not sufficient biological justification.

Freeze each row with:

```text
frozen_before_confirmatory_data = YES
status = PEDICULARIS_CAL_A_TARGET_PROSPECTIVELY_FROZEN
```

plus a timezone-aware timestamp and nonempty target basis note.

## Step 3 — validate CAL-A freeze

Run:

```bash
python scripts/freeze_pedicularis_cal_a_targets.py \
  <completed_cal_a_targets.csv> \
  --output <cal_a_target_freeze_receipt.json>
```

A positive receipt has:

```text
receipt_schema_version = SCH_PEDICULARIS_CAL_A_TARGET_FREEZE_V1
status = PEDICULARIS_CAL_A_TARGETS_FROZEN.
```

## Step 4 — transfer all 20 targets into CAL-C

Run:

```bash
python scripts/apply_pedicularis_cal_a_to_cal_c.py \
  <cal_a_target_freeze_receipt.json> \
  <cal_c_criteria_with_pilot_sd.csv> \
  <cal_c_after_cal_a.csv> \
  --receipt <cal_a_to_cal_c_receipt.json>
```

This copies only:

```text
boundary
basis_note.
```

It does not populate `assumed_true_value`.

Then apply the positive CAL-B receipt. CAL-A and CAL-B are disjoint by gate
path, so the two bridges together fill all 25 CAL-C boundaries:

```text
CAL-A 20
+ CAL-B 5
---------
CAL-C 25/25 boundaries populated
assumed_true_value 25/25 still prospectively unresolved.
```

## Relation to F0

The CAL-A receipt later supplies its 20 values directly to the final P0/P1/G
config assembly. CAL-C supplies the eight sample-size fields and CAL-B supplies
its seven effect/timing fields.

Together with the five registered-contract values these four sources close the
40-field F0 decision-rule set without manually inventing a value.

## What CAL-A may not do

CAL-A must not:

- set every margin equal to q95 measurement noise;
- set every margin equal to the exploratory pilot q95;
- use confirmatory rows to estimate a margin;
- widen a margin later to rescue a failed confirmatory intervention;
- validate P0/P1/G;
- set sample size.

## Claim ceiling

A positive CAL-A receipt establishes only that the 20 separation/equivalence
targets were prospectively defined with pilot context, measurement-precision
context where available, and explicit rationale.

It does not establish manipulation selectivity, functional conflict, causal
compromise, conflict budget L, or dimensional release.
