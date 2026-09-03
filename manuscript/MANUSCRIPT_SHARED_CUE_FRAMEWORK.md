# Shared cues and the evolvability of floral attraction

## Working status

Mechanism-first Chapter 1 framework paired with BITA. SCH develops an identifiable experiment for the one-trait shared-cue problem and uses systematic and targeted literature evidence to establish that the proposed routes and evolutionary outcomes occur in real biological systems. The literature synthesis is evidence grounding, not the primary estimand.

## 1. Question

Floral colour, scent, display and reward can increase pollinator attraction while also exposing flowers to florivores, seed predators, nectar robbers or other antagonists. The central question is:

> **When pollinators and antagonists act on the same floral attraction coordinate, does antagonist exposure measurably constrain the reproductive value of attraction, and can that mechanism be separated into identifiable channels?**

This question has an informational component and a functional component.

- **Informational overlap:** both receiver classes use the same sensory/display coordinate of `A`.
- **Functional conflict:** pollinator access increases the reproductive value of that `A`, while antagonist access decreases it.

A complete SCH result requires these layers to be linked rather than inferred from visitor labels alone.

## 2. Core estimand and 8-cell design

Let `A` be one predeclared and commensurable manipulation of a floral attraction/display trait. Cross it with antagonist state `G` and pollinator state `P`:

```text
A x G x P
```

with two levels of each factor, giving eight cells on one common plant reproductive outcome `W`.

Define

```text
W[a,g,p] = expected reproductive outcome

d[g,p] = W[1,g,p] - W[0,g,p].
```

The natural-community attraction effect is

```text
Delta_A W_natural = d[1,1].
```

That total contrast is not a mechanism allocation.

### 2.1 Pollinator-mediated contribution

At fixed antagonist state `g`,

```text
M_A(g) = d[g,1] - d[g,0].
```

A positive `M_A(g)` means pollinator access makes increasing `A` more reproductively beneficial.

### 2.2 Antagonist-mediated loss

At fixed pollinator state `p`,

```text
G_A(p) = d[0,p] - d[1,p].
```

A positive `G_A(p)` means antagonist presence erodes the reproductive effect of increasing `A`.

### 2.3 Consumer-independent remainder

```text
B_A = d[0,0].
```

`B_A` remains unallocated unless an independent assay identifies a narrower construction, physiological or autonomous-reproduction component. In particular, SCH must not silently equate `B_A` with `-C_A`.

### 2.4 Channel-dependence diagnostic

```text
J_A = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

Equivalently,

```text
J_A = M_A(1) - M_A(0)
    = -(G_A(1) - G_A(0)).
```

A non-zero `J_A` means the pollinator contribution depends on antagonist state and, equivalently, the antagonist loss depends on pollinator state. The simplest separable-channel model should then be rejected in favor of state-specific channel contrasts.

Around the consumer-free baseline,

```text
d[1,1] = B_A + M_A(0) - G_A(0) + J_A.
```

This is an accounting identity, not permission to assign biological labels without selective interventions.

The full inference contract is `docs/SCH_MECHANISM_IDENTIFICATION_DESIGN_V1.md`.

## 3. Shared-cue mechanism

Cue overlap is a biological property of the manipulated coordinate, not a value inferred from the names of interacting species.

### Shared cue

When pollinators and antagonists both track the same coordinate of `A`, increasing attraction can simultaneously increase pollinator-mediated reproductive gain and antagonist-mediated reproductive loss. Attraction is then constrained because the plant cannot move freely along that coordinate for the benefit of one audience without changing exposure to the other.

### Private or separable cue

When the two receiver classes use different components, the plant can move along a pollinator-facing coordinate with weaker antagonist consequences. Component partitioning, conditional expression, temporal gating or receiver specificity can therefore increase the evolvability of attraction even when antagonists remain present in the system.

## 4. Mechanism and constraint claims

The strongest contemporary shared-cue result requires both:

```text
informational overlap on the same A coordinate
+
M_A(g) > 0
+
G_A(p) > 0
```

with uncertainty appropriate to the intended directional claims.

The realized constraint can then be expressed directly. Under natural pollinator access,

```text
G_A(1) = d[0,1] - d[1,1].
```

If `G_A(1) > 0`, antagonists flatten the attraction-fitness effect relative to the antagonist-free state. Stronger functional forms are kept separate:

```text
constraint attenuation:
0 < d[1,1] < d[0,1]

