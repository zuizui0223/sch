# Pedicularis rex parallel geometry-collection contract v1

## Why this execution order exists

The focal programme requires one population and one season for:

- confirmatory P0 manipulation validity;
- confirmatory P1 pollination-weight validity;
- confirmatory G predator exclusion validity;
- the separate nonconfirmatory P2 geometry pilot;
- ultimately the confirmatory P2 surface.

A strictly serial order is biologically awkward because the focal P. rex
programme reports capsules maturing roughly three weeks after anthesis (Sun &
Huang 2015, doi:10.1093/aobpla/plv019). The published flowering window is June
to early August / late June to early August in the focal programme (Sun &
Huang 2015; Sun, Armbruster & Huang 2016, doi:10.1093/aob/mcw097).

Therefore the naive sequence:

```text
P0/P1/G confirmatory
-> wait for seed endpoints
-> readiness
-> geometry pilot
-> wait for seed endpoints
-> power
-> P2
```

can spend roughly two fruit-maturation intervals before P2 can even start.

The execution contract instead separates **collection permission** from
**evidence admissibility**.

## Safe parallel sequence

After CAL-A/B/C and F0 are complete:

```text
F0 frozen P0/P1/G rules
+
pre-outcome selected confirmatory G method
+
frozen P0 level plan
+
frozen geometry precision/accrual plan
        |
        v
PEDICULARIS_GEOMETRY_INTERVENTION_PLAN_BINDING_V1
        |
        +-----------------------------+
        |                             |
        v                             v
randomized P0/P1/G              POWER_GEOMETRY_PILOT
confirmatory collection          separate-cohort collection
        |                             |
        |                             |  data remain inadmissible
        |                             |  for power basis
        v                             |
P0/P1/G final endpoints               |
        |                             |
        v                             |
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3
        |                             |
        +------------- exact-plan ----+
                      SHA match
                          |
                          v
              geometry summary / precision
                          |
                          v
                 W1/W2 power basis
                          |
                          v
                   powered P2.
```

The geometry pilot may therefore be **collected** before readiness is known.

It may not be **summarized, precision-qualified, materialized into the basis
ledger, or used for registered power** until later readiness V3 is positive and
matches the exact pre-outcome intervention plan.

## Pre-outcome intervention binding

Run:

```bash
python scripts/bind_pedicularis_geometry_intervention_plan.py \
  <geometry_pilot_config.json> \
  <p0_level_plan.csv> \
  <p0_field_config.json> \
  <p1_field_config.json> \
  <g_field_config.json> \
  <g_method_selection.json> \
  <f0_assembly_receipt.json> \
  --output <geometry_intervention_binding.json>
```

The binding is created before confirmatory P0/P1/G outcomes are known.

It freezes SHA-256 provenance for:

```text
P0 level plan
P0 field config
P1 field config
G field config
selected G method
F0 assembly receipt
geometry pilot config.
```

It also requires:

- one population / season;
- the current paired-flower P1 intervention;
- geometry z labels/ranks matching the frozen P0 plan;
- geometry G method matching the pre-outcome selected G method;
- selected G method bound to the exact frozen G config.

The binding does not say the interventions work.

## Parallel geometry allocation

Once the binding exists, the geometry cohort can be randomized:

```bash
python scripts/build_pedicularis_p2_geometry_pilot.py \
  <treatment_blind_geometry_flower_manifest.csv> \
  <geometry_pilot_config.json> \
  <geometry_intervention_binding.json> \
  --allocation-seed <PRECOMMITTED_SEED> \
  --field-sheet-out <maximum_geometry_field_sheet.csv> \
  --receipt-out <maximum_geometry_allocation.json>
```

This freezes the maximum geometry cohort, staged precision looks and all
flower-to-z/P/G assignments before geometry outcomes.

The geometry plants remain:

```text
threshold_basis_eligible = NO
confirmatory_eligible = NO
cohort_role = POWER_GEOMETRY_PILOT.
```

They remain disjoint from P0, P1, G and P2 confirmatory plants.

## Deferred admissibility gate

After confirmatory P0/P1/G are analyzed, build readiness V3.

Readiness V3 now carries:

- validated z-level labels;
- current paired P1 experimental unit;
- validated G exclusion method;
- P0/P1/G randomized-allocation identities;
- P0 level-plan SHA;
- P0/P1/G field-config SHA values;
- G method-selection SHA;
- exact source-receipt SHA values.

Only then may one geometry stage be summarized:

```bash
python scripts/summarize_pedicularis_p2_geometry_pilot.py \
  <completed_geometry_stage.csv> \
  <geometry_stage_allocation.json> \
  <cohort_registry.csv> \
  <readiness_v3.json> \
  --output <geometry_summary.json>
```

The summarizer requires the later readiness to match the pre-outcome binding
exactly for:

```text
z labels
P1 experimental unit
G method
P0 level-plan SHA
P0 config SHA
P1 config SHA
G config SHA
G method-selection SHA.
```

A mismatch makes the geometry data inadmissible for W1/W2 power basis.

## Failure worlds

### P0, P1 or G fails

If readiness V3 is not positive:

```text
geometry data may exist physically
but
geometry basis = NOT ADMISSIBLE.
```

The geometry rows cannot be used to rescue the failed intervention.

### Intervention plan changes

If the field team changes the P0 z plan, P1 intervention, G method or frozen
config after the geometry binding:

```text
later readiness SHA != bound plan SHA
-> geometry basis rejected.
```

A new prospective geometry collection would be required for the new
intervention system.

### Everything passes

If randomized P0/P1/G all pass and exact plan identities match, the already
collected geometry pilot can immediately enter its preregistered staged
point-estimate / precision sequence.

## What parallelization buys

The design removes one unnecessary **serial** fruit-maturation wait from the
critical path.

It does not guarantee same-season P2:

- P0/P1/G may fail;
- the first geometry precision look may fail;
- later preregistered geometry looks may require more collection;
- the final W1/W2 power requirement may still exceed available field effort.

The benefit is narrower:

> field time needed to learn P0/P1/G validity and field time needed to estimate
> nuisance geometry can overlap without letting invalid interventions generate a
> registered power basis.

## Claim ceiling

Parallel geometry collection is an execution-efficiency rule only.

It does not:

- weaken readiness;
- convert geometry rows into confirmatory evidence;
- assign W0-W5;
- allow outcome-dependent intervention changes;
- allow a failed P0/P1/G lane to be rescued by geometry;
- guarantee a final P2 sample size or same-season P2.

The biological paper remains determined by the later randomized confirmatory P2
surface.
