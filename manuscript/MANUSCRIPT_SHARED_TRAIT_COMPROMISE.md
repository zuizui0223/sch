# Multifunctionality is not functional conflict: identifying compromise on a shared trait axis

**Canonical SCH full-paper science source**

**Target class:** conceptual / methodological ecology

## Abstract

Multifunctional traits are often described as evolutionary compromises, but multifunctionality alone does not establish conflict. Two functions may use the same phenotypic coordinate while favoring the same state, and even when experiments recover different reproductive optima across ecological contexts, those state-specific optima are not automatically the pure optima of the focal functions. SCH separates these inferential levels. For a shared trait coordinate \(z\), theory may define pure function-specific objectives with optima \(z_{F1}^*\) and \(z_{F2}^*\). A crossed empirical experiment instead identifies state-specific reproductive surfaces \(W_{00}(z),W_{10}(z),W_{01}(z),W_{11}(z)\), with directly estimable optima \(z_P^*\), \(z_G^*\), and \(z_C^*\). Because consumer-independent and direct trait effects can remain in every state, \(z_P^*\neq z_{F1}^*\) and \(z_G^*\neq z_{F2}^*\) in general. We therefore define a promotion ladder from multifunctionality to local functional conflict, state-specific compromise, and—only when component contrasts are context-stable—empirical pure-function optima. We then translate this ladder into literature-observable signatures before prioritizing a focal causal experiment. A source-adjudicated synthesis currently contains 16 independent biological clusters: five direct conflict-signature clusters, seven context-weight-shift clusters, two aligned/no-conflict controls, one shared-tracking conflict candidate, and one sequential-filter boundary. One manipulated system additionally recovers a combined-intermediate/compromise surface, but complete bounded pure-function optima remain unidentified. In a separate factorial *Gymnadenia conopsea* experiment, the flowering-start selection gradient changes from +0.094 (SE 0.031) under open pollination to −0.066 (SE 0.028) under supplemental hand pollination with herbivores excluded in both arms; this is an experimentally changed ecological context, not a manipulated flowering-time optimum. A separate secondary audit of three independent pollen-supplementation programmes finds a familywise-bounded within-year change in selection magnitude for Dactylorhiza spur length and Primula flowering start (14 eligible treatment edges examined); a Trillium petal-size contrast is independently strongly supported by its original source test but more sensitive to reconstruction from rounded printed standard errors. These changes need not constitute supported sign reversals. A separate, explicitly exploratory comparison across four independent published pollination programmes contains 24 within-trait treatment contrasts: 11 change point-estimate sign, but only one has nominally supported opposite signs in both source cells; two source-printed between-treatment differences meet a conditional 24-comparison normal-Wald bound, and neither survives worst-case original-number rounding. These contrasting inferential outcomes distinguish context-driven selection sensitivity from proven sign reversal. A distinct *Lythrum salicaria* apical-damage experiment adds a developmental tolerance route: clipped plants averaged more inflorescences and started flowering later, yet experienced weaker additional-inflorescence selection and stronger selection for earlier flowering, with no detected pollen-treatment x trait selection despite measured pollen limitation. This is one source-bounded study rather than a fifth pollen-programme comparison. A same-experiment *Brassica rapa* source analysis across nine floral traits shows that flower size and phenylacetaldehyde each predict bee visits, butterfly visits and oviposition, while net seed selection on flower size remains positive in all three insect regimes; a nominal negative mixed-regime floral-size × scent interaction and source-reported nonadditivity reveal possible selection on trait combinations and fitness-stage translation rather than automatic opposing single-trait selection. A strict quantitative inventory contains four strong same-coordinate conflict designs at different levels of numerical completeness, but no random-effects stratum currently satisfies the frozen compatibility and uncertainty gate. These results support recurrence of conflict-compatible and compromise-like geometry while showing that multifunctionality can also remain aligned and non-conflicted. They do not identify a general SCH conflict budget \(L\) or justify relabeling state-specific reproductive optima as pure-function optima. The residual empirical target is therefore sharply defined: selective multi-level \(z\times P\times G\) experiments are reserved for final causal state-surface reconstruction and optional pure-function promotion after the cross-system reality pattern has been established.

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

The *Pedicularis rex* cluster already contributes to the five conflict-signature clusters described above; the following triangulation **does not add a seventeenth biological cluster or another independent experimental replicate**. It illustrates why different real ecological measurements can strongly motivate a shared-trait conflict hypothesis without jointly identifying its causal optimum.

