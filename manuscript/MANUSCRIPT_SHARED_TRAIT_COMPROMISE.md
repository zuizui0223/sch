# Multifunctionality is not functional conflict: identifying compromise on a shared trait axis

**Canonical SCH full-paper science source**

**Target class:** conceptual / methodological ecology

## Abstract

Multifunctional floral traits are often called compromises, yet shared use does not establish opposing functional demands. We distinguish conflict-compatible observations from causal state-specific fitness optima and pure-function optima. A source-adjudicated synthesis of 16 independent biological systems recovered five conflict-compatible signatures, seven context-weight shifts, and two aligned multifunctional controls; purposive study selection precludes prevalence inference. Published interventions reveal distinct ecological pathways. In *Gymnadenia conopsea*, flowering-time selection changes sign with pollen supplementation while herbivory is held excluded. Across four published pollination programmes, point-estimate reversals outnumber statistically supported contrasts, and their guarantees depend on multiplicity and source precision. In *Lythrum salicaria*, apical clipping increases mean inflorescence number while weakening selection for further inflorescences. In *Brassica rapa*, floral cues associated with pollinator visits and herbivore oviposition retain positive net seed-fitness selection. *Pedicularis rex* links pollen receipt and predation to floral exsertion but lacks a single identifying factorial experiment. These results show that receiver behavior, developmental responses, and reproductive-stage survival can reshape selection differently. We specify which selective trait-by-consumer interventions would identify a causal compromise without mistaking observed ecological-state optima for pure-function optima.

**Keywords:** multifunctionality; functional conflict; compromise; causal identification; trait optimum; literature synthesis; crossed intervention; promotion gate

## 1. Introduction

A trait can perform more than one ecological function without being under conflict. A floral signal can affect pollinators and antagonists while both favor the same signal state. A structure can contribute to two performance tasks whose optima coincide. A chemical can influence several partners without those pathways pulling phenotype in opposite directions. Multifunctionality is therefore evidence that a coordinate matters to several functions; it is not evidence that those functions impose opposing geometry.

This distinction is often blurred because compromise language is attractive. Once two functions are attached to one trait, an intermediate phenotype is readily interpreted as a trade-off. But an intermediate observation can arise from direct trait costs, environmental context, background pathways, asymmetric weights, or incomplete exploration of the trait surface. A causal compromise claim requires more.

A second inferential problem appears after a crossed experiment. Suppose pollinator-present and antagonist-present conditions favor different trait states. Those optima are real empirical quantities, but they are optima of reproductive states, not automatically optima of pure functional objectives. Direct/background effects of the trait can remain under either condition. Relabelling state-specific optima as pure function optima silently strengthens the claim beyond the design.

SCH addresses these two promotion errors:

```text
multifunctionality
!= identified functional conflict

state-specific reproductive optimum
!= pure-function optimum
```

The paper therefore asks a methodological question: **what evidence is required to promote a multifunctional trait from “serves several functions” to “is causally constrained by opposing functional demands,” and what additional evidence is required to promote context-specific reproductive optima to pure-function optima?**

The empirical strategy mirrors that hierarchy. We first establish the mathematical and identification mechanism, then ask whether its observable signatures recur across independent biological systems, including systems in which multifunctionality is present but conflict is not recovered. Only after that cross-system map is assembled do we reserve a focal experiment for the quantities that existing studies structurally fail to identify.

## 2. Theory target and empirical target are different objects

Let one trait coordinate \(z\) contribute to two theoretical functional objectives,

\[
F_1(z),\qquad F_2(z),
\]

with pure optima

\[
z_{F1}^*=\arg\max F_1(z),\qquad
z_{F2}^*=\arg\max F_2(z).
\]

Theory-level conflict exists when

\[
z_{F1}^*\neq z_{F2}^*.
\]

A simple total-fitness representation is

\[
W_{shared}(z)=w_1F_1(z)+w_2F_2(z)-C(z),
\]

where \(C(z)\) collects direct or background consequences not assigned to either focal function.

Near pure optima, a quadratic benchmark is

\[
L_{shared}(z)=a(z-z_{F1}^*)^2+b(z-z_{F2}^*)^2.
\]

The idealized one-axis mismatch penalty at the shared optimum is

\[
L^*_{compromise,theory}
=\frac{ab}{a+b}(z_{F1}^*-z_{F2}^*)^2.
\]

This formula is useful as a theory benchmark and as an upstream quantity for the SLK framework. It is **not** a licence to substitute experimentally observed context optima for \(z_{F1}^*\) and \(z_{F2}^*\).

## 3. What the crossed experiment directly identifies

Manipulate the same trait coordinate \(z\) across several levels and cross it with selective pollinator and antagonist states. Denote the reproductive surfaces

\[
W_{00}(z)=P_0G_0,
\]

\[
W_{10}(z)=P_1G_0,
\]

\[
W_{01}(z)=P_0G_1,
\]

\[
W_{11}(z)=P_1G_1.
\]

The directly identified state-specific optima are

\[
z_P^*=\arg\max W_{10}(z),
\]

\[
z_G^*=\arg\max W_{01}(z),
\]

\[
z_C^*=\arg\max W_{11}(z).
\]

These are reproductive optima under declared ecological states. In general,

\[
z_P^*\neq z_{F1}^*,\qquad z_G^*\neq z_{F2}^*.
\]

The reason is simple. Even when antagonists are removed, direct/background consequences of \(z\) can remain in \(W_{10}\). Likewise, pollinator removal does not guarantee that \(W_{01}\) equals a pure antagonist objective. The experiment identifies what it manipulates; it does not identify absent pathways by naming them away.

This distinction is the first major claim boundary of SCH.

## 4. A promotion ladder for functional conflict

SCH uses an ordered inference ladder rather than a binary “trade-off present / absent” label.

### Level 0 — multifunctionality

The same declared coordinate affects more than one ecological or functional route. This is necessary background but not conflict.

### Level 1 — local functional conflict

