# SCH PRISMA V25 TA0 holdout screening readout

## Boundary

V3 froze the prospective source roster before V25:

~~~text
prospective V3 source roster        456
~~~

That roster is immutable provenance. V25 does not shrink or rewrite it.

V25 advances the **formal PRISMA screening state** within that frozen source pool.

## Starting formal state after V24

~~~text
identified records                  868
title/abstract screened             412
  retained for full text            284
  excluded                          128
title/abstract unscreened           456
~~~

## TA0 closure

The frozen V20 priority queue contained 32 TA0 explicit-selection records.

Four had already received formal TA decisions before V3:

- SCHPRISMA-000648
- SCHPRISMA-000659
- SCHPRISMA-000775
- SCHPRISMA-000812

V25 therefore screens only the remaining 28.

~~~text
V25 new decisions                    28
  RETAIN_FULLTEXT                    20
  EXCLUDE                             8
~~~

Exclusion reasons:

~~~text
TA_NO_ANTAGONIST_COMPONENT           5
TA_NOT_FLORAL_SIGNAL                 1
TA_NO_POLLINATOR_COMPONENT           1
TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS 1
~~~

Focused syntheses are retained at TA stage when relevant. Therefore SCHPRISMA-000503 and SCHPRISMA-000561 are retained for source-role/full-text adjudication rather than being excluded merely for being review/chapter records.

## Formal state after V25

~~~text
identified records                  868
title/abstract screened             440
  retained for full text            304
  excluded                          136
title/abstract unscreened           428

full-text included primary          120
full-text decision excluded         131
retained but full-text undecided     53
~~~

V25 makes no new full-text inclusion, no new TOTAL_SELECTION_EFFECT promotion and no V3 held-out programme registration.

## Holdout firewall

Every V25 record is a member of the frozen V3 active source roster.

The four TA0 records already screened before V3 are not re-screened in V25.

Thus:

~~~text
V3 prospective source provenance    unchanged
V25 formal TA screening progress    advanced
V3 held-out programme registry      still empty
~~~

## Next step

The next high-information task is full-text/source adjudication of the 20 V25-retained records, with design class frozen before any selection-sign outcome is extracted.

STATUS = TA0_HOLDOUT_SCREEN_COMPLETE_V25
