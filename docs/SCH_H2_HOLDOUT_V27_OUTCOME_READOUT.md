# SCH H2 holdout V27 outcome adjudication

## Purpose

V26 froze predictor classes from METHODS only. V27 is the first separate outcome-adjudication step.

The V26 classes are not changed after viewing coefficients.

## Numeric source freeze

V27 materializes source-table beta and SE values for:

- Dactylorhiza lapponica — open versus supplemental pollination;
- Primula alpicola — open versus supplemental pollination;
- Trillium discolor — open versus pollen-supplemented contexts across 2020 and 2021.

Impatiens capensis remains pending because the required numeric uncertainty table is not yet materialized.

Supported direction is defined prospectively by:

~~~text
beta / SE >  1.96  -> SUPPORTED_POSITIVE
beta / SE < -1.96  -> SUPPORTED_NEGATIVE
otherwise          -> NOT_SUPPORTED
~~~

All uncertainty-resolved source-defined contexts are evaluated. No favorable context pair is selected after viewing signs.

## Programme results

~~~text
Dactylorhiza lapponica
eligible repeated floral axes      5
supported reversal axes            0
q_j                              0.0

Primula alpicola
eligible repeated floral axes      4
supported reversal axes            0
q_j                              0.0

Trillium discolor
eligible repeated floral axes      3
supported reversal axes            2
q_j                         0.666667

Impatiens capensis
outcome                       PENDING
~~~

Primula rosette diameter is excluded because the paper treats it as a plant-condition covariate rather than a floral coordinate.

Trillium petal colour is excluded from the numeric direction denominator because the source analyzes it categorically and does not provide a comparable linear beta ± SE pair.

## Trillium supported reversals

Two Trillium axes contain uncertainty-supported positive and negative source-defined contexts under the registered all-context primary rule:

- floral display height;
- petal size.

Flowering date does not meet the bidirectional support criterion.

A secondary within-year diagnostic finds **0/3** Trillium axes with bidirectionally supported reversal inside a single year. The two primary reversals therefore arise across the full year × pollination context set and are not attributed to pollen supplementation alone.

## Current prospective state

~~~text
registered held-out programmes                4
complete primary programmes                   3
  SINGLE_REGISTERED_MODIFIER                  3
  MULTI_COMPONENT_OR_CONSUMER_TURNOVER        0 complete

complete single-modifier q_j values
  Dactylorhiza                              0
  Primula                                   0
  Trillium                                2/3

primary opening gate                    CLOSED
primary H2M1 test                       NOT RUN
~~~

## Ecological interpretation

The first held-out outcomes already rule out an overly strong reading of the V11 pattern:

> supported directional reversal is not confined to programmes prospectively classified as multi-component.

Trillium contains two supported reversals while prospectively frozen in the SINGLE_REGISTERED_MODIFIER class. Because both are cross-year/cross-stratum under the primary all-context rule, this is not evidence that the single manipulated pollination modifier itself caused the reversal.

This does **not** test the registered directional H2M1 prediction. The primary prediction is comparative and programme-level: multi-component / consumer-turnover programmes are predicted to have a higher mean q_j than single-modifier programmes. No multi-component programme has a completed outcome yet, and the opening gate requires at least five complete programmes in each class.

Thus Trillium is a valid potentially countervailing held-out observation, not a reason to retune the hypothesis.

## Source-axis / canonical boundary

All four V26 studies now have source-axis coverage rows.

~~~text
record-level H1 candidates             38
source-axis covered H1 candidates      38
source-axis evidence records           63
canonical trait axes                   50
~~~

The four new coverage rows are composite source records. They do not automatically increase the 50-axis canonical ledger; individual-axis canonicalization is a later step.

## Claim ceiling

V27 supports:

- a programme prospectively classified as single-modifier can contain supported reversals across its full registered context set;
- zero-reversal outcomes are real holdout outcomes rather than screening failures;
- source-defined context turnover can reverse supported total-selection direction within a programme.

V27 does not support:

- a class comparison;
- a prevalence estimate;
- a conclusion that single-modifier or multi-component contexts reverse selection more often;
- adding Impatiens to the outcome denominator before numeric uncertainty is recovered;
- treating the 12 eligible axes as 12 independent programmes.

STATUS = THREE_HELDOUT_PROGRAMMES_COMPLETE_ONE_PENDING_PRIMARY_GATE_CLOSED
