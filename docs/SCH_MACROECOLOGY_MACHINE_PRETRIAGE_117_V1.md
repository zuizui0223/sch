# SCH macroecology machine pretriage — current 117 primary studies

## Purpose

The current SCH systematic evidence state contains 117 full-text primary-study inclusions. Before continuing manual ecological coding, the existing structured design fields were used to build a **sign-blind machine pretriage**.

The pretriage does not read `selection_form`, claim language, or ecological outcome sign. It only asks which measurement architecture is already present.

## Current design funnel

```text
current primary-study inclusions                    117

both pollinator + antagonist responses measured     62
  + common reproductive outcome                     47
  - common reproductive outcome                     15

pollinator response only                            29
antagonist response only                            15
neither / structured route unresolved               11
```

A separate context flag identifies 33 records that already contain a multisite, geographic, receiver-assemblage, or equivalent repeated-context signal.

## What the 47-record P1 set means

`P1_BOTH_RESPONSES_COMMON_FITNESS` is **not** equivalent to SCH conflict eligibility.

A P1 record can still fail H1 because:

- the two responses refer to different trait coordinates;
- the focal `A` is an induced or upstream ecological state rather than the trait read by both functions;
- several floral traits are bundled and must be split into trait axes;
- the same consumer switches between mutualistic and exploitative roles;
- pollination benefit and exploitation cost are intrinsically coupled in one consumer life cycle;
- the common reproductive outcome is too coarse to recover the relevant component geometry.

P1 therefore means only: **high-value source-recode priority**.

## Why this is useful

The manual recode no longer needs to inspect all 117 records with equal depth.

Priority is now:

```text
P1  both responses + common fitness         47
P2  both responses, common fitness missing  15
P3  one focal response only                 44
P4  neither / unresolved                    11
```

The 47 P1 records are the first source-audit queue for H1 trait-axis eligibility.

The 15 P2 records are especially valuable for H4 because they demonstrate a recurrent design pattern in which shared receiver biology is measured but the plant-fitness geometry remains unidentified.

P3/P4 remain part of H4 and are not discarded.

## Context queue

Thirty-three current primary records already have a source-coded repeated-context signal.

These records are prioritized for:

- population/site decomposition;
- year/season decomposition;
- treatment/consumer-regime decomposition;
- receiver-assemblage contrasts;
- later H2 context-switch analysis.

A repeated-context flag does not imply that a trait-axis geometry is identifiable.

## Trait manipulation structure

Current structured fields report:

```text
direct trait manipulation reported          26
non-direct / observational trait state      82
not reported                                 9
```

This provides a second H4 design axis. However, manipulation status alone does not determine evidence quality: observational studies can identify strong selection geometry, while a manipulated upstream herbivory state can still fail the same-coordinate conflict gate.

## Relationship to the first 44 manual recodes

The first 44 source-verified records have already been manually recoded without outcome sign.

That manual set yielded:

```text
H1 geometry eligible  12
H2 context eligible    8
```

The machine-pretriage result explains why manual eligibility is narrower than the simple P1 count: measurement architecture is necessary but not sufficient.

The remaining workflow is therefore:

```text
117 primary includes
-> machine design pretriage
-> P1/P2/P3/P4 review order
-> source-level trait-axis eligibility
-> cluster/program dependence
-> context-case decomposition
-> ecological outcome coding
-> registered H1-H4 analyses
```

## Claim ceiling

```text
MACHINE_PRETRIAGE = COMPLETE_FOR_CURRENT_117
PAIRED_RESPONSE_RECORDS = 62
PAIRED_PLUS_COMMON_FITNESS = 47
CONTEXT_PRIORITY_RECORDS = 33

H1_GEOMETRY_ELIGIBILITY = NOT_INFERRED_BY_MACHINE
CONFLICT_PREVALENCE = NOT_ESTIMATED
H1_H2_H3_MODELS = NOT_FIT
FINAL_H4_FREQUENCIES = NOT_ESTIMATED
```
