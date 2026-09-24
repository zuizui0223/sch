# SCH H2 prospective reversal holdout protocol V3

## Why V3 is necessary

V2 correctly fixed the inferential unit, the experimental primary contrast and the outcome-independent opening gate. However, it described the V20-era 463-record priority queue as an untouched prospective source pool.

That was no longer literally true at the V2 freeze. Between V20 and V24, seven records from that queue had already received formal title/abstract decisions.

~~~text
V20 unscreened priority queue      463
formally TA-screened in V21/V23      7
actually unscreened at V24 close   456
~~~

V3 corrects only this source-pool boundary before V25 screening and before any held-out programme is registered.

## Seven records excluded before V3

- SCHPRISMA-000434
- SCHPRISMA-000550
- SCHPRISMA-000648
- SCHPRISMA-000659
- SCHPRISMA-000673
- SCHPRISMA-000775
- SCHPRISMA-000812

These records remain part of the formal 868-record PRISMA denominator. They are excluded only from the prospective V3 primary source pool because their formal TA decisions predate the V3 freeze.

## Active source roster

V3 freezes:

data/SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv

with:

~~~text
active prospective source records   456
Git blob SHA
ab5d4348736ff9ad98ca3ce636bd9522fe74c776
~~~

The roster is mechanically required to equal:

~~~text
original 463-record V20 priority queue
minus
the seven pre-V3 formally screened IDs
~~~

and it preserves the original outcome-blind review order.

## Statistical contract

V3 does not alter H2M1's statistical contract from V2:

- current eight V10-V11 programmes remain development-only;
- primary experimental classes remain MULTI_COMPONENT_OR_CONSUMER_TURNOVER and SINGLE_REGISTERED_MODIFIER;
- spatial/landscape studies remain EXTERNAL_SPATIAL_REPLICATION;
- programme score remains q_j = supported-reversal axes / eligible repeated axes;
- primary prediction remains Delta > 0;
- opening gate remains at least five complete programmes in each experimental class;
- opening remains independent of observed reversal outcomes;
- primary inference remains an upper-tail programme-label permutation test.

## Firewall

The V3 evaluator verifies both source layers before evaluating a registry:

1. original 463-record queue Git blob;
2. active 456-record roster Git blob;
3. exact seven-record set difference;
4. preserved review order;
5. active source IDs are unique and outcome-blind;
6. every future registered primary source belongs to the active 456-record roster.

Thus records already screened before the prospective freeze cannot re-enter by accident.

## Current state

~~~text
registered V3 held-out programmes    0
primary test                      CLOSED
next action                  V25 TA0 SCREEN
~~~

STATUS = PROSPECTIVE_HOLDOUT_V3_FROZEN_TEST_NOT_OPEN
