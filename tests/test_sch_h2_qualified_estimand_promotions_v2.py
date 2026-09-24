import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"SCH_H2_QUALIFIED_ESTIMAND_PROMOTIONS_V2.csv"

def test_v2_promotion_ledger_adds_one_helianthus_programme_without_numeric_pooling_inflation():
    with P.open(encoding="utf-8",newline="") as h:
        rows=list(csv.DictReader(h))
    ids={r["programme_id"] for r in rows}
    assert ids=={
        "Lythrum_salicaria_Thomsen_selection_program",
        "Helianthus_annuus_texanus_Mitchell_selection_program",
    }
    hel=next(r for r in rows if r["programme_id"].startswith("Helianthus_"))
    assert hel["primary_source_id"]=="SCHPRISMA-000673"
    assert hel["estimand_family"]=="TOTAL_SELECTION_EFFECT"
    assert hel["numeric_pooling_family"]=="MEAN_STANDARDIZED_SELECTION_GRADIENT_NO_SE"
    assert hel["independent_cluster_qualified"]=="YES"
    assert hel["strict_numeric_pooling_qualified"]=="NO"
    assert (int(hel["n_cases"]),int(hel["n_axes"]))==(2,1)
