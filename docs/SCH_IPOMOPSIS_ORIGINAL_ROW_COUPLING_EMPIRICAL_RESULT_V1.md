# Independent ecological reanalysis of original Ipomopsis plant-level observations

## This is new computation on public source rows, not another literature tally

**Question.** Does plant-level coupling between early seed production and subsequent fruit escape from predispersal seed predation change the apparent effect of floral width, even when the two reproductive stages have similar independent marginal patterns?

This analysis uses publicly archived **original data**, not coefficients copied from a published paper. Source:

- Campbell, Bischoff, Raguso, Briggs & Sosenski (2021 Dryad dataset; source paper 2022), doi **10.7280/D1KM49**; original article doi **10.1086/716740**.
- Full openly available 437-row file: https://zenodo.org/records/5083399/files/Selection_by_pollinators_and_predators.csv?download=1
- Original variable dictionary: https://zenodo.org/records/5083399/files/ReadMe_Selection_by_pollinators_and_predators.csv?download=1
- Verified MD5 original raw file **12ed3dbe6d269c5f808f9c6b230d468c**; original dictionary **e681a5a0885271c4797730b5a30574d8**.
- Exact 437-source-row ingestion: scripts/ingest_sch_ipomopsis_public_raw.py.
- Actual statistical test: scripts/analyze_sch_ipomopsis_primary_coupling.py.
- Verified run + data artifacts: https://github.com/zuizui0223/sch/actions/workflows/sch_ipomopsis_original_raw.yml.
- Frozen numerical inference: data/SCH_IPOMOPSIS_REAL_RAW_STAGE_COUPLING_RESULT_V1.json.

**Do not confuse this with a new field experiment.** The data were collected by the original authors. The scientific contribution here is a distinct, reproducible, postpublication exploratory **independent raw-row analysis**, still requiring replication elsewhere.

## Biological and observation-grain adjudication (completed BEFORE fitting coupling)

Original file: 437 rows, 12 fields, source-coded sites agg/hyb/ten, years 2010–2018, plant type A/H/T (I. aggregata, hybrids, I. tenuituba, respectively). Source dictionary states **hyb and ten were combined into an upper site**; the three printed Site codes must not be treated as three independently randomized study sites.

The reproductive variables are:

- seedsinit = **total estimated seeds initiated**, whether eaten or not;
- flyescape = **proportion of fruits that escaped seed predation** — not a seed-survival fraction;
- seeds = **reported total seeds** — not necessarily numerically equal to seedsinit multiplied by flyescape.

**Observed source audit:** 375/437 rows have both initiation and fruit escape and a reported final seed value. In 40/375, the reported total-seed estimate is greater than reported initiated-seed estimate. There are only 27 exact matches of seedsinit × fruit_escape to seeds, and their median absolute difference is approximately **0.4803** original seed units. Therefore, this data set is not an exact count-level identity for initiated/damaged/mature seeds, and the prior synthetic demonstration of F = I(1−q) cannot be plugged into these rows as if fruits and seeds were interchangeable.

For stage-coupling inference, predeclare the exact source stratum as Site × Year × Type, retain cohorts with >=8 complete initiation + fruit-escape measurements, and give each eligible original cohort **one equal weight** rather than treating all rows as independent ecological communities. That leaves **15 cohorts / 297 matched source rows** across **eight eligible year blocks (2011–2018)**. The secondary width analysis retains 15 cohorts / **277 rows** after missing width values and exact-median-width ties.

## Primary original empirical test: is stage coupling detectable across eligible strata?

For each cohort g, set Irelative_i = seedsinit_i / mean(seedsinit within g) and e_i = flyescape_i. Define

    C_g = mean(Irelative_i * e_i) − mean(e_i)
        = covariance_pop(Irelative, e) within g.

This is an exact finite-row decomposition of the **early-seed × fruit-escape proxy**, not final mature seed fitness. C_g > 0 means disproportionately high initiating plants have higher fruit-escape fractions, and C_g < 0 means high initiating plants tend to have lower escape fractions. No implication of causation or pollinator preference is asserted.

Registered before viewing the cohort-specific coefficients: T = mean(C_g) across all 15 eligible cohorts (equal cohort weight). Under a conditional within-cohort exchangeability null, randomly permute observed escape values **within the same source Site × Year × Type**, keeping all original initiation marginals fixed. Seed fixed to 20261028; **4,999 Monte Carlo permutations**.

