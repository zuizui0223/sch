# SCH: experimentally founded Campanula americana populations — independent raw-data test of reproductive assurance

2026-11-17. Original real seed and visitor records from Makowski, Lamb & Galloway (2024), American Journal of Botany 111:e16351. Article DOI 10.1002/ajb2.16351; original data DOI 10.5281/zenodo.10814705 (Zenodo 10814705, CC BY 4.0). This is a BIOLOGICALLY DISTINCT original study from the 2020 blueberry flower-gate programme, not another re-tabulation of the same blueberry tagged flowers.

## Original source identification and experimental units

The source original files were restored from this repository's authenticated GitHub Actions source artifact run #44034953084, and their published MD5 digests were reverified before statistical analysis:

- PLdataindividual.csv, original 9,523 bytes, MD5 b84fa5c83513dbe75c0bf7840d1c74aa, SHA256 8a2a38a6552126273a83873e317ee68e1472231e19a8090436006736e30053c3.
- pollinator.csv, original 6,262 bytes, MD5 81e0deaa78a6a97e1211484cb9d0d3b3, SHA256 51101f4705b436cd75d21643910bb1fd611df4e71701918e0dcec24c07b009d5.

The archived seed file contains 237 genuine flower seed outcomes, including 24 zero-seed records, with 117 original natural-control flowers (code C) and 120 hand-pollen-supplemented flowers (code S). There are 53 original experimental-population IDs across 10 experimental sites. **52 of 53 experimental populations** have both flower-level treatments, covering **236** of the original seed records; E|22 has only one treatment and is excluded from paired inference, without adding an invented control. **109 original plant labels** have both C and S flower outcomes. The corresponding pollinator census file has 56 experimental-population rows, 53 of which link to the seed dataset at their real site/population key; 44 linked records have nonmissing visits per flower.

Four genuine original genetic source populations are represented: **AB and V** are high-autonomy, whereas **AL79 and VA73** are low-autonomy. Four genetic source populations are NOT four independent published studies, and autonomous selfing ability is not genetically or experimentally randomized independent of their population backgrounds.

## Primary pre-specified analysis: *absolute* benefit of pollen supplementation

For each experimental-population cluster we computed mean seeds per pollen-supplemented original flower minus mean seeds per control original flower. The experiment, NOT the individual flower, is the independent unit for the four-cell analysis. Source population cluster counts are shown for all four combinations.

| Autonomy / founder size | n original experimental populations | Control mean seeds | Supplemented mean seeds | Absolute source supplemental gain |
|---|---:|---:|---:|---:|
| High / single | 15 | 34.47 | 70.87 | **+36.40** |
| High / small | 10 | 36.11 | 66.89 | **+30.78** |
| Low / single | 15 | 10.53 | 44.27 | **+33.73** |
| Low / small | 12 | 22.59 | 47.84 | **+25.25** |

**48/52** original experimental populations have positive supplemented-minus-control mean seed gains, **3** have negative gains and **1** has zero. Within 109 individual plant-label flower pairs, 95 are positive, 11 negative and 3 zero; those are flowers and plants *nested within* the original study's 52 matched experimental populations, not 109 independent experimental founding events.

The original primary autonomy×founder-size interaction in *absolute seed gain* is only **+2.87 seeds** (difference in original low vs high single-minus-small source responses). A predeclared **3,999 population-stratified cluster bootstrap** gives 95% interval **[−23.89,+30.51]** and independently resampling the **10 original sites** gives **[−28.88,+34.74]**. Both include zero, with marked uncertainty. The primary interaction is therefore NOT independently supported by this reanalysis.

This is important because it distinguishes widespread pollen supplementation benefits from a more specific hypothesis that absolute supplemental benefit depends on autonomous selfing × founder density. Do not claim the second from the first.

## Secondary ecological result: realized reproductive assurance depends on original seed-set currency

The source original author study reported that readily autonomous selfers maintained more consistent reproductive output at low founding density. A separate analysis of the same archived data, using the SAME population units, characterizes the actual *control* seed output:

- High-autonomy source: **34.47** seeds per control flower when solitary, **36.11** with a small founding population.
- Low-autonomy source: **10.53** seeds when solitary, **22.59** with a small founding population.

The low-minus-high contrast among **solitary** source populations is **−23.93 seeds per natural-control flower**, and the 10-site source-block bootstrap percentile 95% interval is **[−44.20,−3.70]**. Deleting one entire original site at a time keeps the sign negative in all ten checks. In small source founding populations, the low-minus-high contrast is **−13.52 seeds**, site bootstrap interval **[−24.83,+0.56]**. The specific founder-size × autonomy difference-in-differences on control seeds is **−10.41**, site bootstrap **[−36.82,+17.26]**, not separately established.

**Crucial baseline-fecundity warning:** Even among the hand-supplemented source flowers, high-autonomy groups have higher mean seed counts than low-autonomy groups (single 70.87 vs 44.27; small 66.89 vs 47.84). Hence the control difference cannot be attributed purely to access to self-pollen. Genetic source backgrounds and intrinsic seed capacity are potentially confounded with the autonomy category; there is no randomized switch between high and low self-compatibility genotypes.

