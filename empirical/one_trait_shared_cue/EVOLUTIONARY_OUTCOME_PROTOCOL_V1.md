# Evolutionary-outcome audit protocol v1

## Question

After establishing that pollinators and antagonists can respond to the same attraction coordinate, what does the current evidence explain about the evolutionary fate of that coordinate?

This is a second-stage audit. It does not alter the frozen four-field coverage gate or its counts.

## Outcome classes

The audit distinguishes six hypotheses.

| Outcome | Minimum admissible evidence |
|---|---|
| Integrated compromise maintenance | An interior fitness optimum on a declared `A` coordinate, or replicated temporal evidence of stabilizing selection around it |
| Directional specialization | A supported net fitness gradient over the declared range, with the favored endpoint interpreted as pollinator-gain maximization or antagonist-loss avoidance |
| Polymorphism maintenance | Frequency-dependent or spatially/temporally varying selection plus evidence that alternative values persist or change predictably within populations |
| Population differentiation | Heritable or common-garden phenotype differences, or measured evolutionary change, associated with different mutualist-antagonist regimes |
| Lineage branching | Replicated descendant transitions from an ancestral shared cue toward distinct audience-specific optima, with alternatives to the historical transition tested |
| Cue modularization | Distinct cue components with demonstrated consumer-specific response or selection, not merely two correlated measurements of one signal |

## Fail-closed rules

- Opposing pollinator and antagonist responses do not by themselves identify net fitness geometry.
- A single two-level contrast can support a local directional result but cannot establish an interior optimum or disruptive selection.
- Maintained morphs and population-frequency changes do not establish lineage branching.
- Population differences alone do not reconstruct an ancestral transition or audience-specific lineage specialization.
- Component-specific consumer responses can support separability but not evolved modularization unless evolutionary change or selection on the components is measured.
- `NOT_EVALUABLE` is retained as a result and never recoded as absence of the outcome.

## Historical transition gate

A direct `shared -> private` or lineage-branching claim is stricter than contemporary cue separation. It requires the same evidential chain to contain:

1. an explicitly reconstructed or historically identified ancestral shared cue;
2. a descendant receiver-specific or more partitioned cue architecture;
3. a pollinator response or fitness channel tied to that change;
4. an antagonist response or cost channel tied to the same change; and
5. replicated transitions plus tests of plausible phylogenetic or abiotic alternatives.

Phylogenetic pollinator-associated divergence without antagonist data is therefore a one-audience history result. Contemporary conditional gating or component partitioning without an ancestral transition is a mechanism result. Neither is promoted to lineage branching.

The targeted history-oriented adjudication is kept separately in `HISTORICAL_CUE_TRANSITION_AUDIT_V1.csv` so that near-misses can be informative without changing the 12-source evolutionary-outcome count.

## Source universe

Version 1 codes the eight source-adjudicated anchors in `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv` plus four targeted primary studies admitted only to the evolutionary-outcome audit. These additions do not enter or change the strict four-field coverage audit.

A separate eight-candidate historical-transition audit asks whether the unresolved private-cue/lineage endpoint can be closed. It is a targeted hypothesis-recovery audit rather than a systematic prevalence search and does not alter the 12-source outcome table.

## Claim ceiling

The audit reports which evolutionary hypotheses the current source spine can evaluate. It is not a prevalence estimate, a meta-analysis, or evidence that unevaluable outcomes do not occur in nature.