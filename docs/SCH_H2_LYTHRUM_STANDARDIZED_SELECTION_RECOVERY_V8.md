# SCH H2 Lythrum standardized-selection recovery V8

## Source

Primary numeric source:
- SCHPRISMA-000284
- Thomsen & Sargent 2017, Annals of Botany
- DOI 10.1093/aob/mcx026
- Table 2

Dependent provenance source:
- SCHPRISMA-000812
- Thomsen thesis, University of Ottawa
- This is the same biological programme and is not counted as an additional independent cluster.

## Numeric contract

The source analysis standardizes each trait within treatment and expresses fitness relative to the treatment mean. Table 2 reports direct linear selection gradients beta plus SE.

The six total-selection cells used by H2 are:

~~~text
number of inflorescences:
  clipped   0.20 +/- 0.07
  control   0.47 +/- 0.07

inflorescence height:
  clipped   0.22 +/- 0.06
  control   0.33 +/- 0.09

flowering start time:
  clipped  -0.28 +/- 0.06
  control  -0.03 +/- 0.08
~~~

Damage x trait, pollination x trait, and pollination x damage x trait delta-beta contrasts are also frozen from Table 2 but are not counted as additional TOTAL_SELECTION_EFFECT cases.

## H2 consequence

~~~text
TOTAL_SELECTION_EFFECT
before: 73 cases / 27 axes / 6 clusters
after:  79 cases / 30 axes / 7 clusters

STANDARDIZED_SELECTION_GRADIENT
before: 55 cases / 23 axes / 5 clusters
after:  61 cases / 26 axes / 6 clusters

registered independent-cluster minimum = 8
remaining deficit = 1
~~~

The numeric model remains fail-closed until one more independent qualified programme is recovered.

## Ecological interpretation

Herbivore-simulated meristem damage changes the realized selection surface on inflorescence number and flowering time, while pollination-treatment interactions are weak. This is evidence that an antagonist-associated state can redirect total selection on floral architecture without requiring a strong pollinator-mediated contrast on the same trait in that experiment.

The result strengthens SCH's context-dependent selection claim but is not treated as a universal conflict prevalence estimate.
