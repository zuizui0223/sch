# SCH end-to-end execution spine v1

## One-line programme

```text
real-world multifunctionality
-> qualify a conflict-active context
-> validate selective interventions
-> manipulate one shared z over multiple levels
-> recover causal compromise geometry
-> hand identified one-dimensional constraint to BITA.
```

This document is the operational reader path. Literature products remain evidence that the biological architecture is real; they do not replace any experimental gate below.

## Gate 0 — biological reality

Required before system-specific execution:

```text
same declared trait coordinate plausibly affects function 1 and function 2
common plant fitness scale is biologically meaningful
functional conflict is plausible but not assumed.
```

Current real-world anchors include Dalechampia, Castilleja, Nicotiana, Primula, and negative-control aligned-optimum systems.

## Gate 1 — context qualification

For systems with context-dependent antagonism, first establish that the focal population / season is informative.

Dalechampia implementation:

```text
SCH_DALECHAMPIA_GEOGRAPHIC_CONFLICT_AND_G0_RECOVERY_V1.md
SCH_DALECHAMPIA_STAGE0_DATA_CONTRACT_V1.md
scripts/evaluate_dalechampia_stage0.py population ...
```

Pass state:

```text
QUALIFIED_CONFLICT_ACTIVE_CANDIDATE.
```

Failure is biologically interpretable and does not falsify the general theory.

## Gate 2 — selective functional interventions

The experiment must alter the functional weights without silently moving z or another relevant reward/physiological coordinate.

### Pollinator lane

Validate a P intervention that changes pollinator-mediated reproductive input while preserving G and z as far as biologically possible.

### Antagonist lane

Validate a G intervention that changes antagonist-mediated loss while preserving P and z.

Dalechampia implementation:

```text
controlled adult-weevil exposure
E0 vs candidate E1-E4 windows
within-plant matched design
paired plant bootstrap
```

Pass state:

```text
SELECTIVE_G_WINDOW_CANDIDATE.
```

The field protocol is `SCH_DALECHAMPIA_STAGE0_FIELD_EXECUTION_PROTOCOL_V1.md`.

## Gate 3 — shared-trait manipulation

Manipulate the same declared `z` coordinate over at least three, preferably five or more, informative values.

For Dalechampia:

```text
z = apparent bract display area during the ecological decision window
```

with natural tissue retained and post-pollination carbon function protected.

Manipulation checks must cover:

```text
realized z
optical state / color / UV where relevant
reward / gland state
flower or blossom geometry
persistent direct-cost artefacts.
```

Do not proceed if the manipulation changes several biological coordinates that cannot be separated.

## Gate 4 — full causal surface

Run the randomized factorial:

```text
>=5 z levels x 2 P states x 2 G states.
```

Primary outcome:

```text
one common fitness_value across every cell.
```

Dalechampia intended endpoint:

```text
mature intact viable seeds per focal blossom.
```

Required raw fields are registered in:

```text
empirical/architecture/SCH_CAUSAL_COMPROMISE_SURFACE_TEMPLATE_V1.csv
```

## Gate 5 — causal compromise analysis

Run:

```bash
python scripts/analyze_sch_compromise_surface.py \
  <surface.csv> \
  <frozen_config.json> \
  --output <receipt.json>
```

The analyzer fits the four intervention-defined local surfaces:

```text
W00(z)
W10(z)
W01(z)
W11(z)
```

and recovers:

```text
z_pollinator_context
z_antagonist_context
z_combined
state-optimum separation
shift after removing G
shift after removing P
pollinator component gradient
antagonist component gradient
P x G interaction gradient.
```

The analysis contract is:

```text
SCH_CAUSAL_COMPROMISE_SURFACE_ANALYSIS_V1.md
```

## Positive Chapter-1 decision

The machine status:

```text
MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
```

requires all four registered gates:

```text
C2 distinct state optima
C3 interior combined optimum
C4 opposing causal optimum shifts
C5 opposed functional component gradients.
```

The combined quadratic having zero slope at its own fitted vertex is not counted as independent evidence.

## Sensitivity / confirmatory reporting

A positive first-pass receipt is followed by:

```text
raw cell summary figure
alternative bounded smoother / local polynomial sensitivity
manipulation-check report
cluster / patch / date hierarchical sensitivity where design supports it
direct-cost control
missingness / retention audit.
```

The local quadratic is the registered transparent benchmark, not the only allowable biological curve.

## Stop rules

### S1 — no conflict-active context

Do not force a positive compromise system. Retain the null/weak context as functional-weight variation evidence and move to the next candidate.

### S2 — P or G not selective

Do not compute mechanism-resolved compromise from a factorial whose functional interventions change each other's pathways or alter z materially.

### S3 — z manipulation invalid

If the manipulation changes reward, physiology, geometry, or post-reproductive function beyond the declared tolerances, redesign it or choose another z/system.

### S4 — no interior / no opposing shifts

Report multifunctionality or local conflict at the level actually recovered. Do not narrate an intermediate compromise if the combined surface is monotonic, boundary-limited, or the functional optima overlap.

## Candidate routing

Current roles:

```text
Dalechampia
= conditional first-choice causal compromise system
  requires conflict-active context + selective G recovery

Nicotiana
= strongest local same-coordinate mechanism + BITA continuity

Castilleja
= strong short-path opposing-selection fallback
  but still requires direct calyx manipulation + selective predator intervention

Platycodon / aligned-optimum class
= negative control demonstrating multifunctionality without conflict.
```

## BITA handoff

A positive SCH receipt supplies the one-dimensional reference architecture:

```text
shared trait z
z_pollinator_context
z_antagonist_context
z_combined
compromise displacement / penalty geometry.
```

BITA then tests whether an added trait coordinate yields:

```text
preferential functional loading
+ movement of the first trait toward its function-specific optimum
+ a fitness combination outside the shared one-dimensional path
= dimensional release / functional differentiation.
```

Thus the two chapters are linked by measured quantities rather than by narrative analogy.
