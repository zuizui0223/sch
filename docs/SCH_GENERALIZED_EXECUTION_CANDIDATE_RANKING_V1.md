# SCH generalized execution candidate ranking v1

## Decision criterion

Candidate systems are ranked for **causal compromise identification**, not merely for multifunctionality.

```text
C1  one interpretable shared coordinate z
C2  z can be manipulated at >=3 informative levels
C3  function 1 and function 2 can be measured separately
C4  evidence suggests z1* != z2*
C5  one common fitness outcome is available
C6  functional weights can be selectively altered
C7  function-to-fitness paths are short
C8  evolutionary / heritable extension is feasible
C9  the conflict is active in the focal population / season.
```

`C9` is now explicit because the Dalechampia literature demonstrates geographic turnover in antagonist-mediated selection.

## Rank 1 conditional — Dalechampia bract/display system

### Why it remains the strongest positive case

Pérez-Barrales et al. (2013; DOI `10.1111/j.1600-0706.2013.20780.x`) studied a Mexican `D. scandens` population in which larger showy bracts increased bee visitation and pollen arrival, but also increased seed-predation probability; the integrated female-fitness surface tended toward stabilizing selection on bract size.

Armbruster et al. (2005; DOI `10.1890/04-1873`) experimentally reduced bract size in `D. ipomoeifolia` and reduced pollen arrival, demonstrating programme-level manipulability of the display coordinate.

### Why it is no longer an unconditional first choice

Opedal et al. (2019; DOI `10.1002/ajb2.1209`) studied three focal populations and 20 populations in northern Costa Rica. Seed-predation probability was largely unrelated to floral advertisement, and seed predators had only minor modifying effects on pollinator-driven advertisement evolution.

Therefore:

```text
Dalechampia case-level conflict:       RECOVERED
Dalechampia species-wide conflict:     NOT SUPPORTED
geographic turnover of w2:             RECOVERED
```

A focal Dalechampia population must first pass a conflict-activity screen.

Current score:

```text
C1 shared z:                    STRONG
C2 >=3-level manipulation:      PARTIAL
C3 separate functions:          STRONG
C4 z1* != z2* expectation:      STRONG IN POSITIVE POPULATION ONLY
C5 common fitness:              STRONG
C6 selective function weights:  MAIN BOTTLENECK
C7 short paths:                 STRONG
C8 evolutionary extension:      STRONG programme-level background
C9 focal conflict active:       MUST BE SCREENED
```

### Current execution contract

```text
population / season screen
-> recover pollinator + predator response to bract display
-> validate reversible multi-level z
-> recover controlled adult-weevil exposure window
-> validate selective G0/G1
-> only then run 5 z x 2 P x 2 G.
```

The preferred G pilot is controlled sequential adult-weevil exposure, because the exact Nanobaris oviposition window is not yet directly recovered. The 2013 study's interpretation of predation as adult oviposition choice is conditional on excluding differential larval success / movement as the explanation.

Full audit: `docs/SCH_DALECHAMPIA_GEOGRAPHIC_CONFLICT_AND_G0_RECOVERY_V1.md`.

Current status:

```text
CONDITIONAL_FIRST_CHOICE_CAUSAL_COMPROMISE_SYSTEM
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

If Dalechampia fails the focal-population or selective-G gates, Castilleja is promoted immediately rather than forcing Dalechampia to close L3.

## Rank 3 — Polemonium viscosum flower-size / water-cost system

The `Polemonium viscosum` programme provides a broad, non-antagonist realization of shared-trait conflict.

```text
function 1 = pollination / reproductive display
function 2 = water economy / viability
z          = corolla size.
```

Strengths:

- generalizes SCH beyond consumer conflict;
- water availability can change the weight of the physiological function;
- opposing reproductive versus physiological consequences are established.

Weaknesses:

- a direct multi-level manipulation of corolla size itself is not yet recovered;
- common total fitness spans a longer interval.

Current status:

```text
BEST_BROAD_PHYSIOLOGICAL_CONFLICT_CANDIDATE
```

## Rank 4 — Nicotiana attenuata benzylacetone system

`Nicotiana` remains the strongest same-coordinate mechanism and direct SCH -> BITA bridge.

Strengths:

- benzylacetone is manipulable;
- pollinator-mediated reproduction responds to BA;
- hawkmoth oviposition responds to the same BA axis;
- pollen-loading and egg-removal intervention components exist;
- direct bridge to BITA attraction x defence.

Weaknesses for the generalized optimum test:

- antagonist-to-common-fitness path is long;
- one hawkmoth can occupy both functional roles;
- combined P/G selectivity is unresolved;
- present evidence is strongest for local conflict rather than an internal multi-level optimum.

Current status:

```text
FIRST_CHOICE_LOCAL_MECHANISM_SYSTEM
FIRST_CHOICE_SCH_BITA_BRIDGE
NOT_AUTOMATICALLY_FIRST_CHOICE_COMPROMISE_SURFACE_SYSTEM
```

## Rank 5 — Ipomopsis aggregata floral-display system

Experimental flower-number manipulation changed hummingbird visitation, pre-dispersal seed predation and female reproductive success in the same system. This is unusually close to the desired architecture, but within the tested range the predation increase did not offset the fitness gain from larger displays.

Current status:

```text
NEAR_COMPLETE_NEGATIVE_OR_MONOTONIC_CONTROL
```

## Negative-control class — floral orientation

Experimental flower-angle systems such as `Platycodon grandiflorus` show:

```text
same z affects two functions
but z1* ~= z2*
-> multifunctionality without a compromise penalty.
```

These are important controls and must not be promoted as positive compromise cases.

## Current experimental strategy

### Lane A — causal compromise closure

```text
Dalechampia, conditional on focal-population screen
-> multi-level bract display
-> controlled predator exposure / selective G
-> common seed fitness
-> z1*, z2*, zc* + optimum-shift test

if Dalechampia gates fail
-> promote Castilleja or another short-path system.
```

### Lane B — local mechanism / direct BITA bridge

```text
Nicotiana
-> BA shared-coordinate mechanism
-> combined P/G selectivity
-> local SCH decomposition
-> preserve BA coordinate into BITA A x D.
```

### Lane C — negative-control architecture

```text
Platycodon / aligned-optimum system
-> same trait serves two functions
-> both functions favor the same state
-> multifunctionality != compromise.
```

## Ranking conclusion

```text
best system for shared-cue reality
!= best system for causal compromise geometry
!= best system for Chapter-2 continuity.
```

The updated conclusion is narrower than before: **Dalechampia is first only if a conflict-active population and selective antagonist intervention are recovered.** This geographic contingency is scientifically useful because SCH predicts that weakening one functional weight can move or erase the compromise itself.
