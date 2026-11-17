> **Source and empirical reanalysis completed (2026-11-17):** Exact MD5 verification recovered 237 original seed/flower rows (117 control, 120 supplemented), 56 pollinator population rows, 53 original experimental populations across 10 sites and four source genetic backgrounds. **52/53** experimental populations had both treatments, and **109 plant labels** had matched C/S flower outcomes. Primary absolute supplemental-gain autonomy×founder-size interaction = **+2.87 seeds**, 10-site bootstrap 95% interval **[−28.88,+34.74]** (not supported). A separate exploratory ratio-of-population-equal-means analysis finds relative pollen limitation among solitary founders **76.2% low-autonomy versus 51.4% high-autonomy**; difference **+24.84 points**, 10-site bootstrap **[+8.86,+45.26]**. The founder-size×autonomy relative-PL interaction remains uncertain, and autonomy is **genetic-source-confounded**. All original source results, CIs and inference limits are in [the finished data analysis](SCH_CAMPANULA_2024_EXPERIMENTAL_ASSURANCE_V1.md). None identify causal functional trait optima or SCH loss L.

# SCH independent experimental system: Campanula americana colonization pollen limitation

2026-11-17, source-first original-data work. The immediate research goal is to determine whether the seed-set benefit of supplemental pollen depends jointly on autonomous self-fertilization capacity and founder-population size, using a biological unit of experimental population rather than pretending each flower is independent.

## Independent source provenance

Makowski, Lamb & Galloway (2024), American Journal of Botany 111:e16351. Article DOI 10.1002/ajb2.16351. Original openly licensed Zenodo experimental data, record 10814705, DOI 10.5281/zenodo.10814705, Creative Commons Attribution 4.0.

Two original files are MD5 pinned:
- PLdataindividual.csv: b84fa5c83513dbe75c0bf7840d1c74aa. This is the actual archive filename, even though the landing-page description uses an earlier name.
- pollinator.csv: 81e0deaa78a6a97e1211484cb9d0d3b3.

The original authors founded solitary-plant and small experimental populations from four source populations differing in autonomous selfing. Separate hand-supplemented and control flower treatments measured seed number. Experimental-population-level observations measured bee visitation. The original published conclusion reports that seed set was comparatively insensitive to founder number for high-autonomy plants, while low-autonomy plants showed density-dependent reproduction. This remains a source-author result until SCH computes the original raw rows independently.

## Source-specific estimand and biological denominator

The target within experimental population is the treatment-specific seed-number benefit, mean seeds per supplemented flower minus mean seeds per control flower. It is then contrasted by high/low autonomous selfing and by single/small planted population, with time and spatial/site effects treated as study-design conditions rather than ignored. Individual flowers are repeated within plants, and plants are nested in experimental populations and source-population genetics. Four source genetic populations cannot be promoted to four independent journal studies, and autonomy may not be independently randomized from source background.

The pollinator.csv table is at a different temporal and observational grain. Never attach a population-level visitation number as if it were the exact flower's observed pollinator or pollen deposition count. No causal function-specific optimum or SCH loss L follows from the supplementary seed-set association.

## Source verification gate

GitHub workflow sch_campanula_americana_2024_source.yml retrieves both authentic Zenodo CSVs, checks the published MD5s, records their actual headers, biological ID roles, row counts, level distributions, missingness and repeated flower labels, and archives the original bytes plus SHA256. Original biological inferential tests must wait until this gate succeeds. Source availability should be reported separately from empirical model success.

## 2026 Brassica benchmark remains access gated

Harder & Hamnett-Mount (2026), American Journal of Botany DOI 10.1002/ajb2.70204, original dataset DOI 10.5061/dryad.hx3ffbgtq. Its public manifest has seven CSVs and README. Experiment 1 comprises 86 plants assigned to 25/50/75/100 percent hand-outcrossed flower treatments; Experiment 2 comprises DIFFERENT 46 plants assigned to 25/75 percent treatments with fruit and ovule fertilization / abortion / seed records. No fabricated cross-experiment plant/flower join can create a full pollen to fruit to seed chain from these. The public Dryad metadata are accessible, but its API file-download action requires OAuth2 in this environment (as documented by Dryad's client), and the original CSV bytes are not yet verified. Do not claim newly computed source effects there until the bytes are authenticated.

The alternative original Zenodo Campanula system here supports a different, genuinely independent ecological study and an experimentally imposed founding-density treatment. Its autonomy classes, however, are not a controlled molecular change in self-compatibility, and no shared-floral-trait function conflict loss L is identified.
