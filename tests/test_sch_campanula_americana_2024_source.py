"""Original Makowski et al. 2024 Campanula source SHA/MD5 validation."""
from scripts.ingest_sch_campanula_americana_2024 import (
    ARTICLE_DOI,ZENODO_RECORD,DATA_DOI,LICENSE,MANIFEST,
    _csv_rows,audit_roles,col,_normal
)
import pytest

def test_exact_original_source_archive_and_license():
    assert ARTICLE_DOI=="10.1002/ajb2.16351"
    assert ZENODO_RECORD==10814705
    assert DATA_DOI=="10.5281/zenodo.10814705"
    assert LICENSE=="CC-BY-4.0"
    assert MANIFEST=={
        "PLdataindividual.csv":"b84fa5c83513dbe75c0bf7840d1c74aa",
        "pollinator.csv":"81e0deaa78a6a97e1211484cb9d0d3b3",
    }

def test_nonfile_HTML_and_tabular_outcome_units():
    header="source.population,autonomy,individual,experimental.population,site,size,treatment,seed number"
    rows=[header]
    for n in range(35):
        rows.append(f"P{n%4},{'high' if n%2 else 'low'},i{n},exp{n%6},site1,small,control,{n%10}")
    body=("\n".join(rows)+"\n").encode()
    records,headers,enc=_csv_rows(body)
    v=audit_roles(records,headers,"PLdataindividual.csv")
    assert len(records)==35
    assert v["source_label_roles_qualified"]
    assert not v["required_source_roles_missing"]
    assert v["seed_outcome_diagnostics"]["n_original_nonmissing_integer_seed_counts"]==35
    assert v["seed_outcome_diagnostics"]["n_source_invalid_nonmissing_seed_counts"]==0
    with pytest.raises(ValueError):
        _csv_rows(b"<!doctype html><html>login</html>")

def test_source_variable_normalization_without_invented_identifier():
    fields=["source.population","seed number","experimental.population","visits.per.flower"]
    assert col(fields,"source population")=="source.population"
    assert col(fields,"seed.number")=="seed number"
    assert col(fields,"experimental population")=="experimental.population"
    assert col(fields,"visits per flower")=="visits.per.flower"
    assert _normal("Treatment")=="treatment"
