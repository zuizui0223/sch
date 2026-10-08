# SCH Pedicularis published empirical data recovery v1

## Purpose

The current Pedicularis programme has no project-owned CAL-A/B field
measurements yet. That does **not** mean that Pedicularis rex has no published
empirical data.

This recovery separates historical measurements into:

```text
public raw data
published field measurements / SD
published aggregate supplements
experimental model coefficients / SE
historical field-design sample sizes.
```

These can inform variance, effect-scale, feasibility and biological target
rationale. They do not automatically become same-context prospective F0 gate
values.

## Machine ledgers

Source-level recovery:

```text
empirical/architecture/PEDICULARIS_PUBLISHED_DATASETS_V1.csv
```

Measurement-level recovery:

```text
empirical/architecture/PEDICULARIS_PUBLISHED_EMPIRICAL_PRIORS_V1.csv
```

Audit:

```bash
python scripts/audit_pedicularis_published_empirical_priors.py
```

## Highest-value source — Xia et al. 2013 raw Dryad dataset

Article:

```text
Evidence of a component Allee effect driven by predispersal seed predation
doi:10.1098/rsbl.2013.0387
```

Data repository:

```text
Dryad doi:10.5061/dryad.6cv06
file: raw data.xlsx
size listed by Dryad: 89.60 KB.
```

The article explicitly states that the data were deposited in Dryad and the
current Dryad landing page lists the raw Excel file.

Published design includes:

```text
2005 pollination sample   60 flowers
2011 pollination sample  175 flowers

2005 reproductive sample 16 spikes  (6 sparse / 10 dense)
2011 reproductive sample 58 spikes (26 sparse / 32 dense)

2011 patch size range     1-500 flowering plants
dense definition          >5 flowering plants / m2
sparse definition         <2 flowering plants / m2.
```

Published pollination rates were:

```text
2005  63%
2011  90%.
```

The article-level ANOVA reports a strong density effect on final seed set
(F=39.025, df 1,2926) and seed predation (F=166.220, df 1,2926). These F
statistics are evidence of ecological structure, not portable effect sizes.

The 2011 density-by-patch-size analysis adds a sharper ecological contrast:

```text
initial seed set   density x size F = 44.556   df 1,2047
final seed set     density x size F =  0.023   df 1,2345
fruit predation    density x size F = 10.605   df 1,54
seed predation     density x size F =106.270   df 1,2345.
```

Thus the spatial context dependence of enemy pressure is very strong, while
the same interaction is essentially absent from final seed set. The paper's
post-hoc contrasts show a reversal of the patch-size association with
predation: at low density, small patches had greater predation than large
patches, whereas at high density seed predation was greater in large patches.
This is evidence that antagonist weight is a spatially conditional ecological
variable rather than a fixed population property. It is **not** evidence for a
randomized G effect and these F statistics are not used as portable effect
sizes.

The raw Dryad file is therefore the top recovery target because it may permit
direct reconstruction of seed-set and predation distributions rather than
using only article summaries.

### Current access limitation

The public Dryad v2 metadata API now resolves the file unambiguously:

```text
dataset id    11150
version id    11193
file id       46101
path          raw data.xlsx
size          89,597 bytes
MIME          application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
MD5           10a98383677bbd2a01e19a86c350fdd3
```

Metadata endpoints are anonymously readable, but the exact v2 binary download
endpoint `/api/v2/files/46101/download` currently returns HTTP 401 in the
available fetch environment. Thus the raw workbook has **not** been ingested
into the repository.

Metadata/URL discovery is now complete. The only useful next retrieval action
is a legitimate authenticated/session/library download of exact file 46101 (or
a user-provided copy), followed by MD5 verification and sheet/column/grain
audit. Do not claim raw-data reanalysis until those bytes are actually
retrieved.

## Sun & Huang 2015 — causal water-defence experiment

Article:

```text
Rainwater in cupulate bracts repels seed herbivores in a
bumblebee-pollinated subalpine flower
doi:10.1093/aobpla/plv019
```

Six populations were experimentally studied.

Seed experiment design:

```text
40-60 tagged individuals / population
mean 52.46 / population
20 dense subplots / population
20-30 water-drained individuals / population
>=6 capsules counted / individual.
```

Visitor experiment at Shama:

```text
10 dense plots
8-15 inflorescences / plot
5 drained + 5 intact plots
20-30 observation hours per year
30-minute censuses
2010 and 2011.
```

Reported treatment coefficients include:

```text
pollinator visit rate     beta  0.012   SE 0.224   P=0.958
nectar robber visit rate  beta -0.014   SE 0.225   P=0.951

initial seed set          beta  0.001   SE 0.006   P=0.906
final seed set            beta  0.025   SE 0.006   P<0.0001
seed predation            beta -0.072   SE 0.007   P<0.0001.
```

Site-specific reported seed-predation treatment coefficients were:

```text
Baishuitai  -0.104 +/- 0.014
Sanba       -0.144 +/- 0.015
Zhongdian   -0.093 +/- 0.348
Deqin       -0.035 +/- 0.017
Daxueshan   -0.084 +/- 0.017
Shama       -0.049 +/- 0.017.
```

