# Pedicularis rex nonconfirmatory P2 geometry pilot v1

## Purpose

The production W1/W2 power pipeline is implemented, but a registered sample
size is currently blocked because the randomized four-state geometry and
same-estimand variance structure are unknown.

The current power-basis audit has:

~~~text
21 blockers
12 causal-geometry rows
0/12 causal-geometry rows ready.
~~~

This document implements the registered Route A:

~~~text
SEPARATE_NONCONFIRMATORY_P2_GEOMETRY_PILOT.
~~~

It is **not automatically required**. The prospective robust sensitivity
envelope remains the cheaper value-of-information diagnostic and should be used
first when scientifically justified scenario bounds can be declared.

If geometry uncertainty materially changes the required n, this pilot provides
the direct same-context basis.

## What one pilot can resolve

A single separate randomized z x P x G mini-surface measures 18 of the 21
currently blocking power inputs:

~~~text
final-fitness variance
  between-plant SD
  residual SD                                    2

four final-fitness state surfaces
  P0G0 P1G0 P0G1 P1G1                           4

pollen variance
  between-plant SD
  residual SD                                    2

four state-specific z -> pollen models           4

initial-seed variance
  between-plant SD
  residual SD                                    2

four state-specific z -> initial-seed models     4

total                                            18.
~~~

After a positive geometry-pilot materialization, the canonical basis audit is
expected to retain only:

~~~text
generating_model.z_levels
generating_model.realized_z_sd
production_surface_config.sch_surface.*
~~~

Those three are resolved by P0/F0 and the prospective primary-threshold freeze,
not by the geometry pilot.

## Independence from confirmatory P2

The cohort registry adds:

~~~text
cohort_role = POWER_GEOMETRY_PILOT
lane = P0_P1_G
threshold_basis_eligible = NO
confirmatory_eligible = NO.
~~~

Geometry-pilot plants are required to be disjoint from:

- threshold calibration plants;
- P0/P1/G confirmatory plants;
- full-surface confirmatory plants.

Flower IDs remain globally unique.

Thus no geometry-pilot row can later enter the confirmatory P2 dataset.

## Prospectively staged accrual

The geometry pilot must not choose one arbitrary pilot n and then add plants
post hoc if precision is disappointing.

Before any geometry outcome is read, freeze:

~~~text
planned_n_plants
  = maximum geometry-pilot cohort

candidate_cumulative_plants
  = ordered cumulative precision looks, for example [n1, n2, ..., nmax].
~~~

The final candidate must equal `planned_n_plants`. Every candidate look must
satisfy:

~~~text
candidate_n x flowers_per_plant
  divisible by
n_z_levels x 2 P x 2 G.
~~~

Therefore every precision look is an exact-balanced prefix of the same maximum
randomized allocation.

The SHA-256 allocator freezes one plant accrual order for the maximum cohort.
Each flower carries:

~~~text
plant_accrual_rank
first_precision_look_n.
~~~

No treatment is reassigned when the pilot continues.

Materialize one registered cumulative look with:

~~~bash
python scripts/materialize_pedicularis_p2_geometry_stage.py \
  <maximum_geometry_field_sheet.csv> \
  <maximum_geometry_allocation_receipt.json> \
  --stage-n <REGISTERED_CUMULATIVE_N> \
  --stage-sheet-out <geometry_stage.csv> \
  --stage-receipt-out <geometry_stage_allocation.json>
~~~

After the stage summary and precision audit, adjudicate continuation with:

~~~bash
python scripts/adjudicate_pedicularis_p2_geometry_accrual.py \
  <geometry_pilot_config.json> \
  <current_geometry_summary.json> \
  <current_geometry_precision.json> \
  --prior-precision <earlier_precision.json> \
  --output <geometry_accrual_decision.json>
~~~

The only allowed decisions are:

~~~text
STOP_GEOMETRY_PILOT_AND_MATERIALIZE_BASIS
CONTINUE_TO_NEXT_REGISTERED_GEOMETRY_STAGE
STOP_MAXIMUM_GEOMETRY_PILOT_BASIS_NOT_QUALIFIED.
~~~

Every earlier look must have a formal insufficient-precision receipt before a
later look can be evaluated. Once any earlier look passes, later collection is
not authorized.

Thus the stopping rule is:

> stop at the first preregistered cumulative look that passes the frozen
> precision gate.

## Allocation

Config template:

~~~text
empirical/architecture/PEDICULARIS_P2_GEOMETRY_PILOT_CONFIG_TEMPLATE_V1.json
~~~

