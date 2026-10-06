from __future__ import annotations

from copy import deepcopy

import pytest

from scripts import audit_pedicularis_w1_w2_power_basis as basis
from scripts.build_pedicularis_p2_geometry_pilot import build as allocate
from scripts.evaluate_pedicularis_p2_geometry_precision import (
    READY_STATUS as PRECISION_READY_STATUS,
    build as evaluate_precision,
)
from scripts.materialize_pedicularis_w1_w2_basis_from_geometry_pilot import (
    materialize,
)
from scripts.summarize_pedicularis_p2_geometry_pilot import (
    READY_STATUS,
    build as summarize,
)


def _config(
    *,
    n_plants: int = 10,
    flowers_per_plant: int = 4,
    max_width: float = 0.5,
) -> dict:
    return {
        "schema": "PEDICULARIS_P2_GEOMETRY_PILOT_CONFIG_V1",
        "status": "PEDICULARIS_P2_GEOMETRY_PILOT_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "planned_n_plants": n_plants,
        "flowers_per_plant": flowers_per_plant,
        "z_levels": [
            {
                "assigned_z_level": f"Z{i}",
                "assigned_z_rank": i,
                "target_exsertion": value,
            }
            for i, value in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0))
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
            "max_normalized_95ci_width_per_power_basis_path": max_width,
        },
    }


def _manifest(
    *,
    n_plants: int = 10,
    flowers_per_plant: int = 4,
) -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"GP{plant:02d}",
            "flower_id": f"GP{plant:02d}_F{flower:02d}",
        }
        for plant in range(n_plants)
        for flower in range(flowers_per_plant)
    ]


def _registry(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "record_id": f"R{i:03d}",
            "population_id": row["population_id"],
            "season_id": row["season_id"],
            "plant_id": row["plant_id"],
            "flower_id": row["flower_id"],
            "cohort_role": "POWER_GEOMETRY_PILOT",
            "lane": "P0_P1_G",
            "threshold_basis_eligible": "NO",
            "confirmatory_eligible": "NO",
            "notes": "separate geometry power-basis pilot",
        }
        for i, row in enumerate(rows)
    ]


SURFACES = {
    "P0G0": (40.0, 0.0, 1.0),
    "P1G0": (55.0, 1.0, 2.0),
    "P0G1": (50.0, -1.0, 2.0),
    "P1G1": (48.0, 0.0, 2.0),
}
POLLEN = {
    "P0G0": (20.0, 1.0),
    "P1G0": (25.0, 5.0),
    "P0G1": (20.0, 1.5),
    "P1G1": (25.0, 4.0),
}
SEED = {
    "P0G0": (0.82, 0.01),
    "P1G0": (0.84, 0.02),
    "P0G1": (0.80, 0.01),
    "P1G1": (0.82, 0.02),
}


def _state(row: dict[str, str]) -> str:
    p = 1 if row["pollination_treatment"] == "NATURAL" else 0
    g = 1 if row["predator_treatment"] == "EXPOSED" else 0
    return f"P{p}G{g}"


