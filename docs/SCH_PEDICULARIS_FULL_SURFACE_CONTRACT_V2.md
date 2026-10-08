# SCH Pedicularis full-surface contract v2

## Purpose

This is the registered Chapter-1 execution contract for `Pedicularis rex` when the same species is intended to continue into BITA Chapter 2.

The core change from V1 is causal independence between the SCH antagonist intervention and the BITA water-defence axis.

```text
SCH / Chapter 1
z = exsertion
P = pollination dependence
G = independent seed-predator exposure
water-defence y = held fixed

BITA / Chapter 2
x = exsertion
y = water-defence state / water-retention phenotype.
```

This separation makes the Chapter-2 release test non-circular.

## Threshold provenance gate

Every P0, P1 and G receipt entering V3 readiness must carry positive
`SCH_PEDICULARIS_THRESHOLD_FREEZE_V1` provenance for the same population and
season. The canonical full-surface analyzer rechecks those freeze statuses and
rejects a hand-written READY receipt that omits them.

See `docs/SCH_PEDICULARIS_THRESHOLD_FREEZE_CONTRACT_V1.md`.

## Required readiness receipt

The full surface may run only after the same population and season produce:

```text
z manipulation receipt
  SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1

pollination-weight receipt
  SCH_PEDICULARIS_POLLINATION_WEIGHT_V1

method-qualified independent predator receipt
  SCH_PEDICULARIS_PREDATOR_METHOD_V4
```

The predator method receipt must include both the antagonist-effect/selectivity result and a method-timing qualification showing that the barrier was applied in a registered post-pollination / pre-ovary-swelling window, or by an equivalently validated local barrier, without covering the pollinator-entry zone.

These receipts are assembled by:

```text
scripts/assemble_pedicularis_full_surface_readiness.py
```

The required readiness schema is:

```text
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3
```

and it must contain:

```text
water_y_requirement = HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE
predator_method_requirement = TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED.
```

Earlier readiness receipts are rejected.

V3 now also means **randomized execution provenance is positive**, not merely
that three biological gate statuses are positive. The assembled receipt must
show:

```text
P0  exact treatment-blind flower -> z/sham allocation verified
P1  exact paired NATURAL-sham vs SUPPLEMENTED allocation verified
G   exact preselected-method EXPOSED-sham vs EXCLUDED allocation verified
```

It carries SHA-256 provenance for all three source receipts and stores the
validated z-level labels, paired P1 experimental unit and selected G exclusion
method. The P2 analyzer rechecks this provenance and rejects a raw P2 dataset
whose z labels or EXCLUDED method differ from the validated interventions.

## Prospective primary-surface threshold freeze

The primary surface decision rules must be frozen independently of geometry and
P2 outcomes. Use:

```text
empirical/architecture/PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_TEMPLATE_V1.json
scripts/freeze_pedicularis_full_surface_thresholds.py
```

The receipt binds the exact `sch_surface` and `system_checks` objects by
SHA-256 and requires an explicit pre-outcome basis note for **every** registered
decision threshold, including the water-depth and mechanical-damage tolerances.
These same objects must appear in the registered W1/W2 power config, survive P2
allocation/field verification, and be supplied unchanged to the production
analyzer.

See `docs/SCH_PEDICULARIS_FINAL_W1_W2_BASIS_V1.md`.

## Registered state mapping

The shared coordinate is:

```text
z = realized corolla exsertion above the cupulate bract.
```

Pollination-weight states:

```text
P0 = SUPPLEMENTED
     focal flowers remain open, but standardized supplemental cross-pollen
     reduces dependence on natural pollinator-mediated pollen delivery

P1 = NATURAL
     open natural pollination; pollination-facing dependence remains active.
```

Independent antagonist states:

```text
G0 = PREDATOR_EXCLUDED
     seed-predator access is selectively suppressed by the method-qualified
     independent exclusion intervention

G1 = PREDATOR_EXPOSED
     matched exposed / sham condition; seed-predator pressure remains active.
```

The registered reproductive states are therefore:

```text
W00 = supplemented + predator excluded
W10 = natural      + predator excluded
W01 = supplemented + predator exposed
W11 = natural      + predator exposed.
```

## Water-defence y is held fixed

The water-retention defence state is **not** the SCH `G` intervention in V2.

```text
water defence is held fixed across every P/G/z cell.
```

The full-surface wrapper checks the realized water-depth range against a prospectively frozen tolerance and fails closed if water state differs materially among SCH cells.

This is essential because water defence is the intended BITA Chapter-2 `y` axis. Using the same water manipulation both to define the SCH reference and then to test BITA release toward that reference would create a circular cross-chapter test.

## Why method timing is now part of G

The known natural history places seed-predator oviposition after flowers open but before ovaries swell, with adults attacking from outside through the sepals or corolla tube. Pollination also occurs during the open-flower phase.

