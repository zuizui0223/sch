# Chapter 1 to Chapter 2 positioning

## Dissertation-level question

How do plants evolve floral signals when the same phenotype affects both mutualists and antagonists, and when can an additional defensive trait improve, release or reverse the resulting fitness constraint?

## Chapter 1 — SCH: why attraction becomes conflicted

SCH begins with one attraction/display coordinate `A`.

```text
W(A) = M(A) - G(A) - C(A)
```

Its empirical question is how pollinator benefit and antagonist loss move on that same coordinate. Shared cue use creates the conflict: when both audiences respond to the same sensory component of `A`, increasing attraction can increase pollinator benefit and antagonist exposure together. The plant cannot optimize the pollinator-facing effect independently unless the two response slopes differ enough or another ecological or architectural process breaks the linkage.

Its evolutionary question is which of six bounded outcomes the resulting conflict supports:

- an integrated interior compromise;
- directional specialization on the same coordinate;
- context-dependent polymorphism maintenance;
- population differentiation or measured microevolution;
- lineage branching from an ancestral shared cue; or
- cue modularization that creates more separable coordinates.

The current positive result goes beyond existence of shared tracking. Case-level evidence recovers an integrated stabilizing compromise, context-dependent maintenance of alternative morphs, and population-level evolutionary change. Component partitioning and conditional emission recover partial decoupling mechanisms.

The historical endpoint is a separate fail-closed ladder. A targeted eight-candidate audit finds phylogenetic pollinator-associated scent divergence, contemporary temporal gating, dual pollinator/seed-predator selection and a useful weak-conflict negative control, but no study in the audited set joins an ancestral shared cue, descendant private architecture, both receiver channels, replicated transitions and alternative-history tests. Thus private-cue origin and lineage branching remain `NOT_EVALUABLE`, not absent.

## Chapter 2 — BITA: adding a defence coordinate

BITA asks what a distinct antagonist-reducing trait `D` changes on the same declared reproductive scale. For the four trait states, define

```text
A0 = W10 - W00
     attraction effect when defence is low

A1 = W11 - W01
     attraction effect when defence is high

Delta_AD W = W11 - W10 - W01 + W00
           = A1 - A0
           = rho_delta - iota_delta - kappa_delta
```

The four-cell surface supports three nested outcome claims.

```text
Level 1 — positive interaction relief
Delta_AD W > 0
D shifts the effect of attraction in a positive direction.

Level 2 — constraint release
A0 <= 0 and A1 > 0
Attraction is non-beneficial without D but beneficial with D.

Level 3 — strict sign reversal
A0 < 0 and A1 > 0
D changes attraction from detrimental to beneficial.
```

Therefore

```text
strict reversal
    => constraint release
    => positive interaction relief
```

but the reverse implications do not hold. A positive `Delta_AD W` can occur while `A0` and `A1` are both negative.

## Outcome and explanation are separate ladders

Within the BITA bookkeeping model,

```text
rho_delta > iota_delta + kappa_delta
    <=> Delta_AD W > 0
```

This equivalence decides the Level-1 total-interaction inequality on the declared outcome scale. It does not decide whether attraction crossed zero. Levels 2 and 3 require the conditional attraction contrasts `A0` and `A1`.

Mechanism allocation is a further question. Allocating the total surface to antagonist relief, pollinator interference and a remaining joint channel requires selective crossed interventions, pollinator-absent baseline handling, a separability diagnostic and an independent cost assay.

Thus four questions must not be collapsed:

1. **Did `D` improve the attraction effect?** Use `Delta_AD W`.
2. **Did that improvement release a non-beneficial state?** Use `A0 <= 0 < A1`.
3. **Did it strictly reverse a negative state?** Use `A0 < 0 < A1`.
4. **Why did the outcome occur?** Allocate `rho_delta`, `iota_delta` and the independently validated joint channel.

Full channel point identification is not required for a valid outcome-level decision. Conversely, neither a positive interaction nor a zero crossing identifies a realized mechanism allocation.

## Informational versus functional outcomes

The chapters distinguish changes to receiver overlap from changes to reproductive consequences.

