# SCH Pedicularis G exploratory device screen and selection v1

## Purpose

The current literature frontier no longer asks whether a physical barrier can
ever block a Pedicularis seed predator. Within-genus evidence supports barrier
efficacy when pollination is replaced, and separate evidence supports
post-pollination attack timing.

The unresolved focal problem is narrower:

```text
Can one late/local P. rex barrier be physically valid
+ preserve natural bumblebee pollination
+ keep water-y fixed
+ remain intact through the predator-access window?
```

This contract separates exploratory **device validity** from confirmatory G
effectiveness.

## Step 1 — exploratory multi-device screen

Use the existing V4 exploratory data columns:

```text
empirical/architecture/PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V4.csv
```

Multiple `EXCLUDED` device identities may coexist in one exploratory file.
Matched `EXPOSED` flowers receive sham handling.

Run:

```bash
python scripts/screen_pedicularis_g_devices.py \
  <g_exploratory.csv> \
  --output <g_device_screen.json>
```

The screen applies **no CAL-A/B/F0 effect-size thresholds**.

It may reject a device only for hard method-invalidity observations:

```text
pollination window incomplete before barrier
ovary already swollen at barrier application
pollinator-entry zone covered
predator attack already present before barrier
barrier integrity/access failure
missing sham handling in exposed controls.
```

For each method it also reports descriptive plant-level distributions for:

```text
attack reduction
predation reduction
final seed gain
initial seed-set difference
pollen relative change
pollinator-visit relative change
realized-z relative change
water-depth difference
handling-damage difference
barrier delay.
```

These distributions are decision context only. They are not automatically
converted to PASS/FAIL criteria.

Possible screen statuses:

```text
G_DEVICE_SCREEN_HAS_ADMISSIBLE_METHOD
G_DEVICE_SCREEN_NO_ADMISSIBLE_METHOD.
```

## Step 2 — manual prospective device selection

If one or more devices pass hard validity, choose exactly one before
confirmatory G data are collected.

Template:

```text
empirical/architecture/PEDICULARIS_G_DEVICE_SELECTION_TEMPLATE_V1.json
```

Freeze:

```text
population_id
season_id
selected_exclusion_method
selected_before_confirmatory_data = true
selected_at_utc
basis_document
selection_basis_note
status = PEDICULARIS_G_DEVICE_SELECTION_INPUT_FROZEN.
```

Run:

```bash
python scripts/freeze_pedicularis_g_device_selection.py \
  <g_device_screen.json> \
  <completed_device_selection.json> \
  --output <g_device_selection_receipt.json>
```

A positive receipt has:

```text
receipt_schema_version = SCH_PEDICULARIS_G_DEVICE_SELECTION_V1
status = PEDICULARIS_G_DEVICE_SELECTED_FOR_CONFIRMATORY_QUALIFICATION.
```

A method that failed hard exploratory validity cannot be selected.

## Device identity is not a 41st F0 threshold

The existing G F0 threshold set remains 19 fields and the whole F0 set remains
40 fields.

`selected_exclusion_method` is categorical protocol metadata, not a numeric or
boolean biological gate. It therefore is not inserted into
`prospective_freeze.threshold_basis` and does not change the 5 + 20 + 7 + 8
source accounting.

Instead, the positive device-selection receipt is a separate required input to
F0 config assembly.

## Step 3 — F0 propagation

`scripts/assemble_pedicularis_f0_configs.py` now requires the positive G
device-selection receipt in addition to CAL-A, CAL-B and CAL-C.

The assembled G config receives:

```text
method_gate.selected_exclusion_method = <prospectively selected method>.
```

The F0 receipt preserves the source selection receipt and basis note.

## Step 4 — confirmatory V4 enforcement

`scripts/evaluate_pedicularis_predator_method.py` requires:

```text
all confirmatory EXCLUDED rows use one method
AND
that method exactly equals method_gate.selected_exclusion_method.
```

A confirmatory dataset using a different barrier therefore fails even if its
effect sizes look favorable.

## Claim ceiling

An exploratory hard-validity screen can reject unusable devices early.

A positive device-selection receipt establishes only a prospectively frozen
method identity that survived hard exploratory method checks.

It does not validate predator reduction, selectivity, timing bounds, P0/P1/G
readiness, causal compromise, conflict budget L, or dimensional release.
