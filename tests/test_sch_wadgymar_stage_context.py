"""Source-author hurdle model tests cannot be relabelled linear-beta interactions."""
from copy import deepcopy
from pathlib import Path
import pytest
from scripts.audit_sch_wadgymar_stage_context import META, STAGE, TOTAL, csv_rows, run

ROOT=Path(__file__).resolve().parents[1]

def result():
    return run(csv_rows(META),csv_rows(STAGE),csv_rows(TOTAL))

def test_two_stage_specific_author_direct_interactions():
    r=result()
    assert r['n_original_hurdle_stage_cells']==6
    assert r['n_applicable_interaction_cells']==5
    assert r['n_source_reported_p_lt_0_01_interactions']==2
    assert r['supported_trait_stage_pairs']==[['Biomass','SURVIVAL'],['Flowering onset','SEED_COUNT']]
    assert r['original_programmes']==1
    assert r['source_total_selection_and_hurdle_model_families_must_not_be_pooled']
    assert r['source_total_seed_coefficients_preserved']

@pytest.mark.parametrize('change', ['table3', 'source_model', 'table4', 'row_identity'])
def test_inconsistent_original_source_fails_closed(change):
    a=csv_rows(META);b=deepcopy(csv_rows(STAGE));c=deepcopy(csv_rows(TOTAL))
    if change=='table3': b[1]['interaction_chi2']='6.98'
    if change=='source_model': b[4]['source_link']='HURDLE_NEG_BIN_LOG'
    if change=='table4': c[0]['beta_heated']='-0.99'
    if change=='row_identity': c[1]['source_row_id_1']='777'
    with pytest.raises(ValueError): run(a,b,c)

def test_document_prevents_pseudometa_and_trait_optimism():
    s=(ROOT/'docs/SCH_WADGYMAR_STAGE_SPECIFIC_SELECTION_CONTEXT_V1.md').read_text(encoding='utf-8')
    for needle in ('6.99','6.77','137','独立','L','must not','原著'):
        assert needle.lower() in s.lower()
