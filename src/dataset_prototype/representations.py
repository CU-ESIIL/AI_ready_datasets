"""Local modality-specific scalar encoders with explicit preprocessing."""
from .contracts import HarmonizedObservation, Representation, digest
from .harmonization import authorize


ENCODERS = {"scalar": ("identity-scalar", "1", "none; scientific units retained"),
            "squared": ("scalar-and-square", "1", "append square; no scaling")}


def run(observations, encoder="scalar"):
    if encoder not in ENCODERS:
        raise ValueError("unknown encoder")
    name, version, preprocessing = ENCODERS[encoder]
    for observation in observations:
        if not isinstance(observation, HarmonizedObservation):
            raise TypeError("representation requires HarmonizedObservation")
        observation = HarmonizedObservation.model_validate(observation.model_dump(mode="json"))
        p = observation.provenance
        authorize(p.recipe, p.context_sources or (p.source, *p.related_sources), p.human, p.parent_lineage)
        if observation.value is None:
            raise ValueError("encoder requires a nonmissing value; handle missingness in recipe")
        if observation.observation_id != digest(observation.model_dump(mode="json", exclude={"observation_id"})):
            raise ValueError("observation identity does not match scientific content and lineage")
        vector = (observation.value,) if encoder == "scalar" else (observation.value, observation.value ** 2)
        fields = dict(observation_ids=(observation.observation_id,), modality=observation.modality, vector=vector,
                      encoder=name, encoder_version=version, preprocessing=preprocessing, dimensionality=len(vector),
                      track=observation.track, provenance=(p,))
        yield Representation(representation_id=digest({"observation": observation.observation_id, "encoder": name, "version": version}), **fields)


def batches(observations, size=64):
    if size < 1:
        raise ValueError("batch size must be positive")
    batch = []
    for observation in observations:
        batch.append(observation)
        if len(batch) == size:
            yield tuple(batch)
            batch = []
    if batch:
        yield tuple(batch)
