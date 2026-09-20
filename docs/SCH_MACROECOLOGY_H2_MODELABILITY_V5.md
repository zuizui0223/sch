# SCH macroecology H2 modelability gate V5

## Erysimum update

Eighteen exact *Erysimum mediohispanicum* population-level total direct selection paths are now materialized from Table 5.

Current plant-performance layer:

~~~text
cases = 37
canonical axes = 11
clusters = 6
axes with >=2 local cases = 10
~~~

Registered gates:

~~~text
minimum cases          12   PASS
minimum axes            8   PASS
minimum clusters        8   FAIL: current 6
minimum repeated axes   5   PASS
~~~

For the first time, **only one registered H2 structural gate remains closed**:

`independent biological clusters`

## What changed

Erysimum contributes:

~~~text
18 local net-selection cases
4 canonical floral axes
1 new independent biological cluster
~~~

The four axes are:

- corolla diameter;
- corolla tube length;
- corolla tube width;
- corolla shape.

## Why Erysimum matters

The new cases are not simply extra rows.

They provide a geographic-selection-mosaic structure in which:

- some traits show selective hotspots and coldspots;
- tube width changes from positive to negative net selection;
- corolla shape changes from negative to positive net selection;
- local pollinator assemblages differ strongly among populations;
- ungulate damage also varies geographically.

Thus the new information is independent ecological breadth, exactly the quantity that the H2 modelability gate had been missing.

## Remaining blocker

~~~text
required plant-performance clusters = 8
current plant-performance clusters  = 6
remaining independent clusters      = 2
~~~

Adding more rows to Gymnadenia, Pedicularis, Trifolium or Erysimum does not solve this bottleneck.

The next priority is therefore two additional independent fixed-role systems with source-resolved local plant-performance contexts.

## Status

~~~text
H2_TOTAL_LOCAL_CASES = 44

H2_PLANT_PERFORMANCE_CASES = 37
H2_PLANT_PERFORMANCE_AXES = 11
H2_PLANT_PERFORMANCE_CLUSTERS = 6
H2_PLANT_PERFORMANCE_REPEATED_AXES = 10

CASE_COUNT_GATE = PASS
CANONICAL_AXIS_GATE = PASS
REPEATED_AXIS_GATE = PASS
INDEPENDENT_CLUSTER_GATE = FAIL

H2_MODEL = FAIL_CLOSED
~~~
