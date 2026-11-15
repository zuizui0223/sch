# SCH 2017 orchid original individual-level data: source access boundary (2026-11-15)

## Current state

For Trunschke, Sletvold & Ågren (2017), *New Phytologist*, article DOI **10.1111/nph.14479**, source Dryad DOI **10.5061/dryad.28n72**, the source metadata is publicly accessible, but the original individual-plant workbook and its dictionary were **not downloaded** in the authenticated-free GitHub Actions runtime.

The public Dryad API returned:
- Dataset metadata HTTP **200** (dataset id **2948**).
- Published version list HTTP **200**, version id **2963**.
- Version-file listing HTTP **200**, exactly **two** source files.

| Authentic archived file | Dryad file ID | Metadata bytes | Metadata MD5 |
|---|---:|---:|---|
| Trunschke et al._NewPhytologist_2017_strength of selection_DRYAD_raw data.xls | **19534** | **772608** | **2a0429adade12ddce60ba9e46500f4a9** |
| README_for_Trunschke et al._NewPhytologist_2017_strength of selection_DRYAD_raw data.docx | **19535** | **103526** | **e773115ab4eaab2b75c83f6ffb260239** |

**Actual public file-transfer outcomes for BOTH IDs:**

- Dryad `/api/v2/files/{id}/download`: HTTP **401**
- Dryad `/downloads/file_stream/{id}`: HTTP **403**
- Dryad `/stash/downloads/file_stream/{id}`: HTTP **403**

These codes were returned after source metadata was verified and the correct HAL version and file links were parsed; the issue is not an invented file identity or an empty search. The result is an **access restriction for unauthenticated machine downloads in this execution environment**, *not* evidence that the original research data have vanished or that a person cannot download through the publisher site.

**Reproducible actual execution:** GitHub Actions workflow `SCH orchid original Dryad 2017 source-access probe`, run [#43673625885](https://github.com/zuizui0223/sch/actions/runs/43673625885), with original source access receipt saved as artifact **14145328001** (ZIP sha256 `67bedf80586f23ebc1586e3de85e77f8b59fe4f8ac0ea13ff4b511086aa7abf7`). Public metadata and download HTTP codes are all source-process receipts. The ZIP does **not contain** the 2017 raw workbook or plant observations.

## Why this affects biological inference

The previously merged independent paper audit [PR #243](https://github.com/zuizui0223/sch/pull/243) records **published author ANCOVA** for **12 orchid species × five trait axes**:
- PL versus absolute pollinator-mediated selection: **F=18.79, P<0.001**.
- PL versus absolute net selection: **F=6.374, P=0.015**.
- PL versus absolute nonpollinator-mediated selection: **F=0.0045, P=0.947**.

Those numbers remain authentic *published source analyses*, but no independent re-estimation of original plant-level gradients has occurred. Without the authentic XLS and dictionary, neither an original 12-species unit permutation of PL values, a leave-one-species-out jackknife, a species-block hierarchical variance model, nor a numerical contrast between the 2014 *within-species* and 2017 *between-species* scales can be reported as completed. Five traits within one species are correlated measurements, not five independent species or study replicates.

A testable, but not yet tested, hypothesis is that PL acts as an opportunity constraint on trait-mediated selection between species while trait-to-pollen-success sensitivity dominates across population years within species. This is a prospective research question, not a recovered cross-scale interaction.

## Execution contract

- Keep the source checksum/size/name and study DOI pinned. Never replace the original with a different XLS selected by a keyword alone.
- Do not retry the same 401/403 unauthenticated download endpoints indefinitely; stop until a **legitimate user-supplied original binary**, permissioned download, or independently published **checksum-identical** mirror becomes accessible.
- When authentic raw bytes become available, verify their MD5 against the dataset metadata above **before** opening spreadsheet sheets or fitting a model.
- Check the source dictionary, number of species, treatment labels, treatment-wise standardization, fitness outcome and missingness first.
- Run species-level label permutation / leave-one-species-out robustness only after source row-grain qualification; keep a separate within-species cohort estimator for the 2014 population-year data.
- No claim of ecological universality, cross-scale interaction, causal trait optimum, or SCH compromise loss **L** is unlocked by metadata access alone.

Status: **RAW_ORCHID_2017_AUTHENTIC_METADATA_IDENTIFIED; ORIGINAL_XLS_NOT_ACQUIRED; RAW_COMPARATIVE_ANALYSIS_BLOCKED**. The source-only positive study association and NPH Viewpoint are unchanged.
