# Multifunctionality is not functional conflict: an identification framework for shared plant traits

**Article type:** Viewpoint

## Summary

Multifunctional plant traits are often described as evolutionary compromises, but one trait serving several functions does not establish that those functions favor different trait states. We propose an identification framework that separates multifunctionality, opposing functional geometry, state-specific compromise and pure-function inference. A crossed trait-by-function design directly identifies ecological-state fitness surfaces and their optima; those state-specific optima are not automatically the pure optima of the focal functions because direct and background trait effects can remain in every state. Promotion to function-specific optima therefore requires a second, context-stability gate based on causal component contrasts. A source-adjudicated synthesis of 16 independent plant systems recovers both conflict-compatible signatures and aligned multifunctionality, frequent context-dependent weighting and one manipulated combined-compromise surface, but no system closes the full pure-function identification chain. We argue that this gap should change experimental practice: literature synthesis should establish recurrence and specificity, while final focal experiments should be designed only to recover the causal quantities that existing studies leave unidentified. The result is a falsifiable research agenda for deciding when multifunctionality truly implies functional conflict.

## 1. The inference problem hidden inside multifunctionality

Plant traits routinely face more than one biological audience. Floral size, orientation, colour, scent, reward and phenology can influence pollination, herbivory, seed predation, abiotic protection and other components of performance. This ecological multiplicity is central to plant evolution, and a long literature has shown that floral traits can have simultaneous roles in attraction and defence (Irwin *et al*., 2004), that herbivores can alter floral signalling and reproductive interactions (Schiestl *et al*., 2014), and that herbivory can change plant attractiveness to pollinators in context-dependent ways (Moreira *et al*., 2019).

Yet two statements that sound similar are not equivalent:

```text
one trait contributes to multiple functions
        ≠
the functions impose opposing causal geometry on that trait.
```

A trait can be multifunctional while all relevant functions favor the same state. Horizontal flower orientation, for example, can improve pollen transfer while also reducing rain damage rather than forcing the plant between opposed optima (Yu *et al*., 2021; Nakata *et al*., 2022). These systems are not awkward exceptions. They are the negative controls needed to show that a framework can distinguish multifunctionality from conflict.

A second promotion error appears after manipulative experiments. Suppose pollinator-present and antagonist-present treatments favor different values of the same trait. Those treatment-specific optima are legitimate empirical quantities, but they are optima of reproductive fitness under declared ecological states. They are not automatically the pure-function optima that appear in idealized compromise models. Direct physiological effects, unmeasured consumers and other background pathways can remain when either focal function is experimentally altered.

We therefore distinguish two promotion problems:

```text
multifunctionality
    →? identified functional conflict

state-specific reproductive optimum
    →? pure-function optimum.
```

The first asks whether functions actually pull a shared coordinate in opposing directions. The second asks whether a state-specific optimum can be interpreted as the optimum of a focal causal component rather than of an ecological mixture. Treating either arrow as automatic turns a biological hypothesis into a label.

Our aim is to make both arrows testable. The framework is deliberately plant-centered because floral and reproductive traits provide unusually rich opportunities for selective intervention: pollinator access, antagonist access, rainfall, herbivory, resource state and trait value can often be manipulated independently enough to reconstruct the relevant fitness geometry. But the logic applies to any shared plant trait for which focal functional channels can be selectively perturbed.

![Figure 1. Promotion ladder from multifunctionality to causal functional conflict and optional pure-function inference.](nph_viewpoint_figures/FIG1_PROMOTION_LADDER.svg)

**Figure 1. Promotion is a sequence of evidence gates, not a sequence of synonyms.** Level 0 establishes that one coordinate contributes to several functions. Level 1 requires opposing causal effects on the same trait contrast. Level 2 reconstructs state-specific compromise geometry. Level 3 requires selective-removal shifts and opposed causal components. Level 4 is an optional, stricter promotion to context-stable function-specific optima. Aligned multifunctionality is an expected negative class.

## 2. Theory targets and empirical targets are different objects

Let a shared phenotypic coordinate `z` contribute to two theoretical functional objectives,

```text
F1(z), F2(z),
```

