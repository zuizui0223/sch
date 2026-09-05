# How do conflicting functions balance on one trait? Linking shared-trait compromise to evolutionary response

**Working Chapter 1 integration candidate — preserve the existing shared-cue evidence manuscript as the detailed floral evidence source until this framing is fully validated.**

**Authors and affiliations:** [Author-controlled]

**Corresponding author:** [Author-controlled]

## Abstract

A single trait can contribute to several functions whose preferred phenotypic states differ. While those functions remain coupled to one trait coordinate, selection cannot optimize them independently; the best attainable phenotype is a shared solution whose location depends on the relative strength and shape of the competing functional demands. We formulate that first architectural problem as Chapter 1 of the SCH–BITA programme. For one shared coordinate `z`, let `L_S(z)` be the summed functional loss and let `z*` minimize it. The residual `L_S* = L_S(z*)` is the conflict load that remains after the best possible one-axis compromise has been chosen. In a quadratic baseline, two functions with weights `w1,w2` and preferred states `theta1,theta2` yield `z*=(w1 theta1+w2 theta2)/(w1+w2)` and `L_S*=[w1w2/(w1+w2)](theta1-theta2)^2`. This same `L_S*` is the baseline inherited by BITA Chapter 2, which asks how much of the shared-axis loss can be recovered by partly independent trait axes and whether that recovery pays for the additional architecture. Floral shared cues provide SCH's detailed empirical case: pollinator-mediated benefit and antagonist-mediated loss can move on the same display coordinate, generating stabilizing compromise, context-dependent polymorphism, population-level evolutionary redirection, or partial cue decoupling. Current evidence recovers bounded examples of each of these lower-level responses but does not estimate a common cross-system `L_S*` and does not reconstruct repeated historical evolution from an ancestral shared cue to a private cue. The contribution is therefore not a claim that every trade-off produces an interior optimum. It is a framework for identifying what selection does while functions remain on one axis, measuring the residual conflict left by that shared architecture, and handing that quantity to the sister differentiation problem.

**Keywords:** functional conflict; multifunctionality; shared trait; stabilizing selection; evolutionary compromise; floral signals; cue overlap; trait architecture

## 1. Introduction

Traits are often multifunctional. One morphological, chemical or behavioural coordinate can affect several ecological functions at once, and those functions need not favour the same phenotype. This creates an architectural problem before any question of modularization arises: **what is the best phenotype available while the functions are still forced to share one trait axis?**

This is the Chapter 1 problem in the SCH–BITA programme. Chapter 1 holds architecture fixed and studies the shared solution. Chapter 2 relaxes that architectural restriction and asks whether separating functions across partly independent axes can recover enough of the shared-axis loss to justify the added architecture. The two chapters therefore differ in what is allowed to change, not in their underlying functional conflict.

The present SCH repository was originally organized around a particularly clear floral realization of this problem. Floral colour, scent, display and reward can increase pollinator attraction while also exposing plants to florivores, seed predators, nectar robbers or other antagonists. When both consumer classes track the same sensory coordinate, the plant cannot move that signal for one audience without potentially changing response by the other. Cue overlap is therefore an empirically tractable mechanism of shared-axis conflict.

However, the architectural question is broader than floral cue sharing. A feeding structure can serve incompatible mechanical functions, a physiological coordinate can be pulled by several performance demands, and a gene product can contribute to competing functions. The common structure is that multiple functions are expressed through one measured coordinate. Chapter 1 asks how the joint fitness surface is shaped while that coupling remains.

The key distinction is between **balance** and **differentiation**. Balance means optimizing the existing shared architecture. It may produce an interior compromise, movement toward one end of the same axis, frequency-dependent maintenance of alternatives or context-dependent shifts in the optimum. Differentiation is different: it enlarges the phenotype space by allowing functions to move on more separable coordinates. The existing SCH evidence contains lower-level examples of one-axis compromise and evolutionary redirection and also examples of partial cue decoupling, but it does not by itself establish historical origin of a new module.

We therefore reframe SCH at two nested levels. At the general level, SCH defines the best shared phenotype `z*` and the residual shared conflict load `L_S*`. At the empirical level, the current floral shared-cue framework remains the main case through which those concepts are observed and bounded. This lets Chapter 1 end on exactly the object that Chapter 2 needs as its baseline.

## 2. Shared-axis balance

### 2.1 General architecture

Let one trait coordinate `z` contribute to two functions. Write their losses relative to function-specific optima as `l1(z)` and `l2(z)`. While both functions remain tied to the same coordinate,

```text
L_S(z) = l1(z) + l2(z).
```