The focal functions exert opposing causal effects on the value of the same trait contrast. For a binary attraction contrast \(A\), one useful crossed design is

```text
A × antagonist × pollinator
```

on a common reproductive outcome. If changing pollinator state increases the reproductive value of \(A\) while changing antagonist state decreases it, the same contrast is locally conflicted.

A local contrast does not locate the full compromise optimum. It only establishes opposing causal geometry near the tested contrast.

### Level 2 — state-specific compromise geometry

A multi-level \(z\) experiment identifies distinct state-specific optima and a combined surface. The minimum geometry requires

\[
z_P^*\neq z_G^*,
\]

plus a supported interior optimum \(z_C^*\) over the tested range.

An interior combined optimum is not enough by itself; it could arise without the focal consumers generating the apparent balance.

### Level 3 — causal compromise

The combined optimum must move predictably when each functional demand is selectively removed:

```text
G off  → optimum shifts toward z_P*
P off  → optimum shifts toward z_G*
```

and the functional-component gradients near \(z_C^*\) must be non-zero and opposed.

The zero derivative of an interior fitted curve at its own vertex is not counted as independent evidence. That zero is a property of the fitted optimum, not proof of opposing causal components.

### Level 4 — context-stable function-specific promotion

Only after component contrasts are shown to be stable across the competing context can state-specific references be promoted toward empirical pure-function optima.

This is the stricter optional gate described below.

## 5. The pure-function promotion gate

The same crossed experiment can be used to estimate causal component contrasts. Define

\[
M_{G0}(z)=W_{10}(z)-W_{00}(z),
\]

\[
M_{G1}(z)=W_{11}(z)-W_{01}(z),
\]

for the pollinator-mediated component under two antagonist states, and

\[
H_{P0}(z)=W_{01}(z)-W_{00}(z),
\]

\[
H_{P1}(z)=W_{11}(z)-W_{10}(z),
\]

for the antagonist-mediated component under two pollinator states.

Each component surface has its own optimum. SCH permits promotion to a context-stable empirical function-specific optimum only if the corresponding component optima agree across the alternate consumer state inside a prospectively declared equivalence bound, with interior support and propagated uncertainty.

Schematically,

```text
pollinator component optimum under G0
≈ pollinator component optimum under G1
        ↓ promotion gate
context-stable empirical z_F1*

antagonist component optimum under P0
≈ antagonist component optimum under P1
        ↓ promotion gate
context-stable empirical z_F2*
```

If the component optima differ materially by context, the correct conclusion is not failure. It is that the functional objective itself is context-dependent over the tested range. SCH then retains conditional component optima and does not use the pure-function label.

This gate prevents one of the most consequential interpretive shortcuts in multifunctional-trait experiments: treating a consumer-manipulated state as if every non-focal causal route had disappeared.

## 6. Negative controls are part of the theory

A framework that only searches for conflict will eventually find conflict. SCH therefore treats aligned multifunctionality as a critical negative control.

If two functions both favor the same region of \(z\), then

```text
multifunctionality = true
functional conflict = false.
```

Such systems are not exceptions to the framework; they are required demonstrations that the promotion gate rejects multifunctionality-only evidence.

Likewise, a system can show context dependence without a stable one-axis compromise. Strong environmental switching can move the optimum between states rather than producing a persistent interior balance. That outcome should remain distinct from an integrated compromise claim.

## 7. Source-adjudicated reality-pattern synthesis

We translated the SCH identification ladder into literature-observable signatures before prioritizing a focal causal experiment. The unit of recurrence is an **independent biological cluster**, not a paper, population, year, treatment cell, or measured trait. The current targeted source-adjudicated universe contains 16 independent clusters. Because retrieval was theory-targeted rather than probability-sampled, these counts describe recurrence and evidence structure within the screened universe; they do not estimate natural prevalence.

### 7.1 Conflict signatures recur, but aligned multifunctionality also occurs

Five clusters provide the strongest conflict-linked signatures in the current classification. Four are classified as `OPPOSING_DIRECTION`, where distinct functional routes favor opposing changes on one shared or closely bounded coordinate. A fifth cluster, *Satyrium longicauda*, provides a `COMBINED_INTERMEDIATE_OR_COMPROMISE` surface: experimentally shortened nectar spurs produced a male pollen-export maximum at an intermediate spur treatment, female fitness was highest at the largest tested spur length, and total fitness was hump-shaped in one year.

These positive cases are not the only informative observations. Two independent flower-orientation systems are classified as `SHARED_TRACKING_NO_CONFLICT`: the same trait contributes to multiple functions, but the available evidence does not establish that those functions favor different states. This negative class is central to SCH. It shows why “one trait, several functions” cannot itself be treated as an identified compromise.

One further system is retained as a `SHARED_TRACKING_CONFLICT_CANDIDATE`, where a shared cue affects multiple biological routes but the antagonist-loss component is not sufficiently linked to a common fitness estimand for promotion. Another is retained as `SEQUENTIAL_FILTER_COMBINATION`, where pollination and seed-predation selection occur at different fitness stages rather than forming the same simultaneous shared-coordinate estimand.

The literature therefore recovers both sides of the first promotion gate: opposing functional signatures recur, but multifunctionality without identified conflict also recurs.

### 7.2 Context-weight shifts are common but do not identify pure-function optima

Seven independent clusters are classified as `CONTEXT_WEIGHT_SHIFT`. Across these studies, drought, herbivory, consumer identity, antagonist pressure, phenological setting, or experimental interaction regime alters the effective selection acting on a multifunctional trait. These observations are consistent with the theoretical idea that the realized compromise depends on the relative weighting of functional demands.

They do not identify \(z_{F1}^*\) or \(z_{F2}^*\). A changed directional gradient is not the same object as a bounded optimum, and an optimum recovered under an ecological state is not automatically a pure functional optimum. The literature synthesis therefore records context dependence without silently promoting it to Level 4.

