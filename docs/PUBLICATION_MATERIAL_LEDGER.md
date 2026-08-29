# Publication material ledger

## Editorial boundary

This ledger organizes the one-trait shared-cue paper without importing BITA's two-trait estimand. The current first-choice target is **Journal of Biogeography, Review & Synthesis**, conditional on the systematic-review and biogeographic gates in `docs/SCH_JBI_SUBMISSION_CONTRACT_V1.md`. The fallback remains **Ecology and Evolution** if the systematic synthesis is strong but the geography axis is not analytically consequential.

The older frozen audit remains a source-recovery and claim-boundary result; it is not retroactively relabelled as a systematic-review denominator. Its **existing-study integration plus shared-cue framework** fork remains preserved as provenance. If the retained strict linked set is sparse, the legacy **paired-channel measurement gap** remains a valid paper-level outcome rather than a reason to relax the admission gate. **No pooled effect is authorized** until systematic screening identifies compatible linked experiments and their outcomes/scales pass an explicit commensurability gate.

## Frozen systematic denominator

V1 is retained only as failed-method provenance:

```text
OpenAlex + broad Crossref discovery
raw query/database hits: 5,406
deduplicated records:    2,684
25/28 query×database combinations hit the 200-record cap
status: PRISMA_IDENTIFICATION_TRUNCATED
```

The first complete V2 OpenAlex run is now the immutable screening cohort:

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

The permanent files are under `empirical/prisma/frozen_v2/`. Record IDs and the screening denominator are not regenerated from the live bibliographic index.

A later identical registered OpenAlex query returned `10,969 -> 2,108 -> 869`. The one added live candidate is monitoring information only. The live index therefore has status `LIVE_INDEX_DRIFT_DETECTED`; it does **not** change the 868-record PRISMA denominator or renumber prior decisions.

## Current screening state

Formal decisions are cumulative sparse overlays. V1 preserves the first 40 source-verified title/abstract decisions; V2 adds source-verified full-text adjudication and three already-audited evolutionary sources that were also present inside the frozen 868-record cohort.

Current registered state:

```text
identified frozen cohort:        868
title/abstract screened:          43
retained for full text:           31
title/abstract excluded:          12
unscreened:                      825

full-text eligible:               31
primary studies included:         15
full-text excluded:                3
full-text undecided:              13

STRICT_LINKED_EXPERIMENT:           1
DIRECTIONAL_OR_NEAR_PASS:          14
EVOLUTIONARY_OUTCOME:               5
```

Full-text exclusions currently comprise two secondary syntheses (`FT_REVIEW_ONLY_NO_PRIMARY_ROLE`) and one post-floral ant/PPN study with no declared floral A coordinate (`FT_NO_DECLARED_FLORAL_COORDINATE`). Secondary evidence remains available to the source registry but is not double-counted as primary included studies.

