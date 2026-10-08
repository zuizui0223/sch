# An actual randomization test for the two-flower P. rex predator experiment

## From descriptive optimum differences to a Fisher sharp-null test

The previous SCH two-flower cyclic design (PR #217) randomizes whole
**plants** to antagonist G while two flowers on a plant receive two of
five physical exsertion z settings. The initial 3,000-scenario analysis
(PR #218) counted how often sample mean reproductive peaks changed.
However, the **null** synthetic scenario with NO true peak shift
still gave an apparent positive peak displacement in 19% of ten-plant
realizations. Therefore the scenario classification fractions are
**NOT inferential significance or calibrated statistical power**.

This module adds a **Fisher conditional randomization test** under
the sharp null that predator G has **no effect on the intact mature
seed count of any allocated flower**, conditional on its already
randomized z, source flower position and plant z pair.

It tests a *different null* from "the population's floral optimum
does not change." Rejecting the Fisher sharp null does not by itself
establish that the optimum has changed: predator G could uniformly
increase mature seed counts at all z values, for example.

Methodological precedents:

- Bai, Liu, Shaikh & Tabord-Meehan (2024), *Journal of Econometrics*,
  doi:10.1016/j.jeconom.2024.105873, matched-pair cluster
  randomization inference.
- Wu & Ding (2021), *Journal of the American Statistical Association*,
  doi:10.1080/01621459.2020.1750415, explicitly distinguishing
  Fisher sharp nulls from Neyman weak average-effect nulls.

## Why the permissible permutations are five whole-plant swaps per batch

In each **patch × developmental-stage** group of ten plants, the source
design assigns five plants to each G arm. Within each arm there is one
plant for every edge of the cyclic five-rank incomplete block:

    edge 0: z0,z1
    edge 1: z1,z2
    edge 2: z2,z3
    edge 3: z3,z4
    edge 4: z4,z0

Conditional on the pre-outcome plant-to-edge assignment and on which
flower received which of its two z ranks, **each edge has an excluded
and an exposed plant**. The two G labels can be exchanged within the
edge's matched pair, keeping both seed outcomes of the same plant
together. The five independent pair flips have **2^5 = 32 possible G
label configurations per batch**. With B batches, there are
**2^(5B)** conditional label configurations.

These equally probable permutations are justified **only if**
the prospective plant randomization actually implements the
documented allocation with a genuinely random precommitted seed,
and treatment-independent allocation/measurement validity holds.
The source SHA-256 hash certifies consistency, not actual field
randomization.

**Never swap G independently for individual flowers.** That would
turn two flowers on one plant into fictitious independent units,
violate the actual whole-plant treatment assignment and yield
miscalibrated results.

## Preregistered descriptive test statistic

For a five-rank intact seed-count curve in each arm, find the ranks
with the maximal sample mean viable seed count and use the
**arithmetic mean of all tied maximizing ranks** as a deterministic
midrank. Define the signed, one-sided statistic

    T = peak_midrank(EXCLUDED) - peak_midrank(EXPOSED).

Large positive values favor the candidate ecological hypothesis
that independent predator exclusion moves the reproductive
peak to higher exsertion.

This statistic operates on the full finite-grid response curves,
not just the high-minus-low z contrast. Because T is bounded
and sometimes tied, exact conditional p-values can be
coarse and power is not guaranteed even when a true
reproductive optimum shift exists.

For one batch there are only 32 configurations; the smallest
attainable nonzero one-sided exact p-value is **1/32=0.03125**.
For two batches, 2^10=1024 assignments. The implementation
enumerates exactly up to **15 matched plant pairs** (three
ten-plant batches). For larger datasets it samples random
whole-plant flips and uses the conservative **plus-one**
Monte Carlo p estimator, explicitly including the observed
reference assignment as an additional draw.

The resulting test is an **exact conditional Fisher test
only of the sharp no-effect G null** for complete
mature-seed outcomes. It is NOT an exact test of the
composite no-peak-shift null, and is not automatically
robust to effects on flower disappearance or plant
interference.

## A second control: constant additive predator effects

Even when excluding predators increases seed output,
the gain might be a **common constant** at every
floral exsertion rank. Such an effect does not move
the population's seed-fitness optimum, despite
constituting a genuine predator treatment effect.

The Fisher no-effect null can therefore be
supplemented with a more permissive **union of
sharp constant-additive-effect nulls**:

    H0(tau):
      Y_i(EXCLUDED,z) = Y_i(EXPOSED,z) + tau
      for EVERY flower i and assigned z.

Because exact viable seed counts are integers,
tau is an **integer** gain (possibly negative).
Individual precommitted seed-potential caps
restrict which tau values could physically
produce nonnegative, countable outcomes under
both G treatments. Every feasible tau is
considered, using the same conditional whole-
plant pair swaps and one-sided peak-midrank
statistic.

For each tau, impute the missing alternative
G potential outcome for all flowers and obtain
the Fisher sharp-null p-value. Taking the
**maximum p-value over the feasible tau values**
is a conservative test of the **union** of
all constant-additive sharp hypotheses. It
cannot reject that union merely because
the data disagree with tau=0.

A complete synthetic tau=+2 seed/flower
counterexample tests all 32 possible whole-
plant G assignments. It verifies that the
composite worst-case p-values are also
super-uniform under the truly constant-additive
effect.

**Limits:** rejecting the constant-additive
union means that *not every flower has the
same integer G effect*, subject to the sharp
null assumptions. It does **NOT by itself**
prove a z-specific G interaction: effects
might instead differ among mother plants
without differing systematically with z.
The weak null that the **population optimum
does not move** remains untested by this
simple union calculation.

Invoke with the optional flag:

    python -m scripts.fisher_pedicularis_plant_pair_G_randomization \
      full_maturity.csv frozen_two_flower_receipt.json \
      --test-uniform-additive-constant --output fisher.json

This extra analysis is currently limited
to at most 101 source-compatible integer
tau candidates, failing closed rather
than silently selecting favorable values.

## Complete-fate requirement

The test first calls the existing source-locked
\`analyze_pedicularis_two_flower_cyclic_fruit_bounds.py\`
validator on **all** originally assigned flowers.
It then accepts **only** exact surviving-seed
counts from counted mature fruits or independently
verified zero viable seed yields.

A verified zero intact seed outcome remains usable
even when its *predation mechanism* is unknown:
the Fisher outcome is intact viable seed count,
not the seed predation fraction q.

However, any fruit with unobserved final seed fate
or genuine partial interval censoring **blocks**
the direct sharp-null randomization test.
This is intentional: imputing lost fruits to zero
or deleting them would condition on an outcome
possibly affected by predator G itself.

The separate fruit-fate interval analysis remains
available for such scenarios, but its bound
classification cannot simply be plugged into
this fully-observed Fisher test. A future
sharp-null-compatible worst-case missing-outcome
p-value would need a distinct registered method.

## Adversarial validation

New regression tests verify that:

- with one ten-plant design batch, exactly
  **32** whole-plant permutation assignments exist;
- swapping one edge exchanges **both flowers**
  of one excluded plant against both of
  its matched exposed plant;
- when a source's flower outcomes are truly
  independent of G, the exact conditional
  p-values across all 32 possible assignments
  are **super-uniform** at 1%, 5%, 10%, 20%
  and 50% thresholds;
- a zero-contrast all-equal-outcome fixture
  yields p=1 rather than spurious significance;
- four-batch Monte Carlo results repeat exactly
  under the same random seed and obey
  the plus-one correction;
- altered frozen G/z IDs, missing source
  flowers, partial fates and invalid
  permutation arguments all fail closed.

All new numeric tests use **synthetic** input.
None is a real P. rex antagonist selection p-value.

## What has actually become possible

Before this addition, SCH could compute only:

    How often does the finite sample's mean-optimum rank differ?

It can now also compute:

    If G had no causal effect on any flower's mature seed count,
    how unusual is the observed directional peak-rank statistic
    under the source assignment mechanism?

This is progress toward a valid causal experimental framework,
but a sharp-null rejection alone still cannot establish that
G changes the population optimum, nor estimate
\`L\`, a pure pollination optimum or SLK architecture gain.

For a **confirmatory** test of weak/no-optimum-shift
hypotheses, the project still needs prospective
definition of a biologically meaningful peak shift,
covariance-aware plant and patch inference,
nonregular argmax handling, robust missingness
management and actual validation of predator
exclusion and physical exsertion manipulation.

## Reproduce

    python -m pytest -q \
      tests/test_pedicularis_plant_pair_fisher_randomization.py

    python -m scripts.fisher_pedicularis_plant_pair_G_randomization \
      completed_two_flower_fate.csv \
      original_two_flower_candidate_receipt.json \
      --output sharp_null_randomization.json

Input source labels and the "observed" declaration
are **not** external verification of field measurement;
the receipt explicitly retains
\`observed_field_data_independently_verified=false\`.

This is a non-gating method: original
P0/P1/G/P2/W1/W2, SCH L and SLK R/K/Phi
remain strictly unqualified without actual
direct floral trait and independent predator experiments.
