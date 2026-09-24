# SCH H2 prospective reversal holdout protocol V2

## Status of the amendment

V2 supersedes V1 **before any held-out programme was registered**.

At the amendment point:

~~~text
V1 held-out registry rows = 0
V1 primary test           = CLOSED
held-out outcomes seen    = 0
~~~

V1 remains in the repository as provenance. V2 is the active prospective contract.

The amendment fixes three inferential problems before data accumulation:

1. V1's opening gate depended partly on observing at least two YES and two NO outcomes;
2. observational spatial mosaics could enter the same primary predictor class as experiments;
3. an "any reversal" programme outcome gives programmes with many trait axes more opportunities to score YES.

## Frozen holdout source

The source pool is not an open-ended future literature search.

It is the already frozen outcome-blind queue:

~~~text
data/SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv

formal PRISMA denominator             868
already title/abstract screened       405
untouched holdout records             463
Git blob SHA
1ffd1849b4381a43bb85b2d3473161caabdac510
~~~

The existing review order remains authoritative.

V10 or V11 results cannot be used to reorder these 463 records.

A programme cannot enter the V2 registry unless its primary source belongs to this frozen queue.

## Development set

The eight programmes used by V10-V11 remain permanently excluded from the primary holdout test:

- Brassica rapa;
- Dalechampia scandens;
- Erysimum mediohispanicum;
- Gymnadenia conopsea;
- Helianthus annuus ssp. texanus;
- Lobelia cardinalis;
- Lythrum salicaria;
- Trifolium repens.

They are hypothesis-generating data only.

## Prospective hypothesis H2M1-V2

> Among held-out **experimental** TOTAL_SELECTION_EFFECT programmes, programmes that change multiple biotic components or consumer identity/composition will have a larger programme-level fraction of uncertainty-supported directional-reversal axes than programmes that change one registered biotic modifier.

## Predictor classification

Classification must occur before selection sign, significance or reversal outcome is adjudicated.

### MULTI_COMPONENT_OR_CONSUMER_TURNOVER

Primary-eligible.

Use when an experiment:

- independently varies at least two registered biotic dimensions; or
- manipulates consumer identity/composition/assemblage,

while retaining a comparable plant-fitness TOTAL_SELECTION_EFFECT estimand.

### SINGLE_REGISTERED_MODIFIER

Primary-eligible.

Use when one registered biotic modifier is experimentally manipulated and consumer identity/composition remains conceptually fixed.

### EXTERNAL_SPATIAL_REPLICATION

Not primary-eligible.

Population, landscape and geographic mosaics remain biologically valuable external replication. They are not mixed into the primary causal experimental contrast.

### UNRESOLVED_CONTEXT_DIMENSIONALITY

Not primary-eligible.

Use when design class cannot be assigned without interpretation that could depend on the observed outcome.

## Eligible repeated trait axis

An axis is eligible only when:

1. it is the same canonical trait coordinate across contexts;
2. the estimand is TOTAL_SELECTION_EFFECT;
3. at least two source-defined contexts are comparable;
4. usable uncertainty exists for the source-defined contexts used to establish direction.

All uncertainty-resolved, source-defined contexts are evaluated.

No favorable context pair may be selected after viewing signs.

## Axis-level event

A bidirectionally supported reversal requires:

~~~text
supported positive total selection
+
supported negative total selection
on the same canonical trait axis
~~~

Support may come from:

- confidence interval excluding zero;
- reported SE with |beta / SE| > 1.96;
- reported p < 0.05 paired with the coefficient sign.

Missing uncertainty is not imputed.

## Programme-level score

The biological programme is the independent unit.

For programme j:

~~~text
q_j =
number of eligible repeated axes with bidirectionally supported reversal
-----------------------------------------------------------------------
number of eligible repeated TOTAL_SELECTION_EFFECT axes
~~~

This prevents a programme with nine measured axes from automatically having nine times the inferential weight of a programme with one axis.

Each programme receives equal weight in the primary cross-programme comparison.

## Primary estimand

~~~text
Delta =
mean(q_j | MULTI_COMPONENT_OR_CONSUMER_TURNOVER)
-
mean(q_j | SINGLE_REGISTERED_MODIFIER)
~~~

Frozen directional prediction:

~~~text
Delta > 0
~~~

## Outcome-independent opening gate

The primary test opens when:

~~~text
complete primary programmes
MULTI_COMPONENT_OR_CONSUMER_TURNOVER >= 5

complete primary programmes
SINGLE_REGISTERED_MODIFIER           >= 5
~~~

There is **no requirement** that reversals, YES outcomes or NO outcomes occur before the test opens.

If every programme has q_j = 0, that is a valid confirmatory result and the test returns Delta = 0 rather than remaining closed.

This is deliberately different from V1.

## Primary inference

Registered test:

~~~text
upper-tail programme-label permutation test
on equal-programme-weighted q_j
~~~

If the number of possible label assignments is <= 200,000, all assignments are enumerated exactly.

Otherwise V2 uses 200,000 Monte Carlo programme-label permutations with frozen seed 120926.

This affects computation only; the estimand and directional hypothesis do not change.

## External replication

Spatial and landscape programmes are accumulated separately.

They can answer whether the qualitative pattern also recurs outside experiments, but they cannot by themselves identify a causal effect of "multidimensionality".

## Current state

At V2 freeze:

~~~text
registered V2 holdout programmes       0
complete primary programmes            0
primary opening gate              CLOSED
primary test                    NOT RUN
~~~

The immediate next operation is therefore not another analysis of the eight development programmes.

It is to resume the frozen 463-record screen, beginning with the existing TA0 review order, and admit new programmes only through this firewall.

## Claim ceiling

V2 may eventually test H2M1-V2 in held-out experiments.

It does not estimate:

- literature-wide reversal prevalence;
- universal reversal probability;
- a pooled selection coefficient across incompatible scales;
- a causal effect from observational spatial mosaics;
- independent evidence from multiple axes within the same programme.

~~~text
STATUS = PROSPECTIVE_HOLDOUT_V2_FROZEN_TEST_NOT_OPEN
NEXT = FROZEN_TA0_SCREENING
~~~
