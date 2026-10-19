# SCH shared-trait compromise figure map v1

## Figure 1 — Theory: why one shared coordinate can produce compromise

Four aligned panels:

**A. Architecture.**

```text
function 1 ---\
               >--- shared trait z
function 2 ---/
```

**B. Pure function objectives.** Plot `F1(z)` and `F2(z)` with theory-level optima:

```text
z_F1*
z_F2*.
```

**C. Ideal combined benchmark.** Plot the theory-level shared surface / mismatch loss with `z_C,theory*` between the pure optima.

**D. Theory intervention prediction.** Weakening function 2 moves the theory optimum toward `z_F1*`; weakening function 1 moves it toward `z_F2*`.

Include:

```text
L_compromise,theory*
  = [a b / (a + b)] (z_F1* - z_F2*)^2.
```

Primary message: the theory explains why shared dimensionality can create a mismatch penalty; it does not claim that pure function optima are automatically observed in the factorial experiment.

## Figure 2 — Local mechanism identification

Use the floral `A x antagonist x pollinator` eight-cell design.

Display:

```text
M_A(g)
G_A(p)
B_A
J_A.
```

Separate informational overlap from functional reproductive conflict.

Primary message: both audiences responding to a trait is not enough; selective intervention is required to identify opposing causal contributions.

## Figure 3 — Empirical compromise geometry

Show the multi-level `z x P x G` design with at least five illustrative `z` levels.

Plot the four state surfaces:

```text
W00(z)
W10(z)
W01(z)
W11(z).
```

Mark the directly identified optima:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

Show the causal shifts:

```text
G off -> z_C* toward z_P*
P off -> z_C* toward z_G*.
```

Also show opposite pollinator- and antagonist-component gradients near `z_C*`.

Add an explicit note:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

Primary message: the empirical experiment identifies state-specific compromise geometry without overclaiming pure function optima.

## Figure 4 — Real-world evidence and claim ladder

Place source classes along:

```text
L0 multifunctionality / shared exposure
L1 local functional conflict
L2 state-specific compromise geometry
L3 causal balance
L4 evolutionary maintenance
L5 historical architecture.
```

Highlight:

