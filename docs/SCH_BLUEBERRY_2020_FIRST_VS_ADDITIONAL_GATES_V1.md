# SCH: two distinct visitation gates on the **same** tagged blueberry flowers (2026-11-17)

## A new result from actual original flower records, not a new literature review

Kendall et al. (2020), *Journal of Applied Ecology*, DOI **10.1111/1365-2664.13751**, openly deposited their original experiment at Zenodo **3987488** (original Dryad DOI **10.5061/dryad.tmpg4f4wj**). The original CSVs were recovered and MD5-verified in merged SCH PR #257, and independent per-flower outcome tests were established in merged PR #258. One biological programme studied three distinct blueberry **cultivar types**, not three independent papers or a random sample of natural mating systems.

The source multiple-visit dataset contains **2,080** individually tagged flowers, with a binary fruit-set outcome for the *same* flower that had a recorded 0–15 visits. Original plant labels are nested within cultivar × year × block. The new analysis is restricted **a priori to 0–5 visits: 1,849 flower rows, 238 source plant-label clusters and 10 cultivar/year/block strata**, with 769 bagged zero-visit controls and 1,080 flowers receiving one to five recorded visits.

Rather than compare two regressions with different flower populations, the *same 1,849 source rows* are fitted **in one site-fixed-intercept binomial GLM**, with two **different** regressors for each cultivar:

\[
\mathrm{logit}\Pr(\mathrm{fruit}_i=1)
 = a_{\mathrm{cultivar}\times\mathrm{year}\times\mathrm{block}}
 + b_{\mathrm{first},c}\mathbf 1(v_i\geq1)
 + b_{\mathrm{extra},c}\mathbf 1(v_i\geq1)\log(v_i).
\]

Here \(\mathbf 1(v\ge1)\) distinguishes zero visits (bagged controls) from exactly one visit at fixed site/year; \(\mathbf 1(v\ge1)\log(v)\) describes additional exposure from one through five visits. The two coefficients are estimated jointly and their covariance is computed by a **source-plant-label cluster-robust sandwich**, not by counting each flower as an independent treatment replicate. Both are **associations conditional on source experimental design**, not direct measures of compatible pollen-grain transfer.

## Primary source-computed results

| Original cultivar type | 0 → 1 visit, logit beta (plant-cluster P) | Additional 1–5 visits, slope on log(visits) (plant-cluster P) |
|---|---:|---:|
| Blue Rose (northern highbush) | **+2.9257** (P=**2.54×10⁻¹⁴**) | **+0.5579** (P=**0.0266**) |
| Powder Blue (rabbiteye) | +0.7423 (P=0.1167) | +0.4219 (P=0.0804) |
| Snowchaser (southern highbush) | **+1.9033** (P=**1.23×10⁻⁶**) | **+0.7647** (P=**0.0120**) |

A direct **two-degree-of-freedom** covariance-based test of whether the three cultivar slopes are equal:

| Formal 2020-source fitted question | Wald χ²(2) | Source exploratory P |
|---|---:|---:|
| Does the bagged-zero versus first-visit effect differ across the three cultivars? | **12.9381** | **0.001551** |
| Do *additional* 1–5-visit slopes differ across the three cultivars? | 0.7792 | 0.6773 |

Powder Blue's **first-visit coefficient minus the equally weighted mean** of Blue Rose and Snowchaser first-visit coefficients is **−1.6722**, original plant-cluster robust 95% CI **[−2.7444,−0.6000]**, nominal P=**0.002237**. The comparable *incremental* contrast is **−0.2394 [−0.8505,+0.3718]**, P=**0.4427**.

**Strongest supported biological message:** the *observed contrast between bagged controls and receiving a first visit* differs markedly among these blueberry cultivars; a comparable detectable three-cultivar difference in the *additional 1–5 visitation response* is absent in the same joint model. This does **not** prove that all additional visit slopes are identical, that all cultivar variation is exhausted by the first visit, or that the contrast is a purely randomized first-compatible-pollen effect. The 0-visit flowers were bagged as part of the original treatment protocol, and the flower visitor species also differ between cultivars.

### Observed proportions reveal an important Simpson-like site/year issue

| Cultivar | Fruit from bagged 0-visit flowers | Fruit from exactly 1-visit flowers | Unadjusted 1−0 risk difference |
|---|---:|---:|---:|
| Blue Rose | 46/178 = 25.8% | 138/156 = 88.5% | +62.6 percentage points |
| Powder Blue | **42/276 = 15.2%** | **12/115 = 10.4%** | **−4.8 points** |
| Snowchaser | 48/315 = 15.2% | 34/60 = 56.7% | +41.4 points |

Despite Powder Blue's **negative** *pooled raw* risk difference, its **site-adjusted** first-visit logit slope is **positive, but imprecise** (β=+0.7423, P=0.1167). This is not an error: the 0/1 visit counts were strongly unequal across site/year blocks. In Powder Blue's 2018 B81 and S3R blocks there were just **4** and **5** once-visited flowers, respectively, compared with **80** and **90** bagged zero-visit flowers. The four source site/year block differences are −0.0019, +0.0833, +0.2125 and +0.0556, respectively. Never interpret the unstratified Powder Blue −4.8-point difference as an experimentally certified **negative** effect of receiving a first visit.

