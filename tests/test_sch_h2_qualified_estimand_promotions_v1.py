import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/"data"/"SCH_H2_QUALIFIED_ESTIMAND_PROMOTIONS_V1.csv"
def test_lythrum_promotion_counts_one_programme_not_thesis_twice():
    with P.open(encoding="utf-8",newline="") as h: rows=list(csv.DictReader(h))
    lyr=next(r for r in rows if r["programme_id"]=="Lythrum_salicaria_Thomsen_selection_program")
    assert lyr["primary_source_id"]=="SCHPRISMA-000284"
    assert lyr["dependent_source_ids"]=="SCHPRISMA-000812"
    assert lyr["independent_cluster_qualified"]=="YES"
    assert (int(lyr["n_cases"]),int(lyr["n_axes"]))==(6,3)
    assert lyr["numeric_pooling_family"]=="STANDARDIZED_SELECTION_GRADIENT"
