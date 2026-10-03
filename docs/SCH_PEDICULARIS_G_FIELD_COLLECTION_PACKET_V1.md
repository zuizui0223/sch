# SCH Pedicularis G field collection packet v1

## Purpose

The registered Stage-G V4 evaluator needs both:

```text
final seed / predation outcomes
and
stigmatic pollen receipt.
```

A stigma pollen count can be destructive. Therefore a field sheet must not
silently imply that one flower was destructively sampled for pollen and later
used again for final seed endpoints.

This packet separates:

```text
FOCAL ENDPOINT FLOWERS
  survive through early attack and harvest

MATCHED SACRIFICIAL POLLEN-PROXY FLOWERS
  collected after the natural-pollination window
  and used only to estimate plant x G-treatment pollen receipt.
```

The proxy measurements are then materialized into the canonical V4 table with
explicit provenance.

## Field templates

Endpoint flowers:

```text
empirical/architecture/PEDICULARIS_G_FOCAL_FIELD_TEMPLATE_V1.csv
```

Matched destructive pollen proxies:

```text
empirical/architecture/PEDICULARIS_G_POLLEN_PROXY_TEMPLATE_V1.csv
```

Canonical analysis table, generated rather than hand-edited:

```text
empirical/architecture/PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V4.csv
```

## Eight-stage field sequence

The complete V4 field sequence is frozen in:

```text
empirical/architecture/PEDICULARIS_G_FIELD_SEQUENCE_V1.csv
scripts/audit_pedicularis_g_field_sequence.py
```

Operational order:

```text
0  REGISTRY_ASSIGNMENT
1  ANTHESIS_BASELINE
2  POLLINATION_WINDOW
3  POLLEN_PROXY_COLLECTION
4  BARRIER_APPLICATION
5  POST_BARRIER_INTEGRITY
6  EARLY_POST_TREATMENT
7  HARVEST
```

### 0. Registry assignment

Before outcomes are known:

- assign plant and flower IDs;
- assign EXPOSED versus EXCLUDED within plant;
- record the candidate exclusion method;
- register both endpoint and proxy flowers as CAL_B_G threshold-basis rows;
- keep all calibration flowers ineligible for later confirmatory reuse.

### 1. Anthesis baseline

Record the anthesis reference time for each endpoint flower.

For proxy flowers, record a separate proxy anthesis time.

These clocks are needed because a late barrier can fail by arriving after
predator attack, whereas an early barrier can fail by contaminating pollination.

### 2. Natural pollination window

Before the barrier is applied:

- accumulate legitimate pollinator visits on endpoint flowers;
- measure focal realized exsertion;
- measure water state;
- allow the preregistered natural-pollination window to finish.

Do not use a barrier that covers the natural bumblebee entry/contact zone during
this phase.

### 3. Destructive pollen-proxy collection

After the natural-pollination window is complete, collect the matched proxy
flower(s) for stigma pollen counting.

Required proxy identity:

```text
same population
same season
same plant
same predator treatment
different flower_id from the endpoint flower.
```

A proxy flower is calibration-only and cannot later supply a final seed
endpoint.

The proxy table records:

```text
proxy_flower_id
proxy_anthesis_time_hours
proxy_collection_time_hours
pollination_window_complete_before_collection
pollen_grains.
```

### 4. Barrier / sham application

Immediately before treatment, record:

```text
barrier_application_time_hours
pollination_window_complete_before_barrier
ovary_swollen_at_barrier
barrier_covers_pollinator_entry
pre_barrier_attack_present
sham_device_applied.
```

These include hard method-validity observations.

An EXCLUDED flower that already has attack evidence cannot identify the full
predator-exclusion contrast.

### 5. Post-barrier integrity

During the exclusion period inspect:

```text
barrier_integrity_failure_present.
```

Examples include slippage, a failed seal, pore access inconsistent with the
planned barrier class, or placement failure.

This is a method-validity observation, not a biological effect-size threshold.

### 6. Early post-treatment outcome

Before harvest record:

```text
early_predator_attack_present
mechanical_damage.
```

The first is the early antagonist endpoint; the second detects handling/device
contamination.

### 7. Harvest

Record:

```text
ovule_count
undamaged_seed_count
damaged_seed_count.
```

These yield:

```text
initial seed set
final intact seed set
seed-predation fraction.
```

## Pollen materialization

Run:

```bash
python scripts/materialize_pedicularis_g_field_rows.py \
  <g_focal_endpoint.csv> \
  <g_pollen_proxy.csv> \
  <g_v4_materialized.csv> \
  --receipt <g_materialization_receipt.json>
```

For every plant x predator-treatment pair, the materializer requires at least
one proxy flower.

It writes the mean proxy pollen count into the canonical V4 rows for that
plant x treatment.

This repetition is a compatibility representation only:

```text
proxy mean repeated over endpoint rows
!= extra biological replication.
```

The downstream predator-weight evaluator first averages flowers within
plant x treatment and bootstraps plants. Therefore the statistical unit remains
the plant.

The materialization receipt preserves:

- every proxy flower ID;
- number of proxy flowers;
- materialized mean pollen grains;
- minimum/maximum proxy collection delay.

## Fail-fast before harvest

A large part of G method failure can be detected before waiting for mature
capsules.

Hard validity fields are concentrated at barrier application and the following
integrity phase:

```text
sham_device_applied
pollination_window_complete_before_barrier
ovary_swollen_at_barrier
barrier_covers_pollinator_entry
pre_barrier_attack_present
barrier_integrity_failure_present.
```

Thus harvest endpoints are not required to recognize many mechanically invalid
flowers.

This does not create a new biological stop rule. It prevents wasting endpoint
interpretation on flowers that never instantiated the registered G method.

## Complete field-packet entrypoint

For field execution, prefer the high-level builder:

```bash
python scripts/build_pedicularis_calibration_field_packet.py \
  <cohort_registry.csv> \
  <cal_a_repeatability.csv> \
  <p0_exploratory.csv> \
  <p1_exploratory.csv> \
  <g_focal_endpoint.csv> \
  <g_pollen_proxy.csv> \
  --g-materialized-out <g_v4_materialized.csv> \
  --repeatability-out <repeatability_summary.json> \
  --calibration-out <calibration_summary.json> \
  --g-materialization-receipt-out <g_materialization_receipt.json> \
  --field-packet-receipt-out <field_packet_receipt.json>
```

The builder requires every proxy flower to be registered as:

```text
cohort_role = CAL_B_G
threshold_basis_eligible = YES
confirmatory_eligible = NO.
```

It verifies proxy registry identity, materializes canonical G V4 rows, and then
runs the existing cohort-checked calibration package builder.

A positive receipt has:

```text
receipt_schema_version = SCH_PEDICULARIS_CALIBRATION_FIELD_PACKET_V1
status = PEDICULARIS_CALIBRATION_FIELD_PACKET_READY_FOR_TARGET_FREEZE.
```

## What this packet does not do

It does not:

- choose sample size;
- choose the G timing window;
- choose CAL-A/B thresholds;
- validate G;
- treat proxy flowers as independent endpoint replicates;
- permit calibration flowers to become confirmatory rows.

## Claim ceiling

This packet establishes field-data chronology, pollen-proxy provenance, and
calibration-package integrity only.

The decisive biological question remains empirical:

```text
Can a late/local P. rex barrier reduce predator access
while preserving natural bumblebee pollination and water-y?
```
