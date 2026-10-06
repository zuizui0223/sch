# Pedicularis rex W1/W2 envelope boundability audit v1

## Question

Can the existing *P. rex* evidence constrain the prospective W1/W2
multi-scenario power envelope tightly enough that the separate geometry pilot
might be avoided?

This is different from asking whether the simulator can run. A scenario can
always be typed into a config. The question is whether its numerical bounds
have a biological evidence basis.

Machine audit:

```text
scripts/audit_pedicularis_w1_w2_envelope_boundability.py
```

## Current result

Among the 18 blocking same-estimand geometry/variance inputs targeted by the
separate geometry pilot:

```text
DIRECT SAME-ESTIMAND NUMERIC BOUND        0
DIRECTION ONLY, NO MAGNITUDE              3
FOCAL ENDPOINT SCALE/RANGE ONLY           4
NO NUMERIC BOUND                         11
                                          --
TOTAL                                     18
```

Thus the current focal evidence does **not** by itself identify a quantitative
robust envelope for the final causal geometry.

## What the 2016 focal programme does give

Sun, Armbruster & Huang (2016; doi:10.1093/aob/mcw097) provides a rich
observational geographic programme.

The primary article and supplements include:

- floral phenotype and pollination summaries across 14 populations;
- seed outcomes across 12 populations;
- a positive association between exsertion and stigmatic pollen load;
- a positive association between exsertion and seed-predation risk;
- pooled pollen scale information;
- natural initial-seed and seed-predation variation.

Those data are highly relevant biological context.

They do not contain the registered randomized:

```text
P0G0(z)
P1G0(z)
P0G1(z)
P1G1(z)
```

fitness surfaces.

Therefore they do not locate the four causal quadratic peaks, optima or
curvatures.

## Three direction-only paths

Current evidence supports direction but not a prospective causal magnitude for:

```text
generating_model.state_fitness_surfaces.P1G1
generating_model.pollen_state_models.P1G0
generating_model.pollen_state_models.P1G1.
```

For example, the observational result

```text
higher exsertion -> greater pollen receipt
```

does not specify the slope produced by randomized exsertion under predator
exclusion or exposure.

Likewise, opposing observational selection does not identify a bounded W11
reproductive optimum or its curvature.

Direction may constrain the sign of a sensitivity scenario. It cannot define
its magnitude.

## Four scale/range-only paths

The focal programme provides useful scale information for:

```text
pollen total variation
initial-seed population variation.
```

The power generator, however, needs:

```text
pollen between-plant SD
pollen residual SD

initial-seed between-plant SD
initial-seed residual SD.
```

A pooled pollen SD cannot identify those two variance components.

A range of population means for initial seed set cannot identify either the
within-population plant variance or residual variance after randomized z and
plant blocking.

These sources can be used to reject biologically absurd scenarios. They cannot
directly populate the registered variance decomposition.

## Eleven currently unbounded paths

Eleven of the 18 inputs have no numerical bound in the current canonical basis
ledger.

They include:

- final-fitness between-plant and residual variation;
- P0G0, P1G0 and P0G1 final-fitness surfaces;
- supplemented-state pollen models;
- all four randomized state-specific initial-seed models.

The missing information is not mainly a larger literature denominator. It is
the causal estimand itself.

## Consequence for Route B

The robust-envelope code remains useful for value-of-information analysis.

But with current evidence alone:

```text
CURRENT-EVIDENCE-ONLY QUANTITATIVE ENVELOPE = NOT BOUNDABLE.
```

A narrow scenario set would require additional independently justified
structural assumptions about unmeasured causal optima, curvatures, slopes and
variance decomposition.

Those assumptions must be explicit. They cannot be presented as values
recovered from the current *P. rex* literature.

A deliberately broad envelope can still be run, but its width then reflects
assumption choice as much as empirical knowledge.

## What this means for the geometry pilot

The separate `POWER_GEOMETRY_PILOT` is not valuable merely because another
pilot is statistically tidy.

It is valuable because it measures precisely the 18 quantities for which the
current evidence is weakest:

```text
randomized four-state fitness geometry
state-specific pollen response geometry
state-specific initial-seed response geometry
same-estimand plant/residual variance.
```

A positive geometry-pilot summary can replace all 18 rows with direct
same-context numerical basis.

The canonical basis audit then retains only the three P0/F0-dependent blockers:

```text
generating_model.z_levels
generating_model.realized_z_sd
production_surface_config.sch_surface.*.
```

## Operational decision

The preferred order remains:

```text
1. Use existing evidence to define only bounds that are genuinely defensible.

2. Run a broad sensitivity envelope if useful to understand qualitative
   sample-size sensitivity.

3. Do not promote that envelope to an empirical geometry claim.

4. If a registered n is needed and the key causal geometry still lacks
   independent bounds, run the disjoint POWER_GEOMETRY_PILOT.

5. Finish the remaining P0/F0 basis and then power confirmatory P2.
```

The important shift is that the geometry pilot is now motivated by a specific
missing biological object—the four-state adaptive surface—not by generic
uncertainty.

## Claim ceiling

This audit is bounded to the currently recovered focal evidence and canonical
repo evidence base.

It does not prove that no unpublished or inaccessible source contains relevant
numbers.

It does not choose sensitivity bounds, geometry-pilot n, or confirmatory P2 n.

It does not convert observational direction into causal magnitude.