with pure optima

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z).
```

Theory-level conflict exists when `z_F1* ≠ z_F2*`. A simple local benchmark represents the mismatch cost of sharing one coordinate by

```text
L(z) = a(z-z_F1*)² + b(z-z_F2*)²,
```

so the idealized minimum mismatch penalty is

```text
L_compromise* = [ab/(a+b)](z_F1* - z_F2*)².
```

This benchmark is useful because it makes the logic of compromise explicit: conflict is not merely the presence of two functions but the separation of their preferred states on a common coordinate. It also shows why the size of the separation and the relative weighting of functions matter.

The empirical problem is that the pure functions are generally not observed directly. A crossed experiment instead manipulates `z` while selectively varying two focal channels, here denoted `P` and `G`, and estimates four reproductive surfaces:

```text
W00(z), W10(z), W01(z), W11(z).
```

The directly estimable state-specific optima are

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

These objects are already valuable. If `z_P*` and `z_G*` are separated and the combined surface has a supported interior optimum `z_C*`, the experiment has reconstructed context-specific compromise geometry. But in general

```text
z_P* ≠ z_F1*
z_G* ≠ z_F2*.
```

Turning off one focal consumer does not guarantee that every other pathway has vanished. An ecological state is not a mathematical isolation operator.

This distinction matters because many verbal arguments about trade-offs jump directly from treatment-specific effects to pure functional demands. Doing so can exaggerate what has been identified and can hide a biologically interesting alternative: the focal functional objective itself may change with ecological context.

![Figure 2. Crossed state surfaces and the context-stability promotion gate.](nph_viewpoint_figures/FIG2_CROSSED_IDENTIFICATION.svg)

**Figure 2. Crossed experiments identify ecological-state surfaces before they identify pure functions.** The four state surfaces yield directly estimable contextual optima `z_P*`, `z_G*` and `z_C*`. Function-specific causal components are reconstructed by differencing state surfaces. Promotion to an empirical pure-function optimum requires the component optimum to remain stable across the alternate functional state within a prospectively declared equivalence bound.

## 3. A causal promotion ladder

### 3.1 Level 0: multifunctionality

The same declared trait coordinate influences more than one function or ecological route. This is a necessary starting point, not evidence of conflict. Floral orientation can contribute to pollen transfer and rain avoidance while both functions favor horizontal flowers (Yu *et al*., 2021; Nakata *et al*., 2022). A framework that labels such cases as trade-offs has no specificity.

### 3.2 Level 1: local functional conflict

Local conflict requires opposing causal effects on the same trait contrast and a common fitness scale. Floral traits often satisfy the biological prerequisites. Pollinators and antagonists can respond to the same display or scent coordinate (Irwin *et al*., 2004; Kessler *et al*., 2015), and direct experiments show that enhanced floral fragrance can increase florivore attraction and reduce seed production (Theis & Adler, 2012).

For a binary trait contrast `A`, a crossed `A × antagonist × pollinator` design can estimate whether pollinators increase the reproductive value of `A` while antagonists decrease it. This identifies opposed channel contributions near the tested contrast. It does not yet identify the location or depth of a nonlinear compromise surface.

Observational selection studies can also provide strong conflict signatures without satisfying this causal level. Pollination and pre-dispersal seed predation impose opposing selection on floral traits in *Castilleja linariaefolia* (Cariveau *et al*., 2004), geographic mosaics of opposing pollinator and seed-predator selection occur in *Pedicularis rex* (Sun *et al*., 2016), and sexually conflicting selection has been reported for floral traits in *Silene stellata* (Zhou *et al*., 2020). These studies establish that opposing selection is biologically real. Their inferential ceilings still depend on the exact experimental structure.

### 3.3 Level 2: state-specific compromise geometry

A multi-level trait manipulation is needed to locate optima rather than only local directions. The minimal geometry requires separated state-specific optima and a supported interior optimum of the combined surface. The manipulated spur-length experiment in *Satyrium longicauda* is particularly informative: male pollen export peaked at an intermediate manipulated spur length, female fitness was highest at the largest tested length, and total fitness was hump-shaped in one year (Ellis & Johnson, 2010). This is a strong combined-compromise signature on one coordinate.

But the same example illustrates why boundedness matters. The female response was highest at the largest tested spur treatment, so the upper side of the female function was not experimentally bracketed. An unbounded optimum cannot be silently turned into a fully identified pure-function optimum.

### 3.4 Level 3: causal compromise

An interior combined optimum is still not sufficient. Causal compromise requires showing that the location of the combined optimum changes as the focal functional demands are selectively removed. A strong receipt therefore contains the linked pattern

```text
z_P* ≠ z_G*
W11(z) has a supported interior z_C*
G off → optimum moves toward z_P*
P off → optimum moves toward z_G*
functional-component gradients near z_C* are non-zero and opposed.
```

The final condition is important. The derivative of a fitted combined curve is zero at its own vertex by construction. That mathematical fact is not independent evidence that two causal components oppose each other there.

### 3.5 Level 4: optional pure-function promotion

Pure-function language should be earned by an additional test. Define pollinator-mediated components

```text
M_G0(z) = W10(z) - W00(z)
M_G1(z) = W11(z) - W01(z)
```

and antagonist-mediated components

```text
H_P0(z) = W01(z) - W00(z)
H_P1(z) = W11(z) - W10(z).
```

Each component can have its own optimum. A pollinator component is promoted toward a context-stable empirical `z_F1*` only when the optima of `M_G0` and `M_G1` agree inside a prospectively frozen equivalence region, with interior support and propagated uncertainty. The same rule applies to the antagonist component.

Failure of this gate is not a failed experiment. It means that the effective functional objective changes with the state of the other channel. That conclusion is biologically richer than forcing context-dependent data into a context-free pure-function label.

## 4. What existing plant studies recover

We translated the promotion ladder into literature-observable signatures and assembled a source-adjudicated evidence ledger. The unit of recurrence is an independent biological cluster rather than a paper, population, year, treatment or measured response. The current targeted universe contains 16 clusters. Retrieval was theory-targeted rather than probability-sampled, so the counts below describe recurrence and evidence structure inside the screened universe; they are not estimates of natural prevalence.

Five clusters provide the strongest direct conflict signatures: four show opposing directional selection on the same or a closely bounded trait coordinate, and one provides the manipulated combined-compromise surface described above. Seven additional clusters show context-dependent shifts in functional weighting or effective selection. Two clusters are aligned/no-conflict controls. One shared-cue system remains a conflict candidate because antagonist response has not been linked to a common reproductive loss, and one system represents sequential life-history filtering rather than a simultaneous shared-coordinate estimand.

This distribution matters more for identification than a positive-only case list. It shows that the literature contains both sides of the first gate. Opposing selection occurs in systems such as *Castilleja*, *Pedicularis* and *Silene* (Cariveau *et al*., 2004; Sun *et al*., 2016; Zhou *et al*., 2020), but multifunctionality without identified conflict also occurs in orientation systems (Yu *et al*., 2021; Nakata *et al*., 2022). The framework therefore has an empirical negative class.

Context dependence is equally prominent. Pollinators and herbivores can impose additive yet opposing selection on flowering phenology (Sletvold *et al*., 2015); herbivory can reduce pollinator-mediated selection on floral traits (Gómez, 2003); and multispecies interactions can act at distinct sequential life-history stages (Campbell *et al*., 2022). At a broader scale, meta-analysis shows that herbivore effects on floral traits, pollinator attraction and reproduction are contingent on the tissue attacked and whether damage is real or simulated (Moreira *et al*., 2019). Such results support context-dependent weighting, but they do not by themselves identify bounded component optima.

The shared-cue literature also reveals a recurring mechanistic boundary. Floral scent and reward can affect mutualists and antagonists, as illustrated by *Nicotiana attenuata* (Kessler *et al*., 2015), but common receiver response is not the same as a common-fitness causal decomposition. A cue can be shared informationally without the available design identifying how each receiver contributes to the same reproductive outcome.

![Figure 3. Source-adjudicated recurrence and fail-closed quantitative synthesis.](nph_viewpoint_figures/FIG3_REALITY_PATTERN.svg)

**Figure 3. Existing studies recover recurrence and specificity, but not the full estimand.** The 16-cluster targeted evidence universe contains conflict signatures, frequent context-weight shifts, aligned/no-conflict controls and explicit boundary cases. A strict quantitative pool remains fail-closed because fewer than three independent clusters currently share an admissible estimand family with compatible orientation, valid uncertainty and covariance treatment.

## 5. Why the quantitative synthesis should remain fail-closed

The current strict numerical inventory contains four strong same-coordinate designs at different levels of completeness. Exact component coefficients are available for some systems, while other studies require reconstruction of the relevant shared contrast and its uncertainty. We do not fill missing covariance with an independence assumption and do not recover inaccessible values by eye from figures.

This conservative rule is not a technical nuisance. It protects the scientific target. A random-effects mean is meaningful only when the studies contribute sufficiently comparable estimands. Combining directional selection coefficients, bounded optimum separations, treatment contrasts and state-specific curve parameters because all are verbally related to “conflict” would produce numerical precision around an undefined quantity.

Selection into a quantitative pool creates a second problem. If systems are admitted because they already exhibit the desired opposing-sign pattern, then a mean across those systems is conditional on positive admission. It can summarize effect magnitude among positives, but it cannot estimate prevalence across all eligible plant systems and cannot serve as an independent test that recurrence exists. Aligned/no-conflict cases must remain visible whenever the target is specificity or a design-wide average.

The fail-closed result is therefore a scientific output: existing plant studies recover the biological ingredients of the framework more often than they recover a common estimand suitable for pooling. That diagnosis tells us what the next experiments need to measure.

## 6. A research agenda built from the residual identification gap

The literature synthesis changes the role of the next experiment. A new focal study is no longer needed to show that plants can experience pollinator–antagonist conflict or that ecological context alters selection. Those points already have substantial empirical support. The experiment should be designed only to recover quantities that remain structurally unidentified.

A high-value system should pass four preconditions. First, one continuous or ordered trait coordinate must be manipulable reversibly across enough levels to locate nonlinear optima. Second, focal functional channels must be selectively manipulated without redefining the trait itself. Third, the same reproductive fitness scale must be measurable in all crossed states. Fourth, the candidate population and season must first be qualified as conflict-active; a species-level reputation for conflict is not enough when interaction strength varies geographically or temporally.

The preferred execution chain is therefore:

```text
source-adjudicated recurrence and specificity
→ quantitative compatibility audit
→ identify the residual causal gap
→ qualify a conflict-active focal context
→ validate a reversible multi-level z manipulation
→ validate selective functional interventions
→ fit W00(z), W10(z), W01(z), W11(z)
→ estimate z_P*, z_G*, z_C*
→ test selective-removal shifts and opposed component gradients
→ optionally test context-stable component optima.
```

*Dalechampia* remains an attractive first candidate because pollinator-mediated selection on display traits can be manipulated experimentally (Armbruster *et al*., 2005), while broader work in the genus motivates a conflict interpretation. *Pedicularis* provides a strong geographic conflict template (Sun *et al*., 2016). *Nicotiana attenuata* offers unusually tractable shared-cue biology (Kessler *et al*., 2015). None should be treated as automatically qualified; the point of the gate is to prevent candidate selection from predetermining the conclusion.

The same framework also clarifies what a negative experiment would teach us. If two functions favor the same trait region, the conflict hypothesis is rejected for the declared context. If selective removal does not move the combined optimum as predicted, an apparent compromise may reflect background pathways rather than the focal functions. If component optima move across contexts, the pure-function promotion fails while context-dependent functional geometry remains supported. Each outcome has a different interpretation and therefore a different downstream claim ceiling.

## 7. Keeping conflict identification separate from later evolutionary claims

Once functional conflict is identified, additional questions begin rather than end. A measured conflict budget does not determine whether a more differentiated architecture would recover enough fitness to offset its costs, whether that architecture is mutationally accessible, or whether it can invade and fix. Those downstream questions require new estimands and population-process assumptions. Conversely, an observed interaction between multiple trait axes does not, by itself, identify the ecological mechanism generating that interaction.

We therefore advocate modular inference: first establish whether conflict exists on the shared coordinate; only then export that identified quantity into downstream architecture or evolutionary models. This prevents a common escalation in which multifunctionality is treated as conflict, conflict is treated as evidence for differentiation, and trait interaction is treated as mechanism.

![Figure 4. SCH as the upstream identification gate and the residual experimental programme.](nph_viewpoint_figures/FIG4_PROGRAM_HANDOFF.svg)

**Figure 4. Conflict identification is an upstream gate, not a complete evolutionary theory.** SCH identifies whether a shared plant trait experiences opposing causal geometry and specifies the residual experiment needed to close that claim. Once a conflict quantity is justified, downstream architecture-value and evolutionary-realization questions can be tested separately. Mechanistic allocation of interactions among multiple trait axes is an orthogonal identification problem.

## 8. Conclusion

Multifunctionality is a biological fact; functional conflict is an identified causal relation. The two should not be used as synonyms. Likewise, an optimum measured in an ecological treatment is not automatically the pure optimum of one functional component.

Plant biology is unusually well positioned to enforce these distinctions because selective functional interventions and trait manipulations can reconstruct the relevant fitness surfaces. Existing studies already show that opposing same-coordinate selection recurs, that ecological context changes functional weighting, that combined-compromise surfaces can occur, and that aligned multifunctionality is real. What they rarely provide is the complete promotion chain from state-specific surfaces to context-stable functional optima.

The proposed research agenda is therefore not “collect more examples of trade-offs.” It is to match every biological claim to the estimand that would identify it. That change makes negative results informative, prevents pooled precision from outrunning comparability, and gives multifunctional-trait research a clear experimental endpoint: determine whether the functions really oppose one another on the same coordinate, and stop exactly where the evidence stops.

## References

Armbruster WS, Antonsen L, Pélabon C. 2005. Phenotypic selection on *Dalechampia* blossoms: honest signaling affects pollination success. *Ecology* 86: 3323–3333. doi:10.1890/04-1873.

Campbell DR, Bischoff M, Raguso RA, Briggs HM, Sosenski P. 2022. Selection of floral traits by pollinators and seed predators during sequential life history stages. *The American Naturalist* 199: 808–823. doi:10.1086/716740.

Cariveau D, Irwin RE, Brody AK, Garcia-Mayeya LS, von der Ohe A. 2004. Direct and indirect effects of pollinators and seed predators to selection on plant and floral traits. *Oikos* 104: 15–26. doi:10.1111/j.0030-1299.2004.12641.x.

Ellis AG, Johnson SD. 2010. Gender differences in the effects of floral spur length manipulation on fitness in a hermaphrodite orchid. *International Journal of Plant Sciences* 171: 1010–1019. doi:10.1086/656351.

Gómez JM. 2003. Herbivory reduces the strength of pollinator-mediated selection in the Mediterranean herb *Erysimum mediohispanicum*: consequences for plant specialization. *The American Naturalist* 162: 242–256. doi:10.1086/376574.

Irwin RE, Adler LS, Brody AK. 2004. The dual role of floral traits: pollinator attraction and plant defense. *Ecology* 85: 1503–1511. doi:10.1890/03-0390.

Kessler D, Kallenbach M, Diezel C, Rothe E, Murdock M, Baldwin IT. 2015. How scent and nectar influence floral antagonists and mutualists. *eLife* 4: e07641. doi:10.7554/eLife.07641.

Moreira X, Castagneyrol B, Abdala-Roberts L, Traveset A. 2019. A meta-analysis of herbivore effects on plant attractiveness to pollinators. *Ecology* 100: e02707. doi:10.1002/ecy.2707.

Nakata T, Rin I, Yaida YA, Ushimaru A. 2022. Horizontal orientation facilitates pollen transfer and rain damage avoidance in actinomorphic flowers of *Platycodon grandiflorus*. *Plant Biology* 24: 798–805. doi:10.1111/plb.13414.

Schiestl FP, Kirk H, Bigler L, Cozzolino S, Desurmont GA. 2014. Herbivory and floral signaling: phenotypic plasticity and tradeoffs between reproduction and indirect defense. *New Phytologist* 203: 257–266. doi:10.1111/nph.12783.

Sletvold N, Moritz KK, Ågren J. 2015. Additive effects of pollinators and herbivores result in both conflicting and reinforcing selection on floral traits. *Ecology* 96: 214–221. doi:10.1890/14-0119.1.

Sun S-G, Armbruster WS, Huang S-Q. 2016. Geographic consistency and variation in conflicting selection generated by pollinators and seed predators. *Annals of Botany* 118: 227–237. doi:10.1093/aob/mcw097.

Theis N, Adler LS. 2012. Advertising to the enemy: enhanced floral fragrance increases beetle attraction and reduces plant reproduction. *Ecology* 93: 430–435. doi:10.1890/11-0825.1.

Yu Y-M, Li X-X, Xie D, Wang H. 2021. Horizontal orientation of zygomorphic flowers: significance for rain protection and pollen transfer. *Plant Biology* 23: 156–161. doi:10.1111/plb.13197.

Zhou J, Reynolds RJ, Zimmer EA, Dudash MR, Fenster CB. 2020. Variable and sexually conflicting selection on *Silene stellata* floral traits by a putative moth pollinator selective agent. *Evolution* 74: 1321–1334. doi:10.1111/evo.13965.

**Key words:** causal identification; compromise; floral traits; functional conflict; multifunctionality; pollination; trait optimum.
