# SCH macroecology H2 measurement layer V2

## Numeric upgrade

Gymnadenia Appendix A Table A2 has now been inspected directly and its exact treatment-group linear selection gradients are frozen.

This changes the H2 materialization state from:

~~~text
10 total local cases
3 plant-performance cases
~~~

to:

~~~text
18 total local cases
11 plant-performance cases
7 visitor-role behavior cases
~~~

## Plant-performance measurement state

The current eight source-level measurement records span six canonical trait axes.

Source-supported layers:

~~~text
LOCAL_GEOMETRY              3 records
LOCAL_NET_SELECTION         4 records
LOCAL_ANTAGONIST_PRESSURE   1 record
~~~

Materialized layers:

~~~text
LOCAL_GEOMETRY              2 records
LOCAL_NET_SELECTION         3 records
CONTEXT_STRUCTURE_ONLY      3 records
~~~

Materialized plant-performance rows:

~~~text
LOCAL_GEOMETRY               2 cases
LOCAL_NET_SELECTION          9 cases
LOCAL_ANTAGONIST_PRESSURE    0 cases
~~~

The nine local-net-selection cases are:

- Caryopteris robber exclusion: 1;
- Gymnadenia flowering phenology: 4;
- Gymnadenia spur length: 4.

## Gymnadenia treatment-group cases

For each of the two canonical axes, four treatment groups are materialized:

~~~text
C+H
C+E
HP+H
HP+E
~~~

Each row stores:

- pollination state;
- herbivory state;
- treatment-group beta;
- treatment-group SE;
- common female-fitness endpoint;
- source provenance.

They are local net-selection cases, not local two-function geometry cases.

## Agent-mediated directional contrasts

The source table also gives mediated contrast point estimates.

### Flowering start

~~~text
pollinator-mediated:
  +0.16 with herbivory
  +0.16 without herbivory

herbivore-mediated:
  -0.098 under open pollination
  -0.094 under hand pollination
~~~

Directional interpretation:

~~~text
pollinators -> later flowering
herbivores  -> earlier flowering
=> opposing components
~~~

### Spur length

~~~text
pollinator-mediated:
  +0.10 with herbivory
  +0.12 without herbivory

herbivore-mediated:
  +0.10 under open pollination
  +0.13 under hand pollination
~~~

Directional interpretation:

~~~text
pollinators -> longer spur
herbivores  -> longer spur
=> reinforcing components
~~~

Contrast SE/covariance is not reported, so these contrasts remain directional.

## Source-recovery state

Current registered source objects:

~~~text
Gentiana S3               pending binary/local extraction
Gymnadenia A2             exact values extracted
Pedicularis S1/S2/S1 app  pending binary/local extraction
Primula programme         source-specific objects pending
~~~

Exact-local-value source objects extracted:

~~~text
1 / 6
~~~

## H2 modelability consequence

The plant-performance layer now contains:

~~~text
11 cases
4 canonical axes
3 biological clusters
3 axes with >=2 local cases
~~~

The case-count threshold is almost met, but case count is not the limiting factor.

The primary blockers remain independent-axis and independent-cluster coverage.

~~~text
required axes       8
current axes        4

required clusters   8
current clusters    3
~~~

Therefore:

~~~text
H2_MODEL = FAIL_CLOSED
~~~

## Scientific gain

The upgrade is nevertheless substantial.

Before Table A2 extraction, Gymnadenia contributed source-level statements about conflict and reinforcement.

After extraction, SCH now has exact treatment-specific realized selection surfaces showing that the same ecological factorial context produces very different trait-level dynamics.

This strengthens the central ecological statement:

> Context acts through trait-specific geometry; the same pollinator–herbivore environment can generate opposing components for one floral trait and reinforcing components for another.
