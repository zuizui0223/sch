# Evolutionary-outcome audit readout v1

## Positive result

The primary-source audit recovers several evolutionary outcomes at bounded levels.

- **Integrated compromise:** Pérez-Barrales et al. (2013) directly estimate an observational fitness surface in which pollinator selection for larger bracts is counteracted by seed-predator selection and net selection tends to be stabilizing.
- **Context-dependent polymorphism maintenance:** Toräng et al. (2008) recover frequency-dependent selection on alternative display morphs; Ågren et al. (2013) connect opposing pollinator/grazer selection to long-term morph-frequency change.
- **Population evolutionary change:** Ågren et al. provide field-manipulation and microevolutionary evidence; Knauer et al. (2018) recover common-garden population differentiation in inducible shared-cue emission; Ramos & Schiestl (2019) show experimentally that herbivory redirects pollinator-driven floral evolution.
- **Partial cue decoupling:** Kessler et al. (2013) recover different functions among bouquet components, Kessler et al. (2015) experimentally uncouple scent and nectar axes, and Knauer et al. recover conditional emission of a shared cue.

These results demonstrate that one-trait conflict need not have only one outcome. It can produce an interior compromise, maintained alternative morphs, or population-level trajectory differences; complex or conditionally expressed signals can partially separate receiver effects.

## Where the current data stop

```text
observational interior compromise:          1 direct case
local experimental net-negative direction: 1 direct case
polymorphism maintenance:                   2 direct bounded cases
population differentiation/change:          3 direct bounded sources
partial modularity mechanisms:              3 direct mechanism sources
private-cue evolution from a shared cue:     0 direct sources
lineage branching/specialization:            0 direct sources
```

The positive cases do not all satisfy the strict four-field SCH coverage gate, and they do not share one effect scale. They are hypothesis-recovery evidence, not a pooled estimate or prevalence result.

## The historical gap is now explicitly audited

A separate eight-candidate history-oriented audit asks whether the missing private-cue/lineage endpoint is merely absent from the original source spine or actually fails a stricter historical-identification gate.

The candidates close complementary parts of the chain:

- Joffard et al. (2020) provide a 19-species *Ophrys* phylogeny and phylogenetic comparative evidence linking scent composition to pollinator interactions, but no antagonist channel.
- Mühlemann et al. (2006) provide a plausible contemporary temporal-avoidance mechanism through postpollination scent down-regulation in *Silene*, but no reconstructed lineage transition.
- Campbell et al. (2022) measure pollination and seed-predation fitness components across *Ipomopsis* species and hybrids, but do not reconstruct an ancestral shared cue or private-cue origin.
- Opedal et al. (2019) provide a useful negative control: across 20 *Dalechampia* populations, seed predation was largely unrelated to floral advertisement, so the antagonist conflict required by the branching hypothesis is weak in that system.

None of the eight candidates jointly provides an ancestral shared state, a descendant private architecture, both receiver channels, replicated transitions and alternative-history tests. The historical endpoint therefore remains `NOT_EVALUABLE`, but the missing intersection is now specified rather than left as a generic literature gap.

The detailed adjudication is in `docs/SCH_HISTORICAL_CUE_TRANSITION_PRIMARY_SOURCE_AUDIT_V1.md` and `HISTORICAL_CUE_TRANSITION_AUDIT_V1.csv`.

## Ficus closes the composite-system gap, but not L4

A targeted follow-up found a substantially stronger candidate architecture within one biological radiation. The Cao et al. 32-species receptive-scent comparison is now a fixed species-level matrix rather than a proposed future scaffold.

Within that matrix and its matched receiver-gap extension:

