# Two distinct flower cohorts can identify a marginal pollination–fitness alignment

## The biological target

Does seed-predator exposure push the reproductive optimum for floral exsertion
away from z-settings that produce more **stigmatic pollen deposition** under
natural pollination?

The historical *Pedicularis rex* pollen slide assay destroys stigmas. Requiring
the same flower to furnish both that destructive outcome and later mature seeds
is unnecessary for one important **population-level** question.

Let z be an experimentally randomized *physical exsertion setting* on a
registered >=5-level grid. Define marginal mean functions for a common
population, season, stage, sampling frame and treatment protocol:

    M(z) = E[pollen grains per stigma | do(z), natural visitor access]
    F0(z) = E[viable mature seeds | do(z), natural pollination, predator excluded]
    F1(z) = E[viable mature seeds | do(z), natural pollination, predator exposed]

These means can be separately identified from disjoint flowers, given
treatment randomization, comparable cohorts, full outcome ascertainment and
acceptable interference/handling checks. They do not require the covariance
of pollen and seeds *within an individual flower*.

On the discrete registered z grid:

    z_free = argmax_z F0(z)
    z_exposed = argmax_z F1(z)

    delta_z = rank(z_free) - rank(z_exposed)
    delta_M = M(z_free) - M(z_exposed)

The target biological pattern is **delta_z > 0 and delta_M > 0**. That is
stronger and more precise than testing a globally positive pollen slope:
a hump-shaped pollen response can make delta_M negative despite a positive
average linear tendency.

A concrete **synthetic counterexample** is registered in the unit tests:
the mean pollen curve at z ranks 0–4 has values proportional to
[0, 8, 25, 16, 8]. Its fitted randomized linear ITT slope is positive
(+2.4 pollen grains per rank), yet if predator removal moves the fruit
optimum from rank 2 to rank 4, the pollen contrast is **8 - 25 = -17
grains** (the added constant baseline cancels). Thus a supported
population-average positive linear response is *not sufficient* evidence
that the ecological shift moves flowers toward better pollination.

These numbers are synthetic and cannot be cited as P. rex field evidence.

All optima here are *finite-grid, ecological state-specific reproductive
optima*, never pure pollinator-function optima. Negative and null outcomes
are substantive biological tests, not failed paperwork.

## Which evidence is needed, and what remains missing?

Pollen sentinels: reuse the qualified, independently randomized
`POLLEN_SENTINEL` experimental and analysis receipt from PR #200.
They receive natural pollination, a precommitted physical z setting, and a
destructive stigma pollen count. Do **not** record mature seed counts on them.

Fruit cohort: register disjoint flower IDs with role `TWO_COHORT_FRUIT`
and exploratory `FRUIT_P1_G` lane. Within each plant, randomize one intact
fruit-bearing flower to every precommitted z × G combination, **NATURAL
pollination throughout**, with water defence held fixed and G implemented
only by the validated independent predator exclusion method. The complete
v1 design requires `2 * n_z_levels` flowers per plant. Complete blocks are
a first proof-of-concept; a balanced incomplete-block implementation would
need a separately simulated and qualified estimator.

**Same-plant separate flowers**: resample the same plant IDs jointly across
both cohorts, preserving shared plant-level nuisance covariance while never
claiming within-flower covariance.

**Disjoint plants**: resample plant IDs independently in the two cohorts, but
the causal population-level comparison also requires randomized or otherwise
defensible **cohort sampling exchangeability**. Matching species, site and
calendar year alone does not establish this.

**Partially overlapping plant lists**: blocked. Mixed common and
cohort-specific cluster sets would require a different joint resampling design.

Neither treatment-blind flower assignment nor a statistically positive signal
guarantees an unbiased experiment if flowers of different ages/whorls,
resources or latent developmental stages are systematically allocated
between cohorts. Register cohort assignment and stage/whorl checks before
observing pollen or seeds.

## Experimental validity and identity locks

- Qualify Stage P0 and its physical manipulation setting IDs *first*.
- Qualify Stage G, including timing/retained pollinator access, while holding
  water-y fixed. The fruit allocator requires the full positive readiness V3
  for this independent G.
- Use new `flower_id` values and a precommitted SHA-256 randomizer for each
  fruit plant's z × G combinations; freeze an allocation receipt.
- Fingerprint both positive upstream receipts, the complete fruit assignment
  table and the source-specific sentinel allocation.
- Carry **all** allocated fruit outcomes through to the final table,
  including fruits with zero intact seeds. Avoid preferential dropout of
  attacked or undeveloped fruits.
- Fail if mature seeds appear on a pollen sentinel or a stigmatic pollen
  count is copied into a fruit-only row.
