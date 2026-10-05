# Pedicularis temporal separability hypothesis v1

## Ecological question

The focal *Pedicularis rex* conflict is already biologically real: greater
corolla exsertion can improve pollinator-facing pollen receipt while increasing
exposure to pre-dispersal seed predators. The unresolved question is whether
those opposing functions are also **temporally separable** within a flower's
life.

Primary evidence establishes the relevant ordering without supplying a numeric
clock:

```text
anthesis / natural bumblebee pollination
        |
        | pollen receipt accumulates toward the late-anthesis endpoint
        v
pollination service completion
        ?
        | possible temporal gap
        ?
        v
first predator egg / puncture or ovary swelling
        |
        v
seed-predator loss
```

The event-time pilot tests whether that question mark is a positive interval.

## Latent focal quantity

For a flower, define:

```text
T_poll    time from anthesis to completion of the prospectively defined
          natural-pollination endpoint

T_attack  time from anthesis to first prospectively defined seed-predator
          egg / puncture / attack event

T_swell   time from anthesis to prospectively defined ovary swelling

Delta_T = min(T_attack, T_swell) - T_poll
```

Biologically:

```text
Delta_T > 0
  pollination can finish before antagonist commitment / swelling
  -> temporally separable interaction

Delta_T <= 0
  antagonist commitment or swelling overlaps pollination completion
  -> temporally entangled interaction
```

No hour value is imported from the literature.

## Why the field estimator is not individual Delta_T

Stigmatic pollen counting is destructive. Therefore the registered pilot uses
separate flowers:

- `POLLINATION_SENTINEL`: one destructive pollen observation per flower at a
  prospectively scheduled post-anthesis time;
- `ATTACK_SWELL_SENTINEL`: repeated non-destructive observations of attack and
  swelling on separate flowers.

Consequently the pilot does **not** pretend to estimate an exact individual
`Delta_T`. It estimates population-level event timing on the same
population/season and sampling grid.

### The sampling grid is part of the prospective design

The clock grid must be frozen numerically before event-time observations. The
config therefore records separate elapsed-hour schedules for destructive
pollination sentinels and repeated attack/swelling sentinels, plus a maximum
allowed deviation between the scheduled and actual observation time.

The raw table stores both:

```text
scheduled_elapsed_hours
observation_time_hours
```

so a nominal 8-h slot remains the 8-h design stratum even when field access
occurs slightly early or late. The analyzer reports the actual elapsed-time and
schedule-deviation distributions for every slot and rejects observations outside
the prospectively frozen deviation allowance.

To keep the median crossing a plant-level ecological comparison rather than a
flower-count artefact, the current pilot also requires:

```text
each plant -> exactly one destructive pollination sentinel at every frozen pollination time
each plant -> exactly one attack/swelling sentinel followed at every frozen natural-history time
pollination and attack/swelling lanes -> identical plant set.
```

The script does not choose the number of plants or the clock times. It only
enforces the supplied prospective design. Missing a scheduled slot is therefore
a design deviation, not permission to rebuild the grid after seeing the event
trajectory.

## Registered exploratory descriptor: Delta_T50

The threshold-free summarizer brackets two median crossings on the
prospectively fixed sampling grid:

```text
T_poll,50
  first stable sampled time at which >=50% of pollination sentinels satisfy
  the prospectively frozen pollination-completion definition

T_constraint,50
  first stable sampled time at which >=50% of natural-history sentinels have
  either attack present or ovary swelling
```

Each is retained as an interval:

```text
(previous sampled time, crossing sampled time]
```

or as right-censored if the 50% crossing is not observed.

The exploratory median gap is:

```text
Delta_T50 = T_constraint,50 - T_poll,50
```

but is also retained as an interval rather than collapsed to one hour.

This 50% criterion introduces no convenience threshold: it is the definition
of a median. It does not become the confirmatory G timing bound.

## Three possible biological readouts

### 1. Median temporal separation supported on the sampled grid

If the lower boundary for `T_constraint,50` is at or later than the upper
boundary for `T_poll,50`, interval ordering supports a positive median gap.

Interpretation:

> By the time the median flower has completed the registered pollination
> endpoint, the median antagonist/swelling constraint has not yet begun.

This supports continued development of the post-pollination local
fine-mesh/porous-sleeve route.

It does **not** select a particular device or application hour.

### 2. Median temporal entanglement supported on the sampled grid

If the upper boundary for `T_constraint,50` is at or before the lower boundary
for `T_poll,50`, the median ordering is reversed/non-positive.

Interpretation:

> Antagonist commitment or ovary swelling begins too early for a clean
> population-median post-pollination waiting strategy.

This is not a failed ecological result. It supports moving method development
toward the prospectively retained overlap-compatible route: a local
lower-corolla/ovary barrier that preserves the pollinator entrance during the
overlap period.

It does not automatically validate that alternative barrier.

### 3. Ordering unresolved

If the two median intervals overlap, or one crossing remains insufficiently
bounded, the pilot is inconclusive at the current time resolution.

The correct response is to refine the event-time sampling schedule in a new
nonconfirmatory cohort, not to choose a convenient hour from the same data.

## Relation to SCH

This focal test adds a biological dimension to SCH without changing the core
identification claim.

The shared trait can experience conflict even when the two functions are
sequentially separable. Temporal separation can make the functional channels
experimentally isolatable without making their trait optima aligned.

Conversely, temporal overlap does not prove stronger evolutionary conflict; it
means that the two functional demands are **temporally entangled** over the
flower's life and require a spatially selective intervention if they are to be
separated experimentally.

Thus the focal question is:

> Does the same shared floral coordinate face opposing functions in distinct
> temporal windows, or do the mutualistic and antagonistic windows overlap?

## Comparative boundary

The current canonical SCH ledger cannot test this as a general comparative
rule. Of 35 fixed-role canonical axes, 34 are coded
`SIMULTANEOUS_OR_OVERLAPPING`; there are currently zero fixed-role axes in the
`SEQUENTIAL_LIFE_HISTORY_FILTER` or `TEMPORALLY_SEPARATED` classes.

Therefore:

```text
P. rex temporal separability = focal mechanistic hypothesis

NOT

temporal separation -> general conflict geometry law
```

A cross-system timing claim remains fail-closed until independent temporal
contrast exists.

## Machine implementation

```text
empirical/architecture/PEDICULARIS_G_EVENT_TIME_PILOT_CONFIG_TEMPLATE_V1.json
empirical/architecture/PEDICULARIS_G_EVENT_TIME_PILOT_TEMPLATE_V1.csv
scripts/summarize_pedicularis_g_event_time_pilot.py
```

The resulting `Delta_T50` descriptor is CAL-B calibration evidence only. It
does not select the final lower/upper G timing gates, validate independent G,
or generate a confirmatory receipt.
