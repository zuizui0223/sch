# SCH Pedicularis CAL-B target-freeze contract v1

## Purpose

CAL-B converts exploratory P1/G pilot summaries into seven prospectively frozen
decision targets while keeping the pilot observations and the confirmatory
cutoffs explicitly separate.

The seven CAL-B targets are:

```text
P1 minimum pollen-grain increase
P1 minimum initial-seed-set increase
G minimum early-attack reduction
G minimum predation-fraction reduction
G minimum final intact-seed gain
G earliest allowed barrier time
G latest allowed barrier time
```

Pilot means and quantiles are context, not automatic targets.

The three G effect targets and the two G timing targets come from different
biological cohorts. G effectiveness/selectivity comes from `CAL_B_G`; timing
comes from natural-state `CAL_B_G_TIMING` sentinels. Investigator-selected
`barrier_application_time_hours` is not a natural-history timing target.

## Step 1 — materialize observed pilot descriptors

Template:

```text
empirical/architecture/PEDICULARIS_CAL_B_TARGET_TEMPLATE_V1.csv
```

Run:

```bash
python scripts/materialize_pedicularis_cal_b_observed.py \
  <calibration_summary.json> \
  empirical/architecture/PEDICULARIS_CAL_B_TARGET_TEMPLATE_V1.csv \
  <cal_b_targets_observed.csv> \
  --receipt <cal_b_observed_receipt.json>
```

This copies only:

```text
population / season
observed n
observed mean
observed q05
observed median
observed q95.
```

It leaves the following fields as `REQUIRED_BEFORE_USE`:

```text
target_value
target_basis_note
frozen_before_confirmatory_data
frozen_at_utc
status.
```

## Step 2 — choose the biological target prospectively

For each row, define a target using a biological or method rationale that is
not simply 'the pilot mean passed.'

Allowed basis components can include:

- a minimum biological effect judged worth detecting;
- measurement precision from CAL-A;
- an externally justified natural-history constraint;
- method-feasibility constraints;
- a predeclared compromise between biological relevance and field feasibility.

The target may differ from the pilot mean. That difference is expected and is
recorded explicitly.

Set:

```text
frozen_before_confirmatory_data = YES
status = PEDICULARIS_CAL_B_TARGET_PROSPECTIVELY_FROZEN
```

and use a timezone-aware `frozen_at_utc` timestamp.

## Step 3 — validate the seven-target freeze

Run:

```bash
python scripts/freeze_pedicularis_cal_b_targets.py \
  <completed_cal_b_targets.csv> \
  --output <cal_b_target_freeze_receipt.json>
```

A positive receipt has:

```text
receipt_schema_version = SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1
status = PEDICULARIS_CAL_B_TARGETS_FROZEN.
```

The five minimum-effect targets must be strictly positive.

The G timing bounds must satisfy:

```text
0 <= lower < upper.
```

## Step 4 — transfer effect boundaries into CAL-C

The five effect targets are the CAL-C power boundaries for the matching
criteria. Avoid manual retyping by running:

```bash
python scripts/apply_pedicularis_cal_b_to_cal_c.py \
  <cal_b_target_freeze_receipt.json> \
  <cal_c_criteria_with_pilot_sd.csv> \
  <cal_c_criteria_with_effect_boundaries.csv> \
  --receipt <cal_b_to_cal_c_receipt.json>
```

This bridge fills only:

```text
boundary
basis_note
```

for the five effect criteria.

It does not fill:

```text
assumed_true_value.
```

The two timing targets do not enter CAL-C because they are method timing
requirements rather than sample-size criteria. They later enter the G field
config directly during F0 assembly.

## Separation from confirmatory data

CAL-B rows come from `CAL_B_P1`, `CAL_B_G` and `CAL_B_G_TIMING`
calibration cohorts and therefore remain:

```text
threshold_basis_eligible = YES
confirmatory_eligible    = NO.
```

The same flower-level outcomes may not be reused for the confirmatory P1 or G
receipts. G event-time flowers must also be disjoint from G barrier-effect
flowers so the natural chronology is not altered by the exclusion treatment.

## What CAL-B may not do

CAL-B must not:

- equate the pilot mean with the target automatically;
- choose the timing window after looking at confirmatory G outcomes;
- use a nonsignificant contamination effect as proof of equivalence;
- change a target later because CAL-C produces an inconvenient sample size;
- generate `PEDICULARIS_POLLINATION_WEIGHT_VALIDATED`;
- generate `PEDICULARIS_PREDATOR_METHOD_VALIDATED`.

## Claim ceiling

A positive CAL-B target receipt establishes only that the seven exploratory
effect/timing targets were prospectively defined with explicit pilot context
and rationale.

It does not establish P1/G validity, causal compromise, conflict budget L, or
dimensional release.