constraint release under antagonist removal:
d[1,1] <= 0 < d[0,1]

strict sign reversal under antagonist removal:
d[1,1] < 0 < d[0,1].
```

These outcome levels do not establish a historical shared-cue-to-private-cue transition.

## 5. Predeclared predictions

1. On a validated shared coordinate, pollinator access will make the reproductive effect of `A` more positive: `M_A(g) > 0`.
2. On that same coordinate, antagonist access will make the reproductive effect of `A` less positive: `G_A(p) > 0`.
3. Antagonist presence will flatten or reverse the attraction-fitness effect relative to antagonist suppression.
4. If the two channels are approximately separable, `J_A` will be near zero; if consumer effects depend on one another, `J_A` will be non-zero and channel contrasts will be state dependent.
5. A separable/private cue component will retain pollinator benefit with a smaller antagonist-mediated loss than a shared component measured on the same outcome scale.
6. Repeated `A` levels or population contrasts should translate these channel differences into different fitness-surface geometries and evolutionary outcomes.

## 6. Literature as real-world mechanism evidence

The literature programme is retained because the identification framework must be biologically grounded. It has four explicit roles.

### 6.1 Route reality

Existing studies show that floral attraction/display traits influence pollinator behavior, antagonist behavior and reproductive outcomes across real systems. Shared or opposing responses to floral scent, color, morphology and display demonstrate that the proposed receiver routes are not hypothetical constructs.

### 6.2 Outcome reality

Primary-source audits recover several bounded evolutionary consequences of dual-audience conflict:

- an observational stabilizing compromise around an integrated display;
- context-dependent maintenance and change of alternative floral morphs;
- population-level evolutionary redirection under antagonists and pollinators;
- partial decoupling through component partitioning, conditional emission and temporal receiver separation.

These cases show that conflict can shape evolutionary outcomes even though they do not all satisfy the complete SCH identification design.

### 6.3 Design-gap localization

The strict linked measurement gate asks whether the same study contains

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common plant reproductive outcome.
```

Through the current V20 systematic state, two studies satisfy this measurement architecture: Theis & Adler (2012) and Sánchez-Lafuente (2007). Theis & Adler recovers antagonist attraction and reduced seed production without a detected increase in pollinator attraction; *Linaria lilacina* recovers pollinator/reproductive effects while fruit-predator visitation does not respond to the manipulation.

Thus the linked architecture now replicates, but the central positive dual-audience chain remains unrecovered in those strict cases. The measurement gap motivates the 8-cell experiment rather than replacing it.

Near-passes strengthen the same conclusion. Theis (2006) shows direct shared chemical attraction of pollinators and floral herbivores but lacks a common reproductive outcome. Junker & Bluethgen (2010) shows opposite receiver responses to the same synthetic scent coordinate but also lacks the common plant outcome. Kessler et al. (2015) manipulates a floral scent coordinate but distributes pollinator-mediated reproduction and antagonist oviposition across assay structures. Other observational systems link both receiver roles and reproduction without randomized `A`.

### 6.4 Historical extension

The literature also identifies candidate systems in which contemporary shared/private states might eventually be connected to historical transition. This is a later evolutionary layer, not the primary contemporary mechanism test.

## 7. Current systematic evidence state

The frozen V2 OpenAlex cohort contains 868 records. The current V20 screening state is:

```text
identified frozen cohort:        868
title/abstract screened:         405
primary studies included:        117
unscreened:                      463
strict linked experiments:         2
directional / near-pass lane:    104
evolutionary-outcome lane:        39
historical-transition lane:        4
```

These counts are not natural-prevalence estimates and do not estimate `M_A`, `G_A`, `B_A` or `J_A`. Their current scientific value is real-world recurrence, outcome grounding and measurement-gap localization.

The systematic screen may continue to completion, but completion is no longer the gate that defines SCH's scientific identity.

## 8. Evolutionary outcomes

The one-trait fitness problem can be represented generically as

```text
W(A) = M(A) - G(A) - C(A),
```

when the component scales are commensurable and direct cost is independently identified. Different fitness geometry, frequency dependence, spatial context and signal architecture can produce distinct outcomes:

1. **Integrated compromise:** an interior optimum on one shared coordinate.
2. **Directional specialization:** movement toward one end of the same coordinate.
3. **Polymorphism maintenance:** alternative values maintained by frequency dependence or variable selection.
4. **Population differentiation:** spatially differing mutualist-antagonist balances redirect phenotype means or frequencies.
5. **Cue modularization:** an integrated display separates into more receiver-specific components.
6. **Lineage branching:** replicated historical transitions toward distinct audience-specific optima.

