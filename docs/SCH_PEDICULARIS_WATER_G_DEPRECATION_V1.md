# Pedicularis water-as-G deprecation note v1

## Decision

The earlier Pedicularis SCH prototype used:

```text
G0 = water retained
G1 = bract drained.
```

That mapping is **deprecated for the dissertation-level SCH -> BITA causal chain**.

Reason:

```text
water defence is also the proposed Chapter-2 y axis.
```

If SCH defines its Chapter-1 reference optima by toggling water defence and BITA then tests whether the same water-defence state releases x toward that reference, the Chapter-2 release test becomes partially circular. In particular, the protected-state x optimum can become the reference that the protected-state BITA surface is asked to approach.

## Corrected architecture

SCH now holds water defence fixed and manipulates antagonist pressure independently:

```text
P0 = supplemental pollen / pollination dependence relaxed
P1 = natural pollination / pollination dependence active

G0 = seed predator independently excluded
G1 = seed predator exposed

water y = fixed across all SCH cells.
```

BITA then varies the water-defence axis:

```text
y0 = drained / water defence disabled
y1 = protected / water defence active.
```

This separates:

```text
Chapter 1 functional environment manipulation G
from
Chapter 2 trait/function axis y.
```

## Status of the old water experiment

The 2015 drainage experiment remains valuable evidence. It establishes that water-filled cupulate bracts have a causal antagonist-reducing function and showed no detected effect on legitimate pollinator visitation or initial seed set in the published experiment.

It is now positioned as:

```text
BITA D1a functional-y evidence / selectivity precedent
```

rather than as the definitive SCH G intervention.

The old files using `SCH_PEDICULARIS_ANTAGONIST_WEIGHT_V1` remain as provenance for that water-state audit but **cannot unlock the corrected SCH full-surface readiness gate**.

## Corrected registered files

```text
PEDICULARIS_PREDATOR_WEIGHT_TEMPLATE_V2.csv
PEDICULARIS_PREDATOR_WEIGHT_CONFIG_TEMPLATE_V2.json
scripts/evaluate_pedicularis_predator_weight.py
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V2
PEDICULARIS_FULL_SURFACE_TEMPLATE_V2.csv
PEDICULARIS_FULL_SURFACE_CONFIG_TEMPLATE_V2.json.
```

## Claim consequence

This correction changes the empirical interpretation, not the general theory.

Pedicularis remains a strong programme candidate, but its decisive new Stage G is now:

> can seed-predator pressure be selectively suppressed or restored while exsertion, pollen receipt, pollinator access, and water defence remain effectively fixed?

Until that passes, Pedicularis is not ready for the complete Chapter-1 causal surface.
