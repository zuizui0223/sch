# SCH Dalechampia Stage-0 field execution protocol v1

## Purpose

This protocol turns the conditional Dalechampia lane into a field-executable decision sequence.

It is not the Chapter-1 compromise experiment. It only answers two prerequisite questions:

```text
A. Is the focal population / season conflict-active enough to justify causal work?
B. Can adult seed-weevil exposure be manipulated as a selective G contrast?
```

Only if both pass does the programme proceed to the multi-level `z x P x G` experiment.

## Biological timing anchor

`Dalechampia scandens` blossoms are functionally protogynous. The female flowers are receptive before the male flowers open, followed by a bisexual phase. The exact duration is population- and condition-dependent and must be scored directly in the focal field population.

The seed-weevil literature establishes later seed damage clearly, but the exact adult oviposition window is not directly resolved strongly enough to freeze a single natural-history time point in advance. Stage 0 therefore treats timing as an empirical quantity to recover.

## Phase A — population / season qualification

### Candidate context

Each package is one:

```text
population x season/campaign
```

Do not pool populations before qualification. The Mexican positive case and northern Costa Rican null/weak cases show that antagonist weight and trait tracking vary geographically and temporally.

### Focal sampling unit

The biological cluster is the plant. Sample multiple blossoms per plant where possible.

For each blossom record:

```text
plant_id
blossom_id
measured apparent bract area
female/bisexual developmental state
stigmatic pollen receipt
predator presence / later seed damage
initiated seeds
mature intact seeds when retained to maturity
calendar date / local block
```

The machine-readable minimum columns are defined in `SCH_DALECHAMPIA_STAGE0_DATA_CONTRACT_V1.md`.

### Qualification rule

Run:

```bash
python scripts/evaluate_dalechampia_stage0.py population <csv> <frozen_config.json>
```

The result may be:

```text
QUALIFIED_CONFLICT_ACTIVE_CANDIDATE
```

or

```text
NOT_QUALIFIED_CONFLICT_ACTIVE_CANDIDATE.
```

A positive result means only that the population has enough same-coordinate tracking to justify direct manipulation. It does not establish an optimum or a causal compromise.

### Biological interpretation of failure

A failed population is not a failed theory. It may mean that the antagonist functional weight is weak in that place or season. Such contexts are useful comparative data for the SCH prediction that weak function 2 should reduce or erase the compromise penalty.

## Phase B — controlled adult-weevil exposure

### Experimental block

Use the plant as a matched block.

Preferred layout:

```text
plant 1: E0 E1 E2 E3 E4
plant 2: E0 E1 E2 E3 E4
...
```

Assign comparable blossoms within each plant randomly to exposure windows. If a plant cannot provide every window, retain it only for windows with an E0 match; the evaluator uses complete E0/window plant pairs.

### Exposure windows

Initial biological labels are:

```text
E0 = no adult-weevil exposure / sham enclosure
E1 = female-phase exposure
E2 = early bisexual exposure
E3 = late bisexual exposure
E4 = post-receptive / early fruit-development exposure.
```

Exact clock duration is not fixed by the literature. A short feasibility pilot determines an exposure duration that permits adult investigation while avoiding starvation, heat stress, condensation, blossom damage, or prolonged alteration of plant microclimate.

### Adult identity and sex

The strongest intervention uses identified focal seed-weevil adults. If reliable sexing is available, use known females for the definitive timing screen.

If sex cannot be assigned reliably:

```text
mixed-adult exposure = feasibility evidence only
```

Do not label it `female-weevil exposure` or interpret a negative result as absence of an oviposition window.

Voucher a subset of adults used in the study and preserve the identification basis. If multiple curculionid taxa are present, do not combine them silently into one antagonist treatment.

### Enclosure / sham logic

The cage or sleeve is part of the intervention and therefore needs its own control.

For every exposure window:

```text
G1 candidate = same enclosure + standardized adult exposure
E0 control    = same enclosure + no adults
```

