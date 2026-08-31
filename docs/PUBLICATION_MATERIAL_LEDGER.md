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

## Current screening state — Batch 3 title/abstract complete under V16

Formal decisions are cumulative sparse overlays. Batch 1 (`SCHPRISMA-000001`–`000100`) is completely screened at title/abstract stage and every retained Batch-1 report has a full-text decision. Batch 2 has a frozen 100-record machine-assistance packet. The 29 high-information records were adjudicated first and their retained full texts were closed in V11. V12 then adjudicates the remaining 70 previously undecided Batch-2 records; `SCHPRISMA-000172` was already source-adjudicated in V1 and is therefore not screened twice. Batch 2 is now 100/100 complete at title/abstract stage.

Because nine previously source-adjudicated/evolutionary records lie outside Batch 1, the cumulative PRISMA state is:

```text
identified frozen cohort:        868
title/abstract screened:         307
retained for full text:          202
title/abstract excluded:         105
unscreened:                      561

full-text eligible:              202
primary studies included:         73
formal full-text exclusions:      85
full-text undecided:              44

STRICT_LINKED_EXPERIMENT:           2
DIRECTIONAL_OR_NEAR_PASS:          64
EVOLUTIONARY_OUTCOME:              22
HISTORICAL_TRANSITION:               1
```

V13 adjudicates all 35 reports newly retained by V12: nine are included, twenty-five are assessed full-text exclusions, and one is a retrieval failure (`FT_FULLTEXT_UNAVAILABLE`). Cumulatively, 53 studies are included, 76 assessed reports are excluded at full text, one sought report was not retrieved, and no currently retained report remains undecided.

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
- **Junker & Blüthgen 2010**: the same synthetic floral-scent coordinate attracts bumblebees while repelling ants; this is a clean opposite-receiver same-code near-pass, but it lacks a common plant reproductive outcome.
- **Kleinschmidt et al. 2023, *Lithophragma bolanderi*–*Greya***: floral morphology, pollinator community, pollination efficacy and oviposition differ between populations, supporting a geographic coevolutionary mosaic without randomized `do(A)`.

### Batch-3 title/abstract closure under V16

Batch 2 remains closed. V15 closed all 28 high-information Batch-3 full texts. V16 now adjudicates the remaining 66 genuinely new Batch-3 title/abstract records: 44 are retained for full text and 22 excluded. Batch 3 is therefore 100/100 complete at title/abstract stage, and the current Batch-3 full-text backlog is 44. This does not authorize pooled effects and does not mean the 868-record screen is complete.

## Full-text exclusion and independence boundary

The current formal exclusion ledger contains 85 decisions: 84 assessed full-text exclusions plus one `FT_FULLTEXT_UNAVAILABLE` retrieval outcome. The assessed exclusions include review/meta-analysis/species-synthesis records, duplicate reports, records lacking a declared floral `A`, or records lacking one required biological channel. The unavailable report is not counted as assessed for eligibility. Reviews remain useful source-registry material but are not double-counted as primary included studies.

Preprint/published duplicates are clustered rather than counted twice. Dissertation chapters that overlap published articles are flagged for independence coding before any cross-study synthesis. Dataset and peer-review objects are excluded as reports without removing the corresponding primary publication or data provenance from the source registry.

## Geography / JBI gate

The audit distinguishes:

1. `geographic_contrast_positive` — a real spatial contrast;
2. `receiver_assemblage_contrast_positive` — a real pollinator/antagonist/interactor-regime contrast;
3. `joint_geographic_receiver_positive` — **both occur in the same included record**.

Current full-text-coded counts remain:

```text
positive geographic contrasts:         13
positive receiver/interactor contrasts:12
joint geography + receiver records:    11
```

The eleven joint-positive records are:

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
SCHPRISMA-000151  Lithophragma bolanderi
                   two-population floral morphology / pollinator-community / local-efficacy divergence
SCHPRISMA-000217  Lithophragma heterophyllum / L. parviflorum
                   Hopland-versus-Hastings floral-visitor assemblage and Greya pollinating-parasite contrast
SCHPRISMA-000167  Primula farinosa
                   thesis/manuscript selection mosaic; same research program as SCHPRISMA-000523
SCHPRISMA-000172  Biscutella laevigata
                   lowland/highland crab-spider regime and beta-ocimene inducibility
SCHPRISMA-000523  Primula farinosa
                   69-population pollinator/grazer selection mosaic plus microevolution
SCHPRISMA-000710  Gentiana lutea
                   12-population flower-colour / pollinator-community / selection gradient
```

`SCHPRISMA-000075` (eight-generation bee × aphid experimental evolution) has a real receiver-regime contrast but is deliberately **not** geographic. Likewise, multisite sampling alone is not positive geography: the 25-orchard ant study is coded `NO_REPLICATED_GEOGRAPHIC_RECEIVER_REGIME_CONTRAST` because its focal comparison is floral architecture/visitor role rather than spatial turnover in receiver regimes.

Thus the JBI axis is no longer resting on one isolated anchor. V15 yields 11 joint-positive records, but record count is not an independence count: the two *Primula farinosa* records are one research program, and the two *Lithophragma* records also require explicit program/system clustering before quantitative synthesis. JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 561 records remain title/abstract unscreened, 44 newly retained Batch-3 reports await full-text adjudication, and no common geography-by-cue-overlap estimand has passed independence/scale checks.

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
| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 627 records |
| Estimands | `M_A`, `G_A`, `S_A = M_A - G_A`, direct cost separate | Keeps SCH distinct from BITA `Delta_AD W` | Effect-size scale and outcome compatibility rules |
| Evolutionary outcomes | **12-source primary audit** + systematic additions | Compromise, modularity, population change, experimental evolution | Historical branching/L4 still absent |
| Frozen coverage audit | BITA-derived route candidates and source-adjudicated anchors | Existence and near-pass classes. **Do not insert them into the frozen four-field coverage count** without a separate admission pass. | Not a prevalence denominator |
| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 561 records remain title/abstract unscreened |
| Batch 1 | 100/100 TA decisions; retained reports fully closed | First complete systematic batch | Closed |
| Batch 2 | 100/100 TA decisions; all currently retained reports resolved at full text under V13 | Second systematic batch | Closed; proceed to Batch 3 TA screening |
| Batch 3 | 100/100 TA decisions; V15 closes the 28 high-information full texts; V16 retains 44 additional reports | Third systematic batch | Full-text adjudicate 44 newly retained reports |
| Formal screening cumulative | 307 TA decisions; 73 primary includes; 84 assessed FT exclusions; 1 not retrieved; FT backlog 44 | Evidence lanes and blockers | Close 44 newly retained Batch-3 full texts, then advance to Batch 4 |
| Strict experiments | Theis & Adler 2012; Sánchez-Lafuente 2007 | Two strict linked measurement architectures | Neither closes simultaneous positive pollinator and antagonist response to the same manipulated A |
| Same-code near-pass | Reisenman 2010 | Identical chemical-coordinate feeding/oviposition contrast | Common plant reproductive outcome |
| Geography | 11 joint-positive records; independence count not frozen | JBI axis empirically plausible | Complete screen, cluster overlapping programs, define common analytic question |
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
| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 241 TA decisions; 53 includes; 76 assessed FT exclusions; 1 not retrieved; 28 FT pending |
| Figure 3 | Geographic receiver-regime synthesis | 8 joint-positive systems; final analysis waits for full screen |
| Figure 4 | *Ficus* same-code historical bridge | Core data/matrix fixed |
| Table 1 | Systematic study decisions/blockers | 241 TA screened; 53 primary includes; 28 FT pending |
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
