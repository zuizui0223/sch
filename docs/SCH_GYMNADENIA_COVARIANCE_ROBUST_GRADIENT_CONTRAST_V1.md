# A covariance-free lower bound on a genuine ecological-context gradient change

## Key correction to SCH PR #207

The claim "the published Gymnadenia treatment-cell beta SEs cannot say
anything about the *difference* between two treatment effects because their
covariance is unavailable" was **too restrictive**. The covariance is
needed for the *exact* contrast SE, but not necessarily to certify a
large enough difference's **direction** under a conditional normal-Wald
model.

The original `Gymnadenia conopsea` experimental source is Sletvold,
Moritz & Ågren (2015), *Ecology* 96:214–221,
DOI `10.1890/14-0119.1`; source data are Ecological Archives
E096-022 Appendix A, Table A2, independently frozen as 20
treatment-cell gradient β/SE observations in SCH.

In the two groups where herbivores were excluded,
only pollination was changed:

| Source cell | Gradient on flowering start | Reported SE | Source original significance |
|---|---:|---:|---|
| Open pollination, herbivores excluded (C+E) | +0.094 | 0.031 | P<0.01 |
| Supplemental hand pollination, herbivores excluded (HP+E) | −0.066 | 0.028 | P<0.05 |

The effect of moving from C+E to HP+E is **−0.160** β units,
not a raw fitness percentage and not a claim that floral phenotype
itself was randomized.

## Worst-case covariance bound, not a guessed correlation

For any two estimators with valid SEs `s_A,s_B` and arbitrary covariance:

```text
Var(beta_B - beta_A)
  = s_A² + s_B² - 2 Cov(beta_A,beta_B).

|Cov(beta_A,beta_B)| <= s_A*s_B

=> |s_A-s_B| <= SE(beta_B-beta_A) <= s_A+s_B.
```

The upper bound is **sharp**: it is attained when the errors
have correlation −1. No assumption of zero correlation or
fabricated source covariance is needed to get the upper bound.

For flowering start:

```text
delta beta (HP+E minus C+E) = -0.160
maximum possible contrast SE  = 0.031 + 0.028 = 0.059

minimum absolute Wald z       = 0.160/0.059 = 2.712
maximum nominal normal p      = 2*(1-Phi(2.712)) ≈ 0.0067

conservative 95% interval     ≈ [-0.276,-0.044]
conservative 99% interval     ≈ [-0.312,-0.008]
```

**Interpretation:** conditional on the original cell SEs being valid,
comparable and joint-asymptotically-normal estimators, zero is excluded
from even the **99% covariance-worst-case** normal interval. The exact
contrast SE and exact p remain unknown; the calculation supplies
a **conservative upper bound** on nominal p, not a published author's
ANCOVA contrast or an exact finite-sample procedure.

This is a stronger piece of causal-*context* evidence than inferring
the comparison solely because both individual cell gradients have
source-significant opposite signs. It remains
**phenotypic selection under experimentally manipulated consumer
regimes**, not direct experimental manipulation of flowering time.

## Why multiple comparisons still matter

The full frozen Appendix A has **five traits and four one-factor
comparisons per trait**, i.e. 20 possible exploratory edges.

The same conservative two-sided p upper bound is roughly
`0.0067` for the supported flowering-time contrast.
As sensitivity:

- nominal 5% and 1% **single-edge** thresholds: passes;
- four-edge within-flowering-time Bonferroni upper p ≈ `0.027`
  (passes at 5%, but these four edges were not a prospective family);
- **20-edge exploratory-family Bonferroni upper p ≈ 0.134**.
  This conservative bound does **not** certify family-wise
  significance at 5% across all 20 examined edges.

A bound failing the family threshold is *not* proof that the
actual Bonferroni p would fail. It means the source SEs without
covariance are insufficient to **guarantee** that stronger statement
under worst-case dependence. This is **not** a randomized holdout
or an independent replication; all 20 edges belong to **one
published factorial experiment**.

The spur-length point reversal along the same comparison is
`−0.119` with upper possible SE `0.064`, so its conservative
95% interval crosses zero. It cannot be promoted from
an unsupported negative cell to a second sharp reversible axis.

## Why the additive interaction remains unresolved

The **four-cell interaction** for flowering-time β is the
difference in differences:

```text
D = beta_C+H - beta_C+E - beta_HP+H + beta_HP+E
  = -0.0042.
```

The conservative arbitrary-covariance upper bound is now the
sum of **four** source SEs:

```text
SE(D) <= 0.054 + 0.031 + 0.056 + 0.028 = 0.169.
```

This does not certify an interaction, and it **does not certify
equivalence to zero**. The authors' conclusion that animal
effects were largely additive has independent full-paper
support, but the recovered Appendix table alone cannot
estimate an equivalence band or recover the original factorial
ANCOVA interaction p.

Crucially:

```text
strong covariance-robust one-factor sign change
    != strong evidence of a nonadditive interaction
    != different animal preferences
    != pure-function optimum displacement
    != SLK architecture value.
```

## Biological implication

The same experimental population contains two kinds of
multifunctional floral trait responses:

- flowering time: pollinators favor later flowering and
  herbivores favor earlier flowering, permitting strong **net
  selection sign turnover** with one manipulated input;
- spur length: both agents can select longer spurs, so changes
  in the same two environmental factors do not yield
  two individually supported opposite-sign net gradients.

Thus **ecological context alone does not specify evolutionary
response geometry; the trait coordinate and its baseline
fitness relations matter**. That inference comes from the
same five-trait source, not from treating five axes as five
independent systems.

The empirical result is bounded and already in the
published 2015 source. This new work improves what is
*provable from reported uncertainty*, while correcting the
earlier overly categorical covariance limitation.

## Exact reproducibility

```sh
python scripts/audit_sch_gymnadenia_covariance_robust_contrasts.py
python -m pytest -q tests/test_sch_gymnadenia_covariance_robust_contrasts.py
```

The script reads the same original A2 20 rows, computes all 20
single-factor contrast intervals and the five additive interaction
point residual bounds, and reports exploratory multiplicity
limitations separately. It does not silently change V11/V26/V27
source-programme classifications or registered held-out outcomes.
