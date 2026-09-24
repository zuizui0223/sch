# SCH H2 context-driver decomposition V11

## Question

V10 established a scale-invariant directional result within the qualified \`TOTAL_SELECTION_EFFECT\` family:

- 27 trait axes are observed in at least two ecological contexts;
- 14 show a point-estimate sign switch;
- 3 show an uncertainty-supported sign switch.

V11 asks a different question:

> Are those directional changes confined to geographic turnover, or do they also occur when the interacting biotic regime is experimentally changed?

The analysis is descriptive and programme-aware. It does not compare context-family rates statistically.

## Outcome-blind context-driver rule

Each independent programme is assigned a context family from design metadata rather than from the observed selection result.

~~~text
BIOTIC_REGIME_MANIPULATION
  Gymnadenia   pollination x herbivory
  Trifolium    pollination or herbivory treatment
  Brassica     consumer identity / combination
  Lobelia      pollination supplementation
  Lythrum      damage treatment

NATURAL_SPATIAL_MOSAIC
  Erysimum     population pollinator-herbivory mosaic

ANTHROPOGENIC_PROXIMITY
  Helianthus   near versus far from crop sunflower
~~~

Dalechampia contributes valid total-selection estimates but no repeated within-axis context contrast, so it does not enter V11's repeated-context denominator.

## Programme-level denominator

~~~text
repeated trait axes                       27
independent repeated-context programmes    7
programmes with >=1 point sign switch       6
programmes with >=1 supported switch        2
~~~

The biological programme, not the individual trait axis, is retained as the independent unit.

## Result 1 — manipulated biotic regimes are sufficient to generate directional reorganization

Across five independent programmes in which pollination, herbivory/damage, or consumer composition was manipulated:

~~~text
repeated axes                              22
point-estimate sign-switch axes            10
uncertainty-supported sign-switch axes      1

programmes with >=1 point switch            4 / 5
programmes with >=1 supported switch        1 / 5
~~~

The supported switch is Gymnadenia flowering phenology.

This matters because the V10 context-sensitivity pattern is not only a by-product of comparing different natural populations. Changing the biotic interaction regime within an experimental design can also redirect the realized selection surface.

This does not imply that manipulated biotic regimes have a higher reversal probability than other context types; the programme count is too small for that comparison.

## Result 2 — natural spatial mosaic contains the strongest replicated reversals

Erysimum contributes four repeated corolla axes across natural populations:

~~~text
point-estimate sign-switch axes             3 / 4
uncertainty-supported sign-switch axes       2 / 4
~~~

The supported reversals are corolla tube width and corolla shape.

Because pollinator assemblage, herbivory and other population context vary together, this is a natural spatial mosaic rather than a single identified causal driver.

## Result 3 — anthropogenic proximity is a candidate directional driver, not yet a supported reversal

Helianthus ray length changes mean direction from positive far from crop sunflowers to negative near crops:

~~~text
point-estimate sign switch                  YES
uncertainty-supported sign switch           NO / unresolved
~~~

Numeric uncertainty for the two aggregate context means is not materialized, so crop proximity remains a point-direction pattern only.

## Ecological interpretation

V10 showed that ecological context can reorganize the direction of realized selection.

V11 adds a more specific result:

> context-sensitive selection is recovered both under manipulated biotic regimes and across natural spatial mosaics; therefore the pattern cannot be reduced to geographic turnover alone.

A bounded mechanistic reading is:

~~~text
interaction regime changes
        |
        v
relative functional contributions change
        |
        v
realized selection surface can rotate,
weaken, disappear, or reverse
~~~

The current data support the first two empirical links at the level of repeated selection estimates. They do not yet provide a cross-system estimate of how often each driver causes a reversal.

## Statistical boundary

V11 deliberately does not run a family-level significance test.

Reasons:

- only seven independent repeated-context programmes are available;
- trait axes are nested within programmes;
- the three context families are highly unbalanced;
- Erysimum and Helianthus are spatial comparisons rather than randomized driver manipulations;
- uncertainty support differs among source objects.

The valid output is therefore a programme-aware decomposition, not a meta-regression.

## Claim ceiling

Supported:

- directional reorganization occurs in multiple independent manipulated biotic programmes;
- directional reorganization also occurs in natural spatial mosaics;
- the V10 pattern is not solely a geographic-comparison artifact;
- uncertainty-supported reversals remain concentrated in Gymnadenia and Erysimum.

Not supported:

- a literature-wide reversal prevalence;
- a ranking of context-driver importance;
- a statistical difference among context families;
- causal attribution of the Erysimum spatial mosaic to one specific driver;
- an uncertainty-supported Helianthus near/far reversal;
- cross-family inverse-variance pooling.

~~~text
STATUS = CONTEXT_DRIVER_DECOMPOSITION_READY_NO_FAMILY_COMPARISON
~~~
