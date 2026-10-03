# SCH Pedicularis primary-method adjudication v1

## Purpose

Broad literature screening is already stopped. Three primary binaries can still
plausibly change the historical direct-evidence status:

```text
Jing et al. 2013 Methods   -> P1 treatment identity
Wang 1998 PDF              -> possible P1 treatment/outcome
Tang 2011 thesis           -> possible independent-G method.
```

This adjudicator defines what happens **after** one of those binaries is
retrieved. It prevents ambiguous phrases such as `hand pollination` or
`predator experiment` from being promoted by interpretation alone.

Machine ledger:

```text
empirical/architecture/PEDICULARIS_PRIMARY_METHOD_ADJUDICATION_V1.csv
```

Audit:

```bash
python scripts/adjudicate_pedicularis_primary_methods.py
```

## Three evidence levels for P1

### 1. Direct focal supplementation effect

A historical P. rex study may be called a direct focal supplementation effect
only if primary Methods show:

```text
open natural-pollination control
+ supplemental outcross pollen
+ supplemented flowers remain open to natural visitors
+ sample size reported
+ reproductive outcome reported.
```

A bagged self/cross breeding-system assay does not qualify.

### 2. Registered P1 estimand

To match the current SCH P1 pilot estimand, the study must additionally report
a pre-predation reproductive endpoint such as initial seed set or another
prospectively equivalent pollen-limitation endpoint.

### 3. Registered protocol-family compatibility

Full protocol-family compatibility further requires standardized multi-donor
cross-pollen supplementation. A historical single-donor treatment can still
recover a focal supplementation effect without being identical to the current
registered field protocol.

## Three evidence levels for G

### 1. Direct focal independent G

Primary P. rex Methods must show:

```text
predator-exposed control
+ predator access/exclusion intervention
+ water-y held fixed
+ sample size reported
+ seed-predation outcome.
```

Water retained/drained never qualifies because it manipulates the later BITA-y
axis rather than independent predator access.

### 2. Registered G effect estimand

A final reproductive outcome must also be reported.

### 3. Registered protocol-family compatibility

The historical intervention must additionally preserve:

```text
natural pollination
qualified timing or local barrier placement
pollinator-entry geometry.
```

A cage that works only because natural pollinators are excluded and replaced by
hand crossing may recover barrier efficacy, but not the registered selective G.

## Current three-asset state

```text
Jing2013   binary not retrieved; hand treatment identity unresolved
Wang1998   611-KB PDF listed; binary not retrieved
Tang2011   full abstract recovered; natural-history/selection only in abstract
```

Therefore the current adjudication result remains:

```text
direct focal P1 effect          false
registered P1 estimand          false
registered P1 protocol family  false
direct focal independent G      false
registered G effect estimand    false
registered G protocol family    false.
```

## Historical recovery does not freeze F0

Even if a primary binary recovers a direct focal P1 or G effect, the same
population/season prospective calibration package remains required.

The adjudicator therefore always keeps:

```text
direct_f0_values_recovered = 0
field_calibration_still_required = true.
```

Historical recovery can reduce uncertainty and change the interpretation of
what has already been demonstrated in P. rex. It cannot retroactively create
the prospectively frozen CAL-A/B/C and F0 receipts.

## Update rule after binary retrieval

After obtaining a primary binary:

1. record an exact Methods/Table/page locator;
2. fill only facts directly supported by that primary text;
3. rerun the adjudicator;
4. update P1/G historical evidence status only if the machine rule promotes it;
5. keep field calibration unless the experimental programme itself is changed
   prospectively.

## Claim ceiling

This layer adjudicates historical primary methods against registered
intervention definitions. It does not infer missing Methods, digitize figures
into invented exact values, or replace focal prospective validation.