Sun, Armbruster and Huang (2016; doi:10.1093/aob/mcw097) examined floral exsertion relative to water-bearing cupulate bracts, pollen receipt, pre-dispersal seed predation, and surviving seeds. Greater natural exsertion was associated with more pollen on stigmas and more seed predation, while seed loss reduced final reproduction. The observational pollination and predation associations point in functionally opposing directions on a common flower-geometry coordinate. Floral and pollination measurements spanned 14 populations, seed outcomes 12 populations, and the directly linked plant-level morphology–seed subset seven populations. These are *not* 14 or 12 experimentally randomized trait optima. Likewise, absence of a population-by-exsertion term in the selected pollen/predation models is not a demonstration that consumer-response slopes are identical everywhere. Population-dependent relationships in the final viable-seed model could also emerge downstream of largely shared floral-response geometry.

Sun and Huang (2015; doi:10.1093/aobpla/plv019) experimentally modified cupulate bracts in six populations and found an increase in seed predation following **puncture-plus-water drainage**, significant in five populations; the original site-by-treatment interaction was reported as chi-square = 36.782 on five degrees of freedom (P < 0.0001). This identifies local heterogeneity in the reproductive-antagonist consequences of the *combined treatment package*. It does **not** isolate removal of liquid water from puncturing, injury, or other changes in the bract. Pollinator visitation showed no statistically detected treatment term (P = 0.958), but the comparison was measured **only at Shama**. From the original β=0.012 and SE=0.224, the diagnostic normal-approximation 95% Wald interval is **−0.427 to 0.451** on the source logit coefficient scale; even the 90% interval (−0.356 to 0.380) does not fit an equivalence tolerance narrower than 0.380. There was no prospectively justified equivalence margin, plot-cluster uncertainty reanalysis, or six-population visitation sample. The original model also includes YEAR × TREATMENT (β=−0.099, SE=0.451), with no reported covariance for a two-year marginal effect. **Non-rejection is not an equivalence test**; non-rejection there is neither global neutrality nor an equivalence test, and preferential defence loading without pollination cost is therefore not yet established (see SCH_PEDICULARIS_SHAMA_VISITOR_EQUIVALENCE_LIMITS_V1.md). Most importantly, the 2015 manipulation changes a protection mechanism rather than randomizing exsertion or selectively excluding seed predators while bract water is held constant. It cannot be relabelled as the registered antagonist G intervention in the crossed SCH experiment.

Crucially, the **same 2015 experiment** contains a direct cross-endpoint ecological pattern (original Table 2). For the combined puncture-plus-drainage treatment, the pooled treatment effect was not detected for *initial* seed set (chi-square = 0.014, df = 1, P = 0.906), whereas effects were detected for *final surviving* seed set (chi-square = 16.710, df = 1, P < 0.0001) and *seed predation* (chi-square = 92.808, df = 1, P < 0.0001). The **site-by-treatment interaction** was supported for seed predation (chi-square = 36.782, df = 5, P < 0.0001) but not detected for final seed set (chi-square = 4.913, df = 5, P = 0.4265) or initial seed set (chi-square = 1.032, df = 5, P = 0.960). Thus, geographically heterogeneous effects on seed damage coexist with an overall treatment-associated surviving-seed response **without a detected geographic interaction at the final-fitness stage**. This is a biologically informative *difference in source test-detection patterns*, not evidence that final-seed effects are uniform among sites or that the predation and fitness interaction coefficients differ statistically. Neither response-specific power nor matched raw-capsule covariances are available to distinguish compensation from measurement differences. Source-level values and independent chi-square arithmetic are audited in SCH_PEDICULARIS_2015_REAL_CROSS_ENDPOINT_DEFENCE_MOSAIC_V1.md.

A third independent article, Xia, Sun and Liu (2013; doi:10.1098/rsbl.2013.0387), reported a density-by-patch-size pattern in seed predation, compatible with ecological context changing attack pressure. The 2011 design contained **11 spatial patches** (five sparse and six dense), not thousands of independent patches: the much larger denominator degrees of freedom printed for capsule-level models cannot independently certify cluster-robust spatial inference. This is a context precedent, **not** a new manipulated exsertion response, and its public raw workbook is not presently available in our source-checked analysis. We therefore neither derive new patch-level effect estimates nor attribute an optimum shift to that observational context contrast.

