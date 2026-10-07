# Pedicularis rex antagonist-context secondary v1

## Biological question

The primary P2 paper asks whether seed predators displace the reproductive
optimum of floral exsertion away from trait states that perform better for
pollination.

A second ecological question is available at almost no additional intervention
cost:

> **Is natural seed-predator pressure itself structured by patch flowering
> density and patch size in the new P2 population/season?**

This is motivated directly by the focal P. rex study of Xia, Sun & Liu (2013;
doi:10.1098/rsbl.2013.0387), not by a post-outcome search for moderators.

## Historical prediction frozen before P2 outcomes

Xia et al. classified:

```text
sparse patch   <2 flowering plants / m2
dense patch    >5 flowering plants / m2

small patch    <20 flowering plants
large patch    >20 flowering plants.
```

The exact boundary value 20 is left unclassified in the replication.

Their key predator pattern was:

```text
overall seed predation:
  sparse > dense

within sparse patches:
  small > large

within dense patches:
  large > small.
```

Thus the patch-size effect reverses with density.

These historical cutpoints are frozen in:

```text
empirical/architecture/
  PEDICULARIS_P2_ANTAGONIST_CONTEXT_CONFIG_TEMPLATE_V1.json
```

They are not estimated from the new P2 outcomes.

## Plant-level context registry

Context is stored separately from the canonical P2 surface so that failure to
collect context cannot block or alter the primary W0-W5 experiment.

Register every P2 plant in:

```text
empirical/architecture/
  PEDICULARIS_P2_ANTAGONIST_CONTEXT_REGISTRY_TEMPLATE_V1.csv
```

Required raw context:

```text
population_id
season_id
plant_id
patch_id
context_measurement_date
patch_area_m2
patch_size_flowering_plants
notes.
```

The analysis reconstructs the historical density definition at the **patch**
scale:

```text
patch flowering density
= patch_size_flowering_plants / patch_area_m2.
```

Patch size is the number of flowering plants assigned to the focal patch.
All plants sharing one patch_id must share both patch area and patch size.

## Why the context is not inserted into the primary surface

Patch flowering density and patch size are observational attributes of where a plant grows.
They are not randomized.

Therefore they may explain heterogeneity in enemy pressure, but they do not
belong in the primary causal test of randomized z x P x G.

The primary P2 surface and W0-W5 classifier are unchanged.

## Historical-comparison state

For direct comparability with Xia et al., the secondary analysis uses only
P = NATURAL and G = EXPOSED.

For each plant represented in that natural state it calculates:

- seed-predation fraction: damaged / (damaged + undamaged developed seed);
- early predator-attack rate;
- final undamaged seed fraction.

The historical replication requires a prospectively frozen minimum number of
plants in each of four cells:

```text
SPARSE x SMALL
SPARSE x LARGE
DENSE  x SMALL
DENSE  x LARGE.
```

If one cell is below that minimum, the result is
P2_ANTAGONIST_CONTEXT_HISTORICAL_COMPARISON_NOT_MODELABLE rather than
combining cells or changing thresholds after seeing data.

## Registered sign pattern

When all four cells are adequately represented, the secondary receipt evaluates:

```text
dense - sparse predation                       < 0
sparse: large - small patch effect             < 0
dense:  large - small patch effect             > 0
difference-in-differences                      > 0.
```

All four signs passing yields
P2_ANTAGONIST_CONTEXT_PATTERN_CONSISTENT_WITH_XIA2013.

Otherwise the state is P2_ANTAGONIST_CONTEXT_PATTERN_NOT_RECOVERED.

No p-value fishing or cutpoint search is used.

## Exact P2 data binding

Run:

```bash
python scripts/analyze_pedicularis_antagonist_context.py \
  <completed_verified_p2.csv> \
  <p2_surface_receipt.json> \
  <p2_context_registry.csv> \
  <frozen_context_config.json> \
  --output <p2_antagonist_context_receipt.json>
```

The analysis requires the canonical surface_data_sha256 to match the exact
flower-level data used for the primary P2 surface.

A context registry must cover exactly the P2 plant set. Missing plants, extra
plants, duplicate plant rows, or inconsistent patch-area/patch-size definitions
fail the secondary analysis only.

## Biological interpretation

A consistent result would mean:

> the focal causal experiment was conducted inside an ecological landscape in
> which natural enemy pressure still shows the patch-density/patch-size-size dependence
> previously documented in P. rex.

This would strengthen the ecological interpretation that antagonist weight is
not a fixed species property.

It would not show that patch flowering density or patch size caused the P2 optimum displacement.

Testing whether z_P* - z_C* itself changes with patch-density/patch-size context requires
a separately powered context-by-surface design. The present secondary explicitly
does not make that claim.

## Claim ceiling

The context receipt is secondary observational ecology only.

It cannot:

- change or rescue W0-W5;
- make a negative P2 surface positive;
- identify causal effects of patch flowering density or patch size;
- claim density-dependent optimum displacement;
- change the registered P2 sample size;
- redefine sparse/dense or small/large after outcomes.

Its value is cheap biological context around the main causal result, not a new
methodological gate.
