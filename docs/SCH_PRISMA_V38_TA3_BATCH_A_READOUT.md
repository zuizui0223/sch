# SCH PRISMA V38 TA3 deterministic batch A

## Scope

TA0, TA1 and TA2 are complete. V38 begins the TA3 general remainder without changing the frozen review order.

Batch A is defined mechanically as the first 25 TA3 records in the V3 active source roster:

~~~text
review order 78-102
records          25
~~~

No title is promoted because it appears especially useful to H2M1.

## Decisions

~~~text
RETAIN_FULLTEXT   14
EXCLUDE           11
~~~

Retained records include:

- faba-bean pollination × pest-damage yield experiment;
- Castilleja host-mediated herbivory/pollination/reproduction;
- belowground-herbivore / pollinator synthesis;
- floral-phenotype preferences of bumblebees and thrips;
- nectar-robbery damage × pollinator response;
- native-plant traits for pollinator/herbivore management;
- Tanacetum chemodiversity report pair;
- Lythrum herbivory → floral display → pollinator interaction experiment.

Relevant focused syntheses are retained at TA stage and will be separated from primary-study counts at full text.

## Explicit TA exclusions

The 11 exclusions are records lacking a plant antagonist, lacking a pollinator function, lacking a focal floral signal/reward coordinate, or being a technical method rather than primary/relevant synthesis evidence.

## Formal state after V38

~~~text
identified records                  868
title/abstract screened             508
  retained for full text            353
  excluded                          155
title/abstract unscreened           360

full-text included primary          153
full-text decision excluded         137
full-text unavailable                 1
retained but full-text undecided     63
~~~

V38 changes no full-text decision, canonical axis, H1/H2 denominator or H2M1 registry.

## Frozen-order guarantee

A regression test reconstructs the TA3 tier from the immutable V3 source roster and requires V38 IDs to equal exactly its first 25 records, with review orders 78 through 102.

## Next

Close the 14 V38-retained records at full text or continue deterministic TA3 batching only after preserving this order/provenance boundary.

STATUS = TA3_BATCH_A_SCREEN_COMPLETE_V38
