# SCH H2 switch-mechanism taxonomy V11

## Question

The qualified `TOTAL_SELECTION_EFFECT` family contains 81 local selection cases across 31 trait axes and 8 independent programmes.

V10 established that 14 of 27 repeated axes cross zero in their point estimates somewhere across observed contexts.

V11 asks a stricter question:

> **What kind of ecological context produced those point-direction changes, and how strong is the evidence that selection truly reversed direction?**

## Reversal evidence ladder

A point estimate crossing zero is not treated as equivalent to an uncertainty-supported reversal.

The 27 repeated axes are partitioned as:

~~~text
NO_POINT_REVERSAL                         13

POINT_REVERSAL:
  both directions uncertainty-supported   3
  one direction supported                 5
  both directions unsupported             5
  uncertainty unresolved                  1
~~~

Thus the 14 point-switch axes are more accurately described as:

~~~text
3 strong bidirectional reversals
5 asymmetric-support reversals
5 unsupported point reversals
1 uncertainty-unresolved point reversal
~~~

The three bidirectionally supported axes are:

- *Gymnadenia conopsea* flowering phenology;
- *Erysimum mediohispanicum* corolla tube width;
- *E. mediohispanicum* corolla shape.

## Context-mechanism taxonomy

### Mixed pollination × herbivory factorial

~~~text
repeated axes                    2
point-switch axes                2
bidirectionally supported        1
one-side supported               1
~~~

Both Gymnadenia axes change point direction somewhere in the 2 × 2 pollination/herbivory experiment.

Flowering phenology contains a supported positive context and supported negative contexts.

Spur length crosses zero only at the point-estimate level because the negative cell is not independently supported away from zero.

### Pollination supplementation

Across Trifolium flowering time and six Lobelia axes:

~~~text
repeated axes                    7
point-switch axes                4
bidirectionally supported        0
one-side supported               1
both-sides unsupported           3
~~~

Pollination context can alter realized direction, but the current evidence does not contain a bidirectionally supported reversal in this mechanism class.

This should not be interpreted as evidence that pollination relief cannot reverse selection. The current mechanism cell contains only two programmes.

### Herbivory reduction

~~~text
repeated axes                    1
point-switch axes                0
~~~

The Trifolium inflorescence-production axis remains positive under both ambient and reduced herbivory while changing in magnitude.

This is a useful reminder that ecological context often changes **strength** without changing **direction**.

### Spatial multi-agent mosaic

Erysimum populations vary jointly in pollinator assemblage, ungulate damage and other local ecological conditions.

~~~text
repeated axes                    4
point-switch axes                3
bidirectionally supported        2
one-side supported               1
~~~

The two supported reversals are corolla tube width and corolla shape.

Because several ecological dimensions vary simultaneously, these spatial reversals do not identify one causal modifier.

### Consumer identity / composition

The Brassica experiment compares:

~~~text
bumble bees
bumble bees + cabbage butterflies
cabbage butterflies
~~~

Across nine repeated trait axes:

~~~text
point-switch axes                4
bidirectionally supported        0
one-side supported               2
both-sides unsupported           2
~~~

Consumer composition clearly reorganizes several point estimates, but the current uncertainty structure does not support opposite directions on both sides of zero for any one axis.

### Antagonist damage manipulation

The Lythrum clipping experiment contains three repeated total-selection axes.

~~~text
point-switch axes                0
~~~

Damage context changes selection magnitude, including strong treatment effects on flowering start, without point-direction reversal.

### Landscape crop proximity

Helianthus ray length changes from:

~~~text
far from crops   beta = +0.03
near crops       beta = -0.02
~~~

but uncertainty for those aggregate context means is not numerically materialized.

It remains:

`POINT_REVERSAL_UNCERTAINTY_UNRESOLVED`

## Ecological interpretation

The qualified H2 family now supports a sharper statement than “selection is context dependent.”

> **Ecological context can alter selection strength without changing direction, generate unsupported point-direction crossings, or produce uncertainty-supported reversal of the realized selection surface. These are different biological outcomes and should not be collapsed into one context-effect label.**

The strongest reversals currently occur in:

- a crossed pollination × herbivory experiment;
- a spatial multi-agent mosaic.

This pattern is biologically suggestive because both settings vary more than one ecological component.

However, it is **not yet evidence that multidimensional contexts are more likely to cause reversal**.

## Why no mechanism-rate test is run

The mechanism categories were created after inspection of the current qualified family and are highly programme-confounded.

For example:

- spatial multi-agent mosaic is represented by one Erysimum programme;
- consumer identity/composition is represented by one Brassica programme;
- mixed pollination × herbivory is represented by one Gymnadenia programme.

Therefore ratios such as 3/4 versus 4/9 are descriptive occupancy of the current dataset, not comparable ecological probabilities.

No Fisher test, logistic model or ranking of mechanisms is licensed from V11.

## Prospective implication

The V11 pattern motivates a future outcome-blind hypothesis:

> Strong directional reversal may require either simultaneous change in multiple ecological weights or turnover in the interacting consumer environment, whereas single-factor manipulations may more often change magnitude without establishing opposite supported directions.

That hypothesis must be frozen **before** new qualified programmes are used to test it.

## Status

~~~text
TOTAL_SELECTION_EFFECT cases       81
trait axes                         31
repeated axes                      27

point-switch axes                  14
bidirectional supported reversals   3
one-side supported reversals        5
both-sides unsupported flips        5
uncertainty-unresolved flips        1

MECHANISM_TAXONOMY = DESCRIPTIVE_ONLY
MECHANISM_RATE_INFERENCE = NOT LICENSED
~~~
