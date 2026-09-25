# SCH PRISMA V40 deterministic TA3 batch C

## Scope

V40 screens the third fixed 25-record TA3 remainder batch from the immutable V3 review order.

~~~text
review order 128-152
records          25
~~~

## Decisions

~~~text
RETAIN_FULLTEXT   13
EXCLUDE           12
~~~

## Retained ecological boundaries

V40 retains several high-value role/context systems without changing the order of review:

- Silene latifolia with Hadena ectypa as a pollinating seed predator;
- fig/fig-wasp mutualism and conflict;
- Erica floral conspicuousness with bird pollination and bee nectar robbing;
- fragmented Salvia populations with effective-pollinator loss and pollen/nectar robbers;
- berry-system multi-trophic dissertation evidence;
- herbivory-induced changes in floral traits, pollinator visitation and fruit set in Palicourea;
- a Manduca pollinating-herbivore life cycle;
- linalool pollinator-attraction / herbivore-defence synthesis;
- plant-pollinator network linkage rules including exploitation barriers;
- Centrosema herbivory-pollination fitness costs;
- exploitative low-efficiency small bees in Campanula;
- bee pollination / ant seed predation / yield in Indonesian homegardens.

## Explicit exclusions

V40 excludes records where:

- only pollinator responses are present;
- only non-pollinator interactions are present;
- ecological functions are hypothesized but not measured;
- the item is a commentary/article highlight rather than primary/relevant synthesis evidence;
- the focal response is microbial community assembly rather than a plant floral coordinate or plant reproductive outcome.

## Report/version handling

SCHPRISMA-000463 and SCHPRISMA-000464 are both retained because they are repository/published identities of the Erica bee-avoidance study. Report dependence is resolved explicitly at full text rather than silently during title screening.

## Formal state after V40

~~~text
identified records                  868
title/abstract screened             558
  retained for full text            376
  excluded                          182
title/abstract unscreened           310

full-text included primary          153
full-text decision excluded         137
full-text unavailable                 1
retained but full-text undecided     86
~~~

V40 changes no full-text decision, canonical axis, H1/H2 denominator or H2M1 registry.

## Provenance

A regression test reconstructs the frozen TA3 tier and requires V40 to equal exactly its third 25 records, review orders 128 through 152.

## Next

Continue deterministic TA3 screening from review order 153 and/or begin full-text closure of retained V38-V40 records without outcome-based reprioritization.

STATUS = TA3_BATCH_C_SCREEN_COMPLETE_V40
