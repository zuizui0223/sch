# SCH H2 unscreened title/abstract priority queue V1

## Why this queue exists

The broad H2 ecological layer now passes its original structural breadth gate, but the commensurate estimand-family gate remains fail-closed.

Current broad plant-performance state:

~~~text
cases     42
axes      14
clusters   8
~~~

Largest current estimand family:

~~~text
TOTAL_SELECTION_EFFECT
cases     30
axes       8
clusters   3
~~~

The 29 V20 full-text-pending records were all audited prospectively for their ability to expand this family.

Result:

~~~text
new TOTAL_SELECTION_EFFECT promotions = 0
~~~

The correct next step is therefore to return to the frozen unscreened cohort rather than relaxing the estimand.

## Frozen source universe

~~~text
identified denominator           868
title/abstract screened          405
title/abstract unscreened        463
~~~

The 463 records remain part of the original frozen denominator.

This queue does not add new records.

It changes review order only.

## Outcome-blind priority rule

Priority uses only:

- frozen bibliographic title;
- frozen query IDs from the registered identification search.

It does not use:

- ecological result sign;
- conflict versus alignment;
- p-values;
- whether SCH predictions are supported;
- later full-text knowledge.

Every record was originally identified through a registered floral-trait × pollinator × antagonist query.

The extra priority signals are therefore title-level indicators of likely estimand recoverability.

## Priority tiers

### TA0 — explicit selection

Title contains:

~~~text
selection / selective / selected
+
explicit floral-trait language
~~~

Current count:

~~~text
32
~~~

These are reviewed first because they are the most likely to contain a repeated trait-selection estimand.

Candidate status remains:

`TOTAL_SELECTION_EFFECT_CANDIDATE_UNCONFIRMED`

### TA1 — final performance

Title contains:

~~~text
fitness / reproductive success / reproduction
/ fruit set / seed set / seed production / fecundity
+
explicit floral-trait language
~~~

Current count:

~~~text
25
~~~

These are also candidates for the target estimand family, but no estimand is assigned from the title alone.

### TA2 — repeated context

Title contains:

~~~text
population / geographic / spatial / temporal
/ year / variation / mosaic / gradient
/ treatment / experiment
+
explicit floral-trait language
~~~

Current count:

~~~text
20
~~~

These are prioritized for H2 repeated-context structure.

### TA3 — remainder

All other unscreened records remain eligible for normal title/abstract screening.

Current count:

~~~text
386
~~~

They are not excluded.

They simply follow the estimand-priority records in review order.

## Frozen queue

~~~text
TA0_EXPLICIT_SELECTION   32
TA1_FINAL_PERFORMANCE     25
TA2_REPEATED_CONTEXT      20
TA3_REMAINDER            386

TOTAL                    463
~~~

The full queue is:

`data/SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv`

The reproducible builder is:

`scripts/build_sch_h2_unscreened_ta_priority.py`

The receipt is:

`data/SCH_H2_UNSCREENED_TA_PRIORITY_READOUT_V1.json`

## Why this does not bias the ecological result

The priority queue is frozen before the 463 records are screened.

The queue can affect only:

`which record is inspected first`

It cannot affect:

- title/abstract inclusion criteria;
- full-text inclusion criteria;
- shared-coordinate requirements;
- common-fitness requirements;
- estimand-family assignment;
- biological cluster identity.

A TA0 record can still be excluded or fail the target estimand.

A TA3 record can still ultimately contribute the target estimand.

## First review frontier

The immediate next batch is the 32 TA0 records.

This set includes obvious high-information titles such as:

- Helianthus floral-head selection by pollinators and seed predators;
- Protea inflorescence-colour selection by pollinators and seed predators;
- Lobelia floral-trait selection by pollinators and herbivores;
- Brassica floral-signal selection by pollinators and herbivores.

It also deliberately contains likely false positives and secondary/non-focal records.

Those remain important because the screen must apply the same rules without retuning the queue after seeing yield.

## Claim ceiling

This queue supports workflow prioritization only.

It does not support:

- inclusion;
- conflict prevalence;
- selection prevalence;
- a new estimand-family cluster;
- any statement about TA0 yield before screening.

~~~text
QUEUE_STATUS = FROZEN_OUTCOME_BLIND
SOURCE_SCREEN_VERSION = V20

UNSCREENED = 463
TA0 = 32
TA1 = 25
TA2 = 20
TA3 = 386

NEXT_ACTION = SCREEN_TA0_WITH_FROZEN_TITLE_ABSTRACT_RULES
~~~


## V21 progress

The queue itself remains frozen as the prospective 463-record review order.

V21 has now adjudicated the first tier:

~~~text
TA0_EXPLICIT_SELECTION = 32 screened
RETAIN_FULLTEXT = 20
EXCLUDE = 12
remaining title/abstract unscreened = 431
~~~

The next step is full-text/estimand adjudication of the 20 retained TA0 records. TA1–TA3 remain in their original frozen order.
