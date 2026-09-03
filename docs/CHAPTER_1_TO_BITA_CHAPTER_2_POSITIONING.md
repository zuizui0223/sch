# Chapter 1 to Chapter 2 positioning

## Dissertation-level question

How does evolution solve conflicting functional demands on phenotype?

The two chapters now address one architectural sequence:

```text
Chapter 1 / SCH
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/

Chapter 2 / BITA
shared compromise
      ↓
function 1 ---> trait x
function 2 ---> trait y
      ↓
functional differentiation / modularization
```

The pollinator-antagonist floral system is the main empirical realization, not the upper-level definition of the programme.

## Chapter 1 — SCH: why multifunctionality creates compromise

Chapter 1 begins from one trait coordinate `z` serving two fitness-relevant functions.

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z).
```

If the function-specific optima differ,

```text
z1* != z2*,
```

the single shared coordinate cannot independently optimize both functions. The realized optimum

```text
zc* = argmax W_shared(z)
```

may therefore be a compromise.

### Balance is gradient cancellation

The central ecological claim is not that the two functions contribute equally. At an interior compromise,

```text
w1 dF1/dz + w2 dF2/dz - dC/dz = 0,
```

while the underlying function-specific gradients may remain non-zero and oppose each other.

This makes an important prediction:

> removing or weakening one functional demand should shift the selection gradient or optimum of the shared trait toward the optimum favored by the remaining function.

That intervention prediction is what turns “intermediate phenotype” into an identified compromise mechanism.

## Chapter-1 evidence ladder

```text
L0  multifunctionality
    the same z affects both functions

L1  functional conflict
    selective interventions show opposing contributions on z

L2  compromise geometry
    >=3 z levels recover distinct functional curves / optima and zc*

L3  mechanism-resolved balance
    crossed functional interventions explain how the gradients cancel

L4  evolutionary maintenance
    heritable variation / selection / experimental evolution tracks the surface

L5  historical architecture
    ancestral integration and later differentiation are reconstructed
```

The existing two-level SCH crossed design identifies L1 and part of L3. It is a local conflict experiment, not by itself a full test of compromise geometry. The new confirmatory Chapter-1 target therefore adds a multi-level `z` manipulation.

## Floral realization of Chapter 1

For the existing shared-cue system,

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduction of antagonist-mediated loss
z          = floral attraction / display coordinate
```

and

```text
W(z) = M(z) - G(z) - C(z).
```

The registered local mechanism experiment crosses

```text
A x antagonist x pollinator
8 cells.
```

For one two-level `A` contrast,

```text
d[g,p] = W[1,g,p] - W[0,g,p]
M_A(g)  = d[g,1] - d[g,0]
G_A(p)  = d[0,p] - d[1,p]
B_A     = d[0,0]
J_A     = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

This tells us whether pollination makes `A` more valuable and antagonism makes the same `A` less valuable. The multi-level extension then asks whether these opposing functional effects actually generate different optima and an integrated balance.

## Role of the SCH literature

The literature evidence is now positioned as **real-world support for the architectural mechanism**.

It establishes that:

- the same floral traits can contribute to multiple ecological functions;
- opposing functional selection occurs in nature;
- stabilizing compromise and context-dependent maintenance are real outcomes;
- population-level evolution can be redirected by changing one functional demand;
- component partitioning, conditional emission and temporal separation can reduce functional coupling.

The literature does not replace the chapter-specific causal experiment. It shows that the mechanism to be identified is ecologically real and that the predicted outcomes recur.

## Chapter 2 — BITA: release the shared-coordinate constraint

Chapter 2 starts from the compromise identified in Chapter 1 and asks a different question:

> **Can increasing trait dimensionality allow the two functions to be tuned more independently?**

The general architecture is

```text
shared state
function 1 ---\
               >--- z
function 2 ---/

more differentiated state
function 1 ---> x
function 2 ---> y.
```

The two-trait architecture is not valuable merely because it contains more traits. It is valuable if `x` and `y` reduce the functional coupling that forced compromise on `z`.

## Functional differentiation criteria

A contemporary functional-differentiation result requires separate evidence for four steps.

```text
D1  shared conflict exists
    Chapter 1 identifies opposing functional demands on z

