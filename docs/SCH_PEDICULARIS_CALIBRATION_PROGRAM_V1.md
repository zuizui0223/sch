# SCH Pedicularis calibration programme v1

## Purpose

The Pedicularis causal programme has 40 threshold-freeze gate fields.

Five are already fixed by registered contracts. The remaining 35 are not
thirty-five separate experiments. They are grouped into three nonconfirmatory
calibration modules:

```text
CAL-A  measurement / equivalence / handling calibration     20 gates
CAL-B  exploratory effect + G timing calibration             7 gates
CAL-C  prospective power / precision planning                8 gates

registered contract values                                   5 gates
                                                             --------
total                                                        40 gates
```

The calibration programme exists only to support prospective F0 threshold
freezing. It does not generate a positive P0, P1 or G receipt.

## Order of operations

```text
registered-contract values
        |
        v
CAL-A measurement/equivalence
        |
        v
CAL-B exploratory intervention/timing
        |
        v
freeze biologically meaningful effect/margin targets
        |
        v
CAL-C prospective power/precision
        |
        v
freeze all P0/P1/G configs for one population + season
        |
        v
confirmatory P0 / P1 / G on rows not used for threshold basis
        |
        v
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3
```

CAL-C must not be run conceptually before the effect/margin targets it is meant
to power have been frozen.

## CAL-A — measurement, equivalence and handling

CAL-A begins with a dedicated same-flower repeatability component:

```text
empirical/architecture/PEDICULARIS_CAL_A_REPEATABILITY_TEMPLATE_V1.csv
scripts/summarize_pedicularis_cal_a_repeatability.py
docs/SCH_PEDICULARIS_CAL_A_REPEATABILITY_V1.md
```

This separates measurement noise from flower-to-flower biological variation
before any equivalence margin or minimum realized-z separation is frozen.

CAL-A supplies basis evidence for 20 gate fields.

Machine target-freeze implementation:

```text
empirical/architecture/PEDICULARIS_CAL_A_TARGET_TEMPLATE_V1.csv
scripts/materialize_pedicularis_cal_a_observed.py
scripts/freeze_pedicularis_cal_a_targets.py
scripts/apply_pedicularis_cal_a_to_cal_c.py
docs/SCH_PEDICULARIS_CAL_A_TARGET_FREEZE_V1.md
```

The materializer puts pilot descriptors and, for 13 matched metrics,
same-flower measurement-noise q95 in the same decision table while leaving the
target unresolved. A positive CAL-A target must exceed its measurement-noise
q95 when a matched repeatability metric exists. CAL-A and CAL-B bridges then
populate all 25 CAL-C boundaries while keeping all 25 assumed true values
unresolved.

CAL-A supplies basis evidence for 20 gate fields:

- P0 realized-z separation calibration;
- P0 off-target morphology / water-state equivalence;
- P0 handling-damage tolerance;
- P1 selectivity-equivalence margins;
- P1 handling-damage tolerance;
- G selectivity-equivalence margins.

The aim is not to set every margin equal to observed pilot noise. CAL-A
describes measurement repeatability, within-context variation, sham-handling
variation and exploratory contamination so that a prospective margin can be
justified.

No CAL-A row may later be reclassified as a confirmatory row.

## CAL-B — exploratory P/G effect and G timing

CAL-B supplies basis evidence for seven gate fields.

P1 exploratory evidence:

```text
minimum pollen-receipt increase
minimum initial-seed-set / pollen-limitation relief
```

G exploratory evidence:

```text
minimum early-attack reduction
minimum predation-fraction reduction
minimum final intact-seed gain
earliest usable post-anthesis barrier time
latest usable pre-swelling barrier time
```

Pilot-observed means are evidence about plausibility, not automatically the
confirmatory cutoff. The minimum effect must still have a biological rationale
and be frozen before confirmatory outcomes are read.

The G timing pilot must remain separate from both the barrier-effect pilot and
the confirmatory method-qualified G receipt. Use natural-state sentinel flowers:
single destructive pollen-receipt sentinels across scheduled post-anthesis times,
plus separate repeatedly observed flowers for first predator attack and ovary
swelling. The timing cohort is registered as `CAL_B_G_TIMING`; its flowers
must not be reused in `CAL_B_G` or confirmatory G.

The timing target basis is the natural event chronology, not the distribution
of times at which an investigator happened to apply a barrier.

Machine implementation:

```text
empirical/architecture/PEDICULARIS_CAL_B_TARGET_TEMPLATE_V1.csv
scripts/materialize_pedicularis_cal_b_observed.py
scripts/freeze_pedicularis_cal_b_targets.py
scripts/apply_pedicularis_cal_b_to_cal_c.py
docs/SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1.md
```

Observed pilot descriptors are materialized first with all target fields still
unfrozen. Only after the seven targets receive explicit basis notes and a
prospective freeze may the five effect boundaries be transferred into CAL-C.
The two timing bounds bypass CAL-C and later enter the G config during F0.

