# SCH Pedicularis CAL-A repeatability contract v1

## Purpose

CAL-A needs to distinguish three different quantities before any equivalence
margin or minimum realized-z separation is frozen:

```text
measurement noise
natural flower-to-flower variation
true manipulation / handling effects.
```

This contract isolates the first quantity.

It uses repeated measurements of the **same calibration flowers** and returns
measurement-repeatability summaries only.

It does not choose a field threshold.

## Input

Template:

```text
empirical/architecture/PEDICULARIS_CAL_A_REPEATABILITY_TEMPLATE_V1.csv
```

Analyzer:

```text
scripts/summarize_pedicularis_cal_a_repeatability.py
```

Required fields:

```text
population_id
season_id
plant_id
flower_id
measurement_replicate
observer_id
realized_exsertion
corolla_opening_width
lower_lip_angle_deg
tube_diameter
bract_height
water_depth
flower_orientation_deg
```

Each flower requires at least two measurement replicates.

A `flower_id + measurement_replicate` pair must be unique.

## Preferred measurement design

Use calibration flowers that are not later reused as confirmatory flower-level
rows.

Where practical:

```text
same flower
-> replicate 1
-> remove/reposition measuring device
-> replicate 2

observer / image-reading order randomized or blinded where feasible.
```

If observer effects are of interest, distribute replicate measurements across
observers rather than assigning one observer to one treatment or plant block.

## Outputs

For every metric the analyzer reports:

```text
flower-mean distribution
between-flower SD of flower means
pooled within-flower SD
distribution of each flower's maximum absolute deviation from its own mean
```

For scale-free fields used by relative-change gates it also reports:

```text
distribution of each flower's maximum relative deviation from its own mean.
```

Relative summaries are currently produced for:

```text
realized_exsertion
corolla_opening_width
tube_diameter
bract_height.
```

Absolute summaries are the primary measurement-noise basis for:

```text
lower_lip_angle_deg
water_depth
flower_orientation_deg.
```

## How this feeds CAL-A

The repeatability output can support, but does not determine:

- the minimum adjacent realized-exsertion separation in P0;
- morphology equivalence margins;
- water-depth stability margins;
- orientation / lip-angle stability margins;
- scale-free z / opening / bract-height selectivity margins used in P1/G.

The calibration decision should combine measurement noise with biological
meaning and, where relevant, natural within-state variation or sham-handling
variation.

## What not to do

Do not set a margin mechanically to:

```text
q95 measurement noise
observed maximum noise
2 x SD
or any other fixed multiplier
```

unless that rule is prospectively justified in the threshold-basis document.

The analyzer deliberately returns:

```text
CAL_A_REPEATABILITY_SUMMARY_ONLY_NO_MARGIN_DECISION
thresholds_selected = false
confirmatory_receipt_generated = false.
```

## Cohort separation

Register these flowers as:

```text
cohort_role = CAL_A
threshold_basis_eligible = YES
confirmatory_eligible = NO
```

in:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_COHORT_TEMPLATE_V1.csv
```

and validate the execution registry with:

```text
scripts/validate_pedicularis_cohort_registry.py.
```

## Claim ceiling

A repeatability summary supports only the measurement-precision component of
CAL-A.

It does not identify:

```text
a biological equivalence margin
a minimum useful manipulation effect
a sample size
P0 / P1 / G validity
causal compromise.
```
