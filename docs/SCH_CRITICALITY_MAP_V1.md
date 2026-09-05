# SCH criticality map v1

## Decision

SCH and BITA do **not** start with the same intrinsic critical point.

SCH fixes one shared trait axis and asks how competing functions balance on it. In the current unbounded convex quadratic benchmark, changing functional weights moves the shared optimum continuously. There is no internal shared-versus-differentiated phase switch because the differentiated architecture is not part of the SCH state space.

BITA enlarges the state space and compares two optimized architectures. That comparison has a genuine architecture boundary.

The two chapters can nevertheless be placed on one common critical surface once Chapter-2 decoupling and architecture cost are imported into the Chapter-1 coordinate system.

## Three different boundaries

### C0 — SCH intrinsic conflict onset

For the quadratic shared world,

```text
L_S(z) = w1(z-theta1)^2 + w2(z-theta2)^2
```

and

```text
L_S* = [w1 w2/(w1+w2)](theta1-theta2)^2.
```

The intrinsic no-conflict boundary is

```text
L_S* = 0.
```

With positive weights this occurs at `theta1=theta2`; in the limiting case it also occurs when one functional weight vanishes.

Crossing `L_S*=0` creates functional conflict, but it does **not** by itself trigger a change of architecture. For every finite positive pair of weights in the current convex model, the shared optimum moves continuously.

Thus:

```text
C0 = conflict onset
!= balance -> differentiation switch.
```

### C1 — empirical dimensional-release onset

SCH's actual multi-level crossed experiment identifies state-specific optima

```text
z_P*, z_G*, z_C*.
```

The direct Chapter-2 continuation estimates whether an added coordinate moves the retained optimum toward the frozen SCH state-specific reference. The corresponding geometric release boundary is

```text
R_state = 0.
```

This is expressed in trait-distance units. It is not automatically a fitness-scale architecture boundary.

### C2 — common architecture critical surface

Let

```text
R = fitness loss recoverable by the differentiated architecture before fixed cost
K = additional architecture cost.
```

The common architecture boundary is

```text
Phi = R-K = 0.
```

In the quadratic BITA benchmark,

```text
R = s L_S*
```

so

```text
s L_S* = K.
```

This is the boundary that can be viewed from both chapters.

## Chapter-1 projection of the architecture boundary

If BITA supplies `s` and `K`, SCH can express C2 as a critical shared conflict load:

```text
L_S,crit* = K/s.
```

Therefore:

```text
L_S* < K/s  -> shared compromise remains fitter
L_S* = K/s  -> common architecture critical surface
L_S* > K/s  -> differentiated architecture would be fitter if accessible.
```

This is a **counterfactual cross-world projection**. It is not an intrinsic transition generated inside the fixed one-axis SCH world.

If the control variable is the distance between pure function optima, the same quadratic boundary is

```text
|theta1-theta2|_crit
 = sqrt[
     K (w1+w2) (w1 w2 + lambda(w1+w2))
     / (w1^2 w2^2)
   ].
```

This gives SCH a precise answer to "how much conflict would be enough to make differentiation pay?" once the Chapter-2 architecture parameters are declared.

## Chapter-2 projection of the same boundary

The identical surface can instead be parameterized as

```text
K_crit = s L_S*
```

or, for fixed `L_S*` and `K>0`,

```text
s_crit = K/L_S*.
```

Because

```text
s = w1 w2 / [w1 w2 + lambda(w1+w2)],
```

the critical residual coupling is

```text
lambda_crit
 = [w1 w2/(w1+w2)] (L_S*/K - 1)
```

when `0<K<L_S*`.

These are not new critical surfaces. They are different coordinate projections of the same `Phi=0` surface.

## Reference cross-check

Use

```text
w1=w2=1
K=0.1.
```

### Hold coupling at lambda=1

Then

```text
s = 1/3
L_S,crit* = 0.1/(1/3) = 0.3.
```

Since

```text
L_S* = 0.5 (theta1-theta2)^2,
```

the critical function-optimum distance is

```text
|theta1-theta2|_crit = sqrt(0.6)
                     = 0.7745966692...
```

### Hold function-optimum distance at 1

Then

```text
L_S* = 0.5
s_crit = 0.1/0.5 = 0.2.
```

Solving the coupling expression gives

```text
lambda_crit = 2.
```

Thus the Chapter-1 projection (`critical conflict distance`) and the Chapter-2 projection (`critical coupling`) land on the same architecture surface.

## Are the two chapter critical points "the same"?

### Theory answer

**Yes, for C2.** Once both worlds are mapped onto common fitness units and share the same architecture model, `L_S,crit*=K/s`, `K_crit=sL_S*`, `s_crit=K/L_S*`, and `lambda_crit` are coordinate descriptions of one boundary.

### Intrinsic-world answer

**No.** SCH's intrinsic conflict onset `C0` is a boundary inside the one-axis description. BITA's architecture switch `C2` compares one-axis and multi-axis worlds. They coincide only in special limiting cases, most transparently when `K=0`: then any positive recoverable conflict can make the differentiated world weakly preferable, and the projected C2 load collapses to zero.

### Current empirical answer

**Not yet testable as one numerical point.** Current SCH state-optimum quantities and BITA `R_state` are geometric/causal estimands, whereas the architecture boundary requires a commensurable recoverable fitness amount and architecture cost. A numeric claim that both empirical chapters cross "the same point" therefore requires:

1. a positive SCH causal-compromise receipt;
2. the same biological context and a frozen state-specific reference;
3. a positive BITA dimensional-release receipt;
4. a common reproductive fitness scale across shared and differentiated states;
5. a declared/estimated architecture-cost lane;
6. a decoupling/residual-coupling estimate on that same context.

Until those are available, the honest result is:

```text
THEORY_CRITICAL_SURFACE: SAME
INTRINSIC_CHAPTER_BOUNDARIES: DIFFERENT
EMPIRICAL_RAW_CRITICALITIES: PARALLEL_PROJECTIONS_NOT_YET_COMMENSURATED.
```

## Implementation

- `scripts/analyze_chapter1_criticality.py`
- `tests/test_chapter1_criticality.py`

The analyzer deliberately labels the Chapter-1 architecture threshold as a projection imported from BITA rather than an intrinsic phase transition.
