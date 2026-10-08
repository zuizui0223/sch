# Interaction intensity does not identify trait-specific selection

## Two real studies; different estimands

**Sletvold & Ågren (2014), Evolution 68:1907–1918,
DOI 10.1111/evo.12405.** This study manipulated supplemental
hand pollination over multiple seasons at two populations each
of *Gymnadenia conopsea* and *Dactylorhiza lapponica*.

Published, qualitative results:

- *Gymnadenia*, **nine population-year units** across two populations:
  population-year pollen limitation (PL) predicted the *magnitude of
  net selection* in open-pollinated plants, but its association with
  pollinator-mediated selection was not detected. Pollinator-mediated
  selection was stronger for **spur length** (pollen-transfer efficiency)
  than for display/attraction traits; original Tukey P was below 0.01.
- *Dactylorhiza*, **five population-year units** across two populations:
  no significant within-species association of PL with either selection
  response was detected. The range of PL was limited.
- **Critical negative:** the multiyear *Gymnadenia* analysis excluded
  **flowering start**, owing to inconsistent data quality. It is not an
  independent multiyear replication of the 2015 flowering-time reversal.

The 2014 authors defined mean PL as one minus open-pollinated female
fitness divided by supplemented female fitness, with plant female fitness
measured by number of fruits × average fruit mass. The study estimated
selection gradients for naturally varying traits using within-treatment
and population standardized trait/relative-fitness variables.

The underlying Excel source is listed at
https://doi.org/10.5061/dryad.30dn3
(filename: Dryad MS 13-0868_R1.xlsx). **The binary was not retrieved
in the current session.** No raw-data refits, correlation coefficients
or new source p-values are claimed.

**Sletvold, Moritz & Ågren (2015), Ecology,
DOI 10.1890/14-0119.1.** The independent single-population
pollination × herbivory factorial experiment provides quantitative
point contrasts from its original Appendix A Table A2.

| Focal trait | Pollination contrast, herbivory intact | Pollination contrast, herbivores excluded | Herbivory contrast, open pollination | Herbivory contrast, hand-supplemented |
|---|---:|---:|---:|---:|
| Flowering start | +0.1558 | +0.160 | −0.0982 | −0.094 |
| Spur length | +0.097 | +0.119 | +0.103 | +0.125 |

These are **source-table point differences between treatment-specific
phenotypic selection gradients**, not coefficients from individual-plant
data or new measurements. They illustrate why the same pollination and
herbivory experiment can produce **conflicting selection on flowering
start** and **reinforcing selection on spur length**.

No claim is made that the two studies used exactly the same population-year
sample frame; their effect estimates are **not pooled**.

## A direct third route: pollinator guild affects selection differently from mean seed service

**Sletvold et al. (2012), Ecology 93:1880–1891,
DOI 10.1890/11-2044.1**, selectively excluded diurnal or nocturnal
pollinators from *Gymnadenia* in **two central-Norway populations**.
The original abstract states:

- Excluding **diurnal** pollinators significantly lowered seed
  production compared with open-pollinated plants **in both populations**.
- Excluding **nocturnal** pollinators did **not** show the same
  significant reduction in mean seed production.
- Nevertheless **both diurnal and nocturnal pollination regimes**
  showed selection on traits related to attraction and pollen-transfer
  efficiency. Selection strengths varied among traits and populations,
  but **directions were consistent** in that source.

Thus the pollinator category with the strongest measured contribution
to **mean seed production** was *not* the only category participating
in **trait selection**. Importantly, a nonsignificant nocturnal-removal
effect is **not evidence that nocturnal pollinators provide zero
seed production**.

