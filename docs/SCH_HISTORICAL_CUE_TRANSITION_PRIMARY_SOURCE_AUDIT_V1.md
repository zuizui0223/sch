# SCH historical cue-transition primary-source audit v1

## Decision

The unresolved SCH endpoint can now be stated more precisely. A targeted history-oriented audit found **no direct primary study in the audited candidate set that reconstructs an ancestral shared cue and then demonstrates repeated evolution toward pollinator-private or antagonist-avoiding descendant cues under dual-audience selection**.

This is not a claim that such evolution never occurs. It is a fail-closed result for the current targeted candidate set and it converts the former generic gap into an explicit historical-identification gate.

A follow-up system-focused audit identifies the fig–fig-wasp radiation as a **composite near-L4 candidate**: phylogenetic scent divergence, an extant private pollinator channel, non-pollinating wasp use of receptive scent, and developmental chemical gating all occur within *Ficus*. These pieces still come from separate studies and are not joined in one replicated historical transition analysis, so direct L4 remains unrecovered.

## Direct-history gate

A study counts as a direct `shared -> private` or lineage-branching test only if it supplies all of the following:

1. **ancestral state** — an ancestral integrated/shared cue is explicitly reconstructed or otherwise historically identified;
2. **descendant architecture** — descendant states contain a demonstrably more receiver-specific or partitioned cue architecture rather than merely different trait values;
3. **pollinator channel** — the descendant change is tied to retained or altered pollinator response/fitness;
4. **antagonist channel** — the same historical change is tied to antagonist response/cost rather than inferred from pollination alone;
5. **replicated transition and alternatives** — transitions are replicated across branches or independent lineages and plausible phylogenetic/abiotic alternatives are tested.

Failure of any gate yields `NOT_EVALUABLE` for the direct historical claim. Contemporary gating, population differentiation and experimental evolution remain positive evidence at their own levels.

## What the targeted candidates add

| Source | What it closes | Why it still does not close the historical claim |
|---|---|---|
| Page et al. 2014, doi:10.1371/journal.pone.0098755 | Interspecific recombinant *Silene* material plus direct seed-predator cue discrimination | No same-cue pollinator benefit and no ancestral transition reconstruction |
| Theis et al. 2014, doi:10.3732/ajb.1400171 | Comparative shared tracking of floral traits by specialist pollinators and floral herbivores | Taxon differences are not modeled as historical transitions |
| Knauer et al. 2018, doi:10.1038/s41467-018-03792-x | Shared-cue field manipulation and common-garden differentiation in inducibility | This is conditional deployment of a shared cue and population differentiation rather than private-cue origin |
| Ramos & Schiestl 2019, doi:10.1126/science.aav6962 | Replicated experimental evolution showing antagonism can redirect pollinator-driven floral evolution | Herbivory is not demonstrated as a receiver of the focal floral shared cue and the design does not reconstruct a natural ancestral transition |
| Joffard et al. 2020, doi:10.1111/plb.13104 | A phylogeny of 19 *Ophrys* species and phylogenetic comparative evidence that scent composition is associated with pollinator interactions while phylogenetic constraints differ among compound classes | This closes the phylogenetic-history side but does not include the antagonist channel or demonstrate a shared-to-private dual-audience transition |
| Mühlemann et al. 2006, doi:10.1007/s10886-006-9113-0 | Postpollination down-regulation of *Silene latifolia* scent compounds used by *Hadena bicruris* | Temporal reduction is a contemporary gating candidate; the same moth has pollinator and seed-predator roles and no lineage transition is tested |
| Campbell et al. 2022, doi:10.1086/716740 | Pollination and seed-predation fitness components measured across two *Ipomopsis* species and hybrids | Strong dual-selection information without ancestral-state or private-cue reconstruction |
| Opedal et al. 2019, doi:10.1002/ajb2.1209 | A useful negative control across 20 *Dalechampia* populations: seed predation was largely unrelated to floral advertisement and only weakly modified the inferred pollinator-driven trajectory | The necessary conflict itself is weak in this system; absence of conflict is not evidence that private cues evolved |

