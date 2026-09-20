# SCH H2 Gymnadenia Appendix A Table A2 recovery V1

## Source recovery

The Ecological Archives Appendix A for Sletvold, Moritz & Ågren (2015) is now source-inspected directly.

Source:

`https://esapubs.org/archive/ecol/E096/022/appendix-A.php`

Table A2 reports phenotypic linear selection gradients (beta ± SE) for four pollination × herbivory treatment groups in *Gymnadenia conopsea*.

The four treatment states are:

```text
C+H   open-pollinated control + natural herbivory
C+E   open-pollinated control + herbivores excluded
HP+H  supplemental hand pollination + natural herbivory
HP+E  supplemental hand pollination + herbivores excluded
```

## Flowering phenology

Treatment-cell selection gradients:

```text
C+H    beta = -0.0042 ± 0.054
C+E    beta =  0.094  ± 0.031
HP+H   beta = -0.16   ± 0.056
HP+E   beta = -0.066  ± 0.028
```

The realized net selection on flowering start therefore changes markedly across the factorial contexts.

Positive beta corresponds to selection toward later flowering; negative beta corresponds to selection toward earlier flowering.

## Spur length

Treatment-cell selection gradients:

```text
C+H    beta =  0.18  ± 0.057
C+E    beta =  0.077 ± 0.035
HP+H   beta =  0.083 ± 0.053
HP+E   beta = -0.042 ± 0.029
```

Net selection is positive in three treatment cells and has a negative point estimate in the hand-pollinated herbivore-exclusion cell.

The local treatment cells are therefore source-resolved as **net selection**, not as four agent-specific geometries.

## Agent-mediated contrast point estimates

Table A2 also gives the mediated-selection point estimates.

Pollinator-mediated selection:

```text
Delta beta_poll = beta_C - beta_HP
```

Phenology:

```text
natural herbivory      +0.16
herbivores excluded    +0.16
```

Spur length:

```text
natural herbivory      +0.10
herbivores excluded    +0.12
```

Herbivore-mediated selection:

```text
Delta beta_herb = beta_H - beta_E
```

Phenology:

```text
open pollination       -0.098
hand pollination       -0.094
```

Spur length:

```text
open pollination       +0.10
hand pollination       +0.13
```

These point directions recover the paper-level biological result:

```text
phenology:
  pollinators -> later
  herbivores  -> earlier
  => opposing component directions

spur length:
  pollinators -> longer
  herbivores  -> longer
  => reinforcing component directions
```

## Uncertainty boundary

The treatment-cell beta values have reported SE.

The mediated contrast rows in Table A2 do not provide contrast SE/covariance in the table.

Therefore SCH records:

```text
treatment-cell LOCAL_NET_SELECTION = MATERIALIZED

mediated component direction       = DESCRIPTIVE POINT ESTIMATE

local agent-contrast uncertainty   = NOT IDENTIFIED FROM TABLE A2 ALONE
```

The mediated contrast point estimates are not promoted to covariance-aware local geometry cases.

## H2 effect

This recovery adds:

```text
8 new local plant-performance cases
2 canonical trait axes
1 biological cluster
```

Current H2 state after recovery:

```text
total local H2 cases                  18
plant-performance cases               11
role-behavior cases                     7

plant-performance canonical axes        4
plant-performance biological clusters   3
plant-performance repeated axes          3
```

The plant-performance layer therefore becomes much less dominated by role-behavior examples.

However, the registered H2 modelability gate still fails:

```text
minimum cases per layer      12   current 11
minimum axes per layer         8   current 4
minimum clusters per layer     8   current 3
minimum repeated axes          5   current 3
```

## Ecological result

Gymnadenia adds a distinct H2 mechanism:

> **Consumer manipulations can change the realized net selection on a trait even when the underlying agent-mediated geometry is summarized at the study level as conflict or reinforcement.**

This is recorded as:

```text
NET_SELECTION_CONTEXT_SHIFT
```

and is kept distinct from:

- geometry-class switch;
- geometry disappearance;
- component-weight shift;
- consumer-role behavior shift.

## Claim ceiling

```text
GYMNADENIA_A2_EXACT_TABLE_VALUES = RECOVERED
TREATMENT_CELL_NET_SELECTION = MATERIALIZED
MEDIATED_CONTRAST_POINT_DIRECTIONS = RECOVERED

MEDIATED_CONTRAST_SE = NOT RECOVERED
MEDIATED_CONTRAST_COVARIANCE = NOT RECOVERED
COVARIANCE_AWARE_LOCAL_AGENT_GEOMETRY = NOT ESTIMATED
```
