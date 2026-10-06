# Pedicularis rex W1/W2 robust power envelope v1

## Purpose

The W1/W2 production-power basis audit currently finds:

~~~text
30 power-basis rows
21 blockers for a registered single-scenario n
12 causal-geometry rows
0/12 causal-geometry rows ready.
~~~

The main uncertainty is not whether the simulator runs. It is how strongly the
required sample size depends on the unknown causal geometry.

Before committing to a separate P2 geometry pilot, run a broad **prospective
sensitivity envelope**.

The envelope asks:

> across several scientifically declared W1/W2 generating worlds, how much
> does the sample size needed for the production headline change?

It is a value-of-information diagnostic. It does not resolve the basis gap by
itself.

## Files

~~~text
empirical/architecture/PEDICULARIS_W1_W2_POWER_ENVELOPE_TEMPLATE_V1.json
scripts/evaluate_pedicularis_w1_w2_power_envelope.py
tests/test_pedicularis_w1_w2_power_envelope.py
~~~

## Scenario rules

Every scenario uses sensitivity-only power status.

All scenarios must share exactly the same population/season, candidate plant
grid, flowers-per-plant design, nominal z grid, power targets, production
surface thresholds/bootstrap settings, and secondary-diagnostic settings.

Scenarios may differ in the generating causal geometry, variance structure, and
target truth world (W1 or W2), but each scenario must carry an explicit
scenario role and basis note.

The bounds still require biological justification. Merely making a grid wide
does not make it scientifically registered.

## No averaging

Scenario powers are never averaged and scenarios are never weighted.

For every candidate n:

~~~text
worst_case_primary_surface_power
    = minimum primary power across scenarios

worst_case_headline_W1_or_W2_power
    = minimum headline power across scenarios.
~~~

A candidate is envelope-positive only if both worst-case powers exceed their
registered targets. An optimistic scenario cannot compensate for an adverse
one.

## Scenario-specific n spread

The diagnostic also reports the minimum candidate meeting both targets inside
each scenario.

Example:

~~~text
scenario A -> 20 plants
scenario B -> 30 plants

scenario_minimum_candidate_range = [20, 30]
minimum_candidate_meeting_targets_in_every_scenario = 30.
~~~

The 30-plant value is still a sensitivity-envelope diagnostic, not a registered
field allocation.

## Interpreting information value

No arbitrary threshold is used to declare that a pilot is needed.

The receipt reports:

~~~text
all_scenarios_have_candidate_meeting_targets
all_scenarios_same_minimum_candidate
scenario_minimum_candidate_range
geometry_uncertainty_changes_minimum_candidate
some_scenario_exceeds_candidate_grid.
~~~

If a broad justified envelope gives nearly the same minimum n across scenarios,
causal-geometry uncertainty has little operational effect over that envelope.
That weakens the case for spending a separate field cohort solely to refine
power inputs.

If scenario-specific minimum n changes strongly, or one or more scenarios
exceed the candidate grid, geometry uncertainty materially controls field
effort. That increases the information value of a separate nonconfirmatory
geometry pilot or of improving the scenario bounds.

The script reports the variation; it does not define a post-hoc cutoff for
"large" variation.

## Run

Create prospectively declared sensitivity scenario configs and list their paths
in a frozen envelope manifest.

~~~bash
python scripts/evaluate_pedicularis_w1_w2_power_envelope.py \
  <power_envelope_manifest.json> \
  <power_basis_receipt.json> \
  --output <w1_w2_power_envelope.json>
~~~

The output status is:

~~~text
PEDICULARIS_W1_W2_POWER_ENVELOPE_DIAGNOSTIC_READY_NOT_REGISTERED_N
~~~

## Why this comes before a geometry pilot

A separate geometry pilot is expensive because it must expose the actual
randomized z x P x G architecture rather than only one intervention lane.

The envelope is cheaper and asks whether that extra information is likely to
change the design decision.

The sequence is:

~~~text
current external/same-context information
-> prospective sensitivity envelope
-> inspect n sensitivity to geometry
-> only then decide whether direct geometry-pilot information is worth its
   extra flowers/plants.
~~~

This ordering minimizes field work without pretending that external
observational relationships identify causal state surfaces.

## Claim ceiling

The envelope does not promote observational selection to causal truth, resolve
the current basis blockers, register a P2 sample size, authorize field
allocation, prove that a geometry pilot is necessary, or generate biological
evidence about W1/W2.

It is a transparent value-of-information diagnostic only.
