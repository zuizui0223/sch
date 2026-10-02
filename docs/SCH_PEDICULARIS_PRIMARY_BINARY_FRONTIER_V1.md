# SCH Pedicularis primary-binary retrieval frontier v1

## Purpose

The literature search has reached a point where additional broad screening is
less informative than either retrieving a small number of already identified
primary files or collecting the focal calibration package.

This contract freezes that frontier.

Machine ledger:

```text
empirical/architecture/PEDICULARIS_PRIMARY_BINARY_RETRIEVAL_FRONTIER_V1.csv
```

Audit:

```bash
python scripts/audit_pedicularis_primary_binary_frontier.py
```

## Five remaining primary assets

### 1. Jing et al. 2013 primary Methods

Potential direct-gap value: **HIGH / P1**.

The primary abstract already states that reproductive outputs were measured
under hand and natural pollination, but the hand treatment is not identified
well enough to decide whether it is registered open supplementation or a
different breeding-system assay.

Promotion requires primary Methods showing the actual treatment, unit of
manipulation, sample size and outcome. A bagged self/cross assay does not
become P1 merely because it is called hand pollination.

### 2. Tang 2011 PhD thesis

Potential direct-gap value: **MEDIUM-LOW / G after abstract audit**.

The full English abstract is now recovered. It reports quantitative pollinator
observation in 11 plots, predator behavior/preference and phenotypic-selection
analyses. It does **not** describe a predator-access/exclusion manipulation.

Later focal papers cite the thesis for low autogamy without pollinators and for
seed-predator identity/oviposition timing. The thesis therefore already
strengthens G natural history, but its direct-G value now depends entirely on
whether the unretrieved full Methods/Tables contain an additional P. rex
predator-access manipulation that was not summarized in the abstract.

Only such an explicit focal manipulation could change the G frontier.

### 3. Wang 1998 PDF

Potential direct-gap value: **MEDIUM / P1**.

The JIPB/Acta Botanica Sinica site lists a 611-KB PDF. Searchable text
establishes bumblebee dependence, but not a quantitative supplemental-pollen
contrast.

The PDF can change P1 status only if its Methods/Tables contain a qualifying
hand-supplemented/open contrast.

### 4. Xia et al. 2013 Dryad workbook

Direct-gap value: **LOW; variance value HIGH**.

Dryad publicly lists `raw data.xlsx`. The study design is observational, so
recovering the workbook can improve seed-set/predation distributions and CAL-C
external scenarios but cannot create randomized independent G.

### 5. Sun et al. 2016 supplements

Direct-gap value: **LOW; aggregate-prior value MODERATE**.

The DOC/XLS files can sharpen population means/SE and trait/seed-outcome
priors. They cannot create missing P1/G interventions because the study design
is already known to be observational.

## Concrete retrieval attempts — 2026-10-02

Machine receipt:

```text
empirical/architecture/PEDICULARIS_PRIMARY_BINARY_RETRIEVAL_ATTEMPTS_V1.csv
scripts/audit_pedicularis_primary_binary_retrieval_attempts.py
```

The current attempt state is:

```text
Jing 2013
  Springer content-PDF route       not accessible in current web tool
  ResearchGate author full text    listed; direct binary unavailable/404
  Semantic Scholar route           record blocked; no indexed public PDF
  P1 state                         UNRESOLVED

Tang 2011
  Globethesis host                 indexed but suspended
  full English abstract            RECOVERED
  abstract design                  11-plot visitation + predator behavior/preference + selection
  citing-paper role audit          low autogamy + predator identity/timing
  independent-G manipulation       NOT DESCRIBED IN ABSTRACT OR CITING PASSAGES
  G state                          UNRESOLVED; direct-G expectation reduced

Wang 1998
  JIPB PDF                         listed as 611 KB
  JIPB route                       403 in current web tool
  legitimate archival mirror       not recovered
  P1 state                         UNRESOLVED

Xia 2013 Dryad
  public dataset                   VERIFIED
  file                             raw data.xlsx, 89.60 KB
  legacy file-stream ID            46101
  anonymous file_stream            HTTP 403
  current /api/v2 file download    Bearer-authenticated endpoint
  DataONE dataset metadata mirror  VERIFIED; file object not recovered
  direct G state                   unchanged by design

Sun 2016 supplements
  DOC/XLS identities + sizes       VERIFIED
  binary                           not retrieved
  direct P1/G state                unchanged by design
```

The Dryad result is particularly important: the file is not missing. The
public landing page and file identity are resolved, but the current API file
download route is authenticated. Repeating anonymous file-stream/API attempts
therefore has no information value.

Tang 2011 remains a legitimate primary-binary target, but its observed citation
role is now narrower than the binary frontier alone implied. Later focal
primary papers cite it for very low self-pollination without pollinators and
for seed-predator identity/oviposition timing. That strengthens G natural
history but does not itself evidence a predator-exclusion manipulation.

## Search stop rule

While none of the three direct-gap candidate binaries is retrieved:

```text
general literature expansion      STOP
additional congeneric screening   STOP
field calibration                 PRIMARY PATH
```

The only literature actions still allowed by default are legitimate retrieval
attempts for the five named primary assets.

If Jing/Tang/Wang full primary text is retrieved, audit **that file only**
against its promotion condition before changing any P1/G state.

If Dryad or the 2016 supplements are retrieved, update only external-prior
analyses; field calibration remains the primary path.

## Current status

```text
LITERATURE_EXPANSION_STOPPED_PENDING_PRIMARY_BINARY_OR_FIELD_DATA
```

## Why this matters

This prevents two failure modes:

1. endlessly adding increasingly remote congeners after the relevant method
   families are already demonstrated;
2. mistaking more observational precision for the missing causal intervention.

## Claim ceiling

Failure to retrieve a file is not proof that it does not exist.

The stop rule is a resource-allocation rule: it says that, given the current
indexed evidence, new broad screening has lower information value than focal
field calibration unless one of the named primary binaries becomes available.
