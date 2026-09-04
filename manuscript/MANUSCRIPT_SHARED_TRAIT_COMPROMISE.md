# Shared traits, opposing functions, and the evolution of compromise

## Abstract

A single phenotype often performs more than one ecological function. When those functions favor different regions of trait space, one shared coordinate can impose a compromise. SCH separates the theory of this constraint from what a crossed experiment can directly identify. At the theory level, pure function-specific objectives may have optima `z_F1*` and `z_F2*`. In the empirical floral implementation, however, a multi-level `z x pollinator x antagonist` experiment directly identifies state-specific reproductive optima `z_P* = argmax W10(z)`, `z_G* = argmax W01(z)`, and the combined optimum `z_C* = argmax W11(z)`. Because consumer-independent and direct trait consequences can remain in every reproductive state, `z_P*` is not automatically `z_F1*`, and `z_G*` is not automatically `z_F2*`. The decisive empirical compromise result therefore combines distinct state optima, an interior combined optimum, opposing shifts when either functional demand is removed, and opposing functional-component gradients near the combined optimum. Existing floral studies provide real-world evidence that shared traits experience opposing ecological demands, that stabilizing or context-dependent compromise occurs, and that changing interaction regimes redirects evolutionary trajectories. Literature is therefore ecological grounding rather than the chapter estimand. Chapter 2 / BITA asks whether adding a second, preferentially loaded trait dimension releases the measured one-dimensional constraint.

## 1. The general problem

Traits are often multifunctional. A floral scent can recruit a pollinator and expose a plant to an antagonist; a structure can advertise reproduction while also protecting tissues; a chemical can mediate attraction, defence, physiology, or communication. The evolutionary problem is not multifunctionality alone. It is whether different functional demands pull one shared phenotypic coordinate in different directions.

Let the shared trait be `z`. At the theory level, define pure function-specific objectives

```text
F1(z)
F2(z)
```

with optima

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z).
```

Older shorthand in this programme used `z1*` and `z2*` for the same theory-level quantities. The explicit `z_F1*`, `z_F2*` notation is now preferred because it prevents them from being confused with experimentally observed state optima.

If

```text
z_F1* != z_F2*,
```

one coordinate cannot simultaneously maximize both pure objectives. A simple total-fitness representation is

```text
W_shared(z) = w1 F1(z) + w2 F2(z) - C(z),
```

where `C(z)` represents direct or background consequences not assigned to either focal function.

## 2. What counts as compromise

An intermediate phenotype is not sufficient evidence of compromise.

### 2.1 Multifunctionality

The same declared coordinate must affect both focal functional routes.

### 2.2 Functional conflict

The two functional routes must favor different regions of the coordinate. At the theory level this can be expressed as `z_F1* != z_F2*`. Empirically, the minimum direct test is that the state favored when one competing route is suppressed differs from the state favored when the other is suppressed.

### 2.3 Balance

At an integrated compromise, the total gradient can be near zero while component gradients remain non-zero and oppose each other. Balance therefore means cancellation of selection contributions, not equality of raw benefits or costs.

The strongest evidence is causal: weakening one functional demand should move the realized optimum toward the state favored when that demand is suppressed.

## 3. Theory benchmark versus empirical estimands

Near pure function optima, an idealized mismatch-loss benchmark is

```text
L_shared(z)
  = a (z - z_F1*)^2
  + b (z - z_F2*)^2.
```

The theory-level shared optimum is

```text
z_C,theory* = (a z_F1* + b z_F2*) / (a + b)
```

and the ideal one-dimensional mismatch penalty is

```text
L_compromise,theory*
  = [a b / (a + b)] (z_F1* - z_F2*)^2.
```

This benchmark predicts that the potential value of an extra trait dimension increases as pure functional optima diverge and both functional demands remain strong.

But this formula is not an instruction to relabel experimental state optima as pure function optima. In the crossed reproductive experiment, direct/background effects remain unless independently assayed.

## 4. Two complementary SCH experiments

SCH separates local conflict identification from multi-level compromise identification.

### 4.1 Local crossed intervention

For one floral trait contrast `A`, cross

```text
A x antagonist x pollinator
```

in eight cells on one common reproductive outcome `W`.

Define

```text
d[g,p] = W[1,g,p] - W[0,g,p]
M_A(g) = d[g,1] - d[g,0]
G_A(p) = d[0,p] - d[1,p]
B_A    = d[0,0]
J_A    = d[1,1] - d[1,0] - d[0,1] + d[0,0].
```

A positive `M_A(g)` identifies a pollinator-mediated contribution to the reproductive value of the same trait contrast. A positive `G_A(p)` identifies antagonist-mediated erosion of that value. `B_A` remains an unallocated consumer-independent remainder without an independent assay, and `J_A` diagnoses state dependence between the two pathways.

This experiment shows why a local trait contrast is conflicted. It **does not by itself locate the full compromise optimum**.

### 4.2 Multi-level `z` experiment

Manipulate at least three and preferably five or more levels of the same coordinate and cross them with selective pollinator and antagonist states.

The directly observed reproductive surfaces are

```text
W00(z) = P0 G0
W10(z) = P1 G0
W01(z) = P0 G1
W11(z) = P1 G1.
```

The directly identified optima are

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

These are state-specific reproductive optima.

Critically,

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The equality would require an additional assay or identifying restriction that removes or measures direct/background trait effects.

## 5. The causal compromise test

A strong empirical Chapter-1 result requires four linked observations.

First, `z_P*` and `z_G*` differ by a biologically meaningful amount. Second, `W11(z)` has a supported interior optimum `z_C*`. Third, removing antagonism moves the combined optimum toward `z_P*`, while removing pollination moves it toward `z_G*`. Fourth, the pollinator-mediated and antagonist-mediated component gradients near `z_C*` are non-zero and oppose one another.

In shorthand:

```text
z_P* != z_G*

