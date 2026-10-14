# SCH: test the relative fitness of floral exsertion, not only peak ranks

## Why the prior Fisher test was an inadequate primary statistic

PR #220 executed 900 synthetic candidate P. rex experiment datasets.
In the generous **true predator-induced optimum shift** scenario, the
excluded sample peak was at rank 4 and the exposed peak at rank 2
in **all 180** replicates over 10, 20 and 40 enrolled plants.

Yet the plant-matched Fisher test using the difference in peak *midranks*
rejected the sharp no-G-effect null only **0/60, 0/60 and 1/60** at these
three sample sizes (dedicated GitHub run 38403310656). This is a
**negative detectability finding for a chosen discrete statistic** under
synthetic curves, *not* observed P. rex predation evidence.

A peak-midrank difference discards the magnitude of seed fitness
differences. The next prospective field study would benefit from a
biologically explicit numerical contrast of **how predator G changes the
relative seed fitness of more versus moderately exserted flowers**.

## New ecological estimand and its limitation

Let z0,...,z4 be the original five fixed physical exsertion settings and

    F_E(z) = expected intact mature seeds per flower if G excluded
    F_X(z) = expected intact mature seeds per flower if G exposed.

The **population-level target** for a *preselected* pair of ranks is

    theta_(4,2) =
      [F_E(z4)-F_E(z2)] - [F_X(z4)-F_X(z2)].

When theta is **positive**, predator exclusion increases the *relative
seed-fitness value* of z4 versus z2 compared with predator exposure.
This is a trait-conditioned G response, rather than a uniform change
in mean seed output.

It does **NOT** logically imply that z4 becomes the entire curve's
unique optimum. Unmeasured differences involving z0, z1 or z3 may
matter. A true gain at z4 relative to z2 also does not prove that
the change was caused by consumption rather than another consequence
of G, until G selectivity is independently validated.

The rank pair z4-vs-z2 is **preselected here as a synthetic/theoretical
hypothesis**, informed by the strong-shift configuration in PR #220.
It has NOT been prospectively frozen prior to actual P. rex
field observations and cannot be retrospectively declared a
confirmatory rank-pair selection without a new protocol.

## Preserve the original whole-plant treatment randomization

The PR #217 cyclic incomplete block allocates only **two fruit flowers
per parent plant**. All flowers on the mother receive the SAME
predator state G. Their two fixed z ranks form an edge in a
five-vertex cycle:

    edge 0: z0 -> z1
    edge 1: z1 -> z2
    edge 2: z2 -> z3
    edge 3: z3 -> z4
    edge 4: z4 -> z0

For a mother i assigned one of those edges e with
a=e and b=(e+1)%5, its **within-plant contrast** is

    D_i(G) = Y_i(G,z_b) - Y_i(G,z_a).

Crucially, if predator exclusion has an arbitrary mother-specific
**common additive seed gain** tau_i on both of its flowers,

    Y_i(EXCLUDED,z) = Y_i(EXPOSED,z) + tau_i,

then the difference D_i is EXACTLY UNCHANGED by G, even if
tau_i differs among mother plants and their overall seed
production differs greatly.

That makes D more direct for SCH's trait-functional question
and less sensitive to plant-specific reproductive baseline
than comparing only absolute seed-count curves.

The new **Fisher sharp within-plant-difference null** is

    H0_D: D_i(EXCLUDED) = D_i(EXPOSED)
          for EVERY registered mother plant i,

conditional on the original z-pair and flower assignment.
This null is *weaker* than Fisher's sharp null of
no G effect on absolute seed counts. It allows
mother-specific uniform additive seed gains.

Within every precommitted patch×flower-stage×z-edge stratum,
exactly one plant is G excluded and one is exposed. Under H0_D,
each plant's contrast D_i can be imputed under the
unassigned predator treatment without knowing its unknown
absolute potential seed output. Swapping the two **whole
plants' G labels** preserves the conditional assignment mechanism.
Never permute individual flowers.

## Use all five cycle edges efficiently

There are two routes from z2 to z4 on the closed five-rank graph:

- Forward: z2→z3→z4, using edges 2 and 3.
- Backward: z2→z1→z0→z4, using the negatives of edges 1,0,4.

Each route telescopes to F(z4)-F(z2) at the population-mean level.
Average the two routes for a **symmetric connected-graph estimator**.

For each edge e within patch-stage batch b, define

    delta_(b,e) = D_(excluded,b,e) - D_(exposed,b,e).

