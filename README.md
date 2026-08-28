# Shared Cue Hypothesis (SCH)

SCH is the one-trait companion project separated from [BITA](https://github.com/zuizui0223/bita). BITA asks how an attraction trait `A` and an antagonist-reducing trait `D` jointly shape fitness and whether the resulting interaction can be allocated among mechanisms. SCH asks the prior, simpler question: what happens when pollinators and antagonists track the same floral cue?

## Scientific target

For one predeclared attraction/display contrast,

```text
M_A = change in pollinator-mediated benefit
G_A = change in antagonist-mediated cost
S_A = M_A - G_A
```

If direct physiological or construction costs of changing `A` matter, they are retained separately rather than silently absorbed into `S_A`.

The central mechanism is **cue overlap**:

- shared cues couple `M_A` and `G_A`, constraining signal exaggeration;
- private or separable cues allow pollinator attraction to change with less antagonist exposure;
- the predeclared prediction is that greater cue sharing shifts the display-intensity/net-fitness relationship toward a flatter or more negative slope.

This is not the BITA two-trait estimand `Delta_AD W`, and SCH must never be cited as evidence that BITA tested the original one-trait hypothesis.

## Current evidence gate

The first coverage screen asks only whether the same linked experiment contains:

```text
A manipulated
+ pollinator response measured
+ antagonist response measured
+ common plant reproductive outcome
```

It does **not** require `D`, an `A x D` interaction, a selective consumer intervention, or the BITA 16-cell design. Passing this gate establishes coverage existence, not channel point identification or a meta-analytic effect.

The frozen BITA-derived audit currently finds one directional-only pass among 25 route-ledger clusters: Theis & Adler (2012). The earlier 16-system identification matrix contains zero passes, but it was assembled for the BITA two-trait frontier and is not a complete one-trait literature universe.

## Repository map

- `manuscript/MANUSCRIPT_SHARED_CUE_FRAMEWORK.md` — paper concept, estimands, mechanism and predictions
- `empirical/one_trait_shared_cue/` — fail-closed coverage protocol, adjudications and generated readout
- `data/source_exports/` — immutable source tables exported from BITA
- `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv` — roles and claim ceilings for the current evidence spine
- `empirical/one_trait_shared_cue/EVOLUTIONARY_OUTCOME_READOUT_V1.md` — fail-closed separation of compromise, specialization, branching and cue modularization
- `docs/SCH_EVOLUTIONARY_OUTCOME_PRIMARY_SOURCE_AUDIT_V1.md` — primary-source verification of case-level compromise, polymorphism, population change and remaining historical gaps
- `docs/PUBLICATION_MATERIAL_LEDGER.md` — paper sections, figures, evidence roles, missing gates and stop rules
- `docs/CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md` — SCH Chapter 1 to BITA Chapter 2 narrative
- `scripts/build_one_trait_coverage_audit.py` — deterministic audit builder
- `docs/MIGRATION_RECEIPT.md` — BITA-to-SCH ownership boundary and provenance

## Status

This repository establishes a clean research lane; it is not yet a completed systematic review or submission-ready manuscript. The next gate is a predeclared one-trait literature expansion using the same four coverage fields. A large retained set supports an existing-study synthesis plus shared-cue framework. A sparse retained set supports a measurement-gap result and motivates a linked field experiment.
