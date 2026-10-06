from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.adjudicate_pedicularis_p2_geometry_accrual import (
    CONTINUE,
    INSUFFICIENT,
    READY,
    STOP_MAX,
    STOP_READY,
    build as adjudicate,
)
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.build_pedicularis_p2_geometry_pilot import build as allocate
from scripts.materialize_pedicularis_p2_geometry_stage import (
    build as materialize_stage,
)


def _config() -> dict:
    return {
        "schema": "PEDICULARIS_P2_GEOMETRY_PILOT_CONFIG_V1",
        "status": "PEDICULARIS_P2_GEOMETRY_PILOT_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "planned_n_plants": 10,
        "candidate_cumulative_plants": [5, 10],
        "flowers_per_plant": 4,
        "z_levels": [
            {
                "assigned_z_level": f"Z{i}",
                "assigned_z_rank": i,
                "target_exsertion": z,
            }
            for i, z in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0))
        ],
        "excluded_method_code": "FINE_MESH_LOWER_FRUIT_SLEEVE",
        "exposed_method_code": "SHAM_SLEEVE",
        "allocation_strategy": "BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1",
        "frozen_before_geometry_outcomes": True,
        "pilot_role": "POWER_BASIS_ONLY_NEVER_CONFIRMATORY",
        "precision_gate": {
            "bootstrap_reps": 200,
            "random_seed": 31,
            "min_valid_bootstrap_fraction": 0.80,
            "min_interior_concave_fraction_per_state": 0.80,
            "max_normalized_95ci_width_per_power_basis_path": 0.50,
        },
    }


def _binding(config: dict) -> dict:
    return {
        "receipt_schema": "PEDICULARIS_GEOMETRY_INTERVENTION_PLAN_BINDING_V1",
        "status": (
            "PEDICULARIS_GEOMETRY_INTERVENTION_PLAN_"
            "FROZEN_BEFORE_CONFIRMATORY_OUTCOMES"
        ),
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "geometry_config_sha256": _semantic_sha256(config),
        "p0_level_plan_sha256": "1" * 64,
        "p0_field_config_sha256": "2" * 64,
        "p1_field_config_sha256": "3" * 64,
        "g_field_config_sha256": "4" * 64,
        "g_method_selection_sha256": "5" * 64,
        "f0_assembly_receipt_sha256": "6" * 64,
        "z_level_plan": [
            {
                "assigned_z_level": row["assigned_z_level"],
                "assigned_z_rank": str(row["assigned_z_rank"]),
                "sham_control": (
                    "1" if i == len(config["z_levels"]) - 1 else "0"
                ),
            }
            for i, row in enumerate(config["z_levels"])
        ],
        "p1_experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
        "g_selected_candidate_id": "G_TEST",
        "g_exclusion_method": config["excluded_method_code"],
        "g_exposed_sham_method": config["exposed_method_code"],
        "geometry_collection_may_run_before_lane_validation": True,
        "geometry_analysis_requires_later_positive_readiness_v3": True,
    }


def _manifest() -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"GP{plant:02d}",
            "flower_id": f"GP{plant:02d}_F{flower:02d}",
        }
        for plant in range(10)
        for flower in range(4)
    ]


def _summary(config: dict, stage_n: int) -> dict:
    return {
        "pilot_config_sha256": _semantic_sha256(config),
        "current_precision_look_n": stage_n,
        "n_plants": stage_n,
        "candidate_cumulative_plants": list(
            config["candidate_cumulative_plants"]
        ),
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "marker": f"summary-{stage_n}",
    }


def _precision(
    config: dict,
    summary: dict,
    *,
    ready: bool,
) -> dict:
    return {
        "receipt_schema": "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_V1",
        "status": READY if ready else INSUFFICIENT,
        "pilot_config_sha256": _semantic_sha256(config),
        "candidate_cumulative_plants": list(
            config["candidate_cumulative_plants"]
        ),
        "current_precision_look_n": summary["current_precision_look_n"],
        "n_plants": summary["n_plants"],
        "geometry_summary_sha256": _semantic_sha256(summary),
        "basis_materialization_authorized": ready,
    }


