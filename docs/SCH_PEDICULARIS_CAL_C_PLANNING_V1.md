# SCH Pedicularis CAL-C power / precision planning contract v1

## Purpose

CAL-C resolves the eight sample-size fields that remain open after CAL-A and
CAL-B have supplied measurement/variability information plus prospectively
chosen equivalence margins and minimum useful intervention effects.

CAL-C is a planning layer only. It must not move a biological gate boundary
because the calculated sample size is inconvenient.

## Inputs

### Threshold-free calibration summary

First generate the descriptive calibration summary with:

```bash
python scripts/summarize_pedicularis_calibration_pilots.py \
  --p0 <p0_calibration.csv> \
  --p1 <p1_calibration.csv> \
  --g  <g_calibration.csv> \
  --output <calibration_summary.json>
```

All three lanes are required for a complete CAL-C plan.

### Criterion table

Template:

```text
empirical/architecture/PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv
```

It contains 25 planning criteria:

```text
P0   8
P1   8
G    9
```

Two damage-rate criteria are binomial upper-bound problems. The remaining
23 criteria use plant-level pilot SDs.

Populate only pilot SD and its exact source path with:

```bash
python scripts/materialize_pedicularis_cal_c_pilot_sd.py \
  <calibration_summary.json> \
  empirical/architecture/PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv \
  <cal_c_criteria_with_sd.csv> \
  --receipt <pilot_sd_receipt.json>
```

This step deliberately leaves the following fields unresolved:

```text
boundary
assumed_true_value
basis_note
```

The pilot mean is therefore never silently promoted to the assumed true value
used for power planning.

### Planning config

Template:

```text
empirical/architecture/PEDICULARIS_CAL_C_PLANNING_CONFIG_TEMPLATE_V1.json
```

The registered confirmatory evaluators use 95% intervals, so CAL-C V1 requires:

```text
confidence_level = 0.95
```

The following are prospective planning choices and must be frozen before the
confirmatory data are read:

```text
familywise_target_power
lane-specific design_effect
flowers_per_plant_per_cell
population_id
season_id
basis_document.
```

The planning provenance status is:

```text
PEDICULARIS_CAL_C_INPUTS_PROSPECTIVELY_FROZEN
```

and every criterion row must match its population and season.

## Familywise planning rule

Within a lane all registered criteria must pass. If a lane contains k criteria
and the requested familywise pass probability is P_F, CAL-C allocates the
failure probability using the union bound:

```text
P_each = 1 - (1 - P_F) / k.
```

This is deliberately conservative and does not assume independent criteria.

## Continuous boundary calculation

For a plant-level criterion with pilot SD sigma, boundary b, assumed true
value mu, and distance d to the successful side of the boundary:

```text
d = mu - b    for LOWER criteria
d = b - mu    for UPPER criteria.
```

The normal planning approximation is:

```text
n_raw = ceil( ((z_95CI + z_power) * sigma / d)^2 ).
```

The CI term matches the registered 95% confirmatory gate semantics. A
lane-specific explicit design effect then inflates the planned unit count:

```text
n_inflated = ceil(n_raw * design_effect).
```

If the assumed true value is not on the successful side of the boundary,
planning fails closed.

## Binomial damage-rate calculation

P0 and P1 mechanical-damage criteria use the exact probability, under the
prospectively specified assumed true damage rate, that the 95% Wilson upper
confidence bound is at or below the registered damage-rate ceiling.

The smallest n reaching the per-criterion target probability is found by exact
enumeration of binomial outcome probabilities. That observation requirement is
converted to a plant requirement using the frozen flowers-per-plant-per-cell
assumption and explicit design-effect inflation.

## Lane sample size

For every criterion CAL-C reports:

```text
raw_required_units
inflated_required_units
required_plants
required_flowers_per_cell
pilot_sd_source.
```

The lane sample size is the maximum required plant count across all of its
criteria. Criteria attaining that maximum are retained as driving_criteria.

## Eight CAL-C outputs

A successful plan returns exactly these F0 sample-size fields:

```text
stage_p0.min_plants
stage_p0.min_flowers_per_level

pollination_weight.min_paired_plants
pollination_weight.min_flowers_per_treatment

method_gate.min_paired_plants
method_gate.min_flowers_per_treatment

predator_weight.min_paired_plants
predator_weight.min_flowers_per_treatment.
```

The two G blocks receive the same planned paired-plant and flower requirement
because they are evaluated from the same confirmatory G package.

## Run

After pilot SDs, gate boundaries, assumed true values, basis notes, familywise
power, design effects and flowers-per-plant assumptions are prospectively
frozen:

```bash
python scripts/plan_pedicularis_cal_c.py \
  <completed_cal_c_criteria.csv> \
  <completed_cal_c_planning_config.json> \
  --output <pedicularis_cal_c_plan.json>
```

A valid output has:

```text
status = PEDICULARIS_CAL_C_SAMPLE_SIZE_PLAN_READY
```

The eight sample-size values must then be transferred into the final P0/P1/G
configs together with CAL-C provenance before the global F0 freeze can pass.

## What CAL-C may not do

CAL-C must not:

- set a biological effect target from the sample size that happens to be affordable;
- widen a CAL-A equivalence margin to lower n;
- enlarge a CAL-B minimum useful effect to lower n;
- use confirmatory data as pilot variability;
- treat pilot means as assumed true effects without an explicit prospective basis;
- claim that a planned n guarantees success under model misspecification.

## Claim ceiling

CAL-C supports prospective sample-size/precision gate values only under the
declared pilot variability, assumed true values, familywise power target,
flowers-per-plant design and design-effect scenario.

It does not establish P0/P1/G validity, functional conflict, causal compromise,
pure-function optima, conflict budget L, or dimensional release.
