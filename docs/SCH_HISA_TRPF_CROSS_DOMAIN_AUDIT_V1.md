# SCH HisA/TrpF adaptive-conflict cross-domain audit v1

## Question

Can experimental enzyme evolution provide a non-floral example of two functions constrained through one shared functional unit, while preserving SCH's distinction between a broad shared-conflict analogue and a registered causal optimum-shift test?

## System

`Salmonella enterica` histidine/tryptophan isomerase system.

Shared functional unit candidate:

```text
one bifunctional HisA-derived enzyme / allele
```

Functional lanes:

```text
HisA activity: histidine biosynthesis
TrpF activity: tryptophan biosynthesis.
```

## Primary-source evidence

### 2012 real-time IAD experiment

Näsvall et al. 2012, Science, DOI:

```text
10.1126/science.1226521
```

used a `Salmonella enterica` strain lacking `trpF` and a bifunctional HisA-derived allele that retained HisA activity while gaining weak TrpF activity. Under continuous selection for both biosynthetic functions, the allele amplified and copies accumulated mutations. Evolutionary trajectories included:

```text
HisA specialists
TrpF specialists
generalists retaining both activities.
```

Several specialist trajectories improved one activity at the expense of the other. The experiment therefore demonstrates a real biochemical adaptive-conflict landscape in which one ancestral/shared enzyme can be required to satisfy two selectable functions.

### Structural follow-up

A later structural/functional analysis of the evolved `(beta-alpha)8`-barrel enzymes showed how mutations altered conformational and catalytic properties during specialization, supporting a mechanistic biochemical basis for the HisA/TrpF functional divergence.

### 2026 bifunctional rescue

Näsvall & Abdalaal 2026, G3, DOI:

```text
10.1093/g3journal/jkag167
```

started from wild-type relevant genes in native contexts and evolved `Delta trpF` populations. Mutations in `hisA` or `trpA` restored tryptophan synthesis while retaining enough ancestral function for growth. Target-gene duplication appeared in only one population and did not show functional divergence.

This is important boundary evidence: multifunctional adaptation need not always resolve by duplication/specialization.

## SCH interpretation

The HisA/TrpF system is a strong **cross-domain adaptive-conflict analogue** because:

```text
one molecular unit can carry two selectable functions;
mutational improvement can generate reciprocal activity trade-offs;
selection can maintain generalist or drive specialist trajectories.
```

It supports the biological reality of shared-unit functional conflict outside morphology and floral ecology.

## What is not identified

The 2012/2026 experiments do not implement SCH's registered causal design in which a common scalar coordinate `z` is deliberately varied while the relative weights of function 1 and function 2 are independently manipulated to recover:

```text
z_F1*
z_F2*
z_C*
fitness-scale L.
```

Enzyme sequence/genotype space is multidimensional, and the published activity trajectories are not automatically a one-dimensional `z x P x G` optimum surface.

Therefore the correct role is:

```text
G2_CROSS_DOMAIN_ADAPTIVE_CONFLICT_EXPERIMENTAL_ANCHOR
```

not a complete causal replication of SCH.

## Stronger future route

A direct SCH-style enzyme test would require a preregistered one-dimensional biochemical or sequence coordinate (or a controlled activity-allocation axis), independent histidine- and tryptophan-demand manipulations, and measurement of the optimum along that same coordinate under each demand state.

## Claim ceiling

Appropriate:

> HisA/TrpF experimental evolution shows that one molecular unit can experience selectable multifunctional conflict and can evolve along generalist or specialist trajectories.

Not appropriate:

> HisA/TrpF already estimates the SCH shared-coordinate conflict budget or proves the SCH one-axis optimum-shift mechanism.
