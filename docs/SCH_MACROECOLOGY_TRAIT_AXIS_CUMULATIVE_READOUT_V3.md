# SCH macroecology cumulative trait-axis readout V3

## Current staged ecological layer

After four source-verified trait-axis batches:

```text
source records                     22
independent biological clusters   20
trait axes                         38

fixed-role axes                    29
consumer-role boundary axes         9
```

Fifteen fixed-role axes across eleven biological clusters are currently resolved enough to classify their ecological geometry:

```text
CONFLICT / OPPOSITION              9
ALIGNMENT / REINFORCEMENT         3
ONE-SIDED OR NULL                 3
```

These counts describe the staged recode only. They are not estimates of prevalence in nature or in the final systematic sample.

## Multi-axis studies add real biological information

The new batch confirms that multi-trait studies cannot be represented by one paper-level label.

### Castilleja linariaefolia

The source examines calyx length, flower production and plant height through pollination and pre-dispersal seed-predation pathways.

Only **calyx length** is explicitly reported to experience opposing selection.

```text
calyx length       -> conflict identified
flower production  -> component geometry unresolved
plant height       -> component geometry unresolved
```

The latter two remain in the dataset rather than inheriting the calyx result from the paper-level summary.

### Collaea cipoensis

Both declared attractiveness axes resolve as conflict:

```text
flower size:
  pollinators favor larger flowers
  antagonists favor smaller flowers

flower number:
  pollinators favor more flowers
  antagonists favor fewer flowers
```

Antagonist attack reduces the female-fitness component, converting shared attraction into an opposing fitness contribution.

### Pedicularis rex

Two floral axes independently recover conflict:

```text
corolla exsertion:
  pollen arrival ↑ with exsertion
  seed predation ↑ with exsertion

lower-lip width:
  pollen arrival ↑ with width
  seed predation ↑ with width
```

Because seed predation lowers viable seed production, both traits receive pollinator-mediated selection toward larger/more exposed states and seed-predator-mediated selection toward reduced states.

The geographic component is strongest for corolla exsertion: seed-predator-mediated selection varies among populations while the pollination component is more geographically consistent. Lower-lip conflict is retained without automatically inheriting that trait-specific context shift.

## What the resolved set now demonstrates

The staged evidence contains all of the following on declared trait axes:

1. **opposition** — nine axes;
2. **reinforcement** — three axes;
3. **one-sided/null geometry** — three axes;
4. **cancellation** — at least one resolved axis;
5. **role-dependent or benefit-cost-coupled consumers** — nine boundary axes;
6. **source-level downgrades** where apparent relevance does not survive same-axis/component attribution.

This is the empirical extension of the SCH inference ladder: the literature does not merely contain more or less conflict. It contains qualitatively different ecological geometries that become visible only after the trait coordinate and consumer role are declared.

## Emerging ecological model

The current working biological statement is:

> **The effect of multifunctionality is assembled at trait axis × ecological context × consumer role, rather than being a fixed property of a species, a paper, or even a mutualist-antagonist system.**

The eventual macro models will test narrower versions of this statement after all design-eligible records are decomposed and clustered.

## Remaining bottleneck

The current P1 frontier contains 32 record-level H1 candidates. Twenty-two source records have now contributed to the trait-axis ledger, but several candidate papers still require multi-axis decomposition.

The next priority is therefore not discovering more examples. It is finishing trait-axis extraction for the remaining P1/H1 records and clustering overlapping research programmes before fitting any moderator model.

## Claim ceiling

```text
TRAIT_AXES_RECODED = 38
BIOLOGICAL_CLUSTERS = 20
FIXED_ROLE_RESOLVED_AXES = 15
FIXED_ROLE_RESOLVED_CLUSTERS = 11

CONFLICT_AXES = 9
REINFORCEMENT_AXES = 3
ONE_SIDED_AXES = 3

CONSUMER_ROLE_BOUNDARY_AXES = 9
RESOLVED_CONTEXT_SHIFT_AXES = 5
CANCELLATION_AXES = 1

CONFLICT_PREVALENCE = NOT_ESTIMATED
H1_H2_H3_MODELS = NOT_FIT
FULL_MACRO_INFERENCE = CLOSED
```
