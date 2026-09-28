# SCH Pedicularis F0 config assembly contract v1

## Purpose

F0 is the final pre-confirmatory decision-rule assembly step.

It combines exactly four nonoverlapping sources:

```text
registered contracts   5 gate values
CAL-A                 20 gate values
CAL-B                  7 gate values
CAL-C                  8 gate values
                      --
total                  40 gate values
```

No source may overwrite another source.

## Inputs

Positive CAL-A receipt:

```text
SCH_PEDICULARIS_CAL_A_TARGET_FREEZE_V1
status = PEDICULARIS_CAL_A_TARGETS_FROZEN
```

Positive CAL-B receipt:

```text
SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1
status = PEDICULARIS_CAL_B_TARGETS_FROZEN
```

Positive CAL-C plan:

```text
analysis = pedicularis_cal_c_sample_size_plan_v1
status = PEDICULARIS_CAL_C_SAMPLE_SIZE_PLAN_READY
```

Assembly metadata template:

```text
empirical/architecture/PEDICULARIS_F0_ASSEMBLY_CONFIG_TEMPLATE_V1.json
```

The assembly metadata must be prospectively frozen before confirmatory data
and must carry the same population and season as CAL-A/B/C.

## Registered values

The assembler inserts only the five values already fixed independently of
CAL-A/B/C:

```text
stage_p0.min_z_levels = 5

method_gate.require_pollination_window_complete = true
method_gate.require_ovary_not_swollen = true
method_gate.require_barrier_not_cover_pollinator_entry = true
method_gate.require_sham_on_exposed = true.
```

## CAL-A contribution

CAL-A contributes the 20 prospectively frozen separation/equivalence targets.

Each threshold basis preserves the CAL-A target basis note.

## CAL-B contribution

CAL-B contributes:

```text
5 minimum-effect targets
2 G timing bounds.
```

Each threshold basis preserves the CAL-B target basis note.

## CAL-C contribution

CAL-C contributes the eight sample-size fields.

The threshold-basis text written into the final configs retains:

```text
familywise target power
familywise power basis
lane
required plants
required flowers per cell
driving criteria
design effect
design-effect basis
flowers per plant per cell
flowers-per-plant basis
CAL-C planning basis document.
```

This prevents a bare integer sample size from becoming detached from the
planning scenario that generated it.

## Exact coverage rule

The assembler imports `required_gate_paths()` from the same shared freeze
validator used by the P0/P1/G evaluators.

It refuses to emit configs unless:

```text
source union = exactly the 40 registered gate paths
source intersections = empty
source counts = 5 / 20 / 7 / 8.
```

Every assembled config is then passed back through:

```text
validate_prospective_freeze(config, lane).
```

## Run

```bash
python scripts/assemble_pedicularis_f0_configs.py \
  <cal_a_target_freeze_receipt.json> \
  <cal_b_target_freeze_receipt.json> \
  <cal_c_plan.json> \
  <completed_f0_assembly_config.json> \
  --p0-out <p0_frozen_config.json> \
  --p1-out <p1_frozen_config.json> \
  --g-out <g_frozen_config.json> \
  --receipt-out <f0_assembly_receipt.json>
```

A positive assembly receipt has:

```text
receipt_schema_version = SCH_PEDICULARIS_F0_CONFIG_ASSEMBLY_V1
status = PEDICULARIS_F0_CONFIGS_ASSEMBLED_AND_FROZEN
n_gate_values = 40.
```

## What F0 assembly unlocks

Only after positive F0 assembly may the field programme collect and interpret
the same-context confirmatory P0/P1/G datasets against those frozen configs.

The next empirical receipts remain:

```text
PEDICULARIS_Z_MANIPULATION_VALIDATED
PEDICULARIS_POLLINATION_WEIGHT_VALIDATED
PEDICULARIS_PREDATOR_METHOD_VALIDATED.
```

F0 assembly itself is not any of those receipts.

## What F0 may not do

F0 must not:

- invent a missing threshold;
- resolve a conflict between CAL-A/B/C by overwrite order;
- change a target after seeing confirmatory data;
- detach a CAL-C sample size from its planning provenance;
- infer that an assembled config will pass empirically.

## Claim ceiling

A positive F0 assembly receipt establishes only that the full 40-field
decision-rule package is prospectively complete, source-resolved and internally
validated for one population and season.

It does not establish manipulation validity, functional conflict, causal
compromise, conflict budget L, or dimensional release.