| Form | What changes | What it establishes | What it does not establish |
|---|---|---|---|
| **Informational / architectural escape** | pollinator-facing and antagonist-facing cue coordinates become separable or private | reduced receiver overlap on the signal itself | any particular `A × D` reproductive interaction |
| **Functional interaction relief** | a distinct defence coordinate makes the attraction effect less negative or more positive | `Delta_AD W > 0` on the declared scale | zero crossing, cue privacy or mechanism allocation |
| **Functional constraint release** | attraction changes from non-beneficial to beneficial across defence states | `A0 <= 0 < A1` | cue privacy, historical shared-to-private evolution or channel allocation |
| **Strict functional reversal** | attraction changes from detrimental to beneficial | `A0 < 0 < A1` | disappearance of antagonist detection or a historical signal transition |

BITA can therefore improve or even reverse the reproductive consequence of cue sharing while the SCH conflict remains informationally present. Antagonists may still detect `A`; `D` can act later through access, ingestion, oviposition, damage or another antagonist-reducing route.

## Current BITA evidence ceiling

Kessler et al. 2008 supplies a manipulated `A × D`-like field factorial. Published rounded capsule proportions preserve a positive total interaction range and a positive attraction effect under the defended state, but the attraction effect without defence remains compatible with either side of zero. The exact source/design-based intervals have not been recovered, and nicotine suppression is systemic rather than cleanly flower-restricted.

The current bounded interpretation is therefore:

```text
Level 1: strong positive aggregate-sign anchor;
         formal source/design uncertainty unresolved
Level 2: unresolved
Level 3: unresolved
mechanism allocation: unresolved
flower-specific D scope: unresolved for the historical manipulation
```

Kessler is not evidence that `Delta_AD W > 0` automatically equals release of a previously negative attraction effect.

## Nicotiana as a programme-level composite bridge

The broader *Nicotiana attenuata* programme is the highest-information current candidate for closing the SCH–BITA sequence, but the evidence is distributed across papers.

```text
Kessler 2015
A affects pollinator-mediated outcrossing and hawkmoth oviposition

Kessler 2008
an A × D-like reproductive factorial with a positive aggregate sign

Li 2017
flower-specific jasmonate-regulated defence biology

Li 2018
an upstream-pleiotropy warning because JA perturbation also changes attraction/reward outputs
```

This programme is classified

```text
PROGRAM_COMPOSITE_NEAR_COMPLETE
DIRECT_COMPLETE_CHAIN_NOT_ESTABLISHED
```

Results from these papers cannot be pooled as cells of one experiment. The direct closure requires one invariant attraction manipulation, one independently validated flower-specific defence manipulation, both receiver channels, one common reproductive outcome, `A0`, `A1` and `Delta_AD W` with compatible uncertainty, followed separately by selective channel and independent-cost measurements.

The detailed contract is `docs/NICOTIANA_PROGRAM_COMPOSITE_BRIDGE_V1.md` in SCH and `docs/NICOTIANA_SCH_BITA_CHAIN_CLOSURE_V1.md` in BITA.

## The two chapters answer one sequence

```text
Chapter 1: Why does one shared attraction coordinate create conflict,
           and which one-axis or architectural responses follow?
        ↓
Chapter 2a: Does a second defensive coordinate improve the
            attraction effect?  [Delta_AD W]
        ↓
Chapter 2b: Does that improvement cross from non-beneficial or
            negative to positive?  [A0 and A1]
        ↓
Chapter 2c: Which relief / interference / joint-channel mechanism
            produces the outcome?
```

The chapters therefore share biological motivation but not estimands. SCH must not claim that BITA tested the one-trait hypothesis. BITA may use SCH to state the constraint that motivates `D`, then report separately how far current data recover receiver overlap, interaction relief, constraint release, strict reversal and mechanism allocation.

## Joint claim ceiling

Together the current repositories support a staged result: dual-audience signal conflict has multiple documented evolutionary responses; selective defence architectures recur; and a second trait can produce positive interaction-level improvement in a close historical factorial. Three stronger intersections remain open.

1. SCH has not reconstructed a replicated historical shared-cue-to-private-cue transition.
2. BITA has not recovered source/design-based intervals that establish Level 1, Level 2 or Level 3 with clean flower-specific intervention scope in one complete system.
3. No screened system allocates the complete outcome among the two biotic channels and an independently validated joint channel.

These missing intersections now define specific analyses and experiments rather than an undefined call for more data.
