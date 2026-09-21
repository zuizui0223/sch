# SCH H2 estimand-recovery audit — Batch 1

## Result

The first eight outcome-blind priority records from the frozen V20 full-text queue have now been source-adjudicated.

~~~text
audited records = 8
TOTAL_SELECTION_EFFECT promotions = 0
~~~

This is a useful identification result, not a reason to retune the priority rules after seeing the outcome.

## Why the eight records did not promote

### SCHPRISMA-000317 — Ipomoea cavalcantei

The study is a genuine phenotypic-selection study with fruit-set fitness and pollination experiments.

However, the focal antagonist route is not measured as a matched trait-specific component. Pre-dispersal seed predators are offered as a likely explanation for selection on ovary width.

Therefore:

~~~text
phenotypic selection = YES
common fruit-set fitness = YES
matched antagonist response on selected trait = NO
H2 TOTAL_SELECTION_EFFECT promotion = NO
~~~

### SCHPRISMA-000400 — Brassica rapa floral volatiles

The study directly estimates heritability and correlated response under artificial selection on floral volatiles.

Pollinator attraction and herbivore deterrence motivate the biology, but the focal experiment does not estimate those two consumer-mediated selection components.

Therefore it informs evolutionary architecture, not the H2 repeated consumer-context estimand.

### SCHPRISMA-000309 — trait-mediated plant–pollinator fitness landscapes

This is an “On the Nature of Things” conceptual article proposing a fitness-landscape framework.

It does not contribute a new empirical pollinator–antagonist trait-selection dataset.

### SCHPRISMA-000310 — radish hybrid fitness

The study estimates fitness of wild × crop hybrids across experimental populations.

Shared pollinators are part of the biological system, but the focal estimand is hybrid fitness and crop-gene persistence. Herbivore resistance is discussed as a possible crop trait rather than measured as an opposing consumer component on one floral coordinate.

### SCHPRISMA-000386 — banana poka nectar robbing

The focal field study directly establishes nectar-robbing behavior by native honeycreepers and measures floral nectar resources.

It does not measure a local plant reproductive consequence of robbing.

Therefore it is visitor-role ecology, not a final-performance selection estimand.

### SCHPRISMA-000370 — Isoplexis mutualism–antagonism gradient

This is a rich empirical study.

It identifies individual interaction typologies involving mutualists and antagonists and links those typologies to female reproductive success and mating-network position.

The relevant coordinate is interaction-network composition/strength, not one declared plant phenotypic trait.

Therefore it is a strong ecological context/design case but not a shared-trait TOTAL_SELECTION_EFFECT row.

### SCHPRISMA-000372 — fragmentation and hawthorn arthropods

Fragmentation affects pollinator activity, leaf herbivory and dry-fruit mass.

However, the pollinator and antagonist channels are not linked to one declared plant trait coordinate.

It therefore fails the H2 shared-coordinate estimand target.

### SCHPRISMA-000378 — Himalayan Roscoea

Five years of observation identify bumblebees as the dominant pollination service and long-tongued butterflies/moths as nectar robbers across three Roscoea species.

This is valuable repeated visitor-role and pollination-service ecology.

It lacks the common final-fitness trait-selection estimand required for the targeted TOTAL_SELECTION_EFFECT family.

## Batch-1 reason structure

~~~text
NOT_PRIMARY_EMPIRICAL_STUDY                    1
NO_DIRECT_ANTAGONIST_RESPONSE_ON_SELECTED_TRAIT 1
NO_MEASURED_CONSUMER_COMPONENTS                 1
NO_FOCAL_POLLINATOR_ANTAGONIST_TRAIT_ESTIMAND  1
NO_COMMON_REPRODUCTIVE_OUTCOME                  1
NO_SHARED_TRAIT_COORDINATE                      2
NO_COMMON_FITNESS_SELECTION_ESTIMAND            1
~~~

## Interpretation

The queue did what it was intended to do: it found papers whose titles and title/abstract notes strongly suggested selection, fitness or repeated ecological context.

The source audit then showed that those signals are not equivalent to a commensurate SCH estimand.

This directly supports the identification principle:

~~~text
selection / fitness language
!=
same-trait repeated consumer-mediated selection estimand
~~~

## No post-hoc retuning

The FT0/FT1/FT2 rules remain frozen.

They are not changed merely because the first eight records produced zero TOTAL_SELECTION_EFFECT promotions.

Changing the rule after observing the yield would create outcome-informed search behavior.

Instead, the next 21 V20 full-text-pending records are adjudicated under the same formal screening rules, while the macroecology expansion to the remaining frozen cohort proceeds prospectively.

## Formal screening boundary

This estimand-recovery audit is not itself a PRISMA inclusion/exclusion overlay.

A record can be:

~~~text
useful for H4 / ecological context / programme interpretation
but
not useful for TOTAL_SELECTION_EFFECT pooling
~~~

Formal full-text screening and macro estimand promotion remain separate decisions.

## Current implication for H2

The broad H2 layer can reach high apparent breadth while the commensurate selection family remains narrow.

The next empirical target is therefore not “more interesting multifunctionality papers.”

It is:

> independent biological clusters that repeatedly estimate the same plant-trait selection or final-performance quantity across ecological contexts.

~~~text
BATCH1_AUDITED = 8
TOTAL_SELECTION_EFFECT_PROMOTIONS = 0
PRIORITY_RULE_RETUNED = NO
FORMAL_PRISMA_DECISIONS_CHANGED_BY_THIS_AUDIT = NO
~~~