def _complete(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    completed = deepcopy(rows)
    for row in completed:
        z = float(row["target_exsertion"])
        state = _state(row)
        peak, optimum, curvature = SURFACES[state]
        final = peak - curvature * (z - optimum) ** 2
        pollen_intercept, pollen_slope = POLLEN[state]
        seed_intercept, seed_slope = SEED[state]
        initial = 100.0 * (seed_intercept + seed_slope * z)
        assert initial >= final

        row["realized_exsertion"] = str(z)
        row["water_depth"] = "1.0"
        row["ovule_count"] = "100"
        row["undamaged_seed_count"] = str(final)
        row["damaged_seed_count"] = str(initial - final)
        row["pollen_grains"] = str(pollen_intercept + pollen_slope * z)
        row["early_predator_attack_present"] = (
            "1" if row["predator_treatment"] == "EXPOSED" else "0"
        )
        row["mechanical_damage"] = "0"
    return completed


def _packet(
    *,
    n_plants: int = 10,
    flowers_per_plant: int = 4,
    max_width: float = 0.5,
) -> tuple[list[dict[str, str]], dict, list[dict[str, str]], dict]:
    config = _config(
        n_plants=n_plants,
        flowers_per_plant=flowers_per_plant,
        max_width=max_width,
    )
    allocated, receipt = allocate(
        _manifest(
            n_plants=n_plants,
            flowers_per_plant=flowers_per_plant,
        ),
        config,
        "GEOMETRY-PILOT-SEED",
    )
    completed = _complete(allocated)
    return completed, receipt, _registry(completed), config


def test_geometry_pilot_is_exact_balanced_nonconfirmatory_surface() -> None:
    completed, receipt, registry, _ = _packet()

    assert len(completed) == 40
    assert receipt["n_surface_cells"] == 20
    assert receipt["replicates_per_cell"] == 2
    assert receipt["exact_cell_balance"] is True
    assert receipt["confirmatory_eligible"] is False
    assert receipt["threshold_basis_eligible"] is False
    assert receipt["precision_gate_frozen_before_outcomes"] is True
    assert set(receipt["cell_counts"].values()) == {2}
    assert all(
        row["pilot_role"] == "POWER_BASIS_ONLY_NEVER_CONFIRMATORY"
        for row in completed
    )
    assert all(
        row["cohort_role"] == "POWER_GEOMETRY_PILOT"
        for row in registry
    )


def test_geometry_pilot_summary_is_point_ready_but_not_precision_ready() -> None:
    completed, receipt, registry, _ = _packet()
    result = summarize(completed, receipt, registry)

    assert result["status"] == READY_STATUS
    assert result["geometry_and_variance_point_estimates_complete"] is True
    assert result["geometry_and_variance_basis_complete"] is False
    assert result["precision_qualification_required"] is True
    assert result["n_power_basis_paths_resolved"] == 18
    assert len(result["resolved_power_basis_values"]) == 18
    assert len(result["pilot_data_sha256"]) == 64
    assert all(
        spec["usable_for_registered_power_basis"]
        for spec in result["surface_specs"].values()
    )
    assert result["surface_specs"]["P1G0"]["optimum"] == pytest.approx(1.0)
    assert result["surface_specs"]["P0G1"]["optimum"] == pytest.approx(-1.0)
    assert result["pollen_state_models"]["P1G1"]["z_slope"] == pytest.approx(4.0)
    assert result["initial_seed_state_models"]["P1G0"][
        "z_slope_fraction"
    ] == pytest.approx(0.02)


def test_point_estimates_alone_cannot_materialize_basis() -> None:
    completed, receipt, registry, _ = _packet()
    summary = summarize(completed, receipt, registry)

    with pytest.raises(ValueError, match="precision receipt schema mismatch"):
        materialize(
            basis._read(basis.DEFAULT_LEDGER),
            summary,
            {},
        )


def test_complete_block_geometry_pilot_can_pass_precision_and_reduce_blockers() -> None:
    completed, receipt, registry, config = _packet(
        n_plants=6,
        flowers_per_plant=20,
        max_width=0.10,
    )
    summary = summarize(completed, receipt, registry)
    precision = evaluate_precision(completed, summary, config)

    assert precision["status"] == PRECISION_READY_STATUS
    assert precision["basis_materialization_authorized"] is True
    assert precision["bootstrap_valid_all_18_path_fraction"] == 1.0
    assert precision["n_power_basis_paths_precision_evaluated"] == 18
    assert precision["failing_precision_paths"] == []
    assert all(
        value >= 0.80
        for value in precision[
            "surface_interior_concave_fraction_by_state"
        ].values()
    )

    updated, materialization = materialize(
        basis._read(basis.DEFAULT_LEDGER),
        summary,
        precision,
    )
    audit = materialization["basis_audit_after_materialization"]

    assert materialization["n_paths_promoted"] == 18
    assert audit["n_blocking_rows"] == 3
    assert set(audit["blocking_config_paths"]) == {
        "generating_model.z_levels",
        "generating_model.realized_z_sd",
        "production_surface_config.sch_surface.*",
    }
    rows = {row["config_path"]: row for row in updated}
    assert rows["generating_model.state_fitness_surfaces.P1G1"][
        "current_status"
    ] == "DIRECT_SAME_CONTEXT_READY"
    assert rows["generating_model.fitness_residual_sd"][
        "direct_registered_n_eligible"
    ] == "YES"


def test_small_incomplete_pilot_does_not_gain_precision_authorization_for_free() -> None:
    completed, receipt, registry, config = _packet(
        n_plants=10,
        flowers_per_plant=4,
        max_width=0.10,
    )
    summary = summarize(completed, receipt, registry)
    precision = evaluate_precision(completed, summary, config)

    assert precision["basis_materialization_authorized"] is False
    assert precision["status"] != PRECISION_READY_STATUS

    with pytest.raises(ValueError, match="precision is not ready"):
        materialize(
            basis._read(basis.DEFAULT_LEDGER),
            summary,
            precision,
        )


def test_completed_rows_cannot_drift_from_randomized_geometry_allocation() -> None:
    completed, receipt, registry, _ = _packet()
    completed[0]["pollination_treatment"] = (
        "SUPPLEMENTED"
        if completed[0]["pollination_treatment"] == "NATURAL"
        else "NATURAL"
    )

    with pytest.raises(ValueError, match="drifted from randomized allocation"):
        summarize(completed, receipt, registry)


def test_wrong_cohort_role_cannot_supply_power_basis() -> None:
    completed, receipt, registry, _ = _packet()
    registry[0]["cohort_role"] = "FULL_SURFACE"
    registry[0]["confirmatory_eligible"] = "YES"

    with pytest.raises(ValueError, match="POWER_GEOMETRY_PILOT"):
        summarize(completed, receipt, registry)


def test_boundary_or_nonconcave_state_blocks_even_point_estimate_readiness() -> None:
    completed, receipt, registry, config = _packet()
    for row in completed:
        if _state(row) == "P1G1":
            z = float(row["realized_exsertion"])
            row["undamaged_seed_count"] = str(30.0 + 5.0 * z)
            initial = 100.0 * (
                SEED["P1G1"][0] + SEED["P1G1"][1] * z
            )
            row["damaged_seed_count"] = str(
                initial - float(row["undamaged_seed_count"])
            )

    summary = summarize(completed, receipt, registry)

    assert summary["status"] != READY_STATUS
    assert summary["geometry_and_variance_point_estimates_complete"] is False
    assert summary["surface_specs"]["P1G1"][
        "usable_for_registered_power_basis"
    ] is False

    with pytest.raises(ValueError, match="point estimates are not ready"):
        evaluate_precision(completed, summary, config)


def test_precision_gate_must_be_frozen_before_allocation() -> None:
    config = _config()
    config["precision_gate"][
        "max_normalized_95ci_width_per_power_basis_path"
    ] = "REQUIRED_BEFORE_USE"

    with pytest.raises(ValueError, match="must be prospectively resolved"):
        allocate(
            _manifest(),
            config,
            "GEOMETRY-PILOT-SEED",
        )


def test_precision_receipt_cannot_be_reused_with_different_summary() -> None:
    completed, receipt, registry, config = _packet(
        n_plants=6,
        flowers_per_plant=20,
        max_width=0.10,
    )
    summary = summarize(completed, receipt, registry)
    precision = evaluate_precision(completed, summary, config)
    changed_summary = deepcopy(summary)
    changed_summary["pilot_ovule_count_mean"] = 99.0

    with pytest.raises(ValueError, match="not bound to this summary"):
        materialize(
            basis._read(basis.DEFAULT_LEDGER),
            changed_summary,
            precision,
        )
