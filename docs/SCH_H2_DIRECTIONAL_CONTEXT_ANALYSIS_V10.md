# SCH H2 directional-context analysis V10

## Question

After the registered `TOTAL_SELECTION_EFFECT` breadth gate reached 8 independent programmes, the next analysis asks a scale-invariant question:

> Does the direction of total selection on the same trait axis change across ecological contexts?

This avoids pretending that standardized gradients, path coefficients, mean-standardized gradients and no-SE context means are one inverse-variance meta-analytic effect size.

## Dataset

~~~text
TOTAL_SELECTION_EFFECT cases          81
canonical trait axes                  31
independent programmes                 8
axes with >=2 contexts                27
~~~

## Point-estimate result

Among the 27 repeated axes:

~~~text
point-estimate sign switch            14
same-sign across observed contexts    13
~~~

The 14 point-direction switches occur in 6 of the 8 independent programmes.

This is a bounded description of the qualified H2 family, not a prevalence estimate for the ecological literature.

## Uncertainty-aware result

A point estimate crossing zero is not automatically a supported reversal.

Using reported SE, p-values, confidence intervals or source significance flags where available:

~~~text
uncertainty-supported sign-switch axes       3
independent programmes containing one        2
~~~

The three axes are:

- *Gymnadenia conopsea* flowering phenology;
- *Erysimum mediohispanicum* corolla tube width;
- *Erysimum mediohispanicum* corolla shape.

For *Helianthus annuus* ssp. *texanus* ray length, the published context means switch from +0.03 far from crops to -0.02 near crops, but numeric uncertainty for those aggregate means is not materialized. It therefore remains a point-direction reversal, not an uncertainty-supported reversal.

## Interpretation

The qualified evidence supports two distinct claims.

First, realized selection is often context-sensitive: 14 of 27 repeated axes change point-estimate direction somewhere in their observed context set.

Second, strong sign reversal is much less broadly established once uncertainty is respected. Only three axes in two programmes currently show opposite directions with support on both sides of zero.

Therefore the ecological conclusion is not:

~~~text
context usually reverses selection
~~~

It is:

~~~text
ecological context frequently reorganizes the realized selection surface,
but well-supported directional reversal is concentrated in a smaller subset of systems.
~~~

This is compatible with magnitude changes, cancellation, one-sided effects and true reversals all being manifestations of context-assembled multifunctional selection.

## Statistical boundary

No cross-family pooled mean is estimated here.

The analysis is invariant to coefficient scale because sign is compared only within the same trait axis. The strict numeric-pooling gate remains separate and fail-closed.

The result should not be used as a literature-wide prevalence estimate because the 8-programme qualified family is an estimand-qualified subset of the frozen screening programme, not a completed random sample of all relevant studies.
