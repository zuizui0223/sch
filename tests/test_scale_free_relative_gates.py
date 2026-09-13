from __future__ import annotations

import math

import pytest

from scripts.evaluate_dalechampia_stage0 import _relative_change as dalechampia_relative
from scripts.evaluate_pedicularis_antagonist_weight import _paired_relative_difference as antagonist_relative
from scripts.evaluate_pedicularis_pollination_weight import _paired_relative_difference as pollination_relative
from scripts.evaluate_pedicularis_predator_weight import _plant_pairs as predator_pairs
from scripts.evaluate_pedicularis_stage_p0 import _relative_difference as stage_p0_relative
from scripts.scale_free_relative import relative_change


def test_relative_change_is_invariant_to_common_positive_units():
    for scale in (1e-16, 1e-8, 1.0, 1e8, 1e16):
        assert relative_change(1.5 * scale, scale) == pytest.approx(0.5)
        assert stage_p0_relative(1.5 * scale, scale) == pytest.approx(0.5)
        assert dalechampia_relative(1.5 * scale, scale) == pytest.approx(0.5)


def test_zero_reference_has_exact_degenerate_semantics():
    assert relative_change(0.0, 0.0) == 0.0
    assert math.isinf(relative_change(1e-300, 0.0))


def _paired_rows(treatment_key: str, left: str, right: str, field: str, scale: float):
    rows = []
    for plant in ("p1", "p2"):
        rows.append({"plant_id": plant, treatment_key: left, field: str(scale)})
        rows.append({"plant_id": plant, treatment_key: right, field: str(1.5 * scale)})
    return rows


def test_pollination_and_antagonist_pairwise_relative_gates_are_unit_invariant():
    for scale in (1e-16, 1.0, 1e16):
        poll_rows = _paired_rows(
            "pollination_treatment", "NATURAL", "SUPPLEMENTED", "realized_exsertion", scale
        )
        assert pollination_relative(poll_rows, "realized_exsertion") == pytest.approx(0.5)

        ant_rows = _paired_rows(
            "defence_treatment", "INTACT", "DRAINED", "realized_exsertion", scale
        )
        assert antagonist_relative(ant_rows, "realized_exsertion") == pytest.approx(0.5)


def _predator_row(plant: str, treatment: str, scale: float) -> dict[str, str]:
    multiplier = 1.0 if treatment == "EXPOSED" else 1.5
    return {
        "plant_id": plant,
        "predator_treatment": treatment,
        "early_predator_attack_present": "0",
        "ovule_count": "100",
        "undamaged_seed_count": "60",
        "damaged_seed_count": "20",
        "pollen_grains": str(multiplier * scale),
        "pollinator_visits": str(multiplier * scale),
        "realized_exsertion": str(multiplier * scale),
        "water_depth": "1.0",
        "mechanical_damage": "0",
    }


def test_predator_weight_relative_gates_are_unit_invariant():
    for scale in (1e-16, 1.0, 1e16):
        rows = [
            _predator_row(plant, treatment, scale)
            for plant in ("p1", "p2")
            for treatment in ("EXPOSED", "EXCLUDED")
        ]
        pairs = predator_pairs(rows)
        assert len(pairs) == 2
        for pair in pairs:
            assert pair["pollen_relative_change"] == pytest.approx(0.5)
            assert pair["pollinator_visit_relative_change"] == pytest.approx(0.5)
            assert pair["z_relative_change"] == pytest.approx(0.5)
