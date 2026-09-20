# SCH macroecology H2 measurement layers and change types V1

## Why H2 needs a second gate

A repeated ecological context can contain very different amounts of information.

These are not equivalent observations:

- knowing that a study sampled many populations;
- knowing local seed-predator pressure;
- knowing local total/net selection on the focal trait;
- knowing both local functional components on the same trait and common outcome.

H2 therefore separates **what the source supports** from **what has actually been materialized as a model case**.

## Measurement layers

The ordered H2 measurement layers are:

```text
LOCAL_GEOMETRY
  both local functional routes + common outcome resolve a local geometry

LOCAL_NET_SELECTION
  local realized/net trait effect is resolved,
  but the two functional components are not

LOCAL_ANTAGONIST_PRESSURE
  local antagonist intensity/outcome is resolved,
  but local trait geometry is not

CONTEXT_STRUCTURE_ONLY
  local contexts are known,
  but their outcome values have not been materialized
```

The order describes information content, not biological importance.

A source-supported layer may be higher than the currently materialized layer.

## Current measurement state

The first registry contains eight measurement records across six canonical trait axes.

Source-supported layer:

```text
LOCAL_GEOMETRY              3
LOCAL_NET_SELECTION         4
LOCAL_ANTAGONIST_PRESSURE   1
```

Currently materialized layer:

```text
LOCAL_GEOMETRY              2
LOCAL_NET_SELECTION         1
CONTEXT_STRUCTURE_ONLY      5
```

Five of eight records therefore remain below the measurement level the underlying source can in principle support.

Only three local context rows currently count as H2 model cases:

1. *Gentiana lutea* colour at Torrestío — LOCAL_GEOMETRY;
2. *Caryopteris divaricata* with natural nectar robbery — LOCAL_GEOMETRY;
3. *Caryopteris divaricata* under robber exclusion — LOCAL_NET_SELECTION.

## Pedicularis rex illustrates the distinction

The primary article reports:

```text
pollination/floral contexts                     14 populations
seed predation / seed production contexts       12 populations
same-individual linkage through seed outcomes    7 populations
population-specific local geometry cases         0 materialized
```

The seven individually linked populations are 1, 3, 5, 8, 9, 10 and 11.

In populations 2, 4, 6, 7 and 12, plant labels were lost between floral/pollination measurements and seed-outcome measurements. Those populations can support population-level antagonist pressure but cannot be silently promoted to individual trait -> predation / final-fitness geometry.

This gives a useful H2 distinction:

```text
local antagonist pressure
!=
local two-function trait geometry
```

The source also indicates that the pollinator-mediated relationship is comparatively geographically consistent while the seed-predator-mediated component varies strongly among populations.

Therefore the strongest current H2 statement for *Pedicularis* is a **component-weight shift within an overall conflicted system**, not a demonstrated population-by-population geometry-class switch.

## Source-object registry

Every unmaterialized promotion target now points to a stable source-object ID.

### Gentiana

```text
object: Gentiana_S3
DOI: 10.1371/journal.pone.0132522.s004
target: LOCAL_NET_SELECTION
status: route resolved, DOC bytes not materialized
```

Do not digitize Fig. 4 instead of the published S3 table.

Even after S3 recovery, population-specific total selection does not automatically provide population-specific pollinator and seed-predator components.

### Gymnadenia

```text
object: Gymnadenia_A2
Ecological Archives: E096-022-A1
target: LOCAL_NET_SELECTION
status: route resolved, table bytes not materialized
```

Table A2 contains treatment-group selection gradients ± SE for the four pollination × herbivory groups.

Treatment-group net gradients can be materialized before mediated agent contrasts. The latter require valid contrast uncertainty and must not assume missing covariance.

### Pedicularis

Resolved supplement object names:

```text
Pedicularis_S1
  supp_mcw097_aob-16074-s01.doc

Pedicularis_S2
  supp_mcw097_aob-16074-s02.xls

Pedicularis_AppendixS1
  supp_118_2_227__index.html
```

The supplement bytes remain blocked in the current runtime, but object identity is resolved.

### Primula farinosa

The source programme contains broad surveys, experimental population subsets and long-term follow-up.

The programme-level 69-population count is not a context-case denominator. Individual primary-source population × manipulation × time objects still need to be frozen.

## Context change is not one biological outcome

The current H2 seed already contains at least four distinct forms of ecological change.

### 1. Geometry-class switch

*Gentiana lutea* colour:

```text
focal context:
  reinforcement

broader spatial context:
  one-sided / null with heterogeneous pollinator selection
```

Exact population-by-population transitions remain pending S3 extraction.

### 2. Geometry disappearance

*Caryopteris divaricata* corolla tube:

```text
robbers present:
  short-tube realized advantage

robbers excluded:
  no detected tube-length effect on pollination or seed production
```

This is a within-source experimental H2 switch already materialized.

### 3. Component-weight shift

*Pedicularis rex* corolla exsertion:

```text
overall geometry:
  conflict

pollinator component:
  comparatively consistent across populations

seed-predator component:
  strongly geography dependent
```

The change is currently one of **weight**, not a demonstrated sign/class change.

### 4. Component-weight shift with evolutionary response

*Primula farinosa* scape-height morph:

```text
pollinator-vs-grazer balance varies among populations
-> selection differs
-> morph-frequency change follows
-> grazer exclusion shifts morph frequencies in long-term follow-up
```

Local source-specific rows remain pending.

## Consequence for H2 modeling

A future H2 model must not collapse all four change types into one binary `context_dependent` outcome.

The likely hierarchy is:

```text
context change
  ├─ geometry class switch
  ├─ geometry disappearance
  ├─ component-weight shift
  └─ consumer-role switch / benefit-cost coupling
```

The current seed is too small for inference on these change types.

For now they are **mechanistically distinct descriptive outcomes** that guide context-case extraction.

## Current fail-closed status

```text
H2_MEASUREMENT_RECORDS = 8
CANONICAL_AXES_REPRESENTED = 6

SOURCE_SUPPORTED_LOCAL_GEOMETRY = 3
MATERIALIZED_LOCAL_GEOMETRY = 2

SOURCE_SUPPORTED_LOCAL_NET_SELECTION = 4
MATERIALIZED_LOCAL_NET_SELECTION = 1

SOURCE_SUPPORTED_LOCAL_ANTAGONIST_PRESSURE = 1
MATERIALIZED_LOCAL_ANTAGONIST_PRESSURE = 0

MATERIALIZED_H2_MODEL_CASES = 3

SOURCE_OBJECTS_REGISTERED = 6
SOURCE_OBJECT_BINARIES_MATERIALIZED = 0
EXACT_LOCAL_VALUES_EXTRACTED_FROM_PENDING_OBJECTS = 0

H2_MODEL = NOT READY
```

The scientific gain is that source recovery can now increase H2 resolution without changing the meaning of existing cases or inflating model N.
