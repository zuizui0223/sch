# SCH macroecology H2 modelability gate V6

## Estimand-aware correction

The V5 structural gate is useful but not sufficient.

Current broad H2 state:

~~~text
local cases = 44
plant-performance-labelled cases = 37
broad plant-performance clusters = 6
~~~

At that level, two additional plant-performance clusters would satisfy the registered eight-cluster count.

However, the 37 cases combine three different estimands.

~~~text
LOCAL_GEOMETRY              2 cases / 2 axes / 2 clusters
LOCAL_NET_SELECTION        31 cases / 9 axes / 4 clusters
LOCAL_ANTAGONIST_PRESSURE   4 cases / 1 axis / 1 cluster
~~~

They cannot be pooled as one numeric response.

## Comparable LOCAL_NET_SELECTION layer

This is the strongest current quantitative H2 stratum.

~~~text
cases = 31          PASS
axes = 9            PASS
repeated axes = 8   PASS
clusters = 4        FAIL
~~~

Under the already registered eight-cluster gate, the comparable-layer shortage is therefore:

~~~text
4 additional independent LOCAL_NET_SELECTION clusters
~~~

## Effect-scale problem

The 31 LOCAL_NET_SELECTION cases still use different exact metrics.

~~~text
Gymnadenia:
PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA
clusters = 1

Trifolium:
STANDARDIZED_LINEAR_SELECTION_GRADIENT_BETA
clusters = 1

Erysimum:
SEM_TOTAL_DIRECT_SELECTION_PATH_COEFFICIENT
clusters = 1

Caryopteris:
DIRECTIONAL_GROUP_COMPARISON
clusters = 1
~~~

No raw numeric effect metric currently has replication across biological systems.

Thus:

~~~text
BROAD STRUCTURAL MODEL = FAIL
HOMOGENEOUS NUMERIC MODEL = FAIL
PRIMARY H2 MODEL = FAIL
~~~

## Prospectively frozen alternative

A scale-free directional-state protocol is now frozen in:

docs/SCH_H2_DIRECTIONAL_STATE_PROTOCOL_V1.md

Eligible rows are restricted to LOCAL_NET_SELECTION and are mapped prospectively to:

~~~text
SUPPORTED_POSITIVE
SUPPORTED_NEGATIVE
NO_SUPPORTED_DIRECTION
UNCLASSIFIED
~~~

This route intentionally discards raw effect-size magnitude and therefore asks a different question:

> does the supported direction/state of selection change across ecological contexts?

The protocol is frozen before further independent clusters are added.

## What remains licensed

Current H2 supports:

- exact within-axis context contrasts;
- geographic net-selection mosaics;
- supported sign switches within specific systems;
- mechanism-level change-type synthesis.

It does not yet support a cross-system numeric effect-size regression.

## Corrected bottleneck

~~~text
broad plant-performance clusters:
6 / 8

LOCAL_NET_SELECTION clusters:
4 / 8

max independent clusters sharing one exact numeric metric:
1
~~~

The next high-value systems are independent systems with source-resolved LOCAL_NET_SELECTION contexts.

Simply adding local antagonist pressure, local geometry, visitor behavior, or more rows from an existing cluster does not open the numeric H2 gate.

## Status

~~~text
H2_BROAD_STRUCTURE = FAIL_CLOSED
H2_ESTIMAND_HOMOGENEITY = FAIL_CLOSED
H2_NUMERIC_META_MODEL = FAIL_CLOSED

H2_DIRECTIONAL_STATE_PROTOCOL = FROZEN_PROSPECTIVELY
~~~