Published external meta-analyses of herbivory effects on floral traits, pollinator attraction, and reproduction provide a complementary quantitative layer: antagonist effects vary systematically with ecological context and can propagate into pollinator-facing and reproductive outcomes. Those meta-analytic effects are useful as evidence that functional weights vary; they are not estimates of SCH conflict loss \(L\) or of any function-specific optimum.

### 7.3 Complete separated optima remain the main literature gap

The strongest manipulated combined-compromise case still stops below pure-function identification. In *Satyrium*, the upper side of the female fitness function was not mapped because the manipulation primarily shortened spurs. The female optimum therefore cannot be declared fully bounded within the tested range.

Across the current 16-cluster universe, no literature case is promoted to a complete same-system reconstruction in which both pure functional optima are independently bounded, the combined optimum is identified, and the component surfaces pass the context-stability promotion gate with propagated uncertainty. That absence is itself an identification result. It prevents the paper from converting suggestive state-specific or marginal effects into quantities that the source designs do not identify.

### 7.4 Quantitative recovery is active but random-effects pooling remains fail-closed

The strict quantitative inventory contains four strong same-coordinate conflict designs at different levels of numerical completeness: *Dalechampia*, *Silene*, *Fragaria*, and *Gymnadenia*. Exact component coefficients are currently recorded for *Dalechampia* and *Silene*. The *Fragaria* and *Gymnadenia* studies contain relevant factorial or treatment-specific information. In *Gymnadenia*, one source-table treatment-edge contrast now supports a directionally robust **conditional normal-Wald** sign change under any admissible covariance, but its exact source covariance, experiment-wide adjusted significance, bounded functional optima and cross-system commensurability remain unavailable. That conditional one-edge statement does not open the strict quantitative pooling gate.

No strict random-effects stratum is currently admitted. The frozen gate requires at least three independent biological clusters with the same estimand family, compatible orientation, valid uncertainty, and correct treatment of within-study covariance. Missing covariance is not replaced by an independence assumption, and inaccessible supplementary values are not reconstructed by eye from figures.

The inclusion rule also matters. If a future numerical pool includes only systems admitted because they already show the focal opposing-sign pattern, the resulting mean is **conditional on positive admission**. Such a pool may summarize magnitude and heterogeneity among positive cases, but it cannot serve as an unbiased mean across all design-eligible systems or as an independent statistical test that recurrence exists. A design-wide synthesis would require a sign-independent eligibility rule and retention of aligned/no-conflict systems in the same eligible universe.

### 7.5 Empirical conclusion of the synthesis layer

The literature layer supports four bounded conclusions:

1. same-coordinate opposing functional signatures recur across independent systems;
2. multifunctionality can also occur without identified conflict;
3. ecological context frequently changes effective functional weighting;
4. combined-compromise geometry can be recovered in a manipulated system, while complete pure-function optimum identification remains rare.

It does **not** directly identify a general SCH conflict budget \(L\), the complete state-surface causal chain, or pure-function optima by default. Those objects remain behind the higher promotion gates.


### 7.6 A focal biological anchor: pollination, predator pressure, and survival translation in Pedicularis rex

The *Pedicularis rex* cluster already contributes to the five conflict-signature clusters in the source-adjudicated synthesis; the three independent studies below do not add biological replicates. Sun, Armbruster and Huang (2016; doi:10.1093/aob/mcw097) found observational associations of greater floral exsertion with both higher stigmatic pollen receipt and higher seed predation, while predator losses reduced viable reproduction. Pollen and floral observations span 14 populations, seed outcomes 12 and directly linked morphology–seed data seven. The study identifies opposing function-compatible associations, not assigned exsertion levels or pure functional optima.

Sun and Huang (2015; doi:10.1093/aobpla/plv019) used **puncture-plus-water drainage** on cupulate bracts in six populations. Seed predation increased significantly in **five populations**; the site-by-treatment test was chi-square = 36.782 (df=5, P<0.0001). This compound treatment does not isolate water protection from wounding. In the same original experiment, the population-by-treatment signal for predation contrasted with an undetected final-seed interaction (chi-square = 4.913, P = 0.4265) and initial-seed interaction (P = 0.960), although the overall final-seed treatment effect was detectable. Differing endpoint-specific P values are not a test that the effects differ: non-rejection is **not evidence that final-seed effects are uniform among sites**. Pollinator visitation was compared only at **Shama** (P = 0.958). The source term beta=0.012, SE=0.224 yields a diagnostic normal-Wald 95% interval of **−0.427 to 0.451** on its logit scale; non-rejection there is **neither global neutrality nor an equivalence test**. This is **not an equivalence test** of preserved pollination service. The original model included year-by-treatment interaction, without covariance to recover a marginal two-year effect. Source audit: SCH_PEDICULARIS_2015_REAL_CROSS_ENDPOINT_DEFENCE_MOSAIC_V1.md.

Xia, Sun and Liu (2013; doi:10.1098/rsbl.2013.0387) reported density- and patch-size-associated predation in **11 spatial patches** (five sparse, six dense), **not thousands of independent patches** inferred from nested capsules. Their unrecovered raw workbook prevents source-robust patch estimates and says nothing causal about exsertion optima.

The three sources separate ecological quantities that SCH must not conflate:

1. **Pressure:** patch-average attack, regardless of trait.
2. **Trait discrimination:** change in attack with assigned exsertion at fixed physical defense and opponent exposure.
3. **Fitness translation:** conversion of initiated seeds, damaged seeds and uncertain capsule fates into mature viable reproduction.

A patch may show higher mean attack but weaker exsertion discrimination, or similar attacks but different final fitness gradients; those are **alternative untested mechanisms**, not recovered effect estimates. Identifying the causal reproductive surface requires randomizing several realized exsertion ranks while **selectively excluding seed predators while bract water is held constant** and recording early attack plus intact viable seeds. historical fully consumed capsules cannot be reclassified as observed zeros. The 2013–2016 studies do **not** constitute one crossed exsertion-by-pollinator-by-predator experiment; **none can be promoted to a measured L** or SLK architecture value.

