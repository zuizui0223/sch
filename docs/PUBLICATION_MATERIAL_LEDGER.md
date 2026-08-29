# Publication material ledger

## Editorial boundary

This ledger organizes the one-trait shared-cue paper without importing BITA's two-trait estimand. The current first-choice target is **Journal of Biogeography, Review & Synthesis**, conditional on the systematic-review and biogeographic gates in `docs/SCH_JBI_SUBMISSION_CONTRACT_V1.md`. The fallback remains **Ecology and Evolution** if the systematic synthesis is strong but the geography axis is not analytically consequential.

The older frozen audit remains a source-recovery and claim-boundary result; it is not retroactively relabelled as a systematic-review denominator. Its **existing-study integration plus shared-cue framework** fork remains preserved as provenance, while PRISMA V2 now supplies the independent systematic denominator needed for publication claims. If the retained strict linked set is sparse, the legacy **paired-channel measurement gap** remains a valid paper-level outcome rather than a reason to relax the admission gate. **No pooled effect is authorized** until systematic screening identifies compatible linked experiments and their outcomes/scales pass an explicit commensurability gate.

## Current systematic-review state

The registered discovery work separates a rejected V1 implementation from the valid V2 identification denominator.

```text
V1: OpenAlex + broad Crossref discovery
raw query/database hits: 5,406
deduplicated records:    2,684
25/28 query×database combinations hit the 200-record cap
status: PRISMA_IDENTIFICATION_TRUNCATED
use: method/access provenance only

V2: OpenAlex-only complete retrieval + predeclared title/abstract concept filter
raw OpenAlex records retrieved: 10,953
concept-pass query hits:        2,107
deduplicated candidates:          868
truncated queries:                  0
known frozen anchors recovered:   8/8
status: PRISMA_V2_IDENTIFICATION_COMPLETE
```

The valid title/abstract screening denominator is **868**. It is partitioned deterministically into nine batches (100×8 + 68).

Screening has now started conservatively from the eight frozen studies that were already source-adjudicated before the systematic lane was built. Those records are promoted only to `RETAIN_FULLTEXT`; they are **not** automatically included at full-text stage.

Current audited PRISMA state:

```text
identified after deduplication: 868
title/abstract screened:          8
retained for full text:           8
title/abstract excluded:          0
unscreened:                     860
reports assessed full text:       0
studies included:                 0
status: TITLE_ABSTRACT_IN_PROGRESS
```

The formal decisions live in the sparse version-controlled overlay:

`empirical/prisma/SCH_PRISMA_V2_SCREENING_DECISIONS_V1.csv`

Each populated formal record requires a declared `decision_source`. The generated OpenAlex candidate universe remains independent of those decisions and is regenerated before the overlay is applied and re-audited.

The Batch 1 abstract-free assistance packet currently partitions its 100 records as:

```text
KNOWN_ANCHOR:        2
HIGH_TITLE_TRIPLE:   3
HIGH_TITLE_PAIR:    29
MEDIUM_TITLE_ONE:   35
ABSTRACT_ONLY:      31
```

The first high-information human review queue is therefore 34 records (2 anchors + 3 title-triple + 29 title-pair). The two anchors are already among the eight prior-adjudication retains; the other 32 high-priority records remain formally `UNSCREENED`. Machine priority is an ordering aid only and cannot populate PRISMA decisions.

JBI readiness remains fail-closed until title/abstract screening, full-text screening, evidence-lane coding and geography/receiver-assemblage coding are complete.

## Paper spine

