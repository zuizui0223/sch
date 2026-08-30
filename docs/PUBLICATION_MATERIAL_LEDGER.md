# Publication material ledger

## Editorial boundary

This ledger organizes the one-trait shared-cue paper without importing BITA's two-trait estimand. The current first-choice target is **Journal of Biogeography, Review & Synthesis**, conditional on the systematic-review and biogeographic gates in `docs/SCH_JBI_SUBMISSION_CONTRACT_V1.md`. The fallback remains **Ecology and Evolution** if the systematic synthesis is strong but the geography axis is not analytically consequential.

The older frozen audit remains a source-recovery and claim-boundary result; it is not retroactively relabelled as a systematic-review denominator. Its **existing-study integration plus shared-cue framework** fork remains preserved as provenance. If the strict linked set remains sparse, the legacy **paired-channel measurement gap** remains a valid paper-level result rather than a reason to relax admission. **No pooled effect is authorized** until outcome scale, independence and commensurability pass separate gates.

## Frozen systematic denominator

V1 is retained only as failed-method provenance:

```text
OpenAlex + broad Crossref discovery
raw query/database hits: 5,406
deduplicated records:    2,684
25/28 query×database combinations hit the 200-record cap
status: PRISMA_IDENTIFICATION_TRUNCATED
```

The first complete V2 OpenAlex run is the immutable screening cohort:

```text
retrieved_at_utc:                  2026-08-29T06:59:57Z
raw OpenAlex records retrieved:   10,953
concept-pass query hits:           2,107
deduplicated frozen cohort:          868
truncated queries:                     0
known frozen anchors recovered:      8/8
candidate CSV SHA-256:
ee85f56ae500be17ed45f9010b0a75fa8f6b741b0967db5af596b2d7bb8579a0
status: PRISMA_V2_IDENTIFICATION_COMPLETE
```

Permanent files are under `empirical/prisma/frozen_v2/`. Record IDs and the denominator are never regenerated from the live index.

A later identical OpenAlex query returned `10,969 -> 2,108 -> 869`; this is `LIVE_INDEX_DRIFT_DETECTED`, not a denominator update. Live retrieval failure also cannot invalidate the frozen cohort.

## Current screening state — Batch 1 complete

Formal decisions are cumulative sparse overlays. Batch 1 (`SCHPRISMA-000001`–`000100`) is now completely screened at title/abstract stage, and every record retained from the currently decided set has also received a full-text decision.

Because nine previously source-adjudicated/evolutionary records lie outside Batch 1, the cumulative PRISMA state is:

```text
identified frozen cohort:        868
title/abstract screened:         109
retained for full text:           69
title/abstract excluded:          40
unscreened:                      759

full-text eligible:               69
primary studies included:         35
full-text excluded:               34
full-text undecided:               0

STRICT_LINKED_EXPERIMENT:           1
DIRECTIONAL_OR_NEAR_PASS:          30
EVOLUTIONARY_OUTCOME:              11
```

The strict linked result remains **Theis & Adler 2012 only**. The gate remains:

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common reproductive outcome
```

### Informative near-passes retained without promotion

- **Reisenman et al. 2010, *Datura*–*Manduca***: synthetic floral scent/linalool is manipulated and adult feeding plus female oviposition are measured on the same chemical coordinate, but there is no plant reproductive outcome. This is a strong same-code near-pass, not strict.
- **Disa similis 2025**: yellow anther-mimic petal apices are painted/excised and fruit set changes; the same pollen-feeding beetle also florivores those apices, but florivory was not estimated as a response to `do(A)`. This is `DIRECTIONAL_OR_NEAR_PASS`, not a second strict experiment.
- **Delphinium caeruleum 2022**: nectar-robbing context changes the staminode visitor-screening mechanism, pollinator visitation and pollen transfer; the focal floral coordinate is not itself randomized.
- **Cassia fistula 2021**: stamen exclusion and pollen functionality recover pollinating-versus-feeding division of labour, supporting partial modularity without a common net-fitness test.

## Full-text exclusion boundary

The 34 full-text exclusions include review/meta-analysis/species-synthesis records, duplicate reports, records lacking a declared floral `A`, or records lacking one of the required biological channels. Reviews remain useful source-registry material but are not double-counted as primary included studies.

Preprint/published duplicates are clustered rather than counted twice. Dissertation chapters that overlap published articles are flagged for independence coding before any cross-study synthesis.

## Geography / JBI gate

The audit now distinguishes:

1. `geographic_contrast_positive` — a real spatial contrast;
2. `receiver_assemblage_contrast_positive` — a real pollinator/antagonist/interactor-regime contrast;
3. `joint_geographic_receiver_positive` — **both occur in the same included record**.

Current counts:

```text
positive geographic contrasts:          8
positive receiver/interactor contrasts: 9
joint geography + receiver contrasts:   8
```

The eight joint-positive records are:

```text
SCHPRISMA-000008  Erysimum mediohispanicum
                   eight-population pollinator / ungulate / selection mosaic
SCHPRISMA-000032  Barbarea vulgaris
                   14-site landscape herbivory -> floral display -> pollination pathway
SCHPRISMA-000066  Primula secundiflora
                   six-population nectar-robber / syrphid visitor mosaic
SCHPRISMA-000067  Trollius europaeus
                   Chiastocheta-present versus absent/extinct nursery-pollination populations