Therefore a barrier can reduce predation yet still be invalid for SCH if it is applied early enough to alter bumblebee access or pollen receipt.

The registered Stage-G method audit is:

```text
docs/SCH_PEDICULARIS_PREDATOR_EXCLUSION_METHOD_AUDIT_V1.md
```

and the timing/selectivity evaluator is:

```text
scripts/evaluate_pedicularis_predator_method.py
```

The preferred first pilot is a post-pollination lower-flower / fruit shield. A lower-corolla ovipositor barrier during anthesis remains a second-choice unvalidated method and must independently pass the same pollinator-access and pollen-receipt gates.

## Powered field-allocation integrity

A positive readiness receipt is necessary but no longer sufficient to run the
production P2 analysis.

Before outcomes are collected, the field design must be bound to both:

```text
1. the exact positive readiness V3 receipt that validated P0/P1/G;
2. a W1/W2 power candidate that actually meets both registered power targets.
```

Treatment-blind flower IDs are then allocated with:

```text
scripts/build_pedicularis_full_surface_allocation.py
```

The allocator fails before field assignment if the frozen design disagrees with
readiness on the P0 level-plan SHA, z-label/physical-setting mapping, G0
exclusion method, or G1 exposed-sham method. The allocation receipt fingerprints
the exact readiness JSON, and that fingerprint must survive field verification
and production analysis.

The allocator requires the same nominal z grid and flowers-per-plant design
that were powered, supports complete or balanced incomplete plant blocks, and
gives every z x P x G cell exactly equal total replication.

The allocation is materialized into an identity-locked field sheet with:

```text
scripts/prepare_pedicularis_full_surface_field_sheet.py prepare
```

After field collection, the same tool must pass:

```text
verify --require-complete
```

The verification receipt stores the canonical surface-data SHA-256. It also
carries the exact production-surface analysis-config SHA-256 from the registered
W1/W2 power receipt. The production full-surface CLI recomputes both digests and
rejects any altered/unverified dataset **or any change to the primary
`sch_surface` / system-check configuration after power was registered**.

See `docs/SCH_PEDICULARIS_FULL_SURFACE_ALLOCATION_V1.md`.

## Physical z-treatment identity

Confirmatory P2 must reuse the **validated physical P0 manipulation plan**, not
only its z labels.

The P2 allocation config therefore freezes:

```text
p0_level_plan_sha256
z_levels[*].manipulation_setting_id
```

and every field row carries the assigned manipulation-setting ID. The field
identity lock treats this ID as immutable. Production analysis requires both:

```text
row-level z label -> manipulation_setting_id mapping
==
validated P0 readiness mapping

AND

P2 field-packet p0_level_plan_sha256
==
validated P0 readiness p0_level_plan_sha256.
```

`target_exsertion` remains a prospective nominal phenotype used for design
and power. `realized_exsertion` remains the measured phenotype. Neither is a
substitute for the physical manipulation identity.

## Required biological dual-endpoint feasibility (new blocking gate)

The original focal 2016 study measured stigmatic pollen by removing/crushing
late-anthesis stigmas, but measured mature seeds about three weeks later on
generally different flowers from the same plants. The present P2 data contract
requires pollen plus mature seeds from **one and the same flower ID**. The
historical protocol does not validate that joint measurement.

Before **production** P2 allocation, obtain an independent, pre-outcome
compatibility-pilot receipt showing that the intended same-flower assay can
quantify stigma pollen accurately **and** preserve unbiased mature seed
production, with P/G treatment compatibility. The alternative of destructive
pollen sentinels on separate flowers is **not supported by the existing
single-flower W1/W2 estimator or power model** and needs a separately frozen
two-cohort redesign.

See `docs/SCH_PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_V1.md` for the
prospective template, acceptable routes and stop conditions.

The production P2 allocator additionally requires
`--endpoint-feasibility <p2_endpoint_feasibility.json>`; this binding persists
from allocation to field identity lock, complete verification, and the
production full-surface analyzer. Internal synthetic analyzers remain
available for simulation and cannot establish field feasibility.

## Raw-data contract

Template:

```text
empirical/architecture/PEDICULARIS_FULL_SURFACE_TEMPLATE_V2.csv
```

Required fields:

```text
population_id
season_id
plant_id
flower_id
assigned_z_level
manipulation_setting_id
realized_exsertion
pollination_treatment
predator_treatment
exclusion_method
water_depth
ovule_count
undamaged_seed_count
damaged_seed_count
pollen_grains
early_predator_attack_present
mechanical_damage.
```

Registered treatment values:

```text
pollination_treatment = NATURAL | SUPPLEMENTED
predator_treatment    = EXPOSED | EXCLUDED.
```

`exclusion_method` is retained as provenance. The method itself must already have passed `SCH_PEDICULARIS_PREDATOR_METHOD_V4`.

## Primary outcome

