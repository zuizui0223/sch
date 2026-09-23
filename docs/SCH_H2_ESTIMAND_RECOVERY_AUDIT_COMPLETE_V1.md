# SCH H2 estimand-recovery audit — complete V20 frontier

## Result

All 29 records in the frozen V20 `RETAIN_FULLTEXT` queue have now been source-adjudicated for their ability to contribute the commensurate H2 `TOTAL_SELECTION_EFFECT` family.

~~~text
full-text-pending records audited = 29
new TOTAL_SELECTION_EFFECT promotions = 0
~~~

The queue was frozen before this source audit and was not retuned after seeing the zero-promotion yield.

## Why this matters

The broad H2 layer has already accumulated many ecological context cases.

The current bottleneck is not ecological richness.

It is measurement compatibility.

A study can contain:

~~~text
pollinators
+
antagonists
+
plant reproduction
~~~

and still fail to contribute the target estimand when those quantities are not attached to the same focal plant trait coordinate or when they do not form a repeated selection/final-performance measure.

The completed V20 audit therefore provides direct development evidence for the SCH identification claim.

## Failure structure across all 29 records

~~~text
NO_SHARED_TRAIT_COORDINATE                         8
NOT_PRIMARY_EMPIRICAL_STUDY                        7
NO_COMMON_FITNESS_SELECTION_ESTIMAND               3
NO_COMMON_REPRODUCTIVE_OUTCOME                     3
DUPLICATE_OR_SECONDARY_REPORT                      2
NO_MEASURED_CONSUMER_COMPONENTS                    2
NO_DIRECT_ANTAGONIST_RESPONSE_ON_SELECTED_TRAIT    1
NO_FOCAL_POLLINATOR_ANTAGONIST_TRAIT_ESTIMAND     1
NO_MEASURED_POLLINATOR_COMPONENT                   1
NO_ANIMAL_POLLINATOR_COMPONENT                     1
~~~

The single largest category is failure to identify one shared plant trait coordinate.

That is not a null ecological result.

It is an estimand-identification failure.

## Examples

### Rich ecology, wrong coordinate

Several studies measured mutualists, antagonists and plant performance but on a habitat-, community- or interaction-state coordinate rather than one plant trait.

Examples include:

- Isoplexis individual interaction typologies;
- Syzygium restored versus unrestored habitat;
- cucumber early-herbivory treatment;
- Arctostaphylos stand/year pollination and predation;
- Baptisia resource × seed-predator experiments.

These studies remain biologically relevant but do not enter the same numeric selection family.

### Plant trait and fitness, missing matched antagonist component

Ipomoea cavalcantei measured phenotypic selection on floral traits and fruit-set fitness.

Pre-dispersal seed predators were invoked as a likely explanation for ovary-width selection but were not estimated as a matched local antagonist component on the selected trait.

### Consumer effects on reproduction, no variable plant trait

Hypoestes aristata is especially instructive.

Individual visitor taxa have positive, neutral or negative effects on seed production, including a nectar thief with negative reproductive effects.

But the explanatory coordinate is visitor identity/frequency, not one varying plant trait.

### Strong multifunctional mechanism, no common fitness estimand

The Ficus macula study directly demonstrates a multifunctional structure with secretory, thermal and insect-behavior functions.

It does not estimate repeated plant-fitness selection on macula state.

### Reviews and mechanistic molecular studies

Seven records are non-primary syntheses.

Other records directly characterize floral scent biosynthesis or herbivory-induced volatile genes without measuring both consumer-mediated selection routes.

These are source-chasing or mechanism evidence, not commensurate H2 numeric rows.

## Consequence for the current H2 gate

The completed 29-record audit means the current V20 full-text frontier cannot supply a new `TOTAL_SELECTION_EFFECT` cluster under the registered identification rules.

Therefore the correct next step is not to keep searching within these 29 records for a desirable sign or to relax the estimand.

It is to return to the frozen unscreened cohort.

~~~text
NEXT_FRONTIER = 463 title/abstract-unscreened records
~~~

## Prospective next-screen principle

The next priority queue must again be frozen before outcome adjudication.

Useful priority signals may include:

- explicit selection/fitness language;
- a declared floral trait coordinate;
- both pollinator and antagonist concepts;
- repeated population/year/treatment context.

But the priority rule must change review order only.

It must not change inclusion or estimand criteria.

## Statistical implication

The broad H2 structural breadth and the commensurate-estimand breadth are now empirically separated.

The practical lesson is:

~~~text
many ecological context rows
!=
many independent commensurate selection clusters
~~~

This is exactly why the H2 estimand-family gate remains fail-closed even after the broad breadth gate can pass.

## Publication implication

The zero-promotion yield should not be written as a prevalence estimate for the ecological literature.

It is a development result about the current frozen screening frontier:

> among the 29 V20 full-text-pending records, none added a new repeated same-trait TOTAL_SELECTION_EFFECT estimand after source-level adjudication.

That statement is bounded to this queue and this estimand definition.

## Status

~~~text
V20_FULLTEXT_PENDING = 29
V20_ESTIMAND_AUDITED = 29
TOTAL_SELECTION_EFFECT_PROMOTIONS = 0

FORMAL_PRISMA_INCLUSION_CHANGED_BY_AUDIT = NO
PRIORITY_RULE_RETUNED_AFTER_RESULTS = NO

NEXT_SCREENING_FRONTIER = 20 V21 TA0 RETAINED FULLTEXT RECORDS
~~~


## Frozen next-frontier queue

The 463 title/abstract-unscreened records have now been assigned an outcome-blind review order.

~~~text
TA0 explicit selection    32
TA1 final performance     25
TA2 repeated context      20
TA3 remainder            386
~~~

This queue changes review order only and does not alter any screening or estimand criterion.

See:

- `data/SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv`
- `data/SCH_H2_UNSCREENED_TA_PRIORITY_READOUT_V1.json`
- `docs/SCH_H2_UNSCREENED_TA_PRIORITY_V1.md`

The next adjudication frontier is the 32-record TA0 batch.


## V21 TA0 outcome-blind screen

The frozen 463-record queue has now advanced through its first priority tier.

~~~text
TA0 screened        32
retained full text  20
excluded            12
remaining TA-unscreened 431
~~~

The exclusions are design/relevance exclusions only. No result sign or significance was used.

The next estimand-recovery frontier is the 20 V21 TA0 records retained for full text.