D2  preferential functional loading
    x changes function 1 more strongly / cleanly than function 2
    y changes function 2 more strongly / cleanly than function 1

D3  dimensional release
    the x,y combination reaches a functional / fitness combination that
    cannot be achieved on the constrained shared-trait path

D4  mechanism allocation
    selective interventions identify why the extra dimension improves,
    releases or reverses the original compromise
```

A fifth historical step is deliberately separate:

```text
D5  historical modularization
    ancestral shared architecture -> derived functionally differentiated
    architecture reconstructed with phylogenetic / developmental evidence.
```

Contemporary experiments can establish D1-D4 without proving D5.

## Existing BITA as the floral implementation

In the current floral special case,

```text
x = attraction trait A
    primarily supports pollinator-mediated gain

y = antagonist-reducing trait D
    primarily supports protection / antagonist avoidance.
```

BITA's four-cell trait surface is

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0.
```

Its nested outcome claims remain valid:

```text
Level 1  positive interaction relief
         Delta_AD W > 0

Level 2  constraint release
         A0 <= 0 < A1

Level 3  strict reversal
         A0 < 0 < A1.
```

These outcomes now have a broader interpretation: they test whether adding a second functional coordinate improves the performance of a system that was constrained when functions were coupled.

## BITA mechanism allocation

The full floral implementation crosses

```text
A x D x antagonist x pollinator
16 cells.
```

The channel allocation remains

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
kappa_delta  independently validated remaining joint channel.
```

This is the mechanism-level test of functional differentiation. A useful `D` is not simply “a defence trait”; it is a coordinate that reduces the antagonist penalty while preserving enough of the attraction function that the joint phenotype moves beyond the Chapter-1 compromise.

The `A x D x G x P` interaction remains an internal test of whether the two functional channels are truly separable. A non-zero four-way term means that the putatively differentiated architecture still contains cross-functional coupling.

## The strongest Chapter-2 claim

The strongest contemporary claim is therefore not

> two traits exist.

It is

> **two partially independent trait coordinates allow the system to satisfy conflicting functional demands more independently than one shared coordinate, and the crossed intervention identifies the ecological channels that generate that release.**

This is **functional differentiation / modularization as an escape architecture**.

## Historical claim boundary

The words “functional differentiation” and “modularization” must be used at two levels.

### Contemporary functional modularity

Supported when current `x` and `y` show preferential functional loading and reduced cross-channel interference.

### Historical modularization

Requires evidence that a lineage moved from an ancestrally integrated architecture toward the differentiated architecture. Extant `A + D` alone does not prove that historical transition.

Thus BITA can experimentally establish that a differentiated architecture releases compromise without claiming that `A` and `D` literally arose by splitting one ancestral morphological trait.

## Current empirical bridge

The broader *Nicotiana attenuata* programme remains valuable because it contains:

- a manipulated floral attraction coordinate affecting pollination and antagonist response;
- an attraction-by-defence-like reproductive factorial;
- flower-associated defence biology;
- experimental tools that can be developed into selective pathway interventions.

But the evidence remains distributed across studies. The programme is therefore a candidate bridge, not a completed historical or mechanism-resolved modularization case.

## Unified research sequence

```text
SCH Stage 0
validate one multifunctional z coordinate
        ↓
SCH Stage 1
selective two-level crossed intervention
identify local opposing functional effects
        ↓
SCH Stage 2
multi-level z experiment
recover z1*, z2*, zc* and compromise geometry
        ↓
SCH Stage 3-4
confirm balance and evolutionary maintenance
        ↓
BITA Stage 1
introduce / compare two functional coordinates x,y
ask whether dimensionality improves the constrained outcome
        ↓
BITA Stage 2
cross x,y with the two functional environments
identify preferential loading and cross-functional interference
        ↓
BITA Stage 3
independent cost assay + complete mechanism allocation
        ↓
Historical extension
reconstruct integration -> differentiation / modularization.
```

## Joint claim ceiling

Together the sister projects aim to establish a general evolutionary principle:

> **Multifunctionality can create compromise when different functions are constrained to a shared phenotypic coordinate; increasing trait dimensionality can release that compromise when functions become more independently tunable.**

The floral pollinator-antagonist / attraction-defence system is the first complete empirical implementation of that principle.