Together, these sources distinguish three biological objects that a single phrase such as "stronger enemy selection" could conceal:

1. **Pressure:** the average probability of an attack or seed loss in a patch, without conditioning on exsertion.
2. **Trait discrimination:** how early attack probability changes *with assigned exsertion within a patch*, at a specified bract-water and predator-exposure state.
3. **Fitness translation:** how initial seed development, damage, completely destroyed or unresolved fruits, and surviving mature viable seeds convert the interaction into the final exsertion–fitness surface.

A patch can exhibit greater mean seed-predator pressure yet a smaller high-minus-low exsertion fitness contrast, for example when attack approaches saturation. Equally, similar attack responses can generate different surviving-seed gradients if seed initiation and damage-to-survival translation differ. Both mechanisms are **prospective alternatives**, not results newly identified from the separate 2013–2016 studies. Thus spatial variation in antagonist pressure does not, by itself, establish stronger opposing selection or a change in either consumer's preferred trait state.

The ecological test that would advance the causal ladder is to manipulate several realized exsertion levels while independently varying verified predator access at fixed bract-water state, and to measure both early attack and final **intact mature viable seeds per assigned flower**. Natural pollen arrival can be measured in a linked sentinel cohort, but a same-flower pollen–seed covariance must not be inferred from separate cohorts. Flowers with entirely missing maturity outcomes require source-supported seed bounds; historical fully consumed capsules cannot be reclassified as observed zeros. Only this linked prospective evidence can test whether removing antagonists shifts the **whole reproductive optimum** toward higher exsertion, a *state-specific* optimum shift rather than automatic identification of pure function optima or the SCH conflict budget L.

**Evidence boundary:** observational exsertion–consumer associations (2016), experimentally heterogeneous puncture-plus-drainage effects (2015), and observational patch-context variation (2013) are authentic and complementary; they do **not** constitute one crossed z-by-pollinator-by-predator experiment, and none can be promoted to a measured L or downstream SLK architecture value. The formal data provenance and source-audit calculations remain in the repository's Pedicularis evidence ledgers; this subsection records their biological interpretation, not a new pooled analysis.


### 7.7 Experimentally changing one ecological input can reverse selection on one floral trait

The most informative **already executed factorial source** for distinguishing functional opposition from a merely intermediate observation is the one-population *Gymnadenia conopsea* experiment of Sletvold, Moritz and Ågren (2015; *Ecology* 96:214–221, doi:10.1890/14-0119.1). It crossed natural versus supplemental hand pollination with natural versus excluded herbivory. This is **one independent biological programme**, already counted once among the seven context-weight-shift clusters above; its four treatments, five measured traits and multiple pairwise contrasts are not extra independent systems. Original Table A2 contains the source-reported treatment-cell selection gradients and standard errors, now preserved in the SCH quantitative ledger.

**A real ecological sign reversal with one interaction held fixed.** With herbivores excluded in both arms, the reported selection gradient on flowering start is positive under open pollination (β = +0.094, SE = 0.031; source P < 0.01), favoring later flowering, and negative with supplemental hand pollination (β = −0.066, SE = 0.028; source P < 0.05), favoring earlier flowering. The source-measured point difference, supplemented minus open, is **−0.160** standardized-selection-gradient units. The exact standard error of this between-cell contrast cannot be reconstructed because the original coefficient covariance is not provided. The Cauchy–Schwarz bound nevertheless places the *largest mathematically compatible SE* at 0.031 + 0.028 = 0.059. Conditional on comparable, valid source standard errors and a normal-Wald approximation, even that worst-case covariance yields a 95% interval of approximately [−0.276, −0.044] and a two-sided nominal P upper bound of approximately 0.0067. This interval is not the original authors' factorial-ANCOVA interval, a randomization-test confidence interval, or an adjustment for searching all twenty single-factor comparison edges. A conservative twenty-edge Bonferroni upper P bound of approximately 0.134 does **not** establish familywise significance. Thus the empirical single-edge result is substantial, but its discovery and multiple-testing status must remain visible.

In the same source, flowering-start selection under **natural pollination and natural herbivory** is near zero (β = −0.0042, SE = 0.054). That value is neither proof of precisely balanced functional optima nor proof of zero selective pressure. The factorial treatment-cell estimates imply a pollination-associated positive flowering-time contribution of roughly +0.16, and a herbivory-associated negative contribution of roughly −0.09 to −0.10, producing a weak observed net coefficient. The difference-in-differences in the four source point estimates is −0.0042; this is only a descriptive additive reconstruction. An equivalence margin or a covariance-aware test of zero interaction is not available from Table A2.

