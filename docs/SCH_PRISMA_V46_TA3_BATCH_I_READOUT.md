# SCH PRISMA V46 deterministic TA3 batch I

## Scope

V46 screens the ninth fixed 25-record TA3 remainder batch from the immutable V3 review order.

~~~text
first review order   278
last review order    303
TA3 records           25
~~~

The frozen TA3 slice contains one non-TA3 review-order gap, so provenance is tested by exact slice identity rather than assuming every integer review order is present.

## Decisions

~~~text
RETAIN_FULLTEXT    6
EXCLUDE           19
~~~

## Retained systems

- Impatiens capensis pollinator-decline selection with herbivory context;
- Arabidopsis lyrata pollinator-mediated and herbivory-associated selection across populations/years;
- Silene latifolia post-pollination scent change in a nursery-pollinator seed-predator system;
- Geranium sylvaticum pollinator preference, floral herbivory and seed predation;
- Silene stellata–Hadena ectypa context-dependent pollinating seed-predator interaction;
- Pedicularis rex cupulate-bract manipulation with legitimate pollinators, robbers, seed predators and seed production.

## Exclusion boundary

Most records in this slice are pollinator-only studies, broad pollinator reviews, scent/morphology studies without ecological receiver responses, or non-plant interaction records.

Pollinator parasites are not promoted to a plant antagonist channel merely because they alter pollinator behaviour.

## Formal state after V46

~~~text
identified records                  868
title/abstract screened             708
  retained for full text            439
  excluded                          269
title/abstract unscreened           160

full-text included primary          153
full-text decision excluded         137
full-text unavailable                 1
retained but full-text undecided    149
~~~

V46 changes no full-text decision, canonical axis, H1/H2 denominator or H2M1 registry.

## Next

Continue deterministic TA3 screening with the tenth frozen 25-record slice. Full-text closure of retained TA3 records remains separate from title/abstract progress.

STATUS = TA3_BATCH_I_SCREEN_COMPLETE_V46
