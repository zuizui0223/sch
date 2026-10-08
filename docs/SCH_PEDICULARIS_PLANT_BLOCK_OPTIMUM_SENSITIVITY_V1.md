# Can one plant drive an apparent predator-induced floral optimum shift?

## Biological question

SCH's target is whether seed-predator exclusion changes the floral
exsertion setting that maximizes intact mature seed production.
The source-locked fruit-only method can **already** bound this
displacement despite verified zeros and missing fruit outcomes.

However, flowers that share the same parent plant are not independent
ecological replicates: their carbon resources, reproductive
development, floral display and risk of enemy attack may be shared.
The **plant** is the experimental block in the current P. rex
randomized fruit cohort.

The important distinction is:

> Does a positive pooled optimum displacement recur when any one
> plant's entire randomized set of z×G flowers is omitted, or does
> it depend on one influential parent plant?

This is NOT automatically resolved by missing-data interval
robustness. In particular, a source-complete 20-flower
synthetic example can yield a positive pooled shift **for every
allowed missing fruit fate**, yet fail leave-one-plant-out
stability.

## Exact plant-block deletion

The procedure performs the full original source and
fate qualification first: every flower ID, plant ID,
z treatment, predator G, and source-specific upper viable
seed cap must exactly match the frozen allocation receipt.

Then, for each plant p:

1. Remove **all** its z×G flowers simultaneously.
2. Retain every other plant's **all** assigned flowers,
   including zero-fitness, damaged and unresolved outcomes.
3. Recompute the intact seed count mean **interval** at every
   rank z under predator exclusion and exposure using exact
   fractions.
4. Determine the possible optimum ranks in each predator
   state and the outer excluded-minus-exposed optimum rank
   shift interval, with the same semantics as the already
   tested full-sample estimator.

The source receipt is **never rewritten** as if the
plant-deleted subset were a different preregistered
randomized experiment. Every omission is a sensitivity
projection of the same source-qualified allocation.

A shift is "plant-deletion stable" only when the
**full data and every one-plant-deleted subset**
retain the same guaranteed strictly positive direction
(or strictly negative direction, respectively).

That is much stronger than just finding a stable
point estimate, but **not** a randomization test,
population confidence interval, or claim of
independent replication across plants.

## Synthetic counterexample: observed pooled sign is not universal across plants

Construct five floral exsertion levels and two
predator treatments, allocated once per rank/state
on each of two plants.

- Plant A (a high-fitness strong-response plant)
  has 7 mature intact seeds at high z under
  predator exclusion, and 1 at high z under
  exposure. Intermediate ranks have 3.
- Plant B (a weaker/partly unmeasured plant)
  has high-z excluded viable count only bounded
  [0,4] and high-z exposed [0,3];
  intermediate ranks have 3.

Pooling the two plants gives high-z EXCLUDED
mean at least 3.5, strictly above the
intermediate ranks' mean 3. High-z EXPOSED
mean at most 2, below intermediate mean 3.
The pooled predator-exclusion optimum
rank-shift interval is therefore **[+1,+3]**
in every possible completion of the missing
fruit outcomes.

But remove plant A:

- Only plant B remains. Its high-z EXCLUDED
  and EXPOSED intervals still allow rank 4
  to be or not be an optimum.
- Both predator-state optimum rank sets
  include intermediate ranks and high z,
  making the shift interval **[−3,+3]**.
- The pooled guarantee was not robust to
  removal of the strong-response plant.

Remove plant B instead:

- Plant A remains; the optimum shift remains
  guaranteed positive.

Thus **robustness to unknown individual
fruit fates is not equivalent to robustness
across parent plants**.

This is a constructed mathematical experiment,
not evidence of real P. rex between-plant
heterogeneity or observed selection.

## Positive and negative controls

A synthetic *three*-plant experiment with
two strong-response plants and one weaker
partly unmeasured plant maintains the
guaranteed positive rank shift after deletion
of **any one** parent plant. This is a
finite-sample diagnostic, not proof that
three real plants provide adequate inference.

A second three-plant synthetic control has
a guaranteed *negative* rank shift under
all one-plant omissions, testing the
classification symmetrically.

Adversarial tests ensure no source flower
may be quietly removed or reassigned before
the original validation step, and that
an unobserved fruit cannot be falsely recoded
as a verified zero.

## Ecological next step

The experiment should collect and analyze
**complete blocks across a representative range
of plant size, reproductive vigor, development
stage and source patch**. However, the 2016
P. rex source reported on average
12.51 mature capsules per plant, while the
current same-plant experimental bridge would
need up to 15 separately allocated pollen and
fruit flowers if both cohorts share plant IDs.
This threatens the representativeness of
plants that can supply complete blocks.

The plant-block jackknife tests whether the
recovered finite sample depends on a single
plant; it **does not solve** the plant-supply
bias. A prospective incomplete-block design
or separate randomized plant-to-cohort allocation
may still be necessary.

The next hard empirical challenge is **actual
fruit-level measurements on independently
sampled plants** with verified predator-method
selectivity and no material between-flower
resource or oviposition spillover.

## Claim limits and reproduction

This is a non-gating diagnostic for the
fruit-only natural-pollination × independent G
lane, not a replacement for the primary
four-state P2 experiment or prospective
W1/W2 power/randomization inference.
Two-plant leave-one-out results each contain
a **single retained plant**, so they cannot
estimate population sampling variance.

No causal pure-function optimum, within-flower
pollen–seed mediation, original P. rex
field outcome or SLK architectural value
is identified by this diagnostic.

Run on a future fully qualified data collection:

    python scripts/audit_pedicularis_plant_block_optimum_robustness.py \
      fruit_fate.csv frozen_fruit_allocation.json \
      --output plant_block_optimum_sensitivity.json

Synthetic regression tests:

    python -m pytest -q tests/test_pedicularis_plant_block_optimum_robustness.py
