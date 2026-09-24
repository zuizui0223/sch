import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V21_ESTIMAND_PRIORITY_BATCH1.csv"
BRASSICA = ROOT / "data" / "SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv"
LOBELIA = ROOT / "data" / "SCH_H2_LOBELIA_BARTKOWSKA_2012_SELECTION_GRADIENTS_V1.csv"
DALECHAMPIA = ROOT / "data" / "SCH_H2_DALECHAMPIA_PEREZ_BARRALES_2013_SELECTION_GRADIENTS_V1.csv"

def _rows(path):
    with path.open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h))

def test_v21_freezes_first_six_outcome_blind_priority_records_for_fulltext():
    rows = _rows(PRISMA)
    assert [r["record_id"] for r in rows] == [
        "SCHPRISMA-000434","SCHPRISMA-000550","SCHPRISMA-000648",
        "SCHPRISMA-000659","SCHPRISMA-000775","SCHPRISMA-000812",
    ]
    assert {r["screen_title_abstract"] for r in rows} == {"RETAIN_FULLTEXT"}
    assert {r["decision_source"] for r in rows} == {"SOURCE_VERIFIED_ESTIMAND_PRIORITY_BATCH1_V21_2026-09-23"}

def test_brassica_table2_freeze_has_all_27_trait_context_cells():
    rows = _rows(BRASSICA)
    assert len(rows) == 27
    assert len({r["trait"] for r in rows}) == 9
    assert {r["consumer_regime"] for r in rows} == {
        "BUMBLE_BEE","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY","CABBAGE_BUTTERFLY"
    }
    idx={(r["trait"],r["consumer_regime"]):r for r in rows}
    assert (float(idx[("corolla_size","BUMBLE_BEE")]["beta"]),float(idx[("corolla_size","BUMBLE_BEE")]["se"])) == (0.22,0.04)
    assert (float(idx[("phenylacetaldehyde","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY")]["beta"]),float(idx[("phenylacetaldehyde","BUMBLE_BEE_PLUS_CABBAGE_BUTTERFLY")]["se"])) == (-0.09,0.08)

def test_lobelia_table2_freeze_has_all_12_trait_pollination_cells():
    rows = _rows(LOBELIA)
    assert len(rows) == 12
    assert len({r["trait"] for r in rows}) == 6
    assert {r["pollination_context"] for r in rows} == {"NATURAL","HAND_SUPPLEMENTED"}
    idx={(r["trait"],r["pollination_context"]):r for r in rows}
    assert (float(idx[("flower_number","NATURAL")]["beta"]),float(idx[("flower_number","NATURAL")]["se"])) == (0.74,0.18)
    assert (float(idx[("median_flower_date","HAND_SUPPLEMENTED")]["beta"]),float(idx[("median_flower_date","HAND_SUPPLEMENTED")]["se"])) == (-0.40,0.07)


def test_v7_builder_adds_two_independent_standardized_selection_clusters():
    import importlib.util
    script = ROOT / "scripts" / "build_sch_h2_selection_cluster_expansion_v7.py"
    spec = importlib.util.spec_from_file_location("h2v7", script)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    rows, summary = mod.build(
        ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V6.csv",
        BRASSICA,
        LOBELIA,
        DALECHAMPIA,
    )
    assert summary["added_cases"] == 43
    assert summary["added_axes"] == 19
    assert summary["added_clusters"] == 3
    assert summary["total_selection_effect"]["n_cases"] == 73
    assert summary["total_selection_effect"]["n_axes"] == 27
    assert summary["total_selection_effect"]["n_clusters"] == 6
    assert summary["standardized_selection_gradient"]["n_cases"] == 55
    assert summary["standardized_selection_gradient"]["n_axes"] == 23
    assert summary["standardized_selection_gradient"]["n_clusters"] == 5
    assert summary["h2_commensurate_estimand_gate"] == "FAIL"
    assert summary["remaining_cluster_deficit"] == 2


def test_v22_fulltext_promotes_only_source_resolved_selection_studies():
    rows = _rows(ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V22_ESTIMAND_PRIORITY_FULLTEXT.csv")
    assert {r["record_id"] for r in rows} == {"SCHPRISMA-000659","SCHPRISMA-000775"}
    assert {r["screen_fulltext"] for r in rows} == {"INCLUDE"}
    assert {r["evidence_lanes"] for r in rows} == {"DIRECTIONAL_OR_NEAR_PASS"}



def test_dalechampia_source_freeze_preserves_agent_and_net_gradients():
    rows = _rows(DALECHAMPIA)
    assert {r["trait"] for r in rows} >= {"upper_bract_area","gland_area","gland_stigma_distance"}
    assert {r["selection_component"] for r in rows} >= {"NET","POLLINATOR","SEED_PREDATOR"}
    bract={r["selection_component"]:r for r in rows if r["trait"]=="upper_bract_area"}
    assert float(bract["POLLINATOR"]["beta_percent_fitness"]) > 0
    assert float(bract["SEED_PREDATOR"]["beta_percent_fitness"]) < 0
    assert bract["NET"]["fitness_estimate"] == "relative_seeds_surviving_predation"
