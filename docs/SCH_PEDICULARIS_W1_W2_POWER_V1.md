# Pedicularis rex W1/W2 headline power contract v1

## Biological reason

The existing CAL-C planner answers a necessary but different question:

> how many plants/flowers are needed for P0, P1 and G to pass their registered
> manipulation-validity, selectivity and contamination gates?

That does **not** guarantee enough replication for the final empirical paper.

The biology-first headline is downstream:

```text
valid P0/P1/G
-> fit four z x P x G reproductive surfaces
-> recover the primary causal-compromise surface
-> test whether predator removal shifts the natural-pollination state optimum upward
-> test whether higher randomized z increases pollen receipt
-> assign predeclared W0-W5.
```

The new planner therefore powers the final production pipeline itself.

**Measurement-feasibility caveat:** these simulations currently draw stigmatic
pollen and mature-seed outcomes for every simulated flower. Sun et al. (2016)
measured the former destructively and usually obtained the latter from
different flowers. The simulated W1/W2 probabilities therefore do not
establish that the actual field endpoint pairing is possible. Registered
field allocation requires a separate positive dual-endpoint compatibility
receipt; the power assumptions must also be reviewed against the validated
assay's pollen measurement variance. If split-flower sentinels are used, this
entire joint P2 power route must be redesigned rather than treating sentinel
flowers as independent mature-fruit flowers. See
`docs/SCH_PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_V1.md`.

## Machine files

```text
empirical/architecture/PEDICULARIS_W1_W2_POWER_CONFIG_TEMPLATE_V1.json
scripts/simulate_pedicularis_w1_w2_power.py
tests/test_pedicularis_w1_w2_power.py
```

## Precision-qualified geometry must match the actual power config

A zero-blocker basis receipt certifies that admissible evidence exists. It does
not, by itself, prove that the 18 geometry/variance numbers typed into the final
power config are the values measured by the independent geometry pilot.

For a registered `FROZEN` run, first create an exact binding:

~~~bash
python scripts/bind_pedicularis_w1_w2_geometry_config.py \
  <frozen_power_config.json> \
  <geometry_pilot_summary.json> \
  <geometry_precision.json> \
  <zero_blocker_power_basis_receipt.json> \
  --output <geometry_config_binding.json>
~~~

The binding requires:

~~~text
geometry point summary                 complete
geometry precision receipt             READY_FOR_BASIS
all 18 precision gates                 pass
all 18 frozen config values            exactly match pilot summary
population / season                    identical
~~~

and stores semantic SHA-256 digests of the exact geometry summary, precision
receipt, zero-blocker basis receipt and entire frozen power config.

The final three non-geometry paths are now closed separately by
`docs/SCH_PEDICULARIS_FINAL_W1_W2_BASIS_V1.md`:

~~~text
generating_model.z_levels
  <- means of realized exsertion for each validated physical P0 setting

generating_model.realized_z_sd
  <- pooled within-setting P0 realized-exsertion residual SD

production_surface_config.sch_surface.*
  <- prospective full-surface threshold freeze made before geometry/P2 outcomes.
~~~

After materialization, bind those values to the same frozen power config with:

~~~bash
python scripts/bind_pedicularis_w1_w2_p0_f0_config.py \
  <frozen_power_config.json> \
  <final_p0_f0_basis_receipt.json> \
  <zero_blocker_power_basis_receipt.json> \
  <surface_threshold_freeze_receipt.json> \
  --output <p0_f0_config_binding.json>
~~~

A registered simulator run then requires all three provenance inputs:

~~~bash
--basis-receipt <zero_blocker_power_basis_receipt.json>
--geometry-binding <geometry_config_binding.json>
--p0-f0-binding <p0_f0_config_binding.json>
~~~

Any later edit to the power config or basis receipt invalidates the binding.
Synthetic TEST and sensitivity-envelope runs remain exempt because they cannot
authorize registered P2 field allocation.

This is provenance control after precision qualification; it is not a substitute
for the precision gate itself.

## What is powered

Two power targets are frozen independently:

```text
target_primary_surface_power

target_headline_w1_or_w2_power
```

The second target is the probability that the current production pipeline
assigns either:

```text
W1  enemy-induced optimum displacement
    + positive pollen-receipt slope
    + positive initial-seed slope

or

W2  enemy-induced optimum displacement
    + positive pollen-receipt slope only.
```

