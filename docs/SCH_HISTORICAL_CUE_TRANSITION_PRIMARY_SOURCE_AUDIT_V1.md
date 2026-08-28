# SCH historical cue-transition primary-source audit v1

## Decision

The unresolved SCH endpoint can now be stated more precisely. A targeted history-oriented audit found **no direct primary study in the audited candidate set that reconstructs an ancestral shared cue and then demonstrates repeated evolution toward pollinator-private or antagonist-avoiding descendant cues under dual-audience selection**.

This is not a claim that such evolution never occurs. It is a fail-closed result for the current targeted candidate set and it converts the former generic gap into an explicit historical-identification gate.

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

## New evidence ladder

The SCH endpoint should therefore be reported as a ladder rather than a binary branching claim:

```text
L0  contemporary dual-audience response / opposing selection
 -> L1  component partitioning or conditional gating
 -> L2  population differentiation or measured microevolution
 -> L3  phylogenetic trait divergence associated with one audience
 -> L4  reconstructed shared-cue -> private-cue transition under both audiences
```

The current evidence reaches **L2 directly in strict dual-audience or broader conflict cases**, and reaches **L3 only on the pollinator-history side** through phylogenetic scent studies. It does not reach L4 in the targeted audit.

This distinction matters because a phylogenetic pollinator-scent association is not evidence that antagonists caused the transition, while a contemporary antagonist-avoidance mechanism is not evidence that the mechanism originated by lineage divergence.

## Consequence for Chapter 1

Chapter 1 can make a stronger bounded statement than before:

> Shared signals have multiple empirically demonstrated evolutionary responses: an integrated stabilizing compromise, context-dependent maintenance of alternative phenotypes, population-level evolutionary change, and partial ecological decoupling through component or temporal gating. A targeted history audit additionally finds phylogenetic pollinator-associated scent divergence and contemporary avoidance mechanisms, but no study in the audited set joins those pieces into a replicated ancestral shared-cue to private-cue transition under both mutualist and antagonist selection.

Thus `lineage branching` remains `NOT_EVALUABLE`, but now because the missing intersection is explicitly identified rather than because no candidate literature was inspected.

## Next decisive analysis

The next high-value literature/data pass should search specifically for systems where **both** pieces coexist: a resolved multi-species phylogeny with reconstructed floral cue architecture and matched mutualist/antagonist response or selection data. Candidate discovery should be rejected early if it lacks either historical reconstruction or the second receiver channel.