## Secondary relative-pollen-limitation sensitivity, added after the absolute-gain test

The natural biological ratio is not a mean of per-plant C/S (many individuals or populations can have S=0). For each of the four original autonomy×founder-size groups, we instead calculate:

    relative PL = 1 - [equal-population mean control seed number] /
                       [equal-population mean supplemented seed number]

This is a **ratio of four-cell population-equal means**, not an individual-pollen-limitation estimator. It is an additional exploratory effect size examined after the primary absolute seed-gain contrast; these are not interchangeable estimands.

| Original autonomy / founder group | Relative pollen limitation |
|---|---:|
| High / single | **51.36%** |
| High / small | **46.02%** |
| Low / single | **76.20%** |
| Low / small | **52.78%** |

Among solitary original populations, low autonomy has **+24.84 percentage points higher relative PL** than high autonomy. Exploratory source 95% bootstrap intervals are **[+0.86,+48.97] points** for a 3,999 stratified experimental-population bootstrap and **[+8.86,+45.26] points** for the 10-site bootstrap. This **specific solitary-source contrast remains positive when each one of the ten original sites and each one of the four original genetic source populations is excluded in turn**.

Within low-autonomy source populations, solitary minus small founding population relative PL is **+23.43 points**, 10-site 95% interval **[+2.58,+42.65]**. However, dropping one low-autonomy genetic source population AL79 reduces this density difference to only **+0.92 points**, demonstrating high dependence on the small number of original genetic backgrounds.

The **interaction** of autonomy × founder size on relative PL is **+18.08 percentage points**, with 10-site bootstrap interval **[−14.28,+55.75]**, not convincingly separated from zero. This is **not** a statistically established difference-in-differences across source genetic lineages.

### Why pollinator observations cannot be turned into a causally verified mediator

The 56 separately recorded pollinator experimental-population rows yield 53 site/population joins to seed data (no matched site/population ancestry contradictions); only **44** have reported visits-per-flower. The nonmissing original population-mean visitation rates are **1.345** for high-autonomy solitary, **0.628** for low-autonomy solitary, **0.303** for high-autonomy small and **0.506** for low-autonomy small. These are NOT counts of visits to the particular hand-supplemented or control seed-scored flowers, and visitation varies alongside cultivar/source population and founding design. They can reflect ecological context but cannot identify whether compatibility, visitor abundance or a genotype fecundity difference is the distinct causal pathway of the original seed-set contrast.

## SCH interpretation and design firewall

**Empirically:** the newly recovered independent Campanula original study shows a widespread within-population seed benefit from pollen supplementation (48/52 positive), a descriptive difference in control seed output and relative pollen limitation between high/low autonomous-selfing source populations when founded as solitary plants, and a non-detected autonomy×founder-size interaction under the primary absolute-gain estimand.

**Conceptual connection:** this is a *mate-assurance gate* that can be compared qualitatively with the 2020 blueberry study's flower-level *visit-access and source-pollen-quality gates*. They are two truly separate author programmes with different fitness currencies (seeds per Campanula flower versus blueberry tagged-flower fruit-set probability). Do NOT pool them in a pseudo-meta effect, count source papers by CSV files, or identify a shared trait-specific architectural compromise from them. The Campanula source grouping is genetic-background-confounded and not randomized for autonomy.

The authentic 2026 Harder & Hamnett-Mount Brassica study (10.1002/ajb2.70204, source 10.5061/dryad.hx3ffbgtq) remains a separate benchmark with open metadata but authentication-gated original CSV downloads in this runner; no fabricated raw-row conclusions are borrowed from it.

**SCH causal-functional loss \(\mathcal L\)**, common same-coordinate opposing pure-function optima and causal evolutionary selection for selfing were NOT estimated by this original archive reanalysis.

## Reproduction

- Source ingestion: scripts/ingest_sch_campanula_americana_2024.py, original MD5 verified, original Zenodo 10814705.
- Experimental-population biological unit and all 10-site source bootstrap calculations: scripts/analyze_sch_campanula_americana_2024_assurance.py, reproducible fixed seed 20261117.
- Human-inspectable source-cell and original-pop/site bootstrap outcomes:
  data/SCH_CAMPANULA_2024_REAL_SOURCE_2X2_CELLS_V1.csv and
  data/SCH_CAMPANULA_2024_REAL_SOURCE_BOOTSTRAP_CONTRASTS_V1.csv.
- Original source CSVs and a complete per-experimental-population JSON receipt are retained in the matching GitHub Actions artifacts rather than silently committed as new observations.

**Result classification:** REAL_INDEPENDENT_CAMPANULA2024_SEED_ASSURANCE_GATE; ABSOLUTE_SUPPLEMENT_GAIN_INTERACTION_NOT_DETECTED; RELATIVE_SINGLE_FOUNDER_PL_DIFFERENCE_POSITIVE_DESCRIPTIVELY_WITH_SITE_BOOTSTRAP; AUTONOMY_GENETIC_CAUSAL_IDENTIFICATION_AND_SCH_L_NOT_ESTABLISHED.
