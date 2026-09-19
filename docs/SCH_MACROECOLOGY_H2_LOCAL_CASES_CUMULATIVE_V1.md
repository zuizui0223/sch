# SCH macroecology H2 local context cases — cumulative V1

## Current local-case state

After two H2 context-evidence batches:

```text
context-evidence rows               7
canonical axes with context evidence 6
source records                      6

materialized local cases            3
canonical axes with local cases     2
biological clusters with local cases 2
```

The three local cases are:

1. *Gentiana lutea* colour at the focal Torrestío population;
2. *Caryopteris divaricata* corolla tube with natural nectar robbing;
3. the same *Caryopteris* corolla-tube axis under nectar-robber exclusion.

## Caryopteris provides the first within-source H2 switch

The canonical corolla-tube axis is a role-dependent consumer system.

### Context 1 — nectar robbers present

The source reports:

```text
short corolla tube
-> lower nectar-robbing intensity
-> higher legitimate visitation
-> higher seed production
```

At the realized plant-performance level, both ecological routes favor shorter tubes.

This context is therefore recorded as:

```text
ALIGNMENT / REINFORCEMENT
role architecture = ROLE_DEPENDENT
```

It is not mixed into fixed-role H1 because the bumblebee visitor guild can express legitimate and robbing behavior.

### Context 2 — nectar robbers excluded

When nectar robbers are experimentally excluded, the source reports no difference between long- and short-tubed plants in pollination or seed production.

The local state is recorded as:

```text
CONSUMER_REMOVED_NO_STATIC_GEOMETRY
```

rather than as conflict, reinforcement, or one-sided geometry.

The key H2 transition is therefore:

```text
robbers present
  -> short-tube realized advantage

robbers excluded
  -> tube-length effect on pollination/reproduction disappears
```

This is stronger evidence for context dependence than a study-level statement that robbing intensity varies.

## Current local geometry counts

Across the three actually materialized local cases:

```text
ALIGNMENT / REINFORCEMENT             2
CONSUMER_REMOVED_NO_STATIC_GEOMETRY   1
```

Consumer-role composition:

```text
NET_ANTAGONISTIC   1
ROLE_DEPENDENT     2
```

These numbers are bookkeeping only; with two canonical axes they are not an inferential H2 sample.

## Pending evidence remains larger than model N

Five of seven evidence rows still lack promoted local cases.

These are:

- *Gentiana* 12-population selection table;
- *Gymnadenia* phenology factorial table;
- *Gymnadenia* spur factorial table;
- *Pedicularis* population selection supplement;
- *Primula farinosa* population/experiment/time tables.

Thus:

```text
reported contexts
>>
materialized H2 model cases
```

and only the latter count may enter future H2 model diagnostics.

## Ecological implication

Caryopteris makes the ecological interpretation sharper:

> **The trait geometry itself can disappear when the consumer regime changes.**

That is different from merely changing the magnitude of a fixed trade-off.

The source supports a transition from a realized short-tube advantage in the presence of robbers to no detected tube-length effect on pollination or seed production after robber exclusion.

This supports treating consumer regime as part of the definition of realized geometry.

## H2 model boundary

Current state:

```text
H2 local cases = 3
H2 canonical axes with cases = 2
H2 clusters with cases = 2
H2 model = NOT READY
```

No frequency, odds ratio, or context-switch regression is licensed.

## Next priority

Continue with source-resolved context extraction in this order:

1. Gentiana population selection table;
2. Gymnadenia Appendix A Table A2;
3. directly reported role-switch contrasts in blueberry / sesame;
4. Pedicularis population supplement;
5. Primula farinosa programme decomposition.

The general rule remains:

```text
reported context count != model N
```
