# SCH Pedicularis calibration collection priority v1

## Purpose

The calibration programme already defines what must ultimately be measured.
This contract answers a narrower operational question:

```text
If field effort is limited, which calibration bundle retires the most important
remaining uncertainty first, and how much registered downstream information
does each bundle support?
```

No sample size or biological threshold is introduced here.

Machine ledger:

```text
empirical/architecture/PEDICULARIS_CALIBRATION_COLLECTION_YIELD_V1.csv
```

Audit:

```bash
python scripts/audit_pedicularis_calibration_collection_yield.py
```

## Registered information yield

The counts are derived from the existing CAL-A target table, CAL-B target
table and CAL-C criterion table:

```text
all exploratory lanes together
  CAL-A observed decision distributions      20
  CAL-A same-flower measurement-noise floors 13
  CAL-B effect/timing distributions            7
  CAL-C plant-level pilot-SD criteria          25
  direct F0 values                              0.
```

The 13 repeatability floors support a subset of the same 20 CAL-A targets;
they are not 13 additional F0 gates. Likewise CAL-C SD rows are planning
inputs, not F0 values.

## Bundle-level yield

```text
G exploratory
  CAL-A distributions       6
  CAL-B effect/timing       5
  CAL-C SD criteria         9
  support outputs          20

P0 exploratory
  CAL-A distributions       8
  CAL-B                     0
  CAL-C SD criteria         8
  support outputs          16

CAL-A same-flower repeatability
  measurement-noise floors 13
  support outputs          13

P1 exploratory
  CAL-A distributions       6
  CAL-B effects             2
  CAL-C SD criteria         8
  support outputs          16.
```

## Risk-priority order

### 0. Cohort registry — before assigning calibration flowers

The cohort registry is not a biological experiment. It is the data-integrity
prerequisite that prevents calibration rows from later becoming confirmatory
rows.

### 1. G exploratory — highest fail-fast priority

Current focal evidence already supports:

```text
post-pollination seed-predator attack timing          yes
physical-barrier efficacy within Pedicularis          yes
fruit-development compatibility of post-pollination barriers yes
external selective-efficacy class                     yes.
```

What is still missing is the structurally decisive focal question:

```text
Can a P. rex late/local barrier reduce predator access
while preserving natural bumblebee pollination and water-y?
```

This is the least recovered intervention component of the same-system chain.
It also supplies the largest registered calibration-support yield (20
outputs), so scarce pilot effort should first protect the G lane.

This priority does **not** create an informal G pass/fail criterion. Before F0
the exploratory G data remain descriptive threshold-basis evidence.

### 2. P0 + repeatability — collect together where feasible

No focal P. rex experiment has yet demonstrated >=5 ordered realized
exsertion levels with all current off-target checks.

The same-flower repeatability rows are designed to be a subset of the P0
`CAL_A` flowers. Therefore the efficient unit is:

```text
P0 exploratory flowers
  + repeat the registered morphology/water/orientation measurements
    on the appropriate CAL_A subset.
```

This retires P0 manipulation risk while obtaining 13 measurement-noise floors
without creating a separate flower cohort.

### 3. P1 exploratory — still required, but method risk is lower

The focal P. rex supplementation effect is not recovered. However, method
uncertainty is lower than for G/P0 because the literature already contains:

```text
focal pollinator dependence
focal high outcrossing
multiple congeneric supplementation designs
within-plant paired-flower supplementation
whole-plant supplementation
null-to-large context-dependent congeneric effects.
```

P1 is therefore still mandatory for the same-context package, but it is the
third place to spend scarce method-development effort.

## Priority is not chronology

Flower phenology can require P0, P1 and G assignments to overlap in time.

The registered order means:

```text
when effort/equipment/flowers are scarce:
  protect G method-development first,
  then P0 + nested repeatability,
  then P1.
```

It does **not** mean waiting for all G outcomes before assigning P0/P1 flowers.

All final calibration bundles must still come from the same selected
population and season and must all be completed before the full calibration
package can unlock CAL-A/B/C target freezing.

## Required package remains unchanged

```text
cohort registry
+ same-flower repeatability
+ P0 exploratory
+ P1 exploratory
+ G exploratory
= calibration package.
```

## Claim ceiling

This contract is an information-yield and structural-risk ordering only.

It does not:

- define sample size;
- select CAL-A/B target values;
- validate P0/P1/G;
- create a stop rule;
- excuse omission of a lower-priority bundle from the final package.