The pilot freezes before outcomes:

- population / season;
- number of pilot plants;
- flowers per plant;
- >=5 ordered z levels and nominal target exsertion;
- already-qualified exposed / excluded G methods;
- balanced cyclic allocation strategy.

### Collection may run in parallel with confirmatory P0/P1/G

P. rex fruit endpoints mature on an approximately three-week timescale, while
the focal flowering window is limited to roughly June-early August. Requiring
P0/P1/G final outcomes before **collecting** the geometry pilot would therefore
place two fruit-maturation waits serially on the critical path before P2.

The safer and faster rule is:

~~~text
F0 + selected G method frozen before outcomes
-> bind exact P0/P1/G intervention plan to geometry config
-> collect geometry on a disjoint cohort in parallel with confirmatory P0/P1/G
-> wait for confirmatory readiness
-> only then allow geometry analysis / precision / basis materialization.
~~~

Use:

~~~bash
python scripts/bind_pedicularis_geometry_intervention_plan.py \
  <geometry_pilot_config.json> \
  <p0_level_plan.csv> \
  <p0_field_config.json> \
  <p1_field_config.json> \
  <g_field_config.json> \
  <g_method_selection.json> \
  <f0_assembly_receipt.json> \
  --output <geometry_intervention_binding.json>
~~~

The binding freezes the P0 z labels/ranks, the exact
`manipulation_setting_id` attached to every level, the full P0 level-plan
SHA-256 (which also contains the physical setting specifications), P1
experimental unit, selected G method and exact P0/P1/G field-config SHA-256
values before confirmatory outcomes.

Thus a geometry row is not considered the same z treatment merely because it
uses the same label. It must use the same frozen physical setting ID, while
`realized_exsertion` remains the measured phenotype produced by that setting.

The allocation script is then:

~~~bash
python scripts/build_pedicularis_p2_geometry_pilot.py \
  <treatment_blind_flower_manifest.csv> \
  <geometry_pilot_config.json> \
  <geometry_intervention_binding.json> \
  --allocation-seed <PRECOMMITTED_SEED> \
  --field-sheet-out <geometry_pilot_field_sheet.csv> \
  --receipt-out <geometry_pilot_allocation.json>
~~~

This authorizes **collection only**. It does not make the geometry data
admissible for power.

The allocator uses the same z x P x G state definitions as confirmatory P2,
but it does not require or create a registered P2 sample-size recommendation.

It gives exact global balance across:

~~~text
n_z_levels x 2 P x 2 G
~~~

while allowing balanced incomplete plant blocks.

The script does not choose pilot n.

## Raw outcomes

The field sheet uses the same biological endpoint columns as P2:

- realized exsertion;
- water depth;
- ovule count;
- undamaged mature seed count;
- damaged seed count;
- stigmatic pollen grains;
- early predator attack;
- handling damage.

The pilot therefore measures the same estimand family needed by the production
power generator rather than a surrogate gate metric.

## Summary

Run:

~~~bash
python scripts/summarize_pedicularis_p2_geometry_pilot.py \
  <completed_geometry_pilot.csv> \
  <geometry_pilot_allocation.json> \
  <cohort_registry.csv> \
  <readiness_v3.json> \
  --output <geometry_pilot_summary.json>
~~~

At this point, and not earlier, the later readiness receipt must be positive.
The summarizer verifies that its validated z labels, P1 experimental unit,
selected G method, P0 level-plan SHA and P0/P1/G config/method-selection SHA
values exactly match the pre-outcome intervention binding carried by the
geometry allocation. Any mismatch makes the geometry data inadmissible for
registered W1/W2 power basis.

The summary:

1. verifies the randomized flower/treatment identity;
2. verifies every flower is registered as POWER_GEOMETRY_PILOT;
3. fits the four state-specific quadratic final-fitness surfaces;
4. fits four state-specific linear z-to-pollen models;
5. fits four state-specific linear z-to-initial-seed models;
6. residualizes each endpoint and estimates between-plant and residual
   variance components.

No W0-W5 outcome is assigned.

## Point-estimability fail-closed rule

A fitness-state point estimate is structurally usable only when its quadratic
optimum is:

~~~text
concave
AND
interior to the sampled realized-z range.
~~~

If any state is boundary/nonconcave, the point-estimate summary remains
incomplete.

That structural check is **not enough** to promote the pilot into registered
power basis. A tiny pilot can return four interior quadratic vertices while
still estimating all geometry/variance inputs far too imprecisely for a
sample-size decision.

## Precision qualification