def test_maximum_allocation_contains_nested_exact_balanced_prefixes() -> None:
    config = _config()
    rows, receipt = allocate(
        _manifest(),
        config,
        _binding(config),
        "STAGED-SEED",
    )

    assert receipt["candidate_cumulative_plants"] == [5, 10]
    assert receipt["plant_accrual_order"]
    assert receipt["precision_look_designs"] == [
        {
            "cumulative_plants": 5,
            "cumulative_flowers": 20,
            "replicates_per_cell": 1,
        },
        {
            "cumulative_plants": 10,
            "cumulative_flowers": 40,
            "replicates_per_cell": 2,
        },
    ]

    stage5, receipt5 = materialize_stage(rows, receipt, 5)
    stage10, receipt10 = materialize_stage(rows, receipt, 10)

    assert len(stage5) == 20
    assert len(stage10) == 40
    assert receipt5["replicates_per_cell"] == 1
    assert receipt10["replicates_per_cell"] == 2
    assert set(receipt5["cell_counts"].values()) == {1}
    assert set(receipt10["cell_counts"].values()) == {2}
    assert {
        row["flower_id"] for row in stage5
    } <= {
        row["flower_id"] for row in stage10
    }


def test_first_insufficient_look_authorizes_only_next_registered_stage() -> None:
    config = _config()
    summary5 = _summary(config, 5)
    precision5 = _precision(config, summary5, ready=False)

    decision = adjudicate(config, summary5, precision5, [])

    assert decision["decision"] == CONTINUE
    assert decision["next_registered_precision_look_n"] == 10
    assert decision["additional_geometry_collection_authorized"] is True
    assert decision["basis_materialization_authorized"] is False


def test_first_passing_look_stops_and_authorizes_materialization() -> None:
    config = _config()
    summary5 = _summary(config, 5)
    precision5 = _precision(config, summary5, ready=True)

    decision = adjudicate(config, summary5, precision5, [])

    assert decision["decision"] == STOP_READY
    assert decision["next_registered_precision_look_n"] is None
    assert decision["additional_geometry_collection_authorized"] is False
    assert decision["basis_materialization_authorized"] is True


def test_second_look_requires_formal_insufficient_receipt_from_first() -> None:
    config = _config()
    summary10 = _summary(config, 10)
    precision10 = _precision(config, summary10, ready=True)

    with pytest.raises(ValueError, match="every earlier registered look"):
        adjudicate(config, summary10, precision10, [])


def test_cannot_continue_after_an_earlier_precision_pass() -> None:
    config = _config()
    summary5 = _summary(config, 5)
    precision5 = _precision(config, summary5, ready=True)
    summary10 = _summary(config, 10)
    precision10 = _precision(config, summary10, ready=True)

    with pytest.raises(ValueError, match="cannot continue after an earlier"):
        adjudicate(config, summary10, precision10, [precision5])


def test_maximum_registered_look_can_stop_without_basis_if_still_imprecise() -> None:
    config = _config()
    summary5 = _summary(config, 5)
    precision5 = _precision(config, summary5, ready=False)
    summary10 = _summary(config, 10)
    precision10 = _precision(config, summary10, ready=False)

    decision = adjudicate(
        config,
        summary10,
        precision10,
        [precision5],
    )

    assert decision["decision"] == STOP_MAX
    assert decision["maximum_registered_pilot_reached"] is True
    assert decision["basis_materialization_authorized"] is False
    assert decision["additional_geometry_collection_authorized"] is False


def test_unbalanced_precision_look_is_rejected_before_allocation() -> None:
    config = deepcopy(_config())
    config["candidate_cumulative_plants"] = [6, 10]

    with pytest.raises(ValueError, match="every planned precision look"):
        allocate(
            _manifest(),
            config,
            _binding(config),
            "STAGED-SEED",
        )


def test_stage_n_must_be_preregistered() -> None:
    config = _config()
    rows, receipt = allocate(
        _manifest(),
        config,
        _binding(config),
        "STAGED-SEED",
    )

    with pytest.raises(ValueError, match="prospectively frozen cumulative looks"):
        materialize_stage(rows, receipt, 7)
