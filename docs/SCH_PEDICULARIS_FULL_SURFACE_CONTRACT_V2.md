# SCH Pedicularis full-surface contract v2

## Purpose

This is the registered Chapter-1 execution contract for `Pedicularis rex` when the same species is intended to continue into BITA Chapter 2.

The core change from V1 is causal independence between the SCH antagonist intervention and the BITA water-defence axis.

```text
SCH / Chapter 1
z = exsertion
P = pollination dependence
G = independent seed-predator exposure
water-defence y = held fixed

BITA / Chapter 2
x = exsertion
y = water-defence state / water-retention phenotype.
```

This separation makes the Chapter-2 release test non-circular.

## Required readiness receipt

The full surface may run only after the same population and season produce:

```text
z manipulation receipt
  SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1

pollination-weight receipt
  SCH_PEDICULARIS_POLLINATION_WEIGHT_V1

independent predator-weight receipt
  SCH_PEDICULARIS_PREDATOR_WEIGHT_V2
```

assembled by:

```text
scripts/assemble_pedicularis_full_surface_readiness.py
```

The required readiness schema is:

```text
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V2
```

and it must contain:

```text
water_y_requirement = HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE.
```

A V1 readiness receipt is rejected.

## Registered state mapping

The shared coordinate is:

```text
z = realized corolla exsertion above the cupulate bract.
```

Pollination-weight states:

```text
P0 = SUPPLEMENTED
     focal flowers remain open, but standardized supplemental cross-pollen
     reduces dependence on natural pollinator-mediated pollen delivery

P1 = NATURAL
     open natural pollination; pollination-facing dependence remains active.
```

Independent antagonist states:

```text
G0 = PREDATOR_EXCLUDED
     seed-predator access is selectively suppressed by the validated independent
     exclusion intervention

G1 = PREDATOR_EXPOSED
     matched exposed / sham condition; seed-predator pressure remains active.
```

The registered reproductive states are therefore:

```text
W00 = supplemented + predator excluded
W10 = natural      + predator excluded
W01 = supplemented + predator exposed
W11 = natural      + predator exposed.
```

## Water-defence y is held fixed

The water-retention defence state is **not** the SCH `G` intervention in V2.

```text
water defence is held fixed across every P/G/z cell.
```

The full-surface wrapper checks the realized water-depth range against a prospectively frozen tolerance and fails closed if water state differs materially among SCH cells.

This is essential because water defence is the intended BITA Chapter-2 `y` axis. Using the same water manipulation both to define the SCH reference and then to test BITA release toward that reference would create a circular cross-chapter test.

## Raw-data contract

Template:

```text
empirical/architecture/PEDICULARIS_FULL_SURFACE_TEMPLATE_V2.csv
```

Required fields:

```text
population_id
season_id
plant_id
flower_id
assigned_z_level
realized_exsertion
pollination_treatment
predator_treatment
exclusion_method
water_depth
ovule_count
undamaged_seed_count
damaged_seed_count
pollen_grains
early_predator_attack_present
mechanical_damage.
```

Registered treatment values:

```text
pollination_treatment = NATURAL | SUPPLEMENTED
predator_treatment    = EXPOSED | EXCLUDED.
```

`exclusion_method` is retained as provenance. The method itself must already have passed `SCH_PEDICULARIS_PREDATOR_WEIGHT_V2` selectivity testing.

## Primary outcome

The common primary fitness outcome is:

```text
fitness_value = undamaged mature seed count per focal flower.
```

Mechanism-resolving secondary outcomes include:

```text
initial seed set
seed-predation fraction
pollen receipt
early predator attack
water depth
handling / mechanical damage.
```

## Analysis

Run:

```bash
python scripts/analyze_pedicularis_full_surface_v2.py \
  <pedicularis_surface_v2.csv> \
  <pedicularis_readiness_v2.json> \
  <frozen_config_v2.json> \
  --output <sch_pedicularis_receipt.json>
```

The wrapper validates the system-specific contract, checks that water-y stayed fixed, maps the treatment states to the generic SCH coding, and calls:

```text
scripts/analyze_sch_compromise_surface.py
```

The returned core receipt remains:

```text
SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
```

with system wrapper:

```text
SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2.
```

## Chapter-1 estimands

The registered state-specific optima are:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

A positive causal compromise requires:

```text
z_P* != z_G*
interior z_C*
opposing optimum shifts
opposed pollination and antagonist component gradients.
```

`z_P*` and `z_G*` are not automatically pure function optima.

## Pollination interpretation

Because `P0` is supplemental pollen rather than pollinator absence,

```text
W10(z) - W00(z)
```

measures the reproductive consequence of remaining dependent on natural pollen delivery relative to a saturated-pollen baseline.

Its shape across `z` is the pollination-facing selection signal. Its absolute value may be negative if supplementation raises reproduction.

## Antagonist interpretation

Because V2 uses independent predator exposure,

```text
W01(z) - W00(z)
```

isolates the reproductive consequence of seed-predator exposure under the supplemented-pollen state, subject to the validated selectivity of the exclusion intervention.

The Chapter-1 antagonist effect is therefore no longer defined by manipulating water defence.

## Optional pure-function promotion

After a positive V2 surface, the same converted SCH rows may be evaluated with:

```text
scripts/identify_sch_pure_function_optima.py
```

Only context-stable causal component optima may be promoted to:

```text
identified_pure_function_optima.z_F1
identified_pure_function_optima.z_F2.
```

## BITA handoff

The default BITA state-specific release reference is:

```text
z_P*.
```

BITA then manipulates the previously fixed water-defence axis:

```text
y0 = water defence disabled
y1 = water defence active
```

and tests:

```text
R_state = |x0* - z_P*| - |x1* - z_P*|.
```

Because water-y was held fixed while `z_P*` was identified, this is a non-circular test of dimensional release.

## V1 deprecation boundary

The older V1 Pedicularis surface used:

```text
G0 = water protected
G1 = water drained.
```

That design remains useful for acute water-defence mechanism description, but it must **not** be used as the SCH reference experiment for the same-species water-y BITA release test.

See:

```text
docs/SCH_PEDICULARIS_WATER_G_DEPRECATION_V1.md
```

## Stop rules

Do not run or promote V2 if:

```text
readiness schema is not V2;
independent predator-weight receipt is absent;
raw data and readiness population/season differ;
water depth varies beyond the preregistered tolerance;
handling damage exceeds tolerance;
<5 informative z levels remain;
primary fitness is not measured consistently across all cells.
```

## Claim ceiling

A positive V2 receipt supports:

```text
same-species contemporary causal compromise on exsertion
identified with an antagonist intervention independent of the BITA water-defence axis.
```

It does not by itself establish:

```text
structural independence of x and y
genetic/developmental modularity
architecture-level Delta_mod
historical one-trait -> two-trait transition.
```