**The same ecological interaction produces a different trait outcome.** The orchid's spur-length axis exhibits positive source-point pollinator and herbivore contributions: the two animal interactions can both favor longer spurs instead of opposing one another. The herbivore-excluded spur-length gradients are +0.077 (SE 0.035; source P < 0.05) under open pollination and −0.042 (SE 0.029; not significant) under hand supplementation. Unlike flowering start, spur length does not show two individually supported opposite-sign selection estimates. A species-wide designation of pollinator–herbivore "conflict" would therefore obscure the ecologically decisive distinction between its **trait coordinates**.

Together, the factorial orchid study establishes a positive, source-bounded ecological reality check: **changing a single experimentally assigned interaction can reveal opposing directional selection on flowering time even when natural net selection is weak, and the same actors may instead reinforce selection on a different floral trait**. This directly rejects a restrictive interpretation that reversal necessarily requires several ecological factors to change simultaneously or a demonstrably nonadditive interaction. But the floral phenotypes were measured rather than assigned; experimental manipulation of pollination and herbivory identifies changed selective *regimes*, not causal do(z) component optima, an interior reproductive-fitness optimum, pure function-specific objectives, the SCH conflict budget L, or a downstream SLK architecture payoff.

The exact source Table A2 cell values, covariance-worst-case calculation and all-cell caveats are preserved in data/SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv, docs/SCH_GYMNADENIA_SINGLE_FACTOR_REVERSAL_V1.md, and docs/SCH_GYMNADENIA_COVARIANCE_ROBUST_GRADIENT_CONTRAST_V1.md. The unchanged source identity is doi:10.1890/14-0119.1, Ecological Archives E096-022 Appendix A. This source is not a new held-out programme and does not revise the frozen H2 reversal-prevalence denominator.



### 7.8 Independent pollination-treatment programmes: strong selection changes need not reverse sign

To test whether the Gymnadenia ecological message extends to **independent published plant systems without requiring a directional reversal**, we used the already frozen V27 numerical source records from three separately studied pollination-supplementation programmes: Dactylorhiza lapponica (Sletvold, Grindeland & Ågren 2010; doi:10.1111/j.1469-8137.2010.03296.x), Primula alpicola (Chen, Zhang & Li 2017; doi:10.1038/s41598-017-13340-0), and Trillium discolor (doi:10.1002/ajb2.16101). All source-eligible within-year open-versus-supplemented comparisons were retained **regardless of their sign**: five Dactylorhiza trait axes, four Primula axes, and five Trillium trait-by-year comparisons, for **14 edges** across **three independent biological programmes**. The two Trillium field years are not independent published programmes. This audit is secondary and exploratory; it does not update the outcome-blind V26 design classes, V27 programme q values, or the frozen H2M1 primary gate.

A trait's selection response under a pollination regime was defined as the *difference in reported within-regime selection gradients* (open minus supplemented), never as a source-free pooled coefficient across species. The covariance of the two original gradient estimators is generally unavailable. Since their difference cannot have an SE larger than the sum of the reported marginal SEs, a conservative normal approximation bounds each contrast while allowing arbitrary covariance. We protected the **complete 14-edge family** with a two-sided Bonferroni critical value approximately 2.9137 (nominal familywise alpha=.05), conditional on valid original SEs, comparable estimands within each pair and normal-Wald behavior.

Two independent orchid/herb contrasts are robust even to plausible decimal rounding of the original reported coefficients. In **Dactylorhiza**, selection on spur length changes from +0.300 (SE 0.068) under open pollination to −0.024 (SE 0.037) after supplementation. The open-minus-supplemented difference is **+0.324** with covariance-worst-case SE upper bound 0.105; the reconstructed conditional 14-edge simultaneous normal interval is approximately **[+0.018,+0.630]**. In **Primula**, flowering-start selection is +0.194 (SE 0.035) under open pollination versus −0.012 (SE 0.031) under supplementation. Its difference is **+0.206**, worst possible SE 0.066, and simultaneous interval approximately **[+0.014,+0.398]**. The corresponding upper bounds on Bonferroni-adjusted normal P are approximately 0.0284 and 0.0252. Both original articles independently reported pollinator-mediated selection effects; this reanalysis instead asks what can be guaranteed across a full frozen subset with no guessed pairwise covariance.