A different experimental programme, **Sletvold et al. (2015),
New Phytologist, DOI 10.1111/nph.13555**, studied four populations,
with diurnal/nocturnal comparisons in **two**. It reports that
**only nocturnal pollinators selected longer spurs in the focal
guild-comparison subset**, and that the two guilds mediated
correlational selection on **different combinations of floral
traits**. This is source-level evidence for consumer-specific
multitrait selection geometry. It is **not** evidence of an
evolutionary sign reversal between 2012 and 2015: different
study frames, interventions and fitness analyses must be
kept separate.

Taken with the 2014 mean-pollen-limitation nonprediction, these
field experiments establish the biological importance of
**pollinator identity and trait-specific selective response**
rather than treating mean service or shortage as the entire
functional landscape. They do not reveal exact night/day
response-curve slopes or pure-function optima. Original abstract
results and tested scope are recorded in
data/SCH_GYMNADENIA_GUILD_SERVICE_VS_SELECTION_V1.csv.

## Three mechanisms that SCH must distinguish

1. **Interaction intensity:** mean pollen limitation, mean attack rate,
   or average antagonist pressure in a population.
2. **Trait-conditioned response:** how changing a specified floral
   coordinate changes *pollination quality / pollen receipt* or *predator
   oviposition* at a given background interaction regime.
3. **Fitness translation:** how pollen reception and attack jointly
   become initiated seeds, intact mature seeds and lifetime reproduction,
   potentially with resource limitation and within-fruit covariance.

Mean PL is not a direct estimate of the trait-conditioned
pollen-delivery gradient. Likewise, mean seed-predation incidence
does not identify how attack changes with assigned exsertion.

The 2014 original cross-population/year evidence undermines using
mean PL alone as a sufficient ecological selection predictor.
The 2015 source shows that **trait identity**, even within the same
experimental setting, changes whether component directions are
opposed or reinforcing.

It is still a hypothesis that variation in *measured functional
response curves*, rather than guild composition or resource
effects, caused the unexplained 2014 variation. A decisive future
study would hold PL and flower stage approximately matched while
randomizing the floral coordinate and measuring visitor-verified
pollen transfer, early attack and mature fitness.

### Why even both mean functional curves may be insufficient

The stage-coupling theorem in
SCH_STAGE_COUPLING_SELECTION_SIGN_IDENTIFICATION_V1.md
separates the trait-conditioned stage margins from their
within-fruit pairing. Holding both complete marginal
distributions fixed can still reverse the final fitness
ranking when the seed predator targets different
developing fruits. That is a synthetic mathematical
counterexample, **not** evidence that the orchid
selection gradients were caused by such coupling.

## Limits and explicit negative controls

- **Different significance decisions are not themselves a formal
  statistical difference.** A PL slope detected for net selection
  but not for mediated selection does **not** mean those two
  PL slopes have been tested against each other. Equally,
  significant mean seed loss after diurnal exclusion and a
  nonsignificant loss after nocturnal exclusion do **not**
  alone establish a significant daytime-versus-nighttime
  treatment contrast.
- The 2014 source's nonsignificant within-species PL result is **not
  evidence of exactly zero PL effect** or proof that response gradients
  explain all residual variation.
- The nine/five population-year records are nested in only two
  populations each, not fourteen independent populations.
- The multiyear *Gymnadenia* source **did not test flowering start**.
- The separate 2015 source tests experimentally changed consumer
  conditions, not physically randomized floral phenotypes.
- Source treatment-specific standardized regression gradients are
  not automatically additive physiological payoff components.
- Neither study identifies pure function optima, SCH L, SLK R/K/Phi,
  or a completed randomized *Pedicularis rex* P×G experiment.

## Implementation

Source-coded, source-limited evidence is in:

- data/SCH_GYMNADENIA_INTERACTION_INTENSITY_FUNCTIONAL_RESPONSE_2014_V1.csv
- scripts/audit_sch_orchid_intensity_vs_trait_function.py
- tests/test_sch_orchid_intensity_vs_trait_function.py

The audit fails closed on invented temporal replication, changed
source observations, or false claims of spreadsheet ingestion.
