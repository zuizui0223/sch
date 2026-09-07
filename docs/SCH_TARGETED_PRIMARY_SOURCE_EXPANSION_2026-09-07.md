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

### Satyrium longicauda — manipulated gender compromise surface

Primary source: Ellis & Johnson 2010, *International Journal of Plant Sciences*, DOI `10.1086/656351`.

In the Entabeni population, maximum pollen export occurred at the intermediate spur-length manipulation, whereas female fitness was highest at the maximum spur length. In one year, total fitness (pollen export + receipt) was hump-shaped. The authors explicitly describe the likely evolutionary compromise as lying above the male optimum.

Registered class:

```text
COMBINED_INTERMEDIATE_OR_COMPROMISE
```

This is the strongest new match to the SCH geometry because one manipulated coordinate is evaluated through male and female functions and a combined fitness surface. However, only spur shortening was experimentally available, so the upper side of the female fitness function was not mapped. The female optimum therefore cannot be declared fully bounded within the tested range.

### Gymnadenia conopsea — factorial cancellation of agent-specific selection

Primary source: Sletvold, Moritz & Agren 2015, *Ecology*, DOI `10.1890/14-0119.1`.

A factorial manipulation of pollination and herbivory separated the two selective agents. Pollinators selected for later flowering, whereas herbivores selected for earlier flowering with similar additive strength. Their opposing effects produced no net selection on flowering phenology in the observed context. The paper explicitly notes that the direction of selection, and therefore the favored flowering time, should vary with the relative intensity of the mutualistic and antagonistic interactions.

Registered class:

```text
CONTEXT_WEIGHT_SHIFT
```

This is a strong intervention-based weight-shift anchor because the two agents are experimentally separated and act in opposite directions on the same coordinate. It is not coded as `DIRECT_CONTEXT_DRIVEN_OPTIMUM_MOVEMENT`, because the study does not experimentally traverse several interaction-weight regimes and re-estimate a nonlinear optimum under each regime.

## What remains genuinely missing

The targeted search now recovers one bounded combined-compromise surface in addition to recurrent opposing-direction and context-shift evidence. The strongest remaining SCH-specific gaps are:

```text
SEPARATED_OPTIMA_BOTH_FULLY_IDENTIFIED    still open
COMBINED_INTERMEDIATE_OPTIMUM             recovered once, replication needed
DIRECT_CONTEXT_DRIVEN_OPTIMUM_MOVEMENT    still open
```

The next retrieval round should therefore search explicitly for studies that manipulate one trait bidirectionally over a broad enough range to estimate both component optima and then change the ecological weights experimentally.
