# SCH PRISMA V28 TA1 full-text batch A readout

## Scope

V28 closes the first four retained TA1 records in frozen review order:

- SCHPRISMA-000420 Solidago altissima
- SCHPRISMA-000429 Vaccinium hirtum
- SCHPRISMA-000449 dissertation on floral mutualists/antagonists
- SCHPRISMA-000479 Odontonema cuspidatum

All four are formally included as DIRECTIONAL_OR_NEAR_PASS. None is promoted to STRICT_LINKED_EXPERIMENT because the focal floral trait itself is not independently manipulated in the required crossed causal geometry.

## Formal PRISMA state

Title/abstract state remains:

~~~text
screened                         463
retained for full text           325
excluded                         138
unscreened                       405
~~~

Full-text state becomes:

~~~text
included primary studies     124 -> 128
decision excluded                131
unavailable                        1
retained but undecided        70 -> 66
~~~

Evidence lanes:

~~~text
STRICT_LINKED_EXPERIMENT            2
DIRECTIONAL_OR_NEAR_PASS      111 -> 115
EVOLUTIONARY_OUTCOME               39
HISTORICAL_TRANSITION               4
~~~

## Design-only macro gate

Machine pretriage after V28:

~~~text
current primary includes                     128
P1 both responses + common fitness            57
P2 both responses / no common fitness         15
P3 antagonist only                            16
P3 pollinator only                            29
P4 unresolved/neither                         11
~~~

Manual P1 gate:

~~~text
P1 records manually gated                     57
H1 record-level geometry candidates           39
H2 multi-context candidates                   28
~~~

V28 source decisions:

~~~text
000420 Solidago
  H1 = INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY
  reason = herbivory is an upstream context, not a receiver response to the floral VOC coordinate

000429 Vaccinium
  H1 = ELIGIBLE_SAME_COORDINATE
  H2 = ELIGIBLE_MULTI_CONTEXT
  axis = flowering phenology

000449 dissertation
  H1 = UNRESOLVED_SOURCE
  reason = multiple experiments/traits require chapter- and axis-level decomposition

000479 Odontonema
  machine P1 = NO
  reason = direct pollinator response to the focal floral coordinate is not recovered in the current source audit
~~~

## Source-axis coverage

Vaccinium receives one source-axis record for flowering rank/synchrony.

~~~text
record-level H1 candidates             39
source-axis covered H1 candidates      39
source-axis evidence records           64
model-bearing H1 source records        33
canonical trait axes                   50
~~~

The canonical ledger remains at 50 axes because the V28 source-axis record has not yet been promoted into the frozen canonical model ledger.

## Claim ceiling

V28 advances systematic and design-level coverage only. It does not:

- estimate a new conflict prevalence;
- run H1 regression;
- promote the Vaccinium phenology axis to conflict/alignment without source-level outcome geometry;
- use the unresolved dissertation as multiple independent studies;
- alter the V3 prospective H2M1 outcome registry.

STATUS = TA1_FULLTEXT_BATCH_A_COMPLETE_V28