For **Trillium**, open-minus-supplemented petal-size selection in 2020 is **−4.41**, from −3.94 (SE 1.2) and +0.47 (SE 0.29) on the original *conditional Poisson* scale. Treating the printed figures as exact, the covariance-worst-case SE upper bound is 1.49 and the 14-edge normal interval is approximately **[−8.752,−0.069]**. However, the printed open-arm SE 1.2 has only one decimal place, so a stricter coefficient/SE rounding envelope expands the maximum possible SE to 1.545 and the printed-data-only familywise guarantee **no longer excludes zero**. The original author's same-year petal-size treatment interaction, **−4.41 (SE 1.23, P < 0.0001)**, independently supports a large treatment-associated contrast; its direct source test is distinct from our deliberately worst-case reconstruction. We do not silently infer other source contrasts: the 2020 Trillium display-height Table 1 printed treatment contrast does not equal subtraction of its two printed arm coefficients, so that inconsistency is retained as a source caution, not repaired from conjecture.

These results reveal a more general ecological distinction than merely comparing the number of sign reversals. Neither Dactylorhiza nor Primula has an axis with two *individually* statistically supported opposite-sign treatment gradients in the frozen V27 primary readout; Trillium's two primary all-context supported reversals arise only after combining different year/context cells, whereas its source-defined within-year reversal diagnostic is zero. Yet meaningful **magnitude changes** are documented in each study. This shows that an absence of strongly supported complete reversal does not imply that the selective environment was insensitive to pollination. The studies do not establish a species-wide prevalence, a shared unit-normalized pooled effect, or a unique evolutionary outcome.

Biological identification remains limited. The Primula open arm includes **both long- and short-styled morphs**, whereas supplemental pollination was performed **only on long-styled plants** because hand pollinating short-styled plants risked flower damage. The original authors did not find morph differences for most measured characteristics, but did not establish equivalence of their trait–fitness slopes. Primula therefore supplies a published, statistically bounded **treatment-associated** response, not an unqualified pure causal effect of pollen alone. The 2019 correction (doi:10.1038/s41598-019-43381-6) amended Figure 1 styling and a Table 3 symbol, not the Table 2 linear coefficients used here. Dactylorhiza's source reports only minor effects of herbivory on the measured selection, so its spur response is not itself proof of pollinator–herbivore conflict. Trillium's conditional Poisson coefficient must not be numerically pooled with the linear selection gradients.

**The falsifiable ecological extension is that changing the ecological interaction regime may alter the *magnitude* of net trait selection substantially before any bidirectionally supported sign reversal appears.** This is not a direct z-manipulation result: all three experiments changed the pollen environment but observed rather than randomly assigned the focal phenotypes. Nor does it demonstrate pure functional optima, the SCH shared constraint loss L, or downstream SLK architecture value. The complete fourteen-pair receipt, exact arithmetic, rounding sensitivity and source-specific caveats are in docs/SCH_H2_THREE_PROGRAMME_POLLINATION_SELECTION_V1.md and scripts/audit_sch_h2_cross_programme_pollination_edges.py.



### 7.9 From a striking reversal to a four-programme ecological response spectrum

A complete, independent-source extension of the Gymnadenia factorial and preceding three-programme pollen-supplementation comparison reveals a more informative biological question than "how frequently does selection reverse direction?" **Does the same pollination change alter a trait's selective environment even when strong reversal evidence is absent?** The source-eligible family consists of every matched open-versus-hand-supplemented pollen contrast for the five Gymnadenia traits in **two fixed herbivory regimes**, plus the previously frozen **14 same-year floral-trait comparisons** from Dactylorhiza lapponica, Primula alpicola and Trillium discolor. The combined secondary family therefore has **24 within-source selection-gradient edges**, but **four independent published biological programmes**, not 24 independent replicated experiments. The original V26/V27 heldout study classifications and their primary q values are unchanged.

Within a particular trait and fixed herbivory/year context, we distinguish three measurable objects: (i) an **estimated sign change** between the two point gradients; (ii) **two independently supported but opposite-sign treatment-cell gradients**, assessed by the source SEs at an ordinary nominal threshold; and (iii) an identifiable **difference between the two estimated gradients**, with unknown covariance bounded by the sum of reported SEs. Because the third statistic is conditional on source-SE validity and asymptotic normality, we apply a simultaneous Bonferroni critical value for **all 24 matched edges** and then separately perturb each printed coefficient and SE over its original decimal-rounding interval.

