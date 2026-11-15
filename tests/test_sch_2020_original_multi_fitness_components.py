"""Original archived 572-row multi-fitness audit, no false component promotion."""
from copy import deepcopy
import pytest
from scripts.audit_sch_2020_original_multi_fitness_components import (
    STUDY_FIELDS,source_id_check,qualifies,audit_groups,
)

def template():
    r={
       "row.id":"1","Paper ID":"3","species":"Original x","authors":"Author",
       "pub.year":"2005","within.study.id":"1",
       "generic.year":"2005","generic.spp":"1","generic.population":"2",
       "generic.trait":"1","generic.sex":"female","generic.treatment":"control",
       "agent.selection.defined":"Light",
       "treatment.defined":"Control","experimental.context":"A",
       "trait.name":"original-shared-trait","trait.class":"PH",
       "generic.fitness.measure":"F","fitness.measure.defined":"number sexual structures",
       "fitness.component":"F",
       "grad.linear.value":0.8,"grad.linear.se":.1,
    }
    return r

def test_two_distinct_fitness_endpoints_same_source_key_are_found():
    a=template();b=deepcopy(a)
    b["row.id"]="2"
    b["generic.fitness.measure"]="P"
    b["fitness.measure.defined"]="number asexual cups"
    b["fitness.component"]="P"
    b["grad.linear.value"]=-.3
    b["grad.linear.se"]=.09
    x=audit_groups([a,b],STUDY_FIELDS)
    assert x["n_source_strata_with_two_or_more_fitness_codes"]==1
    assert x["n_naive_distinct_measure_row_pairs"]==1
    assert x["n_original_papers_with_multiple_outcomes_matched"]==1
    assert x["n_source_outcome_pair_point_opposite_beta"]==1
    assert x["n_source_outcome_pair_both_arm_nominal_nonzero_opposite_beta"]==1
    assert x["cross_component_conflict_identified"] is False
    assert x["source_author_fitted_component_difference_recovered"] is False

def test_fitness_code_and_label_not_replaced_by_duplicate_row():
    a=template();b=deepcopy(a);b["row.id"]="2"
    assert not qualifies(a,b)
    x=audit_groups([a,b],STUDY_FIELDS)
    assert x["n_naive_distinct_measure_row_pairs"]==0
    assert x["n_source_strata_with_two_or_more_fitness_codes"]==0

def test_strict_original_within_study_id_stratum_never_adds_pairs():
    a=template();b=deepcopy(a)
    b["row.id"]="2"
    b["generic.fitness.measure"]="P"
    b["fitness.measure.defined"]="asexual"
    b["within.study.id"]="2"
    broad=audit_groups([a,b],STUDY_FIELDS)
    strict=audit_groups([a,b],STUDY_FIELDS+("within.study.id",))
    assert broad["n_naive_distinct_measure_row_pairs"]==1
    assert strict["n_naive_distinct_measure_row_pairs"]==0

def test_missing_original_and_untrusted_data_cannot_be_promoted():
    with pytest.raises(ValueError,match="572"):
        source_id_check([template()])
