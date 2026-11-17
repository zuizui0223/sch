> **Source-independence correction (2026-11-17, exact MD5-verified flower ID audit):** The original 2020 blueberry single-visit CSV reuses **all 331** visited flowers present as exactly-one-visit flowers in the multiple-visit CSV. **768** fully tagged unpollinated controls recur in all three archived source CSVs (one additional Blue Rose unvisited record has missing Tag in each file and cannot be strictly linked). Across the three CSVs there are **5,514 row occurrences**, but only **3,644 distinct fully identified flower IDs** and three unlinked missing-tag records. Hence these files are **not independent experimental flower cohorts**; effects within each file may be calculated, but their apparent agreement cannot be treated as independent replication. The separately fitted hand-self/cross flowers differ from the multiple-visit treatment flowers, but share the no-pollen controls. Full proof and corrected inference: [Source cross-file reuse audit](SCH_BLUEBERRY_2020_INDEPENDENT_SINGLE_VISIT_TAXON_GATE_V1.md).

# SCH: transition from unrelated fitness-stage proxies to genuinely tagged-flower source data (2026-11-17)

## Immediate biological objective

The original 2024 *Asclepias syriaca* reanalysis (merged SCH PRs #252–#256) established a **measurement-denominator failure mode**: apparent selection on flower number differs when fruits are counted on the entire stem but pollinia are scored from a fixed 10-flower sample. Correction for total flower opportunity removes the nominal overall female-stage difference across OLS, Poisson, and NB2. Among fruit-positive stems alone, a negative per-flower association occurs, but this is vulnerable to flower opportunity, conditional selection on F>0, and 10-trait multiplicity; none identifies causal resource allocation or SCH compromise loss L.

The new priority is to assemble **one bona fide experimental source with a labelled flower followed through visits/pollination to fruit outcome**. Preserve the identity of every flower and plant; verify that the input process and outcome refer to **the same risk set**, rather than joining unconnected means.

## Source 1: tagged flowers with known visitation and fate (ingress attempt)

Kendall et al. (2020), *Journal of Applied Ecology*, DOI **10.1111/1365-2664.13751**. Dataset preserved on **Zenodo record 3987488** with original Dryad DOI **10.5061/dryad.tmpg4f4wj**, CC0. The original three flower-level fruit-set source CSV names and exact MD5 checksums are:

| Original published CSV | Expected MD5 | Interpretation |
|---|---|---|
| fruit_set_single_visit_experiments_JAPPL-2020-00197.csv | d7ed02c7aa254a963043539c06c99ed7 | one known visitor (or bagged control) per tagged flower followed to fruit set |
| fruit_set_multiple_visits_experiments_JAPPL-2020-00197.csv | 5617777fcef1c46bb4e0bab5ccc22ce6 | flower visit count 2–15 and ultimate fruit set |
| fruit_set_pollination_experiments_JAPPL-2020-00197.csv | e630cd466935e7709e874ff6706f7ce0 | open, self, cross, bagged flowering treatments and fruit set |

The paper compared three blueberry *types*: a northern and a southern self-compatible highbush type versus a partially self-incompatible rabbiteye type. The original source reports fruits after increasing visits, with >90% achieved at three to five visits in highbush versus 58% after 15 visits in rabbiteye. These are **published original author results**, not new SCH model outputs. The matched flower-tagged source potentially supports a source-reanalysed plant- and block-aware estimate of the relationship between visit number and reproductive conversion.

**Important limits:** Mating system/cultivar type is NOT independently randomized across site, block and year; a blueberry type interaction is observational/descriptive, despite the experimental manipulation of floral visits/pollination protocols. Number of visits is not guaranteed to equal effective compatible pollen transfer, and neither pollen deposition nor fertilization of a given flower was directly counted. Data from three files are *one published research programme*, not three independent trials or three independent papers. Flower identity must be checked for duplicates and the fruit outcome must be binary as the source says.

The source workflow \`scripts/ingest_sch_2020_blueberry_original_flower.py\` fetches each original published CSV from the original Zenodo archive, matches its exact published MD5 and records all columns, visitor/visit/treatment roles and flower composite-ID uniqueness. No regression or new biological P value is reported until source rows are actually retrieved and judged independently.

## Source 2: two linked, but nonidentical, stages within Brassica experiment programmes

Harder & Hamnett-Mount (2026), *American Journal of Botany* 113:e70204, DOI **10.1002/ajb2.70204**, original Dryad DOI **10.5061/dryad.hx3ffbgtq**. Published March 31 2026 on Dryad; paper published May 14 2026. The source archive lists **eight original files**: seven CSVs and one README. Experiment 1 involved **86** plants randomly assigned to hand-outcross **25% (n21), 50% (n23), 75% (n20), 100% (n22)** of flowers, with individual flower timing, raceme and eventual binary fruit outcome. Experiment 2 involved a SEPARATE **46** plants randomized to 25% (n21) or 75% (n25) pollination, with ovule fertilization, abortion and seed development counted in harvested fruits.

The original authors found fruit initiation per flower fell late in the sequence of flower opening and the fruitful window narrowed from approximately nine days for poorly pollinated plants to five days for fully pollinated plants; in experiment 2 roughly **61% of ovules** were fertilized in intentionally pollinated, fruiting flowers, with most fertilized ovules developing into seeds.

**Crucial source separation:** The Experiment-1 *flower fruit fate* and Experiment-2 *ovule fertilization* records are **different plants/experiments** and cannot be joined by a fabricated flower ID to estimate a single joint pollinium→fruit→seed conditional probability. Moreover, the ovule data are from **developing fruits only**, which conditions on a downstream outcome and prevents quantifying failures in flowers that never set fruit. These are separate, meaningful empirical estimands, not one complete causal chain.

The original Dryad data are publicly documented, but the exact downloadable original CSV **bytes have not been acquired here yet**. Earlier SCH source audits found that Dryad currently allows anonymous public metadata while its binary API requires credentials/blocks automated downloads (401/403 in GitHub Actions). Do NOT report new derived 2026 *Brassica* numerical effects until checksum-verified original CSV rows are obtained, and do not retry known denied endpoints indefinitely.

## Scientific test gate

A credible cross-system observation is whether:
1. Actual *flower*-level visit/pollination access changes the probability of *that flower* setting fruit, preserving plant and source experimental block.
2. The same flower's compatibility, fertilization, abortion and final seed/fruit fate are actually measured, rather than proxies with unmatched denominators.
3. Mating system and floral timing change the visitation-to-fruit transition in **biologically distinct** ways across populations/systems, but are not represented as randomized causal factors when they are not.

The minimal target outcome is a plant-cluster-aware, per-tagged-flower \`fruit_set ~ visit_count × host_type + design constraints\` test with qualified visitor/tag/plot fields, registered source licensing and original study denominators. If dataset identity or field grain fails, report the blocker rather than inventing flowers or treating multiple records per plant as independent.

**SCH pure-function optima and empirical compromise loss L are NOT measured by either source.**

## Genuine Zenodo source accession outcome (2026-11-17)

All three archived original tagged-flower CSVs passed their publisher-listed MD5 values. Source-ingress GitHub Actions run #43906931357.

| Source original experimental file | Original flower rows | Fruit set = 1 | Fruit set = 0 | Original unique within-file flower composites |
|---|---:|---:|---:|---:|
| Multiple visits (0–15) | **2,080** | **992** | **1,088** | **2,080** |
| One visit or bagged control | **1,309** | **338** | **971** | **1,309** |
| Hand-cross / hand-self / open / bagged | **2,125** | **1,209** | **916** | **2,125** |

- Multiple original SHA256: d54646e67a7bdd986f27195954b77abf07631cb0d0863ba7edadcf99e32a1f2e, 187849 bytes.
- Single original SHA256: 8e063d82256ef72edad3d429d754b3882888205f78c559bb61aea643c09594c3, 89632 bytes.
- Pollination original SHA256: 07c9cf0da8edd7d89d7a83571b730412b8f586dbadb9311957b0192c8b2ade53, 175687 bytes.

Multiple-visit original cultivar-type counts: Blue Rose 772, Powder Blue 778 and Snowchaser 530 flowers. Visit-number counts: 0:769, 1:331, 2:272, 3:205, 4:142, 5:130, then thin coverage for 6–15 (44 rows at 15 visits). Pollination experiment: cross 320, self 356, open 680, no pollination 769 original tagged flower rows. These sample counts are real original-source descriptive results, **not 5,514 independent biological studies**. Flower tags were unique within each source file when crossed with plant, species, year and block; across-file tags are not source-proven to denote the same flower.

Next code is a new plant-label-block-aware raw-flower outcome regression; this accession step intentionally made no fitted ecological claims.