Thus the sample size is not chosen from a generic t test or from intervention
validation alone.

## Evidence-basis gate before any registered n

A mathematically runnable power configuration is not automatically a
scientifically admissible sample-size plan.

The generating model contains quantities that the intervention-validity
calibration programme does not identify, especially:

```text
four randomized z x P x G reproductive surfaces
between-plant and residual variance of the final fitness endpoint
state-specific z -> pollen slopes
state-specific z -> initial-seed slopes.
```

The basis ledger is:

```text
empirical/architecture/PEDICULARIS_W1_W2_POWER_BASIS_LEDGER_V1.csv
scripts/audit_pedicularis_w1_w2_power_basis.py
```

Current bounded state:

```text
POWER_BASIS_ROWS                         30
REGISTERED_N_BLOCKERS                    21
CAUSAL_GEOMETRY_ROWS                     12
CAUSAL_GEOMETRY_ROWS_READY                0
REGISTERED_SINGLE_SCENARIO_N             BLOCKED
```

The focal 2016 programme supports the directions
`higher exsertion -> greater pollen receipt` and
`higher exsertion -> greater seed-predator risk`, but it does not identify the
randomized four-state quadratic surfaces, their bounded optima or their
curvatures. Those observational relationships are therefore sensitivity
context, not direct generating truth.

Two routes can remove the block:

```text
A. SEPARATE_NONCONFIRMATORY_P2_GEOMETRY_PILOT
   estimate same-context geometry/variance on data that never enter the
   confirmatory P2 inference;

B. PROSPECTIVELY_FROZEN_ROBUST_MULTI_SCENARIO_ENVELOPE
   freeze a biologically justified scenario set and require the chosen n to
   meet the power targets in every scenario.
```

A single convenient generating scenario with no basis is not a registered
route.

Before committing to Route A, use the Route-B sensitivity diagnostic in
`docs/SCH_PEDICULARIS_W1_W2_POWER_ENVELOPE_V1.md`. It keeps all scenarios
sensitivity-only, reports the worst-case power at each candidate n and the
scenario-specific minimum-n range, and never promotes its own result to a
registered field allocation. This asks whether geometry uncertainty is
operationally important enough to justify the extra pilot cohort.

Route A is implemented in
`docs/SCH_PEDICULARIS_P2_GEOMETRY_PILOT_V1.md`. It uses a separate,
nonconfirmatory randomized z x P x G cohort registered as
`POWER_GEOMETRY_PILOT`. A valid pilot can directly materialize the 18
same-estimand fitness/pollen/initial-seed geometry and variance rows, leaving
only the z-grid, realized-z SD and primary-threshold basis rows unresolved.
Those three are not another field-study requirement: they are materialized from
the already-positive same-context P0 manipulation plus a prospectively frozen
full-surface decision-threshold receipt. The registered n remains blocked until
both the 18-path geometry binding and the final-three P0/F0 binding certify the
same frozen power config.

For a registered power run, first materialize a basis-audit receipt whose state
is:

```text
PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N
```

with zero blockers. Then pass it to:

```bash
python scripts/simulate_pedicularis_w1_w2_power.py \
  <frozen_power_config.json> \
  --basis-receipt <power_basis_receipt.json> \
  --output <w1_w2_power_receipt.json>
```

If the basis is still blocked, the same simulator may only be run with:

```text
status = PEDICULARIS_W1_W2_POWER_SENSITIVITY_SCENARIO_ONLY.
```

Such a run reports candidate powers but returns no registered minimum n and is
rejected by the P2 field allocator.

## Truth world must be frozen

The generating scenario must declare:

```text
target_truth_world = W1 | W2.
```

The simulator refuses to run unless the deterministic generating surfaces are
already on the registered primary-success side:

```text
z_P - z_G >= min_optimum_separation
z_P - z_C >= min_optimum_shift
z_G - z_C <= -min_optimum_shift
combined z_C lies inside the sampled z range
pollinator-component gradient at z_C >= min_abs_component_gradient
antagonist-component gradient at z_C <= -min_abs_component_gradient.
```

Both NATURAL-pollination G states must also have positive true z-to-pollen
slopes.

For W1, both true z-to-initial-seed slopes must be positive.
For W2, the stronger initial-seed tier must be absent in at least one G state.

This prevents selecting a convenient sample size from a generating model that
does not actually represent the biological hypothesis being powered.