The best shared phenotype is

```text
z* = argmin_z L_S(z)
```

and the remaining conflict load is

```text
L_S* = L_S(z*).
```

If the component losses are normalized to zero at their separate optima, `L_S*` is the loss generated specifically by forcing both functions onto one axis. It is therefore the maximum conflict load that a more differentiated architecture could potentially recover before paying any additional architecture cost.

For an interior optimum on fitness `W_S(z)=-L_S(z)`,

```text
dW_S/dz at z* = 0
```

and local stability requires

```text
d2W_S/dz2 at z* < 0.
```

These conditions define the canonical integrated compromise. They do not imply that every empirical system must have an interior optimum; boundary solutions, frequency dependence and multiple local states require separate interpretation.

### 2.2 Quadratic common baseline with BITA

Let the two functions prefer `theta1` and `theta2`, with positive weights `w1,w2`:

```text
L_S(z) = w1(z-theta1)^2 + w2(z-theta2)^2.
```

Then

```text
z* = (w1 theta1 + w2 theta2)/(w1+w2)
```

and

```text
L_S* = [w1 w2/(w1+w2)] (theta1-theta2)^2.
```

This gives four immediate Chapter 1 predictions.

First, the shared optimum lies between the two function-specific optima when both weights are positive. Second, increasing the relative weight of one function shifts `z*` toward that function's preferred state. Third, increasing the distance between the function-specific optima increases the residual conflict load. Fourth, if the preferred states coincide, `L_S*=0` and there is no conflict load to be released by architectural separation.

Environmental or ecological context can change the functional weights and therefore move the shared optimum without changing the architecture. A population may consequently show different apparent compromises across environments even when the underlying trait-development system is unchanged.

## 3. Floral shared cues as the Chapter 1 worked case

### 3.1 Mapping the general model

For the existing SCH floral case, set `z=A`, where `A` is one predeclared floral attraction/display coordinate. Write reproductive fitness as

```text
W(A) = M(A) - G(A) - C(A),
```

where `M` is pollinator-mediated reproductive benefit, `G` is antagonist-mediated reproductive loss and `C` is any direct physiological or construction cost not already standardized by design.

A local interior compromise satisfies

```text
M'(A*) - G'(A*) - C'(A*) = 0
```

with negative local curvature of total fitness.

The existing first-order contrasts remain useful:

```text
M_A = change in pollinator-mediated benefit
G_A = change in antagonist-mediated cost
S_A = M_A - G_A.
```

They describe movement along a declared `A` contrast. They do not by themselves reconstruct the whole fitness surface or estimate the location of `A*`.

### 3.2 Cue overlap as a mechanism of coupling

Cue overlap determines whether the same sensory coordinate of `A` changes response by both audiences. If pollinators and antagonists track the same component, movement along that coordinate couples the two ecological channels. If they track separable components, one component can change with weaker consequences for the other audience.

In the programme-level framing, cue overlap is therefore a **mechanism that shapes the one-axis fitness surface**, not the general definition of Chapter 1. The same shared-axis mathematics can apply to other multifunctional traits without sensory receivers.

## 4. What the current SCH evidence already recovers

The existing evidence spine establishes several bounded outcomes rather than one universal response.

**Integrated compromise.** Pérez-Barrales et al. (2013) provide an observational fitness surface in which pollinator selection for larger floral bracts is counteracted by seed-predator selection and net selection tends toward stabilizing balance. This is the clearest current empirical analogue of the interior shared optimum.

**Context-dependent maintenance.** Toräng et al. (2008) and Ågren et al. (2013) recover frequency- or context-dependent maintenance of alternative display phenotypes. These cases show that a shared conflict need not collapse to one fixed interior phenotype.

**Population evolutionary change.** Ågren et al., Knauer et al. and Ramos & Schiestl provide bounded evidence that changes in antagonist or pollinator context redirect floral evolution at population or experimental-evolution scales.

**Partial cue decoupling.** Kessler and colleagues and Knauer et al. recover component partitioning or conditional emission that can reduce coupling among receiver responses. These are important mechanistic precedents for the architectural question, but they do not by themselves establish that an ancestral one-axis trait historically split into a new module.

The evidence therefore supports the Chapter 1 statement that conflict on a shared trait can be resolved by an interior compromise, maintenance of alternatives or directional evolutionary change, and that partial decoupling mechanisms exist. It does not yet support a cross-system quantitative distribution of `z*` or `L_S*`.

## 5. Historical endpoint and claim ceiling

