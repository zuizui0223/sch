# SCH H2 prospective reversal holdout protocol V1

## Why a holdout is now necessary

The current qualified TOTAL_SELECTION_EFFECT family has already been inspected.

It generated the V11 exploratory pattern:

~~~text
27 repeated trait axes
14 point-estimate sign switches
3 bidirectionally uncertainty-supported reversals
~~~

The three strongest reversals occur in:

- one crossed pollination × herbivory programme;
- one spatial multi-agent selection mosaic.

That pattern is useful for hypothesis generation, but it cannot be tested on the same eight programmes.

The current eight programmes are therefore frozen as a development set and permanently excluded from the primary prospective test.

## Baseline development set

Baseline commit:

`18e63173560ef416f211b6184d8dc852e9740946`

Development programmes:

1. Brassica rapa — Knauer selection programme;
2. Dalechampia scandens — Pérez-Barrales selection programme;
3. Erysimum mediohispanicum — selection mosaic;
4. Gymnadenia conopsea — agent-selection programme;
5. Helianthus annuus ssp. texanus — crop-proximity programme;
6. Lobelia cardinalis — Bartkowska selection programme;
7. Lythrum salicaria — Thomsen selection programme;
8. Trifolium repens — selection programme.

These programmes may be used for:

- biological interpretation;
- method development;
- hypothesis generation.

They may never enter the primary H2M1 holdout test.

## Prospective hypothesis H2M1

> **Held-out programmes in which ecological context changes multiple components or the interacting consumer assemblage will more often contain an uncertainty-supported directional reversal than programmes in which one registered ecological modifier changes in isolation.**

The prediction is directional, but the registered primary significance test is two-sided Fisher exact at programme level.

The direction of the effect is evaluated from the odds ratio.

## Primary inference unit

The unit is:

`independent biological programme`

not:

- trait axis;
- treatment cell;
- population;
- source paper.

This prevents a programme with many measured traits from dominating the test.

## Predictor classification

The predictor must be frozen **before selection-sign outcomes are adjudicated**.

### MULTI_COMPONENT_OR_ASSEMBLAGE

Use when the repeated-context design, before viewing outcome signs:

- crosses at least two registered ecological modifiers;
- changes consumer identity or consumer composition;
- or is a spatial ecological mosaic with source-documented variation in at least two ecological components.

Examples from the development set include the Gymnadenia factorial and Erysimum spatial mosaic.

Those examples are explanatory only; they are not holdout observations.

### SINGLE_REGISTERED_MODIFIER

Use when one registered ecological process is manipulated or prospectively stratified while the trait and total-selection estimand remain comparable.

Examples can include:

- pollination supplementation;
- herbivory reduction;
- damage manipulation.

Again, current examples are development data only.

### UNRESOLVED_CONTEXT_DIMENSIONALITY

Use when the source context is composite or observational and cannot be assigned to either primary class without interpretation that depends on outcome signs.

These programmes remain visible but are excluded from the primary comparison.

## Outcome definition

Axis-level strong reversal requires:

~~~text
same canonical trait axis
+
at least one context with supported positive total selection
+
at least one context with supported negative total selection
~~~

Supported direction may come from:

1. a reported confidence interval excluding zero;
2. reported SE with |beta / SE| > 1.96;
3. a reported p < 0.05 paired with the sign of the reported coefficient.

No missing uncertainty is imputed.

Programme-level outcome:

~~~text
YES
if any qualified repeated axis has a bidirectionally supported reversal

NO
only after all qualified repeated axes in the programme are adjudicated
~~~

## Admission firewall

A held-out programme must:

1. first qualify for TOTAL_SELECTION_EFFECT after the baseline commit;
2. be independent of all eight development programmes;
3. satisfy the unchanged same-axis/common-outcome estimand gates;
4. have its context-dimensionality class frozen before outcome-sign adjudication;
5. contain at least one repeated canonical trait axis.

The existing outcome-blind title/abstract and full-text screening order remains authoritative.

## Registered opening gate

The primary test remains closed until all of the following are true:

~~~text
primary-eligible held-out programmes >= 8

MULTI_COMPONENT_OR_ASSEMBLAGE programmes >= 3

SINGLE_REGISTERED_MODIFIER programmes >= 3

programme outcome YES >= 2

programme outcome NO >= 2
~~~

Until then, only descriptive accumulation is allowed.

## Primary test

Once the gate opens:

~~~text
2 x 2 Fisher exact test
programme-level outcome
two-sided alpha = 0.05
~~~

Table:

~~~text
                            strong reversal YES   strong reversal NO

multi-component / assemblage

single registered modifier
~~~

Primary effect summary:

`odds ratio: multi-component / assemblage versus single modifier`

Axes remain secondary descriptive observations.

## Current status

At freeze:

~~~text
held-out programmes registered = 0
primary test gate = CLOSED
Fisher test = NOT RUN
~~~

This is intentional.

The point of this protocol is to ensure that the next result cannot be manufactured from the eight programmes that generated the hypothesis.

## Claim ceiling

The future holdout may test H2M1.

It will not by itself estimate:

- the literature-wide prevalence of reversal;
- a universal probability that a given ecological interaction reverses selection;
- a pooled effect size across incompatible selection metrics;
- a causal effect of “multidimensionality” when the predictor class is observational rather than manipulated.

The current V11 mechanism taxonomy remains descriptive until held-out evidence is accumulated.
