# SCH H2 Gymnadenia Appendix A Table A2 extraction V1

## Source

Sletvold, Moritz & Ågren (2015), Ecology 96:214–221.

DOI:

`10.1890/14-0119.1`

Ecological Archives:

`E096-022-A1`

Appendix A Table A2 reports phenotypic linear selection gradients (beta ± SE) for four pollination × herbivory treatment groups in the *Gymnadenia conopsea* population at Sølendet.

Treatment codes:

~~~text
C+H   open-pollinated control + natural herbivory
C+E   open-pollinated control + herbivores excluded
HP+H  supplemental hand pollination + natural herbivory
HP+E  supplemental hand pollination + herbivores excluded
~~~

## Exact treatment-group gradients

### Flowering start

~~~text
C+H    -0.0042 ± 0.054
C+E     0.094  ± 0.031  **
HP+H   -0.16   ± 0.056  **
HP+E   -0.066  ± 0.028  *
~~~

### Spur length

~~~text
C+H     0.18  ± 0.057  **
C+E     0.077 ± 0.035  *
HP+H    0.083 ± 0.053
HP+E   -0.042 ± 0.029
~~~

The full extracted Table A2 is frozen in:

- `data/SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv`

The file also retains plant height, flower number and corolla size.

## Agent-mediated contrast point estimates

Table A2 defines:

~~~text
Delta beta_poll = beta_C - beta_HP
Delta beta_herb = beta_H - beta_E
~~~

For flowering start:

~~~text
Delta beta_poll-H =  0.16
Delta beta_poll-E =  0.16

Delta beta_herb-C  = -0.098
Delta beta_herb-HP = -0.094
~~~

Thus the directional component interpretation is:

~~~text
pollinator-mediated component -> later flowering
herbivore-mediated component  -> earlier flowering
=> opposing directional components
~~~

For spur length:

~~~text
Delta beta_poll-H = 0.10
Delta beta_poll-E = 0.12

Delta beta_herb-C  = 0.10
Delta beta_herb-HP = 0.13
~~~

Thus:

~~~text
pollinator-mediated component -> longer spur
herbivore-mediated component  -> longer spur
=> reinforcing directional components
~~~

The exact contrast point estimates are frozen in:

- `data/SCH_H2_GYMNADENIA_A2_AGENT_CONTRASTS_V1.csv`

## Important uncertainty boundary

Table A2 reports SE for the treatment-group gradients.

It does **not** report an SE or covariance for the mediated contrast values shown in the lower part of the table.

Therefore SCH promotes:

~~~text
4 treatment-group local net-selection cases per trait
~~~

but does not promote:

~~~text
contrast-level uncertainty
or
local two-function geometry with a contrast CI
~~~

without additional covariance information.

The component interpretation remains directional.

## H2 promotion

Two canonical axes are promoted from context structure only to local net selection:

- `Gymnadenia_000030_phenology`
- `Gymnadenia_000030_spur_length`

Each contributes four treatment-group cases.

~~~text
Gymnadenia H2 cases added = 8
~~~

The local cases are in:

- `data/SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH4_V1.csv`

They are classified as:

~~~text
LOCAL_NET_SELECTION
~~~

not as local static conflict/reinforcement geometry.

## Biological result

The same factorial ecological context generates sharply different trait-level component structure.

### Phenology

~~~text
pollinators and herbivores act in opposite directions
=> conflict-compatible component geometry
=> cancellation possible in net selection
~~~

### Spur length

~~~text
pollinators and herbivores act in the same direction
=> reinforcement
~~~

This is a source-table-level confirmation of the SCH principle that geometry belongs to a trait axis, not to a plant × consumer system as a whole.

## Updated H2 state

After Table A2 extraction:

~~~text
total materialized H2 local cases     18
plant-performance cases               11
role-behavior cases                    7

plant-performance LOCAL_GEOMETRY       2
plant-performance LOCAL_NET_SELECTION  9
plant-performance LOCAL_PRESSURE       0
~~~

H2 remains modelability fail-closed because the 11 plant-performance cases span only four canonical axes and three independent biological clusters.
