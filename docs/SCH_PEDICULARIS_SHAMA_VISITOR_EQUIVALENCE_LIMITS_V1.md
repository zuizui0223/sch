# P. rex: absence of a visitation effect is not proof of a selective defence axis

## Why this changes the ecological claim

Sun & Huang (2015; doi:10.1093/aobpla/plv019) provides strong experimental evidence that a combined **bract puncture-plus-drainage** intervention changes seed predation. The same study found no statistically significant effect on pollinator visitation, but its visitation assay covered **Shama only**. This is useful evidence for a defence-*biased* response; it is insufficient to certify selective functional loading, negligible mutualist cost, or biological equivalence.

Original Table 1 reports a binomial/logit GLM with YEAR, TREATMENT, and YEAR x TREATMENT terms. This companion reads the six original coefficients, not invented plot data. The model's TREATMENT coefficient is **not** a separately established treatment effect averaged across years, because interaction coding and joint covariance are unavailable.

## Source-reported model terms, and independently calculated uncertainty

The source's Shama TREATMENT terms are:

| Shama visitor endpoint | β | Source SE | Source P | Approximate model-based 90% Wald interval | 95% Wald interval |
|---|---:|---:|---:|---:|---:|
| Legitimate pollinator visits | 0.012 | 0.224 | 0.958 | [−0.35645, 0.38045] | [−0.42703, 0.45103] |
| Nectar robber visits | −0.014 | 0.225 | 0.951 | [−0.38409, 0.35609] | [−0.45499, 0.42699] |

These intervals are independently calculated as beta ± z times published SE, at z=1.64485 for 90% and z=1.95996 for 95%. They are *diagnostic normal-approximation Wald intervals* on the original logit coefficient scale, NOT printed confidence intervals from the article or cluster-robust reanalysis of its underlying plots.

### What a valid equivalence claim would require

An ordinary two-one-sided test (TOST) of a single coefficient at alpha=0.05 requires its 90% CI to be contained inside an **independently predeclared, biologically meaningful** symmetric [−Delta, +Delta] equivalence region.

From printed Table 1 alone, the **smallest possible numeric symmetric margin** for the pollinator treatment term is just above **0.38045 logit-coefficient units**; for the robber term it is just above **0.38409**. Any stricter margin cannot contain these 90% intervals. Choosing the margin *after* seeing these data is invalid for confirmatory equivalence.

Crucially, the model also contains YEAR x TREATMENT interactions:

| Endpoint | Interaction β | SE | Source P | 90% Wald interval | Smallest numeric symmetric margin |
|---|---:|---:|---:|---:|---:|
| Pollinator visits | −0.099 | 0.451 | 0.823 | [−0.84083, 0.64283] | 0.84083 |
| Nectar robber visits | 0.117 | 0.444 | 0.792 | [−0.61332, 0.84732] | 0.84732 |

The large intervals do not show absence of year-specific differences. The covariance of the treatment and year-interaction coefficients and the model's precise coding are not recovered; combining them into a claimed two-year marginal causal effect and CI is NOT licensed.

No meaningful prospective equivalence threshold, plot-cluster standard error audit, or six-site visitation transport is available. Therefore **this is not a field-validated equivalence test**, and neither non-significant P is evidence of a zero, tiny or selectively neutral pollinator response.

## Separating real ecological evidence from architecture promotion

**Supported:** The combined bract puncture-and-drain treatment changed seed predation across the six original populations. The source also detected a pooled final-seed response, and a site x treatment interaction for seed predation. Shama's visitor GLM did not reject a zero visitor-treatment term on its reported scale.

**Not supported:** Water-only causality, a pollinator-equivalent y axis across six populations, unchanged pollen receipt or pollination service, unchanged visitor behavior at all times, confirmed lack of physiological damage, or a formal BITA preferential-functional-loading estimand. Even the local Shama visitor CI is wide on its own model scale. It would be invalid to compare absolute effect sizes of source visitor versus predation coefficients directly when links/units/covariances differ.

The biological prediction remains worthwhile: **a protective bract-water mechanism could disproportionately reduce seed predator exposure without proportionately reducing pollination**, but this must be tested in the *same focal population and season* with independently validated water-only and mechanical-damage controls, source-matched pollinator service and viable-seed outcomes, and a prospective equivalence margin.

For SCH, natural corolla exsertion is still associated with pollen receipt and seed predation in the separate 2016 *P. rex* study, but 2015 does not qualify the registered water-fixed independent predator G or a crossed z x P x G experiment. For BITA/SLK, treat preferential loading and architecture value as **NOT IDENTIFIED**, not rescued by P=0.958.

## Source and technical provenance

- Primary study: Sun & Huang (2015), *Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower*. https://academic.oup.com/aobpla/article/doi/10.1093/aobpla/plv019/200213, Tables 1–2, Methods (visitation study at Shama, 2010–2011).
- Original six-row source transcription: data/PEDICULARIS_2015_SHAMA_VISITOR_TABLE1_V1.csv.
- Source-locked computation: scripts/audit_pedicularis_2015_shama_visitor_equivalence.py.
- Regression tests: tests/test_pedicularis_2015_shama_visitor_equivalence.py.

Execute:

    python scripts/audit_pedicularis_2015_shama_visitor_equivalence.py

This program does **not** estimate causal treatment effects from raw observations, recover covariance, perform posthoc equivalence tests, certify data independence, or promote any SCH/BITA/SLK quantity. It reports the numeric model-scale uncertainty implied by the source coefficient and its SE with all inferential restrictions explicit.
