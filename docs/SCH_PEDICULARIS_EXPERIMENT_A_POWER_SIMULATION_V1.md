# SCH Pedicularis Experiment-A power simulation v1

## Purpose

Choose the replication for the Chapter-1 `Pedicularis rex` causal surface by simulating the **production analysis pipeline itself**.

The design being powered is:

```text
>=5 exsertion z levels
x 2 pollination-weight states
x 2 independent seed-predator G states
= >=20 cells
```

Water-defence y is held fixed during Experiment A.

## Why no fixed n is registered yet

The primary estimands are nonlinear optima and a fitness-scale conflict budget, estimated with plant-cluster bootstraps. Power depends on the pilot-estimated surface curvature, plant variance, residual variance, realized manipulation spread and manipulation-failure rates. A generic t-test n would not power the registered decision gates.

## Simulation pipeline

For each candidate number of independent plant clusters per cell:

1. generate a complete-block synthetic `Pedicularis` dataset from prospectively frozen pilot parameters;
2. run `scripts/analyze_pedicularis_full_surface_v2.py` unchanged;
3. require the registered causal-compromise surface status;
4. run `scripts/estimate_sch_conflict_budget.py` unchanged;
5. require the lower 95% bound of the component conflict budget to exceed zero;
6. repeat and report joint gate power.

The current v1 generator is a **balanced complete-block planning model**: every independent plant contributes one focal flower to every treatment cell. If the final field design uses an incomplete block, the generator must be extended before using its n recommendation.

## Generating model

The template freezes, before simulation:

- z levels;
- pollination-facing optimum and curvature;
- antagonist-facing optimum and curvature;
- baseline fitness;
- between-plant and residual variation;
- water-depth variation while y is held fixed;
- mechanical-damage rate;
- predator-attack rate under exposed and excluded G states.

Values must come from pilot/method data or explicitly declared sensitivity scenarios. Do not tune them to obtain a preferred n.

## Conflict-budget note

The simulation knows the generating component optima. It therefore supplies those true component optima only to satisfy the production conflict-budget estimator's context-stability prerequisite. This estimates power **conditional on the registered component-stability interpretation**; it does not estimate the power of a separate empirical assay for pure-function optima.

## Output

For each candidate n:

```text
surface_gate_power
positive_conflict_budget_power
joint_primary_gate_power
analysis_failure_fraction
```

`minimum_candidate_meeting_target` is reported only after `target_joint_power` and all generating/decision parameters are frozen.

## Claim ceiling

Power output is a planning result, not biological evidence. The actual Experiment A still must pass manipulation checks, causal-surface gates and the conflict-budget receipt in field data.
