# SCH H2 directional-state protocol V1

## Purpose

This protocol defines a possible scale-free H2 outcome before adding further independent systems.

It is not yet an analysis result.

## Eligible evidence

A context row may enter the directional-state layer only when:

1. its measurement layer is LOCAL_NET_SELECTION;
2. the local effect has a declared sign;
3. the source supplies a significance / uncertainty interpretation sufficient to determine whether a direction is supported;
4. the trait axis and ecological context are already frozen independently of the result.

Rows from LOCAL_GEOMETRY, LOCAL_ANTAGONIST_PRESSURE, or visitor-role behavior are excluded.

## State mapping

~~~text
SUPPORTED_POSITIVE
  estimate > 0
  and source supports a positive directional effect

SUPPORTED_NEGATIVE
  estimate < 0
  and source supports a negative directional effect

NO_SUPPORTED_DIRECTION
  source explicitly reports no supported directional effect

UNCLASSIFIED
  required uncertainty / significance state is unavailable
~~~

A nonsignificant estimate is coded NO_SUPPORTED_DIRECTION, not zero.

## Axis-level context-change classes

For a canonical axis with at least two eligible contexts:

~~~text
STABLE_POSITIVE
STABLE_NEGATIVE
SUPPORTED_SIGN_SWITCH
HOTSPOT_COLDSPOT
NO_SUPPORTED_DIRECTION_ACROSS_CONTEXTS
MIXED_UNCLASSIFIED
~~~

Definitions are based on context states, not the magnitude of the original coefficients.

## Independence

Context rows are nested:

~~~text
context
-> canonical trait axis
-> biological cluster
~~~

Multiple traits from one biological cluster do not become independent systems.

## Promotion gate

No primary directional-state regression is fit until:

~~~text
>= 8 independent biological clusters
>= 8 eligible canonical axes
>= 5 axes with >=2 eligible contexts
~~~

and all admitted rows have been coded under this frozen protocol.

## Claim ceiling

A directional-state model would estimate recurrence or context dependence of supported direction states.

It would not estimate a common effect-size magnitude, natural prevalence of conflict, pure functional optima, or local two-function geometry unless separately identified.
