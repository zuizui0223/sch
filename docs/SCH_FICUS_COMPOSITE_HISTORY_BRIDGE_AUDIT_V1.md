# SCH Ficus composite history-bridge audit v1

## Decision

The fig–fig-wasp literature is the strongest **composite near-L4 system located so far**, but it does not close the direct historical gate.

Across separate primary studies, *Ficus* supplies pieces that had previously been distributed across unrelated systems:

1. **phylogenetic scent divergence** — Cao et al. (2026; doi:10.1111/nph.71133) measured receptive-fig VOCs in 32 *Ficus* species and recovered strong phylogenetic signal in scent composition;
2. **a resolved single-compound private pollinator channel** — Chen et al. (2009; doi:10.1111/j.1365-2435.2009.01622.x) showed that 4-methylanisole dominates receptive *F. semicordata* scent and is sufficient for attraction of its specific pollinator;
3. **an independently resolved ratio-specific pollinator code** — Proffit et al. (2020; doi:10.1038/s41598-020-66655-w) showed that *F. carica* pollinators are attracted by a particular four-VOC blend and lose attraction when its proportions are perturbed;
4. **shared-cue exploitation by a non-pollinating antagonist/exploiter** — Proffit et al. (2009; doi:10.1111/j.1570-7458.2009.00823.x) showed that both the pollinator and a non-pollinating parasitic fig wasp were attracted to the specific receptive odour of *F. hispida*;
5. **direct temporal receiver separation in a private-code host** — Yan, Peng & Yang (2012; doi:10.1016/j.chnaes.2012.02.003) directly observed *F. semicordata* NPFW oviposition after the pollinator, including *Platyneura cunia* at about 10 days and *Sycoscapter trifemmensis* at 14–32 days after pollinator entry;
6. **developmental signal switching and receiver differentiation** — Long et al. (2026; doi:10.1016/j.ijbiomac.2026.152992) linked receptive-stage attractant synthases, post-pollination repellent synthases, pollinator behaviour, and differential odorant-binding properties of pollinating and non-pollinating fig wasps.

Recent *F. hispida* work (Liang et al. 2026; doi:10.1007/s10886-026-01745-z) additionally supports species-specific pollinator recognition through VOC blends, while the key attractive synthetic code remains less resolved than in *F. semicordata* or *F. carica*.

The original machine-readable decomposition is `empirical/one_trait_shared_cue/FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv`. The candidate radiation is expanded into the fixed 32-species matrix `empirical/one_trait_shared_cue/FICUS_32_SPECIES_L4_CANDIDATE_MATRIX_V1.csv`. The matched receiver-gap extension is `empirical/one_trait_shared_cue/FICUS_SAME_CODE_RECEIVER_GAP_V1.csv`.

## Why this is scientifically useful

The prior SCH history audit could say that the required pieces existed separately. *Ficus* improves that result because those pieces occur **within one biological radiation and chemical-communication system**. The fixed matrix now distinguishes pollinator-code resolution, temporal receiver separation and dual-audience chemical interception rather than treating all three as interchangeable evidence.

```text
Ficus evidence now contains:
phylogeny + scent divergence across 32 species
        + single-compound pollinator code in F. semicordata
        + ratio-specific pollinator code in F. carica
        + direct temporal separation of pollinator and NPFW use in F. semicordata
        + pollinator/exploiter shared tracking in F. hispida
        + leaky/shared pollinator filtering in F. auriculata
        + developmental attraction-to-repellence / receiver mechanisms
```

This makes *Ficus* a high-value candidate system for a direct historical test rather than merely another analogy.

## Why it is still not L4

A direct `shared cue -> private cue` transition under dual-audience selection still requires all five historical gates in one linked comparative analysis.

| Gate | Ficus composite status | Reason |
|---|---|---|
| ancestral shared state | **UNRESOLVED** | the 32-species phylogenetic study detects phylogenetic signal but does not reconstruct shared chemical-code states followed by receiver-specific transitions |
| descendant receiver-specific architecture | **POSITIVE POLLINATOR SIDE** | *F. semicordata* has a single-compound code and *F. carica* a directly resolved ratio-specific code; only *F. semicordata* satisfies the narrow published `private channel` label |
| pollinator channel | **POSITIVE** | multiple studies directly measure behavioural/electrophysiological pollinator responses |
| antagonist/exploiter channel | **POSITIVE CONTEMPORARY AND TEMPORALLY RESOLVED IN PART, BUT NOT ON A RESOLVED POLLINATOR CODE** | NPFWs use receptive odours in *F. hispida* and other species, and NPFW timing is directly resolved in *F. semicordata*; however no coded species combines a resolved attractive pollinator code with direct behavioural response of the exploiter to that same code |
| replicated transition + alternatives | **UNRESOLVED / NOT YET EVALUABLE** | the same-code dual-audience state is absent, so private/shared states cannot yet be reconstructed on a biologically matched coordinate and tested as repeated transitions |

Accordingly the composite classification remains:

```text
COMPOSITE_NEAR_L4
not DIRECT_L4
```

The absence of the final link must not be hidden by combining studies post hoc. Pollinator-code resolution, temporal separation and antagonist tracking are three distinct estimands. None may be substituted for another to manufacture a historical cue-privatization result.

## Strongest bounded SCH statement after the fixed-universe pass

> A fixed 32-species *Ficus* scent scaffold contains two directly resolved pollinator recognition architectures, direct shared pollinator–non-pollinator scent tracking, a leaky/shared chemical-filter comparator, developmental receiver mechanisms, and direct temporal separation of pollinator and non-pollinator oviposition in the private-code *F. semicordata* system. The missing intersection is now precise: no coded species combines a resolved pollinator-attractive chemical code with direct non-pollinating-wasp response to that same code and a reconstructed historical transition. Thus the literature contains several components of cue privatization within one radiation but not the matched state needed to test repeated shared-to-private evolution under dual-audience selection.

## Next decisive analysis

The species matrix is built, the second resolved pollinator-code architecture has been recovered, and one private-code host now has direct temporal receiver separation. The next pass is therefore **not** another broad search and no longer “find a second private-channel species.” It should close the same-code dual-audience cells directly:

1. test or recover non-pollinating-wasp behaviour to 4-methylanisole in *F. semicordata*, while preserving the natural post-pollination windows now documented for its NPFWs;
2. test or recover *Philotrypesis caricae* and other exploiter behaviour to the validated four-VOC ratio code in *F. carica*;
3. resolve the attractive synthetic code in *F. hispida* and test its known non-pollinating *Philotrypesis* against that same code;
4. retain *F. auriculata* as a leaky/shared comparator rather than relabelling shared semiochemicals as a private channel.

Only after matched chemical coordinates exist on both receiver sides should states be reconstructed on the same phylogeny and tested against section, reproductive system, phylogenetic and abiotic/geographic alternatives. If the same-code intersection remains empty, strict repeated L4 remains `NOT_EVALUABLE` and *Ficus* should remain the best `COMPOSITE_NEAR_L4` system rather than being over-promoted.

The numerical bottleneck and stopping rule are recorded in `docs/SCH_FICUS_32_SPECIES_L4_MATRIX_READOUT_V1.md`; the three matched receiver gaps are recorded in `docs/SCH_FICUS_SAME_CODE_RECEIVER_GAP_READOUT_V1.md`.