### 7.7 Experimentally changing one ecological input can reverse selection on one floral trait

The most informative **already executed factorial source** for distinguishing functional opposition from a merely intermediate observation is the one-population *Gymnadenia conopsea* experiment of Sletvold, Moritz and Ågren (2015; *Ecology* 96:214–221, doi:10.1890/14-0119.1). It crossed natural versus supplemental hand pollination with natural versus excluded herbivory. This is **one independent biological programme**, already counted once among the seven context-weight-shift clusters above; its four treatments, five measured traits and multiple pairwise contrasts are not extra independent systems. Original Table A2 contains the source-reported treatment-cell selection gradients and standard errors, now preserved in the SCH quantitative ledger.

**A real ecological sign reversal with one interaction held fixed.** With herbivores excluded in both arms, the reported selection gradient on flowering start is positive under open pollination (β = +0.094, SE = 0.031; source P < 0.01), favoring later flowering, and negative with supplemental hand pollination (β = −0.066, SE = 0.028; source P < 0.05), favoring earlier flowering. The source-measured point difference, supplemented minus open, is **−0.160** standardized-selection-gradient units. The exact standard error of this between-cell contrast cannot be reconstructed because the original coefficient covariance is not provided. The Cauchy–Schwarz bound nevertheless places the *largest mathematically compatible SE* at 0.031 + 0.028 = 0.059. Conditional on comparable, valid source standard errors and a normal-Wald approximation, even that worst-case covariance yields a 95% interval of approximately [−0.276, −0.044] and a two-sided nominal P upper bound of approximately 0.0067. This interval is not the original authors' factorial-ANCOVA interval, a randomization-test confidence interval, or an adjustment for searching all twenty single-factor comparison edges. A conservative twenty-edge Bonferroni upper P bound of approximately 0.134 does **not** establish familywise significance. Thus the empirical single-edge result is substantial, but its discovery and multiple-testing status must remain visible.

In the same source, flowering-start selection under **natural pollination and natural herbivory** is near zero (β = −0.0042, SE = 0.054). That value is neither proof of precisely balanced functional optima nor proof of zero selective pressure. The factorial treatment-cell estimates imply a pollination-associated positive flowering-time contribution of roughly +0.16, and a herbivory-associated negative contribution of roughly −0.09 to −0.10, producing a weak observed net coefficient. The difference-in-differences in the four source point estimates is −0.0042; this is only a descriptive additive reconstruction. An equivalence margin or a covariance-aware test of zero interaction is not available from Table A2.

**The same ecological interaction produces a different trait outcome.** The orchid's spur-length axis exhibits positive source-point pollinator and herbivore contributions: the two animal interactions can both favor longer spurs instead of opposing one another. The herbivore-excluded spur-length gradients are +0.077 (SE 0.035; source P < 0.05) under open pollination and −0.042 (SE 0.029; not significant) under hand supplementation. Unlike flowering start, spur length does not show two individually supported opposite-sign selection estimates. A species-wide designation of pollinator–herbivore "conflict" would therefore obscure the ecologically decisive distinction between its **trait coordinates**.

Together, the factorial orchid study establishes a positive, source-bounded ecological reality check: **changing a single experimentally assigned interaction can reveal opposing directional selection on flowering time even when natural net selection is weak, and the same actors may instead reinforce selection on a different floral trait**. This directly rejects a restrictive interpretation that reversal necessarily requires several ecological factors to change simultaneously or a demonstrably nonadditive interaction. But the floral phenotypes were measured rather than assigned; experimental manipulation of pollination and herbivory identifies changed selective *regimes*, not causal do(z) component optima, an interior reproductive-fitness optimum, pure function-specific objectives, the SCH conflict budget L, or a downstream SLK architecture payoff. In particular, this is not a manipulated flowering-time optimum.

The exact source Table A2 cell values, covariance-worst-case calculation and all-cell caveats are preserved in data/SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv, docs/SCH_GYMNADENIA_SINGLE_FACTOR_REVERSAL_V1.md, and docs/SCH_GYMNADENIA_COVARIANCE_ROBUST_GRADIENT_CONTRAST_V1.md. The unchanged source identity is doi:10.1890/14-0119.1, Ecological Archives E096-022 Appendix A. This source is not a new held-out programme and does not revise the frozen H2 reversal-prevalence denominator.



### 7.8 Independent pollination-treatment programmes: strong selection changes need not reverse sign

A complete secondary analysis of the already frozen V27 source tables examines all **14** same-year, within-trait open-versus-supplemented pollination contrasts from three independent published studies, without selecting comparisons by outcome: *Dactylorhiza lapponica* (Sletvold, Grindeland and Ågren 2010; five traits; doi:10.1111/j.1469-8137.2010.03296.x), *Primula alpicola* (Chen, Zhang and Li 2017; four; doi:10.1038/s41598-017-13340-0) and *Trillium discolor* (Koski 2023; five trait-year contrasts; doi:10.1002/ajb2.16101). These constitute three studies, not 14 independent field experiments; the Poisson-linked *Trillium* gradients cannot be pooled numerically with linear gradients.

Within each source metric, the difference in selection magnitude is open minus supplemented. Under any covariance compatible with the original two reported SEs, the difference SE cannot exceed their sum. Applying a conditional normal-Wald Bonferroni correction across all 14 source-qualified contrasts, *Dactylorhiza* spur length changes **+0.324** (maximum SE 0.105; simultaneous interval approximately [+0.018,+0.630]) and *Primula* flowering start changes **+0.206** (maximum SE 0.066; interval [+0.014,+0.398]). Both remain positive under source decimal rounding for the **14-edge** family; neither gives two independently supported opposite-direction gradients. *Trillium* 2020 petal size changes **−4.41** in printed Poisson coefficients, but its reconstructed simultaneous guarantee fails source one-decimal SE rounding; the original authors independently report a strong direct treatment contrast (P<0.0001), not our refitted result. Full provenance and uncertainty boundaries appear in SCH_H2_THREE_PROGRAMME_POLLINATION_SELECTION_V1.md.

