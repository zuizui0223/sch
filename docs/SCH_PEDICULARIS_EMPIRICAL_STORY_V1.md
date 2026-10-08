# Pedicularis rex empirical story v1

## One biological question

> **Do seed predators displace the reproductive optimum of floral exsertion
> toward lower values, away from trait states that deliver greater pollination
> performance?**

This is the focal biological paper that becomes available if the registered
P. rex execution chain is completed.

It is not a paper about how to qualify a barrier, estimate a threshold, or
calculate a generic conflict index. Those are enabling steps.

## Why P. rex is unusually informative

The existing natural-history programme already supplies four independent
pieces of biological motivation.

### 1. One floral coordinate is pulled in opposite directions

Greater corolla exsertion above the water-bearing bract predicts greater
stigmatic pollen receipt, while the same exposed floral geometry increases
pre-dispersal seed-predator risk.

Thus the system already has a real pollinator-antagonist conflict signature.

### 2. Pollination success and antagonist risk are coupled

In the seven populations with linked plant-level morphology, pollen and
seed-outcome data, the 2016 best seed-predation model retained positive
exsertion, lower-lip width and pollen-load terms plus population.

The admissible observation is:

```text
flowers/plants with greater pollen receipt
also tend to incur greater later seed-predation risk.
```

This does not show that pollen is the predator cue.

### 3. Antagonist weight is strongly context dependent

Xia, Sun & Liu (2013; doi:10.1098/rsbl.2013.0387) report a
density-dependent reversal in how patch size relates to seed-predator attack.
This is an intriguing local context signal, not a proven change in floral
optima or a patch-robust interaction effect.

In their 2011 density x patch-size analysis:

```text
initial seed set   interaction F = 44.556
final seed set     interaction F =  0.023
fruit predation    interaction F = 10.605
seed predation     interaction F =106.270.
```

The paper's post-hoc contrasts show that patch-size effects on predation can
reverse between sparse and dense patches.

The key contrast is that the authors report density x size interactions
in initial seed set and predation but not final seed set. However, the
predictors vary among only 11 independent patches (five sparse, six dense),
whereas the original capsule-level ANOVAs report residual degrees of freedom
of 2047 or 2345. The interaction significance therefore needs a
patch-respecting reanalysis; lack of final-seed-set significance is not proof
of buffering or biological cancellation.

A sharper mechanism to examine is **success–risk coupling**. On matched
capsules, final intact seed set depends not just on average initial seed set
and predation, but also on their within-context covariance:

```text
E[final] = E[initial] (1 - E[predation]) - Cov(initial, predation).
```

Whether that covariance changes with density and patch size is unknown and
requires the Dryad workbook. This motivates separating initial reproduction,
antagonist loss and final reproduction in the causal study. The historical
Xia2013 data do not identify the registered independent G effect, floral
optimum displacement or a capsule-level covariance result. See
`SCH_PEDICULARIS_XIA2013_PATCH_UNIT_AUDIT_V1.md`.

### 4. The two functions may be separable in time

Pollination occurs during the open-flower phase. Predator oviposition occurs
after flowers open and before ovary swelling.

The event-time pilot therefore asks whether a natural interval exists between
pollination completion and antagonist commitment:

```text
Delta_T = min(T_attack, T_swell) - T_poll.
```

A positive interval makes selective late antagonist removal biologically
possible. A non-positive interval indicates temporal entanglement and redirects
method development.

Delta_T is an enabling ecological mechanism, not the main paper endpoint.

## Primary causal hypothesis

The registered full surface gives two directly identified state-specific
reproductive optima under natural pollination:

```text
z_P* = predator excluded
z_C* = predator exposed.
```

The primary directional prediction is:

```text
z_P* > z_C*.
```

In words:

> removing seed predators should move the reproductive optimum toward greater
> floral exsertion.

This is **enemy-induced optimum displacement**.

The claim remains on the reproductive-state scale. `z_P*` is not renamed a
pure pollinator optimum.

## Observation feasibility of the headline

The W1/W2 causal story needs a pollen-receipt slope as well as mature seed
fitness. Those are different biological processes measured at different
stages. Sun et al. (2016) destructively crushed stigmas to count pollen and
usually measured mature seeds on different flowers from the same plants.

The current SCH P2 code nevertheless assigns both outcomes to one flower ID.
That is an **unvalidated same-flower observation assumption**, not a
biological result. Before P2, qualify a same-flower pollen assay that preserves
mature seed set, or prospectively redesign W1/W2 for randomized disjoint pollen
sentinels and seed flowers. This cannot be repaired by filling the CSV with
plant means or attributing sentinel pollen counts to fruit-bearing flower IDs.

See `SCH_PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_V1.md`.

## Pollination-performance consequence

Randomized multi-level exsertion is measured with pollen receipt in both
predator states.

The nested prediction is:

```text
higher randomized z
-> greater pollen receipt.
```

Therefore, if both predictions hold:

```text
predator exposure
-> lower state-specific optimum

and

lower z
-> lower pollen receipt.
```

The biological conclusion is:

> seed-predator pressure displaces the realized reproductive optimum away from
> trait states that provide greater pollination performance.

This is stronger and more ecological than the generic statement that
pollinators and enemies exert opposing selection.

## Stronger reproductive tier

Initial seed set is analyzed separately.

If greater randomized exsertion also increases initial seed set in both G
states, then the antagonist-induced downward optimum shift has a
pre-predation reproductive cost as well as a pollen-receipt cost.

This gives a two-tier result:

```text
Tier 1
enemy-induced optimum displacement
+ pollen-receipt cost

Tier 2
enemy-induced optimum displacement
+ pollen-receipt cost
+ initial-seed-set cost.
```

Tier 2 is stronger, but neither tier by itself proves that seed predators
historically maintain pollen limitation.

## What would be genuinely surprising

The interesting result is not simply that mutualists and antagonists disagree.
That is already known observationally.

The sharper result would be:

```text
the trait value maximizing reproduction changes when the enemy is removed,
and the enemy-present optimum lies in a region that performs worse for
pollination.
```

That connects antagonism to an actual displacement of the adaptive surface,
rather than to two separate selection coefficients.

## Natural-phenotype check

The sham/natural exsertion level provides a descriptive check:

```text
is the realized natural phenotype closer to z_C* than z_P*?
```

If yes, the observed phenotype is consistent with the current
mutualist-antagonist reproductive state rather than the predator-free state.

This is not evidence of historical adaptation or heritable evolutionary
response.

## Success-risk coupling as a secondary mechanism

After randomized z is controlled, the experiment can ask whether stronger
pollination performance still predicts antagonist risk.

If the pollen-risk association persists, it supports a success-risk coupling
that is not explained solely by exsertion.

It still does not identify the predator cue. Floral odour, phenology, reward,
plant quality or another correlated state would require a separate assay.

## Falsifiers

The focal hypothesis is rejected for the tested population/season if any core
link fails:

```text
predator removal does not shift the reproductive state optimum upward;

or

higher randomized exsertion does not increase pollen receipt.
```

A stronger seed-set version is rejected if higher z does not increase initial
seed set.

These negative outcomes do not erase the broader SCH conflict result. They
show that observed opposing selection does not translate into the proposed
enemy-induced pollination-performance cost in that context.

## Predeclared outcome worlds

The empirical interpretation is frozen before focal outcomes. Use
`PEDICULARIS_EMPIRICAL_OUTCOME_WORLDS_V1.csv` rather than choosing a story
after the surface is seen.

```text
W0  primary causal-compromise surface not recovered
    -> focal displacement story is not opened

W1  antagonist displacement + positive pollen slope + positive initial-seed slope
    -> enemy-induced optimum displacement with pollination and pre-predation
       reproductive cost

W2  antagonist displacement + positive pollen slope, but no positive initial-seed slope
    -> enemy-induced optimum displacement with pollen-receipt cost only

W3  antagonist displacement, but no positive pollen slope
    -> enemy shifts the reproductive optimum through some other pathway;
       do not call it a pollination-performance constraint

W4  positive pollen slope, but no antagonist optimum displacement
    -> exsertion benefits pollination, but enemies do not measurably displace
       the optimum in this context

W5  neither predicted displacement nor positive pollen slope
    -> the focal enemy-displacement mechanism is not recovered
```

These worlds are deliberately asymmetric. Initial seed set strengthens W1 over
W2, but cannot rescue W3-W5. None of the worlds automatically identifies a pure
pollinator optimum, historical adaptation, or antagonist maintenance of pollen
limitation.

Machine classifier:

```text
scripts/classify_pedicularis_empirical_outcome.py
```

For a final interpretation bundle that also carries the independent timing
mechanism and optional pure-function upgrade without changing W0-W5, use:

```text
scripts/map_pedicularis_empirical_outcomes.py
docs/SCH_PEDICULARIS_EMPIRICAL_OUTCOME_MAP_V1.md
```

## Claim ladder

```text
existing evidence
shared exsertion conflict                         RECOVERED
geographic antagonist-weight variation            RECOVERED
density x patch-size antagonist-weight context     RECOVERED
component structure masked by final reproduction   OBSERVATIONAL
pollination-success / predation-risk coupling      OBSERVATIONAL

natural timing pilot
temporal separability Delta_T                      TO TEST

full causal surface
enemy-induced state-optimum displacement           TO TEST
higher z -> pollen receipt                         TO TEST
higher z -> initial seed set                       TO TEST

secondary
success-risk coupling after randomized z control   TO TEST

not identified by the above
pure pollinator optimum                            NO
antagonist maintenance of pollen limitation        NO
historical adaptation                              NO
predator cue identity                              NO
adaptive pollen limitation                         NO
```

## Novelty boundary

The paper is not novel because pollinators and enemies impose conflicting
selection, because both consumer classes are manipulated, because a floral
trait is manipulated over multiple levels, or because enemy context can move a
floral optimum. All of those ingredients have close precedents.

The bounded close-precedent audit in
`SCH_PEDICULARIS_EMPIRICAL_NOVELTY_BOUNDARY_V1.md` places novelty on the joint
design/estimand:

```text
randomized multi-level shared z
x selective P
x selective G
-> W00(z), W10(z), W01(z), W11(z)
-> bounded reproductive state optima
-> direct antagonist-removal optimum displacement
-> pollination-performance consequence of that displacement.
```

This is a bounded precedent claim, not a global "first ever" statement.

## Paper spine

The empirical paper can therefore be written around one biological sentence:

> **A floral enemy can shift the reproductive optimum of a multifunctional
> trait away from phenotypes that perform better for pollination.**

The supporting sequence is:

```text
natural conflict and success-risk coupling
-> temporal qualification of selective enemy removal
-> randomized exsertion x pollination x predator surface
-> enemy-induced optimum displacement
-> pollination-performance cost of that displacement.
```

The methodological machinery remains in Methods and validation supplements.
The ecological result stays in the title, abstract, Results and Discussion.
