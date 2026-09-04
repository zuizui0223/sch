# Chapter 1 to Chapter 2 positioning

## Dissertation-level question

How does evolution solve conflicting functional demands on phenotype?

The two chapters address one architectural sequence:

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

At the theory level,

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z).
```

Pure function-specific optima may be written:

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z).
```

The earlier shorthand `z1* != z2*` refers to this theory-level conflict. The explicit notation is now preferred because the empirical crossed experiment does not automatically identify the pure function optima.

### What SCH directly identifies

The multi-level crossed experiment estimates:

```text
W00(z) = P0G0
W10(z) = P1G0
W01(z) = P0G1
W11(z) = P1G1
```

and therefore:

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

These are intervention-defined state optima. Because direct/background effects can remain in the state surfaces:

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The empirical compromise claim does not require that relabeling.

### Balance is causal gradient opposition

At a supported combined optimum, SCH requires opposite functional-component gradients and causal optimum shifts:

```text
G off -> z_C* shifts toward z_P*
P off -> z_C* shifts toward z_G*.
```

This is what turns an intermediate phenotype into an identified compromise mechanism.

## Chapter-1 evidence ladder

```text
L0  multifunctionality
    the same z affects both functions

L1  functional conflict
    selective interventions show opposing contributions on z

L2  compromise geometry
    >=3 z levels recover distinct state-specific optima and z_C*

L3  mechanism-resolved balance
    crossed functional interventions explain how the gradients oppose

L4  evolutionary maintenance
    heritable variation / selection / experimental evolution tracks the surface

L5  historical architecture
    ancestral integration and later differentiation are reconstructed
```

The two-level SCH crossed design identifies L1 and part of L3. The multi-level design adds L2 and the causal optimum-shift test.

## Floral realization of Chapter 1

```text
function 1 = pollinator-mediated reproductive gain
function 2 = antagonist avoidance / reduction of antagonist-mediated loss
z          = floral attraction / display coordinate.
```

The registered local mechanism experiment crosses:

```text
A x antagonist x pollinator
8 cells.
```

For one two-level `A` contrast:

```text
d[g,p] = W[1,g,p] - W[0,g,p]
M_A(g)  = d[g,1] - d[g,0]
G_A(p)  = d[0,p] - d[1,p]
B_A     = d[0,0]
J_A     = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

This tells us whether pollination makes `A` more valuable and antagonism makes the same `A` less valuable. The multi-level extension asks whether those opposing routes generate distinct state optima and an integrated combined optimum.

## Role of the SCH literature

The literature is **real-world support for the architectural mechanism**. It establishes that shared floral traits can contribute to multiple functions, opposing selection occurs, stabilizing/context-dependent compromise is real, population trajectories can be redirected, and component partitioning or gating can reduce coupling.

It does not replace the chapter-specific causal experiment.

## Chapter 2 — BITA: release the shared-coordinate constraint

Chapter 2 asks:

> **Can increasing trait dimensionality allow the two functions to be tuned more independently?**

```text
shared state
function 1 ---\
               >--- z
function 2 ---/

more differentiated state
function 1 ---> x
function 2 ---> y.
```

The two-trait architecture is useful only if the added dimension reduces the functional coupling that generated the Chapter-1 compromise.

## Functional differentiation criteria

```text
D1  shared conflict exists
    Chapter 1 identifies opposing functional demands on z

D2  preferential functional loading
    x changes function 1 more strongly / cleanly than function 2
    y changes function 2 more strongly / cleanly than function 1

D3  dimensional release
    x moves toward the declared SCH reference and the joint phenotype
    reaches a better functional / fitness combination

D4  mechanism allocation
    selective interventions identify why the extra dimension improves,
    releases or reverses the original compromise

D5  historical modularization
    ancestral shared architecture -> derived functionally differentiated
    architecture reconstructed with phylogenetic / developmental evidence.
```

Contemporary experiments can establish D1-D4 without proving D5.

## The cross-chapter reference

The default empirical handoff is:

```text
SCH z_ref = z_P* = z_pollinator_context.
```

BITA tests whether:

```text
|x*(y1) - z_P*| < |x*(y0) - z_P*|.
```

This is **state-specific dimensional release**.

A stricter pure-function lane is allowed only if SCH independently identifies and exports:

```text
z_F1*.
```

Then BITA may additionally test release toward `z_F1*`. State-specific and pure-function release are not silently equated.

## Existing BITA as the floral implementation

```text
x = attraction trait A
y = antagonist-reducing trait D.
```

BITA's four-cell trait surface is:

```text
A0 = W10 - W00
A1 = W11 - W01
Delta_AD W = A1 - A0.
```

Its nested outcome claims remain:

```text
Level 1  positive interaction relief
         Delta_AD W > 0

Level 2  constraint release
         A0 <= 0 < A1

Level 3  strict reversal
         A0 < 0 < A1.
```

These local outcomes complement, but do not replace, the multi-level dimensional-release test.

## BITA mechanism allocation

The full floral implementation crosses:

```text
A x D x antagonist x pollinator
16 cells.
```

The mechanism channels remain:

```text
rho_delta    antagonist relief
iota_delta   pollinator interference
U_delta      remaining unallocated residual.
```

An independently validated remaining joint channel may be named only after its own assay; `U_delta` is not converted into a construction cost by subtraction.

The `A x D x G x P` interaction remains an internal test of residual functional coupling. A non-zero four-way term means the differentiated architecture is still only partially modular.

## Strongest Chapter-2 claim

The strongest contemporary claim is:

> **two partially independent trait coordinates allow the system to satisfy previously conflicting functional demands more independently than one shared coordinate, and crossed intervention identifies the ecological channels that generate that release.**

## Historical claim boundary

Contemporary functional modularity is supported by extant preferential loading and reduced cross-functional interference. Historical modularization additionally requires evidence that a lineage moved from an ancestrally integrated architecture toward the differentiated state.

Extant `A + D` alone does not prove that historical transition.

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
recover z_P*, z_G*, z_C* and causal compromise geometry
        ↓
optional SCH pure-function lane
independently identify z_F1*, z_F2* if possible
        ↓
BITA Stage 1
validate two functional coordinates x,y
        ↓
BITA Stage 2
test preferential loading and dimensional release toward z_P*
(optional stricter test toward z_F1*)
        ↓
BITA Stage 3
16-cell mechanism allocation + independent cost assay
        ↓
Historical extension
reconstruct integration -> differentiation / modularization.
```

## Joint claim ceiling

Together the sister projects aim to establish:

> **Multifunctionality can create compromise when different functions are constrained to a shared phenotypic coordinate; increasing trait dimensionality can release that measured compromise when functions become more independently tunable.**

The floral pollinator-antagonist / attraction-defence system is the first complete empirical implementation of that principle.
