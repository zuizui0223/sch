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

The allocation script is:

~~~bash
python scripts/build_pedicularis_p2_geometry_pilot.py \
  <treatment_blind_flower_manifest.csv> \
  <geometry_pilot_config.json> \
  --allocation-seed <PRECOMMITTED_SEED> \
  --field-sheet-out <geometry_pilot_field_sheet.csv> \
  --receipt-out <geometry_pilot_allocation.json>
~~~

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
  --output <geometry_pilot_summary.json>
~~~

The summary:

1. verifies the randomized flower/treatment identity;
2. verifies every flower is registered as POWER_GEOMETRY_PILOT;
3. fits the four state-specific quadratic final-fitness surfaces;
4. fits four state-specific linear z-to-pollen models;
5. fits four state-specific linear z-to-initial-seed models;
6. residualizes each endpoint and estimates between-plant and residual
   variance components.

No W0-W5 outcome is assigned.

## Surface fail-closed rule

A fitness-state model is usable as direct registered power basis only when its
quadratic optimum is:

~~~text
concave
AND
interior to the sampled realized-z range.
~~~

If any state is boundary/nonconcave, the pilot summary remains
POWER_BASIS_INCOMPLETE.

The code does not invent a quadratic optimum outside the observed z range.

## Basis materialization

A positive summary may be applied to the canonical basis ledger with:

~~~bash
python scripts/materialize_pedicularis_w1_w2_basis_from_geometry_pilot.py \
  <geometry_pilot_summary.json> \
  --ledger-out <w1_w2_basis_after_geometry.csv> \
  --receipt-out <geometry_basis_materialization.json>
~~~

Exactly 18 geometry/variance paths are promoted to:

~~~text
DIRECT_SAME_CONTEXT_READY
direct_registered_n_eligible = YES.
~~~

No other row is changed.

The normal power-basis audit is then rerun on the derived ledger.

## Bind pilot values to the final power configuration

After all remaining P0/F0 basis blockers are resolved and the canonical
power-basis audit reaches zero blockers, do not manually copy the geometry
pilot values into a power config without verification.

Run:

```bash
python scripts/bind_pedicularis_w1_w2_geometry_config.py \
  <frozen_power_config.json> \
  <geometry_pilot_summary.json> \
  <zero_blocker_power_basis_receipt.json> \
  --output <geometry_config_binding.json>
```

All 18 geometry/variance values in the frozen config must exactly match the
summary. The binding also locks the entire config and basis receipt by semantic
SHA-256. Registered W1/W2 power refuses to run without this receipt.

This prevents a direct pilot from serving only as a nominal citation while a
different, more convenient geometry is used for sample-size planning.

The binding does not make pilot point estimates perfectly known. Pilot
sampling uncertainty remains a separate design issue.

## What the pilot does not do

The geometry pilot does not:

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
     run separate POWER_GEOMETRY_PILOT
     -> resolve 18 power-basis blockers
     -> finish P0/F0 remaining 3 blockers
     -> registered W1/W2 power
     -> powered confirmatory P2
   else:
     continue only through a prospectively justified robust-envelope route.
~~~

This preserves the biology-first experiment while avoiding a geometry-pilot
cohort when its information would not change the field decision.