Current direct evidence reaches compromise, polymorphism/population change and partial modularization. Lineage branching from an ancestral shared cue remains unevaluated.

For historical inference, retain the bounded ladder:

```text
L0  contemporary dual-audience response / opposing selection
 -> L1  component partitioning, conditional gating or temporal separation
 -> L2  population differentiation or measured microevolution
 -> L3  phylogenetic trait divergence associated with one audience
 -> L4  reconstructed shared-cue -> private-cue transition under both audiences
```

## 9. Ficus as historical extension, not the main SCH proof

The fig-fig-wasp radiation remains the strongest composite bridge toward L4. Within the current fixed source set:

- *Ficus semicordata* has a resolved pollinator-attractive code, 4-methylanisole, and direct temporal separation of non-pollinating fig-wasp oviposition windows;
- *F. carica* has a validated ratio-specific four-VOC pollinator code and a documented non-pollinating wasp;
- *F. hispida* has direct pollinator and non-pollinator response to receptive odor, but its minimal synthetic pollinator code remains unresolved;
- *F. auriculata* provides a leaky/shared chemical-filter comparator.

The decisive same-coordinate cell is still empty:

```text
resolved pollinator attractive chemical codes:              2
private-code host with direct NPFW temporal separation:      1
resolved code + direct same-code NPFW behavioural response:  0
DIRECT_L4 transitions:                                      0
```

Therefore *Ficus* remains

```text
COMPOSITE_NEAR_L4
not DIRECT_L4.
```

Temporal separation does not prove chemical privacy, host association does not prove interception of the pollinator code, and nonsignificant attraction does not establish equivalence-supported nonresponse.

The existing Ficus matrices, power calculations, trial-data contract and same-code protocol remain valid as the historical extension module.

## 10. Empirical programme

The mechanism-first programme is staged so that effect sizes are learned at the correct scale.

```text
Stage 0  validate one A coordinate and paired receiver access
         manipulation checks + same-coordinate behavioral evidence

Stage 1  pilot A x antagonist x pollinator
         estimate d[g,p], M_A(g), G_A(p), B_A, J_A,
         variance, clustering and intervention selectivity

Stage 2  re-power and execute the confirmatory 8-cell design
         test paired functional conflict and realized constraint

Stage 3  independently assay the consumer-free remainder
         identify construction/physiological cost only if justified

Stage 4  evolutionary extension
         multiple A levels, populations or experimental evolution
         to estimate fitness-surface geometry and longer-term outcomes
```

Literature-derived visitor effects must not be substituted for mechanism-scale pilot effects when powering the confirmatory experiment.

## 11. Relationship to BITA

SCH and BITA answer sequential questions.

```text
Chapter 1 — SCH
A x antagonist x pollinator
8 cells
-> why is one attraction coordinate conflicted?

Chapter 2 — BITA
A x D x antagonist x pollinator
16 cells
-> can a distinct defence coordinate release that conflict,
   and which relief / interference / joint-cost channels explain it?
```

SCH establishes the functional constraint that motivates an additional defence coordinate. BITA then separates the outcome question from the mechanism-allocation question for `A x D`.

Evidence may be shared as provenance and biological grounding, but estimands must not be exchanged between repositories.

## 12. Current claim ceiling

The current literature and source-audit spine supports the following positive statement:

> Floral attraction traits operate in a real multi-audience world: pollinator and antagonist routes recur, opposing biotic effects can generate compromise and evolutionary redirection, and partial signal decoupling occurs through multiple mechanisms. What the literature rarely supplies is the complete same-coordinate selective intervention needed to identify how much pollinator gain and antagonist loss jointly determine the reproductive value of attraction. SCH therefore turns that biological recurrence into an explicit 8-cell mechanism experiment, with BITA as the subsequent test of defence-mediated escape.

Until a complete experiment is executed or fully recovered, the machine-readable conceptual status is:

```text
REAL_WORLD_MECHANISM_COMPONENTS_RECOVERED
COMPLETE_SCH_CHANNEL_IDENTIFICATION_NOT_YET_EXECUTED
HISTORICAL_SHARED_TO_PRIVATE_TRANSITION_NOT_YET_IDENTIFIED
```