The common primary fitness outcome is:

```text
fitness_value = undamaged mature seed count per focal flower.
```

Mechanism-resolving secondary outcomes include:

```text
initial seed set
seed-predation fraction
pollen receipt
early predator attack
water depth
handling / mechanical damage.
```

## Analysis

Run:

```bash
python scripts/analyze_pedicularis_full_surface.py \
  <pedicularis_surface_v2.csv> \
  <pedicularis_readiness_v3.json> \
  <frozen_config_v2.json> \
  --field-verification <p2_field_verification.json> \
  --output <sch_pedicularis_receipt.json>
```

The wrapper validates the system-specific contract, checks that water-y stayed fixed, maps the treatment states to the generic SCH coding, and calls:

```text
scripts/analyze_sch_compromise_surface.py
```

After—and only after—a positive primary causal-compromise receipt, an optional
focal ecological diagnostic may be run:

```bash
python scripts/analyze_pedicularis_antagonist_constrained_pollination.py \
  <pedicularis_surface_v2.csv> \
  <sch_pedicularis_receipt.json>
```

This secondary diagnostic tests whether predator removal shifts the fitted
**state-specific reproductive optimum** toward greater exsertion while
randomized greater exsertion increases pollen receipt under natural
pollination. It is downstream of the primary SCH surface and cannot rescue a
negative compromise result. The full-surface receipt stores a canonical
SHA-256 fingerprint of the raw surface; the secondary diagnostic must receive
the exact same flower-level dataset and fails closed on any fingerprint or row-
count mismatch.

The predator-free state optimum remains a reproductive-state optimum, not a
pure pollinator optimum. A positive secondary diagnostic therefore supports an
antagonist-induced shift away from trait states with greater pollination
performance. It does not by itself establish that antagonists maintain pollen
limitation, and it is not adaptive pollen limitation.

The returned core receipt remains:

```text
SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
```

with system wrapper:

```text
SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2.
```

## Chapter-1 estimands

The registered state-specific optima are:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

A positive causal compromise requires:

```text
z_P* != z_G*
interior z_C*
opposing optimum shifts
opposed pollination and antagonist component gradients.
```

`z_P*` and `z_G*` are not automatically pure function optima.

## Pollination interpretation

Because `P0` is supplemental pollen rather than pollinator absence,

```text
W10(z) - W00(z)
```

measures the reproductive consequence of remaining dependent on natural pollen delivery relative to a saturated-pollen baseline.

Its shape across `z` is the pollination-facing selection signal. Its absolute value may be negative if supplementation raises reproduction.

## Antagonist interpretation

Because V2 uses a method-qualified independent predator intervention,

```text
W01(z) - W00(z)
```

isolates the reproductive consequence of seed-predator exposure under the supplemented-pollen state, subject to both the biological selectivity and timing/access validation of the exclusion method.

The Chapter-1 antagonist effect is therefore no longer defined by manipulating water defence.

## Optional pure-function promotion

After a positive V2 surface, the same converted SCH rows may be evaluated with:

```text
scripts/identify_sch_pure_function_optima.py
```

Only context-stable causal component optima may be promoted to:

```text
identified_pure_function_optima.z_F1
identified_pure_function_optima.z_F2.
```

## BITA handoff

The default BITA state-specific release reference is:

```text
z_P*.
```

BITA then manipulates the previously fixed water-defence axis:

```text
y0 = water defence disabled
y1 = water defence active
```

and tests:

```text
R_state = |x0* - z_P*| - |x1* - z_P*|.
```

Because water-y was held fixed while `z_P*` was identified, and the antagonist G was independently method-qualified, this is a non-circular test of dimensional release.

## V1 deprecation boundary

The older V1 Pedicularis surface used:

```text
G0 = water protected
G1 = water drained.
```

That design remains useful for acute water-defence mechanism description, but it must **not** be used as the SCH reference experiment for the same-species water-y BITA release test.

See:

```text
docs/SCH_PEDICULARIS_WATER_G_DEPRECATION_V1.md
```

## Stop rules

Do not run or promote V2 if:

```text
readiness schema is not V3;
method-qualified independent predator receipt is absent;
predator barrier timing or pollinator-access preservation has not passed;
raw data and readiness population/season differ;
powered P2 allocation / identity lock / complete field verification is absent;
field-verification SHA-256 does not match the exact analyzed CSV;
water depth varies beyond the preregistered tolerance;
handling damage exceeds tolerance;
<5 informative z levels remain;
primary fitness is not measured consistently across all cells.
```

## Claim ceiling

A positive V2 receipt supports:

```text
same-species contemporary causal compromise on exsertion
identified with an antagonist intervention independent of the BITA water-defence axis.
```

It does not by itself establish:

```text
structural independence of x and y
genetic/developmental modularity
architecture-level Delta_mod
historical one-trait -> two-trait transition.
```
