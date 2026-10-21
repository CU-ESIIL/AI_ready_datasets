import pytest
from pydantic import ValidationError
from dataset_prototype.harmonization import run as harmonize
from dataset_prototype.representations import run, batches
from dataset_prototype.contracts import Representation
from dataset_prototype.provenance import export


def test_stream_batch_and_lineage(bundle):
    r,m,p,raw=bundle
    observations=tuple(harmonize((r,),p,raw))
    first=tuple(run(iter(observations)))
    assert first==tuple(run(observations))
    assert [x.vector for x in first]==[(2.,),(4.,),(6.,)]
    assert all(x.encoder_version=='1' and x.preprocessing for x in first)
    assert all(x.dimensionality==1 for x in first)
    for obs,rep in zip(observations,first):
        assert rep.observation_ids==(obs.observation_id,)
        assert rep.provenance[0].source==r
        assert rep.provenance[0].qa.outcome=='approve'
    batched=tuple(x for batch in batches(observations,2) for x in run(batch))
    assert batched==first
    second=tuple(run(observations,'squared'))
    assert second[0].vector==(2,4) and second[0].representation_id!=first[0].representation_id
    graph=export(first)
    assert len(graph['@graph'])>=5
    assert 'prov' in graph['@context']


def test_malformed_and_missing(bundle):
    r,m,p,raw=bundle
    observations=tuple(harmonize((r,),p,raw))
    with pytest.raises(TypeError): tuple(run([{}]))
    with pytest.raises(ValueError,match='nonmissing'): tuple(run([observations[0].model_copy(update={'value':None})]))
    with pytest.raises(ValueError,match='unknown encoder'): tuple(run(observations,'unknown'))
    rep=next(run(observations)).model_dump(); rep['dimensionality']=4
    with pytest.raises(ValidationError): Representation.model_validate(rep)
    with pytest.raises(ValueError): tuple(batches(observations,0))
    assert tuple(run([]))==()


def test_modified_value_cannot_retain_old_observation_identity(bundle):
    r,m,p,raw=bundle
    observation=next(harmonize((r,),p,raw))
    with pytest.raises(ValueError,match='identity'):
        tuple(run((observation.model_copy(update={'value':99}),)))
