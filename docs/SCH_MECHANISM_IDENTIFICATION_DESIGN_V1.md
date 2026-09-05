# SCH mechanism-identification design v1

## Scientific target

SCH is the one-trait mechanism chapter in the SCH -> BITA programme. It asks whether one declared floral attraction/display coordinate `A` creates a functional conflict because pollinators and antagonists act on that same coordinate, and whether that conflict measurably constrains the reproductive effect of attraction.

The primary contribution is not a literature count. The primary contribution is an identification design that can distinguish:

1. pollinator-mediated gain from changing `A`;
2. antagonist-mediated loss from changing the same `A`;
3. the consumer-independent remainder of the `A` manipulation;
4. dependence between the pollinator and antagonist channels.

The literature programme remains essential, but its role is to establish that the proposed routes, conflicts and evolutionary consequences occur in real biological systems and to show which identifying measurements are usually missing.

## Core 8-cell design

Use a crossed

```text
A x antagonist x pollinator
```

factorial with two declared levels of each factor.

```text
A = 0, 1
G = antagonist suppressed/absent, natural/present
P = pollinator suppressed/absent, natural/present
```

The eight cells measure one common plant reproductive outcome `W` on the same experimental scale.

Write

```text
W[a,g,p] = expected reproductive outcome
```

and define the attraction contrast in each consumer state as

```text
d[g,p] = W[1,g,p] - W[0,g,p].
```

The natural-community attraction effect is

```text
Delta_A W_natural = d[1,1].
```

This total effect alone does not identify why attraction helps, fails or harms the plant.

## Channel contrasts

### Pollinator-mediated contribution

At fixed antagonist state `g`, define

```text
M_A(g) = d[g,1] - d[g,0].
```

A positive `M_A(g)` means that pollinator access makes the reproductive effect of increasing `A` more positive on the declared outcome scale.

### Antagonist-mediated loss

At fixed pollinator state `p`, define

```text
G_A(p) = d[0,p] - d[1,p].
```

A positive `G_A(p)` means that antagonist presence erodes the reproductive effect of increasing `A`; it is therefore a loss term rather than a raw antagonist visitation coefficient.

### Consumer-independent attraction remainder

Define

```text
B_A = d[0,0].
```

`B_A` is the effect of the attraction manipulation when both focal consumer routes are suppressed. It may contain construction cost, physiological pleiotropy, autonomous reproduction effects or other pathways. It must remain an unallocated remainder unless an independent assay justifies a narrower interpretation.

If an independent construction/physiological-cost assay supports

```text
B_A = -C_A,
```

then `C_A` may be reported as a direct attraction cost. Without that assay, SCH must not silently rename `B_A` as `-C_A`.

## Channel-dependence diagnostic

The consumer channels need not be separable. Define

```text
J_A = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

This is the `A x G x P` interaction on the declared reproductive scale. It is equivalently

```text
J_A = M_A(1) - M_A(0)
    = -(G_A(1) - G_A(0)).
```

Thus the same contrast tests whether the pollinator contribution depends on antagonist state and whether the antagonist loss depends on pollinator state.

A non-zero `J_A` rejects the simplest additive-channel representation. SCH should then report state-specific channel contrasts rather than forcing one universal `M_A` and `G_A`.

For bookkeeping around the consumer-free baseline,

```text
d[1,1] = B_A + M_A(0) - G_A(0) + J_A.
```

This identity is descriptive. Biological interpretation of each term still requires selective interventions and stable `A` coordinates across cells.

## What counts as a shared-cue mechanism result

A strong SCH mechanism claim requires two linked evidence layers.

### Informational layer: same-coordinate receiver use

The manipulated `A` coordinate must be biologically validated as the same sensory or display coordinate presented to both receiver classes. Suitable evidence includes paired behavioural assays, receptor/choice assays, or a manipulation whose physical/chemical coordinate is demonstrably invariant across consumer treatments.

Visitor labels alone do not prove cue sharing.

### Functional layer: opposing reproductive channels

On the same `A` coordinate and a common reproductive outcome, the selective crossed design should support

```text
M_A(g) > 0
```

for at least one predeclared antagonist state and

```text
G_A(p) > 0
```

for at least one predeclared pollinator state, with uncertainty compatible with the intended directional claims.

The strongest one-trait conflict result is not merely `pollinator response > 0` and `antagonist response > 0`. It is that pollinator access increases the reproductive value of `A` while antagonist access decreases it.

## Constraint claim

The functional constraint is a contrast between attraction effects with and without antagonists.

For example, under natural pollinator access,

```text
G_A(1) = d[0,1] - d[1,1].
```

If `G_A(1) > 0`, antagonists flatten the attraction-fitness slope relative to the antagonist-free state. Stronger forms are:

```text
constraint attenuation:
0 < d[1,1] < d[0,1]