SCHPRISMA-000074  coffee agroecosystem dissertation
                   coffee-field versus forest-fragment nectar-robbing context
SCHPRISMA-000172  Biscutella laevigata
                   lowland/highland crab-spider regime and beta-ocimene inducibility
SCHPRISMA-000523  Primula farinosa
                   69-population pollinator/grazer selection mosaic plus microevolution
SCHPRISMA-000710  Gentiana lutea
                   12-population flower-colour / pollinator-community / selection gradient
```

`SCHPRISMA-000075` (eight-generation bee × aphid experimental evolution) has a real receiver-regime contrast but is deliberately **not** geographic. Likewise, multisite sampling alone is not positive geography: the 25-orchard ant study is coded `NO_REPLICATED_GEOGRAPHIC_RECEIVER_REGIME_CONTRAST` because its focal comparison is floral architecture/visitor role rather than spatial turnover in receiver regimes.

Thus the JBI axis is no longer resting on one isolated anchor. It remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 759 records remain unscreened and no common geography-by-cue-overlap estimand has yet passed independence/scale checks.

A map of study locations cannot rescue a failed geography gate.

## Evolutionary-outcome recovery

The **12-source primary audit** remains the historical backbone, and systematic additions now strengthen several bounded outcomes:

- integrated compromise and context-dependent selection;
- population-level interaction mosaics;
- experimental evolutionary redirection under pollinators and antagonists;
- component/stamen functional partitioning and conditional cue deployment.

**lineage branching untested** remains the claim ceiling. Population differentiation, experimental divergence, and partner-loss comparisons are not ancestral shared-to-private reconstructions.

## Paper spine

| Paper component | Material in hand | Current use | Missing gate |
|---|---|---|---|
| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 759 records |
| Estimands | `M_A`, `G_A`, `S_A = M_A - G_A`, direct cost separate | Keeps SCH distinct from BITA `Delta_AD W` | Effect-size scale and outcome compatibility rules |
| Evolutionary outcomes | **12-source primary audit** + systematic additions | Compromise, modularity, population change, experimental evolution | Historical branching/L4 still absent |
| Frozen coverage audit | BITA-derived route candidates and source-adjudicated anchors | Existence and near-pass classes. **Do not insert them into the frozen four-field coverage count** without a separate admission pass. | Not a prevalence denominator |
| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | Screen remaining 759 |
| Batch 1 | 100/100 TA decisions; retained reports fully closed | First complete systematic batch | Proceed to Batch 2 |
| Formal screening cumulative | 109 TA decisions; 35 primary includes; FT backlog 0 | Evidence lanes and blockers | Remaining 759 TA records |
| Strict experiment | Theis & Adler 2012 | One strict linked directional anchor | Uncertainty-bearing focal A effect unavailable |
| Same-code near-pass | Reisenman 2010 | Identical chemical-coordinate feeding/oviposition contrast | Common plant reproductive outcome |
| Geography | 8 joint positive spatial receiver-regime records | JBI axis empirically plausible | Complete screen, independence, common analytic question |
| Ficus history | fixed 32-species scaffold + same-code gate | `COMPOSITE_NEAR_L4` | Same-code NPFW assays, then historical state reconstruction |

## Planned article structure

1. Geographic turnover in biotic audiences as a constraint on shared versus separable floral cues.
2. Define `M_A`, `G_A`, `S_A` and direct-cost boundary.
3. Derive shared/private-cue predictions.
4. Separate compromise, polymorphism, population differentiation, partial modularization and historical branching.
5. Report frozen PRISMA flow and evidence lanes.
6. Analyze geography/receiver-regime contrasts only after independence and commensurability coding.
7. Use *Ficus* as a bounded historical bridge, not the whole source universe.
8. Report the information asymmetry between detecting interception and supporting behavioral privacy.
9. End with same-code experiments and historical-state reconstruction required for L4.

## Figure and table recovery plan

| Item | Purpose | Source state |
|---|---|---|
| Figure 1 | Shared-cue versus private-cue mechanism | Concept fixed |
| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; Batch 1 complete |
| Figure 3 | Geographic receiver-regime synthesis | 8 joint-positive systems; final analysis waits for full screen |
| Figure 4 | *Ficus* same-code historical bridge | Core data/matrix fixed |
| Table 1 | Systematic study decisions/blockers | 109 screened; 35 primary includes |
| Table 2 | Evidence-role registry and prohibited uses | Systematic update in progress |
| Table 3 | Evolutionary-outcome ledger | Primary audit + systematic additions |

## Admission and stop rules

- The strict coverage gate remains unchanged.
- Lower evidence layers may be retained with explicit claim ceilings but are never counted as strict linked experiments.
- `FAIL`, `NOT_EVALUABLE`, inaccessible raw data, split outcomes and observational A remain results.
- Total plant fitness under `A` does not itself allocate `M_A` and `G_A`.
- The frozen 868 records are identified candidates, not included studies.
- `UNSCREENED` is never exclusion.
- Machine triage may order review but cannot populate formal decisions.
- Live bibliographic drift cannot change the frozen denominator during screening.
- Geography missing from a source is `NOT_REPORTED`; it is never inferred from author affiliation.
- Multisite sampling is not automatically a positive geographic contrast.
- **No pooled effect is authorized** by screening completion alone; outcome scale, independence and commensurability must pass separately.
- JBI is promoted only after systematic completion and an analytically consequential geography/receiver-regime result; otherwise Ecology and Evolution remains the fallback.