| Paper component | Material in hand | Current use | Missing gate |
|---|---|---|---|
| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through systematic screening |
| Estimands | `M_A`, `G_A`, `S_A = M_A - G_A`, with direct cost separate | Keeps the one-trait target distinct from `Delta_AD W` | Effect-size scale and outcome compatibility rules for retained studies |
| Mechanism predictions | four predeclared predictions in the framework manuscript | Links cue overlap to response concordance, net-fitness slope and antagonist-removal effects | Prospective coding fields and analysis plan |
| Evolutionary outcome hypotheses | **12-source primary audit** plus fail-closed outcome ledger | Recovers compromise, polymorphism maintenance, population change and partial decoupling while keeping lineage branching untested | Systematic retained-set update and historical-transition evidence |
| Frozen coverage audit | BITA-derived route candidates and source-adjudicated anchors | Establishes existence and exposes near-pass classes. **Do not insert them into the frozen four-field coverage count** without a separate admission pass. | Not a prevalence denominator; superseded for systematic denominator by PRISMA V2 |
| PRISMA V2 identification | 10,953 retrieved → 2,107 concept-pass hits → 868 deduplicated candidates | Complete automated identification coordinate with 8/8 known-anchor recovery | Finish title/abstract screening of remaining 860 |
| Formal screening | 8 prior-adjudicated anchors retained for full text; 0 excluded; 0 included | Tests the real decision-overlay and PRISMA counting path without allowing machine triage to decide inclusion | Human adjudication of remaining 860; full-text screening of retained records |
| Batch 1 triage | 100 records; 34 in anchor/title-triple/title-pair queue | Orders review while storing no abstract text and writing no formal decisions | Human title/abstract decisions for 32 non-anchor high-priority records |
| Strict experimental anchor | Theis & Adler 2012 | A manipulated, both consumer responses measured, seed-production direction reported | Focal raw table and uncertainty-bearing effect unavailable |
| Ficus historical bridge | fixed 32-species scent scaffold + same-code gap ledger | Strongest `COMPOSITE_NEAR_L4` radiation; exact same-code NPFW behavior remains 0 | Three priority same-code experiments, then state reconstruction |
| Same-code measurement contract | source-anchored assays, power planner, trial CSV and cluster-bootstrap classifier | Makes interception/avoidance/privacy prospectively decidable | New field data |
| JBI geography gate | protocol fields frozen | Tests whether geography/receiver turnover is analytically consequential rather than decorative | Full-text geography coding and retained-set analysis |
| Research fork | systematic retained set + geography evidence | JBI if systematic and geographic gates pass; Ecology and Evolution if geography is weak; the legacy **existing-study integration plus shared-cue framework** and **paired-channel measurement gap** routes remain provenance | Finish screening before journal promotion |

## Planned article structure

1. Introduce geographic turnover in biotic audiences as a potential constraint on shared versus separable floral cues, while keeping geography conceptual until the retained evidence supports analysis.
2. Define `M_A`, `G_A`, `S_A` and the direct-cost boundary.
3. Derive predictions for shared and private cues.
4. Distinguish compromise maintenance, directional endpoints, polymorphism maintenance, population differentiation, lineage branching and cue modularization.
5. Report the PRISMA identification/screening flow and retained systematic evidence lanes.
6. Test the geography/receiver-assemblage gate only where replicated spatial contrasts permit it.
7. Use *Ficus* as the bounded historical bridge, not as the whole source universe.
8. Report the information asymmetry between detecting interception and supporting behavioral privacy.
9. End with the minimum same-code field design and historical-state reconstruction required for L4.

## Figure and table recovery plan

| Item | Purpose | Source state |
|---|---|---|
| Figure 1 | Shared-cue versus private-cue mechanism and predicted `M_A`/`G_A` coupling | Concept fixed; artwork not yet generated |
| Figure 2 | PRISMA identification/screening flow plus strict/near-pass evidence lanes | Identification fixed at 868; live screening counts now generated from decision overlay |
| Figure 3 | Geographic/receiver-assemblage synthesis if JBI Gate J5 passes; otherwise measurement-gap map | Conditional on completed full-text geography coding |
| Figure 4 | *Ficus* same-code historical bridge and missing receiver intersection | Core data/matrix fixed |
| Table 1 | Systematic study-level screening/admission decisions and blockers | Screening active: 8 retained for full text, 860 unscreened |
| Table 2 | Evidence-role registry with admitted and prohibited uses | Existing anchor registry + systematic update pending |
| Table 3 | Evolutionary-outcome hypothesis ledger | Primary audit fixed; systematic update pending |

A geography figure is not mandatory merely because JBI is the first-choice target. If geography is not analytically consequential after screening, the journal gate changes rather than forcing a decorative map.

## Admission and stop rules

- The strict coverage gate remains: `A manipulated + pollinator response measured + antagonist response measured + common reproductive outcome`.
- `D`, `A x D`, selective consumer intervention and a 16-cell design remain outside the initial SCH coverage requirement.
- Lower evidence layers may be retained with explicit claim ceilings but are never counted as strict linked experiments.
- `FAIL`, `NOT_EVALUABLE`, inaccessible raw data, split outcomes and observational A are preserved as results.
- Total plant fitness under `A` does not by itself allocate `M_A` and `G_A`.
- The V2 868 records are **identified candidates**, not included studies.
- `UNSCREENED` is never interpreted as exclusion.
- Machine triage may order review but cannot populate `screen_title_abstract`, `screen_fulltext`, exclusion reasons or evidence lanes.
- Uncertainty at title/abstract screening is resolved toward full-text retention.
- Geography missing from the source is `NOT_REPORTED`; it is never inferred from author affiliation.
- Broad evidence hunting stops only when the registered search/screening universe and any explicitly declared citation-chasing lane are exhausted.
- **No pooled effect is authorized** by screening completion alone; outcome scale, independence and commensurability must pass separately.
- JBI is promoted only if systematic-review completion and the nontrivial geography/receiver-assemblage gate both pass.
