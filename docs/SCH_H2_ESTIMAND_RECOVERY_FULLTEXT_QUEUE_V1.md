# SCH H2 estimand-recovery full-text queue V1

## Why this queue exists

The broad H2 ecological layer can contain many local cases while still failing as a numeric comparative model if the cases do not estimate the same biological quantity.

The current H2 development state therefore separates:

~~~text
broad ecological breadth
!=
commensurate estimand breadth
~~~

The largest current plant-performance estimand family is `TOTAL_SELECTION_EFFECT`, but its independent-cluster coverage remains much smaller than the broad H2 coverage.

The next literature-recovery step should therefore prioritize studies that are most likely to contribute a compatible selection / final-fitness estimand **without inspecting the sign of the ecological result**.

## Source universe

This V1 queue is restricted to the 29 records retained at title/abstract screening in V20 whose full-text decision is still pending.

~~~text
V20 RETAIN_FULLTEXT = 29
~~~

It does not alter inclusion.

It changes review order only.

## Outcome-blind priority signals

Priority uses only:

- title;
- the already-frozen title/abstract screening note;
- source metadata.

It does not use:

- conflict sign;
- alignment sign;
- statistical significance of the desired result;
- whether SCH's hypotheses are supported.

### FT0 — explicit selection

Required text signals:

~~~text
selection / selective
+
focal floral trait
+
pollinator
+
antagonist
~~~

Current records:

1. `SCHPRISMA-000317` — *Ipomoea cavalcantei* floral integration / phenotypic selection;
2. `SCHPRISMA-000400` — *Brassica rapa* floral volatile artificial selection.

These are screened first because the title/abstract metadata directly signals a selection estimand.

### FT1 — final performance

Required text signals:

~~~text
fitness / reproduction / fruit set / seed set
+
focal floral trait
+
pollinator
+
antagonist
~~~

Current records:

3. `SCHPRISMA-000309` — fitness consequences of trait-mediated plant–pollinator interactions;
4. `SCHPRISMA-000310` — radish hybrid fitness with pollinator/herbivore context;
5. `SCHPRISMA-000386` — banana poka nectar robbing with pollination/reproduction context.

These are candidates for a final-performance or total-selection estimand, but no estimand family is assigned until the full text is adjudicated.

### FT2 — context rich

Required text signals:

~~~text
population / geographic / spatial / temporal / treatment / experiment
+
focal floral trait
+
pollinator
+
antagonist
~~~

Current records:

6. `SCHPRISMA-000370` — mutualism–antagonism gradient;
7. `SCHPRISMA-000372` — habitat fragmentation context;
8. `SCHPRISMA-000378` — geographic isolation / pollination syndrome / nectar-robber context.

These are prioritized for H2 context structure even when a selection estimand is not explicit in the title.

### FT3 — other retained full text

The remaining 21 V20 records keep their original full-text eligibility.

They are not rejected.

They simply follow the estimand/context-priority records in review order.

## Current frozen queue

~~~text
FT0_EXPLICIT_SELECTION = 2
FT1_FINAL_PERFORMANCE   = 3
FT2_CONTEXT_RICH        = 3
FT3_OTHER_RETAINED      = 21

TOTAL                    = 29
~~~

The frozen queue is:

`data/SCH_H2_ESTIMAND_RECOVERY_FULLTEXT_QUEUE_V1.csv`

The builder is:

`scripts/build_sch_h2_estimand_recovery_fulltext_queue.py`

## Full-text adjudication questions

Every priority record must still pass the normal SCH gates.

The full text must answer, in order:

1. Is this a primary biological study?
2. What exact plant trait coordinate is analyzed?
3. Are pollinator and antagonist contributions linked to that same coordinate?
4. Is there a common plant outcome?
5. What is the estimand?
6. Is the estimand repeated across populations, years, treatments or consumer regimes?
7. Is uncertainty reported?
8. Does the record add an independent biological cluster or only another row inside an existing programme?

Candidate estimand labels are not accepted from the title alone.

## Promotion target

The immediate target is not simply more H2 rows.

It is:

> more independent biological clusters with a commensurate repeated-context selection or final-performance estimand.

In particular, a record that contributes `TOTAL_SELECTION_EFFECT` in a new independent cluster is more valuable to the current H2 modelability problem than many additional rows from an already represented cluster.

## Claim ceiling

This queue supports only workflow prioritization.

It does not support:

- study inclusion;
- conflict prevalence;
- selection prevalence;
- publication-quality moderator effects;
- treating all final-performance outcomes as numerically commensurate;
- lowering the registered modelability gates.

~~~text
QUEUE_STATUS = FROZEN_OUTCOME_BLIND
FULLTEXT_PENDING = 29
ESTIMAND_PRIORITY = 5
CONTEXT_PRIORITY = 3
OUTCOME_SIGN_USED_FOR_PRIORITY = NO
~~~

## Next stage

After the eight priority records are adjudicated, update the H2 estimand-family registry.

If the commensurate-family gate still cannot be reached from current full-text candidates, move to a separately frozen title/abstract priority queue for the 463 unscreened records in the original 868-record denominator.

That expansion must use the same design-first, outcome-blind logic.
