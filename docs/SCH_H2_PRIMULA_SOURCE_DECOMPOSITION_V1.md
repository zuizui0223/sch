# SCH H2 Primula farinosa source decomposition V1

## Purpose

The *Primula farinosa* H2 programme had previously been represented by one umbrella source object:

`Primula_program_sources`

That representation mixed surveys, causal manipulations and evolutionary follow-up with different context denominators.

The programme is now decomposed into five source objects from the already-included primary study SCHPRISMA-000523 (Ågren et al. 2013, PNAS).

No auxiliary older paper is added to the current macroecology denominator.

## Canonical axis

`Primula_farinosa_000523_scape`

Trait:

`scape-height morph`

Static canonical geometry:

`CONFLICT`

Biological basis:

- pollinator-mediated selection favors the long-scaped morph;
- grazer-mediated selection favors the short-scaped morph;
- the relative strength of those components varies among populations.

## Object 1 — population selection mosaic

`Primula_PNAS2013_Fig2_TableS2`

Source design:

~~~text
2000: 37 population-year contexts
2001: 46 population-year contexts
~~~

Local quantity:

`relative fitness of short versus long scape morph`

Measurement target:

`LOCAL_NET_SELECTION`

The primary text establishes:

~~~text
2000:
  short > long significantly in 14 / 37 populations

2001:
  short > long significantly in 18 / 46 populations
  long  > short significantly in 2 populations
~~~

Exact population-year relative-fitness values remain in Fig. 2 / Table S2 and are not materialized in SCH.

Therefore:

~~~text
83 reported population-year contexts
!=
83 current model cases
~~~

## Object 2 — five-population time series

`Primula_PNAS2013_Fig3_5pop`

Source design:

~~~text
5 populations
x 5 sampled years
= 25 population-year contexts
~~~

Population IDs shown in Fig. 3:

~~~text
13
46
59
81
84
~~~

The mean relative fitness of the short morph across the five-year interval was positive in all five populations, with a source-reported range of 0.047–0.485.

However, selection direction changed among years in four of the five populations.

This is strong source-level H2 evidence for temporal net-selection change.

The 25 local values remain figure-only in current recovery and therefore are not model rows.

## Object 3 — four-population causal factorial

`Primula_PNAS2013_Fig4_factorial`

Source design:

~~~text
4 populations
x
4 treatment states

control
grazer exclusion
supplemental hand pollination
grazer exclusion + hand pollination

= 16 population × treatment contexts
~~~

The primary source reports that control relative fitness of the short morph ranged from:

~~~text
-0.580
to
+1.679
~~~

across the four populations.

Causal treatment results:

~~~text
grazer exclusion
-> reduced relative fitness of the short morph
F(1,9) = 9.5
P = 0.01

supplemental hand pollination
-> increased relative fitness of the short morph
F(1,9) = 5.7
P = 0.04

grazer × pollination interaction
F(1,9) = 0.6
P = 0.46
~~~

With both herbivory and pollen limitation experimentally reduced, no significant selection on scape morph remained.

This is a source-identified causal component-weight mechanism.

The 16 population × treatment point estimates and bootstrap intervals remain figure-only and are not currently materialized as exact local cases.

## Object 4 — nine-population evolutionary response

`Primula_PNAS2013_Fig5_evolution`

Source design:

~~~text
9 populations
x
2 grazer treatments
x
2 time points

2004
2012
~~~

This object measures evolutionary response, not current selection geometry.

Source-level aggregate result:

~~~text
grazer exclosures:
  short morph frequency 0.48 -> 0.36
  P = 0.013

adjacent controls:
  short morph frequency 0.50 -> 0.48
  P = 0.891
~~~

The population-specific points remain Fig. 5 values.

This object is therefore registered as:

`LOCAL_EVOLUTIONARY_RESPONSE`

and remains outside the current plant-performance geometry model.

## Object 5 — PNAS Supporting Information

`Primula_PNAS2013_SI`

Resolved file:

`1301421110_pnas.201301421SI.pdf`

PMC reports a 540.9 KB supporting-information PDF.

The main article explicitly delegates population-selection details to Table S2 and other supporting analyses to the SI.

The binary PDF is not materialized in the current runtime, so exact local values are not reconstructed from figures.

## Exact programme-level quantities frozen

The repository now freezes source-level quantities that are directly reported in the main article, including:

- morph frequency across 69 populations;
- 37 and 46 population-year selection samples in 2000/2001;
- differential grazing damage by morph;
- regressions of relative fitness on grazing intensity;
- the four-population causal factorial summary;
- 24-population morph-frequency trends;
- the five-population fitness/evolution correlation;
- the nine-population exclosure evolutionary response.

See:

- `data/SCH_H2_PRIMULA_MAIN_TEXT_SUMMARY_V1.csv`

## Why no local cases are added yet

The modelability bottleneck is independent fixed-role breadth, but that does not justify approximate digitization.

Current rule:

~~~text
source design resolved
+
local values figure-only
=
context structure / source evidence

not
=
exact local model cases
~~~

The highest-value next extraction is therefore:

1. Table S2 / Fig. 2 exact population-year relative fitness;
2. Fig. 4 exact four-population × four-treatment relative fitness;
3. Fig. 5 exact population-specific 2004/2012 morph frequencies.

## Programme boundary

Earlier Primula papers provide important biological context, including Oikos 2002, New Phytologist 2006 and Ecology 2008.

They are not silently introduced as new records into the current 117-study macro denominator.

If used, they must be declared as auxiliary programme provenance or admitted through a prospectively defined systematic expansion.

## Status

~~~text
PRIMULA_PROGRAMME_SOURCE_OBJECTS = 5
EXACT_MAIN_TEXT_SUMMARY_METRICS = 18
EXACT_LOCAL_CASES_ADDED = 0

PNAS_SI_FILE_ID = RESOLVED
PNAS_SI_BINARY = NOT MATERIALIZED

PRIMULA_H2_PROMOTION = FAIL_CLOSED_PENDING_EXACT_LOCAL_VALUES
~~~