The *Primula* 2019 author correction (Chen, Zhang and Li 2019; doi:10.1038/s41598-019-43381-6) updates Figure 1 and Table 3 notation, not the original Table 2 linear selection coefficients and standard errors used here. The *Primula* open group combined two style morphs while the supplemented group was long-styled only, leaving a composition caveat. The studies manipulated pollen supply, not the trait coordinate. Hence a meaningful between-regime change is **not a direct z** manipulation, a supported optimum shift, or automatic evidence of functional opposition. The biological conclusion is that the **magnitude** of selection can change without two significant and opposed cell gradients; original H2M1 holdout classifications remain unchanged.

### 7.9 From a striking reversal to a four-programme ecological response spectrum

A complete, independent-source extension of the Gymnadenia factorial and preceding three-programme pollen-supplementation comparison reveals a more informative biological question than "how frequently does selection reverse direction?" **Does the same pollination change alter a trait's selective environment even when strong reversal evidence is absent?** The source-eligible family consists of every matched open-versus-hand-supplemented pollen contrast for the five Gymnadenia traits in **two fixed herbivory regimes**, plus the previously frozen **14 same-year floral-trait comparisons** from Dactylorhiza lapponica, Primula alpicola and Trillium discolor. The combined secondary family therefore has **24 within-source selection-gradient edges**, but **four independent published biological programmes**, not 24 independent replicated experiments. The original V26/V27 heldout study classifications and their primary q values are unchanged.

Within a particular trait and fixed herbivory/year context, we distinguish three measurable objects: (i) an **estimated sign change** between the two point gradients; (ii) **two independently supported but opposite-sign treatment-cell gradients**, assessed by the source SEs at an ordinary nominal threshold; and (iii) an identifiable **difference between the two estimated gradients**, with unknown covariance bounded by the sum of reported SEs. Because the third statistic is conditional on source-SE validity and asymptotic normality, we apply a simultaneous Bonferroni critical value for **all 24 matched edges** and then separately perturb each printed coefficient and SE over its original decimal-rounding interval.

The full four-programme descriptive results separate sharply: **11/24** point pairs change sign, only **one** has individually source-SE-supported opposite signs (the previously reported Gymnadenia flowering-start contrast with herbivores excluded), **two** open-versus-supplemented differences clear the **printed-value conditional 24-edge normal-Wald simultaneous bound**, and **zero** remain certified under worst-case **source decimal rounding**. The printed-value contrasts are Dactylorhiza spur length (+0.324; maximum covariance-compatible SE 0.105) and Primula flowering start (+0.206; maximum SE 0.066), with 24-edge adjusted normal-P upper bounds approximately 0.0487 and 0.0432. The Gymnadenia +0.160 flowering-start contrast has one-edge upper P approximately 0.00669, but this is not a 24-edge familywise certificate. The original source directly documents its significant positive and negative cell gradients; neither the original biological observation nor the previous *one-edge* and *14-edge* analyses is overwritten.

The absence of a decimal-rounding-robust 24-edge certificate is an important sensitivity outcome, **not evidence that no biological effects occurred**. Adding a fourth study and ten legitimate source comparisons to the previously analysed 14-edge family increases the multiple-testing burden. It does not change any original fitness measurement or invalidate the original study-specific treatment interactions. In particular, the original Trillium 2020 petal-size treatment test is reported directly by its authors (P < 0.0001), although the corresponding conservative subtraction of source-printed cell coefficients is sensitive to covariance and source precision. Differences across Trillium conditional Poisson models, Dactylorhiza standardized linear selection, Primula morph composition and Gymnadenia factorial backgrounds prohibit a pooled cross-species beta. The 24 observations represent different trait/context comparisons and must not be presented as 24 natural-system replications or as a population prevalence denominator.

The empirical implication for SCH is therefore **trait-axis-specific sensitivity to ecological context**, not a universal tendency to reverse selection. Across separately executed field studies, a point sign flip, two individually significant opposite directions, and a demonstrable change in selection magnitude are three non-equivalent evidential outcomes. Each supports a different ecological statement. Strong pollination-mediated trait selection can attenuate toward a poorly resolved zero without a supported opposite direction; the same source animals can reinforce selection on some axes while opposing selection on others, as Gymnadenia explicitly shows. Neither observation identifies an experimentally assigned trait optimum, pure functional objectives, or the downstream shared-constraint loss L. The complete source-matched analysis and claim boundaries are in docs/SCH_FOUR_PROGRAMME_POLLINATION_SELECTION_SPECTRUM_V1.md and scripts/audit_sch_four_programme_selection_spectrum.py.



### 7.10 Compensation and phenological debt: a different ecological route to selection

The *Lythrum salicaria* field experiment (Thomsen and Sargent 2017; doi:10.1093/aob/mcx026) reveals a distinct route: clipping apical meristems to simulate herbivory changed mean traits and selection on those traits in **opposing directions**. The original group mean number of inflorescences increased from 5.4 to 8.0 (+48.15%), yet selection for additional inflorescences decreased from β=+0.47 to +0.20. The author's direct damage-by-trait selection contrast was **+0.27 (SE 0.10; P<0.01)**. Mean flowering onset moved **5 days** later (Julian 191 to 196), yet selection toward earlier flowering strengthened from β=−0.03 to −0.28, with direct interaction **+0.25 (SE 0.10; P<0.05)**. Both groups had mean flowering end at day 236, implying different **group-mean calendar windows**, not measured individual flowering durations.

Hand-supplemented flowers produced **17.4%** more seeds, establishing pollen limitation, but pollen-treatment-by-trait selection interactions were not detected for these three source traits. Absence of a detected interaction is **not an equivalence** test or proof of no pollinator effects. In a secondary three-damage-term normal Bonferroni sensitivity, both damage selection contrasts exclude zero with reported numbers, but only inflorescence number survives original decimal rounding; a larger nine-interaction family does not certify either. These are conditional recalculations, not the authors' ANCOVA tests.

