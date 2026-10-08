# Which P. rex fruit outcome is worth measuring?

## Biological priority

The existing fruit-fate analysis distinguishes mature counted seed output,
pre-dispersal verified zero, partially censored seeds and unobserved
reproductive outcomes. Missing fruit outputs can bias comparisons if predator
attack itself changes their chance of being counted.

The useful question is **which uncertain allocated fruit could determine the
sign** of the predefined exsertion or predator-exclusion contrast once its
final intact seed number is verified, even if other fruits remain unresolved?

This is a **conditional value of obtaining the true maturity outcome**,
not a prediction of the fruit's seed number and not a probability model.

## Exact integer tipping-point mathematics

For an uncertain fruit with true viable seeds x between documented bounds
[a,b], let n be the number of allocated flowers in its trait-setting × G
cell, and [L,U] the original exact high-minus-low contrast interval.

If the flower contributes **positively** (HIGH or EXCLUDED):

    new lower(x) = L + (x-a)/n
    new upper(x) = U - (b-x)/n

If it contributes **negatively** (LOW or EXPOSED):

    new lower(x) = L + (b-x)/n
    new upper(x) = U - (x-a)/n

Strictly positive selection is certified when new lower > 0;
strictly negative selection requires new upper < 0.
The code solves these exact strict inequalities as inclusive
**integer seed-count intervals**, without sampling, approximation,
or iterating over large seed potential caps.

For a fruit of width b-a, perfect outcome ascertainment
reduces its cell mean and each affected contrast interval width
by **exactly (b-a)/n**, regardless of the unknown actual value.
This is a guaranteed *precision gain*, not guaranteed
classification of the contrast's sign.

## Explicit synthetic 20-flower demonstration

The separate non-gating P. rex fixture contains two plants,
five exsertion ranks and two predator states; all 20
allocated flower IDs are retained.

In the predator **EXPOSED** group, LOW-rank mean viable
seed count is 1.5. HIGH rank has one known viable seed
and an additional unknown fruit x between 0 and 3.

    HIGH−LOW = (1+x)/2 − 1.5 = (x−2)/2.

| Value found if one fruit were measured | Mean viable HIGH−LOW seeds/flower | Strict sign conclusion |
|---:|---:|---|
| 0 | −1.0 | Negative |
| 1 | −0.5 | Negative |
| 2 | 0 | Unresolved at zero |
| 3 | +0.5 | Positive |

Thus an *exact assessment of that fruit* can resolve
the sign if the true value is 0, 1 or 3. The code
does **not** interpret three of four integer values
as a 75% chance of success; no predictive distribution
over the unknown maturity count was measured.

The EXCLUDED HIGH-rank fruit is also uncertain,
but the EXCLUDED high-minus-low contrast was already
guaranteed **positive** despite that uncertainty.
For deciding an as-yet-unknown selection direction,
the exposed fruit has higher conditional priority.
For reducing numeric bound width alone, the excluded
unknown fruit gives a larger improvement (2 vs
1.5 viable seeds per flower). These are **different**
design objectives, and the ranking states its rule.

The source fixture's excluded-minus-exposed optimum
rank shift is already robustly positive. The present
module **does not** claim to re-evaluate optimum
rank displacement after an arbitrary one-fruit result;
its threshold statements concern the specified
direct seed-count contrasts.

## Source and field-method contract

Input: the complete allocated fruit-fate CSV and frozen
fruit-only allocation receipt from PR #213.
The algorithm reruns every original identity, fate
and seed-cap check, including all 20 source flower IDs
in its illustration.

The only candidate fruits are those whose final intact
seed counts remain intervals with strictly positive
width. A verified ZERO yield is not a missing value.

Each candidate is evaluated for:
1. HIGH-minus-LOW z within the same G condition,
   if allocated at the predeclared extreme trait ranks.
2. EXCLUDED-minus-EXPOSED at the same assigned z.
3. The exact reduction in the width of those contrast
   intervals from a complete single-fruit assessment.

All other uncertain fruits stay unresolved. The list
ranks observations first by the number of presently
unresolved contrasts *capable of* sign certification
conditional on some possible measured result, then
the number of affected unresolved contrasts, then
the maximum interval-width reduction.

This is a measurement **information map**, not
a causal model or expected-cost optimization.
Some flowers with missing outcomes have been lost
and cannot be remeasured; prospective monitoring,
pre-dispersal collection and verified individual
ovule/seed-potential caps are therefore necessary.

## Scientific boundary

The 2016 original P. rex paper excluded fully consumed,
unscorable capsules. Without an actual recovered
maturity history we **cannot** retroactively call
those fruits verified zero, obtain the exact missing
counts, or claim an empirical P. rex selection shift.

Conditional intervals are about **finite allocated
flowers** and do not supply population confidence
intervals, a test of trait-manipulation first stage,
independent predator exclusion selectivity, or pure
functional optima. One significant versus one
nonsignificant result is not directly an interaction
test; here no such p-value is calculated.

This remains a *non-gating* companion to the
existing separate pollen/fruit design. No P0/P1/G,
W1/W2, SCH L or SLK R/K/Phi permission changes.

## Reproduction

    python scripts/prioritize_pedicularis_fruit_fate_remeasurement.py \
      completed_fruit_fate.csv frozen_fruit_allocation_receipt.json \
      --output priority.json

    python -m pytest -q tests/test_pedicularis_fruit_fate_measurement_priority.py

Related: SCH_PEDICULARIS_FRUIT_FATE_OUTCOME_BOUNDS_V1.md
and Issue #204.
