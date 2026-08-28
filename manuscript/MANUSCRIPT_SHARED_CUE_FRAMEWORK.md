# Shared cues and the evolvability of floral attraction

## Working status

Conceptual and evidence-audit spine for a separate one-trait synthesis. This document is not part of the BITA submission.

## 1. Question

Floral colour, scent, display and reward can increase pollinator attraction while also exposing flowers to florivores, seed predators, nectar robbers or other antagonists. The operative question is not simply whether conspicuous flowers attract enemies. It is:

> **Does overlap in the cues used by pollinators and antagonists determine whether the attraction-antagonism trade-off can be escaped?**

## 2. Estimands

Let `A` be one declared and commensurable manipulation of a floral attraction/display trait. Define the channel contrasts on that same `A` coordinate:

```text
M_A = E[M | do(A=1)] - E[M | do(A=0)]
G_A = E[G | do(A=1)] - E[G | do(A=0)]
S_A = M_A - G_A
```

`M_A` is the change in pollinator-mediated reproductive benefit and `G_A` is the change in antagonist-mediated reproductive loss. They may be estimated separately and combined only when their outcomes and scales are commensurable. Direct physiological or construction cost remains a separate term when it is not standardized by design.

This first-order target requires neither a second trait `D` nor `Delta_AD W`. It is identifiable under a weaker design than BITA's crossed mechanism-allocation problem, provided the two channels are measured or intervened upon defensibly on the same `A` contrast. Selective consumer intervention is one route to a causal channel estimate; it is not a requirement for the initial coverage count.

## 3. Shared-cue mechanism

Let cue overlap denote the extent to which pollinators and antagonists respond to the same sensory coordinate of `A`. It is a biological property to be operationalized, not a value inferred from role labels alone.

### Shared cue

When both consumer classes track the same cue, increasing `A` tends to move `M_A` and `G_A` together. Selection cannot freely increase pollinator attraction without also changing antagonist exposure. Signal exaggeration is therefore constrained unless pollinator benefit rises faster than antagonist cost or another ecological process breaks the linkage.

### Private or separable cue

When pollinators and antagonists use different cue components, the signal can evolve along a coordinate that increases pollinator response while weakly affecting or reducing antagonist response. The attraction-antagonism trade-off is more avoidable.

## 4. Predeclared predictions

1. Greater cue sharing shifts the relationship between display intensity and net reproductive fitness toward a flatter or more negative slope.
2. Shared-cue systems show more concordant pollinator and antagonist response directions to the same `A` contrast than private-cue systems.
3. Manipulating a separable cue component can increase `M_A` without a corresponding increase in `G_A`.
4. Removing or suppressing antagonists changes selection on shared floral signals more strongly than on pollinator-private signals.

These are framework predictions. Current source counts do not establish their prevalence or effect-size distribution.

## 5. First coverage gate

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common plant reproductive outcome
```

`D`, two-trait interaction, selective intervention and the BITA 16-cell design are deliberately absent from this first screen. The gate asks how often the literature has measured the linked empirical object before deciding whether effect-size synthesis is feasible.

## 6. Evidence spine

- **Sasidharan et al. 2023:** cross-study cue-response synthesis; supports recurrent shared attraction and rarer shared repulsion under source-version and pairing limits.
- **Theis & Adler 2012:** current directional-only coverage pass; enhanced fragrance increased florivore attraction and reduced seed production, without a detected pollinator-attraction increase.
- **Page et al. 2014:** floral colour and scent predict seed-eating pollinator host choice; supports antagonist use of floral cues but supplies no same-study pollination coefficient for the same axes.
- **Junker & Blüthgen 2010:** independent evidence that floral scent responses depend on consumer resource dependence; categories do not map exactly onto pollinator versus antagonist roles.
- **Knauer, Bakhtiari & Schiestl 2018:** antagonist removal by crab spiders changes the ecological context of floral-signal evolution; a mechanism/context anchor rather than a current strict coverage pass.

Three additional source-adjudicated systems form a supporting ring rather than strict passes. Kessler et al. (2015) manipulates a shared scent coordinate but separates pollinator-mediated seed production from antagonist oviposition across assay structures. Pérez-Barrales et al. (2013) links both visitor roles and reproductive components to the same bract axis, but `A` is observational. Theis et al. (2014) provides comparative shared tracking of floral sesquiterpenoids without an `A` manipulation or common reproductive outcome. These near passes locate the measurement gap more precisely: manipulation, paired consumer responses and a commensurable plant outcome are usually distributed across different designs.

The exact admitted and prohibited uses are frozen in `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv`.

## 7. Research fork

If a systematic expansion leaves enough linked experiments, the paper becomes an existing-study integration plus a shared-cue framework, with effect-size lanes defined only after outcome compatibility is established. If few experiments remain, the primary result is a measurement gap: floral-signal research has measured mutualists and antagonists in separate experiments. That result directly motivates a field design measuring both responses and a common reproductive outcome under one `A` manipulation.

## 8. Separation from BITA

BITA explains why mechanism attribution becomes difficult for a two-trait attraction-by-defence interaction. SCH asks what the first-order attraction-antagonism balance looks like before a second trait is introduced. Evidence may be shared as provenance, but estimands and claims must not be exchanged.
