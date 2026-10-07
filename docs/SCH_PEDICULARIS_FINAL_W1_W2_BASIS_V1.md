# Pedicularis rex final three W1/W2 power-basis inputs v1

## Purpose

After a precision-qualified independent geometry pilot materializes the 18
geometry/variance paths, the canonical W1/W2 basis ledger still has three
blocking paths:

```text
generating_model.z_levels
generating_model.realized_z_sd
production_surface_config.sch_surface.*
```

These do **not** require another biological experiment.

They are resolved from two sources that are already part of the registered
same-context programme:

1. the positive randomized P0 manipulation experiment;
2. a prospective full-surface decision-threshold freeze made before geometry
   outcomes are used and before confirmatory P2 outcomes.

The machine route is:

```text
scripts/freeze_pedicularis_full_surface_thresholds.py
scripts/materialize_pedicularis_w1_w2_final_p0_f0_basis.py
scripts/bind_pedicularis_w1_w2_p0_f0_config.py
```

## 1. What z grid is powered

The physical manipulation is identified by the frozen
`manipulation_setting_id`.

The power generator, however, needs a numeric nominal z value for each
validated setting.

For each validated P0 rank k:

```text
z_nominal,k = mean(realized_exsertion | validated setting k).
```

The registered power z grid is the ordered vector of these same-context means.

This is deliberately not:

- the name Z0/Z1/...;
- a nominal bending target invented before field calibration;
- a published congeneric exsertion value.

It is the phenotype actually delivered, on average, by each validated physical
P0 manipulation setting in the focal population/season.

The P2 allocator still carries the exact physical `manipulation_setting_id`.
The numeric target is a design/power coordinate; the final analysis still uses
flower-level `realized_exsertion`.

## 2. What realized_z_sd means

The power generator adds flower-level variation around each nominal z level.

The same-context estimate is therefore:

```text
e_ik = realized_z_ik - mean(realized_z | rank k)

realized_z_sd
  = sqrt( sum(e_ik^2) / (N - K) )
```

where K is the number of validated z levels.

This pooled within-level SD includes the variation actually produced around a
fixed manipulation setting in the focal P0 experiment.

It is not recovered from published morphology, population-wide natural z
variance, or the later confirmatory P2 outcome.

The positive P0 receipt fingerprints the exact raw P0 dataset. If those rows
change after validation, final-three materialization fails.

## 3. Freeze the primary full-surface decision rules

The primary SCH surface has decision thresholds such as:

```text
min_interior_bootstrap_fraction
min_optimum_separation
min_optimum_shift
min_abs_component_gradient
```

plus the registered z-level/bootstrap-quality rules.

These are **decision rules**, not nuisance parameters to estimate from the
geometry pilot.

Before geometry outcomes are used to construct power truth, create a frozen
full-surface config and threshold receipt:

```bash
python scripts/freeze_pedicularis_full_surface_thresholds.py \
  <frozen_full_surface_config.json> \
  <surface_threshold_freeze.json> \
  --output <surface_threshold_freeze_receipt.json>
```

The config must have:

```text
status = PEDICULARIS_FULL_SURFACE_CONFIG_PROSPECTIVELY_FROZEN
```

and the freeze receipt requires one explicit basis note for every registered
full-surface decision path: the `sch_surface` thresholds **and** the
water-depth / mechanical-damage system-check tolerances.

The receipt fingerprints the exact:

```text
sch_surface
system_checks
analysis config = {sch_surface, system_checks}.
```

The threshold values may not be selected from the geometry pilot or P2
outcomes. The system-check notes should point back to the relevant same-context
CAL-A / P0 / G handling-equivalence basis rather than being convenient
post-hoc tolerances.

## 4. Materialize the final three ledger rows

After P0 is positive and the geometry pilot has already promoted the 18
same-estimand geometry/variance rows, run:

```bash
python scripts/materialize_pedicularis_w1_w2_final_p0_f0_basis.py \
  <completed_locked_P0.csv> \
  <positive_P0_receipt.json> \
  <frozen_full_surface_config.json> \
  <surface_threshold_freeze_receipt.json> \
  --ledger <basis_after_geometry.csv> \
  --ledger-out <basis_zero_blocker.csv> \
  --receipt-out <final_p0_f0_basis_receipt.json>
```

Only three paths are changed:

```text
generating_model.z_levels
  -> DIRECT_SAME_CONTEXT_READY

generating_model.realized_z_sd
  -> DIRECT_SAME_CONTEXT_READY

production_surface_config.sch_surface.*
  -> REGISTERED_THRESHOLD_READY.
```

If the geometry 18 paths were already ready, the normal basis audit becomes:

```text
n_blocking_rows = 0

registered_single_scenario_n_basis_ready = true

PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N.
```

If other blockers remain, the receipt is only partial and does not authorize
registered n.

## 5. Bind the final power config to those values

A zero-blocker ledger is not enough if someone can type different z values,
noise or thresholds into the simulator.

Bind the frozen W1/W2 power config to the exact final-three evidence:

```bash
python scripts/bind_pedicularis_w1_w2_p0_f0_config.py \
  <frozen_w1_w2_power_config.json> \
  <final_p0_f0_basis_receipt.json> \
  <zero_blocker_basis_receipt.json> \
  <surface_threshold_freeze_receipt.json> \
  --output <p0_f0_config_binding.json>
```

The binding requires exact equality for:

```text
power generating_model.z_levels
    == P0 validated setting means

power generating_model.realized_z_sd
    == P0 pooled within-level realized-z SD

power production_surface_config.sch_surface
    == frozen full-surface sch_surface

power production_surface_config.system_checks
    == frozen full-surface system_checks.
```

It fingerprints the entire power config and zero-blocker basis receipt.

## 6. Registered W1/W2 power now needs two independent bindings

A registered FROZEN run requires both:

```text
geometry_config_binding
  -> exact precision-qualified 18-path geometry/variance evidence

p0_f0_config_binding
  -> exact final three P0 / prospective-threshold inputs.
```

Run:

```bash
python scripts/simulate_pedicularis_w1_w2_power.py \
  <frozen_w1_w2_power_config.json> \
  --basis-receipt <zero_blocker_basis_receipt.json> \
  --geometry-binding <geometry_config_binding.json> \
  --p0-f0-binding <p0_f0_config_binding.json> \
  --output <registered_w1_w2_power.json>
```

Only then may the receipt set:

```text
registered_field_allocation_recommendation_allowed = true.
```

## 7. Keep the same primary thresholds in the actual P2 analysis

The registered power receipt carries the SHA-256 of the exact production
surface analysis config.

P2 allocation, field lock and complete field verification carry that fingerprint
forward.

The production analyzer recomputes:

```text
SHA256({
  sch_surface: supplied analysis sch_surface,
  system_checks: supplied analysis system_checks
})
```

and rejects the final dataset if it differs from the config used in the
registered power calculation.

Thus the programme cannot:

```text
power under one optimum-shift threshold
then
analyze P2 under another.
```

## Claim ceiling

This closes design-input provenance.

It does not:

- make the P0 z means true biological optima;
- make P0 rows part of confirmatory P2;
- estimate the 18 causal geometry/variance inputs;
- choose the biological primary thresholds;
- produce a W0-W5 result;
- guarantee that any candidate n reaches the requested power.

It only ensures that, once the basis is complete, the registered power
calculation and the final P2 analysis use the same prospectively justified
inputs.
