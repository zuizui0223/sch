# SCH PRISMA V30 TA1 full-text batch C readout

## Scope

V30 closes the next four retained TA1 records in frozen review order:

- SCHPRISMA-000543 Tirpitzia sinensis
- SCHPRISMA-000546 Sesamum radiatum
- SCHPRISMA-000548 Tecomella undulata
- SCHPRISMA-000549 Clinopodium alpinum

All four are formally included as DIRECTIONAL_OR_NEAR_PASS. None is promoted to STRICT_LINKED_EXPERIMENT.

## Formal PRISMA state

~~~text
identified records                  868
title/abstract screened             463
  retained for full text            325
  excluded                          138
title/abstract unscreened           405

full-text included primary      131 -> 135
full-text decision excluded         132
full-text unavailable                 1
retained but undecided           62 -> 58
~~~

Evidence lanes:

~~~text
STRICT_LINKED_EXPERIMENT             2
DIRECTIONAL_OR_NEAR_PASS       118 -> 122
EVOLUTIONARY_OUTCOME                39
HISTORICAL_TRANSITION                4
~~~

Geographic/context coverage:

~~~text
positive geographic contrast    27 -> 28
positive receiver contrast      25 -> 26
joint geographic + receiver     23 -> 24
~~~

Clinopodium provides the new joint spatial/receiver contrast via a 1000-m elevational gradient with turnover in legitimate visitor community and nectar-robbing frequency.

## Design-only macro gate

~~~text
current primary includes                     135
P1 both responses + common fitness            64
P2 both responses / no common fitness         15
P3 antagonist only                            16
P3 pollinator only                            29
P4 unresolved/neither                         11

H1 record-level geometry candidates           39
H2 multi-context candidates                   28
benefit-cost coupled role-boundary records     3
~~~

## Biological identification result

None of the four studies adds a fixed-role H1 trait geometry.

Tirpitzia measures floral morphology, robbery susceptibility, hawkmoth behaviour and seed fitness, but it does not estimate matching pollinator and robber response functions on the same morphological axis.

Sesamum adds a third benefit-cost/role-boundary example: Xylocopa latipes acts both as a primary robber and a legitimate pollinator, so functional sign depends on behavioural state.

Tecomella shows that experimentally increased robbery can change pollinator movement and increase fruit set, but robbery state is the manipulated interaction context rather than a shared plant trait coordinate.

Clinopodium provides strong spatial context evidence: legitimate visitor composition and nectar robbery turn over with elevation and relate differently to seed production, but no shared plant trait axis is isolated.

## H1 source-axis coverage

No new H1 candidate is created, so:

~~~text
H1 record candidates              39
source-axis covered               39
source-axis evidence records      64
canonical trait axes              50
~~~

## Claim ceiling

V30 strengthens evidence for context-dependent consumer role and spatial interaction turnover.

It does not:

- identify a new conflict axis;
- change the H2M1 prospective registry;
- treat robbed/unrobbed state as a plant trait coordinate;
- infer causal trait geometry from elevational interaction turnover;
- increase STRICT_LINKED_EXPERIMENT count.

STATUS = TA1_FULLTEXT_BATCH_C_COMPLETE_V30
