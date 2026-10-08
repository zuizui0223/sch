# Biological evidence from real Pedicularis rex population differences — October 8 source audit

## Question

In a multifunctional flower protected by water-bearing cupulate bracts,
is antagonist protection equally valuable across local environments?
Can geographical differences in predation be dismissed as artifacts of
capsules whose contents were completely destroyed?

Both questions can be **bounded with reported numbers from actual field
studies**. Neither requires treating unobserved flower-level data as measured.

**Sources**

- Sun & Huang (2015), *AoB PLANTS*, doi:10.1093/aobpla/plv019, Tables 1–2
  (experimental puncture-plus-drainage, six populations).
- Sun, Armbruster & Huang (2016), *Annals of Botany*, doi:10.1093/aob/mcw097,
  Methods and Results (observational predation extremes; up to five fully
  consumed capsules per population not scorable).
- Official 2026 PMC data-service migration:
  https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/.

## A. Real 2015 intervention: the defense response varies across sites

All six focal sites show the **same sign** of the original model's water
treatment coefficient. They are *not* six independent research studies:
they are sites within **one** 2015 experiment. The original fitted
site × treatment interaction was significant: χ² = 36.782, df = 5,
P < 0.0001.

The source reports:

| Population | Source GLM treatment β | SE | Original paper's site result |
|---|---:|---:|---|
| Baishuitai | −0.104 | 0.014 | P < 0.0001 |
| Sanba | −0.144 | 0.015 | P < 0.0001 |
| Zhongdian | −0.093 | 0.348 | P = 0.789 |
| Deqin | −0.035 | 0.017 | P = 0.046 |
| Daxueshan | −0.084 | 0.017 | P < 0.0001 |
| Shama | −0.049 | 0.017 | P = 0.005 |

**Independent source-table arithmetic from the six site coefficient/SE
pairs** (not a re-fit to plant/capsule data):

- Reported model-scale β spans **0.109 units** (−0.144 to −0.035). This
  is **not** an absolute predation risk difference or a fold change.
- Inverse-variance heterogeneity Q = **30.282**, df = 5; descriptive
  I² = **0.835**. I² is very uncertain at six sites and is a function
  of the reported SE/model, not a trait-level biological constant.
- DerSimonian–Laird model-scale between-site SD τ ≈ **0.040**.
  Its approximate inverse-variance random-effect mean is **−0.0839**,
  but this is a sensitivity description, **not** a transportable
  species-wide effect estimate or calibrated small-k confidence interval.
- Zhongdian's listed SE = 0.348 is **20.47 times** the median
  SE = 0.017 of the other five. Dropping this site changes the
  approximate pooled estimate from −0.08386 to −0.08381.
  The heterogeneity does not depend on treating Zhongdian as a
  no-effect or reversed-effect site.

**Ecological interpretation:** what is causally established by the
published experiment is the nonuniform *treatment-package*
consequence for seed predation. The package included a hole punctured
in the cupulate bract **plus water drainage**, not cleanly separated
liquid-water removal. This source cannot identify whether population
heterogeneity arises from environmental variation in water levels,
enemy behavior, bract injury, predator guilds, or oviposition geometry.
The pollinator-visit comparison was conducted at Shama only, and
P = 0.958 is **not proof of pollinator unaffectedness everywhere**.

A productive new hypothesis is therefore **spatial turnover in the
fitness return to a protection mechanism, even while an exposed floral
trait performs a similar pollination role**. Testing that requires
within-population randomized exsertion × truly independent predator
manipulation, not another source-level fitted coefficient.

## B. 2016 severe-attack missingness: what can and cannot explain it

Sun et al. (2016) reported seed predation **0.80% in population 11**
and **27.42% in population 5**. They also explain that the contents
of up to **five capsules per population** were completely consumed,
making seed number unknowable; these capsules were not used in the
seed-count analysis.