G off: z_C* -> z_P*
P off: z_C* -> z_G*

sign[g_P(z_C*)] != sign[g_G(z_C*)].
```

The zero derivative of an interior quadratic at its own fitted vertex is not treated as independent evidence; it is a mathematical property of the fit.

## 6. Real-world evidence

The literature is a reality check on the mechanism rather than the primary estimator of SCH quantities.

Pérez-Barrales et al. provide the clearest case-level match: larger showy bracts increase pollination opportunity while also increasing seed-predator exposure, and net selection tends toward stabilizing selection. Theis & Adler experimentally show the negative side of the same logic: enhancing fragrance can increase antagonist attraction and reduce seed production without a compensating pollinator gain. Primula studies show that opposing interaction regimes can maintain polymorphism and shift morph frequencies, while multigeneration Brassica experiments show that antagonism can redirect pollinator-driven evolutionary trajectories.

These studies demonstrate that functional conflict, compromise, context dependence, and evolutionary redirection are real. They do not replace the same-coordinate intervention needed to identify SCH's causal geometry in one system.

## 7. Current execution systems

`Dalechampia` is the conditional first-choice compromise-surface system because a Mexican population provides strong opposing pollinator/seed-predator selection, but Costa Rican populations show that the conflict is not species-wide. It therefore requires population qualification before the full factorial.

`Nicotiana attenuata` remains the strongest local shared-cue mechanism and direct SCH-to-BITA bridge because benzylacetone affects pollinator-mediated reproduction and hawkmoth oviposition on the same attraction axis.

`Castilleja linariaefolia` is a high-value fallback for short antagonist-to-seed pathways, but its focal trait manipulation and selective predator intervention still require Stage-0 development.

Aligned-optimum systems such as experimental flower-orientation cases remain important negative controls: multifunctionality does not imply compromise when both functions favor the same state.

## 8. Literature programme and claim boundary

The frozen systematic cohort contains 868 records. Through V20, 405 records have title/abstract decisions and 117 primary studies are included. Only two studies satisfy the strict linked architecture requiring a manipulated focal trait, both consumer responses, and a common reproductive outcome. These are workflow/evidence counts, not natural prevalence and not the SCH estimand.

Their role is to establish that constituent routes recur, that predicted evolutionary outcomes exist, and that complete identifying experiments are rare.

## 9. From compromise to differentiation

Chapter 1 ends with one-dimensional constraint:

```text
function 1 ---\
               >--- shared trait z ---> compromise / balance
function 2 ---/
```

Chapter 2 asks what happens when another phenotypic dimension becomes available:

```text
shared compromise
      ↓
function 1 -> trait x
function 2 -> trait y
      ↓
functional differentiation / modularization.
```

The default empirical cross-chapter prediction is now deliberately conservative:

> adding a function-2-facing coordinate `y` should move the optimum of retained coordinate `x` toward the **SCH state-specific function-1-facing reference `z_P*`**.

Only if SCH independently identifies the pure function-1 objective should that stricter target be called `z_F1*`.

**Contemporary functional differentiation is distinct from historical modularization.** Demonstrating preferential loading and dimensional release in extant traits **does not prove that an ancestral shared trait split** into two descendant traits.

## 10. Main predictions

1. The same shared coordinate affects both focal functional routes.
2. The intervention-defined state optima differ: `z_P* != z_G*`.
3. The combined state has a supported interior optimum `z_C*` over the tested range.
4. Removing each functional demand moves the optimum toward the state favored when that demand is absent.
5. Functional-component gradients near `z_C*` oppose one another.
6. Systems with stronger measured state-specific conflict should offer greater opportunity for dimensional release, while theory predicts the ideal upper bound from pure `z_F1*` and `z_F2*` when those quantities are independently identified.
7. Partial modularity should leave residual cross-loading or context dependence.

## 11. Current claim ceiling

Current literature supports real-world multifunctional conflict, case-level compromise, context-dependent maintenance, evolutionary redirection, and partial decoupling. The complete causal same-coordinate experiment has not yet been executed on a biological dataset.

Current status:

```text
MULTIFUNCTIONAL_CONFLICT_REALITY_RECOVERED
CASE_LEVEL_COMPROMISE_RECOVERED
STATE_SPECIFIC_CAUSAL_COMPROMISE_ANALYZER_READY
PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED_BY_DEFAULT
COMPLETE_CAUSAL_COMPROMISE_EXPERIMENT_NOT_YET_EXECUTED.
```

## 12. Conclusion

Multifunctionality can constrain evolution because several functional demands are forced to share one coordinate. SCH turns this into an identifiable problem without confusing theory symbols with experimental estimands. The crossed experiment directly asks whether selective functional demands generate distinct state-specific optima, whether their joint state has an interior optimum, and whether changing functional weights moves that optimum predictably. Pure function optima remain a stricter target requiring independent identification of direct/background pathways. This separation makes the Chapter-1 result both stronger and cleaner, and it gives BITA a defensible empirical reference for testing whether an additional trait dimension releases the measured constraint.
