# SCH Ficus composite history-bridge audit v1

## Decision

The fig–fig-wasp literature is the strongest **composite near-L4 system located so far**, but it does not close the direct historical gate.

Across separate primary studies, *Ficus* supplies four pieces that had previously been distributed across unrelated systems:

1. **phylogenetic scent divergence** — Cao et al. (2026; doi:10.1111/nph.71133) measured receptive-fig VOCs in 32 *Ficus* species and recovered strong phylogenetic signal in scent composition;
2. **an extant private pollinator channel** — Chen et al. (2009; doi:10.1111/j.1365-2435.2009.01622.x) showed that 4-methylanisole dominates receptive *F. semicordata* scent and is sufficient for attraction of its specific pollinator;
3. **shared-cue exploitation by a non-pollinating antagonist/exploiter** — Proffit et al. (2009; doi:10.1111/j.1570-7458.2009.00823.x) showed that both the pollinator and a non-pollinating parasitic fig wasp were attracted to the specific receptive odour of *F. hispida*;
4. **developmental signal switching and receiver differentiation** — Long et al. (2026; doi:10.1016/j.ijbiomac.2026.152992) linked receptive-stage attractant synthases, post-pollination repellent synthases, pollinator behaviour, and differential odorant-binding properties of pollinating and non-pollinating fig wasps.

The original machine-readable decomposition is `empirical/one_trait_shared_cue/FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv`. The candidate radiation has now also been expanded into the fixed 32-species matrix `empirical/one_trait_shared_cue/FICUS_32_SPECIES_L4_CANDIDATE_MATRIX_V1.csv`.

## Why this is scientifically useful

The prior SCH history audit could say that the required pieces existed separately. *Ficus* improves that result because those pieces occur **within one biological radiation and chemical-communication system**. The 32-species matrix now shows exactly where those pieces overlap rather than leaving the next analysis as a generic proposal.

```text
Ficus evidence now contains:
phylogeny + scent divergence across 32 species
        + extant pollinator-private cue in F. semicordata
        + contemporary pollinator/exploiter shared tracking in F. hispida
        + additional NPFW scent response in F. racemosa
        + developmental attraction-to-repellence / receiver mechanisms
```

This makes *Ficus* a high-value candidate system for a direct historical test rather than merely another analogy.

## Why it is still not L4

A direct `shared cue -> private cue` transition under dual-audience selection still requires all five historical gates in one linked comparative analysis.

| Gate | Ficus composite status | Reason |
|---|---|---|
| ancestral shared state | **UNRESOLVED** | the 32-species phylogenetic study detects phylogenetic signal but does not reconstruct a shared ancestral cue state followed by private-channel transitions |
| descendant private architecture | **POSITIVE EXTANT SINGLETON** | *F. semicordata* has a directly demonstrated private pollinator-attraction compound, but no second private-channel species is yet directly coded |
| pollinator channel | **POSITIVE** | multiple studies directly measure pollinator olfactory responses |
| antagonist/exploiter channel | **POSITIVE CONTEMPORARY, SPARSE** | non-pollinating wasps use receptive odours in matched species, and molecular work includes non-pollinating wasp OBPs |
| replicated transition + alternatives | **UNRESOLVED / NOT YET EVALUABLE** | a single directly supported private-channel tip cannot establish repeated transitions; no study maps private/shared cue states and both receiver channels onto the same phylogeny with alternative-history tests |

Accordingly the composite classification is:

```text
COMPOSITE_NEAR_L4
not DIRECT_L4
```

The absence of the final link must not be hidden by combining studies post hoc. Cross-study biological coherence identifies a candidate system; it does not create a historical causal estimate.

## Strongest bounded SCH statement after the species-level matrix

> The ingredients needed for historical cue privatization are not merely scattered across unrelated taxa. In a fixed 32-species *Ficus* scent scaffold, a directly demonstrated private pollinator channel, direct shared pollinator–non-pollinator scent tracking, and developmental chemical gating all occur within the same radiation. However, the direct private-channel state is presently represented by only one coded species. The literature therefore does not yet permit a replicated ancestral shared-cue to private-cue transition test under both mutualist and exploiter selection.

## Next decisive analysis

The species matrix is now built, so the next pass is **not** to construct another scaffold or broaden the search universe. The next gate is a fixed-universe evidence expansion across the other 31 Cao et al. species.

The search should first recover a second directly demonstrated private pollinator channel: a receptive VOC or compact bouquet with behavioural evidence of pollinator specificity/sufficiency. A second private-channel tip is necessary but not sufficient for a replicated-transition analysis. For every such candidate, species-matched non-pollinating wasp/exploiter response to the same cue must then be coded.

Only after at least two private-channel tips and adequate shared/dual-audience comparators exist should states be reconstructed on the same phylogeny and tested against section, reproductive system, phylogenetic and abiotic/geographic alternatives. If the fixed 32-species screen produces no second private-channel tip, strict repeated L4 remains `NOT_EVALUABLE` and *Ficus* should remain the best `COMPOSITE_NEAR_L4` system rather than being over-promoted.

The numerical bottleneck and search stopping rule are recorded in `docs/SCH_FICUS_32_SPECIES_L4_MATRIX_READOUT_V1.md`.