Clipping was initially randomized, but eight naturally damaged controls were subsequently reassigned, and pollen supplementation used matched within-plant flowers rather than independently randomized whole-plant pollination regimes. *Compensatory regrowth* is a plausible causal pathway, not a directly identified mediator. Mean phenotypic response, selection on a phenotype and pollen limitation therefore measure **three distinct ecological outcomes**; none establishes a randomized floral-trait optimum. Full source tests and limits: SCH_LYTHRUM_COMPENSATORY_REGROWTH_SELECTION_V1.md.

### 7.11 Stage-dependent ecological roles: aligned attraction can conceal antagonistic fitness translation

Knauer and Schiestl (2017; doi:10.1007/s10682-016-9878-8) manipulated **consumer composition** in *Brassica rapa* cages: bumblebees alone, cabbage butterflies alone, or both. Adult butterflies visit and pollinate flowers but lay eggs whose offspring damage plants; the same species cannot be assigned a fixed functional sign. The original nine-trait Table 1 shows that **corolla size and phenylacetaldehyde** are positively associated with bumblebee visits, butterfly visits and butterfly oviposition (nominally supported in all three response classes). These are distinct count and binary-egg models; 2/9 source-trait overlap is **not a 27-test** familywise result or a natural prevalence estimate, and traits were observed rather than randomized.

**Receiver overlap need not entail opposing univariate fitness selection.** Corolla size has **positive net seed-fitness selection** in all three regimes: β=+0.22±0.04 under bee-only, +0.22±0.08 under both, and +0.26±0.09 under butterfly-only conditions (all original P<0.05). Phenylacetaldehyde shows source-significant positive selection only under bees (+0.15±0.05, P=0.006); the mixed coefficient is negative but unsupported (−0.09±0.08, P=0.27). The authors did not detect a directional trait-by-insect-regime ANCOVA interaction, so differences in individual significance do not prove changes between regimes.

**Different reproductive stages explain the apparent contradiction.** Source-fitted seed production associations were positive for bee visits (+20.5±4.8) and butterfly visits (+6.8±2.0) but negative for subsequent caterpillar infestation (−104.5±19.0). This is not a new individual-level mediation analysis. Under mixed insects, the source reported nominally negative corolla-size × phenylacetaldehyde correlational selection (γ=**−0.17±0.08, P=0.029**), but none of the **18** original trait-pair-by-regime tests clears Bonferroni correction; no regime difference in correlational selection was detected. Under the original authors' additive mixed-versus-single-regime gradient benchmark, their fitted nonadditivity contrasts were −0.20±0.08 (P=0.009) for phenylacetaldehyde and +0.19±0.08 (P=0.018) for 1-butene-4-isothiocyanate. These source tests are not equivalent to a demonstrated change in pure-function optima or to experiment-wide multiplicity control.

Finally, (E)-α-farnesene predicted bee visits (+0.18±0.05, P<0.001) while butterfly visitation and egg-response associations were not detected. Such a candidate biased signal remains neither an equivalence test of butterfly indifference nor a demonstrated functionally private cue. *Brassica* therefore shows genuine shared attraction plus opposite adult-benefit/offspring-cost pathways, while net flower-size selection remains positive. It provides **no causal** randomized trait-by-selective-consumer reproductive surface, pure-function optimum, measured SCH loss L or downstream SLK architecture payoff. Source-linked Table 1–3 details: SCH_BRASSICA_2017_MULTISTAGE_RECEIVER_ROLE_CONFLICT_V1.md.

### 7.12 A unifying ecological test: where does context enter the selection chain?

These published systems are **not replications of one mechanism**. They locate context-dependence at different points between phenotype, receivers, development, and reproductive success. This distinction is the nontrivial ecological contribution of the comparison: changes in net selection do not imply changes in consumer trait preference, and aligned preferences do not imply aligned reproductive contributions.

**Table 1. Four source-supported ecological signatures and their unresolved causal steps.** The table is an evidence map, not a pooled effect or a natural-prevalence estimator.

| Context-sensitive link | Real study-specific observation | What remains unidentified |
|---|---|---|
| Relative functional selection | *Gymnadenia*: flowering-start β +0.094 to −0.066 under pollen supplementation with herbivores excluded | Randomized flowering time and pure-function optima |
| Developmental phenotype and selection | *Lythrum*: clipped mean inflorescences 5.4 to 8.0 while β +0.47 to +0.20 | Unique mediation by compensatory regrowth |
| Receiver versus lifetime role | *Brassica*: corolla size predicts adult visits and oviposition, yet positive net seed-fitness selection across three insect regimes | Selective cue causation and pure antagonist cost |
| Predation versus final reproduction | *Pedicularis*: 2015 predation site-by-treatment χ²=36.782, but final-seed interaction P=0.4265 | A direct statistical test of cross-endpoint effect equality or an exsertion-by-enemy optimum shift |

This yields a prospective discriminating experiment rather than an untested claim of a universal process. Randomize a shared floral trait across independently assigned consumer states, then observe receiver visits or attacks, developmental allocation, initiated seeds, and viable maturity outcomes **on linked, defensibly sampled biological units**. If receiver preference is the changing mechanism, the trait-conditioned early receiver response should vary with context. If instead **fitness translation** changes, early trait-conditioned receiver responses can remain similar while conditional seed survival or trait–fitness slopes differ. If damage-induced developmental compensation dominates, trait expression and resource allocation should shift even without changed receiver preferences. These alternatives are hypotheses, not retrospectively identified mediators in the studies above.

The empirical synthesis therefore supports **multiple locations for ecological reweighting**, not an estimated shared constraint loss L or a demonstrated trait-splitting evolutionary transition. The 16-cluster conceptual ledger and the prospectively frozen quantitative holdouts are not expanded by this table.

## 8. Final causal identification layer

