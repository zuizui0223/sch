# When a missing fruit changes the predator-induced floral optimum

## Biological target

SCH asks whether experimental predator exclusion shifts the **reproductive
optimum for floral exsertion** in Pedicularis rex. The earlier fruit-fate
work can bound mean intact mature seed count and the possible discrete
reproductive optima over five or more precommitted exsertion settings.
The preceding follow-up (PR #214) instead identifies which unknown
seed counts could settle a specified HIGH-minus-LOW contrast.

This analysis targets the **full optimum displacement** directly.
It determines which exact surviving seed counts on ONE uncertain fruit
would guarantee a positive, negative, zero or unresolved
excluded-minus-exposed optimum-rank shift, while other uncertain
fruits retain their original outcome bounds.

## Synthetic ecological example

Two plants contribute one allocated flower to each of five z ranks
(0–4) under predator EXCLUDED and predator EXPOSED treatments.
All 20 allocated flowers remain in the denominator, with two
uncertain high-exsertion fruit outcomes.

The EXCLUDED rank-4 fitness interval is [3.5,5.5]
intact seeds per flower; ranks 0–3 have means no greater than 3.
Its optimum is guaranteed to be rank 4.

The EXPOSED ranks 1–3 have mean 3; rank 0 mean is 1.5.
Rank-4 fitness equals (3+x)/2, where x is the single
unknown intact seed count in the interval [0,8].

| Count x if exactly reobserved | Possible EXPOSED optimum ranks | EXCLUDED−EXPOSED optimum-rank difference | Interpretation |
|---|---|---|---|
| 0–2 | 1,2,3 | +1 to +3 | Strictly positive |
| 3 | 1,2,3,4 | 0 to +3 | Nonnegative; tie possible |
| 4–8 | 4 | 0 | Guaranteed zero shift |

This is a constructed scenario, **not measured P. rex**.
Counting five integers in the last row does NOT imply a
5/9 probability of no shift. No empirical outcome probability
has been estimated. A missing fruit may no longer be
recoverable, so this is chiefly prospective field guidance.

## Exact and efficient mathematical method

When the target fruit's current count is only known to lie
within [a,b] and its treatment cell contains n allocated
flowers, the original cell mean bounds [L,U] would become

    L_new(x) = L + (x-a)/n
    U_new(x) = U - (b-x)/n

after observing an exact integer x. Every other flower
and trait-setting cell retains its original uncertainty.

A rank is a possible optimum if its upper mean seed count
is at least the maximum of all rank-specific lower means.
The guaranteed unique optimum requires its lower mean
to exceed all other ranks' upper means.

The possible-optimum sets can only change when the
varying cell's lower bound crosses another rank's upper
bound, or when its upper bound crosses another rank's
lower bound. The algorithm solves these threshold
equalities using exact rational arithmetic, partitions
the integer seed-count range at critical floor positions,
and checks only the resulting short segments.

Unlike iterating over all conceivable seed counts,
this can handle huge source caps efficiently.
A synthetic one-million-count example is regression
tested; it is mathematical stress testing, not a
biologically plausible P. rex fruit.

All possible optimum ranks in each predator state
and the resulting outer bounds on the excluded-minus-
exposed shift are returned for each integer outcome range.

## Leave-one-plant-out robustness is a separate diagnostic

Even if the excluded-minus-exposed optimum displacement
is guaranteed across **all allowed fruit fates**,
the pooled mean can still depend on one parent plant.
A companion analysis removes each complete plant's
z×G set and recomputes the optimum possible ranks
with all remaining fruits' fate bounds intact.
The original allocation receipt is validated
before omission, never rewritten as a new
randomization experiment.

The synthetic two-plant positive optimum
shift can disappear as a guaranteed direction
after removing the strong-response plant,
even without changing the original data.
This is **between-plant leverage**, not
evidence of actual P. rex selection
heterogeneity. See
`SCH_PEDICULARIS_PLANT_BLOCK_OPTIMUM_SENSITIVITY_V1.md`.

## Scientific distinctions

A mean predator-exclusion effect, a signed contrast
between extreme floral exsertion settings, and a
shift of the entire reproductive optimum are
**different ecological hypotheses**. An intermediate
rank can change the optimal phenotype without
affecting the extreme-rank contrast.

The new method analyzes exactly one completely
ascertained flower at a time. All other unknown fruit
outcomes keep their [lower,upper] ranges.
The original source-locked flower IDs, treatment
assignments, seed caps and verified-zero distinctions
are validated through the existing PR #213 code
before any conditional result is produced.

Unknown output is never set to zero. A counted zero
mature output does not automatically establish
whether seed initiation failed or predators ate all seeds.
No actual source fruit identity is reconstructed.

These calculations are deterministic **finite-sample
partial identification**, not confidence intervals,
a source-independent experimental verification,
a probability model for future seed counts, or
a causal proof that predator exclusion shifts P. rex
trait-specific optima. The focal G and P0
experimental feasibility requirements remain
blocked pending actual field testing. No W1/W2,
pure function optima, SCH L or SLK value is promoted.

## Run

    python scripts/prioritize_pedicularis_optimum_shift_remeasurement.py \
      completed_fruit_fate.csv frozen_fruit_allocation_receipt.json \
      --output conditional_optimum_shift.json

    python -m pytest -q tests/test_pedicularis_optimum_shift_fate_tipping.py

Tests independently recompute the original fruit-fate
estimator after all individual exact integer values in
small censored intervals, checking both possible-optimum
sets and displacement intervals. They also test a
million-integer interval without enumerating that range.

Related:
SCH_PEDICULARIS_FRUIT_FATE_MEASUREMENT_PRIORITY_V1.md
SCH_PEDICULARIS_FRUIT_FATE_OUTCOME_BOUNDS_V1.md
