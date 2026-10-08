# Recover reproductive selection even when predator fate is not identified

## Why this is a biological rather than a bookkeeping problem

Sun, Armbruster & Huang (2016; doi:10.1093/aob/mcw097) examined
*Pedicularis rex* capsules for intact mature seeds, damaged seeds and
unfertilized ovules. In severely consumed capsules (up to five per
population), seed number could not be assessed. Those fruit outcomes
were omitted from the original seed-count analysis.

In a **new experiment**, some outcomes could nonetheless be treated as
known viable-seed zero, while other fruit losses remain unknown.

The pivotal distinction is:

    viable mature seed count     ≠    initial seed count
    viable mature seed count     ≠    proportion predated
    viable mature seed count     ≠    reason a capsule was empty

A recovered pre-dispersal empty capsule can provide convincing evidence
of **zero mature intact seeds**, without identifying whether fertilization
failed or larvae consumed all initiated seeds. In that case **fitness
may be exactly zero while predation q remains undefined**. A lost
capsule, on the other hand, cannot generally be assigned a zero:
seeds may have survived, dispersed, or the fruit may have been missed.

Critically, the 2016 paper's excluded cases do **not** have the
prospectively coded pre-dispersal zero evidence required by this
protocol. We do not retroactively recode them as zero. The underlying
2016 supplemental/raw flower records are not recovered, and **no
new P. rex field effect is estimated here**.

## Four prospectively recorded outcomes

Every **allocated flower ID** from the separate fruit cohort must be
carried through the analysis.

| Status | Primary SCH viable-seed count | Initial/predation stage information |
|---|---|---|
| MATURE_COUNTED | Exact recorded intact count | q computed only with complete identifiable seed-fate counts and initiated>0 |
| ZERO_VIABLE_VERIFIED | Exactly 0 | q remains unidentified if initiated seed number is unknown |
| PARTIALLY_CENSORED | Documented interval [L,U] | q not recovered |
| FATE_UNOBSERVED | [0,U] with an independently measured or prospectively frozen seed-potential cap | q not recovered |

**ZERO_VIABLE_VERIFIED** requires a positive pre-dispersal
verification code, including a genuinely recovered empty capsule,
a documented pre-maturity failure, or documented complete seed
destruction. It does not mean that predation caused the zero.

