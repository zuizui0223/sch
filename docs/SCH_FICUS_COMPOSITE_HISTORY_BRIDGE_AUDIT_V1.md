# SCH Ficus composite history-bridge audit v1

## Decision

The fig–fig-wasp literature is the strongest **composite near-L4 system located so far**, but it does not close the direct historical gate.

Across separate primary studies, *Ficus* supplies four pieces that had previously been distributed across unrelated systems:

1. **phylogenetic scent divergence** — Cao et al. (2026; doi:10.1111/nph.71133) measured receptive-fig VOCs in 32 *Ficus* species and recovered strong phylogenetic signal in scent composition;
2. **an extant private pollinator channel** — Chen et al. (2009; doi:10.1111/j.1365-2435.2009.01622.x) showed that 4-methylanisole dominates receptive *F. semicordata* scent and is sufficient for attraction of its specific pollinator;
3. **shared-cue exploitation by a non-pollinating antagonist/exploiter** — Proffit et al. (2009; doi:10.1111/j.1570-7458.2009.00823.x) showed that both the pollinator and a non-pollinating parasitic fig wasp were attracted to the specific receptive odour of *F. hispida*;
4. **developmental signal switching and receiver differentiation** — Long et al. (2026; doi:10.1016/j.ijbiomac.2026.152992) linked receptive-stage attractant synthases, post-pollination repellent synthases, pollinator behaviour, and differential odorant-binding properties of pollinating and non-pollinating fig wasps.

The machine-readable decomposition is `empirical/one_trait_shared_cue/FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv`.

## Why this is scientifically useful

The prior SCH history audit could say that the required pieces existed separately. *Ficus* improves that result because those pieces now occur **within one biological radiation and chemical-communication system**. It therefore sharply narrows the missing intersection.

```text
Ficus evidence now contains:
phylogeny + scent divergence
        + extant pollinator-private cue
        + contemporary pollinator/exploiter shared tracking
        + developmental attraction-to-repellence switching
```

This makes *Ficus* a high-value candidate system for a direct historical test rather than merely another analogy.

## Why it is still not L4

A direct `shared cue -> private cue` transition under dual-audience selection still requires all five historical gates in one linked comparative analysis.

| Gate | Ficus composite status | Reason |
|---|---|---|
| ancestral shared state | **UNRESOLVED** | the 32-species phylogenetic study detects phylogenetic signal but does not reconstruct a shared ancestral cue state followed by private-channel transitions |
| descendant private architecture | **POSITIVE EXTANT CASE** | *F. semicordata* has a directly demonstrated private pollinator-attraction compound |
| pollinator channel | **POSITIVE** | multiple studies directly measure pollinator olfactory responses |
| antagonist/exploiter channel | **POSITIVE CONTEMPORARY** | a non-pollinating parasitic wasp can use the same receptive-fig odour; molecular work also includes non-pollinating wasp OBPs |
| replicated transition + alternatives | **UNRESOLVED** | no study maps private/shared cue states and both receiver channels onto the same phylogeny and tests repeated transitions against phylogenetic/abiotic alternatives |

Accordingly the composite classification is:

```text
COMPOSITE_NEAR_L4
not DIRECT_L4
```

The absence of the final link must not be hidden by combining studies post hoc. Cross-study biological coherence identifies a candidate system; it does not create a historical causal estimate.

## Strongest bounded SCH statement after this audit

> The ingredients needed for historical cue privatization are not merely scattered across unrelated taxa. In *Ficus*, phylogenetic scent divergence, an extant private pollinator channel, exploitation of receptive scent by non-pollinating wasps, and developmental chemical gating all occur within the same radiation. However, no audited study reconstructs repeated transitions from an ancestral shared cue to private descendant cues while jointly modelling pollinator and antagonist/exploiter regimes. *Ficus* is therefore a composite near-L4 system, not a direct L4 result.

## Next decisive analysis

The next SCH literature/data pass should be narrower than another broad search. For *Ficus*, construct a species-level matrix containing:

- a resolved *Ficus* phylogeny;
- receptive scent architecture, including presence/weight of unusual dominant compounds;
- pollinator identity and behavioural response where available;
- non-pollinating wasp/exploiter use of the same VOCs where available;
- developmental gating state;
- abiotic/geographic covariates.

Then test whether reconstructed changes toward more pollinator-specific cue architecture repeatedly coincide with reduced exploiter tracking after conditioning on phylogeny and alternatives. Until that matrix has adequate overlap, the result remains `NOT_EVALUABLE` rather than negative evidence for the evolutionary hypothesis.
