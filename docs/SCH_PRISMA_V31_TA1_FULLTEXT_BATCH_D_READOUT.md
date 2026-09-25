# SCH PRISMA V31 TA1 full-text batch D readout

## Scope

V31 closes the next four retained TA1 records in frozen review order:

- SCHPRISMA-000564 Digitalis purpurea
- SCHPRISMA-000565 Digitalis preprint/report
- SCHPRISMA-000599 Lonicera etrusca
- SCHPRISMA-000610 Brassica nigra

## Full-text decisions

~~~text
000564 Digitalis       INCLUDE  DIRECTIONAL_OR_NEAR_PASS
000565 Digitalis preprint EXCLUDE FT_DUPLICATE_DATASET_OR_REPORT
000599 Lonicera        INCLUDE  DIRECTIONAL_OR_NEAR_PASS
000610 Brassica        INCLUDE  DIRECTIONAL_OR_NEAR_PASS
~~~

The preprint is excluded only at full text so report duplication remains explicit and auditable.

## Formal PRISMA state

~~~text
identified records                  868
title/abstract screened             463
  retained for full text            325
  excluded                          138
title/abstract unscreened           405

full-text included primary      135 -> 138
full-text decision excluded     132 -> 133
full-text unavailable                 1
retained but undecided           58 -> 54
~~~

Evidence lanes:

~~~text
STRICT_LINKED_EXPERIMENT             2
DIRECTIONAL_OR_NEAR_PASS       122 -> 125
EVOLUTIONARY_OUTCOME                39
HISTORICAL_TRANSITION                4
~~~

## Design-only result

All three new primary studies enter the broad P1 design stratum because pollinator/antagonist information and a common reproductive outcome are present.

None enters H1 trait geometry:

- Digitalis manipulates robbery state and measures pollinator behaviour plus seed production;
- Lonicera aphid herbivory is an upstream cause of floral development, pollination and reproduction;
- Brassica manipulates herbivore identity/timing and measures downstream flowering phenotype, pollinator visitation, pollen-beetle colonization and seed fitness.

These are strong ecological-interaction studies, but no single independently declared floral trait coordinate is fitted with matched pollinator and antagonist response functions.

## Macro gate

~~~text
current primary includes                     138
P1 both responses + common fitness            67
H1 record-level geometry candidates           39
H2 multi-context candidates                   28
~~~

Thus systematic coverage and P1 ecological relevance continue to rise while the H1 trait frontier stays fixed.

## Claim ceiling

V31 does not add a new conflict axis, strict linked experiment, or H2M1 programme. It preserves duplicate-report accounting and the distinction between upstream interaction context and shared-trait functional geometry.

STATUS = TA1_FULLTEXT_BATCH_D_COMPLETE_V31
