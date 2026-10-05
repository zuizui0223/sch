# SCH Pedicularis G fail-fast exploratory screen v1

## Purpose

The current highest-risk empirical uncertainty is not whether a physical
barrier can block a Pedicularis seed predator in principle. Congeneric and
external precedents already support barrier efficacy/timing plausibility.

The unresolved question is whether one focal P. rex device can satisfy the
registered hard method-validity requirements while preserving the natural
pollination lane and water-y.

This screen is the first pass over exploratory Stage-G V4 rows.

## Input

Use the existing V4 raw-data contract:

```text
empirical/architecture/PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V4.csv
```

Multiple exploratory EXCLUDED method identifiers may be present in the same
file. EXPOSED flowers retain matched sham handling.

Run:

```bash
python scripts/screen_pedicularis_g_exploratory_methods.py \
  <g_exploratory_v4.csv> \
  --output <g_method_screen.json>
```

## Hard validity checked immediately

For each candidate exclusion method the screen applies only already-registered
boolean method requirements:

```text
pollination window completed before barrier
ovary not swollen at barrier
pollinator-entry geometry preserved
no attack already present before barrier
barrier integrity preserved
EXPOSED rows receive sham handling.
```

These are not new biological effect thresholds.

## Descriptive effect/selectivity outputs

For each method the screen also summarizes plant-level distributions for:

```text
attack reduction
seed-predation reduction
final intact-seed gain

initial-seed-set difference
pollen-receipt change
pollinator-visitation change
realized-z change
water-state difference
handling-damage difference.
```

No minimum effect or equivalence margin is applied at this stage.

## Fail-fast states

```text
NO_METHOD_PASSES_REGISTERED_HARD_VALIDITY

ONE_METHOD_PASSES_HARD_VALIDITY_
EFFECT_AND_SELECTIVITY_TARGETS_STILL_UNFROZEN

MULTIPLE_METHODS_PASS_HARD_VALIDITY_
NO_AUTOMATIC_METHOD_SELECTION.
```

If no method passes hard validity, do not spend confirmatory effort estimating
fine-grained effect thresholds for those unchanged devices.

If one or more methods pass, use the exploratory distributions as CAL-A/B/C
basis evidence. A method is selected only after prospective target/timing
freezing; the screen itself never selects a winner.

## Relation to confirmatory V4

A positive exploratory screen is not
`PEDICULARIS_PREDATOR_METHOD_VALIDATED`.

Confirmatory V4 still requires:

```text
one prospectively frozen method
frozen timing bounds
frozen sample sizes
frozen antagonist minimum effects
frozen selectivity/equivalence margins
same-context confirmatory rows.
```

## Claim ceiling

The screen can retire mechanically invalid devices early and expose candidate
effect/selectivity distributions.

It does not establish independent G, causal compromise, F0, or dimensional
release.