The E0 enclosure should match exposure duration, material, handling, and placement. An unenclosed natural blossom may be retained as an additional ecological control but cannot replace the sham E0 for selectivity inference.

Record at minimum:

```text
enclosure_id / material batch
start and stop time
air temperature where feasible
condensation / visible heat stress
number of adults introduced
number recovered alive
adult taxon / sex status
blossom developmental state
```

### Pollination protection

The antagonist exposure must not create a pollination treatment accidentally.

Preferred sequence where biology permits:

```text
allow / standardize the declared pollination state
-> record pollen receipt
-> apply short adult-weevil exposure in the candidate window
-> remove adults and enclosure
-> follow seeds to damage / maturity.
```

If the biologically relevant weevil window overlaps pollinator access, the experiment must retain a matched sham enclosure and explicitly test pollen selectivity. Do not infer `G` selectivity from timing alone.

### Direct oviposition observations

Inspect blossoms after exposure for eggs, punctures, scars, or other validated oviposition evidence where technically possible.

Code this separately:

```text
DIRECT_OVIPOSITION_MARKER_OBSERVED
DIRECT_OVIPOSITION_MARKER_NOT_OBSERVED
MARKER_NOT_VALIDATED / NOT_EVALUABLE.
```

Later seed damage may validate a causal exposure-to-damage link without proving that the exact egg-laying event was visually observed. The two claims remain separate.

## Phase B outcomes

For every candidate window, record downstream:

```text
pollen receipt
apparent bract area during exposure
resin amount / gland state
predated seed fraction
mature intact seeds
plant and blossom retention.
```

Run:

```bash
python scripts/evaluate_dalechampia_stage0.py exposure <csv> <frozen_config.json>
```

The registered analysis uses within-plant paired contrasts against E0 and bootstraps complete plants.

## Promotion rule

A candidate window is promotable only when it produces a predeclared antagonist damage increase while remaining within predeclared tolerances for:

```text
pollen receipt
measured z
resin / reward state.
```

The output is only:

```text
SELECTIVE_G_WINDOW_CANDIDATE
```

not `mechanism identified`.

## Stop rules

### Stop D1 — no conflict-active context

If reasonable population/season screening does not recover a context in which both pollination and seed predation track the same display axis, do not force Dalechampia into the positive Chapter-1 experiment.

Action:

```text
retain Dalechampia as context-dependence evidence
-> switch causal compromise closure to Castilleja or another qualified system.
```

### Stop D2 — no selective antagonist window

If no adult-exposure window increases later seed loss without materially altering pollination, z, resin, or blossom condition:

```text
Dalechampia remains an observational compromise anchor
but is not used for mechanism-resolved L3.
```

### Stop D3 — enclosure artefact

If sham enclosures alter pollen receipt, bract posture, resin, or later seed development beyond the predeclared tolerance, redesign the enclosure before interpreting any G result.

### Stop D4 — antagonist identity unresolved

If exposed adults cannot be assigned to a biologically coherent antagonist taxon or treatment class, the package is `NOT_EVALUABLE` for a taxon-specific mechanism claim.

## Unlock condition for the main experiment

Proceed to the Chapter-1 multi-level experiment only after:

```text
population qualification = PASS
reversible z manipulation = PASS
pollinator intervention/selectivity = PASS
controlled G exposure/selectivity = PASS
sham/direct-cost checks = PASS.
```

Then run the registered target:

```text
>= 5 z levels x 2 P states x 2 G states
-> W(z,G,P)
-> z1*, z2*, zc*
-> optimum displacement
-> gradient cancellation.
```

## Provenance and claim boundary

Primary literature supports the existence of a Mexican `D. scandens` conflict case and shows that northern Costa Rican populations need not reproduce that relationship. It also supports the floral developmental sequence and the existence of later predispersal seed damage. It does not supply a validated `Nanobaris` cage protocol or a universally resolved adult oviposition window.

Accordingly, controlled adult exposure is a new Stage-0 method to validate in this system, not a recovered published Nanobaris protocol.