Use integer twice-weights

    2w = [-1,-1,+1,+1,-1].

The prespecified score, in viable seeds per flower, is

    T = (1/(2B)) * sum_{b=1}^B sum_{e=0}^4
                       (2w_e) * delta_(b,e).

The exact identity at the *underlying common response-curve level* is

    sum_e w_e * {Delta(z_(e+1))-Delta(z_e)}
      = Delta(z4)-Delta(z2),

where Delta(z)=F_E(z)-F_X(z).

**Important finite-sample qualification:** T is a weighted sum of
*within-mother pair differences from distinct mothers*. It is NOT
algebraically identical to the crude difference between the observed
z4 and z2 **treatment-cell means** in a single allocation. The two
estimators can differ due to which particular plants received
each edge and treatment. The population target is reached
in expectation under the prospective randomized edge allocation
and comparable eligible plant population assumptions.

The integer-weight numerator makes both the observed statistic
and the exact permutation distribution free of floating rounding.
Under H0_D, each whole-plant pair swap negates that pair's
weighted contribution. For **one ten-plant batch**, all
2^5=**32 assignments** are enumerated; for up to 15 pair
swaps all assignments are enumerated. Larger data use a
preseeded plus-one Monte Carlo tail p estimate.

## A strict synthetic biological counterexample

Use the fully specified **synthetic** PR #220 curves:

    F_E at ranks 0..4 = [5,7,10,14,19]
    F_X at ranks 0..4 = [5,8,13,8,5].

The original peak-rank shift is positive (4−2=+2).
The proposed relative-fitness interaction is

    theta = (19−10) − (5−13) = +17
            surviving seeds/flower.

The corresponding five source edge-pair contrast
contributions to 2T are

    [+1,+2,+9,+8,+14];

their sum is 34, so T=+17. All five pair contributions
are strictly positive in the predeclared direction,
and the exact one-sided Fisher p for this complete
no-noise ten-plant demonstration is

    p = 1/32 = 0.03125.

Thus even the smallest eligible cyclic batch can
**in principle** give a sharp-null rejection for
a well-targeted continuous effect contrast. This
contrasts sharply with the old peak-midrank test,
which showed low rejection under noisy true-shift
synthetic scenarios. These are **different sharp
nulls and different statistics**; their p values
must not be interpreted as interchangeable.

A second synthetic same-optimum contrast is

    F_E = [8,10,17,12,9],
    F_X = [5,8,13,8,5],

for which theta = (9−17)−(5−13)=0
even though other parts of the G response
surface change. The targeted z4-vs-z2 score
cannot by itself detect every G-by-z response.

Additional tests verify exact Fisher superuniformity
over all 32 potential observed plant assignments
under a true within-mother-difference sharp null,
including **mother-specific integer G gains**
that are not constant across mothers.

## Executed 1,080-study synthetic benchmark

