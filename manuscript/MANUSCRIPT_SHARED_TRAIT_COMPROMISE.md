# Multifunctionality is not functional conflict: identifying compromise on a shared trait axis

**Canonical SCH full-paper science source**

**Target class:** conceptual / methodological ecology

## Abstract

Multifunctional traits are often described as evolutionary compromises, but multifunctionality alone does not establish conflict. Two functions may use the same phenotypic coordinate while favoring the same state, and even when experiments recover different reproductive optima across ecological contexts, those state-specific optima are not automatically the pure optima of the focal functions. SCH separates these inferential levels. For a shared trait coordinate \(z\), theory may define pure function-specific objectives with optima \(z_{F1}^*\) and \(z_{F2}^*\). A crossed empirical experiment instead identifies state-specific reproductive surfaces \(W_{00}(z),W_{10}(z),W_{01}(z),W_{11}(z)\), with directly estimable optima \(z_P^*\), \(z_G^*\), and \(z_C^*\). Because consumer-independent and direct trait effects can remain in every state, \(z_P^*\neq z_{F1}^*\) and \(z_G^*\neq z_{F2}^*\) in general. We therefore define a promotion ladder from multifunctionality to local functional conflict, state-specific compromise, and—only when component contrasts are context-stable—empirical pure-function optima. A strong causal compromise result requires distinct state-specific optima, a supported interior combined optimum, predictable optimum shifts when each functional demand is selectively removed, and opposing functional-component gradients near the combined optimum. Existing literature establishes that shared traits can affect multiple ecological routes, opposing demands and compromise occur, and interaction regimes can redirect evolution; it does not substitute for the same-coordinate identifying experiment. SCH's contribution is an explicit claim ceiling: evidence for multiple functions should not be promoted to functional conflict, and state-specific optima should not be promoted to pure-function optima, without the corresponding causal gate.

**Keywords:** multifunctionality; functional conflict; compromise; causal identification; trait optimum; crossed intervention; promotion gate

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

## 7. Existing evidence: reality of the mechanism, not identification of the estimand

The literature provides strong ecological grounding. Shared floral traits can influence pollination and antagonism. Opposing selection on display traits and stabilizing net selection have been reported. Manipulated fragrance can increase antagonist attraction and lower reproduction without a compensating pollinator gain. Interaction regimes can shift morph frequencies and redirect multigeneration evolutionary trajectories.

These studies establish that the constituent biology is real: multifunctionality, opposing ecological effects, compromise-like outcomes, context dependence, and evolutionary redirection all occur.

They do not replace the same-coordinate crossed experiment required by SCH. A literature case with one pollinator result and another antagonist result cannot by itself identify \(z_P^*\), \(z_G^*\), \(z_C^*\), opposing component gradients, or the pure-function promotion gate in one biological system.

The systematic programme therefore plays a reality-check role rather than defining the estimand. Current workflow counts—hundreds of screened records and a much smaller strict linked subset—measure evidence coverage, not natural prevalence of conflict.

## 8. Empirical execution strategy

The empirical programme should proceed through qualification gates rather than choosing a charismatic system and forcing it through the framework.

**Dalechampia** remains a high-value compromise-surface candidate because published populations show opposing pollinator and seed-predator selection on shared floral structures. But the conflict is not species-wide, so population and season must be qualified before a full causal surface experiment.

**Nicotiana attenuata** remains a strong local shared-cue mechanism system because a floral attraction axis affects pollinator-mediated reproduction and antagonist-related processes. It is valuable for local conflict identification and later cross-framework handoff.

**Castilleja linariaefolia** remains a promising fallback where antagonist-to-seed pathways are short, but reversible focal-trait manipulation and selective consumer control require Stage-0 validation.

Aligned-optimum flower-orientation systems remain valuable negative controls precisely because they can demonstrate multifunctionality without conflict.

The preferred execution chain is therefore:

```text
qualify conflict-active context
→ validate reversible multi-level z manipulation
→ validate selective consumer interventions
→ fit W00(z), W10(z), W01(z), W11(z)
→ recover z_P*, z_G*, z_C*
→ test optimum shifts and opposing component gradients
→ optionally test context-stable component optima
→ export only justified quantities downstream
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

The framework is falsified for the declared conflict claim if the two functions favor the same tested state, if consumer manipulations do not shift the trait-fitness surface in the predicted directions, or if the apparent interior optimum disappears under the causal decomposition.

The pure-function promotion is separately falsified when component optima change materially across the alternate consumer state. In that case SCH retains context-dependent functional objectives rather than forcing context stability.

## 11. Claim ceiling

Current evidence supports:

```text
MULTIFUNCTIONALITY_REALITY_RECOVERED
CASE_LEVEL_OPPOSING_DEMANDS_RECOVERED
CASE_LEVEL_COMPROMISE_RECOVERED
STATE_SPECIFIC_CAUSAL_COMPROMISE_ANALYZER_READY
PURE_FUNCTION_PROMOTION_GATE_READY
```

Current evidence does **not** yet support:

```text
COMPLETE_CAUSAL_COMPROMISE_EXPERIMENT_EXECUTED
PURE_FUNCTION_OPTIMA_IDENTIFIED_BY_DEFAULT
HISTORICAL_TRAIT_SPLITTING_INFERRED
```

The latter claims require new biological evidence rather than stronger prose.

## 12. Conclusion

Multifunctionality is not functional conflict, and a context-specific reproductive optimum is not automatically a pure-function optimum. These are separate promotion steps with separate evidence requirements.

SCH turns compromise from an intuitive label into an identification problem. A strong claim requires opposing causal geometry on the same coordinate, a supported combined optimum, predictable shifts when each functional demand is removed, and opposing component gradients. A still stronger pure-function claim requires context-stable component optima rather than a relabelled ecological state.

This narrower paper is stronger because it stops before architecture value and evolutionary realization. Once conflict is identified, those downstream questions belong to SLK. Once multiple traits interact, mechanism allocation belongs to BITA. SCH's job is earlier and more basic: determine whether the conflict being transported downstream has actually been identified at all.