The full four-programme descriptive results separate sharply: **11/24** point pairs change sign, only **one** has individually source-SE-supported opposite signs (the previously reported Gymnadenia flowering-start contrast with herbivores excluded), **two** open-versus-supplemented differences clear the **printed-value conditional 24-edge normal-Wald simultaneous bound**, and **zero** remain certified under worst-case **source decimal rounding**. The printed-value contrasts are Dactylorhiza spur length (+0.324; maximum covariance-compatible SE 0.105) and Primula flowering start (+0.206; maximum SE 0.066), with 24-edge adjusted normal-P upper bounds approximately 0.0487 and 0.0432. The Gymnadenia +0.160 flowering-start contrast has one-edge upper P approximately 0.00669, but this is not a 24-edge familywise certificate. The original source directly documents its significant positive and negative cell gradients; neither the original biological observation nor the previous *one-edge* and *14-edge* analyses is overwritten.

The absence of a decimal-rounding-robust 24-edge certificate is an important sensitivity outcome, **not evidence that no biological effects occurred**. Adding a fourth study and ten legitimate source comparisons to the previously analysed 14-edge family increases the multiple-testing burden. It does not change any original fitness measurement or invalidate the original study-specific treatment interactions. In particular, the original Trillium 2020 petal-size treatment test is reported directly by its authors (P < 0.0001), although the corresponding conservative subtraction of source-printed cell coefficients is sensitive to covariance and source precision. Differences across Trillium conditional Poisson models, Dactylorhiza standardized linear selection, Primula morph composition and Gymnadenia factorial backgrounds prohibit a pooled cross-species beta. The 24 observations represent different trait/context comparisons and must not be presented as 24 natural-system replications or as a population prevalence denominator.

The empirical implication for SCH is therefore **trait-axis-specific sensitivity to ecological context**, not a universal tendency to reverse selection. Across separately executed field studies, a point sign flip, two individually significant opposite directions, and a demonstrable change in selection magnitude are three non-equivalent evidential outcomes. Each supports a different ecological statement. Strong pollination-mediated trait selection can attenuate toward a poorly resolved zero without a supported opposite direction; the same source animals can reinforce selection on some axes while opposing selection on others, as Gymnadenia explicitly shows. Neither observation identifies an experimentally assigned trait optimum, pure functional objectives, or the downstream shared-constraint loss L. The complete source-matched analysis and claim boundaries are in docs/SCH_FOUR_PROGRAMME_POLLINATION_SELECTION_SPECTRUM_V1.md and scripts/audit_sch_four_programme_selection_spectrum.py.



### 7.10 Compensation and phenological debt: a different ecological route to selection

A further independent **experimental example already in SCH's H2 source ledger** resolves a more mechanistic question: must a change in floral selection arise because pollinators or antagonists change their *preferences for flowers*? In *Lythrum salicaria*, Thomsen and Sargent (2017; *Annals of Botany* 119:1295–1303; doi:10.1093/aob/mcx026) experimentally simulated vegetative herbivore damage by **clipping apical meristems** and compared floral architecture, phenology, seed output and pollen supplementation. Its selected field plants were initially randomized to clipping versus control, but eight naturally damaged control stems were subsequently reassigned to the clipped source group; the published contrast is therefore not a completely preserved intention-to-treat estimate. This is **one independent study**, not a new V27 pollen programme or an extra replication added to the four-study pollination-only family.

**The non-obvious observed pattern is a divergence between mean phenotype and the direction or strength of selection on that phenotype.** Following damage, mean inflorescence number increased from **5.4 to 8.0 per plant** (+48.15%) and total mean flower production rose from 825 to 1048 (+27.03%), yet **net directional selection for still more inflorescences weakened** from β=+0.47 (SE 0.07) in controls to β=+0.20 (SE 0.07) in clipped plants. Conversely, clipping delayed mean flowering onset from Julian day 191 to 196 (**5 days later**), while net directional selection for *earlier* flowering became stronger, moving from β=−0.03 (SE 0.08) in controls to β=−0.28 (SE 0.06) in clipped plants. Mean flowering end was day 236 in both source groups: the differences between separately reported group-average start and end dates imply calendar-window proxies of roughly 45 versus 40 days. These are NOT observed individual flowering-duration distributions or fitted tests of duration.

