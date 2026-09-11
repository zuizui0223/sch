# SCH Pedicularis pre-qualification calibration package v1

Status: **PROSPECTIVE / CALIBRATION ONLY**.

## Purpose

The corrected `Pedicularis rex` V2 programme already has fail-closed Qz, Qp and Qg evaluators, but their production configs intentionally retain `REQUIRED_BEFORE_USE` thresholds. SLK's threshold-source audit shows that only `Qz.min_z_levels=5` can be fixed directly from the registered design; the remaining numeric criteria require independent calibration, biological-relevance choices, or prospective precision/power work.

This package defines the **independent calibration data** that may be used to freeze those criteria before confirmatory Qz/Qp/Qg outcomes are opened.

It does not select thresholds automatically.

## Core separation rule

```text
CALIBRATION UNITS
    -> estimate repeatability, natural variation, timing and variance
    -> may inform prospective thresholds / power

QUALIFICATION UNITS
    -> test Qz/Qp/Qg after thresholds are frozen
```

No flower may occur in both sets. Prefer separate plants as well. If the same plant contributes to both sets because of field scarcity, this must be declared prospectively and calibration flowers must remain distinct from qualification flowers.

The calibration dataset IDs must therefore differ from every Qz/Qp/Qg qualification dataset ID.

## Four reusable information blocks

### C1 — morphology and handling repeatability

Goal: estimate the scale of repeated-measurement error and sham-handling changes for the geometry variables that appear as Qz/Qp/Qg off-target gates.

Template:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_C1_MORPHOLOGY_TEMPLATE_V1.csv
```

Registered calibration arms:

```text
BASELINE_REPEAT
Z_SHAM_TAPE
P_SHAM_HANDLING
G_SHAM_DEVICE
```

Record repeated measurements of:

```text
flower length
realized exsertion
corolla opening width
corolla tube diameter
bract height
lower-lip angle
flower orientation
mechanical damage.
```

This block can jointly inform the repeatability component of:

```text
Qz min_adjacent_exsertion_gap
Qz geometry / orientation / damage tolerances
Qp z / bract / opening / damage tolerances
Qg z / damage tolerances.
```

C1 does not by itself define the final biological-negligibility margin. It provides the measurement/sham variance that such a margin must exceed.

### C2 — water-y repeatability and handling stability

Goal: quantify how much cupulate-bract water depth changes naturally and under each sham-handling procedure when no water-defence treatment is intentionally applied.

Template:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_C2_WATER_TEMPLATE_V1.csv
```

Use the same calibration arms as C1 and repeated time points.

Record:

```text
hours since baseline
water depth
recent rainfall / water-input note
bract height
handling arm.
```

This block informs the repeated requirement that

```text
water-y remains fixed
```

in Qz, Qp, Qg and the SCH V2 full surface.

It does not redefine the water-defence axis or estimate BITA release.

### C3 — reproductive and consumer baseline variance

Goal: estimate plant-cluster variation in the outcomes that determine Qp/Qg efficacy, selectivity and prospective sample floors.

Template:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_C3_REPRODUCTIVE_TEMPLATE_V1.csv
```

Use untreated / natural flowers not reused in qualification.

Record at the appropriate stages:

```text
pollinator observation effort
pollinator visits
pollen grains on stigma
ovule count
early predator attack
initial seed count
undamaged mature seed count
damaged seed count
mechanical damage.
```

Derived calibration quantities include:

```text
initial seed set
predation fraction
final intact seed set
plant-level means / variances
within-plant flower variance
between-plant variance.
```

C3 is an input to prospective power / CI-width planning. It is not a substitute for Qp or Qg treatment contrasts.

### C4 — natural-history timing

Goal: convert the qualitative source statement

```text
predator oviposition occurs after flowers open but before ovaries swell
```

into a focal population/season timing distribution that can support Qg's registered barrier window.

Template:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_C4_TIMING_TEMPLATE_V1.csv
```

For each calibration flower record event times for as many of the following as observable:

```text
ANTHESIS_START
POLLINATION_WINDOW_COMPLETE
FIRST_PREDATOR_ATTACK
OVARY_SWELLING_START
COROLLA_SENESCENCE
```

The registered Qg timing window may only be frozen after C4 supports a prospective interval in which:

```text
pollination window is complete
AND
ovary has not swollen
AND
predator suppression can still plausibly act.
```

The final minimum/maximum hours are not generated automatically by this package; they remain a prospective decision justified from the C4 distribution and biological interpretation.

## Dataset identity

Every calibration row must contain:

```text
population_id
season_id
calibration_dataset_id
plant_id
flower_id.
```

`calibration_dataset_id` must be unique to this calibration package and must not equal any later qualification dataset ID.

## Recommended execution order

```text
1. C4 natural-history timing observations begin first because they may span the flowering window.
2. C1 and C2 repeatability / sham handling run on a compact calibration set.
3. C3 natural reproductive / consumer baseline data are collected on independent flowers.
4. summarize C1-C4 without opening any Qz/Qp/Qg confirmatory outcomes.
5. define biological-negligibility and minimum-useful-effect criteria.
6. perform prospective power / CI-width calculations at the plant level.
7. freeze the SLK threshold manifest.
8. only then open / run Qz/Qp/Qg qualification analyses.
```

The blocks may overlap in calendar time but not in confirmatory experimental units.

## Primary-source anchors

The package is sized conceptually from, but does not copy confirmatory thresholds from, three primary studies:

```text
Sun, Armbruster & Huang 2016  DOI 10.1093/aob/mcw097
Sun & Huang 2015              DOI 10.1093/aobpla/plv019
Huang, Wang & Sun 2016        DOI 10.1111/jipb.12460
```

Useful recovered scale facts include:

```text
P. rex geographic study: 16-36 plants/population; caliper precision 0.1 mm
water experiment: 40-60 individuals/population; >=6 capsules/individual
congener manipulation: 72 shortened + 72 control flowers on 12 individuals.
```

These are feasibility / variance anchors, not registered Qz/Qp/Qg minimum n values.

## Output contract

A calibration summary should export only descriptive / uncertainty quantities and provenance, such as:

```text
measurement repeatability distributions
sham-change distributions
water-depth change distributions
plant-level baseline means and variances
timing delays relative to anthesis
sample counts and missingness.
```

It must not emit:

```text
Qz PASS / FAIL
Qp PASS / FAIL
Qg PASS / FAIL
G1 conflict
G2 L
or automatically selected confirmatory thresholds.
```

The threshold freeze remains a separate prospective decision surface in SLK.

## Stop rules

### Calibration and qualification identities overlap

Do not proceed to threshold freeze. Reassign independent qualification units or recollect calibration data.

### Measurement error is too large to support the intended z spacing

Do not lower `min_adjacent_exsertion_gap` after seeing qualification data. Improve measurement / manipulation or revise the method version prospectively.

### No clean post-pollination/pre-swelling window exists

The current timed-barrier Qg method is not qualified. Test a different independently registered local exclusion approach or demote Pedicularis as the first same-species causal chain.

### Baseline predator pressure is near zero

The context is uninformative for Qg efficacy. Do not interpret this as evidence that predator protection is unimportant; move to a higher-pressure population/season for primary qualification.

## Claim ceiling

A complete C1-C4 calibration package licenses only:

```text
independent empirical inputs for prospective threshold and sample-size freezing.
```

It does not license any biological SLK gate.
