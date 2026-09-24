import csv
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LYTHRUM=ROOT/"data"/"SCH_H2_LYTHRUM_THOMSEN_2017_SELECTION_GRADIENTS_V1.csv"

def _rows(path):
    with path.open(encoding="utf-8",newline="") as h:
        return list(csv.DictReader(h))

def test_lythrum_table2_freezes_all_total_and_contrast_coefficients():
    rows=_rows(LYTHRUM)
    assert len(rows)==15
    assert {r["trait"] for r in rows}=={"number_of_inflorescences","inflorescence_height","flowering_start_time"}
    assert {r["estimand_role"] for r in rows}=={"TOTAL_SELECTION","MEDIATED_CONTRAST"}
    totals=[r for r in rows if r["estimand_role"]=="TOTAL_SELECTION"]
    assert len(totals)==6
    idx={(r["trait"],r["context_or_contrast"]):r for r in totals}
    assert (float(idx[("number_of_inflorescences","CLIPPED")]["beta_or_delta"]),float(idx[("number_of_inflorescences","CLIPPED")]["se"]))==(0.20,0.07)
    assert (float(idx[("flowering_start_time","CLIPPED")]["beta_or_delta"]),float(idx[("flowering_start_time","CLIPPED")]["se"]))==(-0.28,0.06)
    assert (float(idx[("inflorescence_height","CONTROL")]["beta_or_delta"]),float(idx[("inflorescence_height","CONTROL")]["se"]))==(0.33,0.09)
    assert {r["fitness_measure"] for r in totals}=={"relative_total_seed_production"}
    assert {r["trait_standardization"] for r in totals}=={"WITHIN_TREATMENT_Z_SCORE"}

def test_v8_adds_lythrum_as_seventh_independent_total_selection_cluster():
    script=ROOT/"scripts"/"build_sch_h2_selection_cluster_expansion_v8.py"
    spec=importlib.util.spec_from_file_location("h2v8",script)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    rows,summary=mod.build(
        ROOT/"data"/"SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V6.csv",
        ROOT/"data"/"SCH_H2_BRASSICA_KNAUER_2017_SELECTION_GRADIENTS_V1.csv",
        ROOT/"data"/"SCH_H2_LOBELIA_BARTKOWSKA_2012_SELECTION_GRADIENTS_V1.csv",
        ROOT/"data"/"SCH_H2_DALECHAMPIA_PEREZ_BARRALES_2013_SELECTION_GRADIENTS_V1.csv",
        LYTHRUM,
    )
    assert summary["total_selection_effect"]=={"n_cases":79,"n_axes":30,"n_clusters":7,"n_repeated_axes":26}
    assert summary["standardized_selection_gradient"]=={"n_cases":61,"n_axes":26,"n_clusters":6,"n_repeated_axes":25}
    assert summary["h2_commensurate_estimand_gate"]=="FAIL"
    assert summary["remaining_cluster_deficit"]==1
    assert "Lythrum_salicaria_Thomsen_selection_program" in summary["new_clusters"]
