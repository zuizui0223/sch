"""Cross-file flower-id reuse is not independent experimental replication."""
import pytest
from scripts.audit_sch_blueberry_2020_crossfile_flower_overlap import (
    DOI,SOURCE_RECORD_ID,SOURCE_EXPECTED,COMPOSITE_FIELDS,
    flower_identity,pair_overlap,strict_original_rows,
)

def demo(tag,fs):
    return {"Species":"Powder Blue","Year":"2017","Block":"B81",
      "Row":"2","Plant.number":"6","RP":"2-6","Tag":str(tag),
      "FS":str(fs),"Pick.date":"2017-12-01","Fresh.wgt":"1.2"}

def test_source_programme_three_files_are_not_three_independent_studies():
    assert DOI=="10.1111/1365-2664.13751"
    assert SOURCE_RECORD_ID==3987488
    assert SOURCE_EXPECTED=={"multiple":2080,"single":1309,"pollination":2125}
    assert COMPOSITE_FIELDS==("Species","Year","Block","RP","Tag")

def test_exact_same_original_flower_identity_and_fruit_agreement():
    a=demo(101,1);b=dict(a)
    c=demo(102,0)
    first,receipt=strict_original_rows([a,c],"first")
    second,_=strict_original_rows([b],"second")
    joined=pair_overlap(first,second)
    assert joined["source_flower_identity_matches"]==1
    assert joined["n_identity_matched_FS_disagreements"]==0
    assert joined["all_matched_fruit_outcomes_agree"]
    assert joined["source_matched_data_not_independent"]
    b["FS"]="0"
    first,_=strict_original_rows([a],"first")
    second,_=strict_original_rows([b],"second")
    mismatch=pair_overlap(first,second)
    assert mismatch["n_identity_matched_FS_disagreements"]==1
    with pytest.raises(ValueError):
        strict_original_rows([a,a],"duplicates")

def test_missing_composite_or_blank_tag_refused():
    x=demo(10,1);x["Tag"]=""
    with pytest.raises(ValueError):
        flower_identity(x)
    y=demo(10,1);del y["RP"]
    with pytest.raises(ValueError):
        flower_identity(y)


def test_missing_original_tag_is_not_invented_as_a_reusable_flower_id():
    original=demo("NA",1)
    found,receipt=strict_original_rows([original],"missing")
    assert found=={}
    assert receipt["n_flower_rows_with_incomplete_tag_or_core_ID"]==1
    assert receipt["crossfile_nonmatch_cannot_certify_flower_independence"] is True
    assert receipt["source_missing_tags_by_type_and_protocol"]


def test_three_original_csvs_are_overlapping_source_flower_records_not_replications():
    import csv
    from pathlib import Path
    with Path("data/SCH_BLUEBERRY_2020_CROSSFILE_FLOWER_REUSE_V1.csv").open(
        encoding="utf-8",newline="") as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==6
    d={x["source_regime_pair"]:x for x in rows}
    one=d["multiple_one__single_one_visited"]
    assert int(one["n_linkable_source_A"])==331
    assert int(one["n_linkable_source_B"])==331
    assert int(one["exact_same_tagged_flower_matches"])==331
    zero=d["multiple_zero__pollination_no"]
    assert int(zero["n_linkable_source_A"])==768
    assert int(zero["n_linkable_source_B"])==768
    assert int(zero["exact_same_tagged_flower_matches"])==768
    assert int(d["multiple_zero__single_unvisited"]["exact_same_tagged_flower_matches"])==768
    assert int(d["single_unvisited__pollination_no"]["exact_same_tagged_flower_matches"])==768
    for row in rows:
        assert int(row["n_matched_binary_fruit_disagreements"])==0
        assert int(row["n_matched_pick_date_weight_disagreements"])==0
    assert int(d["multiple_one__pollination_no"]["exact_same_tagged_flower_matches"])==0
    assert int(d["multiple_zero__single_one_visited"]["exact_same_tagged_flower_matches"])==0
