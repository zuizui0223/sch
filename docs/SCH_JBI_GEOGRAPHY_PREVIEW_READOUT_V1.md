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

Batch 1 (`SCHPRISMA-000001`–`000100`) and Batch 2 (`SCHPRISMA-000101`–`000200`) are now completely title/abstract screened. Batch 3 (`SCHPRISMA-000201`–`000300`) is in progress: one record (`000219`) was already adjudicated in V1, 33 high-information records are decided in V14, and 66 genuinely new Batch-3 records remain undecided. V12 adjudicated the 70 genuinely undecided Batch-2 title/abstract records, and V13 now resolves all 35 reports retained by V12. Nine are included, twenty-five are assessed exclusions and one is not retrieved.

Cumulative state:

```text
frozen candidates:                     868
title/abstract screened:               241
retained for full text:                158
title/abstract excluded:                83
unscreened:                            627

primary full-text inclusions:           73
formal full-text exclusions:            85
full-text undecided among retained:      0

STRICT_LINKED_EXPERIMENT:                2
DIRECTIONAL_OR_NEAR_PASS:               64
EVOLUTIONARY_OUTCOME:                   22
HISTORICAL_TRANSITION:                    1
```

Batch 2 remains closed. V15 now also closes the 28 high-information Batch-3 full texts retained by V14: 20 are included and eight excluded. Strict remains 2, while near-pass and evolutionary lanes rise to 64 and 22; one role-transition study enters the historical-transition lane without satisfying L4.

## Geography counters

The current audit explicitly separates spatial and receiver-regime evidence:

```text
positive geographic contrast:            13
positive receiver/interactor contrast:    12
joint geographic + receiver records:      11
```

The joint counter is the JBI-relevant object: both a real geographic contrast and a real receiver/interactor-regime contrast must occur in the same included record.

The eleven current joint-positive records are:

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

SCHPRISMA-000151  Lithophragma bolanderi
                   two-population pollinator-community and local-efficacy divergence

SCHPRISMA-000217  Lithophragma heterophyllum / L. parviflorum
                   Hopland-versus-Hastings floral-visitor assemblage and Greya pollinating-parasite contrast

SCHPRISMA-000167  Primula farinosa
                   overlapping thesis/manuscript selection mosaic; same program as SCHPRISMA-000523

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
- *Lithophragma bolanderi* adds a two-population pollinator-community and local-pollination-efficacy mosaic in a pollinating seed-parasite interaction, but floral traits remain observational;
- the V13 *Primula farinosa* thesis record overlaps the existing PNAS research program and cannot be counted as an independent system;
- **lineage branching remains untested**;
- strict linked measurement architecture is now replicated in Theis & Adler 2012 and Sánchez-Lafuente 2007, but neither study demonstrates simultaneous positive pollinator and antagonist responses to the same manipulated `A`.

## Batch-2 geography update after V13

All currently retained Batch-2 reports are adjudicated. V13 adds explicit geographic/receiver evidence from *Lithophragma bolanderi* and an overlapping *Primula farinosa* thesis/manuscript record. The raw record counters rise to 11 geographic-positive, 11 receiver-positive and 10 joint-positive records. Because the two *Primula farinosa* records belong to one research program, 10 joint records correspond to at most nine obvious independent biological systems before the final independence audit.

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
current retained full-text backlog:      0
multiple joint geographic records:      YES (11 records; independence count not frozen)
full title/abstract screening:          NO (627 remaining)
independence / duplicate coding:        ACTIVE
cross-study scale compatibility:        NOT_EVALUATED
JBI Gate J5:                            UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE
```

The change from historical `1/8` to eleven joint-positive records means the geography axis is worth developing, but overlapping *Primula* and *Lithophragma* research programs must be clustered before any independent-system count is frozen. It is **not** permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks.

A map of study locations cannot rescue a failed geography gate.

## Next systematic priority

The Batch-3 high-information queue is now closed through full text under V15. The next work object is the **remaining 66 genuinely new Batch-3 title/abstract records**. Independence and outcome-scale coding continue in parallel; screening progress alone does not authorize pooling.

The same rules continue:

1. uncertainty at title/abstract stage resolves toward full-text retention;
2. machine triage orders review but never writes the formal decision;
3. reviews, dissertations, preprints, datasets and duplicate reports remain visible until the appropriate protocol stage decides their role;
4. geography is a prioritization/coding field, not an inclusion requirement;
5. candidate historical/phylogeographic records are retained when they could move L3/L4 even if they fail the strict contemporary experiment gate;
6. **No pooled effect is authorized** before outcome scale, independence and commensurability pass separate gates.

## Fallback remains live

If completed screening yields a strong shared-cue/evolutionary synthesis but the geographic contrasts are too heterogeneous or too indirect for a defensible biogeographic analysis, the manuscript should move first submission to **Ecology and Evolution** rather than force a decorative geography story.
