from datetime import date
import pytest
from dataset_prototype.embedding_study.short_history import ShortObservation,views,summary_values,capabilities


def test_single_observation_keeps_scale_without_inventing_development():
    a=views([ShortObservation(2.,date(2020,1,1),'1')]);b=views([ShortObservation(200.,date(2020,1,1),'2')])
    assert a['normalized_allocation']==b['normalized_allocation']==(1.,)
    assert summary_values(a)==(2.,) and summary_values(b)==(200.,)
    assert a['change_between_observed_increments'] is None and a['sidecar']['date_gap_days'] is None
    assert capabilities(1)['observed_allocation_shape']=='NOT_APPLICABLE'
    assert capabilities(1)['physical_extinction']=='UNKNOWN'


def test_gappy_pair_retains_values_order_support_and_scale():
    a=views([ShortObservation(6.,date(2020,1,5),'9'),ShortObservation(2.,date(2020,1,1),'4')])
    assert summary_values(a)==(2.,6.) and a['sidecar']['date_gap_days']==4
    assert a['normalized_allocation']==(.25,.75)
    assert a['sidecar']['source_refs']==('4','9')
    assert a['change_between_observed_increments']==4.
    b=views([ShortObservation(20.,date(2020,1,1),'5'),ShortObservation(60.,date(2020,1,5),'10')])
    assert a['normalized_allocation']==b['normalized_allocation'] and a['observed_total']!=b['observed_total']


def test_observed_zero_does_not_become_missing_or_defined_shape():
    a=views([ShortObservation(0.,date(2020,1,1),'1')]);assert a['native']==(0.,) and a['observed_total']==0.
    assert a['normalized_allocation'] is None and not a['normalization_defined']


@pytest.mark.parametrize('value',[-1.,float('nan'),float('inf'),True])
def test_invalid_values_fail_without_repairs(value):
    with pytest.raises(ValueError):views([ShortObservation(value,date(2020,1,1),'1')])


def test_duplicate_dates_and_unsupported_lengths_rejected():
    obs=ShortObservation(1.,date(2020,1,1),'1')
    for records in [[],[obs,obs],[obs,obs,obs]]:
        with pytest.raises(ValueError):views(records)
