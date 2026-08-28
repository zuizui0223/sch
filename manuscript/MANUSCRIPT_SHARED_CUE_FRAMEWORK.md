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

## 5. Evolutionary outcomes that must be distinguished

The same dual-audience trade-off can generate different evolutionary outcomes. They are not interchangeable interpretations of a positive or negative response to one experimental contrast.

Let the net one-trait fitness surface be

```text
W(A) = M(A) - G(A) - C(A).
```

Six outcome classes follow from different fitness geometry, frequency dependence, scale or architecture.

1. **Integrated compromise maintenance.** A single trait is maintained near an interior optimum `A*` when the net selection gradient is zero there and local curvature is negative. Pollinator gain and antagonist cost are balanced; neither channel must be absent.
2. **Directional specialization on the same axis.** If the net gradient remains positive over the observed range, selection is toward stronger attraction and greater pollinator gain. If it remains negative, selection is toward weaker exposure and antagonist avoidance. An endpoint shift is directional specialization, not evolutionary branching.
3. **Polymorphism maintenance.** Alternative values of one display can persist through negative frequency dependence, spatially or temporally varying selection, or gene flow among differently selected populations. This does not require an internal continuous optimum.
4. **Population differentiation.** Different mutualist-antagonist balances can redirect heritable phenotype frequencies or means among populations. Population change is an evolutionary result, but not yet a historical lineage split.
5. **Lineage branching.** True branching requires evidence for replicated transitions from an ancestral shared coordinate toward distinct audience-specific optima. Opposing consumer responses, maintained morphs or extant population differences alone do not establish this outcome.
6. **Cue modularization.** A formerly integrated display may separate into pollinator-facing and antagonist-facing components. This is an architectural escape from the one-coordinate constraint and must be distinguished from divergence toward opposite ends of one unchanged `A` axis.

The current evidence spine establishes more than shared tracking. A one-system observational fitness surface supports a stabilizing compromise, field studies of a floral-display dimorphism support context-dependent polymorphism maintenance and microevolutionary frequency change, and experimental or common-garden studies show that antagonists can redirect population-level floral evolution. Component partitioning and conditional emission support partial cue decoupling at the mechanism level. None of these results reconstructs the evolution of a private cue from an ancestral shared cue or a split into audience-specialized lineages.

## 6. First coverage gate

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common plant reproductive outcome
```

`D`, two-trait interaction, selective intervention and the BITA 16-cell design are deliberately absent from this first screen. The gate asks how often the literature has measured the linked empirical object before deciding whether effect-size synthesis is feasible.

## 7. Evidence spine

- **Sasidharan et al. 2023:** cross-study cue-response synthesis; supports recurrent shared attraction and rarer shared repulsion under source-version and pairing limits.
- **Theis & Adler 2012:** current directional-only coverage pass; enhanced fragrance increased florivore attraction and reduced seed production, without a detected pollinator-attraction increase.
- **Page et al. 2014:** floral colour and scent predict seed-eating pollinator host choice; supports antagonist use of floral cues but supplies no same-study pollination coefficient for the same axes.
- **Junker & Blüthgen 2010:** independent evidence that floral scent responses depend on consumer resource dependence; categories do not map exactly onto pollinator versus antagonist roles.
- **Knauer, Bakhtiari & Schiestl 2018:** antagonist removal by crab spiders changes the ecological context of floral-signal evolution; a mechanism/context anchor rather than a current strict coverage pass.

Three additional source-adjudicated systems form a supporting ring rather than strict passes. Kessler et al. (2015) manipulates a shared scent coordinate but separates pollinator-mediated seed production from antagonist oviposition across assay structures. Pérez-Barrales et al. (2013) links both visitor roles and reproductive components to the same bract axis, but `A` is observational. Theis et al. (2014) provides comparative shared tracking of floral sesquiterpenoids without an `A` manipulation or common reproductive outcome. These near passes locate the measurement gap more precisely: manipulation, paired consumer responses and a commensurable plant outcome are usually distributed across different designs.

The exact admitted and prohibited uses are frozen in `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv`.

## 8. Research fork

If a systematic expansion leaves enough linked experiments, the paper becomes an existing-study integration plus a shared-cue framework, with effect-size lanes defined only after outcome compatibility is established. If few experiments remain, the primary result is a measurement gap: floral-signal research has measured mutualists and antagonists in separate experiments. That result directly motivates a field design measuring both responses and a common reproductive outcome under one `A` manipulation.

## 9. Separation from BITA

BITA explains why mechanism attribution becomes difficult for a two-trait attraction-by-defence interaction. SCH asks what the first-order attraction-antagonism balance looks like before a second trait is introduced. Evidence may be shared as provenance, but estimands and claims must not be exchanged.
