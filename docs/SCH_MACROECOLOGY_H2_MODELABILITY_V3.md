# SCH macroecology H2 modelability gate V3

## Update

Four exact *Pedicularis rex* population seed-predation values are now materialized as local antagonist-pressure cases.

The current H2 local-case denominator becomes:

~~~text
TOTAL_LOCAL_CASES = 22
CANONICAL_AXES_WITH_CASES = 8
BIOLOGICAL_CLUSTERS_WITH_CASES = 6
AXES_WITH >=2 LOCAL_CASES = 7
~~~

## Plant-performance layer

~~~text
cases = 15
canonical axes = 5
clusters = 4
axes with >=2 local cases = 4
~~~

Repeated plant-performance axes:

- *Caryopteris divaricata* corolla tube;
- *Gymnadenia conopsea* flowering phenology;
- *Gymnadenia conopsea* spur length;
- *Pedicularis rex* corolla exsertion.

The Pedicularis rows contribute local antagonist pressure, not local trait geometry.

## Visitor-role behavior layer

Unchanged:

~~~text
cases = 7
canonical axes = 3
clusters = 2
axes with >=2 local cases = 3
~~~

## Project gates

~~~text
minimum cases per layer             12
minimum canonical axes per layer     8
minimum independent clusters         8
minimum repeated axes                5
~~~

For the plant-performance layer:

~~~text
case-count gate       PASS   15 >= 12
canonical-axis gate   FAIL    5 < 8
cluster gate          FAIL    4 < 8
repeated-axis gate    FAIL    4 < 5
~~~

This is an important transition.

The bottleneck is no longer the raw number of local rows.

The bottleneck is independent ecological breadth.

Adding many more rows to Gymnadenia or Pedicularis alone cannot open the registered H2 model.

## Current H2 estimands

Materialized plant-performance rows:

~~~text
LOCAL_GEOMETRY              2
LOCAL_NET_SELECTION         9
LOCAL_ANTAGONIST_PRESSURE   4
~~~

Role-behavior rows:

~~~text
ROLE_BEHAVIOR_CONTEXT       7
~~~

These four measurement classes remain distinct.

## What is licensed now

Allowed:

- within-axis treatment contrasts;
- local net-selection comparison;
- local antagonist-pressure comparison;
- descriptive component-weight-shift synthesis;
- mechanistic change-type synthesis.

Not licensed:

- mixed-effects H2 regression;
- local antagonist pressure treated as local conflict geometry;
- combined role-behavior and plant-performance regression;
- context-switch prevalence.

## Next data priority

Because the raw case-count threshold now passes, the next highest-value sources are those that add independent axes/clusters.

Priority remains:

1. *Gentiana lutea* S3 — expands a second independent fixed-role cluster spatially;
2. *Primula farinosa* experiment/time tables — adds local plant-performance states in another cluster;
3. Pedicularis S2 — useful for pressure completeness, but lower marginal modelability value than adding a new independent cluster.

## Status

~~~text
H2_TOTAL_LOCAL_CASES = 22

H2_PLANT_PERFORMANCE_CASES = 15
H2_PLANT_PERFORMANCE_AXES = 5
H2_PLANT_PERFORMANCE_CLUSTERS = 4
H2_PLANT_PERFORMANCE_REPEATED_AXES = 4

RAW_CASE_COUNT_GATE = PASS
STRUCTURAL_MODEL_GATE = FAIL

H2_MODEL = FAIL_CLOSED
~~~
