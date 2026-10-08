# Randomized P. rex pollen sentinel experiment — biology-first route

## A directly testable ecological question

**Does physically increasing floral exsertion cause greater stigmatic pollen
receipt under natural bumblebee visitation?**

Earlier *Pedicularis rex* studies linked exsertion with pollen receipt
observationally. A treatment-blind, randomized manipulation of the same
physical exsertion setting is a stronger test of the **pollination-facing
component** of the floral trait.

This question is biologically substantive even if the later seed-predator G
experiment cannot qualify: exsertion could increase visibility but fail to
improve actual pollen delivery. Both outcomes would inform the core
pollinator–enemy-conflict hypothesis.

## Why sacrifice separate sentinel flowers?

Sun, Armbruster & Huang (2016; doi:10.1093/aob/mcw097) counted pollen by
crushing late-anthesis stigmas onto slides. This is an established focal
measurement of pollen receipt, but is not a validated way to retain the same
flowers through mature seed production.

Therefore register **separate flowers**:

```text
POLLEN_SENTINEL
  natural pollination, randomized exsertion setting
  -> late-anthesis stigma pollen count
  -> no mature-seed observation on that flower

FULL_SURFACE (future separate cohort)
  randomized exsertion x pollination x predator
  -> intact mature seed fitness and antagonist damage
  -> no imputed sentinel pollen count on the fruit-bearing flower.
```

The global cohort registry rejects duplicate flower IDs across these roles.
A pollen sentinel is not assigned a post-pollination G treatment, since its
stigma may be removed before the barrier is applied.

## Execution

1. Positively validate the P0 manipulation and its randomized assignment in
   the same population/season. The physical z-setting IDs, rank order and
   sham-control level are already frozen.
2. Register **treatment-blind new flower IDs** in the sentinel cohort, not
   reusing P0 or fruit-bearing flower IDs.
3. Reuse the P0 physical z-level plan and within-plant SHA-256 randomizer,
   but produce a distinct `POLLEN_SENTINEL` allocation receipt.
4. At a prospectively specified floral stage under natural pollination,
   record flower age, realized exsertion and stigmatic pollen grains.
   Destructive stigma removal is permitted; no mature seed count is expected.
5. Analyze an **intention-to-treat (ITT) pollen slope against randomized
   z-setting rank**, with plant-centered regression, plant-cluster bootstrap
   and within-plant randomization permutation test.

Required fields:

```text
population_id, season_id, plant_id, flower_id
assigned_z_level, assigned_z_rank, manipulation_setting_id, sham_control
realized_exsertion, pollen_grains
flower_age_at_sampling_hours, pollen_sampling_stage
pollen_assay_method_id, stigma_removed, mechanical_damage.
```

The inference config prospectively freezes: age/treatment-stage control,
method ID, minimum plants, acceptable handling damage, bootstrap/permutation
replications, one-sided significance threshold and the biologically
meaningful pollen gain per rank.

The **registered biological estimand** is:

```text
beta_ITT = mean change in stigmatic pollen grains per one-unit increase
           in randomly assigned physical exsertion setting rank,
           after removing each plant's mean.
```

It estimates the effect of assigning the physical manipulation, not a
post-treatment association with realized exsertion. Realized-z ordering is
checked to ensure that increasing rank did increase the intended coordinate.

Primary result status:

```text
RANDOMIZED_EXSERTION_TREATMENT_INCREASES_POLLEN_RECEIPT
or
RANDOMIZED_EXSERTION_POLLEN_BENEFIT_NOT_ESTABLISHED.
```

A positive result requires both a plant-cluster bootstrap lower 95% bound above
the preregistered minimal pollen gain and a one-sided within-plant randomization
test passing its prospective alpha. This is a **biological causal response
for the test context**, not a pure pollinator function optimum.

## Full randomized dose-response: do not hide an intermediate peak

The registered linear ITT test is intentionally directional, following the
2016 observational positive exsertion–pollen association. But **five assigned
physical settings** also allow the experiment to show whether pollen delivery
is hump-shaped, flat or locally reversed. An intermediate exsertion optimum is
biologically plausible if visitor contact geometry deteriorates at the
highest positions. A zero linear slope can coexist with a large positive
intermediate response.

The production receipt now preserves a **non-gating descriptive curve**:
mean stigmatic pollen grains by randomized setting rank, plant-cluster bootstrap
intervals at each rank, adjacent mean differences, and a predefined
central-rank versus two-endpoints contrast with a plant-cluster interval.
The highest observed mean rank and whether it lies inside the tested range
are reported explicitly.

