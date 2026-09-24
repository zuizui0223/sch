import csv
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HEL=ROOT/"data"/"SCH_H2_HELIANTHUS_TEXANUS_SELECTION_GRADIENTS_V1.csv"

def _rows(path):
    with path.open(encoding="utf-8",newline="") as h:
        return list(csv.DictReader(h))

def test_helianthus_maintext_freeze_has_exact_two_context_ray_length_gradients():
    rows=_rows(HEL)
    assert len(rows)==2
    assert {r["trait"] for r in rows}=={"ray_length"}
    assert {r["context"] for r in rows}=={"FAR_FROM_CROP_MULTIYEAR_SITES1_2","NEAR_CROP_MULTIYEAR_SITES1_2"}
    idx={r["context"]:r for r in rows}
    assert float(idx["FAR_FROM_CROP_MULTIYEAR_SITES1_2"]["beta"])==0.03
    assert float(idx["NEAR_CROP_MULTIYEAR_SITES1_2"]["beta"])==-0.02
    assert {r["fitness_measure"] for r in rows}=={"log_relative_whole_plant_seed_production"}
    assert {r["trait_standardization"] for r in rows}=={"WITHIN_POPULATION_Z_SCORE"}
    assert {r["uncertainty_status"] for r in rows}=={"NOT_NUMERICALLY_REPORTED_FOR_CONTEXT_MEAN"}
    assert {r["numeric_pooling_family"] for r in rows}=={"MEAN_STANDARDIZED_SELECTION_GRADIENT_NO_SE"}

def test_v9_opens_estimand_gate_but_keeps_strict_numeric_pooling_fail_closed():
    script=ROOT/"scripts"/"build_sch_h2_selection_cluster_expansion_v9.py"
    spec=importlib.util.spec_from_file_location("h2v9",script)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    rows,summary=mod.build(
        ROOT/"data"/"SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V6.csv",
        ROOT/"data"/"SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv",
        ROOT/"data"/"SCH_H2_LOBELIA_BARTKOWSKA_2012_SELECTION_GRADIENTS_V1.csv",
        ROOT/"data"/"SCH_H2_DALECHAMPIA_PEREZ_BARRALES_2013_SELECTION_GRADIENTS_V1.csv",
        ROOT/"data"/"SCH_H2_LYTHRUM_THOMSEN_2017_SELECTION_GRADIENTS_V1.csv",
        HEL,
    )
    assert summary["total_selection_effect"]=={"n_cases":81,"n_axes":31,"n_clusters":8,"n_repeated_axes":27}
    assert summary["standardized_selection_gradient"]=={"n_cases":61,"n_axes":26,"n_clusters":6,"n_repeated_axes":22}
    assert summary["helianthus_numeric_family"]=={"n_cases":2,"n_axes":1,"n_clusters":1,"n_repeated_axes":1}
    assert summary["h2_commensurate_estimand_gate"]=="PASS"
    assert summary["strict_numeric_pooling_gate"]=="FAIL"
    assert summary["remaining_cluster_deficit"]==0

def test_v23_v24_formally_screen_and_include_helianthus_before_numeric_use():
    v23=_rows(ROOT/"empirical"/"prisma"/"SCH_PRISMA_V2_SCREENING_DECISIONS_V23_HELIANTHUS_TEXANUS_TA.csv")
    v24=_rows(ROOT/"empirical"/"prisma"/"SCH_PRISMA_V2_SCREENING_DECISIONS_V24_HELIANTHUS_TEXANUS_FULLTEXT.csv")
    assert [r["record_id"] for r in v23]==["SCHPRISMA-000673"]
    assert v23[0]["screen_title_abstract"]=="RETAIN_FULLTEXT"
    assert [r["record_id"] for r in v24]==["SCHPRISMA-000673"]
    assert v24[0]["screen_fulltext"]=="INCLUDE"
    assert v24[0]["evidence_lanes"]=="DIRECTIONAL_OR_NEAR_PASS"
