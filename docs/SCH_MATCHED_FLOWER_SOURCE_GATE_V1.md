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
