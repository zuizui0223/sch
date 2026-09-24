# SCH H2 prospective reversal hypothesis V12

## Why V12 exists

V10 and V11 turned the H2 layer from a generic "context matters" statement into a structured pilot result.

The current qualified family contains 81 TOTAL_SELECTION_EFFECT cases across 31 trait axes and 8 independent programmes. Among 27 repeated axes, 14 cross zero at the point-estimate level, but only 3 contain supported positive and supported negative contexts. V11 further showed that context mechanisms are strongly confounded with the small set of programmes.

That makes V11 useful for hypothesis generation, but not for testing which ecological contexts are most likely to generate directional reversal.

V12 freezes the next test before any new holdout outcome is inspected.

## Frozen hypothesis

Among new experimental programmes, changing multiple biotic weights or changing consumer identity/composition will produce a larger programme-level fraction of uncertainty-supported directional-reversal axes than changing the intensity of one biotic factor alone.

This prediction may fail. A negative result is confirmatory information and must not trigger retuning of the classes.

## Pilot / holdout split

The eight programmes already used in V10-V11 are permanently pilot-only for this hypothesis:

- Gymnadenia conopsea
- Trifolium repens
- Erysimum mediohispanicum
- Brassica rapa
- Lobelia cardinalis
- Dalechampia scandens
- Lythrum salicaria
- Helianthus annuus ssp. texanus

They may be shown as motivation but cannot contribute to the V12 confirmatory estimate.

The holdout is the already frozen, outcome-blind title/abstract queue:

~~~text
formal PRISMA denominator          868
already screened before V12       405
V12 holdout records               463
~~~

Exact source:

data/SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv

Git blob at freeze:

1ffd1849b4381a43bb85b2d3473161caabdac510

The existing review order is retained. V11 mechanism or reversal results cannot be used to reorder the 463 records.

## Prospective design classes

Design class is assigned before selection coefficient sign, significance or uncertainty outcome is extracted.

### A - MULTIWEIGHT_OR_CONSUMER_TURNOVER

Use when an experimental programme:

- independently manipulates at least two biotic dimensions in the relevant context contrast; or
- changes consumer identity/composition/assemblage while measuring the same plant fitness endpoint.

### B - SINGLE_FACTOR_INTENSITY

Use when an experimental programme changes one biotic dimension while consumer identity/composition is held conceptually fixed.

Examples include a single pollination-supplementation axis, one herbivory-reduction treatment, or one damage-intensity manipulation.

### External spatial replication

EXTERNAL_SPATIAL_REPLICATION contains observational population, landscape or geographic contrasts.

These studies remain biologically valuable, but they are not pooled into the primary causal A-versus-B comparison.

### Fail closed

A design that cannot be assigned from source design information alone is:

UNCLASSIFIABLE_FAIL_CLOSED

It is not classified using the observed direction of selection.

## Eligible axis

An axis enters the V12 outcome only when it has:

1. the same canonical trait coordinate across contexts;
2. TOTAL_SELECTION_EFFECT as the estimand family;
3. at least two qualified contexts;
4. usable uncertainty for the contexts being compared.

A bidirectionally supported reversal requires at least one supported-positive and at least one supported-negative context on that same axis.

Point crossings without support do not count as V12 events.

## Independent unit and score

Trait axes are nested measurements, not independent replicates.

For each new biological programme j:

~~~text
q_j =
number of eligible axes with bidirectionally supported reversal
---------------------------------------------------------------
number of eligible repeated TOTAL_SELECTION_EFFECT axes
~~~

Every programme receives equal weight in the primary comparison regardless of how many axes its source reports.

The primary estimand is:

~~~text
Delta =
mean(q_j | MULTIWEIGHT_OR_CONSUMER_TURNOVER)
-
mean(q_j | SINGLE_FACTOR_INTENSITY)
~~~

Frozen directional prediction:

~~~text
Delta > 0
~~~

A secondary programme-level endpoint records whether a programme contains at least one supported-reversal axis.

## Inference gate

No inferential comparison is licensed until the future holdout yields at least:

~~~text
new A programmes                       >= 5
new B programmes                       >= 5
programmes with non-zero q_j           >= 2
~~~

Before that point:

DESCRIPTIVE_COUNTS_ONLY_FAIL_CLOSED

After the gate passes, the registered primary inference is an exact permutation test over programme labels for the equal-programme-weighted difference in mean q_j.

The gate is a minimum estimability requirement, not a promise that the eventual analysis will be highly powered.

## What V12 changes scientifically

SCH now has three sequential evidence states:

~~~text
V10
context can change realized selection direction

V11
point reversal, asymmetric support and supported reversal are distinct;
mechanism cells are post-hoc and programme-confounded

V12
a directional mechanism hypothesis is frozen against untouched evidence
~~~

This is the important upgrade. SCH no longer needs to keep mining the same eight programmes for a prettier explanation.

The next ecological result can genuinely confirm or falsify a prediction.

## Claim ceiling

V12 does not claim that multidimensional biotic change is already the cause of the three supported reversals.

It licenses only a future test in untouched programmes.

It also does not:

- use the 463-record queue as 463 independent biological replicates;
- use trait axes as independent inferential units;
- pool observational spatial mosaics into the primary causal comparison;
- treat unsupported point crossings as reversals;
- alter the existing title/abstract screening order after seeing V11;
- guarantee that enough new programmes will qualify to open the inference gate.

~~~text
STATUS = PROSPECTIVE_HOLDOUT_HYPOTHESIS_FROZEN
PILOT = V10_V11_EIGHT_PROGRAMMES
HOLDOUT = PREEXISTING_463_UNSCREENED_RECORDS
PRIMARY_UNIT = INDEPENDENT_BIOLOGICAL_PROGRAMME
PRIMARY_INFERENCE = FAIL_CLOSED_UNTIL_GATE
~~~
