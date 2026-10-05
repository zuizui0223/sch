# SCH Pedicularis G timing primary-evidence audit v1

## Biological question

Can the independent seed-predator intervention in *Pedicularis rex* be placed in
a real biological interval that begins after natural pollination is complete but
ends before seed-predator access or ovary swelling makes the intervention too
late?

The recovered primary literature supports the existence of relevant event
ordering. It does **not** supply a focal hour-scale interval that can be copied
into the registered G configuration.

Machine ledger:

```text
empirical/architecture/PEDICULARIS_G_TIMING_PRIMARY_EVIDENCE_V1.csv
scripts/audit_pedicularis_g_timing_primary_evidence.py
```

## What is directly recovered in focal P. rex

### Seed-predator access is an open-flower, pre-swelling event

Sun, Armbruster & Huang (2016; doi:10.1093/aob/mcw097) report that the
pre-dispersal Dipteran/Lepidopteran seed predators lay eggs on ovaries after
flowers are open but before ovaries swell, piercing sepals or corolla tubes from
outside.

Thus focal evidence supports:

```text
flower open
-> predator oviposition is possible
-> ovary swelling is a late boundary.
```

It does not establish:

```text
natural pollination has already completed when predator access begins
or
a numeric number of hours after anthesis at which a barrier is safe.
```

That distinction matters. The existing *Pedicularis furbishiae* precedent
supports a genus-level ordering in which seed-predator attack can occur after
pollination, but it is not a focal *P. rex* clock.

### P. rex is strongly pollinator dependent

Sun & Huang (2015; doi:10.1093/aobpla/plv019), drawing on focal pollination
work, describe *P. rex* as self-compatible but lacking effective autogamous
pollination and depending on bumblebees for seed production.

Tang, Xie & Sun (2007; doi:10.1016/j.flora.2006.09.001) describe bumblebees as
the primary and effective pollinators of *P. rex* subsp. *rex*. During typical
nectar foraging, the stigma contacts the thorax/abdomen of the bee.

Therefore preserving the natural pollination lane is a biological requirement,
not just a method preference. A barrier that changes bee entry or stigma contact
cannot be treated as independent G.

### The downstream reproductive clock is long

Sun & Huang (2015) report that capsules generally mature approximately three
weeks after anthesis.

This is useful for harvest scheduling and demonstrates that the final seed
endpoint occurs far downstream of flowering. It cannot identify the much
shorter barrier-placement interval.

### Antagonist pressure is real but highly context dependent

The same focal programme reports seed predation spanning roughly 1.36-27.42%
among sampled populations, with strong geographic variation also recovered in
the 2016 selection study.

This supports two biological points:

1. the antagonist lane is large enough to matter in at least some populations;
2. a focal population cannot be assumed to have a species-wide predation rate.

It does **not** justify setting the allowable device hard-failure probability to
5%, 10%, 20%, or any other value. Natural predation prevalence is a biological
process rate. Device hard failure is a method-error rate. Treating one as the
other would mix two different probabilities.

## What close Pedicularis evidence adds

Huang & Shi (2013; doi:10.1111/nph.12327) report flower longevities of roughly
4-7 d across nine other *Pedicularis* species.

This demonstrates that multi-day flower lifetimes are plausible in the genus,
but the species were not focal *P. rex*. The 4-7 d range is therefore context
only and cannot be converted into an hour-scale P. rex G cutoff.

## Biological estimands left for the focal timing pilot

The literature search now narrows the unresolved timing problem to three
time-to-event quantities measured from anthesis in the same population and
season:

```text
T_poll
  time until the prospectively defined natural-pollination window is complete

T_attack
  time until first detectable predator egg / puncture / attack evidence

T_swell
  time until the ovary reaches the prospectively defined swelling state.
```

A practical selective-G interval exists only where:

```text
T_poll < barrier time < min(T_attack, T_swell)
```

for enough focal flowers to support the registered method-reliability
requirement.

The pilot should therefore estimate these event-time distributions rather than
start by choosing an arbitrary number of hours.

## Consequence for the existing gates

The current threshold-basis states remain correct:

```text
method_gate.min_hours_after_anthesis_before_barrier
  -> NEEDS_METHOD_PILOT

method_gate.max_hours_after_anthesis_before_barrier
  -> NEEDS_METHOD_PILOT
```

Recovered literature can constrain the interpretation and field observations,
but it recovers zero numeric F0 timing values.

Likewise, the hard-validity pilot's
`max_acceptable_per_plant_hard_failure_probability` remains a prospective
method-reliability choice with its own rationale. The natural 1.36-27.42%
predation range is not an eligible substitute.

## Ecological interpretation

This changes the emphasis of the next field step.

The key question is not merely whether a sleeve blocks insects. It is whether
*P. rex* has a **temporal ecological niche for selective antagonist removal**:
a period after bumblebees have delivered the pollination service but before
pre-dispersal seed predators have committed their attack.

If that interval is consistently present, the plant's sequential interaction
biology makes independent manipulation of the two functions possible. If the
pollination and antagonist windows overlap too strongly, failure of G is itself
biologically informative: the conflict is temporally entangled rather than
experimentally separable by a late local barrier.

## Current state

```text
focal predator access route                 RECOVERED
focal open-flower -> pre-swelling ordering  RECOVERED
focal bumblebee dependence                  RECOVERED
focal pollination mechanism                 RECOVERED
focal hour-scale pollination completion     NOT RECOVERED
focal first-attack time distribution        NOT RECOVERED
focal ovary-swelling time distribution      NOT RECOVERED
portable focal barrier window in hours      NOT RECOVERED
natural predation as device-failure cutoff  REJECTED
```

The next empirical gain is therefore the focal event-time pilot, not another
generic literature expansion and not an invented timing threshold.
