# SCH Pedicularis calibration field packet v1

## Purpose

The calibration programme is now the primary execution path. This packet turns
the registered field templates into one immutable deployment unit without
inventing thresholds, sample sizes, or confirmatory claims.

Materializer:

```text
scripts/materialize_pedicularis_calibration_field_packet.py
```

## Packet contents

A materialized packet contains exactly:

```text
packet_manifest.json
cohort_registry.csv
g_exploratory.csv
p0_exploratory.csv
cal_a_repeatability.csv
p1_exploratory.csv.
```

Each CSV is copied byte-for-byte from the registered repository template.

The manifest records:

- source template path;
- SHA-256 of the source template;
- exact header;
- cohort role;
- structural-risk class;
- risk priority;
- execution mode;
- allowed flower-overlap rule.

## Materialize

```bash
python scripts/materialize_pedicularis_calibration_field_packet.py \
  <empty_output_directory> \
  --population-id <population_id> \
  --season-id <season_id>
```

The output directory must be absent or empty. Existing files are never
overwritten, because a field-data file must not be silently replaced by a new
blank template.

## Registered bundle order

```text
0  cohort registry
1  G exploratory
2  P0 exploratory
2  CAL-A same-flower repeatability
3  P1 exploratory.
```

The numbers are structural-risk priorities, **not chronology and not sample
size**. Phenology may require assignments to overlap in time.

## Overlap rule

The only allowed cross-file flower overlap is:

```text
CAL-A repeatability flower IDs
  subset of
P0 exploratory CAL_A flower IDs.
```

P0/P1/G flower-level outcomes remain disjoint. The cohort registry is created
before calibration assignments and remains the authority for calibration vs
confirmatory eligibility.

## No thresholds or sample sizes

The packet manifest explicitly records:

```text
sample_size_status = NOT_SET_FIELD_PACKET_DOES_NOT_RUN_CAL_C
threshold_status   = NOT_FROZEN_FIELD_PACKET_PRECEDES_CAL_A_B_C
confirmatory_use   = PROHIBITED_CALIBRATION_ONLY.
```

Thus a field packet can be prepared before CAL-A/B/C threshold setting without
creating an informal sample size or pass/fail rule.

## After collection

Once the four calibration datasets plus registry contain field rows, run:

```text
scripts/build_pedicularis_calibration_package.py
```

That package builder checks role membership, context consistency, and flower
reuse before producing the repeatability and threshold-free calibration
summaries.

## Claim ceiling

A materialized packet proves only that the registered blank schemas and their
provenance were deployed for one named population and season.

It does not establish data quality, sample-size adequacy, CAL-A/B targets,
CAL-C power, F0 readiness, or P0/P1/G validity.
