# SCH macroecology H2 estimand-homogeneity gate V1

## Why the V5 structural gate is not sufficient

After Erysimum, the broad H2 bookkeeping layer contains:

~~~text
44 local cases
14 canonical axes
8 total H2 clusters

37 plant-performance-labelled cases
11 plant-performance axes
6 plant-performance clusters
~~~

The V5 gate therefore correctly identified independent-cluster breadth as the last broad structural blocker.

However, the 37 plant-performance-labelled cases are not one statistical estimand.

They contain three different measurement layers:

~~~text
LOCAL_GEOMETRY
LOCAL_NET_SELECTION
LOCAL_ANTAGONIST_PRESSURE
~~~

These layers answer different biological questions and cannot be pooled as one numeric response.

## Current estimand decomposition

### LOCAL_GEOMETRY

~~~text
cases = 2
axes = 2
clusters = 2
repeated axes = 0
~~~

Current systems are Gentiana colour and Caryopteris corolla tube under natural robbery.

### LOCAL_NET_SELECTION

~~~text
cases = 31
axes = 9
clusters = 4
repeated axes = 8
~~~

Current clusters are Caryopteris, Gymnadenia, Trifolium and Erysimum.

This is the only current H2 layer with enough rows, axes and within-axis replication to be a plausible basis for a quantitative comparative model.

Its remaining structural blocker is independent-cluster breadth:

~~~text
required clusters = 8
current clusters  = 4
~~~

Thus the current comparable-layer target is +4 independent LOCAL_NET_SELECTION clusters, not merely +2 broad plant-performance clusters.

### LOCAL_ANTAGONIST_PRESSURE

~~~text
cases = 4
axes = 1
clusters = 1
repeated axes = 1
~~~

Current system is Pedicularis seed-predation pressure.

These cases quantify antagonist pressure, not trait selection geometry.

## Numeric effect metrics remain heterogeneous inside LOCAL_NET_SELECTION

Even LOCAL_NET_SELECTION is not yet a common numeric effect-size family.

~~~text
PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA
  8 cases
  2 axes
  1 cluster
  Gymnadenia

STANDARDIZED_LINEAR_SELECTION_GRADIENT_BETA
  4 cases
  2 axes
  1 cluster
  Trifolium

SEM_TOTAL_DIRECT_SELECTION_PATH_COEFFICIENT
  18 cases
  4 axes
  1 cluster
  Erysimum

DIRECTIONAL_GROUP_COMPARISON
  1 case
  1 axis
  1 cluster
  Caryopteris
~~~

No exact effect-metric family currently has cross-system replication.

Therefore a numeric meta-regression on raw coefficients is not licensed even if four more LOCAL_NET_SELECTION clusters are added using different effect metrics.

## Corrected H2 modelability statement

The previous broad statement:

~~~text
two more plant-performance clusters
-> registered cluster-count gate passes
~~~

remains true only for the broad bookkeeping layer.

It is not sufficient for a primary numeric H2 model.

The estimand-aware statement is:

> A primary H2 model requires either a genuinely repeated common effect metric across independent systems, or a prospectively frozen scale-free state representation defined before additional systems are admitted.

Current status:

~~~text
BROAD_STRUCTURAL_H2 = NEAR_GATE
NUMERIC_H2_EFFECT_MODEL = FAIL_CLOSED
ESTIMAND_HOMOGENEITY = FAIL_CLOSED
~~~

## Prospective scale-free route

A possible route is a directional state model that deliberately discards effect-size magnitude.

The mapping is frozen before new clusters are admitted.

Eligible source rows:

~~~text
measurement layer = LOCAL_NET_SELECTION
signed local effect available
source reports uncertainty / significance state
~~~

Candidate states:

~~~text
SUPPORTED_POSITIVE
SUPPORTED_NEGATIVE
NO_SUPPORTED_DIRECTION
UNCLASSIFIED
~~~

NO_SUPPORTED_DIRECTION is not interpreted as biological zero.

At the canonical-axis level, repeated contexts can then be described as stable positive, stable negative, hotspot/coldspot, or supported sign switch.

This is a different estimand from raw effect size and must be analysed separately.

## Current publication consequence

The ecological synthesis remains valid:

> ecological context can change the realized state of selection on the same trait axis.

What remains fail-closed is the attempt to reduce those heterogeneous states to one general numeric moderator model.

This strengthens SCH because the same identification discipline is being applied to the macroecology layer itself.

## Status

~~~text
H2_BROAD_PLANT_PERFORMANCE_CASES = 37
H2_BROAD_PLANT_PERFORMANCE_CLUSTERS = 6

H2_LOCAL_NET_SELECTION_CASES = 31
H2_LOCAL_NET_SELECTION_AXES = 9
H2_LOCAL_NET_SELECTION_CLUSTERS = 4
H2_LOCAL_NET_SELECTION_REPEATED_AXES = 8

MAX_CLUSTERS_IN_ONE_EXACT_NUMERIC_METRIC_FAMILY = 1

H2_PRIMARY_NUMERIC_MODEL = FAIL_CLOSED
H2_ESTIMAND_HOMOGENEITY = FAIL_CLOSED
~~~
