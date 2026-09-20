# SCH macroecology H2 measurement layers and change types V1

## Current H2 local-case architecture

The H2 layer now contains eighteen materialized local cases, but they belong to two different biological measurement families.

```text
TOTAL_H2_LOCAL_CASES = 18

PLANT_PERFORMANCE_CASES = 11
ROLE_BEHAVIOR_CASES = 7
```

These counts must not be pooled as if they were ten equivalent geometry observations.

## Plant-performance measurement layer

Eight measurement records across six canonical axes are tracked in:

`data/SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V1.csv`

The ordered information states are:

```text
LOCAL_GEOMETRY
LOCAL_NET_SELECTION
LOCAL_ANTAGONIST_PRESSURE
CONTEXT_STRUCTURE_ONLY
```

Source-supported states:

```text
LOCAL_GEOMETRY              3
LOCAL_NET_SELECTION         4
LOCAL_ANTAGONIST_PRESSURE   1
```

Currently materialized states:

```text
LOCAL_GEOMETRY              2
LOCAL_NET_SELECTION         3
CONTEXT_STRUCTURE_ONLY      3
```

Three of eight records therefore remain below the resolution that the underlying source could in principle support.

The eleven materialized plant-performance cases are:

1. *Gentiana lutea* colour at Torrestío — `LOCAL_GEOMETRY`;
2. *Caryopteris divaricata* with natural nectar robbery — `LOCAL_GEOMETRY`;
3. *Caryopteris divaricata* under robber exclusion — `LOCAL_NET_SELECTION`;
4–7. *Gymnadenia conopsea* flowering phenology in four pollination × herbivory treatment cells — `LOCAL_NET_SELECTION`;
8–11. *Gymnadenia conopsea* spur length in the same four treatment cells — `LOCAL_NET_SELECTION`.

## Visitor-role behavior layer

Seven additional local cases are source-resolved at the level of visitor role or foraging tactic rather than plant-fitness geometry.

They are:

```text
Blueberry:
  Duke
  Bluecrop

Sesame corolla access:
  normal corolla
  short tube without landing space
  short tube with landing space

Sesame resource state:
  low-resource control
  high nectar + high pollen
```

These cases are real local H2 observations, but their local reproductive endpoint is absent or programme-level.

They are therefore coded as:

```text
ROLE_BEHAVIOR_CONTEXT
```

rather than conflict, alignment, or one-sided plant-fitness geometry.

## Pedicularis linkage boundary

The source structure is now explicit:

```text
pollination/floral contexts                     14 populations
seed outcome / predation contexts               12 populations
same-individual linkage                          7 populations
local two-function geometry cases materialized   0
```

Same-individual linkage is retained in populations:

```text
1, 3, 5, 8, 9, 10, 11
```

Labels were lost in populations:

```text
2, 4, 6, 7, 12
```

Those five populations can support local antagonist pressure, not individual-level shared-trait geometry.

Thus:

```text
LOCAL_ANTAGONIST_PRESSURE
!=
LOCAL_GEOMETRY
```

## Pending source objects

Six plant-performance source objects are registered:

```text
Gentiana_S3
Gymnadenia_A2  [Table A2 values extracted]
Pedicularis_S1
Pedicularis_S2
Pedicularis_AppendixS1
Primula_program_sources
```

Current state:

```text
binary materialized                 0
exact local values extracted        1
```

The registry therefore raises provenance without inflating local model N.

## Ecological change types

The H2 change seed now contains seven canonical-axis change records accounting for all ten materialized local cases.

### Geometry-class switch

*Gentiana lutea* colour:

```text
focal population -> reinforcement
broader spatial source -> one-sided / null with heterogeneous pollinator selection
```

### Geometry disappearance

*Caryopteris divaricata* corolla tube:

```text
robbers present -> short-tube realized advantage
robbers excluded -> no detected tube-length effect
```

### Component-weight shift

*Pedicularis rex*:

```text
overall conflict retained
pollinator component comparatively stable
seed-predator component varies geographically
```

### Component-weight shift with evolutionary response

*Primula farinosa*:

```text
pollinator-grazer balance varies
-> selection changes
-> morph-frequency evolution follows
```

### Consumer-role behavior shift

Three canonical-axis records represent local behavioral switching:

- blueberry corolla-access geometry;
- sesame corolla access;
- sesame nectar/resource state.

These are not relabelled as plant-fitness geometry.

## Change-type seed status

```text
CHANGE_RECORDS = 9
CANONICAL_AXES = 9

GEOMETRY_CLASS_SWITCH = 1
GEOMETRY_DISAPPEARANCE = 1
COMPONENT_WEIGHT_SHIFT = 1
COMPONENT_WEIGHT_SHIFT_WITH_EVOLUTIONARY_RESPONSE = 1
CONSUMER_ROLE_BEHAVIOR_SHIFT = 3
NET_SELECTION_CONTEXT_SHIFT = 2

MATERIALIZED_LOCAL_CASES_REPRESENTED = 18
CHANGE_RECORDS_WITH_LOCAL_CASES = 7
CHANGE_RECORDS_WITHOUT_LOCAL_CASES = 2
```

The two source-level change records still lacking materialized local rows are *Pedicularis* and *Primula farinosa*.

## Main ecological implication

The H2 layer now rejects a single binary notion of “context dependence.”

At least five different processes are already distinguishable:

```text
context dependence
  ├─ geometry class switch
  ├─ geometry disappearance
  ├─ component-weight shift
  ├─ component-weight shift with evolutionary response
  └─ consumer-role behavior shift
```

This supports a stronger ecological interpretation:

> Context can alter not only the magnitude or sign of selection, but the very type of functional relationship realized between a trait and its interacting consumers.

## Inference boundary

Current status:

```text
H2_LOCAL_CASES = 18
PLANT_PERFORMANCE_CASES = 11
ROLE_BEHAVIOR_CASES = 7

PLANT_PERFORMANCE_AXES_WITH_CASES = 2
ROLE_BEHAVIOR_AXES_WITH_CASES = 3

H2_MODEL = NOT READY
H2_PREVALENCE = NOT ESTIMATED
```

Plant-performance and role-behavior cases remain separate analysis layers.

The next gains should come from recovering local plant-performance values for:

1. *Gentiana* S3;
2. *Pedicularis* S1/S2/Appendix S1;
3. *Primula farinosa* experiment/time tables.
