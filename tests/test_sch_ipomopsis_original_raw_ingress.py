"""Offline, explicitly synthetic ingress *software* fixtures only.

Scientific measurements MUST come from the verified archive file, not these tests.
"""
from __future__ import annotations

import hashlib
import pytest
from scripts.ingest_sch_ipomopsis_public_raw import (
    FILES, MAX_DOWNLOAD, MISSING, source_urls, verified_bytes,
    schema_report,
)


def test_public_archive_names_are_pinned_and_urls_are_specific():
    assert len(FILES)==2
    assert FILES["Selection_by_pollinators_and_predators.csv"]=="12ed3dbe6d269c5f808f9c6b230d468c"
    assert FILES["ReadMe_Selection_by_pollinators_and_predators.csv"]=="e681a5a0885271c4797730b5a30574d8"
    for name in FILES:
        urls=source_urls(name)
        assert len(urls)==3
        assert all("5083399" in url and name in url for url in urls)
        assert all(url.startswith("https://zenodo.org/") for url in urls)
    with pytest.raises(ValueError):
        source_urls("../not-an-archive-file.csv")


def test_wrong_bytes_are_always_rejected_not_mistaken_as_original_data():
    for name in FILES:
        with pytest.raises(ValueError,match="checksum mismatch"):
            verified_bytes(b"toy,row\n1,2\n",name)
        with pytest.raises(ValueError,match="missing or unexpectedly large"):
            verified_bytes(b"",name)
        with pytest.raises(ValueError,match="missing or unexpectedly large"):
            verified_bytes(b"x"*(MAX_DOWNLOAD+1),name)
    with pytest.raises(ValueError,match="unregistered"):
        verified_bytes(b"toy", "unknown.csv")


def test_column_audit_preserves_missingness_and_original_label_levels():
    # A code-only mock; these 3 rows are NOT ecological study observations.
    csv_text=(
        "site,plant_id,initiated,predated,escape\n"
        "north,a,10,2,0.8\n"
        "south,b,20,.,0.6\n"
        "north,c,0,0,NA\n"
    ).encode()
    dictionary=b"Mock only, NOT real field metadata"
    report=schema_report(csv_text,dictionary)
    assert report["status"]=="REAL_DATA_INGRESS_SCHEMA_ONLY_NO_BIOLOGICAL_INFERENCE"
    assert report["n_original_data_rows"]==3
    assert report["n_columns"]==5
    columns={r["column"]:r for r in report["columns"]}
    assert columns["site"]["categorical_distribution"]=={"north":2,"south":1}
    assert columns["predated"]["missing"]==1
    assert columns["initiated"]["n_zero"]==1
    assert columns["escape"]["missing"]==1
    assert report["positive_scientific_effect_estimated"] is False
    assert report["sample_weighting_or_cluster_independence_assumed"] is False


def test_fail_closed_on_duplicate_headers_empty_study_and_record_mismatch():
    with pytest.raises(ValueError,match="duplicated column"):
        schema_report(b"x,x\n1,2\n",b"d")
    with pytest.raises(ValueError,match="no plant rows"):
        schema_report(b"x,y\n",b"d")
    with pytest.raises(ValueError,match="wider than stated header"):
        schema_report(b"x,y\n1,2,3\n",b"d")
