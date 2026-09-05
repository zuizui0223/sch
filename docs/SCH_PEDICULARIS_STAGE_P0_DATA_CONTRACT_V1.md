# SCH Pedicularis Stage-P0 exsertion-manipulation contract v1

## Purpose

This contract answers one narrow question before any causal compromise experiment is allowed:

> can `Pedicularis rex` corolla exsertion be manipulated over multiple ordered levels without simultaneously moving the other floral / defence coordinates that make the SCH interpretation possible?

The evaluator is:

```text
scripts/evaluate_pedicularis_stage_p0.py
```

Input template:

```text
empirical/architecture/PEDICULARIS_STAGE_P0_EXSERTION_TEMPLATE_V1.csv
```

Config template:

```text
empirical/architecture/PEDICULARIS_STAGE_P0_CONFIG_TEMPLATE_V1.json
```

## Biological basis

A congeneric Pedicularis field experiment shortened corolla tubes by bending them and fixing them with clear sticky tape rather than cutting tissue. This establishes a manipulation precedent, not validation in `P. rex`.

The Stage-P0 experiment therefore tests an adapted bending / fixation design in the focal species.

## Blocking and sham design

Preferred design:

```text
each plant contributes flowers across all assigned z levels
one assigned rank is a sham-tape / natural-exsertion control
active levels use the same handling / tape family plus graded bending
randomize flower-to-level assignment within plant.
```

`assigned_z_rank` is ordered from lowest intended realized exsertion to highest intended realized exsertion.

The evaluator does not infer this ordering from observed outcomes.

## Required fields

```text
population_id
season_id
plant_id
flower_id
assigned_z_level
assigned_z_rank
sham_control
realized_exsertion
corolla_opening_width
lower_lip_angle_deg
tube_diameter
bract_height
water_depth
flower_orientation_deg
mechanical_damage
pollinator_visits
pollen_grains
```

`sham_control` and `mechanical_damage` are coded `0/1`.

Only one assigned rank may be the sham rank.

## Primary manipulation target

```text
realized_exsertion
= (flower length - cupulate-bract height) / flower length
```

or the prospectively frozen measurement implementation of the same biological coordinate.

A valid manipulation must recover ordered, meaningfully separated realized z levels.

The primary separation gate uses the lower 95% plant-cluster bootstrap bound for the **minimum adjacent realized-exsertion gap**.

This is stricter than checking only the highest versus lowest treatment.

## Off-target gates

The manipulation must not become a hidden manipulation of the second functional axis or another floral coordinate.

Relative-to-sham gates:

```text
corolla opening width
tube diameter
cupulate-bract height
```

Absolute-change gates:

```text
lower-lip angle
water depth / retention state
flower orientation.
```

A separate gate limits mechanical-damage rate.

All thresholds are prospectively supplied by config; the repository template deliberately contains `REQUIRED_BEFORE_USE` placeholders rather than invented universal cutoffs.

## Why pollinator visits and pollen grains are not equivalence gates

The purpose of changing exsertion is to alter the pollination-facing function. Therefore:

```text
pollinator visits
pollen grains
```

are recorded and summarized by z rank but are **not required to remain equal across z levels**.

At Stage P0 they are descriptive functional checks only.

A later experiment tests whether the pollination response is biologically meaningful and how it combines with antagonist protection.

## Positive decision

All gates must pass for:

```text
PEDICULARIS_Z_MANIPULATION_VALIDATED
```

Required classes:

```text
sample / plant / z-level coverage
ordered realized exsertion
minimum adjacent exsertion separation
off-target geometry stability
water-defence stability
low mechanical damage.
```

If any gate fails:

```text
PEDICULARIS_Z_MANIPULATION_NOT_VALIDATED
```

Do not average failures into one score.

## Claim ceiling

A positive Stage-P0 result means only:

```text
multi-level exsertion manipulation is technically valid enough to enter the next causal stage.
```

It does not establish:

```text
functional conflict
z_P* != z_G*
causal compromise
pure function optima
dimensional release.
```

## Next gate

If P0 passes:

```text
validate pollination-weight intervention
replicate selective bract-water antagonist-weight manipulation
-> run multi-level z x P x G surface
-> analyze with scripts/analyze_sch_compromise_surface.py
-> optionally test component-optimum stability with scripts/identify_sch_pure_function_optima.py.
```

If P0 fails, Pedicularis remains a strong real-world D1 / selective-weight anchor but should not be forced into the causal SCH experiment. Return execution priority to Dalechampia or the next ranked system.
