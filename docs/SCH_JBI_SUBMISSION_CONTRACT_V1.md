# SCH Journal of Biogeography submission contract v1

## Decision

The first submission target is **Journal of Biogeography (JBI)**. The safest current article category is **Review & Synthesis**, not Research Article, because SCH combines a conceptual framework, a source-adjudicated evidence audit, and original reclassification/analysis rather than a single new geographical field dataset.

The fallback remains **Ecology and Evolution** if the systematic expansion does not recover a defensible biogeographic axis.

This document is a submission gate, not a claim that the current manuscript is already JBI-ready.

## Current journal requirements checked 2026-08-29

The current JBI author guidance permits theoretical synthesis/review papers to include original analysis, allows Review & Synthesis papers up to about 10,000 words unless extra length is justified, uses double-anonymous peer review, requires a Data Accessibility Statement and open archiving of data supporting the results, and requires 6–10 keywords. The journal explicitly requires a PRISMA flow diagram for Review & Synthesis papers and other material containing a literature-review section.

JBI also requires a clearly biogeographic contribution: papers should sit at the intersection of biology and geography and articulate theoretical foundations and conceptual advance. A floral-signal review without a geographical/historical axis is therefore not automatically in scope.

## Current SCH fit

Positive fit:

- a general theoretical mechanism: cue overlap constrains whether attraction can evolve independently of antagonist exposure;
- explicit evolutionary outcomes from compromise to population change, modularization and historical transition;
- a phylogenetic/historical *Ficus* candidate radiation;
- quantitative evidence-gap and experimental-identification results;
- original analysis components are allowed inside a JBI Synthesis.

Current blockers:

1. the existing frozen audit explicitly is **not** a systematic-review result;
2. the current literature universe is partly inherited from BITA and partly target-expanded, so it cannot be presented as prevalence;
3. no PRISMA identification/screening flow exists yet;
4. geographical context is not coded consistently across the evidence ledger;
5. the current same-code *Ficus* result is a historical/mechanistic bridge, not yet a reconstructed geographic evolutionary transition.

## JBI promotion gates

SCH may be described as JBI-ready only after all of the following are closed.

### Gate J1 — systematic identification

Run the predeclared bibliographic search independently of the frozen BITA-derived audit. Preserve raw hit counts by database/query, deduplicate transparently, and freeze the identified candidate universe.

### Gate J2 — PRISMA screening

Every identified record receives a title/abstract decision and, if retained, a full-text decision with a predeclared exclusion reason. The PRISMA counts must be generated mechanically from that ledger rather than reconstructed after manuscript writing.

### Gate J3 — unchanged scientific admission fields

The systematic expansion must not relax the existing core gate simply to increase yield:

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common plant reproductive outcome
```

Lower evidence layers may be retained in explicitly separate lanes, but they may not be counted as strict linked experiments.

### Gate J4 — biogeographic context

For every retained study, code at least:

```text
study_region
country_or_ocean_basin
spatial_grain
spatial_extent
single_site_vs_multisite
geographic_contrast
receiver_assemblage_contrast
island_mainland_or_other_biogeographic_context
historical_or_phylogenetic_context
```

Missing geography is `NOT_REPORTED`, not inferred from author affiliation.

### Gate J5 — geography is analytically consequential

Before choosing JBI over the fallback, the expanded evidence must support at least one nontrivial biogeographic synthesis question, for example:

- whether cue-overlap states or conflict outcomes differ across replicated geographic receiver assemblages;
- whether spatial turnover in pollinators/antagonists predicts changes in the direction or strength of shared-cue conflict;
- whether historical transitions in cue architecture can be linked to geographic/historical changes in receiver regimes.

A map of study locations by itself does not satisfy this gate.

### Gate J6 — reproducible open materials

Search ledger, screening decisions, code, derived tables and figure inputs must be archive-ready. Publisher PDFs and copyrighted full text are never stored in the repository.

## Fail-closed journal decision

```text
J1–J6 closed
    -> JBI Review & Synthesis

systematic/evolutionary synthesis strong but J4/J5 weak
    -> Ecology and Evolution fallback

J1/J2 incomplete
    -> NOT_SUBMISSION_READY; do not present source counts as systematic prevalence
```

This preserves the first-choice JBI strategy without forcing a geographical story that the evidence cannot support.

## Manuscript implications

### Main text

Keep:
- cue-overlap theory and estimands;
- evolutionary-outcome ladder;
- systematic evidence result after J1/J2;
- biogeographic synthesis only if J4/J5 pass;
- bounded *Ficus* historical bridge;
- the key information-asymmetry result that privacy requires equivalence evidence, not nonsignificance.

### Methods

Add:
- bibliographic databases and exact query version;
- search date;
- deduplication algorithm;
- screening/exclusion rules;
- geography coding rules;
- source-role and claim-ceiling rules;
- same-code prospective analysis contract when used as a generated research agenda.

### Supporting information

Place:
- PRISMA flow;
- complete search-query registry;
- identified-record ledger;
- title/abstract and full-text exclusion ledger;
- full 32-species *Ficus* matrix;
- detailed same-code power and assay protocol;
- reproducibility receipts.

## Title/abstract discipline

The title must describe the general biogeographic problem rather than advertise *Ficus* as the whole paper. *Ficus* is currently the strongest historical bridge/case study, not the total source universe.

The abstract should make the sequence explicit:

```text
geographic turnover in biotic audiences
-> shared versus separable sensory coordinates
-> constraints on floral-signal evolution
-> systematic evidence state
-> missing matched historical transition
```

If the systematic expansion does not support the first arrow empirically, that wording must remain conceptual and the JBI gate should be reconsidered rather than overstated.
