# SCH H2 Trifolium exact context recovery V1

## Source

Santangelo et al. 2019, Journal of Evolutionary Biology.

DOI: `10.1111/jeb.13392`

The source uses 50 clonal genotypes of *Trifolium repens* in a common-garden factorial design crossing cyanogenic defence, invertebrate-herbivore suppression and supplemental pollination.

## Inflorescence production

Exact source-reported standardized selection gradients:

~~~text
ambient herbivory    beta = 0.91   P < 0.001
reduced herbivory    beta = 1.34   P < 0.001
~~~

The trait × herbivory interaction is significant at P < 0.001.

Interpretation:

> herbivory weakens positive selection for increased inflorescence production.

These are local net-selection states averaged across the other experimental factors. They are not local pollinator-versus-herbivore geometry.

## Flowering time among cyanogenic genotypes

Exact source-reported gradients:

~~~text
open pollination          beta = -0.03   P = 0.77
supplemental pollination  beta =  0.19   P = 0.03
~~~

The flowering-time × defence × pollination interaction is P = 0.013.

The source cautions that this effect may partly reflect pleiotropic or allocation effects associated with cyanogenic-glycoside genetics.

Therefore the two rows are retained as local net selection under pollination context, not as pure pollinator-mediated local geometry.

## H2 promotion

Four exact local plant-performance cases are materialized:

- two inflorescence-production herbivory contexts;
- two flowering-time pollination contexts.

No figure digitization is used.

## Modelability effect

Before Trifolium:

~~~text
plant-performance cases      15
canonical axes                5
independent clusters          4
repeated axes                 4
~~~

After Trifolium:

~~~text
plant-performance cases      19
canonical axes                7
independent clusters          5
repeated axes                 6
~~~

Thus:

~~~text
case-count gate       PASS
repeated-axis gate    PASS
canonical-axis gate   FAIL: 7 < 8
cluster gate          FAIL: 5 < 8
~~~

The H2 bottleneck is now unambiguously independent-cluster breadth.
