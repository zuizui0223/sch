# SCH: same-flower original data reuse across three blueberry CSVs — exact source audit and honeybee subgroup (2026-11-17)

## Executive correction: the 2020 "single visit" data are NOT an independent replication of the 2020 "multiple visit" source

The original data from **Kendall et al. (2020), Journal of Applied Ecology, DOI 10.1111/1365-2664.13751**, Zenodo source **3987488**, original Dryad DOI **10.5061/dryad.tmpg4f4wj**, were independently downloaded and authenticated using the original source MD5 values (SHA-256 values pinned in merged PR #257). A follow-up analysis on the single-visit CSV must not be interpreted as independent validation of the already fitted multiple-visitation CSV.

**New primary-data record linkage**, keyed by source blueberry cultivar, year, block, source RP plant ID and actual treatment-flower Tag, verifies:

| Original source file comparison | Exactly matched same-flower IDs | Matched original binary fruit outcomes | Other shared measurements |
|---|---:|---|---|
| **Single-visit HB/Other** ↔ **multiple-visits exactly one** | **331 of 331 source flowers** | **0 conflicts** | Pick dates, fresh weight and other nonmissing common columns also match |
| **Multiple-visits bagged zero** ↔ **pollination no-added-pollen control** | **768 source flowers** | **0 conflicts** | Matching ancillary fields |
| **Multiple-visits bagged zero** ↔ **single-visit UP control** | **768 source flowers** | **0 conflicts** | Matching ancillary fields |
| All three files | **768 source flower identities present in all three** | **0 conflicts** | Same original flower records reused |

All 331 originally observed one-visit outcomes **were already contained in the multiple-visits source**; there is **no new visited-flower holdout** from this file. All three archived CSVs have **5,514 rows in total**, but after excluding **three exact source rows with missing original Tag (one in each original CSV, all Blue Rose unvisited)** there are **5,511 fully linkable row occurrences describing 3,644 distinct exactly identified flower records**, of which **2,545 occur in one original file**, **331 occur in two**, and **768 occur in all three**. There are **209 source single-visit unvisited records present only in the single-visit file**, from Snowchaser. Whether the three \`Tag=NA\` rows are the same physical flower cannot be proven with the missing key and is intentionally left unresolved; we DO NOT invent a unique identifier for them.

**Implication for all previous SCH blueberry results:** The source cross/self effects from hand-pollination flowers are biologically distinct experimental treatments, but their "no pollen" control rows reuse the original zero-visit controls in the other two files. None of these controls constitutes a second independent negative-control cohort. Three CSV file names are **one published study and overlapping records**, not three independent experiments/replications or 5,514 unique tagged flowers. The previous numerical within-file estimates remain numerically reproducible, but **the claimed independent replication from the 2020 single-visit file is retracted**.

Source overlap regression code: \`scripts/audit_sch_blueberry_2020_crossfile_flower_overlap.py\`. Original source counts and exact link certificates: \`data/SCH_BLUEBERRY_2020_CROSSFILE_FLOWER_REUSE_V1.csv\`. All three original full CSVs, SHA/MD5 and source JSON are retained in source-specific GitHub Actions run receipts.

## A valid, narrower biological result: honeybees fixed as the visitor identity

The *same underlying tagged-flower observations* can still answer a more conditional question: **does the between-cultivar initial-visit pattern persist when the visitor is restricted to one common bee species, Apis mellifera?** This is a visitor-taxonomic **subgroup sensitivity of the original experiment**, not an independent test.

The original 2020 single-visit CSV contains **1,309 source rows, 219 original source plant labels, 338 fruits and 971 non-fruits**:
- \`HB\` = exactly one *Apis mellifera* visit, **179** tagged flowers.
- \`Other\` = exactly one *Bombus terrestris* in northern-highbush **Blue Rose** or one *Tetragonula carbonaria* in rabbiteye **Powder Blue** and southern-highbush **Snowchaser**, **152** tagged flowers in total. These are **NOT the same bee species across cultivars**.
- \`UP\` = original bagged unpollinated control, **978** tagged flowers, including 209 source-unvisited Snowchaser flowers not in the multiple-visit file.

These code meanings are explicitly defined in the source authors' published <https://zenodo.org/records/3987488/files/README.pdf>. Within-file "unique composite IDs" alone were insufficient to detect the cross-file duplicates.

### Source-observed fruit formation by visitor

| Original cultivar | Bagged UP | Honeybee HB | Type-specific Other bee |
|---|---:|---:|---:|
| **Blue Rose** | **46/178 = 25.8%** | **60/74 = 81.1%** | **78/82 = 95.1%** (*B. terrestris*) |
| **Powder Blue** | **42/276 = 15.2%** | **8/66 = 12.1%** | **4/49 = 8.2%** (*T. carbonaria*) |
| **Snowchaser** | **66/524 = 12.6%** | **24/39 = 61.5%** | **10/21 = 47.6%** (*T. carbonaria*) |

The source risk-set is the **same tagged flower** followed from its single visitor/UP treatment to fruit formation, and original plant labels nested in cultivar × year × block supply correlated uncertainty. No treatment is counted as a new study or an independent repeat of original multiple-visit rows.

### Site-overlap-constrained, plant-label-clustered single-visitor regression

Rather than extrapolate from source sites containing only one observed visitor type, each pairwise contrast uses **only original cultivar/year/block strata in which both treatments occur**, with source site-year fixed intercepts and source plant-label-cluster robust covariance.

For the **honeybee HB vs bagged UP** contrast there are **1,148 source flower rows / 184 plant-label clusters / 9 original site-year strata**. The source site-matched subset for Snowchaser includes **30 of its 39** honeybee single-visit flowers (9 were observed in a site without matched UP controls).

| Original cultivar | Site-adjusted HB versus UP log-odds coefficient | Cluster robust nominal P | 95% cluster interval |
|---|---:|---:|---|
| **Blue Rose** | **+2.8895** | **3.81×10⁻¹¹** | [+2.0329,+3.7461] |
| **Powder Blue** | +0.8146 | 0.0873 | [−0.1193,+1.7484] |
| **Snowchaser** | **+2.1040** | **0.000723** | [+0.8841,+3.3238] |

The original 3-type slope-equality test for one *honeybee* versus bagged UP yields **P=0.00565**. Powder Blue versus the equally weighted average of Blue Rose/Snowchaser gives logit β difference **−1.6822**, plant-cluster robust 95% interval **[−2.8770,−0.4874]**, nominal P=**0.00579**.

This is **consistent with the prior PR #259 mixed-visitor first-gate difference** (P=0.00155), but **it is not an independent replication**: the 331 visited source flowers are an exact subset of the multiple-visit experiment's one-visit rows; the UP controls overlap heavily. Holding \`HB\` fixed removes one form of visitor-species mixture in this exploratory source subgroup analysis, but cannot randomize cultivar mating system, year, visitor behaviour, site pollen sources or genetic compatibility.

The original plant-label bootstrap of the **unadjusted, within site-overlap source flowers' HB−UP fruit-set risk difference** (1,999 valid source resamples) gives:
- Blue Rose **+55.2 percentage points** [**+40.7,+69.0**].
- Powder Blue **−3.1 points** [**−13.4,+7.8**].
- Snowchaser (site-overlap subset) **+44.1 points** [**+22.9,+67.3**].
- Powder Blue versus the mean of highbush source contrasts **−52.7 points** [**−69.5,−35.7**].

These confidence intervals describe variation among original plant labels **within this one research programme**; they do not control for random source-site/landscape selection or genotype-level dependence.

### Same-source alternate insect comparisons are NOT interchangeable

Within source type/year/block sites with matched visitor protocols:
- \`Other vs UP\`: 873 flowers / 142 original plant-label groups / 7 site-year intercepts. Original type-effect heterogeneity **P=0.000962**. Blue Rose (*Bombus*) and Snowchaser (*Tetragonula*) differ from unvisited controls in their respective sampled contexts, whereas Powder Blue *Tetragonula* has **no source-site-adjusted detected positive effect** (β=+0.082, P=0.896).
- \`Other vs HB\`: 312 flowers / 116 original plant labels / 8 site-year strata. Type-effect heterogeneity **P=0.255**, with strong source visitor by location imbalance. Not detecting a difference is not equivalence. A striking warning: Blue Rose's raw *Other−HB* fruit rate is +14.0 points, but its source-site-adjusted logistic effect is imprecise (P=0.734); source controls/site composition must not be omitted.

Do **not** pool \`Other\` across the three blueberry types as if it were one insect species. They are *B. terrestris* in Blue Rose versus *T. carbonaria* in Powder Blue/Snowchaser. These visitor identities were observed, not randomly assigned.

## Strongest SCH conclusion that survives the audit

A genuine tagged-flower, source-plant-clustered signal indicates **the initial recorded honeybee visit versus an unvisited bagged flower is strongly associated with fruit formation in both highbush cultivars but has no clearly detected positive effect in Powder Blue**. The difference persists after restricting to one bee species, yet comes from **the same original visited flowers as the earlier first-visit result**, not an external replication. Separately, original same-flower hand-pollination **self vs cross** treatments show Powder Blue's fruit-set gain under cross-pollen, but the original *bagged controls are reused across datasets*, and the compatible pollen deposition amount or mating-system genotype is not measured for the single-visit flower.

This pattern is a useful ecological **quantity vs quality gate** illustration and a rigorous lesson on source granularity: whether a flower received a visit, which pollen was provided, and whether that *same* flower set fruit are distinct biological observables. Genetic self-incompatibility cannot be assigned as the unique causal mediator by comparing three cultivars at non-random sites and visitors. There is still **no common manipulated floral trait \(z\) with two causally identified function-specific optimum surfaces, nor SCH compromise loss \(L\)**.

### Reproduction and source-result files

- \`scripts/analyze_sch_blueberry_2020_single_visit_taxon_holdout.py\` (source-honeybee/other bee/UP raw data rates, site-overlap GLMs, plant-label bootstrap);
- \`scripts/audit_sch_blueberry_2020_crossfile_flower_overlap.py\` (original three-file full flower-ID crosslink, source missing-tag ledger and strict zero-disagreement overlap checks);
- \`data/SCH_BLUEBERRY_2020_SINGLE_VISIT_ORIGINAL_SOURCE_CELLS_V1.csv\`;
- \`data/SCH_BLUEBERRY_2020_SINGLE_VISIT_TAXON_RESULTS_V1.csv\`;
- \`data/SCH_BLUEBERRY_2020_CROSSFILE_FLOWER_REUSE_V1.csv\`.

The full original CC0 CSVs are held in a signed GitHub Actions source-data artifact and every run checks original MD5s; primary source identities and original complete denominators fail closed. No row-level original data are duplicated in Git history.

**Evidence status: HONEYBEE_TAXON_SUBGROUP_EFFECT_PERSISTS_WITHIN_ORIGINAL_SINGLE_PROGRAMME; EXACT_331_VISITED_FLOWER_REUSE_AND_768_TRIPLE_CONTROLS_VERIFIED; NO_INDEPENDENT_REPLICATION_FROM_SINGLE_VISIT_CSV; CAUSAL_COMPATIBILITY_AND_SCH_L_NOT_IDENTIFIED.**
