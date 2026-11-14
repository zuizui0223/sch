# SCH: original experimental plant-functional-trait macro/meta reanalysis — V1

## Tested claim, independent of the literature-review narrative

**Question:** Does experimentally changing the biotic environment, compared with experimentally changing the abiotic environment, more often reverse the directional selection gradient on a given plant functional trait?

This is a *new quantitative reanalysis* of the original, previously published **Caruso, Maherali & Martin (2020)** plant functional-trait selection meta database (article doi: **10.1086/706199**; primary publicly archived data doi: **10.5061/dryad.sn02v6x0q**). It is **not newly collected field data**, not a full world-flora trait-frequency estimate, and not a causal identification of SCH's function-optimum conflict loss L.

The relevant original dataset (archived at https://zenodo.org/records/5000217) contains **572 un-duplicated experimental selection-coefficient records from 43 original papers and 46 reported species**. Two other archive objects are explicitly kept separate: 815 observational records and a **1,014-row, intentionally duplicated author analysis workbook**. Those extra rows are *not* added to the independent experiment count. The experimental master original file MD5 is **7f680c344c0a418a3d8742649de24d52**.

The reproducible pipeline is:

1. scripts/ingest_sch_plant_functional_selection_2020_raw.py — source MD5-verified original workbook acquisition
2. scripts/audit_sch_plant_functional_meta_grain.py — original 26-column variable dictionary, 43 publications, agent names, numeric SE and pairing audit
3. scripts/analyze_sch_plant_functional_selection_macro.py — source-adjudicated matched treatment-pair quantitative analysis with entire-PAPER-level replication
4. data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv — **all 137 paired quantitative source records**, including source study and exact treatment-row IDs
5. data/SCH_2020_FUNCTIONAL_META_EXPERIMENTAL_READOUT_V1.json — all numerical results, full agent/context diagnostics and source-conditional inference receipts
6. scripts/audit_sch_2020_meta_direct_source_interactions.py — primary-publication validation of the strongest numerical contrasts

## Genuine quantitative sample

The unduplicated data have 228 possible same-study/year/species/population/trait/sex/fitness groups; of these, **172** have exactly two different treatments. Of the 172, **35 lack a complete source linear beta+SE pair**. The retained **137 complete pairs** use 274 unique originally compiled gradient rows representing **26 original papers and 34 species**. These counts are source-tested, not extrapolated.

A pair is accepted ONLY when the same Paper ID, source year, species, source population, trait, sex, fitness measure, original agent and experimental setting are retained across two different treatment codes with different published treatment labels. This excludes arbitrary comparisons of unrelated outcomes. Trait classes follow the original dictionary: PH phenology, PY physiology, S plant size, MO leaf morphology, CH leaf chemistry.

### Main comparison, never 137 independent studies

| Treatment-agent category | Original matched pairs | Independent original papers | Point-estimate beta sign changes | Two individually SE-supported opposite beta signs |
|---|---:|---:|---:|---:|
| BIOTIC (pollinators, herbivores, competitors, etc.) | **75** | **17** | **21** | **0** |
| ABIOTIC (soil moisture, temperature, light, etc.) | **58** | **8** | **20** | **0** |
| MIXED / unresolved agent coding | **4** | **1** | **0** | **0** |
| **Total** | **137** | **26** | **41** | **0** |

**41/137** are estimated sign crossings, **not 41 biologically established directional reversals**. Zero of 137 have source-SE-supported individually nonzero slopes of the opposite direction in both treatment arms at nominal two-sided 95% normal-Wald thresholds. This is an evidence classification, not a conclusion that no ecological reversal exists.

Among the 25 publications with an exclusively biotic or exclusively abiotic manipulated driver, the mean of each **paper's** within-paper sign-flip fraction is **0.2132** for biotic and **0.3142** for abiotic. Difference (biotic − abiotic) **−0.1010**, two-sided 9,999-study-label permutation P=**0.3996**. Paper-bootstrap descriptive 95% interval **[−0.322,+0.117]**. This exploratory label-permutation relies on a hypothetical exchangeability of already-published studies; the agent types were **not randomly assigned among papers**, so this is not a causal comparison nor a probability-sampled meta-analytic frequency.

### Design-confounding and fitness sensitivity

The biotic and abiotic strata have substantially different study compositions. **37 of 75 biotic pairs** were collected under a source-defined in-situ natural population setting; **zero of 58 abiotic pairs** have that setting. A direct difference in sign-change prevalence is therefore confounded with source setting and probably trait/study choice.

Restricted checks on independent papers:

- **Indoor or outdoor semi-controlled only (A/B):** 96 source pairs across 17 papers (biotic 38 vs abiotic 58), paper-level contrast **−0.1568, permutation P=0.2044**, bootstrap interval approximately [−0.378,+0.061].
- **Fecundity fitness component only (F):** 94 pairs across 20 papers, paper-level contrast **−0.1313, P=0.3842**, bootstrap interval [−0.393,+0.139].
- **Indoor setting only (A):** 51 eligible pairs, but only **one** source biotic paper versus six abiotic papers; fail closed as **NOT MODELABLE** rather than reporting a misleading moderator P value.

No case provides statistical support for "biotic manipulations reverse selection more often than abiotic manipulations". The direction of descriptive differences is actually the opposite of that prediction, but inference remains too weak and source-design confounded for a general sign-of-effect claim.

## Strong gradient changes without confirmed sign reversals

Applying a **conditional** source-marginal-beta-SE normal-Wald difference reconstruction to each of the 137 complete pairs, using the Cauchy–Schwarz upper bound **SE(β₂−β₁) ≤ SE₁+SE₂**, gives 3 calculated changes outside a two-sided 137-comparison Bonferroni threshold (critical z approximately **3.5642**), all drawn from **two papers**. None is a point sign reversal.

| Published source | Treatment labels | Trait, original fitness endpoint | Original beta ± SE | Conditional reconstructed Bonferroni P upper | Stored decimal sensitivity |
|---|---|---|---|---:|---|
| Beans & Roach 2015, *Impatiens capensis* | invasive competitor absent → present | Early growth rate; fruit number | +0.090 ±.020 → +0.003 ±.002 | 0.0105 | **Fails** |
| Beans & Roach 2015, *I. capensis* | invasive competitor absent → present | Total internode number; fruit number | +0.140 ±.010 → +0.360 ±.020 | 3.08×10⁻¹¹ | Passes |
| Stinchcombe *et al.* 2002, *Ipomoea hederacea* | source-coded herbivores absent → present | Total leaf area; seed number | +0.790 ±.030 → +0.044 ±.050 | 1.52×10⁻¹⁸ | Passes |

For the compiled *Ipomoea* pair, the arithmetic coefficient contrast is **Δβ = 0.044 − 0.790 = −0.746**. Its primary fitted interaction significance has not been independently recovered.

**These three reconstructed P values are NOT all directly validated original-study interaction P values.** The stored-decimal check perturbs the original archived Excel coefficients by half their last visible decimal unit; it is not proof of complete original paper printing precision or correct reported interaction SE.

### High-priority primary-source adjudication

The original Beans & Roach (2015) experimental paper (**doi:10.3732/ajb.1400355**, *American Journal of Botany* 102:217–224) reports, in its **Table 2 greenhouse experiment**, a directly fitted treatment × trait test of **F=4.38, P=0.04** for early growth and **F=82.74, P<0.0001** for total internodes. The reconstructed source-marginal-SE method gives a vastly smaller P for the early-growth contrast; this is a **primary-study model/uncertainty mismatch**, not a validation of a superior new test. Direct fitted source P=.04 does NOT survive a 137-test Bonferroni benchmark. The original internode interaction **P<0.0001** DOES survive that benchmark, because 0.0001×137=0.0137 <0.05.

The original compiled Stinchcombe *et al.* (2002) entry is precisely **The American Naturalist 160:511–523**, doi: **10.1086/342069**, *Testing for Environmentally Induced Bias in Phenotypic Estimates of Natural Selection: Theory and Practice*. Its whole-paper scientific result explicitly demonstrates that environmental covariance can bias a subset of phenotypic selection gradients. **This does not prove that the particular leaf-area coefficient here was biased**, but means the original study must be re-examined before the pair is promoted as a causal herbivore-mediated selection effect or as a validated direct primary interaction. No source-fitted interaction P has been independently verified for this specific pair.

Consequently, the source-compiled screening supplies **three strong conditional reconstructed contrast candidates**, two robust to a stored-decimal sensitivity. But **only ONE** of those three has, as yet, a independently verified original-author interaction that survives the 137-comparison criterion: *Impatiens capensis* total internode number. The rest are **nominal or unresolved** under primary-source adjudication. This is a crucial inferential ceiling for the manuscript.

## Ecological interpretation and publication boundary

The positive supported observation is deliberately narrow: *Impatiens* source selection for more internodes becomes stronger under invasive-competitor exposure without changing sign, with an original direct interaction test robust to a 137-hypothesis familywise threshold. Across independent papers, however, **the biotic-versus-abiotic frequency hypothesis is not supported**, and none of the 41 point sign reversals is independently supported in both treatment slopes.

The full meta dataset can therefore support an original **methodological and comparative ecological analysis** of *selection responses versus sign changes*, but it does not yet establish a universal trade-off mechanism, a multi-species effect-size pooled mean, an ecological prevalence estimate, pure functional optima, or the SCH compromise loss **L**. In particular, the compiled experimental meta is not a sample of every plant species on Earth and the number of trait pairs is not the number of independent biological replications.

The next substantive question is no longer to add more source examples blindly; it is to recover the **original author-fitted interaction contrasts and variance structures for a common, preregistered manipulation/fitness family**. Only then would a genuinely multi-study primary-test-based random-effects model be justified, including publication bias, trait/study clustering and heterogeneity diagnostics.

## Exact reproduction

Original source: doi:10.5061/dryad.sn02v6x0q; archive https://zenodo.org/records/5000217.
Original paper: doi:10.1086/706199.

Run from the SCH repository root with a network-enabled Python environment:

    python scripts/ingest_sch_plant_functional_selection_2020_raw.py --outdir artifacts/plant_functional_selection_original
    python scripts/audit_sch_plant_functional_meta_grain.py --outdir artifacts/plant_functional_selection_original
    python -m scripts.analyze_sch_plant_functional_selection_macro --outdir artifacts/plant_functional_selection_original
    python -m scripts.audit_sch_2020_meta_direct_source_interactions

Primary workbooks and all matched results are persisted in the rerunnable source GitHub Action \`.github/workflows/sch_plant_functional_selection_2020.yml\`; complete 137-row derived ledger, source-metadata receipt, and externally validated direct original test metadata are permanently versioned in \`data/\`. The source archive's intentionally duplicated 1,014-row workbook and 815 observational records are kept separate.

**Status:** ORIGINAL_FUNCTIONAL_META_REANALYSIS_COMPLETE; 26 independent papers; 137 matched original pairs; null biotic–abiotic difference; 41 unconfirmed sign crossings; 1 directly independently verified Bonferroni-compatible strong selection-magnitude change; no SCH loss L; not a causal field replication; not prevalence.
