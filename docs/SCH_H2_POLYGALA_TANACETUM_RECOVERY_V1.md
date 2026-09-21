# SCH H2 Polygala and Tanacetum recovery V1

## Why these systems were added

After Erysimum, the broad H2 plant-performance layer had enough cases and canonical axes but still lacked independent biological clusters.

Two source-resolved fixed-role systems were therefore inspected for exact local information:

- *Polygala vayredae*
- *Tanacetum vulgare*

The purpose was not to force a pooled model. The purpose was to increase ecological breadth while preserving the estimand represented by each local case.

## Polygala vayredae

Source: Castro, Silveira & Navarro, *Ecological Research*.

DOI: 10.1007/s11284-008-0481-5

Canonical axis promoted: Polygala_000334_nectar_reward.

Table 5 reports population-specific regression models for successful pollination.

~~~text
Montmajor
  raw coefficient = 7.192
  standardized b = 0.311
  t = 3.293
  p = 0.001

Serrat dels Boixos
  raw coefficient = 10.429
  standardized b = 0.169
  t = 1.559
  p = 0.123

Colldecarrera
  raw coefficient = 13.955
  standardized b = 0.255
  t = 2.573
  p = 0.011
~~~

These three rows are classified as LOCAL_REPRODUCTIVE_COMPONENT_EFFECT.

Estimand family: REPRODUCTIVE_COMPONENT_EFFECT.

Numeric family: SUCCESSFUL_POLLINATION_STANDARDIZED_B.

They are not final-fitness selection gradients and not local two-function geometry.

## Tanacetum vulgare

Source: Sasidharan et al. 2024, *Functional Ecology*.

DOI: 10.1111/1365-2435.14673

Two canonical axes receive one exact 2021 reproductive-performance case each:

- Tanacetum_000352_individual_chemotype
- Tanacetum_000352_plot_chemodiversity

The source did not measure seed set. It measured germination of field-produced seeds as a proxy for reproductive success.

~~~text
chemotype -> germination
chi-square = 10.44
df = 4
p = 0.034
n = 95

plot type -> germination
chi-square = 0.61
df = 1
p = 0.434
n = 95

pollinator visits -> germination
chi-square = 5.05
df = 1
p = 0.025

florivore visits -> germination
chi-square = 0.85
df = 1
p = 0.356
~~~

These rows are classified as LOCAL_REPRODUCTIVE_PERFORMANCE_PROXY.

Estimand family: REPRODUCTIVE_PERFORMANCE_PROXY.

Numeric family: GERMINATION_WALD_TEST.

They are not selection gradients and are not seed-set effects.

## Why the estimand split matters

After adding Polygala and Tanacetum, the broad plant-performance layer reaches:

~~~text
42 cases
14 canonical axes
8 independent biological clusters
11 repeated axes
~~~

Those values pass the original breadth thresholds.

However, the 42 cases do not measure one common quantity.

Current materialized estimand families include:

~~~text
LOCAL_TWO_FUNCTION_GEOMETRY
TOTAL_SELECTION_EFFECT
REALIZED_NET_PERFORMANCE
ANTAGONIST_PRESSURE
REPRODUCTIVE_COMPONENT_EFFECT
REPRODUCTIVE_PERFORMANCE_PROXY
~~~

The largest family is TOTAL_SELECTION_EFFECT:

~~~text
30 cases
8 axes
3 independent clusters
~~~

Thus ecological breadth is adequate, but a common numeric estimand is not.

## Consequence

SCH now separates two gates:

~~~text
Gate A — ecological breadth
PASS

Gate B — commensurate estimand family
FAIL
~~~

A broad mixed model is therefore not opened merely because eight clusters have at least one plant-performance case.

## Current interpretation

> Ecological breadth is no longer the primary limitation; measurement heterogeneity is.

The next high-value work is to increase the number of independent systems inside one predeclared estimand family, especially TOTAL_SELECTION_EFFECT, rather than adding arbitrary performance proxies.
