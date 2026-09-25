# SCH PRISMA V39 TA3 deterministic batch B

## Scope

V39 screens the second fixed 25-record TA3 remainder batch from the immutable V3 review order.

~~~text
review order 103-127
records          25
~~~

## Decisions

~~~text
RETAIN_FULLTEXT   10
EXCLUDE           15
~~~

Retained records include direct mutualist-antagonist systems, focused syntheses, and report/version pairs that require explicit full-text deduplication.

Key retained boundaries:

- Chelonanthus circum-floral nectaries, bat pollination and ant protection against floral herbivores;
- herbivory-induced changes in Brassica pollinator behaviour;
- faba-bean pollination × pest × yield version of record;
- attractive/defensive phytochemical integration in Arabis;
- parasite × herbivory effects on bumblebee response;
- fig pollinator / gall-wasp synthesis;
- Protea mutualist/seed-predator trait matching;
- Cerrado pollinator–florivore density dependence;
- Tanacetum chemodiversity version of record.

## Explicit exclusions

Records are excluded where the focal study contains only pollination, only antagonism, omics/chemistry without ecological receiver responses, a non-floral interaction, or a broad editorial/meeting report rather than primary/relevant synthesis evidence.

## Formal state after V39

~~~text
identified records                  868
title/abstract screened             533
  retained for full text            363
  excluded                          170
title/abstract unscreened           335

full-text included primary          153
full-text decision excluded         137
full-text unavailable                 1
retained but full-text undecided     73
~~~

V39 changes no full-text decision, canonical axis, H1/H2 denominator or H2M1 registry.

## Provenance

A regression test reconstructs the TA3 tier from the frozen V3 source roster and requires V39 to equal exactly its second 25 records, review orders 103 through 127.

Known report pairs are intentionally retained at title/abstract stage:

- 000436 is the version of record corresponding to earlier faba-bean report 000401;
- 000456 is the final Tanacetum chemodiversity paper corresponding to earlier report identities 000424/000425.

These dependencies are resolved explicitly at full text rather than by silent title-stage deletion.

## Next

Continue deterministic TA3 screening from review order 128 and/or close the 10 retained V39 records at full text.

STATUS = TA3_BATCH_B_SCREEN_COMPLETE_V39
