# SCH macroecology H2 modelability gate V4

## Trifolium update

Four exact *Trifolium repens* local net-selection contexts are now materialized from the primary article.

Current plant-performance layer:

~~~text
cases = 19
canonical axes = 7
clusters = 5
axes with >=2 local cases = 6
~~~

Registered gates:

~~~text
minimum cases          12   PASS
minimum axes            8   FAIL: current 7
minimum clusters        8   FAIL: current 5
minimum repeated axes   5   PASS
~~~

This marks a second major transition:

> H2 no longer lacks case count or within-axis replication. It lacks independent ecological breadth.

The remaining primary task is to add new independent fixed-role clusters, not more rows from Gymnadenia or Pedicularis.

## New Trifolium contexts

Inflorescence production:

~~~text
ambient herbivory   beta = 0.91
reduced herbivory   beta = 1.34
~~~

Flowering time among cyanogenic genotypes:

~~~text
open pollination          beta = -0.03
supplemental pollination  beta =  0.19
~~~

All four are LOCAL_NET_SELECTION.

They are not promoted to local pollinator–herbivore geometry.

## Current status

~~~text
H2_TOTAL_LOCAL_CASES = 26
H2_TOTAL_AXES_WITH_CASES = 10
H2_TOTAL_CLUSTERS_WITH_CASES = 7

H2_PLANT_PERFORMANCE_CASES = 19
H2_PLANT_PERFORMANCE_AXES = 7
H2_PLANT_PERFORMANCE_CLUSTERS = 5
H2_PLANT_PERFORMANCE_REPEATED_AXES = 6

CASE_COUNT_GATE = PASS
REPEATED_AXIS_GATE = PASS
CANONICAL_AXIS_GATE = FAIL
INDEPENDENT_CLUSTER_GATE = FAIL

H2_MODEL = FAIL_CLOSED
~~~

## Next priority

The highest-value next systems are independent fixed-role clusters with source-resolved context values.

One additional canonical axis would pass the axis-count gate, but three additional independent plant-performance clusters are still needed for the registered cluster gate.