The literature synthesis defines rather than replaces the remaining experiment. Its role is no longer to show that multifunctionality, opposing demands, or compromise-like outcomes exist; those patterns are already recovered across independent systems. The final experiment is needed only for the quantities that the literature leaves structurally unidentified.

A qualified focal system should therefore be chosen by fail-closed gates rather than by prominence. The strongest direct design manipulates the same trait coordinate \(z\) across several levels and selectively crosses pollinator and antagonist states so that \(W_{00}(z), W_{10}(z), W_{01}(z), W_{11}(z)\) can be fitted on one reproductive scale.

A strong Level-3 causal compromise receipt then requires:

```text
z_P* != z_G*
combined W11(z) has a supported interior z_C*
G off -> optimum shifts toward z_P*
P off -> optimum shifts toward z_G*
opposing functional-component gradients near z_C*
```

Promotion to empirical pure-function optima is optional and stricter. The component surfaces \(M_{G0}(z),M_{G1}(z),H_{P0}(z),H_{P1}(z)\) must support context-stable component optima inside prospectively frozen equivalence bounds with propagated uncertainty. If they do not, SCH retains conditional component optima rather than forcing a pure-function interpretation.

**Dalechampia** remains a high-value first candidate because published populations contain opposing pollinator and seed-predator selection on shared floral structures, but conflict is not species-wide and must be qualified by population and season. **Pedicularis rex** is an especially informative observational-conflict and experimentally perturbed defence *reality anchor*, but its 2015 defence intervention is not selective predator exclusion, and its 2016 exsertion is not a randomized multi-level treatment. It can become a focal causal execution system only after reversible exsertion manipulation and a pollination-preserving, water-fixed predator-access intervention are qualified in the same population and season. The variance-aware five-rank analysis is a **synthetic-tested inferential tool**, not executed field inference.

**Nicotiana attenuata** remains a strong local shared-cue mechanism candidate and downstream bridge system. **Castilleja linariaefolia** remains a fallback requiring reversible trait manipulation and selective consumer control. Aligned-optimum systems remain valuable experimental negative controls.

The final execution chain is therefore deliberately last in the empirical programme:

```text
literature recurrence / specificity map
-> quantitative compatibility audit
-> residual identification gap
-> qualify conflict-active focal context
-> validate reversible multi-level z manipulation
-> validate selective consumer interventions
-> fit W00(z), W10(z), W01(z), W11(z)
-> recover z_P*, z_G*, z_C*
-> test optimum shifts and opposing component gradients
-> optionally test context-stable component optima
-> export only justified quantities downstream
```

## 9. Relation to SLK and BITA

SCH now has a narrow ownership boundary.

**SCH owns identification of conflict.** Its primary output is a justified statement about whether opposing functional demands have been identified on one shared coordinate and, when possible, the corresponding compromise geometry.

**SLK owns downstream transport.** Once an empirically defensible conflict budget \(L\) exists on a common fitness scale, SLK asks how much of it is recoverable, whether architecture value \(\Phi\) becomes positive, whether the favored architecture is locally accessible, and whether it invades, fixes, or dominates long-run occupancy.

**BITA owns mechanism identification after multiple trait axes exist.** Its central question is whether an observed trait interaction has actually identified the ecological route generating the joint effect.

The programme therefore contains two different promotion problems around one flagship:

```text
SCH
multifunctionality
  != conflict
        ↓ identified L

SLK
L → R → Phi → accessibility → invasion → fixation → occupancy

BITA
trait interaction
  != mechanism
```

This division prevents all three papers from claiming the same architecture result.

## 10. Main predictions and falsifiers

SCH predicts that a truly conflicted shared coordinate should satisfy the following linked observations:

1. the same coordinate contributes causally to both focal functional routes;
2. state-specific optima differ, \(z_P^*\neq z_G^*\);
3. the combined surface has a supported interior optimum over the tested range;
4. removing each functional demand moves the optimum toward the state favored when that demand is absent;
5. functional-component gradients near the combined optimum oppose one another.

The *P. rex* implementation supplies a particularly discriminating ecological falsifier: a population may have high seed-predator pressure without having a steep **assigned-exsertion-dependent** early attack slope, and a steep attack slope need not survive as a correspondingly steep final viable-seed gradient. A valid G intervention must therefore identify trait-conditioned early attack and final reproductive surface differences separately, rather than promote mean damage rates into a fitness optimum.

The framework is falsified for the declared conflict claim if the two functions favor the same tested state, if consumer manipulations do not shift the trait-fitness surface in the predicted directions, or if the apparent interior optimum disappears under the causal decomposition.

A nine-trait *Brassica* controlled-cage source identifies a further ecological prediction: **an adult pollinating herbivore may share positive preferences for two floral cues with mutualists, even while its larval stage imposes a negative fitness pathway**. Such receiver alignment does not demand a negative net selection gradient on each cue; the most diagnostic signal may lie in reproductive translation, nonadditive selection or multivariate signal combinations. Receiver-specific candidate signals must still clear a true equivalence or preference manipulation test before any dimensional-release claim.

An additional *Lythrum* artificial-damage experiment supplies a falsifier for an overly narrow pollinator-preference explanation of changed floral selection: disturbance produced more inflorescences while weakening selection for further inflorescence number and delayed flowering while increasing selection for earlier flowering. Detectable pollen limitation was not coupled to a detected pollination-treatment-by-trait selection effect. Thus SCH must allow **developmental compensation, resource allocation and altered opportunity windows**, alongside consumer preferences, as candidates for context-specific fitness translation; these candidates require direct mediation tests and cannot be inferred automatically from the signs of selection gradients.

The full four published study-family sensitivity adds a sharper evidential distinction: **11 point sign flips, one nominal double-supported sign reversal, two printed-value simultaneously protected slope changes, and zero source-rounding-robust changes** among 24 matched contrasts. These are outcomes of nested evidential standards in a targeted literature subset—not estimates of natural prevalence, and not reason to erase independently reported original treatment interactions.