These provide real experimental effect-scale and heterogeneity information.

However, water drainage is deliberately deprecated as the SCH independent G.
It is retained as an external effect/feasibility prior and BITA-y causal
precedent. It cannot directly freeze the independent predator-exclusion G.

## Sun, Armbruster & Huang 2016 — 14-population conflict dataset

Article:

```text
Geographic consistency and variation in conflicting selection generated by
pollinators and seed predators
doi:10.1093/aob/mcw097
```

Field design:

```text
14 populations for floral/pollination traits
12 populations for seed production/predation
16-36 plants / population
mean plants / population = 21.38 +/- 1.04 SE
two flowers from different whorls / plant
digital-caliper resolution = 0.1 mm.
```

Published pooled measurements:

```text
stigmatic pollen load  mean 12.53, SD 5.36
                      n=299 plants / 598 flowers

ovules / flower        mean 25.96, SD 6.33
                      n=120

capsules / plant       mean 12.51, SD 5.60.

linked-population GLM inputs:
pollen load             mean 12.28, SD 5.30
seed predation rate     mean 0.127, SD 0.120.
```

Across 12 populations:

```text
initial seed set  31.10-48.53%
seed predation      0.80-27.42%.
```

Seed-outcome sampling is described as usually six capsules from ~20
individuals per population (~120 fruits/population). In seven populations,
morphology/pollination and seed outcomes retained plant linkage, although
different flowers were usually used.

### Public supplements

PMC lists:

```text
supp_mcw097_aob-16074-s01.doc
supp_mcw097_aob-16074-s02.xls.
```

The supplements contain population locations, initial/final seed set and seed
predation for 12 populations, and means/SE for 12 phenotypic traits plus
pollination success in 14 populations.

The supplement identities are verified but the binary files have not yet been
ingested in the current environment.

### 2026 public-source distribution update

As of **August 26, 2026**, the legacy PMC FTP/OA article-dataset
distribution routes were removed. The official supported source for
eligible articles is now the **PMC Article Datasets public AWS S3 cloud**
and includes individually addressable supplementary files *when the
article's licensing and OA inclusion permit*. See the NCBI documentation:
https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/.

That migration is a new potential official *retrieval route*, not evidence
that `PMC4970362` is included in this public dataset or that either
specific supplemental object is available. This research session was
unable to retrieve the binary; **the supplement contents, exact
per-population n, and full row-level measurements remain unverified**.
Do not claim ingestion based only on the listed filenames, expected
cloud path pattern, or source abstract. Use the exact official metadata
and materialize source bytes before any analysis that needs those rows.

In the meantime, exact published Table 1 AICc and six-site 2015 GLM
treatment coefficients are reproducibly audited without inventing
underlying data. See
`SCH_PEDICULARIS_FITNESS_TRANSLATION_MOSAIC_V1.md` and
`SCH_PEDICULARIS_REAL_WORLD_ANTAGONIST_HETEROGENEITY_V1.md`.


## P. rex population-genetic mating context

Li, Gao & Wang (2005) surveyed five Yunnan P. rex populations
(Zhongdian, Lijiang, Dali, Wuding and Kunming; Zhongdian included three
subpopulations) with RAPD markers.

Published summaries are:

```text
polymorphic loci          82.0%
Shannon diversity I       0.361
Nei gene diversity h      0.240
Gst                       0.747.
```

The authors interpret the strong among-population differentiation as
potentially related to a mixed mating system with relatively high selfing.
That interpretation is retained as **population-genetic context only**:
`Gst=0.747` is not a selfing-rate estimate.

This is useful precisely because a later focal study reported very high
multilocus outcrossing in two patches. The two records together argue against
a single species-wide expected P1 effect or mating-state assumption.

## P. rex nectar dynamics and reproductive allocation

Liu et al. (2016; doi `10.1111/jipb.12374`) measured nectar production
through flower development in focal P. rex populations at Kunming, Lijiang and
Daocheng. Table 1 gives 13 exact stage/population rows with 4–6 flowers per row.

Across those rows the authors report:

```text
nectar volume                 1.13 ± 0.68 uL SD
nectar sugar concentration      33 ± 5 % SD
```

Individual rows span:

```text
volume   0.23–2.50 uL
sugar    26–41%.
```

This shows strong natural reward heterogeneity across population/stage and
explains why the separate 2007 P. rex report of 22% sugar should not be treated
as a universal species constant.

Yang & Guo (2007; doi `10.1111/j.1744-7909.2007.00398.x`) report for
P. rex subsp. rex:

```text
pollen–ovule ratio = 11222.04 ± 4887.18 SD.
```

These are focal reproductive/pollinator-reward context measurements. Neither is
a P1 supplementation effect or direct F0 value.

## Focal floral morphology and pollen-grain scale

Corbet & Huang (2014; doi `10.1093/aob/mcu195`) measured floral traits in
eight sympatric Pedicularis species and reports exact P. rex values:

```text
corolla tube length    23.43 ± 0.498 SEM mm   n=20 specimens
lower-lip width        12.71 ± 0.382 SEM mm   n=20 specimens
pollen-grain volume    4448  ± 89.28 SEM um3  n=20 plants
```

These measurements are focal natural-trait scale information. They can inform
whether a proposed P0 manipulation range is biologically extreme, but they do
not provide same-flower repeatability, measurement error or a manipulation
effect. The audit therefore keeps `SEM` as a separate uncertainty type rather
than silently merging it with SD/SE or using it as a CAL-A equivalence margin.

## Focal mating-system data

Jing Xia, Liu & Qin (2013; doi `10.1007/s00606-012-0701-x`) directly
estimated mating-system parameters in sparse and dense P. rex patches.

The primary abstract reports:

```text
sparse patch multilocus outcrossing   t_m = 1.151
dense patch multilocus outcrossing    t_m = 0.924
```

and states that reproductive outputs under hand and natural pollination were
also measured. A secondary thesis that cites this study reproduces the
outcrossing estimates as:

```text
1.151 ± 0.108
0.924 ± 0.042.
```

The uncertainty type of those ± values has not yet been verified in the
primary full text, so the ledger deliberately labels it
`SECONDARY_REPORTED_UNCERTAINTY_TYPE_UNVERIFIED` rather than SD or SE.

The same primary abstract reports a regression-derived theoretical maximum of
63 fruits per plant.

These results strengthen the focal natural-state conclusion that
self-compatibility does not imply predominantly selfed realized reproduction.
They remain mating-system/resource-context priors and are not the registered
P1 supplementation intervention.

## Older pollination data

Tang, Xie & Sun 2007 report a nectar sugar concentration of 22% for
`P. rex` subsp. `rex` (28% for subsp. `lipskyana`) and identify bumblebees as
effective pollinators.

Wang 1998 reports that seed production in studied P. rex populations depended
on bumblebee pollination. Indexed text did not expose a quantitative
supplementation effect.

These older records are retained as natural-history context, not P1
supplementation calibration.

## What published measurements can support

### CAL-A

Published data can support:

- external floral-trait variation;
- historical device resolution (0.1 mm calipers);
- field-feasibility/sample-size context.

They do **not** supply same-flower repeatability for the registered P0 metrics
or a graded z-manipulation with off-target measurements.

### CAL-B

Published data can support:

- baseline pollen/seed/predation scales;
- experimental seed-predation effect plausibility;
- evidence that a water intervention can change predation without a detected
  visitor-rate effect;
- natural among-population predation heterogeneity.

They do **not** supply the registered P1 supplementation effect or an
independent seed-predator-exclusion G with water-y fixed.

### CAL-C

Published data can support:

- historical SDs where directly reported;
- sample-size/replication feasibility;
- external variance and assumed-effect scenarios once the raw Dryad data or
  supplementary tables are recovered.

The 2016 linked-population analysis directly reports plant-level marginal SDs
for pollen load (5.30 grains) and seed predation (0.120 proportion). Because
the registered P1/G designs are paired, the unknown within-pair correlation is
kept explicit rather than pretending these are paired-difference SDs.

Under equal marginal variances,

```text
sd_delta = sd_marginal * sqrt(2 * (1-rho)).
```

For rho = 0, 0.25, 0.50, 0.75 this gives:

```text
P1 pollen delta SD      7.495, 6.491, 5.300, 3.748 grains
G predation delta SD    0.170, 0.147, 0.120, 0.085 proportion.
```

These are external CAL-C sensitivity scenarios only. They are generated by
`scripts/build_pedicularis_published_cal_c_sd_scenarios.py` and must not be
written into the CAL-C criterion table as observed pilot SD.

Model-coefficient SE is not silently converted into raw-data SD.

## Direct F0 boundary

Current recovery result:

```text
published source records         10
published measurement rows       77
direct F0 gate values recovered   0.
```

This is intentional.

Historical measurements are external priors. They do not share the same
prospectively registered population/season/intervention package as the current
confirmatory P0/P1/G chain.

## Remaining direct empirical gaps

Even after this recovery, the following remain unmeasured in the registered
form:

```text
same-flower repeatability for registered P0 metrics
multi-level P. rex z manipulation + off-target checks
P. rex pollen supplementation effect
independent seed-predator exclusion with water-y fixed
qualified independent-G timing window in P. rex.
```

## Next recovery order

1. Retrieve and inspect Dryad `10.5061/dryad.6cv06/raw data.xlsx`.
2. Retrieve the 2016 `mcw097` supplementary XLS/DOC files.
3. Recompute only estimands supported by actual columns/grain in those files.
4. Feed any usable historical SD/effect information into external-prior
   scenarios for CAL-A/B/C, never directly into F0 without prospective
   justification.

## Claim ceiling

Published-data recovery can reduce uncertainty and field-design arbitrariness.
It cannot convert historical observational or differently manipulated data
into the missing same-context causal Pedicularis experiment.
