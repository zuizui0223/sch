# Pedicularis rex powered full-surface allocation v1

## Purpose

The P2 full-surface experiment now has two prospective sample-size layers:

```text
CAL-C
  -> enough replication to validate P0/P1/G interventions

W1/W2 power
  -> enough replication to recover the biology-first full-surface headline
     conditional on valid interventions.
```

A powered design is not enough if the field allocation drifts from the design
that was simulated.

This contract binds the W1/W2 power receipt to treatment-blind flower IDs before
P2 outcomes exist.

## Files

```text
empirical/architecture/PEDICULARIS_FULL_SURFACE_FLOWER_MANIFEST_TEMPLATE_V1.csv
empirical/architecture/PEDICULARIS_FULL_SURFACE_ALLOCATION_CONFIG_TEMPLATE_V1.json
scripts/build_pedicularis_full_surface_allocation.py
scripts/prepare_pedicularis_full_surface_field_sheet.py
```

## Step 1 — freeze the actual P2 field design

The allocation config freezes:

- population and season;
- planned number of plants;
- flowers per plant;
- ordered z-level labels/ranks;
- nominal target exsertion for every z level;
- the already-qualified excluded and exposed G method codes;
- confirmation that the config was frozen before full-surface outcomes.

The config does **not** choose those values.

## Step 2 — require an actually powered candidate

The allocator accepts only a current W1/W2 power receipt.

It requires:

```text
same population / season
same nominal z grid
same flowers_per_plant
same balanced cyclic allocation strategy.
```

The planned plant count must match exactly one candidate that was actually
evaluated in the power simulation.

That candidate must satisfy both:

```text
primary_surface_power >= registered primary target

headline_W1_or_W2_power >= registered headline target.
```

Using an unevaluated plant count, a smaller convenient n, or a different
flowers-per-plant design fails closed.

## Step 3 — register treatment-blind flowers

Before treatment assignment, the field manifest contains only:

```text
population_id
season_id
plant_id
flower_id.
```

Every plant must contribute exactly the prospectively frozen number of flowers.
Flower IDs must be globally unique.

## Step 4 — exact balanced random allocation

Run:

```bash
python scripts/build_pedicularis_full_surface_allocation.py \
  <treatment_blind_flower_manifest.csv> \
  <frozen_allocation_config.json> \
  <w1_w2_power_receipt.json> \
  --allocation-seed <PRECOMMITTED_NEUTRAL_SEED> \
  --allocations-out <p2_allocations.csv> \
  --receipt-out <p2_allocation_receipt.json>
```

The allocation method is:

```text
SHA256_BALANCED_CYCLIC_Z_BY_P_BY_G_V1.
```

The number of cells is not hard-coded:

```text
n_surface_cells = n_z_levels x 2 P x 2 G.
```

Thus five z levels give 20 cells, six levels give 24, and so on.

The precommitted seed deterministically randomizes:

1. the global cell order;
2. plant order;
3. treatment-blind flower order within plant.

Each plant receives nonduplicated cells. Across all plants every cell receives
exactly the same total replication.

The script does not choose:

- n plants;
- flowers per plant;
- z levels;
- method codes;
- power targets;
- biological thresholds.

## Complete and incomplete blocks

A complete block is allowed but not required.

If there are five z levels:

```text
20 cells total.

6 plants x 20 flowers = 120 flowers = 6 per cell
  -> complete block.

10 plants x 4 flowers = 40 flowers = 2 per cell
  -> balanced incomplete block.
```

For six z levels:

```text
24 cells total.

8 plants x 6 flowers = 48 flowers = 2 per cell.
```

The field design must match the one used in the W1/W2 power receipt.

## Step 5 — generate the locked field sheet

Do not manually copy allocations into the P2 outcome table.

Run:

```bash
python scripts/prepare_pedicularis_full_surface_field_sheet.py prepare \
  <p2_allocations.csv> \
  <p2_allocation_receipt.json> \
  --field-sheet-out <p2_field_sheet.csv> \
  --identity-lock-out <p2_field_identity_lock.json>
```

Only frozen identity/treatment fields are prefilled:

- population / season;
- plant / flower;
- assigned z level;
- pollination treatment;
- predator treatment;
- qualified exclusion/sham method;
- z-rank / nominal target / allocation-cell provenance.

Biological outcome columns remain blank.

## Step 6 — verify after field collection

After all P2 outcomes are entered:

```bash
python scripts/prepare_pedicularis_full_surface_field_sheet.py verify \
  <completed_p2_field_sheet.csv> \
  <p2_field_identity_lock.json> \
  --require-complete \
  --receipt-out <p2_field_verification.json>
```

Verification rejects:

- flower substitution;
- missing or extra rows;
- duplicate flowers;
- z/P/G treatment drift;
- method-code drift;
- incomplete canonical outcome cells.

A complete positive receipt contains the exact canonical surface-data SHA-256.

## Step 7 — production analysis is verification-gated

The production CLI now requires the complete verification receipt:

```bash
python scripts/analyze_pedicularis_full_surface.py \
  <completed_p2_field_sheet.csv> \
  <pedicularis_readiness_v3.json> \
  <frozen_surface_config.json> \
  --field-verification <p2_field_verification.json> \
  --output <sch_pedicularis_receipt.json>
```

The analyzer recomputes the canonical surface-data SHA-256 and fails if it does
not match the verification receipt.

Therefore a field CSV cannot be edited after verification and silently analyzed
as the registered P2 experiment.

## Relationship to the W0-W5 paper

This contract changes no biological estimand.

It protects the chain:

```text
powered field design
-> exact randomized implementation
-> exact verified flower-level dataset
-> primary full surface
-> secondary antagonist displacement diagnostic
-> predeclared W0-W5 classification.
```

It produces no positive biological result by itself.

## Claim ceiling

The allocation and verification receipts support execution integrity only.

They do not establish:

- causal compromise;
- W1/W2;
- enemy-induced optimum displacement;
- a positive pollen response;
- pure-function optima;
- historical adaptation.
