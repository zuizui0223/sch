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

For that stronger historical endpoint, evidence is reported as a ladder rather than a binary branching claim:

```text
L0  contemporary dual-audience response / opposing selection
 -> L1  component partitioning, conditional gating or temporal receiver separation
 -> L2  population differentiation or measured microevolution
 -> L3  phylogenetic trait divergence associated with one audience
 -> L4  reconstructed shared-cue -> private-cue transition under both audiences
```

Current evidence reaches L2 directly in several conflict systems and reaches L3 on the historical trait-divergence side. The strict L4 endpoint remains unrecovered.

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

### 7.1 Historical bridge: Ficus is near L4 but not L4

A targeted history audit identifies the fig–fig-wasp radiation as the strongest composite bridge to the missing historical endpoint. A fixed 32-species receptive-scent scaffold contains two directly resolved pollinator recognition architectures and direct dual-audience evidence elsewhere in the same radiation.

- **Ficus semicordata:** 4-methylanisole is sufficient for attraction of its pollinator. In the same host system, direct field observations place *Platyneura cunia* oviposition about 10 days after pollinator entry and *Sycoscapter trifemmensis* 14–32 days after pollinator entry. This is direct temporal receiver separation, but neither NPFW has been shown behaviourally to ignore, avoid or follow 4-methylanisole itself.
- **Ficus carica:** its pollinator is attracted by a precise four-VOC ratio, and small perturbations of that ratio abolish attraction. *Philotrypesis caricae* is documented from the host, but no matched test has been recovered for NPFW response to the validated four-VOC code.
- **Ficus hispida:** pollinator and non-pollinating *Philotrypesis* respond directly to receptive odour, but the minimal synthetic pollinator-attractive code is not yet resolved to the same standard.
- **Ficus auriculata:** a useful leaky/shared comparator in which pollinator host preference is not chemically absolute.

The matched historical bottleneck is therefore not generic lack of phylogeny or lack of pollinator specificity. It is the absence of the same chemical-coordinate receiver intersection:

```text
resolved pollinator attractive chemical codes:              2
private-code host with direct NPFW temporal separation:      1
resolved code + direct same-code NPFW behavioural response:  0
DIRECT_L4 transitions:                                      0
```

This distinction is essential. Temporal separation does not prove chemical privatization, NPFW host association does not prove interception of the pollinator code, and whole-odour response does not identify response to an unresolved key code. The radiation is therefore classified `COMPOSITE_NEAR_L4`, not `DIRECT_L4`.

The remaining same-code experiment also exposes an information asymmetry that matters for interpreting both old and future bioassays. Strong attraction can be detected with tens to roughly a hundred decisive choices, whereas a positive claim of behavioural privacy requires an equivalence design rather than a failed attraction test. Under the registered default criterion — a 90% Wilson interval wholly inside `[0.40, 0.60]` when the true NPFW choice probability is 0.50 — the exact prospective planner requires 206 decisive choices for 80% power and 260 for 90%. With an explicit design-effect inflation of 1.5 and a decisive-choice fraction of 0.75, those targets become approximately 412 and 520 introduced wasps. By contrast, if true interception is strong (`p=0.65`), the corresponding 80% and 90% targets are 82 and 111 decisive choices; at `p=0.70` they are 43 and 62. Thus nonsignificance at a legacy attraction sample size cannot be reinterpreted as evidence for a private channel.

The assay classifier therefore requires three gates before `BEHAVIORAL_NONRESPONSE_EQUIVALENT` can be assigned: replication of the pollinator code, a working NPFW host/stage positive control, and an NPFW same-code interval contained inside the predeclared equivalence zone. Interception, avoidance, equivalence-supported nonresponse and inconclusive response remain separate states. These rules convert the historical gap into a prospective measurement contract rather than a post hoc label.

The machine-readable and bounded records are `empirical/one_trait_shared_cue/FICUS_32_SPECIES_L4_CANDIDATE_MATRIX_V1.csv`, `empirical/one_trait_shared_cue/FICUS_SAME_CODE_RECEIVER_GAP_V1.csv`, `empirical/one_trait_shared_cue/FICUS_SAME_CODE_ASSAY_POWER_V1.json`, `docs/SCH_FICUS_32_SPECIES_L4_MATRIX_READOUT_V1.md`, `docs/SCH_FICUS_SAME_CODE_RECEIVER_GAP_READOUT_V1.md`, and `docs/SCH_FICUS_SAME_CODE_EXPERIMENT_PROTOCOL_V1.md`.

## 8. Research fork

The research fork now differs by evidence layer.

For the first-order coverage and lower evolutionary layers, a broader systematic expansion remains useful: if enough linked experiments survive the coverage gate, the paper can estimate compatible effect-size lanes; if few survive, the measurement gap itself becomes a result.

For the historical L4 endpoint, the strategy is no longer a broad literature search. The high-value next step is to close three explicit same-code cells inside *Ficus*:

1. test NPFWs in *F. semicordata* against 4-methylanisole at their natural post-pollination timing windows;
2. test *Philotrypesis caricae* and other relevant exploiters against the validated *F. carica* four-VOC ratio and perturbed ratios;
3. resolve the minimal *F. hispida* pollinator code and test *Philotrypesis* against that identical synthetic coordinate.

Those experiments should be powered to the intended claim. Interception/avoidance detection and equivalence-supported privacy are different information targets; the latter must not be inferred merely because the former is nonsignificant.

Only after matched receiver states exist should shared/private code states be reconstructed on the 32-species phylogeny and tested against section, reproductive system, phylogenetic and abiotic/geographic alternatives. If the same-code cell remains empty, repeated shared-to-private evolution remains `NOT_EVALUABLE` rather than negative evidence for the hypothesis.

## 9. Separation from BITA

BITA explains why mechanism attribution becomes difficult for a two-trait attraction-by-defence interaction. SCH asks what the first-order attraction-antagonism balance looks like before a second trait is introduced. Evidence may be shared as provenance, but estimands and claims must not be exchanged.