The strongest historical claim would be that dual-function or dual-audience conflict repeatedly caused an ancestral shared coordinate to split into more private or specialized trait axes. The current SCH evidence does not establish that endpoint.

The historical ladder remains useful:

```text
L0  contemporary dual-function conflict
 -> L1  component partitioning / conditional gating / temporal separation
 -> L2  population differentiation or measured microevolution
 -> L3  phylogenetic trait divergence associated with one function or audience
 -> L4  reconstructed shared -> differentiated/private transition with both functional channels
```

Current evidence reaches lower and intermediate levels, including L2 directly and L3 on parts of the historical side. The *Ficus* programme is a strong composite bridge because resolved pollinator codes, non-pollinator use of receptive scent, temporal separation and phylogenetic structure coexist within one radiation. But the same chemical coordinate has not yet been paired with matched exploiter behaviour and then reconstructed as repeated shared-to-private transitions. L4 therefore remains `NOT_EVALUABLE` rather than negative.

This ceiling is essential for symmetry with BITA. Chapter 1 does not claim historical origin of a new axis, and Chapter 2 does not claim historical origin merely because a differentiated architecture would have higher optimized fitness.

## 6. Handoff to BITA Chapter 2

The Chapter 1 output is the best shared architecture:

```text
z*
L_S*.
```

BITA keeps the same functional conflict but enlarges the phenotype space. Let `R` be the part of `L_S*` recoverable by the differentiated architecture and `K` its additional fixed cost. The general Chapter 2 result is

```text
Delta_arch = R - K
```

with differentiation favoured when

```text
K < R.
```

Under the matched quadratic model, residual coupling leaves a decoupling fraction `s`, giving

```text
R = s L_S*
Delta_arch = s L_S* - K.
```

The sister-paper handoff is therefore exact:

```text
Chapter 1 / SCH
functions remain on one axis
-> find the best shared phenotype z*
-> characterize the residual conflict load L_S*

Chapter 2 / BITA
relax the one-axis restriction
-> recover R from L_S*
-> pay architecture cost K
-> identify the ecological mechanism of the resulting multi-trait phenotype
```

The floral mappings are deliberately different. SCH asks how pollinator and antagonist effects move on one shared attraction/display coordinate. BITA's detailed floral case adds a distinct second trait and asks what the cross-trait reproductive interaction means and how its ecological channels can be identified. The chapters share a conceptual baseline but not empirical estimands.

## 7. Predictions created by the paired framework

The paired Chapter 1–2 architecture generates a sharper set of prospective tests.

1. Contexts that increase separation between function-specific optima should increase the shared conflict load measured in Chapter 1.
2. Contexts that change the relative functional weights should shift `z*` even without architectural change.
3. Systems with large measured shared conflict but weak developmental or functional decoupling may remain integrated despite strong trade-offs.
4. Systems with large shared conflict and cheap, weakly coupled additional axes are the strongest candidates for differentiation.
5. After differentiation, cross-trait fitness interactions remain mechanistically ambiguous unless pathway or consumer interventions resolve the channels.

A particularly strong empirical programme would estimate the one-axis surface first, then measure or manipulate a second partially independent axis in the same biological system. That would turn the current sister-paper logic into a direct within-system test rather than a conceptual handoff across different evidence sets.

## 8. Conclusions

Chapter 1 is the problem of optimization under a fixed shared architecture. When several functions are tied to one coordinate, the relevant object is not simply whether their effects oppose each other but where the best shared phenotype lies and how much conflict remains after that optimum is chosen.

The current SCH floral evidence shows that dual-audience conflicts can produce integrated compromise, maintained alternatives, population-level evolutionary redirection and partial cue decoupling. The strongest historical transition remains unresolved. The general model makes these results usable beyond flowers by defining the shared optimum `z*` and the residual conflict load `L_S*`.

That residual load is the exact bridge to BITA. SCH asks how functions balance while coupled. BITA asks whether enough of the resulting conflict can be recovered by partial differentiation to pay for a larger architecture, and then how the mechanism of that multi-trait phenotype can be identified. The pair therefore separates **optimization within an architecture** from **evolutionary advantage of changing the architecture**.

## Evidence and reference boundary

This integration candidate does not replace the detailed source adjudications in `MANUSCRIPT_SHARED_CUE_FRAMEWORK.md`, `evidence/EVIDENCE_ROLE_REGISTRY_V1.csv`, `empirical/one_trait_shared_cue/EVOLUTIONARY_OUTCOME_READOUT_V1.md`, or the *Ficus* history audits. Those files remain the evidence source of truth until the general Chapter 1 manuscript receives its own focused reference and package audit.
