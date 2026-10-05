# SCH Pedicularis exploratory G hard-validity pilot planning v1

## Purpose

The independent-G programme now has bounded candidate classes and a fail-fast
hard-validity screen. This contract adds the missing pre-field question:

> How many paired plants must a candidate pass with zero hard failures before
> its per-plant hard-failure probability is bounded below a prospectively
> chosen tolerance?

This is **method-reliability planning**, not effect-size power.

## Hard failures

The exploratory screen already treats the following as hard failures:

```text
pollination window incomplete before barrier
ovary already swollen at barrier
pollinator entry covered
attack already present before barrier
barrier integrity failure
missing/incorrect sham handling on exposed flowers.
```

Any observed hard failure prevents a zero-failure candidate from satisfying
this planning rule as implemented.

## Exact zero-failure rule

If `n` paired plants show zero hard failures, the one-sided exact upper bound
for the true per-plant failure probability is:

```text
p_upper = 1 - (1 - confidence)^(1/n).
```

The planner finds the smallest integer n such that:

```text
p_upper <= prospectively frozen maximum acceptable hard-failure probability.
```

Examples at 95% confidence:

```text
maximum acceptable failure probability  0.10 -> n = 29 / candidate
maximum acceptable failure probability  0.05 -> n = 59 / candidate.
```

These examples are mathematical consequences, not default tolerances.

## Inputs

Template:

```text
empirical/architecture/PEDICULARIS_G_HARD_VALIDITY_PLANNING_CONFIG_TEMPLATE_V1.json
```

Before exploratory G data are read, prospectively fill:

```text
confidence_level
max_acceptable_per_plant_hard_failure_probability
planning_basis_note
population_id
season_id
frozen_at_utc
status = PEDICULARIS_G_HARD_VALIDITY_PILOT_PLAN_PROSPECTIVELY_FROZEN.
```

The tolerance must have a biological/method basis. Do not choose 5% or 10%
because it gives a convenient n.

## Run

```bash
python scripts/plan_pedicularis_g_hard_validity_pilot.py \
  <completed_planning_config.json> \
  --output <g_hard_validity_plan.json>
```

The current first-tier candidates are:

```text
G_A1_FINE_MESH
G_A2_POROUS_TUBING.
```

At a 10% failure tolerance and 95% confidence, testing both requires 58
paired-plant **candidate assignments**. At 5%, it requires 118.

Do not interpret those totals automatically as 58 or 118 distinct plants.
Multiple candidate flowers may share a plant only if assignment and
within-plant interference are prospectively controlled.

## Separation from effect/selectivity planning

Passing this screen means only that the device can be applied without observed
registered hard failures at the planned reliability resolution.

It does not establish:

```text
predator exclusion effectiveness
minimum predation reduction
final seed gain
equivalence of pollen/visits/z/water/damage
candidate superiority.
```

Those remain CAL-B/C and exploratory effect/selectivity questions.

## Why this is useful

Without this layer, a candidate could be advanced after only two or three
apparently clean plants even though zero failures at that n gives a very weak
upper bound on the true failure probability.

For example, at 95% confidence:

```text
0/2 failures   -> upper bound about 0.776
0/10 failures  -> upper bound about 0.259
0/29 failures  -> upper bound below 0.10.
```

Thus the planner turns 'the sleeve seemed to work' into an explicit
prospective method-reliability statement.

## Claim ceiling

A positive hard-validity pilot plan is only a sample-size plan for method
failure screening. It is not a positive G receipt and does not replace
same-context exploratory or confirmatory field data.