The dedicated [GitHub Actions run 38405724755](https://github.com/zuizui0223/sch/actions/runs/38405724755)
completed the source-identical comparison of **six
synthetic ecological scenarios × three eligible plant
counts × 60 independent datasets**. Both tests
used the exact cyclic candidate allocation and the
matched whole-plant G randomization conditional
on registered flower positions.

This table reports **one-sided p≤0.05 rejection
fractions** as *old peak-midrank Fisher /
new maternal z-difference Fisher*:

| Entirely synthetic G-effects scenario | 10 plants | 20 plants | 40 plants |
|---|---:|---:|---:|
| True sharp no-G-effect | 0% / 1.7% | 0% / 3.3% | 0% / 5.0% |
| Common additive +3 seeds/flower | 0% / 0% | 0% / 3.3% | 0% / 1.7% |
| Plant-heterogeneous G gain | 0% / 1.7% | 0% / 5.0% | 0% / 5.0% |
| z-response changes, but top z remains z2 | 0% / 0% | 0% / 5.0% | 0% / 1.7% |
| **z4 becomes optimum under exclusion** | **0% / 46.7%** | **0% / 100%** | **1.7% / 100%** |
| **Exact mother-specific integer additive G gain** | 0% / 0% | 0% / 1.7% | 0% / 5.0% |

These are **different tests with different sharp
nulls**. The former targets no G effect on any
flower's absolute mature seed count; the latter
targets no G effect on each mother's
*between-z* seed count difference. The
new shape statistic has dramatically higher
sensitivity **under this one hypothesized
peak-shift curve**.

The separate exact maternal additive negative
control permits different integer G gains
among parent plants, but constrains the same
gain across their two flowers. Under that
genuine sharp within-parent-difference null,
the measured rejection fractions did not
exceed 5% in these 60-replicate benchmarks.
The exact conditional Fisher validity is
verified independently by enumeration of
all 32 matched-plant assignments in a
single batch; the rates here are noisy
Monte Carlo diagnostics, not proofs of
population-level generalizability.

There is an important **negative biological
control**: when the G response changes with
z but the z4-vs-z2 target contrast is zero
and the overall optimal rank stays z2,
the new test often does not reject. It is
a *targeted functional response* test,
not a generic interaction detector.
The true population curve could also
have a peak displacement between other
z values that this prechosen contrast misses.

At 20 and 40 plants, 60/60 rejections have
a Wilson 95% simulation-proportion lower
bound of about 94%. That does **NOT**
justify asserting that 20 real P. rex
plants provide at least 94% statistical
power; the synthetic means, maternal
effects, missing-fate rate (zero here),
and first-stage G effectiveness are
not empirically calibrated.

Finally, under the nominal plant-effect
heterogeneity generator, a **noninteger**
G gain is rounded separately for each
flower. Rounding can introduce minor
departures from an exact mother-specific
common-additive seed-gain null, even
without biological G-by-z structure.
The explicitly constructed **integer
maternal gain** row above is the
proper exact negative control for
the claimed weaker Fisher sharp null.

The complete source-linked benchmark JSON
is attached to the successful workflow,
and can be regenerated by
`scripts/benchmark_pedicularis_within_plant_shape_fisher.py`
using the frozen PR #220 scenario file.

## A separate ten-cell simultaneous full-peak confidence calculation

The present matched-mother Fisher test targets a specific z4-vs-z2
change in **relative viable seed fitness** and its **sharp null**
permits plant-specific common additive G seed gains. Neither
rejecting that null nor a high positive-sample-peak frequency
establishes that a full *population reproductive optimum*
changes across all five exsertion ranks.

A separate new non-gating calculation now places one
simultaneous **familywise** Hoeffding/union band around
each of the ten randomized expected z×G cell seed
means, using **independently randomized entire
patch-stage batches** as units and a registered
upper seed cap valid for all potential outcomes.
It then projects joint bands into conservative
possible optimum ranks and predator-state rank
shift intervals. A persistent fraction of missing
mature outcomes is preserved as source-backed
seed-count envelopes.

This guarantee is CONDITIONAL on a real
pre-outcome physical K bound, valid independent
batch randomization and no between-batch
interference. The current synthetic example is
very conservative and finds **320 plants
insufficient even with perfect mean fitness
curves** under K=25. See
`SCH_PEDICULARIS_FIVE_RANK_SIMULTANEOUS_INFERENCE_V1.md`.

## Limits for a real field experiment

The method requires every originally randomized flower's **exact**
mature intact seed count, or a prospectively verified zero intact
seed outcome. It **fails closed** on fully lost or partially
unscorable mature fruit outcomes; no zero imputation or
complete-case selection is allowed.

The explicit null H0_D concerns the **individual mother's
two-z difference**, not the weaker average-value null
theta=0, and certainly not the null that the
population optimum rank stays unchanged. A
rejection is evidence against a plant-specific
sharp no-differential-G-effect assumption
under valid randomization and no interference.
It is *compatible* with G-driven trait-dependent
seed selection, but cannot distinguish realized
seed predation from collateral G intervention
effects without a qualified antagonist pilot.

Plant z first-stage manipulation effectiveness
must be validated at all five settings; a
positive z rank contrast can describe the
assigned physical manipulation even if its
realized exsertion is not ordered.

Actual P. rex seed-count data, intervention G
selectivity, between-mother predator spillover,
resource competition between a mother's two
flowers, comparative destructive pollen
sentinel results and a confirmatory W1/W2
architecture-value basis remain **unobtained**.

No pure pollinator-function or predator-function
optimum, SCH L, or SLK architectural payoff
is promoted by this mathematical/synthetic test.

## Reproduction

    python -m pytest -q \
      tests/test_pedicularis_within_plant_z_shape_fisher.py

    python -m scripts.fisher_pedicularis_within_plant_z_shape \
      exact_fruit_fates.csv frozen_two_flower_receipt.json \
      --output shape_fisher.json

The separate same-scenario comparison uses
\`scripts/benchmark_pedicularis_within_plant_shape_fisher.py\`,
the frozen PR #220 synthetic configuration, and
an additional **exact integer arbitrary maternal-additive gain**
negative control.
