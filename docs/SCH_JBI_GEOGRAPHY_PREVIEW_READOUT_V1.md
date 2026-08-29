# SCH JBI geography preview readout v1

## Question

Does the source-adjudicated evidence contain a nontrivial geographic or receiver-regime axis capable of supporting the first-choice **Journal of Biogeography** route?

This document preserves two stages separately:

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
primary full-text inclusions:          22
full-text exclusions:                   9
full-text undecided among retained:     0

positive geographic contrast:           6
positive receiver/interactor contrast:   6
STRICT_LINKED_EXPERIMENT:                1
DIRECTIONAL_OR_NEAR_PASS:               20
EVOLUTIONARY_OUTCOME:                    6
```

Thus all reports retained so far have already received a protocol-valid full-text decision. The active screening bottleneck is now the remaining **825 title/abstract records**, not a backlog of retained reports.

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

The full-text expansion also recovered a high-information non-geographic boundary case: Reisenman et al. 2010 directly manipulates a synthetic *Datura* floral-scent coordinate and measures both *Manduca* feeding and oviposition. The missing common plant reproductive outcome keeps it a near-pass rather than a second strict linked experiment.

## Current JBI decision

```text
JBI conceptual fit:                    YES
frozen systematic denominator:         CLOSED at 868
multiple geographic systems recovered: YES (6 currently coded)
title/abstract screening complete:     NO
current retained full-text backlog:    CLOSED (0 undecided)
independence / duplicate coding:        ACTIVE; known preprint pairs resolved
cross-study scale compatibility:        NOT_EVALUATED
JBI Gate J5:                            UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE
```

The change from `1/8` to six positive systematic records is evidence that the geography axis is worth continuing rather than abandoning. It is not permission to declare JBI ready before screening and analysis are complete.

A map of study locations cannot rescue a failed geography gate. The required object is replicated spatial change in interaction regimes that is analytically related to cue overlap, conflict, or cue architecture.

## Next systematic priority

The next high-value step is now **title/abstract screening of the frozen cohort**, because every report retained so far has a full-text decision.

Prioritize the remaining Batch-1 records first, then subsequent batches using the same fail-closed rules. At title/abstract stage:

1. uncertainty resolves toward full-text retention;
2. machine triage orders review but never writes the decision;
3. explicit review/meta-analysis and duplicate objects remain visible until their protocol stage is decided;
4. geography is a prioritization/coding feature, not an inclusion requirement;
5. candidate historical/phylogeographic records are retained when they could move L3/L4 even if they do not satisfy the strict contemporary experiment gate.

Only after systematic title/abstract screening is substantially advanced should a geography-by-cue-overlap synthesis be defined. **No pooled effect is authorized** before outcome scale, independence, and commensurability pass their separate gates.

## Fallback remains live

If completed screening yields rich shared-cue/evolutionary evidence but the geographic contrasts are too heterogeneous or too indirect for a defensible biogeographic analysis, the manuscript should retain the synthesis and move first submission to **Ecology and Evolution** rather than force a decorative geography story.