The original **direct ANCOVA** damage-by-trait selection contrasts support differences in both axes: **Δβ(control−clipped)=+0.27 (SE 0.10; source P<0.01)** for inflorescence count and **+0.25 (SE 0.10; source P<0.05)** for flowering onset. Height gave +0.11 (SE 0.11; not significant). A separate, non-preregistered three-damage-term Bonferroni normal-Wald calculation using directly published contrast SEs excludes zero for the two reported damage effects; only the inflorescence-number effect survives a stricter source-decimal-rounding envelope. Across all nine original direct interaction terms (damage, pollen, damage-by-pollen for each of three traits), none is certified by the corresponding conservative nine-test normal Bonferroni diagnostic. None of these secondary adjustments replaces the source author's reported ANCOVA tests or implies causal isolation of compensatory regrowth from other treatment-induced pathways.

**Pollen limitation and selection on a particular flower trait were decoupled.** Hand-supplemented flowers produced on average **17.4% more seeds** than naturally pollinated comparison flowers, yet the degree of pollen limitation did not detectably differ between damage states (source P=0.2718) and the paper did not detect significant **pollination-treatment-by-trait** or **pollination-by-damage-by-trait** effects for the measured inflorescence number, height and flowering-start gradients. This is not demonstration of pollinator neutrality, equivalence or complete lack of pollen limitation. Rather it is positive original experimental evidence for pollen limitation alongside a different, experimentally induced source of trait-selection heterogeneity: vegetative disturbance and the inferred tolerance/regrowth response.

This contrasts with the previously discussed *Gymnadenia conopsea* factorial example, in which manipulating pollen supply within a fixed herbivory treatment shifts selection on flowering start between source-significant opposite gradients. In *Lythrum*, apical damage reorganizes the average plant phenotype and its subsequent trait–fitness association **without a detected pollinator-mediated selection shift on those traits**. These are distinct ecological routes for a multifunctional flower to acquire different realized selection gradients: **changes in mutualist-associated selection** versus **changes in developmental allocation, phenology and damage tolerance**. Both systems are real published experiments, but the trait values themselves were not randomized; therefore neither directly identifies SCH pure-function optima, the five-rank causal compromise, loss L, or SLK architecture value.

The study also illustrates why compensatory phenotypic growth should not be confused with adaptation or causal mediation. Pollen supplementation was implemented as **429 matched flower pairs within plants**, not independent whole-plant pollinator states. Treatment-specific trait standardization and fitness normalization, reassignment of eight stems, and unavailable matched plant data limit transport and mechanism identification. The source-frozen Table 1 phenotype and Table 2 selection results, exact test directions and the ecological-fork audit are in docs/SCH_LYTHRUM_COMPENSATORY_REGROWTH_SELECTION_V1.md and scripts/audit_sch_lythrum_compensatory_regrowth_selection.py.



### 7.11 Stage-dependent ecological roles: aligned attraction can conceal antagonistic fitness translation

A third source-distinct experimental route addresses a core ecological ambiguity: **an adult insect can be both a pollinator and the parent of damaging herbivores, so the sign of its response to a floral cue is not the sign of its net reproductive contribution**. Knauer and Schiestl (2017; *Evolutionary Ecology* 31:285–304; doi:10.1007/s10682-016-9878-8) exposed *Brassica rapa* plants to bumblebees, cabbage butterflies (*Pieris brassicae*), or both in controlled cages. The butterflies pollinated flowers as adults but laid eggs whose caterpillars damaged plants. Thus a butterfly-only cage is not an antagonist-only G state, and the experiment varied consumer identity/composition without randomizing flower size or scent emission. The source already belongs to the SCH H2 selection evidence universe; reading its original behavioral Tables 1 and 3 beside its previously frozen seed-selection Table 2 supplies **one** linked published ecological system, not a new independent cluster or measured two-function optimum.

**Both shared attraction and antagonistic recruitment are directly visible in the same nine-trait source.** Across the original Table 1 models, **two of nine** measured floral coordinates—**corolla size** and **phenylacetaldehyde**—had positive associations with **all three** outcomes: bumblebee visitation, cabbage-butterfly visitation, and butterfly oviposition. For corolla size, the source reported receiver β ± SE of +0.24±0.05, +0.15±0.04, and +0.45±0.16, respectively (each nominal P<0.05). For phenylacetaldehyde, these three responses were +0.15±0.06 (P=0.010), +0.09±0.04 (P=0.029), and +0.41±0.17 (P=0.016). This is **not a 27-test familywise demonstration**: these are original, nominal source tests for nine trait axes and three receiver classes, not an ecological prevalence rate or randomized do(z) manipulations. Moreover, counts of flower visits and the binary presence of eggs are fitted on distinct scales; these coefficients are not additive functional fitness weights.

