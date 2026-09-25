import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "SCH_H2_HOLDOUT_V27_NUMERIC_SOURCE_FREEZE.csv"
READOUT = ROOT / "data" / "SCH_H2_HOLDOUT_V27_OUTCOME_READOUT.json"
SCRIPT = ROOT / "scripts" / "analyze_sch_h2_holdout_v27_outcomes.py"


def _mod():
    spec = importlib.util.spec_from_file_location("v27", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _build():
    return _mod().build(SOURCE)


def test_v27_freezes_three_programmes_without_forcing_impatiens_completion():
    built = _build()
    assert built["source_row_count"] == 31
    assert built["eligible_numeric_row_count"] == 28
    assert built["ineligible_source_row_count"] == 3
    assert built["n_programmes_adjudicated"] == 3
    assert built["n_eligible_axes"] == 12


def test_v27_programme_denominators_and_supported_reversals_are_frozen():
    rows = {row["programme_id"]: row for row in _build()["programme_rows"]}
    assert rows["Dactylorhiza_lapponica_000649_selection_program"] == {
        "programme_id": "Dactylorhiza_lapponica_000649_selection_program",
        "n_eligible_repeated_axes": 5,
        "n_bidirectionally_supported_reversal_axes": 0,
        "q_j": 0.0,
        "reversal_axis_ids": [],
    }
    assert rows["Primula_alpicola_000651_selection_program"] == {
        "programme_id": "Primula_alpicola_000651_selection_program",
        "n_eligible_repeated_axes": 4,
        "n_bidirectionally_supported_reversal_axes": 0,
        "q_j": 0.0,
        "reversal_axis_ids": [],
    }
    assert rows["Trillium_discolor_000661_selection_program"] == {
        "programme_id": "Trillium_discolor_000661_selection_program",
        "n_eligible_repeated_axes": 3,
        "n_bidirectionally_supported_reversal_axes": 2,
        "q_j": 2 / 3,
        "reversal_axis_ids": [
            "Trillium_000661_display_height",
            "Trillium_000661_petal_size",
        ],
    }


def test_v27_trillium_reversals_require_supported_opposite_directions():
    axes = {
        row["canonical_axis"]: row
        for row in _build()["axis_rows"]
        if row["programme_id"] == "Trillium_discolor_000661_selection_program"
    }
    assert axes["Trillium_000661_display_height"]["supported_positive"] is True
    assert axes["Trillium_000661_display_height"]["supported_negative"] is True
    assert axes["Trillium_000661_petal_size"]["supported_positive"] is True
    assert axes["Trillium_000661_petal_size"]["supported_negative"] is True
    assert axes["Trillium_000661_flowering_date"]["bidirectionally_supported_reversal"] is False


def test_v27_nonfloral_primula_rosette_and_categorical_trillium_color_are_excluded():
    built = _build()
    axis_ids = {row["canonical_axis"] for row in built["axis_rows"]}
    assert "Primula_000651_rosette_diameter" not in axis_ids
    assert "Trillium_000661_petal_color" not in axis_ids


def test_v27_readout_summary_matches_builder():
    built = _build()
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    for key in (
        "analysis",
        "source_row_count",
        "eligible_numeric_row_count",
        "ineligible_source_row_count",
        "n_programmes_adjudicated",
        "n_eligible_axes",
        "n_supported_reversal_axes",
        "programme_rows",
        "status",
        "claim_ceiling",
    ):
        assert built[key] == frozen[key]