- *F. semicordata* has a directly resolved single-compound pollinator code, 4-methylanisole, and direct field observations place at least two NPFW oviposition windows after the pollinator (*Platyneura cunia* at about 10 days; *Sycoscapter trifemmensis* at 14–32 days); the NPFWs have still not been tested behaviourally against 4-methylanisole itself;
- *F. carica* independently has a directly resolved ratio-specific four-VOC pollinator code and a documented NPFW, *Philotrypesis caricae*, but no same-code NPFW behavioural test;
- *F. hispida* has direct pollinator plus non-pollinating-parasite response to receptive odour and newer species-specific blend evidence, but its minimal synthetic pollinator code remains unresolved;
- *F. auriculata* supplies a directly tested leaky/shared chemical-filter comparator because its pollinator also responds to an alternative host sharing semiochemicals;
- *F. racemosa* adds direct non-pollinating-wasp response to stage-specific fig odour;
- developmental attraction-to-repellence switching and pollinator/non-pollinator receptor differentiation are recovered within the same radiation.

This matters because the L3 history side and L0–L1 dual-audience/mechanism side are no longer merely scattered across unrelated plant systems. They coexist within the fig–fig-wasp radiation, at least two distinct pollinator recognition architectures are resolved, and one private-code host now has direct temporal receiver separation. We therefore classify *Ficus* as:

```text
COMPOSITE_NEAR_L4
not DIRECT_L4
```

The promotion still stops there. The fixed evidence contains **zero species in which a resolved pollinator-attractive chemical code is paired with direct non-pollinating-wasp behaviour to that same code**. Temporal separation does not close that chemical-coordinate cell: a delayed NPFW can still detect or use the pollinator cue. Consequently there is not yet a biologically matched shared/private state to reconstruct through history. Cross-study coherence identifies a high-value candidate radiation; it cannot manufacture the missing historical estimand.

The dedicated sources are `FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv`, `FICUS_32_SPECIES_L4_CANDIDATE_MATRIX_V1.csv`, `FICUS_SAME_CODE_RECEIVER_GAP_V1.csv`, `docs/SCH_FICUS_COMPOSITE_HISTORY_BRIDGE_AUDIT_V1.md`, `docs/SCH_FICUS_32_SPECIES_L4_MATRIX_READOUT_V1.md`, and `docs/SCH_FICUS_SAME_CODE_RECEIVER_GAP_READOUT_V1.md`.

## Hypothesis recovery statement

Current data recover three ways in which a one-trait conflict can be handled: stabilizing balance around an integrated phenotype, context-dependent maintenance and change of alternative phenotypes, and population-level redirection of floral evolution. They also recover component partitioning, conditional gating and direct temporal separation as plausible decoupling mechanisms.

What remains unrecovered is the stronger historical claim that dual-audience selection caused an ancestral shared cue to evolve into pollinator-private and antagonist-avoiding modules or into distinct specialized lineages. *Ficus* is now the strongest composite bridge because phylogenetic divergence, multiple pollinator-code architectures, exploiter use of receptive scent, leaky filtering, temporal separation and developmental gating occur within the same radiation. The remaining gap is no longer generic: the resolved pollinator code and exploiter response have not yet been measured on the same chemical coordinate and then reconstructed as repeated historical transitions.

## Next valid gates

1. Extend the unchanged four-field coverage screen beyond the BITA-derived source universe only for the lower evidence layers; do not use another broad search as the main L4 strategy.
2. For retained experiments, code `selection_form`, `cue_architecture`, `evolutionary_level`, `causal_strength`, and `claim_ceiling` separately.
3. Use “directional specialization” for supported endpoint movement; reserve “lineage branching” for replicated historical transitions from an ancestral shared cue.
4. Test cue decoupling with a common factorial design showing preserved pollinator benefit, reduced antagonist cost, and improved net plant fitness.
5. For the historical endpoint, prioritize the fixed *Ficus* matrix and reject other candidate systems early unless they contain both a resolved transition/ancestral-state analysis and matched mutualist-antagonist response or selection data.
6. Close the three same-code cells first: non-pollinator response to 4-methylanisole in *F. semicordata* at the natural NPFW timing windows; *Philotrypesis caricae* or other exploiter response to the four-VOC ratio code in *F. carica*; and a synthetically resolved pollinator code plus *Philotrypesis* response in *F. hispida*.
7. Only after those receiver states overlap should shared/private code states be reconstructed on the 32-species phylogeny and tested against section, reproductive system, phylogenetic and abiotic/geographic alternatives.