**FATE_UNOBSERVED** is *not* a verified zero, including when a
fruit disappears or its reproductive outcome is not readable.
The ovule/seed-potential upper must have measured-pre-event or
prospectively committed provenance. A site-average ovule number
(such as the 2016 paper's mean of 25.96) is **not an upper bound**
on any unobserved individual flower and must never be used
as one.

**PARTIALLY_CENSORED** can retain a counted minimum of intact seeds
and a smaller maximum potential count, but those constraints must
be independently documented in the field; the input declaration
alone cannot authenticate the claimed biological evidence.

All outputs use **intact mature seeds per flower**, not viable
seeds divided by ovules. No current P0, P1, G or four-state
W1/W2 threshold is changed.

## Exact interval arithmetic on the assigned finite sample

For each assigned z rank and independent-predator exposure state G,
each flower contributes an interval [l_i,u_i].
If all allocated flowers are included, the observed-sample mean is
bounded by:

    mean viable G,z ∈ [Σ_i l_i/n, Σ_i u_i/n].

This is exact rational finite-sample accounting, not a normal
confidence interval. For a HIGH-minus-LOW z contrast at one G:

    Δ_z ∈ [L_high - U_low, U_high - L_low].

A sign fixed away from zero is identified **conditional on valid
fruit outcome caps**, even if some individual fruits were not
measured at maturity.

Likewise, for the predator exclusion contrast at each z:

    excluded − exposed ∈
      [L_excluded − U_exposed, U_excluded − L_exposed].

For a finite-grid optimum, a setting k **can** be an optimum
if its U_k is at least as large as the greatest other
settings' lower bound. A strictly guaranteed unique
optimum requires L_k > every other U_j. The possible rank
ranges in excluded and exposed states also bound the
direction of their **descriptive optimum displacement**.

The code explicitly does **not** claim that the source
allocation hash proves actual randomized implementation,
lack of interference between neighboring flowers, balanced
source population sampling, or any causal mediator identity.
Without those field checks the estimands are conditional
descriptions, not a confirmed causal SCH compromise.

## Adversarial synthetic demonstration (not P. rex)

Construct **two plants**, each with one randomized intact-fruit
flower per five z ranks × two predator G states. Retain all 20
assigned flower IDs.

In the predator **excluded** state:

- LOW rank: 2 intact seeds and one **confirmed zero** ->
  mean fitness exactly 1 seed/flower;
- ranks 1–3: 3 intact seeds per fruit -> mean 3;
- HIGH rank: 7 intact seeds and one **unobserved**
  outcome with an independently frozen maximal potential
  of 4 -> HIGH mean in [3.5, 5.5].

Thus HIGH is a **uniquely identified finite-grid
reproductive optimum** in the excluded state, despite
an entirely missing fruit outcome.

In the predator **exposed** state:

- LOW rank: 3 intact seeds and one verified zero -> mean 1.5;
- ranks 1–3: mean exactly 3;
- HIGH rank: 1 intact seed and one unobserved outcome
  with upper bound 3 -> HIGH mean [0.5, 2].

The exposed-state optimum lies somewhere among ranks
1, 2 and 3, never the HIGH rank 4. Thus the
**excluded-minus-exposed optimum rank shift** is bounded
to **[1,3]**, positive across every feasible completion
of the unknown fruit outcomes.

However, the direct exposed-state HIGH-minus-LOW
fitness contrast remains inconclusive. The method
correctly differentiates an identified **optimum shift**
from an unsupported claim about every pairwise gradient.

These are constructed values, not observations or
evidence that P. rex really has such an optimum shift.

## Relation to PR #203 and PR #212

- PR #203: destructive pollen sentinels and distinct
  fruit-bearing flowers; stage decomposition on matched
  fruit records when seed fates are completely known.
- PR #212: exact polynomial-time optimization of
  **unpaired** complete initiation and predation
  distributions using integer seed-count constraints.
- **This addition:** outcomes may themselves be censored,
  unobserved, or confirmed zero. It directly bounds
  viable seed fitness without pretending to recover
  missing initiation/predation q.

Thus these are **different missing-information problems**.
An unknown q does not make verified zero mature fitness
unknown. But when final viability is not observed at all,
the valid upper cap must be retained and all allocated
flowers remain in the analysis. Bounds may be too wide
to identify any optimum; then the result must stay
unresolved.

## Reproduction

The provided template is:

    empirical/architecture/PEDICULARIS_TWO_COHORT_FRUIT_FATE_TEMPLATE_V1.csv

One row per preallocated flower, carrying the exact
FROZEN_FIELDS from the fruit allocation receipt plus
all outcome-fate columns. Run:

    python scripts/bound_pedicularis_fruit_fate_selection.py \
      completed_fruit_fate.csv frozen_fruit_allocation_receipt.json \
      --output nonconfirmatory_fate_bounds.json

The existing non-gating two-cohort analyzer is unchanged
and still requires complete individually countable fruit
outcomes. This separate module **does not unlock** the
same-flower P2 or full four-state SCH route.

Regression tests cover verified zero with undefined q,
missing high-risk fruits with positive seed caps, partial
censoring, source-ID/allocation drift, false pre-dispersal
proof, invalid counts and both identified/unidentified
trait responses.

## Research priority

In the next field pilot, the most informative protocol
change is to record pre-dispersal fruit fate **independently**
from the damage/seed-development stage:
fruit present or absent, dispersed/not yet dispersed,
intact mature seeds demonstrably counted, empty fruit
verification, larval destruction evidence, and the
earliest defensible per-flower seed-potential cap.

That permits a real answer to **whether predator-exposed
and predator-excluded reproductive optima can be ordered**,
even if larvae prevent assigning exact predation fractions
to every fruit.