constraint release under antagonist removal:
d[1,1] <= 0 < d[0,1]

strict sign reversal under antagonist removal:
d[1,1] < 0 < d[0,1].
```

These claims concern reproductive consequences, not historical evolution of cue privacy.

## Inference ladder

SCH should keep the following levels separate.

```text
Level 0  same-coordinate receiver response
         pollinator and antagonist both detect/respond to A

Level 1  paired functional conflict
         pollinator-mediated gain and antagonist-mediated loss
         are both identified on the same A contrast

Level 2  realized constraint
         antagonist presence measurably flattens or reverses
         the reproductive effect of attraction

Level 3  mechanism-resolved one-trait conflict
         selective 8-cell decomposition + consumer-independent
         remainder + channel-dependence diagnostic

Level 4  evolutionary consequence
         repeated A levels / selection surface / experimental evolution
         shows compromise, divergence, polymorphism or decoupling

Level 5  historical architectural transition
         ancestral shared cue -> private/separable cue reconstructed
         under both receiver channels
```

Evidence at one level must not be promoted to the next by interpretation alone.

## Minimum experimental contract

1. Predeclare one biologically interpretable `A` coordinate and maintain it across all cells.
2. Validate that consumer suppression/exclusion is selective enough for the intended channel interpretation.
3. Measure the same reproductive outcome in all eight cells.
4. Retain plant, block, day, population and repeated-measure structure in the uncertainty model.
5. Report `d[g,p]`, `M_A(g)`, `G_A(p)`, `B_A` and `J_A` with compatible uncertainty.
6. Do not call `B_A` a direct cost without an independent assay.
7. Pair the reproductive experiment with a same-coordinate receiver assay when the claim is specifically about shared cues rather than generic opposing selection.
8. Power directional channel claims and equivalence/nonresponse claims separately; failure to detect antagonist response is not evidence for a private cue.

## Staged implementation

```text
Stage 0  validate A and receiver access
         same physical/chemical/display coordinate; manipulation checks

Stage 1  pilot the 8-cell reproductive design
         estimate d[g,p], channel magnitudes, variance and clustering

Stage 2  re-power and execute the confirmatory 8-cell design
         test paired functional conflict and realized constraint

Stage 3  independent remainder/cost assay
         decide whether B_A can be allocated to construction or physiology

Stage 4  evolutionary extension
         multiple A levels, population contrasts or experimental evolution
         to estimate the shape and consequences of the conflict
```

The pilot must determine mechanism-scale effect sizes. A literature-derived visitor effect or a total attraction effect must not be reused as the power effect for a channel interaction without justification.

## Role of the literature evidence

The systematic and targeted source audits are retained as a **real-world mechanism evidence layer**.

They serve four purposes.

1. **Route reality.** Existing studies show that floral attraction/display traits can alter pollination and antagonist exposure, so the two channels are biologically recurrent rather than hypothetical.
2. **Outcome reality.** Existing systems recover stabilizing compromise, polymorphism maintenance, population-level evolutionary change and partial cue decoupling, showing that dual-audience conflict can have evolutionary consequences.
3. **Design-gap localization.** The sparse strict linked set shows that manipulation, both consumer responses and a common plant outcome are rarely measured together; this motivates the 8-cell design rather than substituting for it.
4. **Historical extension.** Ficus and other transition candidates identify where shared/private architecture might be reconstructed after contemporary mechanism states are measured on matched coordinates.

The literature layer does **not** by itself estimate the SCH channel effects, prove prevalence, or substitute cross-study coherence for a complete mechanism experiment.

## Relationship to BITA

SCH is Chapter 1. BITA is Chapter 2.

```text
SCH
A x antagonist x pollinator
8 cells
-> identify why one attraction coordinate is conflicted

BITA
A x D x antagonist x pollinator
16 cells
-> identify whether a distinct defence coordinate releases that conflict
   and which relief/interference/joint-cost channels explain the outcome
```

SCH therefore establishes the constraint that motivates `D`; BITA tests a functional escape route from that constraint. The chapters share biological logic but not estimands.

## Claim ceiling before new data

Current literature and source-audit evidence establishes that the constituent routes and several evolutionary outcomes occur in nature, and that complete linked measurement is rare. It does not yet provide SCH's own mechanism-resolved 8-cell estimate.

Until a new or fully recoverable complete experiment is available, the correct status is:

```text
REAL_WORLD_MECHANISM_COMPONENTS_RECOVERED
COMPLETE_SCH_CHANNEL_IDENTIFICATION_NOT_YET_EXECUTED
```
