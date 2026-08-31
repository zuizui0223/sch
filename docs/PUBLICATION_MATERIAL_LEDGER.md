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

A later identical OpenAlex query returned `10,969 -> 2,108 -> 869`; this is `LIVE_INDEX_DRIFT_DETECTED`, not a denominator update. The Batch-2 triage also detected one record whose live abstract no longer reproduces the frozen concept hit. That record remains in the frozen cohort and is adjudicated normally; live metadata drift never deletes or renumbers a frozen record.

## Current screening state — Batch 1 complete, Batch 2 high-information full text closed

Formal decisions are cumulative sparse overlays. Batch 1 (`SCHPRISMA-000001`–`000100`) is completely screened at title/abstract stage and every retained Batch-1 report has a full-text decision. Batch 2 has a frozen 100-record machine-assistance packet; its 29 highest-information records—nine title triples, nineteen title pairs and one live-concept-drift record—have formal title/abstract decisions. All 26 reports retained from this high-information screen now have source-verified full-text decisions: nine are included and seventeen are excluded. Batch-2 high-information full-text adjudication is therefore closed.

Because nine previously source-adjudicated/evolutionary records lie outside Batch 1, the cumulative PRISMA state is:

```text
identified frozen cohort:        868
title/abstract screened:         138
retained for full text:           95
title/abstract excluded:          43
unscreened:                      730

full-text eligible:               95
primary studies included:         44
full-text excluded:               51
full-text undecided:               0

STRICT_LINKED_EXPERIMENT:           2
DIRECTIONAL_OR_NEAR_PASS:          38
EVOLUTIONARY_OUTCOME:              12
```

The three Batch-2 high-information title/abstract exclusions are non-study objects: two eLife decision letters and one Dryad dataset record. Of the 26 reports retained conservatively for full text, nine are now included and seventeen excluded. The resulting cumulative state is 44 primary inclusions and 51 full-text exclusions. The geography counters remain 8/9/8 because V11 closes evidence eligibility without retroactively inferring geography from titles or author affiliations.

The strict linked measurement architecture now occurs in **two** studies: Theis & Adler 2012 and Sánchez-Lafuente 2007 (*Linaria lilacina*). The gate remains:

The two passes sharpen rather than close the conflict claim. In Theis & Adler, enhanced fragrance increased florivore attraction and reduced seed production but did not produce a detected increase in pollinator attraction. In *Linaria*, corolla manipulation changed pollinator response and reproduction, while fruit-predator visitation was not affected by the manipulation. Thus linked measurement architecture now replicates across two systems, but a single manipulated `A` showing both positive pollinator response and positive antagonist response remains unrecovered.

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common reproductive outcome
```

### Informative near-passes already retained without promotion

- **Reisenman et al. 2010, *Datura*–*Manduca***: synthetic floral scent/linalool is manipulated and adult feeding plus female oviposition are measured on the same chemical coordinate, but there is no plant reproductive outcome. This is a strong same-code near-pass, not strict.
- **Disa similis 2025**: yellow anther-mimic petal apices are painted/excised and fruit set changes; the same pollen-feeding beetle also florivores those apices, but florivory was not estimated as a response to `do(A)`. This is `DIRECTIONAL_OR_NEAR_PASS`, not a second strict experiment.
- **Delphinium caeruleum 2022**: nectar-robbing context changes the staminode visitor-screening mechanism, pollinator visitation and pollen transfer; the focal floral coordinate is not itself randomized.
- **Cassia fistula 2021**: stamen exclusion and pollen functionality recover pollinating-versus-feeding division of labour, supporting partial modularity without a common net-fitness test.

### Batch-2 high-information full-text closure

All 26 retained high-information reports have now been adjudicated. V11 contributes nine inclusions and seven exclusions after the ten V10 exclusions. The next systematic work object is the remaining 71 Batch-2 title/abstract records, followed by later batches. Full-text closure of the currently retained set does not authorize pooled effects and does not mean the 868-record screen is complete.

## Full-text exclusion and independence boundary

The 51 completed full-text exclusions include review/meta-analysis/species-synthesis records, duplicate reports, records lacking a declared floral `A`, or records lacking one required biological channel. Reviews remain useful source-registry material but are not double-counted as primary included studies.

Preprint/published duplicates are clustered rather than counted twice. Dissertation chapters that overlap published articles are flagged for independence coding before any cross-study synthesis. Dataset and peer-review objects are excluded as reports without removing the corresponding primary publication or data provenance from the source registry.

## Geography / JBI gate

The audit distinguishes:

1. `geographic_contrast_positive` — a real spatial contrast;
2. `receiver_assemblage_contrast_positive` — a real pollinator/antagonist/interactor-regime contrast;
3. `joint_geographic_receiver_positive` — **both occur in the same included record**.

Current full-text-coded counts remain:

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

Thus the JBI axis is no longer resting on one isolated anchor. It remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 730 records remain title/abstract unscreened, and no common geography-by-cue-overlap estimand has passed independence/scale checks.

A map of study locations cannot rescue a failed geography gate.

## Evolutionary-outcome recovery

The **12-source primary audit** remains the historical backbone, and systematic additions strengthen several bounded outcomes:

- integrated compromise and context-dependent selection;
- population-level interaction mosaics;
- experimental evolutionary redirection under pollinators and antagonists;
- component/stamen functional partitioning and conditional cue deployment.

**lineage branching untested** remains the claim ceiling. Population differentiation, experimental divergence, and partner-loss comparisons are not ancestral shared-to-private reconstructions.

## Paper spine

| Paper component | Material in hand | Current use | Missing gate |
|---|---|---|---|
| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 730 records |
| Estimands | `M_A`, `G_A`, `S_A = M_A - G_A`, direct cost separate | Keeps SCH distinct from BITA `Delta_AD W` | Effect-size scale and outcome compatibility rules |
| Evolutionary outcomes | **12-source primary audit** + systematic additions | Compromise, modularity, population change, experimental evolution | Historical branching/L4 still absent |
| Frozen coverage audit | BITA-derived route candidates and source-adjudicated anchors | Existence and near-pass classes. **Do not insert them into the frozen four-field coverage count** without a separate admission pass. | Not a prevalence denominator |
| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | Screen remaining 730 |
| Batch 1 | 100/100 TA decisions; retained reports fully closed | First complete systematic batch | Closed |
| Batch 2 high-information | 29/29 TA decisions; 26 retained; 26/26 FT decided | Prioritized second-batch gate | Closed; next screen remaining 71 Batch-2 records |
| Formal screening cumulative | 138 TA decisions; 44 primary includes; current FT backlog 0 | Evidence lanes and blockers | Continue title/abstract screening: 730 remain |
| Strict experiments | Theis & Adler 2012; Sánchez-Lafuente 2007 | Two strict linked measurement architectures | Neither closes simultaneous positive pollinator and antagonist response to the same manipulated A |
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
| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 138 TA decisions; 51 FT exclusions; 0 FT undecided |
| Figure 3 | Geographic receiver-regime synthesis | 8 joint-positive systems; final analysis waits for full screen |
| Figure 4 | *Ficus* same-code historical bridge | Core data/matrix fixed |
| Table 1 | Systematic study decisions/blockers | 138 TA screened; 44 primary includes; current FT queue closed |
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
