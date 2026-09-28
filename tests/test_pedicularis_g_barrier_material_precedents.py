from scripts.audit_pedicularis_g_barrier_material_precedents import build


def test_barrier_material_ledger_preserves_external_only_boundary() -> None:
    result = build()
    assert result["n_barrier_precedents"] == 3
    assert result["focal_p_rex_barrier_effectiveness_recovered"] is False
    assert result["focal_p_rex_barrier_selectivity_recovered"] is False
    assert result["status"] == (
        "G_BARRIER_MATERIAL_PRECEDENTS_RECOVERED_"
        "P_REX_EFFECTIVENESS_SELECTIVITY_STILL_REQUIRED"
    )


def test_porous_tubing_and_mesh_failure_modes_are_both_recovered() -> None:
    result = build()
    assert result["porous_tubing_material_class_feasibility_recovered"] is True
    assert result["mesh_aperture_failure_mode_recovered"] is True
    assert result["mesh_mechanical_load_failure_mode_recovered"] is True
    assert result["pilot_material_classes"] == [
        "SOFT_POROUS_OR_DIALYSIS_LIKE_TUBING",
        "FINE_INERT_MESH",
    ]


def test_within_genus_timing_does_not_become_material_effectiveness() -> None:
    result = build()
    assert result["pedicularis_postpollination_timing_recovered"] is True
    assert "within_genus_timing_is_not_material_effectiveness" in (
        result["claim_ceiling"]
    )


def test_focal_pilot_checks_include_water_and_pollination_lanes() -> None:
    result = build()
    assert {
        "pollen_receipt_stability",
        "pollinator_visitation_stability",
        "water_state_stability",
        "mechanical_damage_stability",
        "predator_attack_reduction",
        "seed_predation_reduction",
    } <= set(result["required_focal_checks"])
