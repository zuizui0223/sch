# SCH JBI geography preview readout v1

## Question

Does the source-adjudicated evidence contain a nontrivial geographic or receiver-regime axis capable of supporting the first-choice **Journal of Biogeography** route?

This document preserves two stages separately:

1. the original eight-anchor preview, before systematic full-text expansion;
2. the current frozen-PRISMA systematic coding state after completing Batch 1 and advancing the Batch-2 high-information records through title/abstract and complete high-information full-text adjudication.

Neither stage alone closes JBI Gate J5.

## Historical anchor-only preview

The original diagnostic was:

```text
prior source-adjudicated anchors:                 8
clear direct geographic/interactor-regime case:   1
clear no-direct-geography / synthesis cases:       7
JBI geography gate:                                UNRESOLVED / EMPIRICALLY_SPARSE_IN_ANCHOR_SPINE
```

The one clear case was **Knauer, Bakhtiari & Schiestl 2018** (`10.1038/s41467-018-03792-x`). The source compares populations where crab spiders are present versus absent and reports stronger induced beta-ocimene emission in spider-associated populations, consistent with local adaptation.

Do **not** conclude from `1/8` that relevant biogeographic evidence is rare in the literature. Those eight records were an inherited high-information anchor set, not a systematic geography sample.

## Frozen systematic denominator

The first complete V2 identification cohort is frozen at **868 records**. Live OpenAlex changes are monitored separately and cannot change that denominator or record IDs.

The initial complete run was:

```text
10,953 OpenAlex records
2,107 concept-pass query hits
868 deduplicated candidates
0 truncated queries
```

A later live run returned 869 candidates. Batch-2 triage also found one record whose current live abstract no longer reproduced the original three-concept match. Both are index-drift observations, not amendments to the frozen cohort.

## Current systematic state

Batch 1 (`SCHPRISMA-000001`–`000100`) and Batch 2 (`SCHPRISMA-000101`–`000200`) are now completely title/abstract screened. V12 adjudicates the 70 Batch-2 records that were genuinely undecided after accounting for the prior V1 decision on `SCHPRISMA-000172`: 35 are retained for full text and 35 excluded.

Cumulative state:

```text
frozen candidates:                     868
title/abstract screened:               208
retained for full text:                130
title/abstract excluded:                78
unscreened:                            660

primary full-text inclusions:           44
full-text exclusions:                   51
full-text undecided among retained:     35

STRICT_LINKED_EXPERIMENT:                2
DIRECTIONAL_OR_NEAR_PASS:               38
EVOLUTIONARY_OUTCOME:                   12
```

The Batch-2 high-information full-text queue remains closed, and V12 completes the remainder of Batch-2 title/abstract screening. Because the 35 newly retained reports have not yet been full-text coded, included-study and evidence-lane counts remain at 44 / 2 strict / 38 near / 12 evolutionary, and geography counters remain 8/9/8.

## Geography counters

The current audit explicitly separates spatial and receiver-regime evidence:

```text
positive geographic contrast:             8
positive receiver/interactor contrast:     9
joint geographic + receiver contrast:      8
```

The joint counter is the JBI-relevant object: both a real geographic contrast and a real receiver/interactor-regime contrast must occur in the same included record.

The eight current joint-positive systems are:

```text
SCHPRISMA-000008  Erysimum mediohispanicum
                   eight-population pollinator / ungulate / selection mosaic

SCHPRISMA-000032  Barbarea vulgaris
                   14-site agricultural-landscape herbivory -> floral display -> pollination pathway

SCHPRISMA-000066  Primula secundiflora
                   six-population nectar-robber / syrphid visitor mosaic

SCHPRISMA-000067  Trollius europaeus
                   Chiastocheta-present versus absent/extinct nursery-pollination populations

SCHPRISMA-000074  coffee agroecosystem dissertation
                   coffee-field versus forest-fragment nectar-robbing context

SCHPRISMA-000172  Biscutella laevigata
                   lowland/highland crab-spider regime and beta-ocimene inducibility

SCHPRISMA-000523  Primula farinosa
                   69-population pollinator/grazer selection mosaic plus microevolutionary change

SCHPRISMA-000710  Gentiana lutea
                   12-population flower-colour / pollinator-community / selection gradient
```

