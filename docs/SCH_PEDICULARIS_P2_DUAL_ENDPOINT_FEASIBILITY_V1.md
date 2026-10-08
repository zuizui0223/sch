# P. rex P2: the pollen-receipt / mature-seed endpoint collision

## Biological problem (not a paperwork concern)

The registered ecology-first question is whether seed predators move the
natural-pollination reproductive optimum of exsertion away from floral states
with better pollination performance.

Two independently necessary readouts enter the same predeclared W1/W2
interpretation:

1. an intact mature-fruit reproductive fitness surface over randomized
   `z × P × G`, including intact and damaged mature seeds;
2. pollen-receipt response to randomized `z`, currently computed from
   `pollen_grains` on the **same flower IDs** that contribute mature seed
   counts.

The canonical P2 raw schema, preparation, fingerprinting, secondary analyzer
and production W1/W2 power simulator all inherit this same-flower assumption.

### What the focal primary study actually did

Sun, Armbruster & Huang (2016), *Annals of Botany* 118:227–237,
doi:10.1093/aob/mcw097, Methods, measured pollen by taking late-anthesis
stigmas, crushing them onto microscope slides, and counting adhering pollen
grains. Mature viable/damaged seeds were counted roughly three weeks after
flowering. For the seven populations with linkable individuals, the authors
used the **same plants but generally different flowers** for morphology/pollen
and seed outcomes.

That is not a validated method for obtaining an accurate stigmatic pollen
count and an unbiased mature-fruit endpoint from one and the same flower.

**Therefore the current P2 field-allocation protocol cannot be called
biologically executable merely because P0/P1/G, geometry precision and
W1/W2 simulation gates are positive.**

This does not prove that same-flower measurement is intrinsically impossible.
It means compatibility must be tested with the *actual intended assay*.

## Two biologically defensible routes

### Route A — validate joint endpoints on one flower

Potential approaches include a genuinely non-destructive quantitative
stigma pollen assay, or experimentally validated late stigma sampling that
does not alter fertilization or mature seed yield in the focal context.

A separate *P. rex* validation cohort must demonstrate, under prospectively
frozen acceptance margins:

- accurate pollen quantification against an independent reference;
- explicit flower-ID linkage from the pollen observation to mature fruit;
- equivalence/no meaningful loss in mature seed set due to pollen sampling;
- compatibility with P and post-pollination G intervention lanes;
- a cohort disjoint from confirmatory P2.

Only a positive `PEDICULARIS_P2_DUAL_ENDPOINT_PILOT_VALIDATION_V1` receipt
and a frozen assay config can produce a
`PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_V1` receipt.

No particular non-destructive assay is asserted to work here. The 2016
destructive slide protocol is **a source of the problem**, not a positive pilot.

### Route B — separate pollen sentinels and seed-bearing flowers

This is probably the more conventional biologically feasible direction
if joint observation cannot be validated.

The first independent component of this route is now implemented:
`build_pedicularis_randomized_pollen_sentinels.py` and
`analyze_pedicularis_randomized_pollen_sentinels.py` permit a separate
randomized exsertion experiment under NATURAL pollination on sacrificial
flowers. Its response is a plant-block-randomized, intention-to-treat
effect of the physical z manipulation on stigmatic pollen grains. It is a
substantive test of the pollination-facing function, but **not the joint
two-cohort W1/W2 analysis**. See
`docs/SCH_PEDICULARIS_RANDOMIZED_POLLEN_SENTINELS_V1.md`.

A complete split W1/W2 design would randomly allocate two disjoint sets of
flower IDs, ideally within the same plant/block and z-setting:

- **pollen sentinel flowers**: measure pollen in late anthesis; destroy
  stigmas if necessary; do not require mature seeds;
- **seed flowers**: retain reproductive structures until maturity and measure
  seed outcomes, predator attack, and fruit-level fitness.

But this is **not a drop-in replacement** in the current analysis:

- sentinel flowers collected before barrier application cannot truthfully
  have a realized post-pollination G effect;
- the existing two-G-state pollen-slope test must be rewritten as an
  explicitly registered pollination-facing response estimand, conditional
  on the earlier demonstration that G is selective and applied after
  pollination;
- block-level matching and plant-cluster uncertainty must replace
  unobserved within-flower pollen–seed covariance;
- sample size, flowers-per-plant, separate sentinel/seed allocation,
  raw-schema fingerprinting, secondary classification and W1/W2 production
  power must be rebuilt and refrozen before P2 outcomes.

For that reason the current P2 pipeline **fails closed** on
`SPLIT_FLOWER_POLLEN_SENTINEL`. That route is a future, separately validated
analytical design, not a way to fabricate same-flower pollen entries.

## Machine stop implemented

```text
empirical/architecture/PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_CONFIG_TEMPLATE_V1.json
empirical/architecture/PEDICULARIS_P2_DUAL_ENDPOINT_PILOT_RECEIPT_TEMPLATE_V1.json
scripts/audit_pedicularis_p2_dual_endpoint_feasibility.py
tests/test_pedicularis_p2_dual_endpoint_feasibility.py
```

To validate Route A:

```bash
python scripts/audit_pedicularis_p2_dual_endpoint_feasibility.py \
  <frozen_joint_assay_config.json> \
  <independent_compatibility_pilot_receipt.json> \
  --output <p2_endpoint_feasibility.json>
```

The production P2 allocator now requires:

```bash
python scripts/build_pedicularis_full_surface_allocation.py \
  <registered_treatment_blind_flowers.csv> \
  <frozen_P2_allocation_config.json> \
  <registered_W1_W2_power_receipt.json> \
  <readiness_v3.json> \
  --endpoint-feasibility <p2_endpoint_feasibility.json> \
  --allocation-seed <PRECOMMITTED_SEED> \
  --allocations-out <p2_allocation.csv> \
  --receipt-out <p2_allocation_receipt.json>
```

The registered allocation records the feasibility receipt's SHA-256 and assay
identity. Field-sheet preparation preserves them in the identity lock;
the production surface analyzer rejects a complete packet without the
positive endpoint-feasibility binding.

The low-level `build()` and `analyze()` functions remain available for
synthetic regression/power tests only; they do **not** certify field
feasibility.

## Immediate biological consequence

This is a genuine experimental stop on the *ecology-first* causal paper:

```text
pollen -> stigma assay
       -> potentially destroys the tissue needed for reproduction

mature seed fitness
       -> requires the flower/ovary to persist through seed maturation.
```

Without validated compatible measurement, a W1 or W2 claim would depend on
an endpoint pairing that was not physically observed.

Even a positive endpoint-feasibility pilot does not create a W1/W2 result.
Its measurement variance must inform the frozen production power model;
a different assay precision may require replanning.

## Current factual state

```text
2016 destructive stigmatic pollen method                       RECOVERED
2016 separate pollen and seed flowers                          RECOVERED
same-flower accurate pollen + unbiased mature seeds in P. rex   NOT VALIDATED
validated non-destructive P. rex pollen count                   NOT RECOVERED
split-sentinel W1/W2 estimator and power                         NOT IMPLEMENTED
registered P2 dual-endpoint field permit                       BLOCKED
```

**Do not treat simulated complete rows, a correctly filled CSV, or the
historical plant-level association as a positive same-flower assay receipt.**
