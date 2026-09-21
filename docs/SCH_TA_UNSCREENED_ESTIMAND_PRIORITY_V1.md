# SCH next title/abstract frontier — outcome-blind estimand-priority rule V1

## Why the frontier changes

The completed V20 estimand-recovery audit inspected all 29 full-text-pending records and yielded:

~~~text
TOTAL_SELECTION_EFFECT promotions = 0 / 29
~~~

The correct next step is therefore to return to the frozen title/abstract-unscreened cohort rather than relax the estimand.

Current frontier:

~~~text
frozen candidates             868
formally TA screened          405
TA unscreened                 463
~~~

## Prospective review-order rule

This rule is frozen before the next title/abstract decisions.

It changes **review order only**.

### TA0 — explicit selection / fitness

Title contains:

- selection / selective;
- fitness.

### TA1 — final reproductive performance

Otherwise title contains language such as:

- reproductive success / output / performance;
- fecundity;
- fruit set / fruit production;
- seed set / seed production / seed output.

### TA2 — repeated context

Otherwise title contains context language such as:

- population / geographic / spatial;
- temporal / year;
- gradient;
- habitat / environment / fragmentation / landscape;
- variation / context / community.

### TA3 — other unscreened

All remaining frozen unscreened records.

## Tie-breakers within a tier

1. floral-trait + pollinator + antagonist language all visible in the title;
2. explicit focal-trait language in the title;
3. repeated-context language in the title;
4. number of matched priority phrases;
5. record ID.

## What this rule does not do

It does not:

- retain or exclude a title/abstract;
- change the PRISMA denominator;
- change full-text eligibility;
- use conflict/alignment sign;
- use any desired result;
- relax same-axis, common-outcome or estimand-family criteria.

All 463 records remain formally UNSCREENED until human title/abstract adjudication.

## Why this priority is appropriate now

The broad H2 layer already passes the ecological breadth gate after Polygala and Tanacetum.

The active bottleneck is commensurate estimand breadth.

Therefore the next human-screening effort should see explicit selection/fitness candidates first while keeping the scientific gate unchanged.

## Output

The deterministic builder:

`scripts/build_sch_ta_unscreened_estimand_priority.py`

can materialize:

- an ordered 463-record CSV;
- a JSON receipt with tier counts;
- no formal screening decisions.

## Claim ceiling

~~~text
PRIORITY_RULE = FROZEN_BEFORE_NEXT_SCREEN
FORMAL_TA_DECISIONS_GENERATED = 0
OUTCOME_SIGN_USED = NO
SEARCH_COORDINATE_CHANGED = NO
SCIENTIFIC_ADMISSION_RULE_CHANGED = NO
~~~
