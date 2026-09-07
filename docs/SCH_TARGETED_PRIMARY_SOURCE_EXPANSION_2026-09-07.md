# SCH targeted primary-source expansion — 2026-09-07

## Purpose

Fill underrepresented reality-pattern classes after moving SCH to the sequence

```text
theory -> observable signatures -> source-adjudicated synthesis -> focal experiment last
```

This is a targeted expansion, not a completed systematic review and not a prevalence estimate.

## New high-confidence anchors

### Silene stellata — opposite signs through male and female function

Primary source: Zhou et al. 2020, *Evolution*, DOI `10.1111/evo.13965`.

The study reports opposite-sign sex-specific selection on petal dimensions. The authors interpret the conflict as positive male-function selection associated with pollen export by adult *Hadena ectypa* versus negative female-function selection associated with oviposition and subsequent fruit predation.

Registered class:

```text
OPPOSING_DIRECTION
```

Claim ceiling: this is strong conflicting-selection evidence, but the repository does not reconstruct separate nonlinear state optima `z_1*`, `z_2*`, and a combined optimum from the source.

### Erysimum mediohispanicum — functional-weight/context shift

Primary source: Herrera 2003, *The American Naturalist*, DOI `10.1086/376574`.

Ungulate exclusion revealed pollinator-mediated selection on multiple floral and plant traits. With ungulates present, selection on floral traits disappeared and selection strength on plant morphology decreased.

Registered class:

```text
CONTEXT_WEIGHT_SHIFT
```

Claim ceiling: this demonstrates a strong context-dependent change in the effective selection surface, not separated function-specific optima.

### Ipomopsis spp. and hybrids — sequential filters

Primary source: Campbell et al. 2022, *The American Naturalist*, DOI `10.1086/716740`.

The study decomposes female fitness into seed initiation during pollination and escape from seed predation and estimates selection on multiple floral traits across the two sequential life-history stages. Directional and quadratic selection were stronger during seed initiation than seed predation.

Registered class:

```text
SEQUENTIAL_FILTER_COMBINATION
```

Claim ceiling: this shows how multispecies filters combine across life stages; it is not a direct one-coordinate SCH optimum decomposition.

## What remains genuinely missing

The targeted search strengthened opposing-direction and context-shift recurrence, but the strongest SCH-specific signatures remain sparse:

```text
SEPARATED_OPTIMA_IDENTIFIED             still open
COMBINED_INTERMEDIATE_OPTIMUM           still open as a repeated class
DIRECT_CONTEXT_DRIVEN_OPTIMUM_MOVEMENT  still open
```

Therefore the next retrieval round should search explicitly for studies reporting nonlinear fitness functions or experimentally shifted optima rather than adding more generic opposing-selection examples.
