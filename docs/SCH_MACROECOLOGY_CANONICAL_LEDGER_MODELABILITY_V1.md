# SCH macroecology canonical ledger and H1 modelability gate V1

## Canonical model units

The complete current source-axis recode has now been collapsed into one row per canonical biological trait axis.

```text
57 source-axis evidence records
- 7 source-axis records failing geometry eligibility
= 50 model-eligible/boundary source-axis records
-> 48 canonical biological trait axes
```

The canonical ledger is:

`data/SCH_MACROECOLOGY_CANONICAL_TRAIT_AXIS_LEDGER_V1.csv`

It retains source provenance, cluster identity, trait domain, consumer-role architecture, antagonist guild, context status and the canonical ecological geometry.

## Current canonical geometry

Across all 48 canonical axes:

```text
CONFLICT                    9
ALIGNMENT / REINFORCEMENT   2
ONE-SIDED / NULL            8
CONTEXT-VARIABLE            1
ROLE BOUNDARY              13
UNRESOLVED                 15
```

The role-boundary category includes role-dependent consumers and intrinsically benefit-cost-coupled interactions. These axes are not forced into the fixed-antagonist H1 analysis.

## Static fixed-role H1 frontier

The primary static H1 denominator currently contains only fixed-role axes with a resolved, non-context-variable geometry.

```text
static resolved fixed-role axes     19
independent biological clusters     13

CONFLICT                             9
ALIGNMENT / REINFORCEMENT            2
ONE-SIDED / NULL                     8
```

Six of the thirteen contributing biological clusters contain more than one resolved static trait axis.

Therefore 19 axes are not equivalent to 19 independent systems.

## Trait-domain structure

The 19 static resolved axes are distributed as:

```text
MORPHOLOGY                    9
DISPLAY_STATE                 4
CHEMICAL_SIGNAL               3
CHEMICAL_OR_VISUAL_SIGNAL     2
PHENOLOGY                     1
```

Geometry by trait domain:

```text
MORPHOLOGY:
  conflict 5
  reinforcement 2
  one-sided 2

DISPLAY_STATE:
  conflict 2
  one-sided 2

CHEMICAL_SIGNAL:
  one-sided 3

CHEMICAL_OR_VISUAL_SIGNAL:
  conflict 1
  one-sided 1

PHENOLOGY:
  conflict 1
```

These cells are descriptive only. The current distribution is too sparse for a stable uncollapsed trait-domain regression.

## Antagonist-guild structure

Static resolved axes:

```text
SEED_PREDATOR            8
HERBIVORE_GRAZER         5
FLORIVORE                4
MULTIPLE_ANTAGONISTS     1
MULTIPLE_GUILDS          1
```

Geometry by antagonist family:

```text
SEED_PREDATOR:
  conflict 4
  reinforcement 1
  one-sided 3

HERBIVORE_GRAZER:
  conflict 2
  reinforcement 1
  one-sided 2

FLORIVORE:
  conflict 1
  one-sided 3

MULTIPLE_ANTAGONISTS:
  conflict 1

MULTIPLE_GUILDS:
  conflict 1
```

Again, these are pattern descriptions, not inferential moderator effects.

## H1 modelability gate

Before fitting any ecological moderator model, SCH now freezes a conservative project gate:

```text
minimum multinomial class n       5
minimum binary outcome n         10
minimum independent clusters     20
minimum moderator-level n         3
```

These are project safeguards, not universal statistical laws.

Current state:

```text
multinomial geometry model       FAIL
binary conflict model            FAIL
trait-domain moderator           FAIL without collapse
antagonist-guild moderator       FAIL without collapse
```

Reasons:

1. reinforcement contains only two static canonical axes;
2. only thirteen independent biological clusters contribute static resolved axes;
3. six clusters contribute multiple resolved trait axes;
4. trait-domain levels contain cells as small as one;
5. antagonist-guild families contain cells as small as one;
6. fifteen fixed-role canonical axes remain outcome-unresolved;
7. the full frozen 868-record systematic screen is still incomplete.

## What is licensed now

Primary results that are currently licensed:

- canonical geometry counts;
- cluster-aware ecological case synthesis;
- source-level promotion and demotion results;
- role-boundary versus fixed-role distinction;
- explicit context-variable axes;
- prospective exact/Fisher sensitivity analyses only after a biological category collapse is declared in advance.

Not licensed as primary analyses now:

- multinomial regression;
- multivariable logistic regression;
- post-hoc merging of trait or antagonist categories to manufacture power;
- conflict prevalence claims.

## Biological interpretation

The fail-closed model gate does not remove the ecological result.

The canonical dataset already establishes that the same broad pollinator-antagonist setting can resolve as:

```text
opposition
reinforcement
one-sided / null response
context-variable geometry
role switching
benefit-cost coupling
```

The most defensible current statement is:

> **Multifunctional geometry is heterogeneous at the canonical trait-axis level, and the heterogeneity cannot yet be reduced to a stable moderator model without stronger sampling and outcome resolution.**

This preserves the biological discovery while preventing overfitting.

## Next step

The highest-value next operation is H2 context decomposition.

The current canonical ledger already flags axes with source-supported context shifts. Those axes should now be expanded into population/year/treatment/consumer-regime context cases.

That will answer a more data-supported ecological question than forcing H1 regression now:

> **When does the same canonical trait axis switch ecological geometry across contexts?**

## Status

```text
CANONICAL_LEDGER = MATERIALIZED
CANONICAL_TRAIT_AXES = 48
STATIC_RESOLVED_FIXED_ROLE_AXES = 19
STATIC_RESOLVED_FIXED_ROLE_CLUSTERS = 13

H1_MULTINOMIAL_MODEL = FAIL_CLOSED
H1_BINARY_MODEL = FAIL_CLOSED
H1_DESCRIPTIVE_PATTERN = READY

NEXT_PRIMARY_BUILD = H2_CONTEXT_CASES
```
