# SCH macroecology H2 context evidence — Batch 1

## Purpose

H2 requires local ecological contexts, not merely a statement that a study is spatially or experimentally heterogeneous.

Batch 1 therefore separates:

1. **context evidence** — the source tells us what contexts exist and what object contains the local information;
2. **materialized context cases** — one row per local population/year/treatment context whose geometry is actually source-resolved.

This prevents a study reporting 14 or 69 populations from contributing 14 or 69 model rows before those local observations have been extracted.

## Batch-1 evidence

```text
context-evidence rows             6
canonical axes represented         5
source records                     5
local model cases materialized     1
evidence rows still pending        5
```

### Gentiana lutea — focal Torrestío population

The focal population is the first promoted H2 local case.

```text
canonical axis: Gentiana_lutea_color_axis
context:        Torrestío, León, Spain
pollinator:     yellow favored
seed predator: yellow favored through lower seed-predation cost
geometry:       ALIGNMENT / REINFORCEMENT
```

This is retained as the reference local context for the canonical colour axis.

### Gentiana lutea — 12-population study

The broader source provides the context structure but is not yet expanded to 12 population rows.

```text
contexts: 12 populations, 2010-2011
pollinator color response: varies among populations
seed-predator color response: no overall color effect detected
local selection coefficients: source table required
```

The population-specific geometry requires the published population selection table before promotion.

Thus the canonical axis remains known to be context-variable, but the 12 local cases are not yet model rows.

### Gymnadenia conopsea — 2 × 2 factorial context

Two canonical axes use the same factorial context structure:

- flowering phenology;
- spur length.

The source reports four pollination × herbivory treatment groups.

At the source-summary level:

```text
phenology -> conflict + cancellation
spur      -> reinforcement
```

However, exact local treatment-group gradients are stored in Appendix A Table A2 / Ecological Archives E096-022.

Therefore:

```text
factorial structure resolved = YES
four local treatment outcomes materialized = NO
```

No treatment cell is promoted to a local H2 case until the table values are inspected.

### Pedicularis rex — geographic mosaic

The source design contains:

```text
14 populations with floral/pollination information
12 populations with seed-predation / seed-production information
```

The canonical corolla-exsertion axis is conflicted overall.

The key H2 signal is that the pollinator-associated component is comparatively consistent whereas seed-predator-mediated selection changes geographically.

Local population geometry remains pending the supplement / population table.

No 14-row pseudo-dataset is created from the population count alone.

### Primula farinosa — population × experiment × time programme

The broader programme contains many populations and long-term observations, but experimental population subsets differ among studies.

The source programme supports:

- pollinator-versus-grazer conflict on scape-height morph;
- spatial variation in their relative strengths;
- morph-frequency change over time;
- experimental grazer exclusion effects.

But the programme-level count of populations is not a context-case table.

Population/treatment/year rows require source-specific extraction before H2 modeling.

## Promotion states

Batch 1 uses four explicit states:

```text
LOCAL_CONTEXT_GEOMETRY_RESOLVED
LOCAL_CONTEXT_TABLE_REQUIRED
CONTEXT_STRUCTURE_RESOLVED_LOCAL_OUTCOMES_PENDING
LOCAL_CONTEXT_SOURCE_EXTRACTION_REQUIRED
```

Current counts:

```text
LOCAL_CONTEXT_GEOMETRY_RESOLVED                 1
LOCAL_CONTEXT_TABLE_REQUIRED                    2
CONTEXT_STRUCTURE_RESOLVED_LOCAL_OUTCOMES_PENDING 2
LOCAL_CONTEXT_SOURCE_EXTRACTION_REQUIRED        1
```

## Why this matters

The distinction is essential:

```text
number of contexts reported
!=
number of model cases
```

Without this gate, the macroecology layer would inflate replication by converting study descriptions into pseudo-observations.

The current implementation instead requires a traceable source object for every local geometry.

## Current H2 status

```text
H2 context evidence       READY
H2 local cases            1
H2 model                  NOT READY
context-switch prevalence NOT ESTIMATED
```

The first real context case is *Gentiana lutea* at Torrestío.

The next promotions should come from:

1. *Gentiana* population-selection table;
2. *Gymnadenia* Appendix A Table A2;
3. *Pedicularis* population supplement;
4. *Primula farinosa* experiment/population tables.

## Claim ceiling

The current evidence supports that context dependence exists and that at least one canonical axis changes ecological geometry across sources.

It does **not** yet support:

- a frequency of geometry switching;
- a mixed-effects H2 model;
- treating reported population counts as replicated cases;
- filling missing local component signs from study-level summaries.
