# SCH H2 holdout V26 methods-only design freeze

## Purpose

V25 closed the still-unscreened TA0 title/abstract tier. V26 begins prospective programme admission without extracting selection direction, significance or reversal outcomes.

Only source design information is used here.

## Registered pending programmes

~~~text
SCHPRISMA-000649  Dactylorhiza lapponica
  class = SINGLE_REGISTERED_MODIFIER
  design = supplemental hand-pollination vs open control

SCHPRISMA-000651  Primula alpicola
  class = SINGLE_REGISTERED_MODIFIER
  design = supplemental hand-pollination vs open control
  seed-predator damage = observed, not manipulated

SCHPRISMA-000661  Trillium discolor
  class = SINGLE_REGISTERED_MODIFIER
  design = pollen supplementation vs open pollination across years
  antagonist damage = observed at natural levels

SCHPRISMA-000723  Impatiens capensis
  class = MULTI_COMPONENT_OR_CONSUMER_TURNOVER
  design = ambient / reduced pollinator access /
           reduced pollinator access + increased herbivory
~~~

## Classification firewall

Each class is frozen from METHODS-only fields.

~~~text
classification evidence scope                  METHODS_ONLY
selection sign used for classification        NO
selection significance used for classification NO
numeric beta extracted at V26                  NO
supported reversal adjudicated at V26          NO
~~~

The methods-only design freeze is committed before the registry update. That commit SHA is stored as `first_qualified_commit` for all four programmes.

## Holdout state after V26

~~~text
registered held-out programmes           4
  SINGLE_REGISTERED_MODIFIER             3
  MULTI_COMPONENT_OR_CONSUMER_TURNOVER   1

complete outcome-adjudicated programmes  0
eligible-axis counts extracted           0
supported-reversal counts extracted      0

primary opening gate                 CLOSED
primary test                       NOT RUN
~~~

These four registrations therefore add design breadth only. They do not contribute any result to H2M1 yet.

## Next step

Recover source tables / uncertainty objects for these programmes and adjudicate eligible repeated TOTAL_SELECTION_EFFECT axes. The already frozen context classes cannot be changed in response to the observed coefficient signs.

STATUS = FIRST_FOUR_HELDOUT_PROGRAMMES_REGISTERED_PENDING_OUTCOME
