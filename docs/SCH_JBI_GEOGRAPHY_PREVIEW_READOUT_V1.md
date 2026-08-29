# SCH JBI geography preview readout v1

## Question

Does the source-adjudicated evidence contain a nontrivial geographic or receiver-regime axis capable of supporting the first-choice **Journal of Biogeography** route?

This document now preserves two stages separately:

1. the original eight-anchor preview, before systematic full-text expansion;
2. the current frozen-PRISMA systematic coding state.

Neither stage alone closes JBI Gate J5.

## Historical anchor-only preview

The original diagnostic was:

```text
prior source-adjudicated anchors:                 8
clear direct geographic/interactor-regime case:   1
clear no-direct-geography / synthesis cases:       7
JBI geography gate:                                UNRESOLVED / EMPIRICALLY_SPARSE_IN_ANCHOR_SPINE
```

The one clear case was **Knauer, Bakhtiari & Schiestl 2018** (`10.1038/s41467-018-03792-x`). The source compares plant populations where crab spiders are present versus absent and reports stronger induced beta-ocimene emission after florivore infestation in spider-associated populations, interpreted as evidence consistent with local adaptation.

The other seven anchors were single systems, common-field taxon comparisons, non-spatial experimental contrasts, antagonist-only cue discrimination, or cross-study syntheses. Thus the early `1/8` result correctly warned that the inherited anchor spine alone could not justify JBI.

Do **not** conclude from `1/8` that relevant biogeographic evidence is rare in the literature. The eight studies were an inherited high-information/source-adjudicated anchor set, not a systematic geography sample.

## Current systematic state

The first complete V2 identification cohort is frozen at **868 records**. Live OpenAlex index changes are monitored separately and cannot change that denominator.

Current cumulative screening/full-text state:

```text
frozen candidates:                    868
title/abstract screened:               43
retained for full text:                31
primary full-text inclusions:          15
full-text exclusions:                   3
full-text undecided among retained:    13

positive geographic contrast:           6
positive receiver/interactor contrast:   6
STRICT_LINKED_EXPERIMENT:                1
```

The six currently included positive geographic/interactor records are:

```text
SCHPRISMA-000008  Erysimum mediohispanicum
                   eight-population pollinator / ungulate / selection mosaic

SCHPRISMA-000032  Barbarea vulgaris
                   14-site agricultural-landscape herbivory -> floral display -> pollination pathway

SCHPRISMA-000066  Primula secundiflora
                   six-population nectar-robber / syrphid / morph-specific pollination mosaic

SCHPRISMA-000172  Biscutella laevigata
                   lowland/highland crab-spider regime and beta-ocimene inducibility

SCHPRISMA-000523  Primula farinosa
                   69-population pollinator/grazer selection mosaic plus microevolutionary frequency change

SCHPRISMA-000710  Gentiana lutea
                   12-population flower-colour / pollinator-community / selection gradient
```

This changes the journal-fit diagnosis materially: geography is no longer supported by only one isolated anchor. Replicated spatial interaction mosaics recur across several independent systems.

## What the six cases do and do not establish

They support the existence of analyzable spatial turnover in biotic audiences, interaction intensity, selection, or phenotype–selection relationships. They do **not** yet establish one common quantitative `geography -> cue overlap -> evolutionary outcome` effect.

Important boundaries remain:

- *Erysimum*, *Primula secundiflora* and *Gentiana* use observational trait variation rather than randomized `do(A)`;
- the *Barbarea* landscape pathway includes herbivory-mediated changes in floral display, while pollinator-community composition itself was not the main landscape-responsive object;
- *Primula farinosa* provides unusually strong field-manipulation/microevolution evidence, but it concerns frequencies of existing display morphs rather than origin of a private cue;
- *Biscutella* supports conditional gating and population differentiation, not ancestral shared-to-private reconstruction;
- none of these additions changes the strict linked-experiment count, which remains Theis & Adler 2012 only;
- **lineage branching remains untested** in the current systematic state.

## Current JBI decision

```text
JBI conceptual fit:                    YES
frozen systematic denominator:         CLOSED at 868
multiple geographic systems recovered: YES (6 currently coded)
title/abstract screening complete:     NO
full-text screening complete:          NO
independence / duplicate coding:        INCOMPLETE
cross-study scale compatibility:        NOT_EVALUATED
JBI Gate J5:                            UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE
```

The change from `1/8` to six positive systematic records is evidence that the geography axis is worth continuing rather than abandoning. It is not permission to declare JBI ready before screening and analysis are complete.

A map of study locations cannot rescue a failed geography gate. The required object is replicated spatial change in interaction regimes that is analytically related to cue overlap, conflict, or cue architecture.

## Next systematic priority

The next high-value step is not more broad discovery. It is to finish full-text adjudication of the remaining retained reports and then complete title/abstract screening within the frozen 868 cohort.

At full text, prioritize:

1. duplicate preprint/published pairs so independence is not inflated;
2. studies that may add another strict four-field linked experiment;
3. replicated populations/sites with explicit pollinator-versus-antagonist turnover;
4. evolutionary outcomes tied to those spatial contrasts;
5. explicit historical/phylogeographic cases capable of moving L3/L4 rather than merely adding locations.

Only after these are coded should a geography-by-cue-overlap synthesis be defined. **No pooled effect is authorized** before outcome scale, independence, and commensurability pass their separate gates.

## Fallback remains live

If completed screening yields rich shared-cue/evolutionary evidence but the geographic contrasts are too heterogeneous or too indirect for a defensible biogeographic analysis, the manuscript should retain the synthesis and move first submission to **Ecology and Evolution** rather than force a decorative geography story.