## Realized-z uncertainty

The generator includes:

```text
realized_z_sd
```

around each nominal z treatment.

The production analyzers receive the resulting realized exsertion values.
Power therefore declines when manipulation levels overlap, rather than assuming
perfectly realized trait values.

For a registered run, the numeric z grid is the ordered vector of mean
`realized_exsertion` values produced by the validated physical P0 settings.
`realized_z_sd` is the pooled within-setting residual SD from those exact P0
rows. The positive P0 receipt fingerprints the raw dataset used to derive both.
Sensitivity runs may still use explicitly labelled hypothetical values, but
those cannot authorize P2 field allocation.

## Plant-level blocking

The full surface contains:

```text
n_surface_cells = n_z_levels x 2 P states x 2 G states,
with n_z_levels >= 5.
```

Five z levels therefore give 20 cells, six give 24, and so on.

The simulator no longer assumes that every plant can provide 20 focal flowers.

Freeze:

```text
field_design.flowers_per_plant
field_design.allocation_strategy =
  BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1.
```

For each candidate plant count:

```text
n_plants x flowers_per_plant
```

must be divisible by `n_surface_cells`.

The simulator randomizes the 20-cell order, assigns each plant a consecutive
non-repeated block on that cyclic order, and therefore gives every cell exactly
the same total replication.

Examples for five z levels (20 cells):

```text
6 plants x 20 flowers = 120 flowers = 6/cell  (complete block)

10 plants x 4 flowers = 40 flowers = 2/cell   (incomplete block)

20 plants x 5 flowers = 100 flowers = 5/cell  (incomplete block).
```

For six z levels (24 cells), for example:

```text
8 plants x 6 flowers = 48 flowers = 2/cell.
```

Plant ID remains the bootstrap cluster, so incomplete blocking is propagated
through the actual production bootstrap rather than converted into independent
flowers.

## Production pipeline

Every Monte Carlo replicate uses the current canonical code:

```text
analyze_pedicularis_full_surface.py

-> if positive:
   analyze_pedicularis_antagonist_constrained_pollination.py

-> classify_pedicularis_empirical_outcome.py
   -> W0 ... W5.
```

The power planner does not implement a simplified surrogate test.

For each candidate n it returns:

```text
primary_surface_power
enemy_optimum_shift_power
positive_pollen_gradient_both_G_states_power
positive_initial_seed_gradient_both_G_states_power
headline_W1_or_W2_power
strongest_W1_power
target_truth_world_power
W0-W5 probabilities
analysis_failure_fraction.
```

The registered recommendation is the smallest candidate satisfying **both**
the primary-surface and W1/W2 headline power targets.

## Relationship to CAL-C

The two planning layers are sequential, not alternatives:

```text
CAL-C
  powers intervention validity / selectivity gates

then

W1/W2 headline power
  powers the final ecological result conditional on valid interventions.
```

The final full-surface sample size must be at least as demanding as the
registered headline-power design.

A CAL-C-positive design is therefore not automatically a sufficiently powered
empirical-paper design.

## Generating model

The frozen scenario contains:

- the five-or-more nominal z levels;
- realized-z SD;
- four state-specific quadratic fitness surfaces;
- final-seed plant and residual variation;
- pollen intercepts/slopes plus plant/residual variation;
- initial-seed intercepts/slopes plus plant/residual variation;
- ovule count;
- early-attack rates;
- fixed water depth.

Expected initial seed count must be at least expected undamaged mature seed
count at every nominal cell.

Monte Carlo clipping/flooring is reported so a scenario that frequently relies
on impossible boundary corrections can be rejected rather than trusted.

## What this does not establish

Power simulation is planning, not biology.

It does not show that:

- the focal P. rex population is W1 or W2;
- P0/P1/G are valid;
- seed predators move the optimum;
- higher z improves pollen receipt;
- pure pollinator or antagonist optima are identified;
- antagonists maintain pollen limitation.

Those statements remain outcome-dependent.

## Current execution consequence

Before full-surface collection, SCH now needs two distinct sample-size
receipts:

```text
1. CAL-C validity/selectivity plan
2. W1/W2 production-headline power plan.
```

The second plan must use the **actual intended flowers-per-plant blocking
scheme**. If the field allocation changes, rerun the prospective power
simulation before confirmatory outcomes are read.
