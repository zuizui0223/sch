# SCH H2 estimand gate opening with Helianthus texanus — V9

## Result

The registered `TOTAL_SELECTION_EFFECT` estimand-family breadth gate now reaches its predeclared independent-cluster minimum.

~~~text
before Helianthus:
79 cases / 30 axes / 7 clusters / 26 repeated axes

after Helianthus:
81 cases / 31 axes / 8 clusters / 27 repeated axes

TOTAL_SELECTION_EFFECT ESTIMAND GATE = PASS
~~~

This does **not** open the strict cross-study numeric pooling gate.

~~~text
STANDARDIZED_SELECTION_GRADIENT
61 cases / 26 axes / 6 clusters / 22 repeated axes

STRICT NUMERIC POOLING GATE = FAIL
~~~

## Source and estimand

Primary source:

- SCHPRISMA-000673
- Mitchell, Chamberlain & Whitney 2021
- DOI 10.1111/eva.13201
- *Helianthus annuus* ssp. *texanus*

The phenotypic-selection analysis uses log relative whole-plant seed production as fitness. Traits are transformed as needed and standardized within population to mean 0 and SD 1.

For the multi-year Sites 1/2 comparison, the article text reports exact average direct-selection gradients for ray length:

~~~text
far from crop sunflower:  beta = +0.03
near crop sunflower:      beta = -0.02
~~~

These two context means are frozen as the eighth independent TOTAL_SELECTION_EFFECT programme.

## Why the strict pooling gate remains closed

The article figure displays uncertainty around context means, and the supplementary workbook contains population-level coefficients, but the context-mean SE values are not numerically reported in the source text materialized here.

Therefore Helianthus is coded as:

~~~text
numeric_pooling_family = MEAN_STANDARDIZED_SELECTION_GRADIENT_NO_SE
strict_numeric_pooling_qualified = NO
~~~

No figure digitization, imputation, or invented uncertainty is used.

## Ecological implication

The same standardized floral-display trait changes the sign of direct selection across replicated agricultural contexts: positive average selection for longer rays far from crop sunflowers and slightly negative average selection near crops.

The study also independently documents pollinator and seed-predator mediation of selection in replicated population pairs. The Helianthus contribution therefore strengthens SCH's claim that realized floral selection is context assembled by changing interaction environments.

It does not establish that ray-length sign reversal itself is attributable to one uniquely identified consumer pathway.

## Statistical consequence

Passing the estimand-family breadth gate means SCH can now proceed to the **registered TOTAL_SELECTION_EFFECT family analysis**.

It does not license pooling all coefficient types as one common effect size. The next statistical task is therefore:

1. fit the estimand-family model while retaining numeric-pooling-family strata;
2. do not mix no-SE Helianthus context means with inverse-variance standardized-gradient meta-analysis;
3. retain cluster-level dependence;
4. report the stricter numeric-pooling gate as unresolved.