The independent Dactylorhiza, Primula, and Trillium source programmes further show why SCH must distinguish *magnitude response* from *supported sign reversal*: an ecological treatment can substantially modify a selection gradient without proving a full optimum displacement or even a signed reversal of both treatment-cell gradients. Programme-matched contrasts and biological treatment specificity are essential.

The *Gymnadenia* factorial experiment supplies a direct ecological discriminant at the selection-gradient level: a near-zero net gradient can coexist with large, opposite contextual contributions, and one pollination intervention can reverse a gradient while the herbivory treatment remains fixed. Conversely, spur length in the same population shows reinforcing rather than opposing directional contributions. SCH must therefore make predictions for a *specified trait axis and outcome*, not for a plant species or the identities of the interacting consumers in general.

The pure-function promotion is separately falsified when component optima change materially across the alternate consumer state. In that case SCH retains context-dependent functional objectives rather than forcing context stability.

The literature synthesis supplies an additional specificity falsifier: aligned multifunctionality is an admissible and expected negative class. A framework that promoted every multifunctional trait to conflict would fail its own evidence ladder.

## 11. Claim ceiling

Current evidence supports:

```text
MULTIFUNCTIONALITY_REALITY_RECOVERED
CASE_LEVEL_OPPOSING_DEMANDS_RECOVERED
CASE_LEVEL_COMPROMISE_RECOVERED
SOURCE_ADJUDICATED_CONFLICT_RECURRENCE_RECOVERED
ALIGNED_NO_CONFLICT_CONTROLS_RECOVERED
STATE_SPECIFIC_CAUSAL_COMPROMISE_ANALYZER_READY
PURE_FUNCTION_PROMOTION_GATE_READY
```

Current evidence does **not** yet support:

```text
GENERAL_SCH_LOSS_L_META_ESTIMATED
COMPLETE_CAUSAL_COMPROMISE_EXPERIMENT_EXECUTED
PURE_FUNCTION_OPTIMA_IDENTIFIED_BY_DEFAULT
HISTORICAL_TRAIT_SPLITTING_INFERRED
```

Contemporary functional differentiation and mechanism allocation are distinct from historical trait splitting. The latter claims require new biological evidence rather than stronger prose.

## 12. Conclusion

Multifunctionality is not functional conflict, and a context-specific reproductive optimum is not automatically a pure-function optimum. These are separate promotion steps with separate evidence requirements.

SCH turns compromise from an intuitive label into an identification problem. The cross-system synthesis shows that opposing same-coordinate signatures and compromise-like geometry recur, that ecological weighting is strongly context-dependent, and that aligned multifunctionality provides a real negative class. At the same time, the literature rarely identifies complete bounded pure-function optima and does not justify a general conflict budget \(L\).

This combination is the point of the paper: mathematics defines the promotion gates, the literature tests whether their observable signatures occur in reality, and the focal crossed experiment is reserved for the residual causal quantities that published studies do not identify. A strong final causal claim requires opposing geometry on the same coordinate, a supported combined optimum, predictable shifts when each functional demand is removed, and opposing component gradients. A still stronger pure-function claim requires context-stable component optima rather than a relabelled ecological state.

This narrower ownership keeps the programme clean. Once conflict is identified, downstream architecture value and evolutionary realization belong to SLK. Once multiple traits interact, mechanism allocation belongs to BITA. SCH's job is earlier and more basic: determine whether the conflict being transported downstream has actually been identified at all.

## Literature Cited

Chen, L., B. Zhang, and Q. Li. 2017. Pollinator-mediated selection on flowering phenology and floral display in a distylous herb *Primula alpicola*. *Scientific Reports* **7**:13157. https://doi.org/10.1038/s41598-017-13340-0

Chen, L., B. Zhang, and Q. Li. 2019. Author Correction: Pollinator-mediated selection on flowering phenology and floral display in a distylous herb *Primula alpicola*. *Scientific Reports* **9**:7054. https://doi.org/10.1038/s41598-019-43381-6

Knauer, A. C., and F. P. Schiestl. 2017. The effect of pollinators and herbivores on selection for floral signals: a case study in *Brassica rapa*. *Evolutionary Ecology* **31**:285–304. https://doi.org/10.1007/s10682-016-9878-8

Koski, M. H. 2023. Pollinators exert selection on floral traits in a pollen-limited, narrowly endemic spring ephemeral. *American Journal of Botany* **110**:e16101. https://doi.org/10.1002/ajb2.16101

Sletvold, N., J. M. Grindeland, and J. Ågren. 2010. Pollinator-mediated selection on floral display, spur length and flowering phenology in the deceptive orchid *Dactylorhiza lapponica*. *New Phytologist* **188**:385–392. https://doi.org/10.1111/j.1469-8137.2010.03296.x

Sletvold, N., K. K. Moritz, and J. Ågren. 2015. Additive effects of pollinators and herbivores result in both conflicting and reinforcing selection on floral traits. *Ecology* **96**:214–221. https://doi.org/10.1890/14-0119.1

Sun, S.-G., and S.-Q. Huang. 2015. Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* **7**:plv019. https://doi.org/10.1093/aobpla/plv019

Sun, S.-G., W. S. Armbruster, and S.-Q. Huang. 2016. Geographic consistency and variation in conflicting selection generated by pollinators and seed predators. *Annals of Botany* **118**:227–237. https://doi.org/10.1093/aob/mcw097

Thomsen, C. J. M., and R. D. Sargent. 2017. Evidence that a herbivore tolerance response affects selection on floral traits and inflorescence architecture in purple loosestrife (*Lythrum salicaria*). *Annals of Botany* **119**:1295–1303. https://doi.org/10.1093/aob/mcx026

Xia, J., S.-G. Sun, and G.-H. Liu. 2013. Evidence of a component Allee effect driven by predispersal seed predation in a plant (*Pedicularis rex*, Orobanchaceae). *Biology Letters* **9**:20130387. https://doi.org/10.1098/rsbl.2013.0387
