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
- Campbell et al. (2022) measure pollination and seed-predation selection components across *Ipomopsis* species and hybrids, but do not reconstruct an ancestral shared cue or private-cue origin.
- Opedal et al. (2019) provide a useful negative control: across 20 *Dalechampia* populations, seed predation was largely unrelated to floral advertisement, so the antagonist conflict required by the branching hypothesis is weak in that system.

None of the eight candidates jointly provides an ancestral shared state, a descendant private architecture, both receiver channels, replicated transitions and alternative-history tests. The historical endpoint therefore remains `NOT_EVALUABLE`, but the missing intersection is now specified rather than left as a generic literature gap.

The detailed adjudication is in `docs/SCH_HISTORICAL_CUE_TRANSITION_PRIMARY_SOURCE_AUDIT_V1.md` and `HISTORICAL_CUE_TRANSITION_AUDIT_V1.csv`.

## Ficus closes the composite-system gap, but not L4

A targeted follow-up found a substantially stronger candidate architecture within one biological radiation. Across separate primary studies, *Ficus* now supplies phylogenetic scent divergence across 32 species, an extant pollinator-private volatile channel in *F. semicordata*, direct exploitation of receptive fig odour by a non-pollinating parasitic wasp in *F. hispida*, and developmental attraction-to-repellence switching with pollinator/non-pollinator olfactory differentiation.

This matters because the L3 history side and L0–L1 dual-audience/mechanism side are no longer merely scattered across unrelated plant systems. They coexist within the fig–fig-wasp radiation. We therefore classify *Ficus* as:

```text
COMPOSITE_NEAR_L4
not DIRECT_L4
```

The promotion stops there. No audited *Ficus* study maps shared versus private cue states, both receiver channels and repeated transitions onto the same phylogeny while testing alternative histories. Cross-study coherence identifies a high-value candidate system; it cannot manufacture the missing historical estimand. The dedicated ledger and audit are `FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv` and `docs/SCH_FICUS_COMPOSITE_HISTORY_BRIDGE_AUDIT_V1.md`.

## Hypothesis recovery statement

Current data recover three ways in which a one-trait conflict can be handled: stabilizing balance around an integrated phenotype, context-dependent maintenance and change of alternative phenotypes, and population-level redirection of floral evolution. They also recover component partitioning and conditional gating as plausible decoupling mechanisms.

What remains unrecovered is the stronger historical claim that dual-audience selection caused an ancestral shared cue to evolve into pollinator-private and antagonist-avoiding modules or into distinct specialized lineages. *Ficus* is now the strongest composite bridge because phylogenetic divergence, a private pollinator channel, exploiter use of receptive scent and temporal gating occur within the same radiation, but those pieces have not yet been joined in one replicated dual-audience transition analysis.

## Next valid gates

1. Extend the unchanged four-field coverage screen beyond the BITA-derived source universe.
2. For retained experiments, code `selection_form`, `cue_architecture`, `evolutionary_level`, `causal_strength`, and `claim_ceiling` separately.
3. Use “directional specialization” for supported endpoint movement; reserve “lineage branching” for replicated historical transitions from an ancestral shared cue.
4. Test cue decoupling with a common factorial design showing preserved pollinator benefit, reduced antagonist cost, and improved net plant fitness.
5. For the historical endpoint, prioritize *Ficus* and reject other candidate systems early unless they contain both a resolved transition/ancestral-state analysis and matched mutualist-antagonist response or selection data.
6. In *Ficus*, build a species-level phylogenetic matrix of cue architecture, pollinator response, non-pollinating wasp/exploiter tracking, developmental gating and abiotic alternatives before attempting an L4 transition model.