The pilot config must freeze the precision gate **before geometry outcomes are
collected**:

~~~text
precision_gate.bootstrap_reps
precision_gate.random_seed
precision_gate.min_valid_bootstrap_fraction
precision_gate.min_interior_concave_fraction_per_state
precision_gate.max_normalized_95ci_width_per_power_basis_path.
~~~

Run:

~~~bash
python scripts/evaluate_pedicularis_p2_geometry_precision.py \
  <completed_geometry_pilot.csv> \
  <geometry_pilot_summary.json> \
  <geometry_pilot_config.json> \
  --output <geometry_precision.json>
~~~

Whole plants are resampled. The evaluator requires enough bootstrap replicates
to recover all 18 power-basis paths simultaneously and separately records how
often each of the four fitness surfaces remains interior-concave.

For the 18 path-level precision checks, 95% interval widths are normalized to
biological scales:

~~~text
fitness surface peak
  CI width / mean ovule count

fitness surface optimum
  CI width / realized-z span

fitness surface curvature
  CI width x z-span^2 / mean ovule count

pollen model
  max(
    CI width of predicted pollen at z-center,
    CI width of predicted change across z-span
  ) / observed pollen SD

initial-seed model
  analogous quantities / observed initial-seed-fraction SD

between-plant or residual SD
  CI width / observed endpoint SD.
~~~

This yields one dimensionless precision width for every canonical power-basis
path. All 18 must be within the prospectively frozen maximum.

Thus:

~~~text
point estimate exists
!=
precision sufficient for registered power basis.
~~~

## Basis materialization

A point-estimate summary may be applied to the canonical basis ledger only
after a precision receipt authorizes materialization:

~~~bash
python scripts/materialize_pedicularis_w1_w2_basis_from_geometry_pilot.py \
  <geometry_pilot_summary.json> \
  <geometry_precision.json> \
  <geometry_accrual_decision.json> \
  --ledger-out <w1_w2_basis_after_geometry.csv> \
  --receipt-out <geometry_basis_materialization.json>
~~~

Only when point estimability and the frozen precision gate pass at the **first
eligible preregistered cumulative look**, and the staged-accrual decision
authorizes stopping, are exactly 18 geometry/variance paths promoted to:

~~~text
DIRECT_SAME_CONTEXT_READY
direct_registered_n_eligible = YES.
~~~

No other row is changed.

The normal power-basis audit is then rerun on the derived ledger.

## Bind qualified pilot values to the final power configuration

After the geometry point estimates and precision receipt pass, and after the
remaining P0/F0 basis blockers are resolved so the canonical power-basis audit
has zero blockers, bind the final frozen power configuration to the exact pilot:

~~~bash
python scripts/bind_pedicularis_w1_w2_geometry_config.py \
  <frozen_power_config.json> \
  <geometry_pilot_summary.json> \
  <geometry_precision.json> \
  <zero_blocker_power_basis_receipt.json> \
  --output <geometry_config_binding.json>
~~~

All 18 geometry/variance values in the power config must equal the exact
precision-qualified pilot point estimates. The binding also fingerprints the
summary, precision receipt, basis receipt and power config.

This prevents the geometry pilot from becoming a nominal citation while a
different, more convenient optimum, curvature, slope or variance is used for
sample-size planning.

## What the pilot does not do

The geometry pilot does not:

- become basis-ready merely because a model can be fitted;
- test the paper's causal compromise hypothesis;
- assign W0-W5;
- contribute rows or plants to confirmatory P2;
- choose the final power target;
- choose the primary effect threshold;
- substitute its realized-z SD for the registered P0 basis;
- automatically authorize the final sample size.

It provides nuisance/geometry inputs for prospective power planning only.

## Decision sequence

The intended decision path is:

~~~text
current basis audit
-> scientifically justified sensitivity envelope
-> inspect how much geometry uncertainty changes n
-> if information value is high:
     F0 + pre-outcome G method selection
     -> bind exact intervention plan
     -> collect separate POWER_GEOMETRY_PILOT in parallel with P0/P1/G
     -> obtain randomized P0/P1/G readiness V3
     -> if readiness fails or plan SHA mismatches:
          discard geometry for registered power basis
        else:
          evaluate staged geometry precision
          -> resolve 18 power-basis blockers
          -> finish remaining P0/F0 basis
          -> registered W1/W2 power
          -> powered confirmatory P2
   else:
     continue only through a prospectively justified robust-envelope route.
~~~

This preserves the biology-first experiment while avoiding a geometry-pilot
cohort when its information would not change the field decision.