`SCHPRISMA-000075` supplies a real bee-versus-aphid selection-regime contrast in an eight-generation experiment but is deliberately **not geographic**. Likewise, sampling many locations does not itself satisfy JBI: the 25-orchard ant study is coded negative because its focal comparison is flower architecture and ant visitor role, not geographic turnover in receiver assemblages.

## What the current geographic systems establish

The systematic screen supports a positive existence statement: replicated spatial interaction mosaics occur across multiple independent plant–consumer systems, and those mosaics can covary with floral phenotype, interaction outcome, or evolutionary response.

The evidence does **not** yet identify one common quantitative path such as:

```text
geography
-> receiver turnover
-> cue overlap
-> net selection / evolutionary outcome
```

Important boundaries remain:

- several systems use observational trait variation rather than randomized `do(A)`;
- *Barbarea* primarily identifies landscape effects through herbivory-mediated floral display rather than full receiver-community replacement;
- *Trollius* documents partner loss and changed nursery-pollination economics, but floral architecture is not experimentally randomized;
- the coffee dissertation overlaps a published chapter and must be clustered before quantitative synthesis;
- *Primula farinosa* supplies strong microevolutionary evidence on existing morph frequencies, not origin of a private cue;
- *Biscutella* supports conditional gating and population differentiation, not ancestral shared-to-private reconstruction;
- **lineage branching remains untested**;
- strict linked measurement architecture is now replicated in Theis & Adler 2012 and Sánchez-Lafuente 2007, but neither study demonstrates simultaneous positive pollinator and antagonist responses to the same manipulated `A`.

## Batch-2 high-information geography closure

The previously provisional 16-report full-text queue has been adjudicated. Several records add useful receiver-overlap or multisite context, but none is promoted into the joint-positive geography counter without explicit source-coded geographic and receiver-regime fields. The positive geography / receiver / joint counts therefore remain 8 / 9 / 8. This prevents multisite sampling or a network label from being mistaken for demonstrated geographic receiver turnover.

## High-information non-geographic boundary cases

Two cases make the strict gate especially clear:

- **Reisenman et al. 2010, *Datura*–*Manduca*** directly manipulates synthetic floral scent/linalool and measures both adult feeding and female oviposition on the same chemical coordinate. No plant reproductive outcome is supplied, so it remains near-pass.
- **Disa similis 2025** manipulates the yellow anther-mimic visual signal and measures pollination/fruit set. The same pollen-feeding beetle also florivores the signal-bearing petal apices, but florivory is not independently measured as a response to `do(A)`. It therefore remains near-pass rather than a second strict experiment.

The Batch-2 high-information full-text queue is now closed. The strict count is two, but both are measurement-architecture passes with complementary nulls rather than a closed positive dual-audience conflict chain.

## Current JBI decision

```text
JBI conceptual fit:                    YES
frozen systematic denominator:         CLOSED at 868
Batch 1 title/abstract screening:       COMPLETE
Batch 2 title/abstract screening:       COMPLETE (100/100)
Batch 2 high-information FT decisions:  26/26 retained reports
current retained full-text backlog:     35
multiple joint geographic systems:     YES (8 currently coded)
full title/abstract screening:          NO (660 remaining)
independence / duplicate coding:        ACTIVE
cross-study scale compatibility:        NOT_EVALUATED
JBI Gate J5:                            UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE
```

The change from historical `1/8` to eight joint-positive systematic records means the geography axis is worth developing. It is **not** permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks.

A map of study locations cannot rescue a failed geography gate.

## Next systematic priority

The next work object is **full-text adjudication of the 35 newly retained Batch-2 reports**. Once that queue closes, title/abstract screening advances to Batch 3.

The same rules continue:

1. uncertainty at title/abstract stage resolves toward full-text retention;
2. machine triage orders review but never writes the formal decision;
3. reviews, dissertations, preprints, datasets and duplicate reports remain visible until the appropriate protocol stage decides their role;
4. geography is a prioritization/coding field, not an inclusion requirement;
5. candidate historical/phylogeographic records are retained when they could move L3/L4 even if they fail the strict contemporary experiment gate;
6. **No pooled effect is authorized** before outcome scale, independence and commensurability pass separate gates.

## Fallback remains live

If completed screening yields a strong shared-cue/evolutionary synthesis but the geographic contrasts are too heterogeneous or too indirect for a defensible biogeographic analysis, the manuscript should move first submission to **Ecology and Evolution** rather than force a decorative geography story.
