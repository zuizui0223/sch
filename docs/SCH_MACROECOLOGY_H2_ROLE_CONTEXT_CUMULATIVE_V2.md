# SCH macroecology H2 role-context cases — cumulative V2

## Current state

Three source-resolved H2 context batches now contain:

```text
context-evidence rows                10
canonical axes with context evidence  9
source records                        8

materialized local cases             10
canonical axes with local cases       5
biological clusters with local cases  4
```

The local cases now span two distinct ecological layers:

```text
plant-performance geometry
consumer-role / foraging-behavior context
```

These are not collapsed into one outcome.

## Blueberry — floral morphology switches the role of the same visitor

In highbush blueberry, cultivar floral morphology changes how managed honey bees use flowers.

### Duke

The source reports wider flowers and higher honey-bee visit rates relative to Bluecrop and Draper.

Apis mellifera visits Duke flowers legitimately.

Local state:

```text
visitor role = legitimate
corolla access = wide
```

### Bluecrop

Bluecrop has long, narrow flowers.

The same honey-bee species is reported as a frequent nectar robber.

Local state:

```text
visitor role = nectar robber
corolla access = long / narrow
```

All observed bumble-bee visits are legitimate.

Thus the H2 result is not a fixed plant-fitness trade-off. It is a morphology-dependent switch in visitor role:

```text
cultivar floral morphology
-> legitimate versus robbing use by Apis mellifera
```

The crop-yield result is programme-level and is not used to invent a cultivar-specific fitness geometry.

## Sesame — corolla access changes robbing behavior

The sesame experiment manipulates corolla access directly.

Three local contexts are materialized.

### Normal corolla

```text
visitor abundance = 2.24 ± 1.45 / flower / 10 min
robbing = higher than both short-tube treatments
```

The exact normal-treatment robbing percentage remains in Table 3 and is not back-calculated.

### Short tube, no landing space

```text
visitor abundance = 1.08 ± 0.98
robbing = 11.97 ± 4.69 %
```

Shortening the tube lowers robbing, but removing landing space also impedes legitimate entry.

### Short tube, landing space retained

```text
visitor abundance = 2.06 ± 1.29
robbing = 12.37 ± 7.97 %
```

Visitor abundance is close to the normal-flower context while robbing is lower.

This separates two aspects of floral access:

```text
tube accessibility
+
landing geometry
```

rather than reducing the treatment to a single "short flower" effect.

## Sesame — resource state changes the same visitors' tactics

A second canonical axis is nectar availability.

At peak foraging time:

### Low-resource control

```text
visitor abundance = 2.24 ± 1.45
robbing = 19.06 ± 5.72 %
```

### High nectar + high pollen

```text
visitor abundance = 3.01 ± 1.65
robbing = 2.26 ± 3.68 %
```

Thus higher resource availability is associated with more visitors but much less robbing.

The primary source also reports a high-nectar pollen-less context with robbing of 2.99 ± 4.24 %, but that treatment is retained as source evidence rather than promoted here because the current text extraction does not preserve the same full abundance tuple.

## Reproductive consequence in sesame

The study separately shows that:

- open visitation increases reproductive success relative to pollinator exclusion;
- single legitimate and single robbing visits do not differ significantly in seed set;
- multiple-visit sequences beginning with a robbing visit do not significantly reduce fruit or seed set.

Therefore sesame nectar robbing is interpreted by the source as commensal with respect to measured reproduction.

For H2 this means:

> **A switch toward robbing behavior does not automatically imply a switch toward plant-fitness antagonism.**

The role-behavior contexts are therefore coded as `ROLE_BEHAVIOR_CONTEXT`, not as conflict.

## Cumulative local context state

Across all ten currently materialized H2 cases:

```text
ALIGNMENT / REINFORCEMENT               2
CONSUMER_REMOVED_NO_STATIC_GEOMETRY     1
ROLE_BEHAVIOR_CONTEXT                   7
```

Consumer-role status:

```text
NET_ANTAGONISTIC   1
ROLE_DEPENDENT     9
```

Five cases are explicit shifts away from their registered reference context.

## Ecological implication

The H2 layer now distinguishes at least three forms of context dependence:

1. **geometry changes** — e.g. Gentiana across sources/populations;
2. **geometry disappears when an antagonist regime is removed** — Caryopteris robber exclusion;
3. **consumer role changes while plant-fitness effect can remain neutral** — blueberry and sesame.

This sharpens the main ecological statement:

> **Context can change not only the strength or sign of selection, but also which functional role an interacting animal expresses.**

## Inference boundary

Despite ten local cases, H2 is not model-ready.

Current local cases represent only:

```text
5 canonical axes
4 biological clusters
```

and nine of ten cases belong to role-dependent consumer systems.

The remaining source-table targets for fixed-role H2 remain high priority:

- Gentiana population S3 table;
- Gymnadenia Appendix A Table A2;
- Pedicularis population supplement;
- Primula farinosa experiment/population tables.

## Status

```text
H2_CONTEXT_EVIDENCE_ROWS = 10
H2_LOCAL_CASES = 10
H2_AXES_WITH_LOCAL_CASES = 5
H2_CLUSTERS_WITH_LOCAL_CASES = 4

ROLE_BEHAVIOR_CONTEXT_CASES = 7
FIXED_ROLE_LOCAL_CASES = 1

H2_MODEL = NOT READY
H2_PREVALENCE = NOT ESTIMATED
```