These summaries are **not an alternative significance test**. They cannot
rescue or reverse the prospective linear-benefit decision, identify a
population-level pollinator optimum, establish the source of pollen grains,
or promote W1/W2. A shape-specific ecological hypothesis would require
separate prospective registration and sufficient field replication.

An additional mechanism boundary matters: the experiment grants **ambient
visitor access**, but an open-flower pollen count does not isolate pollinator
deposition from possible manipulation-related pollen transfer. Direct
pollinator mediation would need an independently validated visitor-exclusion
or pollen-source control; this cannot be inferred from the recorded pollen
count alone.

## Files

```text
empirical/architecture/PEDICULARIS_RANDOMIZED_POLLEN_SENTINEL_CONFIG_TEMPLATE_V1.json
empirical/architecture/PEDICULARIS_RANDOMIZED_POLLEN_SENTINEL_TEMPLATE_V1.csv
scripts/build_pedicularis_randomized_pollen_sentinels.py
scripts/analyze_pedicularis_randomized_pollen_sentinels.py
tests/test_pedicularis_randomized_pollen_sentinels.py
```

Allocation:

```bash
python scripts/build_pedicularis_randomized_pollen_sentinels.py \
  <treatment_blind_sentinel_flowers.csv> \
  <frozen_P0_level_plan.csv> \
  <positive_P0_receipt.json> \
  --allocation-seed <PRECOMMITTED_SEED> \
  --out <sentinel_allocation.csv> \
  --receipt-out <sentinel_allocation_receipt.json>
```

Append measured pollen and floral-age fields to those same flower IDs, then:

```bash
python scripts/analyze_pedicularis_randomized_pollen_sentinels.py \
  <completed_sentinel_pollen.csv> \
  <sentinel_allocation_receipt.json> \
  <positive_P0_receipt.json> \
  <cohort_registry.csv> \
  <frozen_sentinel_inference_config.json> \
  --output <randomized_pollen_response.json>
```

## Separate-cohort ecological contrast is now implementable (not confirmatory)

A new non-gating companion uses another randomized
`TWO_COHORT_FRUIT` set with intact mature seeds under natural pollination
and qualified independent G. The two cohorts need not share flower IDs:
the marginal curves `E[pollen | do(z)]` and
`E[viable seeds | do(z), G]` are each experimentally estimable when
cohort sampling and interference assumptions hold. The ecological
contrast is pollen deposition at the *two predator-state reproductive
rank maxima*. This directly handles a nonlinear pollen curve: an overall
positive pollen slope can coexist with a negative pollen contrast over
the selected pair of z settings.

`scripts/analyze_pedicularis_two_cohort_ecological_bridge.py` implements
only a descriptive, plant-cluster-resampled comparison with explicit
tied-peak and provenance checks. It does not perform the still-missing
confirmatory **two-cohort W1/W2** sample-size planning, selective argmax
inference, or primary four-state SCH estimation. See
`SCH_PEDICULARIS_TWO_COHORT_ECOLOGICAL_ALIGNMENT_V1.md`.

## What the new route does **not** yet do

A separate positive sentinel result **does not** automatically complete W1
or W2. The original W1/W2 code asks for pollen slopes in both future G
states on the same flower rows used to fit mature-seed surfaces. Sentinels
collected before G are not exposed to either realized post-pollination G
treatment.

A redesigned W1/W2 outcome route would:

- test the ITT pollen benefit on independently randomized sentinel flowers;
- estimate the G-induced seed-fitness optimum shift on distinct mature-fruit
  flowers using the already registered z x P x G treatments;
- justify common pollen performance across G using positive intervention
  selectivity and temporal separation, **not fabricated G-labeled sentinel
  pollen measurements**;
- account for plant- and stage-level uncertainty in both independent
  experiments;
- refreeze the joint classifier and W1/W2 power for two cohorts before either
  outcome is used for confirmatory inference.

That integrated two-cohort W1/W2 route is **not yet implemented or authorized**.
The original same-flower P2 route remains stopped unless the separate
dual-endpoint assay feasibility gate passes.

## Claim boundary

No sentinel data have yet been supplied or analyzed.
The test suite uses exclusively synthetic fixtures. No W0–W5 world is
promoted, no seed-predator effect is recovered, and no individual flower's
pollen count is ever copied into the seed dataset.