This is potentially **outcome-dependent missingness**, not random
dropout. It could make local rates of predation look too small,
especially at the low end. Since the precise per-population number
of assessed and excluded fruits and the aggregation weights are
unavailable, there is **no defensible corrected estimate**.

One purely conditional sensitivity question can nevertheless be
answered analytically. Suppose a published percentage is the
**unweighted mean** of predation fractions from `n` assessable
capsules, and `m` additional capsules have unknown predation
fractions between zero and one. Then the corrected mean must satisfy

```text
n*p_obs/(n+m) <= p_all <= (n*p_obs + m)/(n+m).
```

If both extreme populations had **115 assessable capsules and five
unscorable capsules each** (scenario, **not observed n**):

- low reported site 0.80% → bound **0.767% to 4.933%**;
- high reported site 27.42% → bound **26.278% to 30.444%**;
- even the worst-case corrected high-minus-low contrast remains
  **21.344 percentage points**.

More generally, under the *same equal-capsule-mean model*, each
site's assessable sample ≥ **19 capsules** and ≤ 5 missing capsules
is sufficient to preserve the sign of this particular high-minus-low
contrast. For 18 or fewer, the worst-case envelope can overlap.
The paper's usual field design mentions about 120 capsules per site;
**this is not an independently verified analyzed denominator**.

**No empirical rank correction is implied.** The population rate
might be a mean of plant-level means rather than a direct capsule
mean; the case of a completely unrecognizable consumed seed has an
ambiguous initial-seed denominator; and per-population observed n
and missing m were not recovered. Consequently, the 19-capsule
result is a conditional **sensitivity benchmark**, not a new
source-derived confidence interval or proof of complete robustness.

## What this changes for SCH

The biological distinction becomes more concrete:

1. **Antagonist pressure / defence payoff can differ strongly in
   space**, directly shown at the population-treatment level in 2015,
   without first demonstrating that different insects prefer
   different floral protrusions.
2. Large published geographic predation contrasts are **not
   automatically explained away** by a few entirely destroyed
   fruits when realistic capsule numbers and the stated
   equal-weight aggregation assumption hold.
3. Neither result establishes **the slope of predator-induced
   selection on experimentally randomized floral exsertion**,
   *pure-function* optima, SCH compromise `L`, or architectural
   separation. Source studies involve different years,
   observational/experimental contrasts, and units.

The next genuinely biological measurement remains a joint local
design that separates **attack incidence, seed development,
complete fruit destruction, surviving fitness**, and how these
responses move across assigned and realized floral geometry.

## Current public raw-data access boundary (2026)

The previous PMC FTP/OA-service routes were discontinued in **August
2026**. NCBI now documents individual supplemental files in its
public S3 bucket (`pmc-oa-opendata`) for articles available in the
qualifying dataset, with file visibility depending on the article
license. The old PMC-source file identities in this repo are
legitimate leads, but the legacy URLs should not be assumed live.

Official cloud documentation:
https://pmc.ncbi.nlm.nih.gov/tools/pmcaws/

**Not verified:** whether PMC4970362 is distributed within the
2026 cloud dataset and, if so, whether its
`supp_mcw097_aob-16074-s02.xls` and
`supp_mcw097_aob-16074-s01.doc` objects are accessible.
The current research environment did not obtain either binary.
No downloaded file checksum, workbook row, or model fitted to raw
supplements is claimed. The source Dryad 2013 file 46101 remains
unretrieved as well.

## Reproducible files

```text
scripts/audit_pedicularis_2015_site_heterogeneity.py
scripts/audit_pedicularis_2016_censored_predation_bounds.py
tests/test_pedicularis_source_backed_heterogeneity.py
```

Both source-facing scripts read or use only the frozen published
measurements already recorded in the repo; regression tests guard
against changed coefficients, confused units, and unsupported
promotions.

Related:
`SCH_PEDICULARIS_WATERLINE_ACCESS_MECHANISM_V1.md`,
`SCH_PEDICULARIS_FITNESS_TRANSLATION_MOSAIC_V1.md`.
