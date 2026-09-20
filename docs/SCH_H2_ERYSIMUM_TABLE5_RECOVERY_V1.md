# SCH H2 Erysimum Table 5 recovery V1

## Source

Gómez et al. 2009, Ecological Monographs 79:245–263.

DOI: `10.1890/08-0511.1`

Table 5 reports total direct selection path coefficients relating phenotypic traits to plant fitness in eight *Erysimum mediohispanicum* populations.

The H2 extraction uses four canonical floral axes already registered in SCH:

- corolla diameter;
- corolla tube length;
- corolla tube width;
- corolla shape.

## Exact local cases

Only numeric Table 5 cells are materialized.

Blank cells are **not** recoded as zero.

~~~text
corolla diameter     4 numeric population cases
corolla tube length  5 numeric population cases
corolla tube width   4 numeric population cases
corolla shape        5 numeric population cases

TOTAL                18 local cases
~~~

All 18 are classified as:

`LOCAL_NET_SELECTION`

because Table 5 reports total direct selection paths rather than separate local pollinator- and herbivore-mediated coefficients.

## Geographic sign changes

### Corolla tube width

~~~text
Em01  +0.058  significant
Em21  -0.079  significant
~~~

The primary text explicitly describes wider tubes as selected in Em01 and narrower tubes in Em21.

### Corolla shape

~~~text
Em01  -0.091
Em21  +0.149
Em22  +0.208
Em23  +0.256
Em25  +0.066
~~~

The source links divergent shape selection to changing local pollinator groups.

These are strong H2 net-selection sign changes across populations.

They are not automatically local pollinator–herbivore geometry.

## Other axes

Corolla diameter:

~~~text
Em01  -0.037  significant
Em08  -0.033
Em23  +0.022
Em25  -0.005
~~~

The Results identify Em01 as the only significant population for this trait.

Corolla tube length:

~~~text
Em01  +0.087  significant
Em22  +0.035  significant
Em23  +0.061  significant
Em24  +0.100  significant
Em25  +0.011
~~~

The primary text identifies the first four as significant positive selection for deeper flowers.

## Local ecological context

The same source quantifies ungulate damage across the eight populations.

SCH stores the local herbivory-pressure context alongside the total selection coefficient but does not relabel the Table 5 coefficient as herbivore-mediated selection.

This preserves the distinction:

~~~text
local total selection
!=
local pollinator component
!=
local herbivore component
~~~

## H2 modelability effect

Before Erysimum:

~~~text
plant-performance cases      19
canonical axes                7
independent clusters          5
repeated axes                 6
~~~

After Erysimum:

~~~text
plant-performance cases      37
canonical axes               11
independent clusters          6
repeated axes                10
~~~

Registered gates:

~~~text
case-count gate       PASS
canonical-axis gate   PASS
repeated-axis gate    PASS
cluster gate          FAIL: 6 < 8
~~~

Thus the only remaining registered H2 structural blocker is independent-cluster breadth.

## Scientific implication

Erysimum adds a strong geographic-selection-mosaic example without requiring local component overclaiming.

The same floral axis can move between selective hotspots, coldspots, and even opposite net-selection directions over sub-kilometer to kilometer scales.

This strengthens the H2 synthesis:

> ecological context can alter not only the magnitude of selection but the realized direction of selection on the same canonical trait axis.

## Claim ceiling

~~~text
ERYSIMUM_TABLE5_NUMERIC_CELLS = SOURCE_VERIFIED
LOCAL_NET_SELECTION_CASES = 18

LOCAL_POLLINATOR_COMPONENTS = NOT GENERALLY IDENTIFIED_FROM_TABLE5
LOCAL_HERBIVORE_COMPONENTS = NOT GENERALLY IDENTIFIED_FROM_TABLE5
LOCAL_TWO_FUNCTION_GEOMETRY = NOT PROMOTED_FROM_TOTAL_PATHS

H2_CLUSTER_GATE = STILL FAIL_CLOSED
~~~
