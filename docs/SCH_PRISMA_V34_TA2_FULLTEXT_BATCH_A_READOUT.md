# SCH PRISMA V34 TA2 full-text batch A

## Scope

V34 closes the first four TA2 records retained for full text:

- SCHPRISMA-000569 Isoplexis canariensis
- SCHPRISMA-000594 Tribulus cistoides
- SCHPRISMA-000621 Solanum pollen-dispensing preprint
- SCHPRISMA-000622 Solanum pollen-dispensing version of record

## Full-text decisions

~~~text
000569  INCLUDE  DIRECTIONAL_OR_NEAR_PASS
000594  INCLUDE  EVOLUTIONARY_OUTCOME
000621  EXCLUDE  FT_DUPLICATE_DATASET_OR_REPORT
000622  INCLUDE  DIRECTIONAL_OR_NEAR_PASS
~~~

## Formal state

~~~text
primary studies                  142 -> 145
full-text decision excluded      134 -> 135
retained but undecided            63 -> 59

DIRECTIONAL_OR_NEAR_PASS         129 -> 131
EVOLUTIONARY_OUTCOME              39 -> 40
STRICT_LINKED_EXPERIMENT                2
~~~

Title/abstract state remains 483 screened / 339 retained / 144 excluded / 385 unscreened.

## Evidence-lane separation

### Isoplexis 000569

Bird exclusion and hand-pollination demonstrate effective pollinator service and insect nectar thieves/secondary robbers occur on the same flowers. The plant trait coordinate itself is not manipulated or modeled with matched two-function response surfaces, so the study is broad P1 ecological evidence but H1-ineligible.

### Tribulus 000594

Island and continental populations differ in floral traits associated with pollination and fruit-defense traits associated with vertebrate granivory. Direct receiver responses and a common reproductive estimand are absent. The study therefore enters EVOLUTIONARY_OUTCOME rather than H1 functional geometry.

### Solanum 000621 / 000622

000621 is excluded explicitly as the preprint duplicate of the published 000622 report.

000622 links poricidal anther morphology to pollen dispensing under bee-like vibration. The same bees provide pollination service while consuming pollen, creating a service-cost coupling. Because the source lacks a common plant reproductive endpoint for the two functions, it is a P2 boundary case rather than H1 conflict geometry.

## Design funnel

~~~text
current primary studies                     145
P1 both-response/common-fitness               72
P2 both-response/no-common-fitness            16
H1 record-level candidates                    39
H2 multi-context candidates                   29
~~~

The H1 frontier does not expand.

## Ecological interpretation

TA2 begins by splitting repeated-context evidence into qualitatively different inferential objects:

- ecological near-pass;
- comparative evolutionary outcome;
- report duplication;
- coupled pollination-service/pollen-consumption cost.

> repeated ecological context is not itself one estimand and cannot be pooled as if every study measured the same conflict geometry.

## Next

Continue TA2 full-text closure in frozen order with Sabatia 000626, Hakea 000628, Silene-Hadena 000721 and the within-flower scent synthesis 000733.

STATUS = TA2_FULLTEXT_BATCH_A_COMPLETE_V34
