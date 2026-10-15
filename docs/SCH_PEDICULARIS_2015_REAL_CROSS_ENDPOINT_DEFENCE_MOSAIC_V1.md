# Real 2015 Pedicularis rex defence-response mosaic across three reproductive endpoints

## Evidence-based ecological result

**Question:** Does a defence intervention that affects seed predation differently among plant populations necessarily show correspondingly heterogeneous effects on final seed production?

**Sun & Huang 2015**, AoB PLANTS, doi:10.1093/aobpla/plv019, Table 2, provides a field-experimental signature that makes this a biological question. The treatment was **hole-puncturing the base of water-retaining cupulate bracts PLUS drainage** before anthesis; intact bracts served as controls. This is a single six-population experiment, **not** six independent studies or a clean water-only manipulation.

### Three responses show different treatment-by-population detection

The source analyzes initial seed set, final surviving seed set and predation under site, bract treatment and their interaction.

| Endpoint | Treatment chi-square (df=1) | Treatment P | Site x treatment chi-square (df=5) | Interaction P |
|---|---:|---:|---:|---:|
| Initial seed set | 0.014 | 0.906 | 1.032 | 0.960 |
| Final undamaged seed set | 16.710 | <0.0001 | 4.913 | 0.4265 |
| Seed predation | 92.808 | <0.0001 | 36.782 | <0.0001 |

Predation response to the combined treatment varied detectably across populations; the original article found increased predation after treatment in five of six sites. Final undamaged seed set changed when analyzed across sites, but a site x treatment interaction was **not statistically detected**. Initial seed set showed neither a detected treatment effect nor treatment interaction.

This is a real published **cross-endpoint statistical pattern**, not new raw measurements or a meta-analysis.

### Three distinct biological explanations remain viable

1. **Different baseline seed initiation:** the same proportional damage change need not yield the same intact-seed change if initial seed production differs by patch.
2. **Coupled seed development and damage:** at a capsule with identifiable developed seeds and ovules, F=I(1-q), where I=(intact+damaged)/ovules, q=damaged/(intact+damaged), and F=intact/ovules. Across fruits, E(F)=E(I)[1-E(q)]-Cov(I,q). Covariance may change by site, but the paper's Table 2 does **not** contain this source-matched covariance. Undefined q and unrecognizable consumed seed fates cannot be silently omitted.
3. **Different GLM precision, link or sample hierarchy:** nonsignificance for final seed set could reflect lower sensitivity or a different response scale even if final-fitness effects are heterogeneous.

**No specific explanation is identified by comparing the separate P values.** The difference between two significance outcomes is not a formal test of the difference between endpoint-specific interaction effects. A nonsignificant final-seed interaction is not geographic equivalence or evidence of fitness buffering.

### Relation to SCH

The cross-endpoint signature supports a concrete question: **when does spatial variation in antagonist attack translate into variation in final reproductive fitness, and when does it not?** The source does not estimate exsertion-conditioned attack preference, since no trait z grid or water-fixed seed-predator exclusion G was randomized. The 2016 observational exsertion study (10.1093/aob/mcw097) and the 2013 11-patch density study (10.1098/rsbl.2013.0387) are distinct studies and cannot be pooled into a fictitious crossed z x P x G surface.

The relevant prospective field measurements are independent patch IDs, plant-level G assignment, realized z, seed initiation, seed damage, viable mature seed output, stage and verified fully destroyed or unknown fruit fate. A valid selective intervention and unconfounded timing must be validated before causal component interpretation.

**Licensed claim:** A source-report-supported site-specific **predation response** to puncture-plus-drainage contrasts with a detected pooled final viable-seed treatment response but no detected **site-by-treatment interaction** for final seed production.

**Not licensed:** identical fitness response across sites, experimentally demonstrated compensation, water-only causality, phenotypic optimum shift, SCH L or SLK architecture value.

## Source and reproducibility

Primary article: https://academic.oup.com/aobpla/article/doi/10.1093/aobpla/plv019/200213, Table 2.

Files:

- data/PEDICULARIS_2015_CROSS_ENDPOINT_TABLE2_V1.csv: nine frozen source GLM tests.
- scripts/audit_pedicularis_2015_cross_endpoint.py: chi-square tail reconstruction and claim ceiling.
- tests/test_pedicularis_2015_cross_endpoint.py: source-identical regression checks.

Run from the repository root:

    python scripts/audit_pedicularis_2015_cross_endpoint.py

No plant data were retrieved, and no site-specific final-fitness effects, covariance, endpoint-difference test or cluster-robust estimates can be reconstructed from the printed table. The Shama-only pollinator-visitation test (treatment P=0.958) cannot establish equivalence across six sites. The raw 2013 Dryad workbook is still unavailable in this environment and is not used.