The full original site/year zero/one count and fruit-set ledger is \`data/SCH_BLUEBERRY_2020_ZERO_TO_ONE_SITE_RISKS_V1.csv\`.

## Site-overlap sensitivity: no extrapolation from sites without zero controls

One Snowchaser block, 2017 SFI, includes **46** flowers with 1–5 visits but **zero bagged 0-visit controls**. Repeating the single joint model on the **nine** cultivar/year/block strata that contain *both* zero and exact-one visits retains **1,803 original tagged flower rows and 222 source plant clusters**. This completely removes any implicit first-visit contrast extrapolation from the nonoverlap site.

| Same original joint site/plant cluster model | All ten original sites | Nine sites with matched 0 and 1 visit support |
|---|---:|---:|
| First-visit three-type heterogeneity P | **0.001551** | **0.001568** |
| Additional 1–5 visit heterogeneity P | 0.6773 | 0.7566 |
| Powder Blue versus mean highbush *first* coefficient difference | −1.6722 | −1.6795 |
| Powder Blue versus mean highbush first-effect P | 0.002237 | 0.002281 |

Thus the differentiated first-visit/source-bagged contrast does **not** depend on the single original site lacking controls. The same nine-site sensitivity does not make cultivar assignment random and does not correct selection/mating-system confounding across the different source sites.

## Separate original hand-pollination experiment: source quality gate, not the same flowers

The archived 2020 **hand-pollination** source includes **2,125 individually tagged flower rows**, with all four original pollen treatments: bagged/no pollination, hand-self, hand-cross and open pollination. These are **not the same tagged flowers as the multiple-visit experiment**, and records are never joined across files by an unverified tag string.

| Original cultivar | Bagged, no added pollen | Hand self-pollination | Hand cross-pollination | Open pollination |
|---|---:|---:|---:|---:|
| Blue Rose | 46/178 = 25.8% | 92/100 = 92.0% | 19/20 = 95.0% | 120/125 = 96.0% |
| **Powder Blue** | **42/276 = 15.2%** | **60/167 = 35.9%** | **128/181 = 70.7%** | **213/269 = 79.2%** |
| Snowchaser | 48/315 = 15.2% | 79/89 = 88.8% | 112/119 = 94.1% | 250/286 = 87.4% |

These directly observed per-tagged-flower original fruit-set proportions are not planted per-stage pseudo-counts. The original **hand-cross and hand-self** treatments on different flowers both involved emasculation and hand pollination, so their within-site contrasts are especially interpretable (fully analysed with 1,999 original plant-label block bootstrap in PR #258). The **no-pollination bagged controls**, however, were not necessarily equivalently emasculated; their comparisons against manually pollinated flowers should **not** be treated as a clean randomized change in pollen-grain quality or compatibility. The source 0-visit controls had surprisingly frequent fruits (15–26%), which may arise from experimental leakage, autonomous fruit set or other original mechanisms; the archive does not distinguish them. No mechanism is invented for this baseline.

Year×block source-overlap was checked for every cultivar/treatment pair. For Powder Blue all four sampled site/year blocks contain both self and cross, and the matched-site cross−self fruit risk difference was **+0.3480**, as independently found in PR #258. With no-added-pollen controls, some source contrasts differ because the true treatment protocols differ in emasculation and bagging; *do not* call cross−no a pure compatibility effect.

Original source treatment and site-coverage counts are retained in \`data/SCH_BLUEBERRY_2020_FOUR_POLLINATION_PROTOCOL_RATES_V1.csv\`.

## Meaning for SCH: distinguish access, compatibility and stage-specific realized fitness

The original study supplies one useful cross-context *observational gate*:
- **Access:** whether an original tagged flower received a recorded visitor at least once (against bagged unvisited controls).
- **Dose:** conditional additional recorded visits on already-visited flowers.
- **Quality/context:** source-specific hand-self versus hand-cross manipulation, on a *different original flower cohort*.
- **Realized outcome:** fruit formation on the **same original flower** as its own applied visit/pollination treatment.

It does **not** join a measured *compatible deposited pollen grain*, pollen-tube germination, zygote, ovule fertilization, fruit abortion and viable seed into a measured common flower-stage mediation chain. It does **not** independently randomize cultivar-specific self-incompatibility alleles, pollinator species assignment or floral trait phenotypes. The 3 cultivars belong to one original author programme, and source plant labels are not necessarily independent genets. Nominal regression/Wald P values are exploratory and do not establish a confirmatory meta effect across global plants.

### Reproducibility

The workflow \`.github/workflows/sch_blueberry_2020_first_additional_gates.yml\` restores the original three published CC0 CSVs from the verified Zenodo-source artifact in this same repository, rechecks publisher-listed MD5, runs \`scripts/analyze_sch_blueberry_2020_first_additional_gates.py\` and preserves signed source JSON and original rows. The script fits the 0-versus-1/extra-visits **joint** logit, the nine-site overlap check and original four-pollination treatment risk/overlap table without silently aligning separate experiments. Numeric original-source result ledgers:

- \`data/SCH_BLUEBERRY_2020_FIRST_ADDITIONAL_GATE_RESULTS_V1.csv\`
- \`data/SCH_BLUEBERRY_2020_ZERO_TO_ONE_SITE_RISKS_V1.csv\`
- \`data/SCH_BLUEBERRY_2020_FOUR_POLLINATION_PROTOCOL_RATES_V1.csv\`

**Current scientific status: GENUINE_SAME_TAGGED_FLOWER_VISIT_FIRST_GATE_HETEROGENEITY_WITH_SOURCE_SITE_ROBUSTNESS; EXTRA_VISIT_TYPE_DIFFERENCE_UNDETECTED; GENETIC_COMPATIBILITY_MEDIATION_AND_SCH_CONFLICT_LOSS_L_NOT_IDENTIFIED.**
