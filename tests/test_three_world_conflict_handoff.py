import pytest

from scripts.export_three_world_conflict_handoff import export_handoff


def _receipt():
    return {
        "receipt_schema_version": "SCH_COMPONENT_CONFLICT_BUDGET_V1",
        "status": "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED",
        "fitness_scale_id": "INTACT_SEEDS_PER_FLOWER",
        "source_sch_receipt_schema": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "criticality_export": {
            "L_S_component": 0.4,
            "L_S_component_95_ci": [0.3, 0.5],
        },
    }


def _context():
    return {
        "context_id": "PEDICULARIS_POP_A_2027",
        "system": "Pedicularis rex",
        "population_id": "POP_A",
        "season_id": "2027",
        "fitness_scale_id": "INTACT_SEEDS_PER_FLOWER",
    }


def test_export_freezes_context_and_scale():
    result = export_handoff(_receipt(), _context())
    assert result["receipt_schema_version"] == "THREE_WORLD_CONFLICT_HANDOFF_V1"
    assert result["status"] == "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED"
    assert result["context_id"] == "PEDICULARIS_POP_A_2027"
    assert result["population_id"] == "POP_A"
    assert result["season_id"] == "2027"
    assert result["fitness_scale_id"] == "INTACT_SEEDS_PER_FLOWER"
    assert result["conflict_load"] == {
        "point": 0.4,
        "lower_95": 0.3,
        "upper_95": 0.5,
        "source_field": "criticality_export.L_S_component",
    }


def test_scale_mismatch_fails_closed():
    context = _context()
    context["fitness_scale_id"] = "RELATIVE_FITNESS"
    with pytest.raises(ValueError, match="exactly match"):
        export_handoff(_receipt(), context)


def test_missing_context_id_fails_closed():
    context = _context()
    context["context_id"] = ""
    with pytest.raises(ValueError, match="context_id"):
        export_handoff(_receipt(), context)


def test_conflict_point_must_lie_inside_interval():
    receipt = _receipt()
    receipt["criticality_export"]["L_S_component"] = 0.8
    with pytest.raises(ValueError, match="within"):
        export_handoff(receipt, _context())