## CAL-C — prospective sample size / precision

CAL-C covers eight sample-size fields.

It is downstream of CAL-A/CAL-B because a power or precision calculation needs:

```text
variance / repeatability information
+ a prospectively selected minimum effect or equivalence target
+ the registered clustered / paired design.
```

CAL-C produces sample-size minima only. It must not revise the selected effect
or equivalence target merely to make the required sample size smaller.

Machine implementation:

```text
empirical/architecture/PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv
empirical/architecture/PEDICULARIS_CAL_C_PLANNING_CONFIG_TEMPLATE_V1.json
scripts/materialize_pedicularis_cal_c_pilot_sd.py
scripts/plan_pedicularis_cal_c.py
docs/SCH_PEDICULARIS_CAL_C_PLANNING_V1.md
```

The pilot-SD materializer copies variability and its exact source path only.
It intentionally leaves each boundary, assumed true value and basis note
unresolved until those planning targets are frozen prospectively.

The planner then allocates lane-level familywise failure probability by a
union bound across 8 P0, 8 P1 and 9 G criteria and returns the eight registered
sample-size fields.

## Calibration package entrypoint

For field execution, prefer the package-level entrypoint:

```text
scripts/build_pedicularis_calibration_package.py
docs/SCH_PEDICULARIS_CALIBRATION_PACKAGE_V1.md
```

It jointly validates the cohort registry plus repeatability/P0/P1/G
nonconfirmatory data, permits repeatability flowers only within the CAL-A P0
set, rejects other cross-lane flower reuse, and emits both calibration
summaries needed downstream.

## Threshold-free pilot summarizer

Before thresholds are frozen, pilot data can be summarized with:

```bash
python scripts/summarize_pedicularis_calibration_pilots.py \
  --p0 <p0_exploratory.csv> \
  --p1 <p1_exploratory.csv> \
  --g  <g_method_exploratory.csv> \
  --output <calibration_summary.json>
```

The script reuses the registered raw-data contracts but **does not invoke the
confirmatory decision rules**.

Its output status is:

```text
CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION
```

and it explicitly reports:

```text
thresholds_selected = false
confirmatory_receipt_generated = false.
```

It is therefore safe to use before F0 freezing, provided the pilot rows are
kept separate from confirmatory rows.

## Cohort separation

Use:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_COHORT_TEMPLATE_V1.csv
scripts/validate_pedicularis_cohort_registry.py
```

Registered roles are:

```text
CAL_A
CAL_B_P1
CAL_B_G
CAL_B_G_TIMING
CONFIRMATORY_P0
CONFIRMATORY_P1
CONFIRMATORY_G
FULL_SURFACE
```

A flower ID may appear only once across the entire execution registry.

Calibration rows are:

```text
threshold_basis_eligible = YES
confirmatory_eligible    = NO
```

Confirmatory/full-surface rows are the reverse.

Plant-level overlap between calibration and confirmatory phases is reported.
It does not silently convert calibration rows into confirmatory evidence.
Where feasible, plant-level disjointness is cleaner; flower-level data reuse is
prohibited.

## Machine ledgers

Gate-to-basis state:

```text
empirical/architecture/PEDICULARIS_THRESHOLD_BASIS_LEDGER_V1.csv
```

Gate-to-calibration-module mapping:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_MODULE_LEDGER_V1.csv
```

The module mapping is exhaustive:

```text
REGISTERED_CONTRACT   5
CAL_A                20
CAL_B                 7
CAL_C                 8
```

## F0 handoff

After CAL-A, CAL-B and CAL-C are positive, do not manually construct the three
confirmatory configs. Use:

```text
empirical/architecture/PEDICULARIS_F0_ASSEMBLY_CONFIG_TEMPLATE_V1.json
scripts/assemble_pedicularis_f0_configs.py
docs/SCH_PEDICULARIS_F0_CONFIG_ASSEMBLY_V1.md
```

The assembler imports five registered contract values, 20 CAL-A values, seven
CAL-B values and eight CAL-C sample-size values, checks for overlap/missing
fields, records source provenance for every gate, and reruns the shared freeze
validator.

## What calibration may not do

Calibration must not:

- generate `PEDICULARIS_Z_MANIPULATION_VALIDATED`;
- generate `PEDICULARIS_POLLINATION_WEIGHT_VALIDATED`;
- generate `PEDICULARIS_PREDATOR_METHOD_VALIDATED`;
- generate `PEDICULARIS_FULL_SURFACE_READY`;
- choose a cutoff merely because it makes the pilot pass;
- reuse the same flower-level outcome as both threshold basis and confirmatory
  evidence;
- turn unit-test values into field thresholds.

## Claim ceiling

A completed calibration programme supports only:

```text
the empirical and design inputs needed to prospectively freeze F0 thresholds.
```

It does not establish functional conflict, causal compromise, pure-function
optima, conflict budget L, dimensional release or architecture value.