The machine-readable adjudication is `empirical/one_trait_shared_cue/HISTORICAL_CUE_TRANSITION_AUDIT_V1.csv`.

## Ficus composite bridge

The system-focused follow-up is intentionally kept separate from the study-level ledger because no single *Ficus* source passes all historical gates. Its value is that the required pieces occur within one radiation rather than in unrelated analogies.

| Primary source | Piece recovered | Historical limit |
|---|---|---|
| Cao et al. 2026, doi:10.1111/nph.71133 | receptive-fig VOC composition across 32 *Ficus* species with strong phylogenetic signal | phylogenetic divergence is observed, but an ancestral shared cue and repeated private-cue transitions are not reconstructed |
| Chen et al. 2009, doi:10.1111/j.1365-2435.2009.01622.x | 4-methylanisole is an unusual dominant volatile sufficient for attraction of the specific *F. semicordata* pollinator | an extant private pollinator channel does not identify its evolutionary origin or antagonist contribution |
| Proffit et al. 2009, doi:10.1111/j.1570-7458.2009.00823.x | both pollinating and non-pollinating parasitic fig wasps track the specific receptive odour of *F. hispida* | contemporary shared-cue exploitation is not a historical transition |
| Long et al. 2026, doi:10.1016/j.ijbiomac.2026.152992 | receptive attractant synthesis, postpollination repellent synthesis, pollinator behaviour and pollinator/non-pollinator olfactory binding differences | developmental gating and receiver differentiation are mechanism evidence, not replicated lineage history |

The composite status is therefore:

```text
COMPOSITE_NEAR_L4
not DIRECT_L4
```

Detailed decomposition is in `docs/SCH_FICUS_COMPOSITE_HISTORY_BRIDGE_AUDIT_V1.md` and `empirical/one_trait_shared_cue/FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv`.

## New evidence ladder

The SCH endpoint should therefore be reported as a ladder rather than a binary branching claim:

```text
L0  contemporary dual-audience response / opposing selection
 -> L1  component partitioning or conditional gating
 -> L2  population differentiation or measured microevolution
 -> L3  phylogenetic trait divergence associated with one audience
 -> L4  reconstructed shared-cue -> private-cue transition under both audiences
```

The current evidence reaches **L2 directly in strict dual-audience or broader conflict cases**, and reaches **L3 on the historical trait-divergence side**. *Ficus* additionally places L0/L1 dual-audience mechanisms, an extant private pollinator channel and L3 phylogenetic scent divergence inside one radiation. It still does not reach L4 because those states have not been reconstructed as repeated transitions jointly conditioned on both receiver regimes.

This distinction matters because a phylogenetic pollinator-scent association is not evidence that antagonists caused the transition, while a contemporary antagonist-avoidance mechanism is not evidence that the mechanism originated by lineage divergence.

## Consequence for Chapter 1

Chapter 1 can make a stronger bounded statement than before:

> Shared signals have multiple empirically demonstrated evolutionary responses: an integrated stabilizing compromise, context-dependent maintenance of alternative phenotypes, population-level evolutionary change, and partial ecological decoupling through component or temporal gating. A targeted history audit finds phylogenetic cue divergence and contemporary avoidance mechanisms, and *Ficus* now supplies the strongest composite bridge because phylogenetic scent divergence, an extant private pollinator channel and non-pollinating wasp cue use occur within one radiation. No audited study nevertheless joins those pieces into a replicated ancestral shared-cue to private-cue transition under both mutualist and antagonist selection.

Thus `lineage branching` remains `NOT_EVALUABLE`, but now because the missing intersection is explicitly identified rather than because no candidate literature was inspected.

## Next decisive analysis

The next high-value step is no longer an unrestricted literature search. Prioritize *Ficus* and build a species-level matrix combining a resolved phylogeny, receptive scent architecture, pollinator identity/response, non-pollinating wasp or exploiter tracking of the same cues, developmental gating, and abiotic/geographic covariates. Only then test whether transitions toward more pollinator-specific cue architecture repeatedly coincide with reduced exploiter tracking after conditioning on phylogeny and alternatives.

Other candidate systems should be rejected early if they lack either historical reconstruction or the second receiver channel.
