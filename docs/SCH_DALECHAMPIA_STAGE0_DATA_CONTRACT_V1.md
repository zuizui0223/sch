# SCH Dalechampia Stage-0 data contract v1

## Purpose

This contract makes the two Dalechampia promotion gates machine-readable without promoting a screening association into a causal compromise claim.

```text
Gate A: is this population / season conflict-active enough to justify intervention work?
Gate B: can controlled adult-weevil exposure generate a selective antagonist contrast?
```

The evaluator is:

```text
scripts/evaluate_dalechampia_stage0.py
```

Two modes are registered:

```text
population
exposure
```

## Claim ceiling

Neither mode estimates `z1*`, `z2*`, or `zc*`.

```text
population screen
!= causal multifunctionality
!= distinct function-specific optima
!= shared-trait compromise

controlled exposure screen
!= direct observation of oviposition
!= complete antagonist mechanism
!= mechanism-resolved balance.
```

The output may only qualify a focal context or a candidate `G1` exposure window for the next experiment.

## Population-screen CSV

Template:

```text
empirical/architecture/DALECHAMPIA_STAGE0_POPULATION_TEMPLATE_V1.csv
```

Required columns:

| column | meaning |
|---|---|
| `population_id` | one focal population per file |
| `season_id` | one focal season / campaign per file |
| `plant_id` | resampling cluster |
| `blossom_id` | unique focal blossom |
| `bract_area` | measured apparent display coordinate |
| `pollen_grains` | stigmatic pollen receipt; primary pollination screen |
| `seed_predator_present` | `0` or `1` indicator |
| `predated_seed_count` | later damaged / predated seeds |
| `initiated_seed_count` | denominator for predation fraction; must be >0 |

The evaluator reports:

```text
predator incidence
bract-area vs pollen correlation
bract-area vs predated-seed-fraction correlation
plant-cluster bootstrap 95% intervals
predeclared promotion gates.
```

The simple standardized relationship is intentionally a screen, not the final response-surface model. A positive screen is followed by direct trait and functional interventions.

## Controlled-exposure CSV

Template:

```text
empirical/architecture/DALECHAMPIA_STAGE0_EXPOSURE_TEMPLATE_V1.csv
```

Required columns:

| column | meaning |
|---|---|
| `population_id` | focal qualified population |
| `season_id` | focal season / campaign |
| `plant_id` | matched biological block and resampling unit |
| `blossom_id` | unique blossom |
| `exposure_window` | `E0`, `E1`, `E2`, `E3`, `E4`, or additional preregistered window |
| `bract_area` | measured z during exposure |
| `pollen_grains` | pollination selectivity check |
| `resin_amount` | reward / gland-state selectivity check |
| `predated_seed_count` | later antagonist damage |
| `initiated_seed_count` | denominator; must be >0 |

Registered exposure logic:

```text
E0 no adult-weevil exposure
E1 female-phase exposure
E2 early bisexual exposure
E3 late bisexual exposure
E4 post-receptive / early fruit-development exposure.
```

Exact calendar windows are determined prospectively from focal-population phenology.

### Matched within-plant design

The preferred Stage-0 exposure experiment is blocked within plant. Each focal plant should contribute blossoms randomized across `E0` and as many candidate exposure windows as feasible.

```text
plant 1: E0 E1 E2 E3 E4
plant 2: E0 E1 E2 E3 E4
...
```

Multiple blossoms per plant/window are allowed and are first averaged within that plant/window. The primary exposure contrasts are then paired within plant:

```text
E1 - E0
E2 - E0
E3 - E0
E4 - E0.
```

This removes stable between-plant differences in vigor, blossom size, resin production, mating geometry, and local microsite from the first-pass `G` selectivity contrast. Incomplete plants may contribute to other windows, but a given window is judged only from plants containing both `E0` and that window.

The evaluator therefore bootstraps complete plant-level pairs rather than treating exposure groups as independent samples.

## Threshold config

Thresholds are **not hard-coded** in the evaluator because the current literature does not justify universal biological cutoffs.

A deliberately non-runnable template is stored at:

```text
empirical/architecture/DALECHAMPIA_STAGE0_CONFIG_TEMPLATE_V1.json
```

Its threshold fields contain `REQUIRED_BEFORE_USE` rather than permissive zero defaults. Copy it to a new versioned config, replace every placeholder from a prospectively declared pilot / feasibility rationale, and freeze that config before evaluating the target package.

The final config has this structure:

```json
{
  "bootstrap_reps": 2000,
  "random_seed": 20260904,
  "population": {
    "min_blossoms": 0,
    "min_plants": 0,
    "min_predator_incidence": 0.0,
    "min_positive_correlation": 0.0
  },
  "exposure": {
    "min_complete_plants": 0,
    "min_damage_fraction_delta": 0.0,
    "max_pollen_relative_change": 0.0,
    "max_z_relative_change": 0.0,
    "max_resin_relative_change": 0.0
  }
}
```

The zeros above show numeric field types only; they are **not recommended thresholds**. At least 200 bootstrap replicates are required by code; confirmatory screening should normally use substantially more.

## Population promotion logic

`QUALIFIED_CONFLICT_ACTIVE_CANDIDATE` requires all declared gates:

```text
sample-size gate
plant-cluster gate
predator-incidence gate
lower 95% bootstrap bound for bract-pollen correlation >= declared positive threshold
lower 95% bootstrap bound for bract-predation correlation >= declared positive threshold.
```

This does **not** show `z1* != z2*`. It establishes only that the same display coordinate tracks both relevant routes strongly enough in this population to justify causal Stage 0/1 work.

## Exposure promotion logic

For each candidate exposure window relative to `E0`, the evaluator estimates within-plant paired changes in:

```text
predated-seed fraction
pollen receipt
measured z
resin amount.
```

For pollen, z, and resin, the plant-level quantity is the absolute relative change from that plant's `E0` value. The damage quantity retains its sign because `G1` must increase antagonist damage relative to `E0`.

A window passes only if:

```text
minimum number of complete E0/window plant pairs is met
lower 95% paired-bootstrap damage-delta bound >= declared minimum
upper 97.5% paired-bootstrap pollen relative-change bound <= declared tolerance
upper 97.5% paired-bootstrap z relative-change bound <= declared tolerance
upper 97.5% paired-bootstrap resin relative-change bound <= declared tolerance.
```

If more than one window passes, the evaluator selects the passing window with the largest observed paired damage-fraction increase as the candidate `G1` window.

Output status:

```text
SELECTIVE_G_WINDOW_CANDIDATE
```

or

```text
NO_SELECTIVE_G_WINDOW_RECOVERED.
```

The selected window is still a candidate. It must be frozen and independently checked in the later factorial experiment.

## Fail-closed rules

The analyzer stops or rejects a window rather than silently imputing when:

- required columns or values are missing;
- a package mixes populations or seasons;
- initiated seed count is zero or invalid for a scored blossom;
- predation exceeds initiated seeds;
- fewer than two plant clusters are available for population screening;
- a candidate exposure window has too few complete `E0`/window plant pairs;
- the predeclared complete-plant minimum is not met.

`NOT_EVALUABLE` or unqualified inputs are not converted into negative biological evidence.

## Why plant matching matters

Multiple blossoms on one plant are not independent biological replicates. More importantly, `D. scandens` plants can differ strongly in vigor, blossom geometry, resin production, autonomous selfing, and local visitation environment. The exposure screen therefore uses the plant as a matched block: first summarize blossoms within plant/window, then compare each exposure window with that same plant's `E0`, then bootstrap those plant-level paired contrasts.

A final hierarchical model may replace this first-pass bootstrap if it preserves the same estimands and declared promotion rules while representing patch, date, genotype, and repeated-blossom dependence more fully.

## Next stage

A qualified population plus a validated exposure window unlocks the causal experiment:

```text
multi-level z x pollinator state x predator state
-> W(z,G,P)
-> z1*, z2*, zc*
-> causal optimum-shift test.
```

No Stage-0 output is allowed to pre-empt those Stage-1/2 estimands.