- Record realized physical exsertion **before applying G** on every intact
  fruit-bearing flower. The assigned setting rank remains the ITT coordinate;
  failing to produce ordered realized exsertion across z ranks in both G states
  blocks calling its contrast an *exsertion* optimum.
- Confirm that the physical z manipulation and barrier do not introduce
  unregistered geometry interactions across G; V3 readiness at one geometry
  does not guarantee selectivity at all manipulated z levels.
- Store initial seed set and early predator attack if available, but do not
  infer the **cause** of a 0/0 seed count without validated fate evidence.
- Audit water-depth and mechanical handling variation under their pre-frozen
  diagnostic tolerances.

**Important**: the allocation verifier uses a frozen map and cryptographic
fingerprint; it is not a substitute for an independently dated preregistration,
field identity checks or observed lack of spillover. A predator excluded flower
might change enemy allocation to nearby exposed flowers, and fruit/resource
competition within one plant may induce interference. Those are biological
pilot questions, not assumptions proven by the code.

## Analysis status and statistical limitation

`scripts/analyze_pedicularis_two_cohort_ecological_bridge.py` reconstructs
the full z-response curves from the separate pollen and fruit datasets and
reports the discrete state-specific maxima, displacement and their *actual
pollen contrast*. It recomputes the already frozen pollen-sentinel analysis
instead of trusting a user-supplied status flag.

The output also repeats a **plant-cluster bootstrap**. Identical plant lists
are sampled jointly; fully disjoint plant lists independently. It reports
the fraction of bootstrap replicates with positive displacement **and**
positive marginal pollen difference, and the frequency of tied maxima.
Tied peaks are recorded as unresolved rather than selecting an arbitrary
best z rank.

**Those are descriptive stability summaries, not 95% confirmatory tests.**
Argmax estimators on a finite noisy grid are nonregular, and post-selection
bootstrap percentiles need not have nominal coverage. Peak-based adaptive
contrast classification also requires a frozen discovery/validation or
selective-inference design. The v1 code explicitly cannot unlock W1/W2.

Crucially, the joint observed contrast is a comparison of separate marginal
population responses. It cannot establish:

- individual-flower pollen–seed covariance or mediation;
- the identity of a pollen donor or a specifically bumblebee-mediated effect;
- that natural pollen delivery, rather than another source, explains all
  initial seed-set differences;
- pure pollinator and antagonist function optima;
- a four-state W00–W11 causal-compromise receipt, SLK L, R or Phi;
- historical evolution of differentiated architectures.

A true **confirmatory split-cohort W1/W2** would need prospective sample
size and power simulation over both datasets, staged cohort assignment,
selectivity and interference validation, formal uncertainty for selected
optima, and a newly registered classifier. This remains **not implemented**.

## Paths and example commands

Templates:

    empirical/architecture/PEDICULARIS_P1_FRUIT_ONLY_TREATMENT_BLIND_MANIFEST_TEMPLATE_V1.csv
    empirical/architecture/PEDICULARIS_P1_FRUIT_ONLY_TEMPLATE_V1.csv
    empirical/architecture/PEDICULARIS_TWO_COHORT_ECOLOGICAL_BRIDGE_CONFIG_TEMPLATE_V1.json

Generate a fruit allocation only after qualified P0 and readiness:

    python scripts/build_pedicularis_two_cohort_fruit_allocation.py \
      <blind_fruit_manifest.csv> <frozen_P0_level_plan.csv> \
      <positive_P0_receipt.json> <qualified_readiness_v3.json> \
      --allocation-seed <PRECOMMITTED_SEED> \
      --allocations-out <fruit_assignment.csv> \
      --receipt-out <fruit_allocation_receipt.json>

Append the fruit-only outcomes to each exact assigned flower ID, then:

    python scripts/analyze_pedicularis_two_cohort_ecological_bridge.py \
      <completed_sentinels.csv> <sentinel_allocation_receipt.json> \
      <positive_P0_receipt.json> <global_cohort_registry.csv> \
      <frozen_sentinel_config.json> <completed_fruit_only.csv> \
      <fruit_allocation_receipt.json> <qualified_readiness_v3.json> \
      <frozen_two_cohort_config.json> --output <ecological_contrast.json>

The `TWO_COHORT_FRUIT` role is intentionally marked
`confirmatory_eligible=NO`. The current locked original same-flower P2
allocator, analyzer and W1/W2 power route are **unchanged**. No experimental
fruit observations or P. rex pollen-sentinel data have been recovered;
all new tests use synthetic fixtures.

Sources: Sun, Armbruster & Huang 2016, doi:10.1093/aob/mcw097 (stigmatic
pollen slides and separately sampled mature-seed flowers); Sun & Huang 2015,
doi:10.1093/aobpla/plv019 (seed predators and water-bract interference).
