# SCH 2020 blueberries: original same-tagged-flower compatibility and visitation gates (2026-11-17)

## An actual source-computed biological result, not source-background literature

Kendall et al. (2020), *Journal of Applied Ecology* 57:2454–2462, DOI **10.1111/1365-2664.13751**, studied fruit formation in individually tagged blueberry flowers under natural/controlled visits and hand-pollination treatments. The archived original CC0 source is Zenodo **record 3987488**, original Dryad DOI **10.5061/dryad.tmpg4f4wj**. All 3 original tagged-flower CSVs passed the public original Zenodo manifest MD5 checks (ingress PR #257), and this analysis additionally re-verifies the exact same files before calculating source summaries.

The original source flower-count evidence belongs to **ONE original published study programme**, **not** 5,514 independent taxon/study replicates. Each original experiment follows binary fruit formation (FS=0/1) on its **same tagged flower**. The original composite (cultivar type, year, block, plant label, flower tag) had no duplicate flower identity within each file:

| Source original experiment | Original flower rows | Source original plant-label clusters | Fruits 1 | Fruits 0 |
|---|---:|---:|---:|---:|
| Multiple visits (0–15) | **2,080** | **238** | 992 | 1,088 |
| Hand self/cross/open/no pollen | **2,125** | **243** | 1,209 | 916 |
| Single visit/bagged control | **1,309** | **219** | 338 | 971 |

The raw files remain in the signed GitHub Actions source artifacts and are not republished as invented observations. Original source SHA256s:
- Multiple visits: d54646e67a7bdd986f27195954b77abf07631cb0d0863ba7edadcf99e32a1f2e.
- Hand pollination: 07c9cf0da8edd7d89d7a83571b730412b8f586dbadb9311957b0192c8b2ade53.
- Single visit: 8e063d82256ef72edad3d429d754b3882888205f78c559bb61aea643c09594c3.

### Positive result 1 — biological compatibility strongly changes how pollination reaches fruit formation

Among original **676 hand-pollinated tagged flowers** (320 other-cultivar pollen, 356 same-cultivar pollen), cross versus self comparisons are in the **same flower fruit-set outcome currency**. All three blueberry types had both pollen treatments represented in each original year × block site used for that comparison.

| Original blueberry cultivar type | Hand cross pollination | Hand self pollination | Source empirical risk difference (cross − self) | 1,976 valid source-plant-label block bootstrap draws, 95% CI |
|---|---:|---:|---:|---|
| **Blue Rose** (northern highbush; source n cross=20, self=100) | **19/20 = 95.0%** | **92/100 = 92.0%** | **+0.0300** | [−0.1048,+0.1238] |
| **Powder Blue** (rabbiteye; n cross=181, self=167) | **128/181 = 70.7%** | **60/167 = 35.9%** | **+0.3479** | **[+0.1837,+0.5083]** |
| **Snowchaser** (southern highbush; n cross=119, self=89) | **112/119 = 94.1%** | **79/89 = 88.8%** | **+0.0535** | [−0.0451,+0.1614] |

The descriptive **Powder Blue minus equally weighted average Blue Rose/Snowchaser cross-self risk-difference contrast** is **+0.3061**, bootstrap **[+0.1220,+0.4855]**. Source-plant ID labels nested in cultivar × year × block are resampled as blocks, rather than treating each original flower as an independent experimental replicate. Of 1,999 requested bootstrap resamples, 23 lacked at least one treatment in a source-type resample and were rejected according to the published source-computation rules; 1,976 valid draws remain.

The source year×block overlaps for Powder Blue all have positive cross-minus-self contrasts: B81 in 2017 **+0.3870**, S3R in 2017 **+0.5208**, B81 in 2018 **+0.0696**, and S3R in 2018 **+0.1704**. The within-site **harmonic-count weighted** risk difference is **+0.3480**, close to the unstratified +0.3479. For Blue Rose, one original site gives +.0300, and Snowchaser's two sites produce a harmonic-weighted +.0406. **All source year×block comparisons used for this specific within-type contrast have both treatments represented**, so the strong Powder Blue signal is not an artifact of pooling fully disconnected original sites. It does show substantial **spatial/temporal response heterogeneity** in the original one programme.

**Scope:** Pollen source is an experimental treatment, but original host **cultivar/self-compatibility type was not randomized** across experimental environments. The contrast is not proof that *genetic self-incompatibility alone* causes the original study's between-type variation, or that either cultivar type is representative of the global plant community. This is a source reanalysis of known primary results, with newly computed plant-block uncertainty and explicit within-site denominator check, not a second independent biological experiment.

### Positive result 2 — the visitor-to-fruit gate is steeply conditional on the flower's cultivar type

The original 2,080 tagged flowers in the multiple-visit CSV contain **769** controls with 0 visits, **331** flowers with 1 visit, **272** with 2 visits, **205** with 3 visits, **142** with 4 visits and **130** with 5 visits. Higher visits (6–15) occur less frequently and are not forced to inform the primary 0–5 slope; no visit count is fabricated by pooling separate flowers.

Observed source fruit proportions, **per tagged flower**, with prespecified visit bins:

| Original cultivar type | 0 visits | 1 visit | 2–3 visits | 4–5 visits | 6–10 visits |
|---|---:|---:|---:|---:|---:|
| **Blue Rose** | 46/178 = **25.8%** | 138/156 = **88.5%** | 242/271 = **89.3%** | 125/135 = **92.6%** | 31/32 = 96.9% |
| **Powder Blue** | 42/276 = **15.2%** | 12/115 = **10.4%** | 25/132 = **18.9%** | 24/99 = **24.2%** | 60/92 = 65.2% |
| **Snowchaser** | 48/315 = **15.2%** | 34/60 = **56.7%** | 56/74 = **75.7%** | 30/38 = **78.9%** | 27/27 = 100% |

This is a **new original-source unit-aligned calculation**: the flower exposed to a recorded number of visits is the SAME flower whose fruit outcome was recorded. A site-(year×block)-intercept binomial GLM with cultivar-specific log(1+visits) slopes and original plant-ID-label cluster-robust covariance gives:

| Original source-visitation support | Blue Rose source log-odds slope | Powder Blue slope | Snowchaser slope | All 3 slopes equal: nominal Wald P |
|---|---:|---:|---:|---:|
| **0–5 visits** (1,849 tagged flowers, 238 plant clusters, 10 site intercepts) | **+2.5029** | **+0.8112** | **+1.9747** | **0.000288** |
| **1–5 visits only** (1,080 tagged flowers, 192 plant clusters) | **+0.8731** | **+0.5942** | **+1.2447** | **0.497** |

For the 0–5 model, the Powder Blue log-visit slope is **−1.4276** relative to the equally weighted average Blue Rose/Snowchaser slopes (plant-cluster robust 95% CI **[−2.1289,−0.7262]**, nominal P=**0.000066**). On **only already visited flowers** the corresponding contrast is **−0.4647 [−1.3600,+0.4307]**, nominal P=0.309.

**Interpretation:** When unvisited bagged controls are included, source blueberry types differ substantially in fitted visit–fruit relationships. Once the 0-visit controls are excluded, a contrast among type-specific *incremental* 1–5 visit slopes is **not detected**. These are **different subsets, power and exposure processes**, so the latter is not evidence that all positive-visit effects are identical or that every source difference is caused exclusively by the first visit. In particular, visitor taxon composition differs across cultivar types, and 0-visit controls are bagged flowers rather than a randomized exposure count sampled from exactly the positive-visitor process.

## A genuine SCH mechanism connection — but not yet function-specific adaptive conflict

Together the authentic flower-level data show why the presence of floral visitors is not itself sufficient to specify **realized reproductive fitness**: the same basic type of visit can have different probabilities of yielding a fruit depending on the **source pollen's compatibility and host floral system**. The flower-level common denominator avoids a key artifact of the 2024 milkweed stage contrast (whole-plant fruits versus ten-flower pollinium insertions).

This is one original source programme with three cultivar types, not proof of an ecological law across unrelated plants. It does **not** report deposited compatible pollen grains, pollen tube germination, ovule fertilization, post-zygotic abortion or seed viability from these SAME tagged flowers. Pollen source treatments and pollen compatibility types are not interchangeable, and the fruit outcome alone is not final maternal descendant fitness. No controlled floral phenotype trait axis here directly identifies two opposing pure-function fitness optima or SCH loss \(L\).

### Reproducibility and supported claim boundaries

Source input was byte-verified against Zenodo original published MD5 for each CSV, and each source file's SHA256 and the exact original row and plant-cluster counts are recorded in the GitHub source analysis JSON receipt. Script \`scripts/analyze_sch_blueberry_2020_matched_flower_gate.py\` produces: per-cultivar cross/self fruit counts; 1,999 plant-ID-label resample percentile intervals; source year×block overlap and site-adjusted risk differences; 18 original visit-bin fruit count/rate rows; and two site-adjusted, source-plant-label sandwich logistic models with 0–5 versus 1–5 visit support.

The numerical model outputs are preserved separately in:
- \`data/SCH_BLUEBERRY_2020_GENUINE_CROSS_SELF_FLOWER_GATE_V1.csv\`
- \`data/SCH_BLUEBERRY_2020_GENUINE_VISIT_BINS_V1.csv\`
- \`data/SCH_BLUEBERRY_2020_GENUINE_VISIT_CLUSTER_SLOPES_V1.csv\`

The complete original three CSVs and original-source JSON output are stored in the dedicated short-retention GitHub Actions artifact, not silently added as fabricated new observations or independent replicate studies.

**Current status: POSITIVE_SOURCE_VERIFIED_SAME_TAGGED_FLOWER_VISIT_AND_CROSS_SELF_FRUIT_GATES; HOST_BREEDING_SYSTEM_CAUSAL_EFFECT_NOT_IDENTIFIED; SOURCE_TRAIT_SPECIFIC_COMPROMISE_L_NOT_IDENTIFIED.**
