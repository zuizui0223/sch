# SCH H2 Pedicularis local antagonist-pressure recovery V1

## Source

Sun, Armbruster & Huang (2016), *Annals of Botany*.

DOI:

`10.1093/aob/mcw097`

The primary Results text reports exact pre-dispersal seed-predation percentages for four populations of *Pedicularis rex*.

## Exact local pressure values

~~~text
population 11   0.80 %
population 3    1.36 %
population 12  18.50 %
population 5   27.42 %
~~~

These values are now materialized as four H2 local context cases.

## Measurement layer

The four rows are classified as:

`LOCAL_ANTAGONIST_PRESSURE`

not:

`LOCAL_GEOMETRY`

Each row identifies local seed-predator pressure only.

The population-specific pollinator-mediated and seed-predator-mediated trait gradients are not reconstructed from these percentages.

## Linkage boundary

The broader source programme reports:

~~~text
floral / pollen contexts                  14 populations
seed-predation / seed-production contexts 12 populations
same-individual linkage                    7 populations
~~~

Same-individual linkage is preserved in populations:

~~~text
1, 3, 5, 8, 9, 10, 11
~~~

Plant labels were lost in populations:

~~~text
2, 4, 6, 7, 12
~~~

Among the four pressure cases materialized here:

- populations 3, 5 and 11 retain individual trait/pollination/seed linkage in the broader programme;
- population 12 is pressure-only because labels were lost.

Therefore the four exact pressure values must not be interpreted as four local shared-trait geometries.

## Ecological range

The four main-text values already demonstrate substantial geographic heterogeneity in antagonist pressure:

~~~text
minimum reported = 0.80 %
maximum reported = 27.42 %
~~~

The ratio of the largest to the smallest reported pressure is more than thirtyfold.

This supports the source-level interpretation that the antagonist component varies strongly among populations.

It does not identify the population-specific sign or magnitude of seed-predator-mediated selection on corolla exsertion.

## H2 consequence

Before this recovery, the Pedicularis H2 record was:

~~~text
context structure known
population-specific pressure rows = 0
~~~

After recovery:

~~~text
LOCAL_ANTAGONIST_PRESSURE cases = 4
LOCAL_GEOMETRY cases = 0
~~~

The H2 change class remains:

`COMPONENT_WEIGHT_SHIFT`

with the stronger bounded interpretation:

> Geographic variation in antagonist pressure is directly observed, while population-specific two-function trait geometry remains unresolved.

## Modelability consequence

After adding these four rows, the plant-performance H2 layer reaches:

~~~text
cases = 15
canonical axes = 5
biological clusters = 4
axes with >=2 local cases = 4
~~~

The registered raw case-count threshold is 12, so that one gate now passes.

The structural gates still fail:

~~~text
required canonical axes = 8   current = 5
required clusters       = 8   current = 4
required repeated axes  = 5   current = 4
~~~

This is useful: additional rows from the same few systems are no longer the main need.

The next information gain must come from additional independent canonical axes and biological clusters.

## Remaining source recovery

The published supplement objects remain high value:

- Table S1 — locality / altitude;
- Table S2 — seed set, predation and chi-square for all 12 seed-outcome populations;
- Appendix S1 — trait means / SE and pollination success for 14 populations.

Recovering Table S2 can expand local antagonist-pressure coverage from four to twelve populations.

It still would not automatically create twelve local shared-trait geometry cases.

## Claim ceiling

~~~text
PEDICULARIS_MAIN_TEXT_PRESSURE_CASES = 4
EXACT_PRESSURE_VALUES = RECOVERED

POPULATION_SPECIFIC_LOCAL_GEOMETRY = NOT ESTIMATED
POPULATION_SPECIFIC_COMPONENT_SELECTION = NOT ESTIMATED

H2_CASE_COUNT_GATE = PASS
H2_STRUCTURAL_MODEL_GATE = FAIL
~~~
