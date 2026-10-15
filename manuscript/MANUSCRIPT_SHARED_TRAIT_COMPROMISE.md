# Multifunctionality is not functional conflict: identifying compromise on a shared trait axis

**Canonical SCH full-paper science source**

**Target class:** conceptual / methodological ecology

## Abstract

Multifunctional traits are often described as evolutionary compromises, but multifunctionality alone does not establish conflict. Two functions may use the same phenotypic coordinate while favoring the same state, and even when experiments recover different reproductive optima across ecological contexts, those state-specific optima are not automatically the pure optima of the focal functions. SCH separates these inferential levels. For a shared trait coordinate \(z\), theory may define pure function-specific objectives with optima \(z_{F1}^*\) and \(z_{F2}^*\). A crossed empirical experiment instead identifies state-specific reproductive surfaces \(W_{00}(z),W_{10}(z),W_{01}(z),W_{11}(z)\), with directly estimable optima \(z_P^*\), \(z_G^*\), and \(z_C^*\). Because consumer-independent and direct trait effects can remain in every state, \(z_P^*\neq z_{F1}^*\) and \(z_G^*\neq z_{F2}^*\) in general. We therefore define a promotion ladder from multifunctionality to local functional conflict, state-specific compromise, and—only when component contrasts are context-stable—empirical pure-function optima. We then translate this ladder into literature-observable signatures before prioritizing a focal causal experiment. A source-adjudicated synthesis currently contains 16 independent biological clusters: five direct conflict-signature clusters, seven context-weight-shift clusters, two aligned/no-conflict controls, one shared-tracking conflict candidate, and one sequential-filter boundary. One manipulated system additionally recovers a combined-intermediate/compromise surface, but complete bounded pure-function optima remain unidentified. A strict quantitative inventory contains four strong same-coordinate conflict designs at different levels of numerical completeness, but no random-effects stratum currently satisfies the frozen compatibility and uncertainty gate. These results support recurrence of conflict-compatible and compromise-like geometry while showing that multifunctionality can also remain aligned and non-conflicted. They do not identify a general SCH conflict budget \(L\) or justify relabeling state-specific reproductive optima as pure-function optima. The residual empirical target is therefore sharply defined: selective multi-level \(z\times P\times G\) experiments are reserved for final causal state-surface reconstruction and optional pure-function promotion after the cross-system reality pattern has been established.

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

The strict quantitative inventory contains four strong same-coordinate conflict designs at different levels of numerical completeness: *Dalechampia*, *Silene*, *Fragaria*, and *Gymnadenia*. Exact component coefficients are currently recorded for *Dalechampia* and *Silene*. The *Fragaria* and *Gymnadenia* studies contain relevant factorial or treatment-specific information, but a valid shared contrast with its full uncertainty must be reconstructed before quantitative promotion.

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
