# SCH generalized execution candidate ranking v1

## Decision criterion

After generalizing SCH, candidate systems are ranked for **causal compromise identification**, not merely for multifunctionality.

A high-value system should satisfy as many of the following as possible:

```text
C1  one interpretable shared coordinate z
C2  z can be manipulated at >=3 informative levels
C3  function 1 and function 2 can be measured separately
C4  evidence suggests z1* != z2*
C5  one common fitness outcome is available
C6  functional weights can be selectively altered
C7  function-to-fitness paths are short
C8  evolutionary / heritable extension is feasible.
```

## Rank 1 — Dalechampia bract/display system

### Why it ranks first

Pérez-Barrales et al. (2013; DOI `10.1111/j.1600-0706.2013.20780.x`) already recover the exact qualitative Chapter-1 geometry: larger showy bracts increase bee visitation and pollen arrival, but also increase seed-predator oviposition; net selection on bract size tends toward stabilizing selection.

The broader *Dalechampia* programme also supplies manipulation feasibility. Armbruster et al. (2005; DOI `10.1890/04-1873`) experimentally reduced bract size in *D. ipomoeifolia* and observed reduced pollen arrival, demonstrating that the display coordinate is experimentally alterable.

Current score:

```text
C1 shared z:                    STRONG
C2 >=3-level manipulation:      PARTIAL / needs one-system implementation
C3 separate functions:          STRONG
C4 z1* != z2* expectation:      STRONG
C5 common fitness:              STRONG
C6 selective function weights:  PARTIAL
C7 short paths:                 STRONG
C8 evolutionary extension:      STRONG programme-level background
```

### Missing closure

The key missing experiment is not another observational selection analysis. It is one system/population in which bract size is manipulated over multiple levels while pollinator and seed-predator pathways are independently varied or quantified on the same flowers.

Target result:

```text
recover z_pollinator*
recover z_seed-predator-avoidance*
recover z_combined*
selectively suppress seed predators -> z_combined* shifts toward z_pollinator*.
```

Current status:

```text
FIRST_CHOICE_CAUSAL_COMPROMISE_SYSTEM
```

## Rank 2 — Castilleja linariaefolia calyx/display system

Cariveau et al. (2004; DOI `10.1111/j.0030-1299.2004.12641.x`) recover opposing selection on calyx length through pollination versus pre-dispersal seed predation, with relative seed set as the fitness scale.

Strengths:

- distinct pollinator and seed-predator pathways;
- short antagonist-to-seed-loss path;
- opposing selection already recovered;
- common female fitness is natural.

Weakness:

- the focal calyx coordinate was observational in the key source;
- a clean multi-level manipulation must be validated.

Current status:

```text
HIGH_VALUE_SHORT_PATH_CANDIDATE
```

## Rank 3 — Polemonium viscosum flower-size / water-cost system

The *Polemonium viscosum* programme provides a broad, non-antagonist realization of shared-trait conflict.

Evidence includes:

- pollinator-mediated positive selection on corolla morphology;
- direct physiological evidence that larger corollas use more water;
- drought-dependent demographic costs of large flowers;
- experimental watering that changes the cost regime.

The mapping is

```text
function 1 = pollination / reproductive display
function 2 = water economy / viability
z          = corolla size.
```

Strengths:

- generalizes SCH beyond consumer conflict;
- function-2 weight is experimentally manipulable through water availability;
- strong evidence for opposing reproductive versus physiological consequences.

Weakness:

- direct multi-level manipulation of corolla size itself is not yet recovered;
- common total fitness may require integrating survival and reproduction over a longer interval.

Current status:

```text
BEST_BROAD_PHYSIOLOGICAL_CONFLICT_CANDIDATE
```

## Rank 4 — Nicotiana attenuata benzylacetone system

*Nicotiana* remains the strongest same-coordinate mechanistic reality anchor for the original floral shared-cue realization.

Strengths:

- benzylacetone is directly manipulable;
- pollinator-mediated reproduction responds to BA;
- hawkmoth oviposition responds to the same BA axis;
- pollination and egg-removal intervention components exist;
- direct bridge to BITA attraction x defence.

Weaknesses for the generalized Chapter-1 optimum test:

- the antagonist-to-common-fitness path is long;
- the same hawkmoth can occupy both functional roles;
- combined selectivity is still the critical gate;
- current evidence is strongest for local conflict, not a multi-level internal optimum.

Current status:

```text
FIRST_CHOICE_LOCAL_MECHANISM_SYSTEM
NOT_AUTOMATICALLY_FIRST_CHOICE_COMPROMISE_SURFACE_SYSTEM
```

## Rank 5 — Ipomopsis aggregata floral-display system

An experimental manipulation of flower number altered hummingbird visitation, pre-dispersal seed predation, and female reproductive success in the same system.

This is unusually close to the desired architecture because `z` is directly manipulated and both functions plus common fitness are measured.

However, within the tested range greater seed predation did not offset the fitness gains of larger displays. The recovered result is therefore a strong local multifunctionality design but **not a positive compromise result**.

Current status:

```text
NEAR_COMPLETE_NEGATIVE_OR_MONOTONIC_CONTROL
```

A wider or more finely resolved display gradient could still test whether curvature appears outside the original contrast.

## Negative-control class — floral orientation

Experimental floral-angle studies in *Platycodon grandiflorus* show that one coordinate can affect both pollination and rain protection, but horizontal orientation benefits both functions over important alternatives. This is a critical control for the theory:

```text
same z affects two functions
but z1* ~= z2*
-> multifunctionality without a compromise penalty.
```

Such systems should not be promoted as positive SCH compromise cases.

## Current experimental strategy

Use two parallel lanes rather than forcing one species to do everything.

### Lane A — strongest causal compromise closure

```text
Dalechampia
-> recover one manipulable bract-size coordinate
-> >=3 levels
-> pollinator and seed-predator functions
-> common seed fitness
-> predator suppression / functional-weight shift.
```

### Lane B — local mechanism / direct BITA bridge

```text
Nicotiana
-> BA shared-coordinate mechanism
-> combined P/G selectivity
-> local 8-cell SCH
-> preserve BA coordinate into BITA A x D.
```

### Lane C — negative-control architecture

```text
Platycodon / aligned-optimum system
-> same trait serves two functions
-> both functions favor the same state
-> demonstrate that multifunctionality alone does not imply compromise.
```

## Ranking conclusion

The generalized framing changes the execution priority:

```text
best system for shared-cue reality
!= best system for causal compromise geometry
!= best system for Chapter-2 continuity.
```

Dalechampia currently ranks first for the Chapter-1 compromise claim, whereas Nicotiana remains first for the local shared-cue mechanism and direct BITA hand-off.
