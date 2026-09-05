# SCH Chapter 1 figure plan v1 — BALANCE

The figure sequence is designed to be structurally symmetric with BITA Chapter 2 without forcing identical empirical content.

## Figure 1 — One shared axis, two functional optima

**Question:** What does it mean for two functions to remain coupled on one trait?

Show one horizontal trait coordinate `z` with function-specific preferred states `theta1` and `theta2`, their loss curves, and the combined shared loss.

Primary labels:

```text
L_S(z) = l1(z) + l2(z)
z*     = argmin L_S(z)
L_S*   = L_S(z*)
```

Quadratic inset:

```text
z* = (w1 theta1 + w2 theta2)/(w1+w2)
L_S* = [w1w2/(w1+w2)](theta1-theta2)^2
```

Reader takeaway: **Chapter 1 optimizes position within a fixed shared architecture.**

Symmetry with BITA: BITA Figure 1 begins from this shared state and asks what happens when the phenotype space is enlarged.

## Figure 2 — Context moves the shared balance without changing architecture

**Question:** How can the same one-axis architecture produce different compromises?

Use two or three panels that vary relative weights `w1,w2` and/or function-specific optima. Show `z*` shifting while the trait remains one-dimensional.

Distinguish:

- interior compromise;
- directional movement toward one side of the same axis;
- possible context dependence of the optimum.

Do not depict trait splitting in this figure.

Reader takeaway: **selection can move the balance without creating a new axis.**

## Figure 3 — Floral shared-cue mapping of the general balance problem

**Question:** How does the general one-axis model map onto SCH's empirical system?

Map

```text
z -> floral display / attraction coordinate A
function 1 -> pollinator-mediated benefit M(A)
function 2 -> antagonist-mediated loss G(A)
direct cost -> C(A)
```

and show

```text
W(A) = M(A) - G(A) - C(A)
M'(A*) - G'(A*) - C'(A*) = 0
```

Include two cue architectures:

1. high receiver overlap — pollinator and antagonist responses move on the same component;
2. partial separability — component partitioning, conditional emission or temporal gating reduces coupling.

Reader takeaway: **shared cue is one mechanism producing shared-axis conflict; it is not the general definition of Chapter 1.**

## Figure 4 — What one-trait conflict actually does in existing evidence

**Question:** Which evolutionary outcomes are currently supported, and at what claim level?

Use four evidence lanes:

```text
integrated compromise
context-dependent polymorphism maintenance
population evolutionary redirection
partial cue decoupling
```

Representative bounded anchors may include Pérez-Barrales, Toräng / Ågren, Ramos & Schiestl / Knauer, and Kessler / Knauer.

Add a clear stop line:

```text
shared -> private cue historical transition: NOT_EVALUABLE
lineage branching from ancestral shared cue: NOT_EVALUABLE
```

Reader takeaway: **Chapter 1 evidence supports several ways to resolve conflict while staying below the historical splitting claim.**

## Figure 5 — Chapter handoff: balance becomes the baseline for differentiation

**Question:** What exactly passes from SCH to BITA?

Central flow:

```text
SCH / Chapter 1
one shared axis z
   -> best shared phenotype z*
   -> residual shared conflict load L_S*
                    |
                    v
BITA / Chapter 2
partly independent axes x,y
   -> recoverable loss R
   -> architecture cost K
   -> Delta_arch = R-K
   -> quadratic: R=sL_S*
                    |
                    v
mechanism identification of the multi-trait phenotype
```

Add the empirical mappings below the mathematical flow:

```text
SCH floral case: shared cue A tracked by pollinator + antagonist channels
BITA floral case: A x D phenotype + crossed consumer interventions
```

Reader takeaway: **the sister-paper relationship is a mathematical handoff, not merely shared biological motivation.**

## Main-text / Appendix boundary

Main should contain the five figures above. Detailed *Ficus* L4 candidate matrices, same-code equivalence design, literature coverage tables and source-level adjudications remain Appendix / Open Research material unless one becomes a direct headline result.

## Figure-level overclaim guard

Do not use arrows implying that

```text
interior compromise -> historical trait splitting
partial cue decoupling -> new module origin
large L_S* -> differentiation necessarily occurred
```

The only justified cross-chapter arrow is conceptual:

```text
measured/defined shared architecture -> baseline for testing a differentiated architecture.
```
