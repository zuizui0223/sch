"""Core ten-reference coverage and outstanding sixteen-cluster bibliography audit."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from scripts.audit_sch_amnat_reference_coverage import (
    PAPER,VERIFIED,SOURCE_NOTE,LEDGER,PRIMARY_DOIS,CORRECTION_DOI,
    read_csv,doi_set,build,
)


def _inputs():
    return (
        PAPER.read_text(encoding="utf-8"),
        read_csv(VERIFIED),
        read_csv(LEDGER),
        SOURCE_NOTE.read_text(encoding="utf-8"),
    )


def test_ten_verified_primary_and_correction_publication_records():
    m,meta,ledger,note=_inputs()
    a=build(m,meta,ledger,note)
    assert len(meta)==10
    assert len(PRIMARY_DOIS)==9
    assert CORRECTION_DOI not in PRIMARY_DOIS
    assert a["n_verified_source_records"]==10
    assert a["n_original_experiment_references"]==9
    assert a["n_linked_author_correction_references"]==1
    assert a["n_unique_prose_dois"]==10
    assert a["n_unique_bibliography_dois"]==10
    assert a["complete_prose_doi_to_core_bibliography_match"]
    assert {r["doi"] for r in meta}==doi_set(m)
    assert a["known_issue_year_exception"][
        "publisher_issue_citation_year"]==2023
    assert a["primula_2019_correction_does_not_change_used_table2_linear_beta"]


def test_core_bibliography_does_not_claim_all_conceptual_literature_has_been_cited():
    m,meta,ledger,note=_inputs()
    a=build(m,meta,ledger,note)
    assert a["original_pattern_clusters"]==16
    assert a["n_such_clusters"]==14
    assert len(a["clusters_not_explicitly_doi_supported_in_prose"])==14
    assert not a["all_16_cluster_references_completed"]
    assert not a["external_herbivory_meta_analysis_citations_verified"]
    assert not a["submission_ready"]
    assert a["status"].endswith("REFERENCE_COMPLETENESS_OPEN")
    missing={r["cluster_id"] for r in a[
        "clusters_not_explicitly_doi_supported_in_prose"]}
    assert "Satyrium_spur_gender_compromise" in missing
    assert "Castilleja_calyx" in missing
    assert "Silene_petals_sexual_function" in missing
    assert "Gymnadenia_agent_weight_shift" not in missing
    assert "Pedicularis_exsertion" not in missing


def test_2023_issue_year_and_2019_correction_are_not_silently_conflated():
    m,meta,ledger,note=_inputs()
    assert "Koski 2023" in m
    assert "Koski 2022" not in m
    assert "Chen, Zhang and Li 2019" in m
    assert "Table 3 notation" in m
    assert "## Literature Cited" in m
    a=build(m,meta,ledger,note)
    assert a["known_issue_year_exception"]["online_first_year"]==2022
    assert a["known_issue_year_exception"]["field_years"]==[2020,2021]


@pytest.mark.parametrize(("change","message"),[
    ("delete_correction","all verified DOI source items"),
    ("delete_primula_citation","all verified DOI source items"),
    ("change_koski_year","original author-year"),
    ("remove_bibliography","unique core Literature Cited"),
])
def test_missing_or_wrong_primary_reference_fails_closed(change,message):
    m,meta,ledger,note=_inputs()
    if change=="delete_correction":
        m=m.replace(
            "https://doi.org/10.1038/s41598-019-43381-6","https://doi.org/none"
        )
    elif change=="delete_primula_citation":
        m=m.replace("doi:10.1038/s41598-017-13340-0",
                    "doi:MISSING_PRIMARY_SOURCE",1)
    elif change=="change_koski_year":
        m=m.replace("Koski 2023","Koski 2022",1)
    elif change=="remove_bibliography":
        m=m.replace("## Literature Cited\n","## SOURCES REMOVED\n",1)
    with pytest.raises(ValueError,match=message):
        build(m,meta,ledger,note)


def test_metadata_noncanonical_publication_year_or_title_is_rejected():
    m,meta,ledger,note=_inputs()
    corrupted=deepcopy(meta)
    koski=next(r for r in corrupted if r["first_author"]=="Koski")
    koski["issue_year"]="2022"
    with pytest.raises(ValueError,match="missing 2022|unverified|publisher issue year"):
        build(m,corrupted,ledger,note)
    corrupted=deepcopy(meta)
    corrupted[0]["article_title"]="FICTIONAL TITLE"
    with pytest.raises(ValueError,match="unverified"):
        build(m,corrupted,ledger,note)


def test_no_duplicate_DOI_or_cluster_pseudoreplication_allowed():
    m,meta,ledger,note=_inputs()
    double=deepcopy(meta)
    double[1]["doi"]=double[0]["doi"]
    with pytest.raises(ValueError,match="ten source-verified"):
        build(m,double,ledger,note)
    double=deepcopy(ledger)
    double[0]["cluster_id"]=double[1]["cluster_id"]
    with pytest.raises(ValueError,match="16 biological-cluster"):
        build(m,meta,double,note)
