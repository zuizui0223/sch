# SCH PRISMA V21 — H2 estimand-priority TA0 title/abstract screen

## Purpose

V21 screens the first frozen priority tier from the 463-record title/abstract-unscreened cohort.

The priority queue was frozen before adjudication and used only:

- bibliographic title;
- frozen registered query metadata.

It did not use result sign, statistical significance, conflict/alignment outcome or later full-text knowledge.

## V21 batch

~~~text
TA0 records screened          32

RETAIN_FULLTEXT               20
EXCLUDE                       12
~~~

Exclusion reasons:

~~~text
TA_NO_ANTAGONIST_COMPONENT             5
TA_NO_POLLINATOR_COMPONENT             3
TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS   3
TA_NOT_FLORAL_SIGNAL                   1
~~~

No record was excluded because its result was null, aligned, one-sided or contrary to an SCH expectation.

## Current PRISMA state

After V21:

~~~text
frozen denominator             868

title/abstract screened        437
retained for full text         297
title/abstract excluded        140
title/abstract unscreened      431

full-text included primary     117
full-text decision excluded    131
full-text pending               49
~~~

The 117-study primary inclusion set is unchanged.

V21 advances only the title/abstract layer.

## Examples of retained designs

### Strong direct candidates

Retained records include primary studies explicitly measuring floral traits with both focal interaction routes, for example:

- *Helianthus grosseserratus* floral-head traits, insect pollinators, seed predators and seed production;
- *Protea* inflorescence colour, pollinators and seed predators;
- *Lobelia cardinalis* pollinator- versus herbivore-mediated selection;
- *Brassica rapa* pollinator/herbivore selection on floral signals;
- *Silene* recombinant floral traits with pollinator visitation, seed set and *Hadena* predation.

### Null or weak antagonist designs retained

V21 also retains studies where the antagonist route may be weak or null.

Examples include:

- *Trillium discolor*, where antagonist damage did not detectably alter floral-trait selection;
- *Dactylorhiza lapponica*, where fruit herbivory was measured but had only minor influence on pollinator-mediated selection.

These are retained because the design is relevant.

The result sign is not an admission criterion.

## Examples of exclusions

### No measured antagonist component

Records were excluded when antagonists were discussed only as possible explanations or future work.

Examples:

- pollinator-mediated selection in *Linum pubescens*;
- two *Penstemon digitalis* selection studies;
- *Hesperis matronalis* floral-scent dissertation where herbivore attraction is proposed as a possible cost rather than a measured antagonist-selection component;
- water-deficit × pollinator-access experiment in *Ipomoea purpurea*, where the second selective agent is abiotic drought.

### No measured pollinator component

The *Claytonia virginica* colour study focuses on herbivores and pathogens.

The volatile-enzyme molecular-selection study does not measure a focal plant-pollinator component.

### Not primary

A floral-selection review chapter and the New Phytologist scent Commentary are excluded as non-primary records.

### Not a plant floral coordinate

The flower-dwelling spider study focuses on predator prey choice rather than selection on a plant floral signal.

## Next estimand-recovery frontier

The immediate full-text frontier is now:

~~~text
20 V21 TA0 retained records
~~~

These records remain only candidates.

Full text must still establish:

1. primary empirical design;
2. declared focal floral coordinate;
3. pollinator component;
4. antagonist/exploiter component;
5. common reproductive/fitness endpoint;
6. repeated local context if H2 is claimed;
7. estimand family.

The preferred H2 promotion remains:

`TOTAL_SELECTION_EFFECT`

because the broad H2 breadth gate already passes but the commensurate TOTAL_SELECTION family spans only three independent biological clusters.

## Status

~~~text
V21_TA0_SCREEN = COMPLETE
TA0_RETAIN = 20
TA0_EXCLUDE = 12

TITLE_ABSTRACT_SCREENED = 437
TITLE_ABSTRACT_UNSCREENED = 431

PRIMARY_FULLTEXT_INCLUDED = 117
NEXT_FULLTEXT_RECOVERY = 20 V21 TA0 RECORDS
~~~
