# SCH fitness-scale conflict budget v1

## Purpose

The main critical-point obstacle after defining `s L_S* = K` is units. SCH's directly identified `z_P*`, `z_G*`, and `z_C*` are trait-space quantities, whereas the architecture threshold is a fitness comparison.

This note defines a fail-closed route from a positive SCH causal surface to an empirical **focal-component conflict budget** on one common reproductive scale.

## Prerequisite

Run only after:

```text
SCH causal compromise surface: MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
+
pure-function/component upgrade: CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED.
```

The second gate is essential because separate component maxima are not interpretable if the focal causal component surfaces change their optima strongly across the other consumer state.

## Four state surfaces

SCH observes

```text
W00(z)
W10(z)
W01(z)
W11(z).
```

Define two context-averaged causal component curves:

```text
F1_bar(z)
 = 0.5 * [(W10-W00) + (W11-W01)]

F2_bar(z)
 = 0.5 * [(W01-W00) + (W11-W10)].
```

These are symmetric averages across the other consumer state.

## Exact identity

Adding them gives

```text
F1_bar + F2_bar
= W11 - W00.
```

This is exact algebra, not an approximation. It means the two averaged focal components partition the **combined-state reproductive contribution above the P0G0 baseline** even when a P×G interaction is present; the symmetric averaging distributes that interaction across the two component curves rather than discarding it.

The implementation regression-checks this identity coefficient-wise.

## Conflict budget

On their common z support define

```text
C_independent
 = max_z F1_bar(z)
 + max_z F2_bar(z)

C_shared
 = max_z [F1_bar(z)+F2_bar(z)].
```

Then

```text
L_S,component*
 = C_independent - C_shared
 >= 0.
```

This is the focal-component reproductive amount unavailable because both functions must use the same z coordinate.

It is the empirical quantity closest to the quadratic `L_S*` after the component-identification gate.

## What is excluded

`W00(z)` is deliberately excluded from this component conflict budget. Therefore:

```text
L_S,component*
!= total whole-organism architecture loss
!= construction cost
!= maintenance cost
!= K.
```

This separation is desirable. BITA's architecture cost lane should measure the additional cost of maintaining/using the differentiated architecture rather than hide it inside the SCH conflict estimate.

## Quadratic reference check

If

```text
F1(z) = 10 - (z-2)^2
F2(z) = 10 - (z+2)^2,
```

then

```text
max F1 = 10
max F2 = 10
max(F1+F2) = 12 at z=0
```

so

```text
L_S,component* = 10+10-12 = 8.
```

The same value follows from the ideal quadratic formula with unit weights and function-optimum distance 4:

```text
L_S* = [1*1/(1+1)] * 4^2 = 8.
```

The test suite recovers this value exactly from synthetic four-state data and cluster bootstrap.

## Critical-point export

A positive receipt exports

```text
criticality_export.L_S_component
criticality_export.L_S_component_95_ci
fitness_scale_id.
```

BITA may compare this against `K/s` only when:

1. `s` is estimated for the same biological context;
2. `K` is expressed on a compatible reproductive-fitness scale;
3. the shared and differentiated experiments use a declared cross-scale mapping;
4. the same focal component definition is retained.

Then the empirical Chapter-1 projection is

```text
L_S,component* - K/s = 0.
```

This finally puts the Chapter-1 conflict side and Chapter-2 architecture side into common units.

## Current empirical status

The estimator is now implemented, but no current biological dataset in SCH has yet passed the full causal-compromise plus context-stable component-optimum sequence. Therefore:

```text
FITNESS_SCALE_CONFLICT_BUDGET_ANALYZER: IMPLEMENTED
BIOLOGICAL_L_S_COMPONENT_RECEIPT:       NOT_YET_EXECUTED
NUMERIC_C2_IN_NATURE:                  NOT_YET_IDENTIFIED.
```

## Implementation

- `scripts/estimate_sch_conflict_budget.py`
- `empirical/architecture/SCH_CONFLICT_BUDGET_CONFIG_TEMPLATE_V1.json`
- `tests/test_sch_conflict_budget.py`