**A shared oviposition cue need not produce negative net selection on that cue.** Original Table 2 still shows **positive net seed-fitness selection on corolla size in all three insect regimes**: bumblebee only β=+0.22±0.04 (P<0.001), bee plus butterfly β=+0.22±0.08 (P=0.005), and butterfly only β=+0.26±0.09 (P=0.007). The species-wide claim "larger corollas are selected against because butterflies lay eggs on them" would therefore be contradicted by the observed net selection, notwithstanding genuine oviposition association. Phenylacetaldehyde had a positive source-supported net gradient only in bee-only cages (+0.15±0.05, P=0.006), compared with an unsupported negative point estimate in mixed cages (−0.09±0.08, P=0.27) and unsupported positive estimate in butterfly-only cages (+0.08±0.10, P=0.18). The original authors **did not detect a directional trait × insect-treatment ANCOVA interaction**, so differing cell significance must not be promoted to an established between-regime selection reversal or equality claim.

**The conflict-compatible cost reappears later, in the reproductive and joint-trait stages.** The original source fitted positive plant seed-production associations for bee and butterfly flower visits (+20.5±4.8 and +6.8±2.0, respectively), but a large negative caterpillar-infestation association (−104.5±19.0). Bee-visit effects were weaker in infested plants (source visit × infestation β=−18.9±9.5, P=0.046); all are original source model terms, not newly reconstructed causal mediation paths. In its mixed-insect cages, the original Table 3 also reported **negative correlational selection** between corolla size and phenylacetaldehyde, γ=**−0.17±0.08, P=0.029**. Crucially, this is only *one nominally significant result in the complete original 18 source Table 3 interaction tests*; it **does not survive** a conservative 18-test Bonferroni threshold, and the authors did not detect a between-regime ANCOVA change in correlational selection. It is an ecological candidate for multivariate, combination-dependent constraint, **not** a familywise-certified transition in fitness surface geometry.

An independent original nonadditive-selection analysis does supply a different, source-fitted comparison, conditional on the authors' additive reference model (mixed-regime gradient = mean of the two single-consumer gradients). For phenylacetaldehyde, the reported departure from that reference was **−0.20±0.08, P=0.009**; for 1-butene-4-isothiocyanate the departure was **+0.19±0.08, P=0.018**. Both are author-fitted source contrasts, not p-values reconstructed by pretending the separate gradients have zero covariance. The printed Table 2 coefficients reproduce their point departures to source rounding, but no study-wide multiplicity promotion or isolation of consumer preference change is inferred.

**A possible route out of receiver overlap is visible but not yet proven.** The scent (E)-α-farnesene had a positive bumblebee visitation association (+0.18±0.05; P<0.001), whereas butterfly visitation (−0.05±0.04; P=0.19) and oviposition (−0.16±0.16; P=0.35) associations were not detected. This is a candidate receiver-biased communication channel, **not** verified selectivity or equivalence of a missing butterfly response. Demonstrating a BITA functional partition would require independently assigned signals, a predefined butterfly-neutrality/equivalence margin, pollination fitness on the same scale, dimensional costs and a comparable architecture; none is available.

The biologically non-obvious synthesis is that **receiver-level alignment and reproduction-level opposition can coexist**, even where a shared attractive trait retains a positive net directional selection gradient. Functional conflict cannot be diagnosed from an insect's taxonomic role, from the sign of an oviposition correlation, or from one univariate flower–fitness slope alone. It may involve **adult-benefit versus offspring-damage translation and selection on combinations of floral signals**, or may be fully outweighed by positive pollination benefit at the observed trait range. This source is more directly linked in one study across behavioral and reproductive stages than the separate-source *Pedicularis rex* triangulation, but still provides **no causal** randomized floral trait z × selective pollinator P × predator G reproductive surface, no bounded pure-function optima, and no observed SCH conflict loss L or downstream SLK architecture payoff. The nine-axis sign-blind source audit and inferential limits are in docs/SCH_BRASSICA_2017_MULTISTAGE_RECEIVER_ROLE_CONFLICT_V1.md and scripts/audit_sch_brassica_multistage_receiver_geometry.py.


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
