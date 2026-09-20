import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL = ROOT / "data" / "SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv"
CONTRASTS = ROOT / "data" / "SCH_MACROECOLOGY_GYMNADENIA_A2_MEDIATED_CONTRASTS_V1.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_full_table_a2_freeze_has_all_20_trait_treatment_cells():
    rows = _rows(FULL)
    assert len(rows) == 20
    assert {row["trait"] for row in rows} == {
        "plant_height",
        "number_of_flowers",
        "corolla_size",
        "spur_length",
        "flowering_start",
    }
    assert {row["treatment"] for row in rows} == {"C+H", "C+E", "HP+H", "HP+E"}


def test_full_table_a2_freeze_preserves_registered_h2_axis_values():
    rows = {(r["trait"], r["treatment"]): r for r in _rows(FULL)}

    assert (float(rows[("flowering_start", "C+H")]["beta"]), float(rows[("flowering_start", "C+H")]["se"])) == (-0.0042, 0.054)
    assert (float(rows[("flowering_start", "C+E")]["beta"]), float(rows[("flowering_start", "C+E")]["se"])) == (0.094, 0.031)
    assert (float(rows[("flowering_start", "HP+H")]["beta"]), float(rows[("flowering_start", "HP+H")]["se"])) == (-0.16, 0.056)
    assert (float(rows[("flowering_start", "HP+E")]["beta"]), float(rows[("flowering_start", "HP+E")]["se"])) == (-0.066, 0.028)

    assert (float(rows[("spur_length", "C+H")]["beta"]), float(rows[("spur_length", "C+H")]["se"])) == (0.18, 0.057)
    assert (float(rows[("spur_length", "C+E")]["beta"]), float(rows[("spur_length", "C+E")]["se"])) == (0.077, 0.035)
    assert (float(rows[("spur_length", "HP+H")]["beta"]), float(rows[("spur_length", "HP+H")]["se"])) == (0.083, 0.053)
    assert (float(rows[("spur_length", "HP+E")]["beta"]), float(rows[("spur_length", "HP+E")]["se"])) == (-0.042, 0.029)


def test_full_table_a2_freeze_reconstructs_existing_mediated_contrast_points():
    rows = {(r["trait"], r["treatment"]): float(r["beta"]) for r in _rows(FULL)}
    contrasts = {r["contrast_id"]: float(r["delta_beta"]) for r in _rows(CONTRASTS)}

    assert round(rows[("flowering_start", "C+H")] - rows[("flowering_start", "HP+H")], 2) == contrasts["Gymnadenia_phenology_poll_H"]
    assert round(rows[("flowering_start", "C+E")] - rows[("flowering_start", "HP+E")], 2) == contrasts["Gymnadenia_phenology_poll_E"]
    assert round(rows[("flowering_start", "C+H")] - rows[("flowering_start", "C+E")], 3) == contrasts["Gymnadenia_phenology_herb_C"]
    assert round(rows[("flowering_start", "HP+H")] - rows[("flowering_start", "HP+E")], 3) == contrasts["Gymnadenia_phenology_herb_HP"]

    assert round(rows[("spur_length", "C+H")] - rows[("spur_length", "HP+H")], 2) == contrasts["Gymnadenia_spur_poll_H"]
    assert round(rows[("spur_length", "C+E")] - rows[("spur_length", "HP+E")], 2) == contrasts["Gymnadenia_spur_poll_E"]
    assert round(rows[("spur_length", "C+H")] - rows[("spur_length", "C+E")], 2) == contrasts["Gymnadenia_spur_herb_C"]
    assert round(rows[("spur_length", "HP+H")] - rows[("spur_length", "HP+E")], 2) == contrasts["Gymnadenia_spur_herb_HP"]


def test_full_table_a2_freeze_preserves_non_target_traits_too():
    rows = {(r["trait"], r["treatment"]): r for r in _rows(FULL)}
    assert float(rows[("plant_height", "C+E")]["beta"]) == 0.087
    assert float(rows[("number_of_flowers", "C+H")]["beta"]) == 0.44
    assert float(rows[("corolla_size", "HP+H")]["beta"]) == -0.023
