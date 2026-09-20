# SCH macroecology H2 modelability gate V2

## Update

Gymnadenia Appendix A Table A2 has been source-extracted.

This adds eight exact treatment-group local net-selection cases:

~~~text
2 canonical trait axes
x
4 pollination × herbivory treatment groups
=
8 local net-selection cases
~~~

## Current H2 local-case denominator

~~~text
TOTAL_LOCAL_CASES = 18
CANONICAL_AXES_WITH_CASES = 7
BIOLOGICAL_CLUSTERS_WITH_CASES = 5
AXES_WITH >=2 LOCAL_CASES = 6
~~~

## Plant-performance layer

~~~text
cases = 11
canonical axes = 4
clusters = 3
axes with >=2 local cases = 3
~~~

Repeated plant-performance axes:

- *Caryopteris divaricata* corolla tube;
- *Gymnadenia conopsea* flowering phenology;
- *Gymnadenia conopsea* spur length.

The local plant-performance layer is now much larger, but it remains too narrow in independent axes and clusters for the registered mixed model.

## Visitor-role behavior layer

Unchanged:

~~~text
cases = 7
canonical axes = 3
clusters = 2
axes with >=2 local cases = 3
~~~

Blueberry and sesame remain a separate visitor-role estimand.

## Project modelability gates

~~~text
minimum cases per layer             12
minimum canonical axes per layer     8
minimum independent clusters         8
minimum repeated axes                5
~~~

Current result:

~~~text
PLANT_PERFORMANCE_MODEL = FAIL
ROLE_BEHAVIOR_MODEL = FAIL
COMBINED_LAYER_MODEL = PROHIBITED_BY_ESTIMAND
~~~

The plant-performance layer is now one case below the raw case-count threshold, but that is not the limiting issue.

The stronger blockers are:

~~~text
canonical axes = 4 < 8
clusters = 3 < 8
repeated axes = 3 < 5
~~~

Thus adding one more local row would not open the model gate.

## New licensed analysis

Gymnadenia now licenses direct descriptive comparison of treatment-group net selection:

~~~text
beta_C+H
beta_C+E
beta_HP+H
beta_HP+E
~~~

with source-reported SE for each beta.

It also licenses directional interpretation of the source-reported mediated contrasts.

It does **not** license contrast-level inference without contrast uncertainty.

## Current change-type synthesis

The H2 seed now contains:

~~~text
GEOMETRY_CLASS_SWITCH                         1
GEOMETRY_DISAPPEARANCE                        1
COMPONENT_WEIGHT_SHIFT                        1
COMPONENT_WEIGHT_SHIFT_WITH_EVOLUTIONARY_RESPONSE 1
CONSUMER_ROLE_BEHAVIOR_SHIFT                  3
NET_SELECTION_SHIFT_ACROSS_CONSUMER_REGIME   2
~~~

The last category is the two Gymnadenia axes.

## Next priorities

The largest gains now require new independent fixed-role systems, not more treatment cells from Gymnadenia.

Priority:

1. Gentiana S3 population selection table;
2. Pedicularis S1/S2/Appendix S1;
3. Primula farinosa population × manipulation × time tables.

These can increase the number of plant-performance axes and independent clusters.

## Status

~~~text
H2_TOTAL_LOCAL_CASES = 18
H2_PLANT_PERFORMANCE_CASES = 11
H2_ROLE_BEHAVIOR_CASES = 7

H2_PLANT_PERFORMANCE_AXES = 4
H2_PLANT_PERFORMANCE_CLUSTERS = 3

H2_MODEL = FAIL_CLOSED
~~~
