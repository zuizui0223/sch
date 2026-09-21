# SCH macroecology H2 modelability gate V6

## Milestone

The broad plant-performance H2 layer now passes the original structural breadth gate.

~~~text
TOTAL_H2_LOCAL_CASES = 49

PLANT_PERFORMANCE_CASES = 42
PLANT_PERFORMANCE_AXES = 14
PLANT_PERFORMANCE_CLUSTERS = 8
PLANT_PERFORMANCE_REPEATED_AXES = 11
~~~

Registered breadth thresholds:

~~~text
minimum cases          12
minimum axes            8
minimum clusters        8
minimum repeated axes   5
~~~

Therefore:

BROAD_PLANT_PERFORMANCE_STRUCTURAL_GATE = PASS

This does not make the primary H2 numeric model ready.

## Why the old gate is no longer sufficient

The plant-performance layer contains multiple non-equivalent estimands.

~~~text
LOCAL_TWO_FUNCTION_GEOMETRY
  2 cases / 2 axes / 2 clusters

TOTAL_SELECTION_EFFECT
  30 cases / 8 axes / 3 clusters

REALIZED_NET_PERFORMANCE
  1 case / 1 axis / 1 cluster

ANTAGONIST_PRESSURE
  4 cases / 1 axis / 1 cluster

REPRODUCTIVE_COMPONENT_EFFECT
  3 cases / 1 axis / 1 cluster

REPRODUCTIVE_PERFORMANCE_PROXY
  2 cases / 2 axes / 1 cluster
~~~

No single estimand family reaches the registered breadth thresholds.

## Numeric pooling families

Even inside TOTAL_SELECTION_EFFECT, the effect metrics are not all numerically identical.

~~~text
STANDARDIZED_SELECTION_GRADIENT
  12 cases
  4 axes
  2 clusters

TOTAL_SELECTION_PATH_COEFFICIENT
  18 cases
  4 axes
  1 cluster
~~~

Thus:

~~~text
COMMENSURATE_ESTIMAND_FAMILY_MODEL = FAIL
COMMENSURATE_NUMERIC_POOLING_MODEL = FAIL
~~~

## Revised gate architecture

### Gate A — ecological breadth

Asks whether the comparative evidence spans enough independent contexts, axes and systems.

Current result: PASS.

### Gate B — estimand harmonization

Asks whether one biologically comparable quantity is represented across enough independent systems.

Current result: FAIL.

The primary H2 status is therefore:

BREADTH_GATE_PASS_ESTIMAND_HARMONIZATION_FAIL

## Why this is better than the old gate

Without Gate B, adding antagonist pressure, germination proxy and standardized selection gradients could mechanically trigger a mixed model.

That would create statistical precision by combining different biological quantities.

The revised gate prevents that failure mode.

## Current ecological contribution

The broad comparative layer is now large enough to support a descriptive ecological result across independent systems, including context-dependent total selection, geometry disappearance, local two-function geometry, antagonist-pressure mosaics, reproductive-component differences, performance-proxy differences and consumer-role shifts.

But the quantities are not interchangeable.

> Context dependence is recovered across independent systems, but it is expressed through several distinct ecological estimands rather than one universal effect size.

## Next quantitative target

The most valuable target is now TOTAL_SELECTION_EFFECT.

Current independent clusters:

1. *Gymnadenia conopsea*
2. *Trifolium repens*
3. *Erysimum mediohispanicum*

High-value pending routes remain:

- Gentiana S3 population selection table
- Primula farinosa Table S2 / exact local selection rows
- other source-audited fixed-role systems with directly extractable total-selection effects

## Status

~~~text
H2_BROAD_BREADTH_GATE = PASS

H2_COMMENSURATE_ESTIMAND_GATE = FAIL
H2_COMMENSURATE_NUMERIC_POOLING_GATE = FAIL

PRIMARY_H2_NUMERIC_MODEL = FAIL_CLOSED
PRIMARY_H2_OUTPUT = DESCRIPTIVE_COMPARATIVE_MECHANISM_SYNTHESIS
~~~
