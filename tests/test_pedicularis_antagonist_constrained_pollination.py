from __future__ import annotations

from copy import deepcopy

from scripts.analyze_pedicularis_antagonist_constrained_pollination import build


def _rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(12):
        plant_effect = (plant % 4) * 0.2
        for z_index, z in enumerate((0.2, 0.35, 0.5, 0.65, 0.8)):
            for predator in ("EXCLUDED", "EXPOSED"):
                pollen = 5.0 + 20.0 * z + plant_effect
                initial_seed_count = int(round(8 + 20 * z + plant_effect))
                damaged = 0 if predator == "EXCLUDED" else 3
                undamaged = max(0, initial_seed_count - damaged)
                rows.append(
                    {
                        "population_id": "P_REX_TEST",
                        "season_id": "S1",
                        "plant_id": f"P{plant:02d}",
                        "flower_id": (
                            f"P{plant:02d}_Z{z_index}_{predator}"
                        ),
                        "assigned_z_level": f"Z{z_index}",
                        "realized_exsertion": str(z),
                        "pollination_treatment": "NATURAL",
                        "predator_treatment": predator,
                        "exclusion_method": (
                            "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
                            if predator == "EXCLUDED"
                            else "SHAM_SLEEVE"
                        ),
                        "water_depth": "1.0",
                        "ovule_count": "40",
                        "undamaged_seed_count": str(undamaged),
                        "damaged_seed_count": str(damaged),
                        "pollen_grains": str(pollen),
                        "early_predator_attack_present": (
                            "0" if predator == "EXCLUDED" else "1"
                        ),
                        "mechanical_damage": "0",
                    }
                )
    return rows


def _surface_receipt() -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "system_wrapper_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2",
        "system": "Pedicularis rex",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "observed_estimands": {
            "z_pollinator_context": 0.8,
            "z_combined": 0.5,
            "shift_remove_antagonist": 0.3,
        },
        "bootstrap": {
            "shift_remove_antagonist_95_ci": [0.12, 0.47],
        },
    }


def _config() -> dict:
    return {"bootstrap_reps": 300, "random_seed": 17}


def test_positive_surface_supports_contemporary_antagonist_constraint() -> None:
    result = build(_rows(), _surface_receipt(), _config())

    assert result["predator_removal_shifts_optimum_upward"] is True
    assert result["higher_z_increases_pollen_receipt_in_both_G_states"] is True
    assert result["higher_z_increases_initial_seed_set_in_both_G_states"] is True
    assert (
        result[
            "contemporary_antagonist_constrained_pollination_chain_supported"
        ]
        is True
    )
    assert result["status"] == (
        "CONTEMPORARY_ANTAGONIST_CONSTRAINED_POLLINATION_SUPPORTED"
    )


def test_positive_contemporary_chain_does_not_become_adaptive_evolution_claim() -> None:
    result = build(_rows(), _surface_receipt(), _config())

    assert result["adaptive_pollen_limitation_supported"] is False
    assert result["evolutionary_maintenance_identified"] is False
    assert result["cue_identity_identified"] is False
    assert "does_not_promote_to_adaptive_pollen_limitation" in (
        result["claim_ceiling"]
    )


def test_optimum_shift_ci_crossing_zero_fails_chain() -> None:
    receipt = _surface_receipt()
    receipt["bootstrap"]["shift_remove_antagonist_95_ci"] = [-0.05, 0.40]

    result = build(_rows(), receipt, _config())

    assert result["predator_removal_shifts_optimum_upward"] is False
    assert (
        result[
            "contemporary_antagonist_constrained_pollination_chain_supported"
        ]
        is False
    )


def test_nonpositive_z_to_pollen_response_fails_chain() -> None:
    rows = deepcopy(_rows())
    for row in rows:
        if row["predator_treatment"] == "EXPOSED":
            z = float(row["realized_exsertion"])
            row["pollen_grains"] = str(30.0 - 20.0 * z)

    result = build(rows, _surface_receipt(), _config())

    assert result["higher_z_increases_pollen_receipt_in_both_G_states"] is False
    assert (
        result[
            "contemporary_antagonist_constrained_pollination_chain_supported"
        ]
        is False
    )


def test_requires_positive_primary_causal_surface() -> None:
    receipt = _surface_receipt()
    receipt["status"] = "COMPROMISE_CRITERIA_NOT_ALL_RECOVERED"

    try:
        build(_rows(), receipt, _config())
    except ValueError as exc:
        assert "positive causal-compromise surface" in str(exc)
    else:
        raise AssertionError("negative primary surface should fail closed")