The strict linked result remains **Theis & Adler 2012 only**. None of the additional full-text decisions relaxes the gate:

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common reproductive outcome
```

## Geography / JBI gate

The systematic lane now contains multiple direct geographic/interactor contrasts rather than one isolated anchor. Six included primary records currently pass the fail-closed positive geography and receiver/interactor-regime counters:

```text
SCHPRISMA-000008  Erysimum: eight-population selection mosaic
SCHPRISMA-000032  Barbarea: 14-site agricultural landscape gradient
SCHPRISMA-000066  Primula secundiflora: six-population visitor mosaic
SCHPRISMA-000172  Biscutella: lowland/highland crab-spider regime contrast
SCHPRISMA-000523  Primula farinosa: 69-population selection/evolution mosaic
SCHPRISMA-000710  Gentiana lutea: 12-population color/selection gradient
```

This is enough to reject the earlier concern that the JBI axis rests on a single case. It is **not** enough to call the JBI gate closed: 825 records remain unscreened, 13 retained reports remain undecided at full text, independence/duplicate-report coding is incomplete, and no pooled geography-by-cue-overlap analysis is authorized yet.

`NO_*`, `NOT_REPORTED`, single-site and explicitly non-geographic experimental-setting labels are not counted as positive geography. A map of study locations cannot rescue a failed geography gate.

## High-value results already recovered

- *Erysimum mediohispanicum*: pollinator assemblages, ungulate damage and floral-trait selection vary among eight populations, with divergent selection for some corolla traits.
- *Barbarea vulgaris*: across a 14-site Finger Lakes agricultural gradient, landscape composition changes herbivory and indirectly changes floral display, pollinator contribution and seed set; resident local adaptation remains an inference.
- *Primula farinosa*: 69 populations plus replicated pollinator/grazer experiments and an eight-year manipulation connect spatially variable selection to rapid genetic morph-frequency change.
- *Gentiana lutea*: 12 populations show geographic flower-color variation, variation in pollinator communities and spatially variable selective pressures; phenotypic local adaptation is supported, but genetic causality of the color differentiation is not established by that study.
- *Petunia*: component-specific transgenic perturbations directly recover host-location versus florivore-deterrence functions within a floral scent bouquet, supporting partial modularity but not a same-component pollinator-preservation test.
- *Ficus*: remains the strongest `COMPOSITE_NEAR_L4` historical bridge; exact same-code NPFW behavior remains zero and strict L4 remains `NOT_EVALUABLE`.

## Paper spine

| Paper component | Material in hand | Current use | Missing gate |
|---|---|---|---|
| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining screening |
| Estimands | `M_A`, `G_A`, `S_A = M_A - G_A`, direct cost separate | Keeps SCH distinct from BITA `Delta_AD W` | Effect-size scale and outcome compatibility rules |
| Evolutionary outcomes | **12-source primary audit** plus systematic V2 additions | Compromise, partial modularity, population change and geographic selection mosaics are now represented | Finish systematic outcome coding; **lineage branching untested** |
| Frozen coverage audit | BITA-derived route candidates and source-adjudicated anchors | Establishes existence and exposes near-pass classes. **Do not insert them into the frozen four-field coverage count** without a separate admission pass. | Not a prevalence denominator |
| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator; live OpenAlex only monitors index drift | Screen remaining 825 |
| Formal screening | 43 TA decisions; 15 primary full-text includes | Builds systematic evidence lanes without machine inclusion | 13 retained full texts undecided; 825 TA unscreened |
| Strict experiment | Theis & Adler 2012 | One strict linked directional anchor | Raw uncertainty-bearing focal A effect unavailable |
| Geography | 6 positive included geographic/interactor records | JBI axis is now empirically plausible across multiple systems | Complete screening and define analyzable cross-study geography question |
| Ficus history | fixed 32-species scaffold + same-code gate | Bounded historical bridge | Same-code NPFW assays, then state reconstruction |

## Planned article structure

1. Introduce geographic turnover in biotic audiences as a potential constraint on shared versus separable floral cues.
2. Define `M_A`, `G_A`, `S_A` and the direct-cost boundary.
3. Derive predictions for shared and private cues.
4. Distinguish compromise, polymorphism maintenance, population differentiation/change, partial modularization and historical branching.
5. Report the frozen PRISMA identification/screening flow and evidence lanes.
6. Analyze geography/receiver-regime contrasts only after independence and commensurability coding.
7. Use *Ficus* as the bounded historical bridge, not as the whole source universe.
8. Report the information asymmetry between detecting interception and supporting behavioral privacy.
9. End with the minimum same-code experiment and historical-state reconstruction required for L4.

## Figure and table recovery plan

| Item | Purpose | Source state |
|---|---|---|
| Figure 1 | Shared-cue versus private-cue mechanism | Concept fixed |
| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator and live screening counts available |
| Figure 3 | Geographic receiver-regime synthesis | Six positive coded primary records already; final form waits for completed screening |
| Figure 4 | *Ficus* same-code historical bridge | Core data/matrix fixed |
| Table 1 | Systematic study-level decisions and blockers | 43 screened records, 15 primary includes |
| Table 2 | Evidence-role registry and prohibited uses | Existing registry + systematic update in progress |
| Table 3 | Evolutionary-outcome ledger | Primary audit + systematic additions in progress |

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
- **No pooled effect is authorized** by screening completion alone; outcome scale, independence and commensurability must pass separately.
- JBI is promoted only after systematic completion and an analytically consequential geography/receiver-regime result; otherwise Ecology and Evolution remains the fallback.
