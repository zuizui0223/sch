# SCH–BITA symmetry contract v1

## Programme-level split

The SCH/BITA pair is defined at the level of trait architecture.

```text
SCH / Chapter 1 — BALANCE
multiple functional demands remain coupled on one trait coordinate z
-> where is the best shared phenotype z*?
-> how much fitness is lost because the functions must share that axis?

BITA / Chapter 2 — DIFFERENTIATION
allow partly independent trait coordinates x and y
-> how much of the Chapter 1 shared-axis loss can be recovered?
-> is that recovery large enough to pay for the extra architecture?
-> once several axes exist, what mechanism makes the multi-trait phenotype work?
```

Pollinator–antagonist floral cue sharing is SCH's most developed empirical case. Floral attraction × defence is BITA's most developed mechanism-identification case. Neither floral case defines the programme's general scope.

## 1. Shared mathematical interface

Let one measured trait coordinate `z` contribute to two functions with loss components `l1(z)` and `l2(z)`. While the phenotype remains on one shared axis,

```text
L_S(z) = l1(z) + l2(z)
z*     = argmin_z L_S(z)
L_S*   = L_S(z*)
```

`z*` is the best phenotype attainable while the functions remain coupled on the same coordinate. `L_S*` is the residual conflict load created by that architectural restriction, after choosing the best possible shared phenotype on the declared scale.

If the individual loss functions are normalized to zero at their separate optima, `L_S*` is directly the fitness opportunity available to an architecture that can decouple the functions. If an additional direct cost is present, it must either be represented explicitly in both architectures or kept outside the cross-chapter interface; it must not be silently absorbed on only one side.

### Quadratic common baseline

For

```text
l1(z) = w1 (z-theta1)^2
l2(z) = w2 (z-theta2)^2
```

the Chapter 1 optimum is

```text
z* = (w1 theta1 + w2 theta2)/(w1+w2)
```

and the unavoidable shared-axis conflict load is

```text
L_S* = [w1 w2/(w1+w2)] (theta1-theta2)^2.
```

This is exactly the `L_S*` used by the current BITA quadratic corollary.

## 2. Chapter 1 claim: balance on a shared axis

SCH asks what happens **while the two functions remain coupled to the same trait coordinate**.

An interior stable compromise on a fitness scale `W_S(z)=-L_S(z)` requires

```text
dW_S/dz at z* = 0
d2W_S/dz2 at z* < 0.
```

In the quadratic baseline this is automatically satisfied for positive `w1,w2`. The biological content lies in the location of `z*`, the distance between the function-specific optima, the relative weights placed on the two functions, and whether context changes those quantities.

Chapter 1 must distinguish the canonical interior-balance state from other one-axis outcomes already present in the SCH evidence spine:

- directional movement toward one end of the same axis;
- maintained polymorphism or frequency dependence;
- population-level evolutionary change;
- partial cue/component decoupling;
- historical branching or private-cue evolution, which require stronger evidence and are not established by an interior compromise alone.

The programme shorthand `BALANCE` therefore means **shared-axis optimization while the functions remain architecturally coupled**, not a claim that every system has one interior optimum.

## 3. Floral SCH mapping

For the current floral worked case, set `z=A` and write

```text
W(A) = M(A) - G(A) - C(A),
```

where `M` is pollinator-mediated reproductive benefit, `G` is antagonist-mediated reproductive loss and `C` is any direct physiological/construction cost that is not already standardized by design.

A local interior balance satisfies

```text
M'(A*) - G'(A*) - C'(A*) = 0
```

with negative local curvature of total fitness.

The current SCH contrasts

```text
M_A = change in pollinator-mediated benefit
G_A = change in antagonist-mediated cost
S_A = M_A - G_A
```

remain valid first-order empirical quantities. Cue overlap is one biological mechanism that makes the same `A` coordinate affect both channels. It is **not** the programme-level definition of Chapter 1.

Current evidence supports bounded examples of integrated compromise, context-dependent polymorphism maintenance, population evolutionary change and partial cue decoupling. It does not yet supply a cross-system estimate of `z*` or `L_S*`, nor a replicated historical shared-cue -> private-cue transition.

## 4. Chapter 2 handoff

BITA receives the Chapter 1 shared architecture as its baseline. Let `R` be the amount of `L_S*` recoverable after expanding the phenotype space and let `K` be the additional fixed architecture cost.

General BITA result:

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0  <=>  K < R.
```

For the matched quadratic model with residual coupling,

```text
R = s L_S*
Delta_arch = s L_S* - K,
```

where `s` is the retained fraction of function-specific trait separation.

The logical handoff is therefore

```text
SCH measures/characterizes the best attainable shared solution
                 z*, L_S*
                      |
                      v
BITA asks whether a larger architecture can recover enough of L_S*
                 R = recoverable loss
                      |
                      v
                 compare R with K
```

The Chapter 2 theory does not require pollination, antagonists or defence. Conversely, SCH does not require a second trait axis or a two-trait interaction estimand.

## 5. Symmetry table

| Dimension | SCH / Chapter 1 | BITA / Chapter 2 |
|---|---|---|
| Architectural question | Best solution while functions share one axis | Whether relaxing the shared-axis restriction pays |
| State variables | one shared coordinate `z` | partly independent coordinates `x,y` |
| Core optimum | `z* = argmin L_S(z)` | `(x*,y*) = argmin L_D(x,y)` |
| Core quantity | shared conflict load `L_S*` | recoverable loss `R` and architecture gain `Delta_arch` |
| Quadratic result | `L_S* = w1w2/(w1+w2) (theta1-theta2)^2` | `R=sL_S*`, `Delta_arch=sL_S*-K` |
| Main ecological uncertainty | where/why the shared balance is maintained or redirected | how much decoupling is realized and what mechanism produces the joint fitness effect |
| Floral worked case | shared floral cue tracked by pollinators and antagonists | attraction × defence plus crossed consumer intervention |
| Historical ceiling | private-cue origin / lineage branching not established | historical origin of a second trait axis not established |

## 6. Non-equivalences that must remain explicit

```text
interior balance
!= proof that the architecture cannot differentiate

one-axis directional change
!= trait differentiation

partial cue decoupling
!= historical origin of a new module

positive multi-trait interaction
!= historical splitting

structural differentiation
!= functional independence

route or case recurrence
!= prevalence.
```

## 7. Editorial consequence

The sister-paper framing should be expressed consistently in both repositories:

```text
Chapter 1 / SCH
How do conflicting functions resolve selection while they remain coupled on one trait?
-> characterize z* and the shared conflict load L_S*

Chapter 2 / BITA
When does relaxing that shared-axis constraint pay?
-> recover R from L_S*, subtract K, then identify the mechanism of the resulting architecture
```

This contract changes the programme-level framing, not the evidentiary ceiling of existing SCH floral cases. General notation must not be mistaken for empirical estimation of `L_S*` where the underlying studies do not provide it.