- **Four-programme selection response spectrum, a study-grain graphic, not a prevalence graph:** show four horizontal rows labelled Dactylorhiza (5 same-year pairs), Primula (4), Trillium (5 across two years), and Gymnadenia (10 pairs across two herbivory backgrounds, five axes total). In each row, preserve distinct markers for the three evidential classes rather than conflating their meaning: point sign differences (3,2,3,3), both opposite cell slopes individually supported (0,0,0,1), and full 24-edge conditional normal Bonferroni printed-value difference (1,1,0,0). The family contains 24 pairs from only FOUR independent studies. The **source-decimal-rounding-robust** 24-edge total is ZERO; show it explicitly and separately from the legacy 14-edge family, where Dactylorhiza and Primula remain rounding robust. Do NOT represent 11/24 as an ecological prevalence estimate or the 24 statistical edges as independent plants/systems.
- Place an accompanying annotation: *a point sign flip, a supported pair of opposite slopes, and a change in slope between treatments are separate empirical claims*. Gymnadenia supplies the one individually supported reverse-sign pair, though its nominal conditional between-cell contrast does NOT clear a 24-edge familywise correction. Trillium supplies an original source-reported treatment contrast that is NOT inferred from the common covariance-worst-case procedure; preserve its different conditional Poisson scale. No manipulated floral phenotype optimum, general L, BITA functional partition or SLK architecture value is identified by this panel.
- **Three-programme independent corroboration strip**, from the already-frozen V27 published numeric field sources (not new studies): Dactylorhiza lapponica spur-length open minus pollen-supplemented selection **+0.324**; Primula alpicola flowering-start **+0.206**; Trillium discolor 2020 petal-size **−4.41** (Poisson conditional coefficient, NOT the same units as the other two). Draw *paired within-year selection gradients* with their original SEs and a second smaller annotation: 14 predeclared-source-eligible exploratory edges, Bonferroni nominal corrected bound passing for both Dactylorhiza and Primula even under source-value rounding. The printed Trillium source-value bound barely passes under exact printed figures but fails worst-case one-decimal SE rounding; its **original fitted treatment contrast P < 0.0001** remains independently reported. Explicitly distinguish a treatment-associated **gradient magnitude change** from two individually significant *opposite-direction* gradients. These three programmes contain **no within-year two-sided supported sign reversal** under their own frozen V27 criterion. Primula's open group mixes style morphs but the supplemented group contains long-styled plants only; draw that caveat under the panel.
- The three-programme strip plus the factorial Gymnadenia panel supports "selection magnitude may respond without a bidirectionally significant sign reversal", NOT a four-study meta-analytic pooled number or general prevalence estimate. Retain the original 16-cluster ledger, original V27 holdout primary inference, and all SCH causal z-optimum gates unchanged.
- **Experimental ecology panel: Gymnadenia conopsea**, original Sletvold, Moritz & Ågren 2015, Ecological Archives Table A2. Show FOUR genuine phenotypic-selection treatment cells for flowering start on ONE axis, with β ± source SE: open pollination + natural herbivory −0.0042 ± 0.054; open + herbivores excluded +0.094 ± 0.031; supplemented + natural herbivory −0.160 ± 0.056; supplemented + herbivores excluded −0.066 ± 0.028. Mark the ONE-factor, fixed-herbivore comparison +0.094 versus −0.066 and its source-point contrast −0.160. Annotate that any admissible coefficient covariance implies SE(contrast) ≤ 0.059, yielding a **conditional nominal** 95% normal-Wald interval approximately [−0.276,−0.044], NOT the published contrast CI; the exploratory 20-edge family is not certified. Phenology itself was not randomized.
- Place a separate small **spur-length** strip from that same experiment: the two animal pathways have positive source-point contributions (reinforcement), while the apparently negative herbivore-excluded hand-supplemented spur coefficient (β=−0.042 ± 0.029) is unsupported. Do NOT promote this axis to bidirectionally supported reversal, another independent source, or pure-function optima.
- This pair of panels is the concrete ecological message of Figure 4: *one ecological regime can mask opposing trait selection, but the conflict/reinforcement class is trait-specific even within one species*. Preserve the 16-cluster denominator unchanged.
- *Pedicularis rex* evidence distinction (already counted among SCH conflict-signature clusters): 2016 **observational** exsertion -> pollen receipt (+) and seed predation (+); 2015 **experimentally manipulated puncture-plus-drainage** -> seed predation (+) with geographically heterogeneous effects; 2013 **observational** 11-patch density/size context. Render these as THREE separate source-labeled horizontal lanes, **not connected into a fictitious experimental z x G surface**. The common biological interpretation is an attractive-versus-vulnerable floral geometry with spatially contingent realised reproductive consequences, whereas neither pure component optima nor L are yet identified.
- Add a small source/causal-unit panel distinguishing attack prevalence, trait-conditioned attack slope and surviving viable-seed fitness.
- Inside the **single 2015 causal treatment package** lane, show the published three-endpoint comparison, marking site x treatment as detectable for seed predation (P < 0.0001) but not detected for final viable seed set (P = 0.4265) or initial seed set (P = 0.960). Plot as a **Table 2 model-test classification**, not invented original percentage curves, and label non-rejection as NOT EQUIVALENCE. Cross-endpoint P comparisons do not directly test equality of effects.
- Add a distinct **Shama-only Table 1 visitor uncertainty** strip: pollinator treatment term β=0.012, SE=0.224, approximate 90% Wald CI [−0.356,0.380] on logit scale, and YEAR × TREATMENT still included. Label VISITOR EFFECT NOT DETECTED — EQUIVALENCE NOT ESTABLISHED. Do not draw zero-width pollinator costs, pool this with six-site fruit tests, or use source main terms as a two-year marginal response.
- Do not use any of the synthetic 277/856 patch thresholds as observed seed-predator effect sizes or field recruitment estimates.
- Pérez-Barrales: case-level stabilizing compromise;
- Theis & Adler: negative side of the fitness surface;
- Primula: context-dependent maintenance and microevolution;
- Brassica experimental evolution: functional-weight redirection;
- Nicotiana: same-coordinate reality and execution candidate;
- Ficus: historical extension, not the contemporary mechanism proof.

Primary message: literature establishes ecological reality but does not substitute for the identifying experiment.

## Figure 5 — Hand-off to BITA

Show:

```text
SCH empirical
z_P*, z_G*, z_C*
-> measured one-dimensional constraint

BITA
add y
-> x* moves toward z_P* by default
-> preferential functional loading
-> functional differentiation.
```

Alongside this, show the **separate theory benchmark**:

```text
Delta_mod,theory
  = [a b / (a + b)] (z_F1* - z_F2*)^2 - K.
```

If a pure `z_F1*` is independently identified, show it as an optional stricter release target with a different line style or panel annotation.

Primary message: Chapter 1 supplies a measured state-specific reference for Chapter 2, while the pure-function quadratic remains a theory-level upper-bound framework.
