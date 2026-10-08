# A more representative P. rex experiment: two flowers per plant

## The biological bottleneck

The merged plant-block sensitivity analysis (PR #216) showed that even an
apparently robust (to fruit loss) shift in reproductive optima can depend
on one large or unusually fertile mother plant.

In the 2016 published P. rex flower study (Sun, Armbruster & Huang,
doi:10.1093/aob/mcw097), seed production was based on a mean
**12.51 ± 5.60 SD mature capsules per sampled plant**, not an exact
census of all available flowers. The existing complete-block fruit
experiment requires **ten flowers per plant** (five exsertion ranks ×
two G predator levels), and potentially 15 if destructive pollen
sentinels come from the same plant.

Those requirements could preferentially enroll large/reproductively
vigorous plants. A leave-one-plant-out test diagnoses leverage *after*
sampling; it cannot remove a biased sampling frame.

## Prospective candidate: reduce 10 fruit flowers/plant to 2

Use ten eligible plants from each **prospectively defined patch ×
developmental-stage batch**, with two eligible, independently
identifiable, stage-matched flowers per plant. The 5 physical
exsertion settings (z0...z4) remain the candidate coordinates.

The prospective arrangement per group of ten plants:

1. Randomize **five whole plants to independent predator exclusion**
   and five to exposed-sham. Every flower on a plant receives the
   **same predator G assignment**; G is no longer mixed within a plant.
2. Within each arm, assign five plants to different edges of
   a circular z-rank graph: (0,1), (1,2), (2,3), (3,4), (4,0).
3. Randomize the two registered flower IDs within each plant
   to the two assigned z ranks.
4. Consequently **each z×G cell gets exactly two flowers from
   two distinct plants** per ten-plant batch. Across multiple
   patch-stage batches, the design repeats with independent
   source identity and assignment seeds.

| Property | Earlier complete fruit blocks | Two-flower cyclic plan |
|---|---|---|
| Fruit flowers on each plant | 10 | **2** |
| Number of z settings | 5 | 5 |
| Predator G assigned | To individual flowers within plant | **To entire plants** |
| z assignment | All five ranks on each plant, both G arms | Two connected adjacent ranks per plant |
| z×G per 10 plants | 10 flowers per cell (100 total) | **2 flowers per cell (20 total)** |
| Comparison of G within one plant | Yes, but possible resource/enemy interference | **No**; G contrast is between randomized plants |
| Per-cell precision with only one ten-plant batch | More measurements | **Very low; do not claim adequate power** |

The design has **equal treatment replication** and its within-arm
co-occurrence graph of exsertion ranks is connected, but it is
**not a balanced incomplete block design (BIBD)**: not every
pair of z levels occurs together on a plant. The word
"cyclic" describes incidence, not a proof of statistical
efficiency or noninterference.

A classic discussion of randomized incomplete-block incidence and
randomization is Pennsylvania State University STAT 503, Lesson 4.7
and Purdue STAT 514, "Incomplete Block Designs." These are
method precedents, not evidence that this specific biological
design has the required power.

## Why this is a biological improvement, not a finished experiment

The key structural change is **predator G at plant level**.
If a local seed predator redistributes its oviposition between
neighboring flowers, a within-plant excluded versus exposed
experiment may alter the exposed flower's attack risk.
Assigning one G treatment to all study flowers on a plant
removes *within-plant mixed-G interference*, but G can still
spill over between plants or patches; a pilot must measure it.

Two z settings on one plant can still compete for resources,
and treatment z itself might change displayed attraction
and visitation of adjacent flowers. Spacing, time, maternal
vigor and flower position are separate validity concerns.
No absence of interference is presumed.

Randomization is **hierarchical**:
plants are randomized to G and z-pair slots within each
patch-stage stratum; the two flower IDs are then randomized
to assigned z ranks. The resulting marginal cell means
are descriptively identifiable even with unequal maternal
baseline fitness, conditional on a genuinely precommitted,
treatment-blind eligible sample and valid randomization,
but a **valid test or precision interval** needs
plant-level and patch-aware randomization inference, outcome
fate censoring sensitivity, and a prospectively simulated
sample-size analysis.

Importantly, the pilot requires **10 eligible plants per
patch-stage batch**, not any arbitrary number of plants.
The number available in natural populations and the
fraction with *two suitable flowers* remain unknown.
A field flower-supply census must precede execution.

## Why not just reuse the old fruit analyzer?

The previous analyzer's identity contract requires one
flower on **each plant** in *every* z×G combination.
It must not be tricked into treating plants assigned
only one G level as complete blocks.

The new non-gating analyzer reconstructs exact
mean **intact mature seed count / flower** intervals
within each z×G treatment and patch-stage block,
retaining verified zero fitness separately from
unknown mature fruit outcome:

- all 20 original treatment-blind allocated fruit IDs
  must be included for each batch;
- allocation, patch/stage labels, flower position, z rank
  and plant-level G must match the immutable receipt;
- each z×G cell contains two flowers from distinct
  plants in each batch;
- final viable seed counts are exact or individually
  bounded according to the previously validated
  four-state mature-fruit fate scheme;
- the output reports possible and guaranteed unique
  finite-grid reproductive optima, descriptive G
  contrasts, plus conditional optimum-rank displacement.

A positive rank shift in these **synthetic input tests**
is not observed P. rex biology. No new study participant
or source flower is actually recruited and no source
treatment is qualified just by generating a manifest.
Neither P0 phenotype effectiveness nor G predator
selectivity is certified by the candidate seed/hash.

## Prospective sample demand and missing-fate information bottleneck

A new simulation framework executes the actual
cyclic plant-level G allocator on explicitly
hypothetical seed-count response curves,
varying the variance attributable to patches,
plants and individual flowers, and the
rate and mechanism of missing maturity outcomes.
It compares complete-outcome and worst-case
fate-bound reproductive optimum shift
classification. These scenario success rates
are **not calibrated confirmatory power**.

A separate exact binomial screening model
reports how many total plants need examination
to fill ten two-flower-eligible plant slots
in every patch-stage batch, conditional on
explicitly assumed (not observed) eligibility
probabilities. In particular, if half the
plants were eligible, 28 screened for one
batch or 32 per batch for four batches
would meet the model's joint 95% fill target.

However, if a fixed fraction of mature
fruits stays unobservable, its worst-case
seed-count uncertainty need not diminish
as additional plants are enrolled.
**Maturity follow-up and source-specific
upper seed caps are therefore part of
sample-size planning**, rather than
treating lost outcomes as ordinary
observed zero seed counts.

See `SCH_PEDICULARIS_TWO_FLOWER_DETECTABILITY_AND_ELIGIBILITY_V1.md`.

## Pollen sentinel cohort

The destructive pollen-stigma assay cannot be run on
the fruit-bearing flowers without losing their maturity
endpoint. A separate **plant-randomized pollen sentinel
cohort** is still needed. A future lower-demand candidate
could assign one flower per plant to one of the five
physical z settings, balanced across patch/stage strata,
but it must be separately randomized and validated.
It is **not** implemented by the present fruit-only tool.

Cohort comparability, flower supply, whorl effects,
pollinator timing, independently verified G selectivity,
and power remain unresolved before connecting pollen
response M(z) to the state-specific reproductive
curves F0(z) and F1(z).

## Files and execution

    empirical/architecture/PEDICULARIS_TWO_FLOWER_CYCLIC_TREATMENT_BLIND_MANIFEST_V1.csv
    empirical/architecture/PEDICULARIS_TWO_FLOWER_CYCLIC_Z_LEVEL_PLAN_V1.csv
    empirical/architecture/PEDICULARIS_TWO_FLOWER_CYCLIC_FRUIT_FATE_TEMPLATE_V1.csv

    python scripts/plan_pedicularis_two_flower_cyclic_blocks.py \
      blind_two_flower_manifest.csv candidate_five_level_plan.csv \
      --allocation-seed PRECOMMITTED_LONG_SEED \
      --g-exclusion-candidate-method DESCRIPTIVE_G_BARRIER \
      --g-exposed-sham-candidate-method DESCRIPTIVE_G_SHAM \
      --allocations-out candidate_assignments.csv \
      --receipt-out candidate_receipt.json

    python scripts/analyze_pedicularis_two_flower_cyclic_fruit_bounds.py \
      complete_fate_rows.csv candidate_receipt.json \
      --output nonconfirmatory_fitness_bounds.json

Tests:

    python -m pytest -q tests/test_pedicularis_two_flower_cyclic_blocks.py

**Claim ceiling:** design and synthetic evidence only. Do not promote
the original P. rex P1/G/P2/W1/W2 gates, pure pollinator or predator
functional optima, SCH compromise L, or SLK architecture payoff.
