"""The raw Dryad source-probe is discovery-only and never manufactures data."""
from scripts.probe_sch_orchid_2017_raw_access import (
    DATA_DOI, DOI_ID, EXPECTED_ARCHIVE, values_any, file_names, file_id, is_source_excel,
)

def test_source_doi_and_url_are_frozen():
    assert DATA_DOI=="10.5061/dryad.28n72"
    assert DOI_ID=="doi%3A10.5061%2Fdryad.28n72"

def test_schema_extraction_accepts_metadata_but_not_html():
    synthetic={"_embedded":{"stash:versions":[{"id":123}],"stash:files":[
        {"id":456,"path":"source.xls"},{"id":457,"path":"Readme.docx"}]}}
    assert values_any(synthetic,"versions")[0]["id"]==123
    assert len(values_any(synthetic,"files"))==2
    assert file_names(values_any(synthetic,"files")[0])=="source.xls"
    assert is_source_excel(b"<html>unauthorized</html>") is False
    assert is_source_excel(bytes.fromhex("d0cf11e0a1b11ae1")+b"0"*20)
    assert is_source_excel(b"PK\x03\x04"+b"0"*20)

def test_original_repository_source_files_are_exactly_pinned():
    assert len(EXPECTED_ARCHIVE)==2
    xls=next((k,v) for k,v in EXPECTED_ARCHIVE.items() if k.endswith(".xls"))
    assert xls[1]==(772608,"2a0429adade12ddce60ba9e46500f4a9")
    doc=next((k,v) for k,v in EXPECTED_ARCHIVE.items() if k.endswith(".docx"))
    assert doc[1]==(103526,"e773115ab4eaab2b75c83f6ffb260239")
    assert file_id({"_links":{"self":{"href":"https://datadryad.org/api/v2/files/19534"}}})=="19534"
