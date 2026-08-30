# SCH JBI geography preview readout v1

## Question

Does the source-adjudicated evidence contain a nontrivial geographic or receiver-regime axis capable of supporting the first-choice **Journal of Biogeography** route?

This document preserves two stages separately:

1. the original eight-anchor preview, before systematic full-text expansion;
2. the current frozen-PRISMA systematic coding state after completing Batch 1.

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

A later live run returned 869 candidates. That is index drift, not an amended PRISMA cohort.

## Current systematic state — Batch 1 complete

Batch 1 (`SCHPRISMA-000001`–`000100`) is completely title/abstract screened. Because nine previously adjudicated records outside Batch 1 also have formal decisions, the cumulative state is:

```text
frozen candidates:                     868
title/abstract screened:               109
retained for full text:                 69
title/abstract excluded:                40
unscreened:                            759

primary full-text inclusions:           35
full-text exclusions:                   34
full-text undecided among retained:      0

STRICT_LINKED_EXPERIMENT:                1
DIRECTIONAL_OR_NEAR_PASS:               30
EVOLUTIONARY_OUTCOME:                   11
```

The active screening bottleneck is therefore the remaining **759 title/abstract records**, not a backlog of retained full texts.

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

`SCHPRISMA-000075` supplies a real bee-versus-aphid selection-regime contrast in an eight-generation experiment but is deliberately **not geographic**. Likewise, sampling many locations does not itself satisfy JBI: the 25-orchard ant study is coded negative for geographic receiver-regime contrast because the focal comparison is flower architecture and ant visitor role, not spatial turnover in receiver assemblages.

## What the current geographic systems establish

The systematic screen now supports a positive existence statement: replicated spatial interaction mosaics occur across multiple independent plant–consumer systems, and those mosaics can covary with floral phenotype, interaction outcome, or evolutionary response.

The evidence does **not** yet identify one common quantitative path such as:

```text
geography
-> receiver turnover
-> cue overlap
-> net selection / evolutionary outcome
```

Important boundaries remain:

- several systems use observational trait variation rather than randomized `do(A)`;
- *Barbarea* primarily identifies landscape effects through herbivory-mediated floral display rather than a full receiver-community replacement;
- *Trollius* documents partner loss and changed nursery-pollination economics, but floral architecture is not experimentally randomized;
- the coffee dissertation overlaps a published chapter and must be clustered before quantitative synthesis;
- *Primula farinosa* supplies strong microevolutionary evidence on existing morph frequencies, not origin of a private cue;
- *Biscutella* supports conditional gating and population differentiation, not ancestral shared-to-private reconstruction;
- **lineage branching remains untested**;
- the strict linked-experiment count remains Theis & Adler 2012 only.

## High-information non-geographic boundary cases

Two cases make the strict gate especially clear:

- **Reisenman et al. 2010, *Datura*–*Manduca*** directly manipulates synthetic floral scent/linalool and measures both adult feeding and female oviposition on the same chemical coordinate. No plant reproductive outcome is supplied, so it remains near-pass.
- **Disa similis 2025** manipulates the yellow anther-mimic visual signal and measures pollination/fruit set. The same pollen-feeding beetle also florivores the signal-bearing petal apices, but florivory is not independently measured as a response to `do(A)`. It therefore remains near-pass rather than a second strict experiment.

These are useful because they show exactly what the strict four-field gate still demands rather than merely reporting a vague literature gap.

## Current JBI decision

```text
JBI conceptual fit:                    YES
frozen systematic denominator:         CLOSED at 868
Batch 1 title/abstract screening:       COMPLETE
current retained full-text backlog:    CLOSED (0 undecided)
multiple joint geographic systems:     YES (8 currently coded)
full title/abstract screening:          NO (759 remaining)
independence / duplicate coding:        ACTIVE
cross-study scale compatibility:        NOT_EVALUATED
JBI Gate J5:                            UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE
```

The change from historical `1/8` to eight joint-positive systematic records means the geography axis is worth developing. It is **not** permission to declare JBI ready before the frozen cohort is screened and an analyzable cross-study geography question passes independence and scale checks.

A map of study locations cannot rescue a failed geography gate.

## Next systematic priority

The next work object is **Batch 2 title/abstract screening**, not more broad discovery and not more Batch-1 full-text recovery.

The same rules continue:

1. uncertainty at title/abstract stage resolves toward full-text retention;
2. machine triage orders review but never writes the formal decision;
3. reviews, dissertations, preprints and duplicate reports remain visible until the appropriate protocol stage decides their role;
4. geography is a prioritization/coding field, not an inclusion requirement;
5. candidate historical/phylogeographic records are retained when they could move L3/L4 even if they fail the strict contemporary experiment gate;
6. **No pooled effect is authorized** before outcome scale, independence and commensurability pass separate gates.

## Fallback remains live

If completed screening yields a strong shared-cue/evolutionary synthesis but the geographic contrasts are too heterogeneous or too indirect for a defensible biogeographic analysis, the manuscript should move first submission to **Ecology and Evolution** rather than force a decorative geography story.
