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

## Machine files

```text
empirical/architecture/PEDICULARIS_W1_W2_POWER_CONFIG_TEMPLATE_V1.json
scripts/simulate_pedicularis_w1_w2_power.py
tests/test_pedicularis_w1_w2_power.py
```

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

The value of `realized_z_sd` must come from the same-context P0 calibration or
a prospectively labelled sensitivity scenario. It must not be tuned after the
full-surface result is seen.

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
