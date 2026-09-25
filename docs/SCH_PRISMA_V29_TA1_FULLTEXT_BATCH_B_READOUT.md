# SCH PRISMA V29 TA1 full-text batch B readout

## Scope

V29 closes the next four retained TA1 records in frozen review order:

- SCHPRISMA-000510 Abronia umbellata thesis
- SCHPRISMA-000538 Desfontainia fulgens
- SCHPRISMA-000540 Lonicera etrusca
- SCHPRISMA-000542 Ipomopsis aggregata

## Full-text decisions

~~~text
000510 Abronia       EXCLUDE  FT_NO_ANTAGONIST_EVIDENCE
000538 Desfontainia  INCLUDE  DIRECTIONAL_OR_NEAR_PASS
000540 Lonicera      INCLUDE  DIRECTIONAL_OR_NEAR_PASS
000542 Ipomopsis     INCLUDE  DIRECTIONAL_OR_NEAR_PASS
~~~

Abronia is excluded at full text because the focal thesis/source tests moth pollination, pollen limitation and floral-trait vestigialization but does not measure the proposed herbivore channel as a focal antagonist response.

## Formal PRISMA state

~~~text
identified records                  868
title/abstract screened             463
  retained for full text            325
  excluded                          138
title/abstract unscreened           405

full-text included primary      128 -> 131
full-text decision excluded     131 -> 132
full-text unavailable                 1
retained but undecided           66 -> 62
~~~

Evidence lanes:

~~~text
STRICT_LINKED_EXPERIMENT             2
DIRECTIONAL_OR_NEAR_PASS       115 -> 118
EVOLUTIONARY_OUTCOME                39
HISTORICAL_TRANSITION                4
~~~

## Design-only macro gate

Machine pretriage:

~~~text
current primary includes                     131
P1 both responses + common fitness            60
P2 both responses / no common fitness         15
P3 antagonist only                            16
P3 pollinator only                            29
P4 unresolved/neither                         11
~~~

Manual P1 gate:

~~~text
P1 records manually gated                     60
H1 record-level geometry candidates           39
H2 multi-context candidates                   28
benefit-cost coupled role-boundary records     2
~~~

## Biological identification result

None of the three new primary inclusions adds a fixed-role H1 trait geometry.

Desfontainia and Ipomopsis manipulate or observe nectar-robbing state/intensity rather than two functions responding to one independently declared floral trait coordinate.

Lonicera is more informative but in a different way: the same nectar-robbing visitors directly cross-pollinate while also reducing legitimate visitor rates. The interaction therefore enters BENEFIT_COST_COUPLED rather than fixed antagonist conflict.

This adds a second explicit example that consumer identity or behavioral label does not uniquely determine functional sign.

## H1 source-axis coverage

No new H1 candidate is created, so coverage remains:

~~~text
H1 record candidates              39
source-axis covered               39
source-axis evidence records      64
canonical trait axes              50
~~~

## Claim ceiling

V29 supports another coupled-role boundary case and expands the systematic denominator.

It does not:

- add a new strict linked experiment;
- add an H1 conflict axis;
- change the H2M1 prospective registry;
- infer conflict from nectar robbery itself;
- treat the same consumer's positive and negative pathways as independent opposing agents.

STATUS = TA1_FULLTEXT_BATCH_B_COMPLETE_V29
