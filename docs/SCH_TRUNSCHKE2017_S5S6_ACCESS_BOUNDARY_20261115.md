# Trunschke et al. (2017) publisher supplementary S5/S6 access (2026-11-15)

**Source:** Original peer-reviewed article DOI `10.1111/nph.14479`. The Wiley/New Phytologist article advertises original supplement `nph14479-sup-0001-SupInfo.pdf` (about 946 KB), containing **Table S5** (12 orchid species' reproductive performance and population pollen limitation) and **Table S6** (net, hand-supplemented and pollinator-mediated selection gradients for five traits per species). This is the identified primary PDF, **not a recovered document**.

## Actual evidence from independently executed source access

GitHub Actions `SCH Trunschke 2017 publisher supplement S5 S6 access` run [43674775659](https://github.com/zuizui0223/sch/actions/runs/43674775659) ran `scripts/probe_sch_trunschke2017_suppinfo.py` on GitHub's external network. Its archived receipt is artifact **14145955894**, SHA-256 of the artifact ZIP:
`a53062fc736b77d40936a3e4171afac3e3ba8a7b3b1c9136b9c24bd3461148af`.

Observed HTTP status:

| Official publisher request | Result |
|---|---|
| nph.onlinelibrary.wiley.com DOI supplement direct PDF | **403** |
| onlinelibrary.wiley.com DOI supplement direct PDF | **403** |
| nph.onlinelibrary.wiley.com action/downloadSupplement | **403** |
| onlinelibrary.wiley.com action/downloadSupplement | **403** |
| nph.onlinelibrary.wiley.com doi/supinfo landing | **403** |

All five are external-access refusals in the CI environment; they are **not evidence the publisher file is missing or invalid**. The workflow intentionally does **not** authenticate or evade restrictions, and it does not save or redistribute PDF bytes. It rejects HTML/login pages masquerading as a PDF.

**Machine-readable outcome:** `source_pdf_verified=false`, `S5_data_extracted=false`, `S6_data_extracted=false`, `independent_species_level_refit_executed=false`.

## Confirmatory data boundary

1. Published main-article results and previously audited 2017 author ANCOVAs in PR #243 remain source-backed, but are **not newly refitted individual-plant estimates**.
2. Without authentic Table S5/S6 (or checksum-verified original Dryad XLS/README), the 12 independent species' pairwise PL and five-trait selection-gradient values cannot be reconstructed. The 60 trait-axis measurements must **not** be treated as 60 independent species.
3. No source-level leave-one-species-out regression, split rewarding/deceptive within-class slope or cluster-aware SE has been executed. Do not impute values from figures or quote a hypothetical result as empirical.
4. Stop repeatedly retrying these unchanged publisher routes. Reopen access only through a genuinely available publisher/library copy, author-supplied original, or a provenance-verifiable legitimate archive and then validate table units and S5/S6 structure before modeling.

The directly accessible *HTML article*, rather than this inaccessible supplement, may still support **separate, source-numeric checks of claims printed in the main article**. Keep such checks on a separate ledger and distinguish reported from recomputed test P-values.

**Status:** `PUBLISHER_SUPPLEMENT_IDENTIFIED_ACCESS_BLOCKED_403_ALL_TESTED_PATHS; S5_S6_NUMERIC_SOURCE_UNAVAILABLE; ORIGINAL_SPECIES_LEVEL_REANALYSIS_BLOCKED`.
