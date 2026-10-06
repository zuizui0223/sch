# Pedicularis rex P2 context selection v1

## Biological purpose

The focal P2 experiment asks whether seed predators displace the reproductive
optimum of floral exsertion away from trait states with greater pollination
performance.

That question is meaningful only in a population/season where both functional
lanes are actually active.

A high historical predation value is useful for finding such a context, but it
is not evidence that the same population has the same antagonist pressure in
the present field season.

This contract therefore separates:

```text
historical geographic information
    -> recruitment / enrichment prior only

same-season P1 + G validation
    -> actual P2 context qualification.
```

## Historical source boundary

Sun, Armbruster & Huang (2016; doi:10.1093/aob/mcw097) sampled 14 P. rex
populations and retained same-individual trait/pollination/seed linkage in:

```text
POP1, POP3, POP5, POP8, POP9, POP10, POP11.
```

Labels were lost before seed outcomes in:

```text
POP2, POP4, POP6, POP7, POP12.
```

Four seed-predation percentages are given exactly in the primary main text:

```text
POP5   27.42%   highest exact case; linkage retained
POP12  18.50%   high exact case; linkage lost
POP3    1.36%   low exact case; linkage retained
POP11   0.80%   lowest exact case; linkage retained.
```

Machine ledger:

```text
empirical/architecture/PEDICULARIS_P2_HISTORICAL_CONTEXT_PRIORS_V1.csv
scripts/audit_pedicularis_p2_context_priors.py
```

## What POP5 means—and does not mean

Among the four exact main-text pressure values, POP5 is the strongest historical
antagonist-pressure case that also retained individual trait/pollination/seed
linkage.

Therefore POP5 is a legitimate **historical high-antagonism enrichment prior**.

It is not:

- automatically the P2 population;
- evidence that current-season predation is still 27.42%;
- a species-wide high-antagonism threshold;
- a population-specific causal optimum;
- evidence that W1/W2 will occur.

## Source locality mapping is still unresolved

The main text identifies the population numbers but puts detailed locality and
altitude in Supplementary Table S1.

Until that primary table or an equivalent primary source is actually recovered,
the repository cannot safely state that a modern field site is historical POP5,
POP3, POP11, etc.

Accordingly:

```text
historical_population_code = POPx
```

is accepted only when:

```text
historical_mapping_status = SOURCE_VERIFIED
```

and the exact primary mapping source is recorded.

If no such mapping is available, use:

```text
selection_mode = CURRENT_CONTEXT_ONLY
historical_population_code = NONE.
```

This still permits P2 after current-season qualification; it simply forbids an
unsupported historical identity claim.

## Current-season biological qualification

The final context freeze occurs only after the same population and season have
a positive:

```text
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3.
```

That receipt already requires:

```text
P0 = PEDICULARIS_Z_MANIPULATION_VALIDATED

P1 = PEDICULARIS_POLLINATION_WEIGHT_VALIDATED

G  = PEDICULARIS_PREDATOR_METHOD_VALIDATED

same population + same season.
```

For the biology-first paper, the important interpretation is:

```text
P1 positive
-> the current context contains a measurable pollination-facing reproductive
   dependency that can be experimentally shifted by supplementation.

G positive
-> the current context contains measurable seed-predator pressure that can be
   selectively reduced without invalidating the pollination lane.
```

Only after both are positive is the context described as:

```text
P2_CONTEXT_FROZEN_CURRENT_SEASON_BOTH_FUNCTIONAL_LANES_VALIDATED.
```

This uses the already frozen P1/G biological gates. It does not invent a new
predation percentage or pollen threshold.

## Freeze file

Template:

```text
empirical/architecture/PEDICULARIS_P2_CONTEXT_FREEZE_CONFIG_TEMPLATE_V1.json
```

Run:

```bash
python scripts/freeze_pedicularis_p2_context.py \
  <context_config.json> \
  <full_surface_readiness_v3.json> \
  empirical/architecture/PEDICULARIS_P2_HISTORICAL_CONTEXT_PRIORS_V1.csv \
  --output <p2_context_freeze.json>
```

The config declares, before P2 outcomes:

- population;
- season;
- whether a historical context prior is being used;
- source-verified historical mapping when applicable;
- the intended inference scope;
- the biological reason for selecting this context.

## Enriched-context inference

If a source-verified historical high-antagonism context is deliberately chosen,
the primary claim must remain scoped to that enriched context.

A positive W1/W2 result would then mean:

> in a prospectively selected conflict-active/high-antagonism context, current
> seed-predator pressure causally displaces the reproductive optimum away from
> higher-pollination trait states.

It would not establish that:

- most P. rex populations behave this way;
- the effect has the same size elsewhere;
- high historical predation predicts current W1/W2.

A later low-antagonism population can be used as an external context contrast,
but it should not be retroactively added to rescue or redefine the primary
result.

## Why no new pressure threshold is introduced

The 0.80–27.42% historical range is not converted into a cut-off such as
"predation must exceed 10%."

Such a cut-off would be arbitrary and would mix historical natural pressure
with current experimental detectability.

Instead:

```text
historical pressure -> rank/prior
current P1/G receipts -> same-season functional-lane qualification.
```

## Binding to P2 allocation

The P2 flower allocator now requires the context-freeze receipt in addition to
the W1/W2 power receipt.

Thus P2 cannot be allocated unless:

```text
same-season context is biologically qualified
AND
the exact design meets the registered primary/headline power targets.
```

The allocation receipt stores a SHA-256 binding to the context receipt. The
subsequent field identity lock is already bound to the allocation receipt, so
the context qualification travels through to the exact analyzed flower-level
surface.

## Claim ceiling

This contract supports prospective context enrichment and same-season
qualification only.

It does not establish:

- W1/W2;
- population prevalence;
- species-wide generality;
- persistence of historical predation rates;
- historical adaptation;
- pure-function optima.
