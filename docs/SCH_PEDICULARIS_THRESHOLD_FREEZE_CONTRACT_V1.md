# SCH Pedicularis prospective threshold-freeze contract v1

## Purpose

The Pedicularis execution pipeline is deliberately fail-closed before any
confirmatory P0, P1, or G outcome is interpreted.

The current field config files are templates, not preregistered thresholds.
They contain `REQUIRED_BEFORE_USE` placeholders by design. The next empirical
gate is therefore:

```text
F0 = prospectively freeze the P0, P1 and G decision thresholds
     for one population and season
     before reading confirmatory outcomes.
```

This gate precedes the three positive evaluator receipts required for
`SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3`.

## What must be frozen

Each lane config must contain:

```text
prospective_freeze.schema
  = SCH_PEDICULARIS_THRESHOLD_FREEZE_V1

prospective_freeze.status
  = PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN

prospective_freeze.lane
  = P0 | P1 | G

population_id
season_id
frozen_before_confirmatory_data = true
frozen_at_utc
basis_document
threshold_basis.<one entry for every gate field>
```

The three lane configs must target the same population and season before the
full-surface readiness chain is allowed to open.

## Gate coverage

The freeze contract currently requires a basis note for every decision field:

```text
P0: 11 gate fields
P1: 10 gate fields
G : 19 gate fields
```

This includes sample-size minima, effect/separation minima, equivalence or
contamination maxima, timing limits, and the boolean method requirements in G.

A numeric value without a basis note is not considered frozen.

## Allowed basis logic

A threshold basis may come from one or more of:

- an independent method-development pilot;
- measurement precision / repeatability work;
- a biological minimum effect that was defined before confirmatory outcomes;
- a prospective power or precision calculation;
- a directly relevant source-based constraint;
- a method-feasibility or natural-history constraint.

The basis document must make clear which route supports each threshold.

If a threshold is pilot-derived, the pilot used to set it must remain separate
from the confirmatory dataset that will be evaluated against it. Do not tune a
cutoff on the same outcome data and then call the gate prospective.

## Test fixtures are not field thresholds

Synthetic values inside `tests/` exist only to exercise the code path.

Examples such as:

```text
15 plants
0.10 exsertion separation
0.05 equivalence tolerance
6-30 hour barrier windows
```

must not be promoted to field thresholds merely because a unit test passes with
them. They have no empirical standing unless independently justified and frozen
under this contract.

## Threshold-basis ledger

The resolution state for all 40 gate fields is tracked in:

```text
empirical/architecture/PEDICULARIS_THRESHOLD_BASIS_LEDGER_V1.csv
```

Current bounded state:

```text
40 total gate fields
 5 RESOLVED_FROM_REGISTERED_CONTRACT
35 still require independent justification
```

The five already resolved values are the registered minimum of five realized z
levels and four boolean G-method requirements. No unresolved numeric cutoff is
filled from a unit-test fixture.

The remaining rows specify the required resolution route rather than a guessed
value: power/precision, measurement-equivalence calibration, effect-size
justification, method-feasibility calibration, or a separate G timing pilot.

## Machine enforcement

Shared validation is implemented in:

```text
scripts/pedicularis_config_freeze.py
```

The three confirmatory evaluators refuse configs that do not pass the freeze
contract:

```text
scripts/evaluate_pedicularis_stage_p0.py
scripts/evaluate_pedicularis_pollination_weight.py
scripts/evaluate_pedicularis_predator_method.py
```

Each positive evaluator receipt carries a `config_freeze` provenance block.

The readiness assembler then requires positive threshold-freeze provenance from
all three lanes, and the canonical full-surface analyzer rechecks it.

## Current execution frontier

Run:

```bash
python scripts/audit_pedicularis_execution_frontier.py
```

Against the committed templates, the expected current result is:

```text
current_blocker = PROSPECTIVE_THRESHOLD_FREEZE_REQUIRED
```

After all three same-context configs are genuinely frozen, the frontier becomes:

```text
current_blocker = CONFIRMATORY_P0_P1_G_RECEIPTS_REQUIRED
```

Only after those three positive receipts may
`SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3` unlock the z x P x G experiment.

## Claim ceiling

A positive threshold-freeze audit establishes only that the decision rules were
specified prospectively with explicit provenance.

It does not establish manipulation validity, functional conflict, causal
compromise, pure-function optima, conflict budget L, or dimensional release.
