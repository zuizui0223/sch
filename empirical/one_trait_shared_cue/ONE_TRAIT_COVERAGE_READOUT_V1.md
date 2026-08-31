# One-trait shared-cue coverage readout v1

## Result

- frozen BITA route-ledger clusters screened: **25**
- clusters with at least one A route: **8**
- clusters with both `A_to_pollination` and `A_to_antagonism`: **5**
- strict one-trait coverage passes: **1**
- original 16-system identification matrix strict passes: **0/16**

The strict pass is **Theis & Adler (2012), directional source evidence only**. The same field experiment manipulated floral fragrance, recorded florivore and pollinator attraction, and reported seed production. The publisher-linked public deposit does not contain the main experiment's raw table, so this audit does not manufacture an uncertainty-bearing effect.

The 0/16 result does not contradict the 1/25 result. The 16-system matrix was assembled around the two-trait identification frontier and does not include Theis & Adler (2012). It is therefore not a complete one-trait source universe.

## Candidate adjudications

| Cluster | A manipulated | pollinator response | antagonist response | common reproductive outcome | result |
|---|---|---|---|---|---|
| `Gorden_Adler_2018_Impatiens_capensis` | no_observational | yes | yes | yes_same_plant_reproductive_components | `FAIL` |
| `Gross_Sun_Schiestl_2016_Gymnadenia_odoratissima` | no_observational | no_current_same_study_route | yes | no_common_reproductive_outcome | `FAIL` |
| `Kessler_et_al_2015_Nicotiana` | yes | yes | yes | no_separate_seed_and_oviposition_assays | `FAIL` |
| `McCall_2013_Raphanus_sativus` | no_reproductive_A_intervention | no_current_same_study_route | yes | no_common_reproductive_outcome | `FAIL` |
| `Page_2014_Silene_signals` | no_recombinant_observational_axes | no_current_same_study_route | yes | no_common_reproductive_outcome | `FAIL` |
| `Perez_Barrales_2013_Dalechampia_scandens` | no_observational | yes | yes | yes_observational_fitness_decomposition | `FAIL` |
| `Theis_Adler_2012_Cucurbita` | yes | yes | yes | yes_seed_production_directional_only | `PASS_DIRECTIONAL_ONLY` |
| `Theis_et_al_2014_Cucurbitaceae` | no_comparative | yes | yes | no_common_reproductive_outcome | `FAIL` |

## Interpretation

The original one-trait hypothesis was not tested by BITA's two-trait estimand. It is nevertheless not evidence-free: the frozen source export contains one directional experiment meeting the predeclared coverage fields, plus several observational or comparative shared-tracking systems.

The one-trait accounting identity is `Delta_A W = Delta_A M - Delta_A G - Delta_A C`. A reduced biotic balance `S_A = Delta_A M - Delta_A G` requires direct attraction cost to be standardized or measured; it must not be assumed away. Total `W(A)` alone still does not allocate the channels.

## Claim ceiling

This result establishes **coverage existence in the committed screened evidence**, not a pooled effect, natural prevalence, causal cue-overlap coefficient, or point identification of pollinator benefit and antagonist cost. Kessler et al. (2015) remains a strong experimental shared-tracking example but fails the strict common-outcome field because pollinator-mediated seed production and oviposition come from different assay structures. Sasidharan et al. (2023) remains a cross-study assembled response synthesis and is not a same-experiment coverage pass.

## Next gate for a companion paper

Before meta-analysis, expand the audit beyond the A/D-oriented 25-cluster universe with the same four fields and preserve `FAIL`, `NOT_EVALUABLE`, and source-access limits. If enough linked experiments remain, define route-compatible effect-size lanes. If not, report the paired-channel measurement gap rather than weakening the gate.