**Actual archived-row result:**

    T (average normalized initiation–fruit escape covariance)  = −0.014898
    two-sided within-cohort permutation P                     =  0.1020
    Bonferroni two-test family adjusted P                     =  0.2040
    exploratory year-block bootstrap 95% interval             = [−0.02921, +0.00084]

The point direction is **negative** but a null of zero conditional coupling is NOT rejected at the declared two-test family threshold. The eligible years are only eight, and the block-bootstrap interval reaches zero. We cannot claim a general tendency for seed-initiation investment to incur higher predation or stage-level functional conflict.

Descriptive stratum means of C_g: Site agg ≈−0.01243 across 8 cohorts (n=173 original matched rows); Site hyb ≈−0.02353 across 5 (n=92); Site ten ≈−0.00320 across 2 (n=32). These are **not** independently validated differences between habitats, ecological types or natural species. Site codes and genotype composition are interdependent.

## Secondary test: does coupling change the apparent corolla-width contrast?

Within each eligible original cohort, split each plant into higher or lower corolla width than its own cohort median; omit exact-median ties rather than arbitrarily assigning equal widths to opposite categories. Require at least three matched original rows on both sides. Normalize initiated seeds by the *full within-cohort width-complete mean*. Then the **finite-sample identity**

    Δ mean(Irelative × e)
    = Δ [mean(Irelative) × mean(e)]
      + Δ covariance_pop(Irelative, e)

separates the difference in the matched-stage **proxy** from a comparison that uses two independently paired within-width marginals. Positive/negative Δ refers only to the source proxy, not directly to final seeds.

Test the width-specific covariance difference with **4,999 independent permutations of fruit escape *within* each fixed width bin and source cohort**, retaining all observed width-specific marginals.

**Actual archived-row result:**

    equal-cohort average Δ covariance (high width − low)  = −0.019130
    two-sided conditional permutation P                  =  0.2566
    Bonferroni two-test family adjusted P                =  0.5132
    exploratory year-block bootstrap 95% interval        = [−0.03930, +0.01285]

Not supported as a different coupling response across width bins. None of the **15** eligible source cohorts showed an actual sign inversion between the raw proxy high-minus-low response and the independent-marginal prediction. The sign of the source-reported **final seeds** width contrast agreed with the proxy contrast in all **15/15** eligible cohorts, but this is **descriptive and not an independent fitness-pathway test**: all endpoints are from the same source estimate pipeline, and the proxy is not source-confirmed to be a seed survival identity.

## What is and is not a new biological result?

**Genuinely new source-row calculation:** the hypothesis that initiation–escape covariance creates a detectable additional cohort-average selection component receives **no support** in this first archived Ipomopsis system under the registered source-stratified tests. The theory demonstrates a mathematical possibility, not a ubiquitous empirical process. This is an informative **negative, limited-scope original reanalysis**. It should not be promoted as a broadly positive ecological law.

**Still open:** whether stage coupling changes net selection for other floral traits, more species, true seed-fate-level samples, or new independently measured and randomly assigned traits; whether fruit escape and seed survival differ systematically; and whether selective consumer manipulation shifts the *causal* reproductive optimum.

**Not estimated:** SCH shared-trait compromise loss L, pure function-specific optima, SLK architecture value, historical splitting or a multi-species macroecological effect.

## Workflow and reproducibility

Run on a network-enabled execution environment:

    python scripts/ingest_sch_ipomopsis_public_raw.py --outdir artifacts/ipomopsis_original_ingress
    python scripts/audit_sch_ipomopsis_source_grain.py --source artifacts/ipomopsis_original_ingress/Selection_by_pollinators_and_predators.csv
    python -m scripts.analyze_sch_ipomopsis_primary_coupling --source artifacts/ipomopsis_original_ingress/Selection_by_pollinators_and_predators.csv --output artifacts/ipomopsis_original_ingress/original_stage_coupling_permutation_result.json

GitHub Actions workflow: .github/workflows/sch_ipomopsis_original_raw.yml.

Source and dataset artifacts are verified against the original MD5, not imputed, and preserved as short-lived GitHub Action artifacts (can be re-fetched automatically). A committed JSON result in data/ permanently documents the verified run receipt. Statistical source code and tests are retained in git, so a later source drift or inference change must be visible.

**Next science-first extension:** rather than add more literature-source examples, run the same explicit early-stage/late-stage coupling question on a separately sampled raw public system or independently collected *Pedicularis* seed-fate observations. The Ipomopsis result alone does not validate or refute universal theory.
