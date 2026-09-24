import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_sch_h2_switch_mechanisms_v11.py"
READOUT = ROOT / "data" / "SCH_H2_SWITCH_MECHANISM_READOUT_V11.json"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_switch_mechanisms_v11", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(ROOT)


def test_v11_preserves_v10_directional_denominator():
    built = _build()
    assert built["n_cases"] == 81
    assert built["n_axes"] == 31
    assert built["n_repeated_axes"] == 27
    assert built["n_point_switch_axes"] == 14
    assert built["n_point_switch_clusters"] == 6


def test_v11_reversal_evidence_ladder_is_stricter_than_point_switch():
    built = _build()
    assert built["reversal_evidence_counts"] == {
        "NO_POINT_REVERSAL": 13,
        "POINT_REVERSAL_BOTH_SIDES_UNSUPPORTED": 5,
        "POINT_REVERSAL_ONE_SIDE_SUPPORTED": 5,
        "POINT_REVERSAL_BIDIRECTIONAL_SUPPORTED": 3,
        "POINT_REVERSAL_UNCERTAINTY_UNRESOLVED": 1,
    }
    strong = {
        row["axis"]
        for row in built["switch_axis_rows"]
        if row["reversal_evidence_level"] == "POINT_REVERSAL_BIDIRECTIONAL_SUPPORTED"
    }
    assert strong == {
        "Gymnadenia_000030_phenology",
        "Erysimum_000008_corolla_tube_width",
        "Erysimum_000008_corolla_shape",
    }


def test_v11_mechanism_taxonomy_is_descriptive_and_cluster_bounded():
    built = _build()
    rows = {row["mechanism"]: row for row in built["mechanism_rows"]}

    assert rows["MIXED_POLLINATION_X_HERBIVORY"]["n_point_switch_axes"] == 2
    assert rows["MIXED_POLLINATION_X_HERBIVORY"]["n_bidirectional_supported_axes"] == 1

    assert rows["SPATIAL_MULTI_AGENT_MOSAIC"]["n_point_switch_axes"] == 3
    assert rows["SPATIAL_MULTI_AGENT_MOSAIC"]["n_bidirectional_supported_axes"] == 2

    assert rows["POLLINATION_SUPPLEMENTATION"]["n_point_switch_axes"] == 4
    assert rows["POLLINATION_SUPPLEMENTATION"]["n_bidirectional_supported_axes"] == 0

    assert rows["CONSUMER_IDENTITY_COMPOSITION"]["n_point_switch_axes"] == 4
    assert rows["CONSUMER_IDENTITY_COMPOSITION"]["n_bidirectional_supported_axes"] == 0

    assert rows["ANTAGONIST_DAMAGE_MANIPULATION"]["n_point_switch_axes"] == 0
    assert "mechanism_cells_are_cluster_confounded" in built["claim_ceiling"]
    assert "do_not_compare_mechanism_rates_inferentially" in built["claim_ceiling"]


def test_v11_helianthus_remains_uncertainty_unresolved():
    built = _build()
    hel = next(
        row for row in built["switch_axis_rows"]
        if row["axis"] == "Helianthus_000673_ray_length"
    )
    assert hel["reversal_evidence_level"] == "POINT_REVERSAL_UNCERTAINTY_UNRESOLVED"
    assert hel["uncertainty_unresolved_contexts"] == 2


def test_v11_readout_matches_builder():
    built = _build()
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    assert built["analysis"] == frozen["analysis"]
    assert built["n_cases"] == frozen["n_cases"]
    assert built["n_axes"] == frozen["n_axes"]
    assert built["n_repeated_axes"] == frozen["n_repeated_axes"]
    assert built["n_point_switch_axes"] == frozen["n_point_switch_axes"]
    assert built["n_point_switch_clusters"] == frozen["n_point_switch_clusters"]
    assert built["reversal_evidence_counts"] == frozen["reversal_evidence_counts"]
    assert built["mechanism_rows"] == frozen["mechanism_rows"]
    assert built["status"] == frozen["status"]
    assert built["claim_ceiling"] == frozen["claim_ceiling"]
