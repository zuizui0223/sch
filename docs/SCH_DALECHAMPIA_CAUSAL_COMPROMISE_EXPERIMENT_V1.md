# SCH Dalechampia causal compromise experiment v1

## Decision

*Dalechampia* is the first-choice system for a direct Chapter-1 test of **shared-trait compromise geometry** because the literature already supplies three unusually valuable pieces:

1. larger showy bracts increase pollinator visitation and pollen arrival;
2. the same bract axis increases predispersal seed-predator exposure and the combined selection surface tends toward stabilizing selection;
3. experimental reduction of bract size in *Dalechampia ipomoeifolia* reduces pollen arrival, showing that the advertisement axis is manipulable rather than purely observational.

The missing object is not another correlational selection analysis. It is a causal multi-level experiment that identifies

```text
z1*   pollination-function optimum
z2*   antagonist-avoidance optimum
zc*   combined shared-trait optimum
```

and then verifies that changing the weight of either function moves the combined optimum in the predicted direction.

## Trait and functions

Primary shared trait:

```text
z = apparent involucral-bract display area during the receptive / pollinator-choice window
```

Primary functions:

```text
F1 = pollinator-mediated pollen transfer / reproductive gain
F2 = avoidance of predispersal seed-predator loss
```

The natural-history anchor is the *D. scandens* population in Pérez-Barrales et al. 2013, where larger bracts increased bee visitation and pollen arrival while also increasing seed-predator attack, yielding a net tendency toward stabilizing selection.

## Critical manipulation problem

Permanent bract clipping is **not** the preferred confirmatory manipulation when mature seeds are the common outcome.

Later in *D. scandens* development, involucral bracts turn green and contribute photosynthate to developing seeds. Permanent removal or shading after pollination lowers seed mass. Therefore a permanent size reduction can create a direct carbon / construction pathway that is not part of the pollinator-versus-seed-predator conflict.

The confirmatory manipulation must therefore alter the **display coordinate during the ecological decision window** while preserving post-pollination bract tissue and function.

## Stage 0A — reversible apparent-size manipulation

Develop a reversible display manipulation before the full factorial.

Preferred candidate:

```text
natural bract tissue remains intact
+
removable, spectrally matched occluders for downward display shifts
+
removable, spectrally matched artificial extensions for upward display shifts
```

A five-level initial target is:

```text
z = 0.60, 0.80, 1.00, 1.20, 1.40 x the standardized reference apparent area
```

These are planning levels, not frozen biological doses. Stage 0 must revise them if they exceed the natural or behaviourally relevant range.

Promotion checks:

```text
Z0.1 apparent area is changed as intended
Z0.2 visible / UV reflectance is matched closely enough that area, not colour, is the dominant changed coordinate
Z0.3 gland visibility and access are unchanged
Z0.4 resin amount / gland size are unchanged
Z0.5 bract posture and blossom geometry are not mechanically distorted
Z0.6 manipulations can be removed after the ecological exposure window without lasting tissue damage
Z0.7 sham material controls do not alter visitation, oviposition or seed development
```

If upward artificial extension cannot be made biologically credible, do not pretend a five-level causal surface exists. Use a bounded lower-side perturbation experiment plus natural-trait surface as separate evidence layers.

## Stage 0B — selective functional interventions

The causal compromise claim requires changing the weight of pollination and seed-predator functions without changing `z` itself.

### Pollinator intervention candidates

```text
P1 = natural pollinator access during the receptive window
P0 = pollinator exclusion during that window
```

Because *D. scandens* can produce seeds by autonomous self-pollination, `P0` is not assumed to imply zero reproduction. The consumer-independent / autonomous baseline is measured rather than set to zero.

A hand-pollinated calibration arm should be retained to map pollen load to seed production independently of pollinator choice.

### Seed-predator intervention candidates

The seed predators in the focal *D. scandens* work are small curculionid weevils; most feeding is visible later in developing seeds, while oviposition is presumed earlier. The exact selective intervention is therefore **not yet frozen**.

Candidate routes to pilot are:

```text
G1 = natural seed-predator access
G0 candidate A = selective adult-weevil exclusion during the oviposition window
G0 candidate B = post-oviposition egg / early-stage removal if eggs can be detected and removed without blossom damage
G0 candidate C = highly focal barrier around the oviposition target after the pollinator window, only if timing is shown to separate the routes
```

Broad bagging or insecticide is not accepted as `G0` unless manipulation checks show that pollinator access, bract optical state, resin reward and blossom microclimate remain unchanged.

### Selectivity gate

Before a confirmatory compromise experiment, demonstrate:

```text
P manipulation changes pollen delivery / visitation strongly
but does not directly change G exposure or z

G manipulation changes seed-predator establishment / loss strongly
but does not directly change pollination or z
```

If the two functional routes cannot be separated adequately in this system, Dalechampia remains a strong real-world compromise anchor but is not used for a mechanism-resolved L3 claim.

## Stage 1 — five-level local surface pilot

After Stage 0 passes, use a balanced factorial:

```text
5 z levels x 2 pollinator states x 2 seed-predator states
= 20 cells
```

Randomize treatment within plant / patch as far as biology permits. Preserve at least:

```text
plant / genotype
patch
blossom
calendar date
female vs bisexual exposure day
z target and measured apparent area
pollinator treatment
seed-predator treatment
sham / manipulation batch
```

Primary common fitness endpoint:

```text
number of mature intact viable seeds per focal blossom
```

Secondary decomposition:

```text
bee visitation / visit probability
stigmatic pollen load
fruit set
fertilized seed number before predation where measurable
predated seed number
intact seed number
seed mass / viability
```

The primary outcome is deliberately downstream of both functions. Visitor counts and predator occurrence are mediators, not substitutes for `W`.

## Function-specific surfaces

The pilot estimates state-specific response surfaces rather than forcing a single additive curve.

At each `z`, estimate:

```text
W(z, G, P)
```

and derive pollinator-mediated contribution and predator-mediated loss analogues over the continuous / multi-level trait axis.

The simplest target surfaces are:

```text
F1(z)  pollinator-mediated reproductive contribution
F2(z)  predator-avoidance / surviving-seed contribution
W(z)   combined mature-intact-seed fitness
```

Use smooth curves or low-order polynomial models only after checking that the five-level data support the chosen shape. The quadratic bridge is a local benchmark, not a mandatory global model.

## Primary Chapter-1 decisions

### C1 — multifunctionality

```text
z changes both functional routes
```

### C2 — conflict

```text
z1* != z2*
```

with uncertainty showing biologically meaningful separation of the function-specific preferred states.

### C3 — shared compromise

```text
zc* lies between the function-specific optima in the predeclared trait orientation
```

with the combined surface showing an interior optimum or a bounded balancing region.

### C4 — causal optimum shift

This is the decisive test.

```text
weaken / remove seed-predator function
-> combined optimum moves toward z1*

weaken / remove pollinator function
-> combined optimum moves toward z2*
```

The effect is reported as an optimum displacement with uncertainty, not only a treatment p-value.

### C5 — gradient cancellation

Near `zc*`, the total gradient is approximately zero while the two function-specific marginal gradients are non-zero and oppose one another.

This distinguishes a true balance from a flat, weak-selection surface.

## Negative-control logic

A multifunctional trait is not automatically a compromise. The programme explicitly retains aligned-optima examples such as flower orientation systems in which pollination and abiotic protection favor the same state.

Therefore the Dalechampia experiment fails the positive compromise hypothesis if the estimated functional optima overlap substantially, even if both functions respond strongly to bract display.

## Direct-cost control

Because bracts have post-pollination carbon functions, direct manipulation costs receive a dedicated check.

After all temporary display materials are removed, compare sham and manipulated blossoms under standardized hand pollination and predator exclusion. Any persistent difference in seed mass, viability or seed number is treated as a direct manipulation / bract-function pathway rather than silently allocated to pollination or predation.

## Pilot size and power policy

Do **not** power the final experiment from the published observational stabilizing-selection coefficient or from the experimental bract-reduction pollen effect in another *Dalechampia* species.

Stage 1 must estimate:

```text
within-plant and within-patch variance
cell retention
pollinator visit probability
pollen-load dispersion
seed-predation incidence
mature-intact-seed variance
curvature / optimum uncertainty
cross-route contamination of P and G interventions
```

The confirmatory sample size is then determined by simulation for the predeclared decisions C2-C5, especially confidence in optimum separation and optimum displacement. Power for a single `z x treatment` coefficient is not an adequate substitute.

## Relationship to the existing literature

The experiment closes a very specific gap between already established results.

- Pérez-Barrales et al. 2013: real-world opposing pollinator and seed-predator selection plus net stabilizing tendency on *D. scandens* bract size.
- Armbruster et al. 2005: experimental reduction of *D. ipomoeifolia* bract size lowers pollen arrival, establishing causal manipulability of the advertisement axis.
- Pélabon et al. 2015: post-pollination bracts contribute carbon to developing seeds, establishing why permanent clipping is a confounded common-fitness manipulation.

The new experiment therefore does not ask whether Dalechampia has an interesting trade-off. It asks whether the observed balance can be **causally reconstructed as two function-specific optima competing on one shared coordinate**.

## Handoff to BITA

If C2-C5 are recovered, Chapter 1 delivers an identified one-dimensional compromise:

```text
z1*, z2*, zc*, compromise penalty / displacement
```

BITA then asks whether a second functional coordinate can reduce that penalty. The strongest cross-chapter prediction is not simply a positive two-trait interaction; it is that the first trait's optimum is released toward its function-specific optimum when the second coordinate carries more of the competing function.

## Current status

```text
REAL_WORLD_OPPOSING_SELECTION: RECOVERED
OBSERVATIONAL_STABILIZING_COMPROMISE: RECOVERED_CASE_LEVEL
BRact_ADVERTISEMENT_MANIPULABILITY: RECOVERED_IN_GENUS
PERMANENT_BRact_REMOVAL_COMMON_W_CONFOUND: RECOVERED
REVERSIBLE_MULTI_LEVEL_Z_MANIPULATION: TO_VALIDATE
SELECTIVE_P_INTERVENTION: TO_VALIDATE
SELECTIVE_G_INTERVENTION: TO_VALIDATE / MAIN BOTTLENECK
CAUSAL_Z1_Z2_ZC_RECOVERY: NOT_YET_EXECUTED
```
