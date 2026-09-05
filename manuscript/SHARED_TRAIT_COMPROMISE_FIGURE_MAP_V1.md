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
