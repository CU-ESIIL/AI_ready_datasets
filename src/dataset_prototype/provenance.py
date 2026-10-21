"""PROV-inspired JSON-LD 1.1 export; no graph service or network resolution."""
from .contracts import digest


def export(representations):
    graph = {}

    def ref(identifier):
        return {"@id": f"urn:sha256:{identifier}"}

    def source(resource):
        key = digest(resource)
        graph[key] = {**ref(key), "@type": "prov:Entity", "record": resource.model_dump(mode="json")}
        return ref(key)

    def observation(identifier, lineage):
        recipe_id = digest(lineage.recipe)
        inputs = [source(lineage.source), *(source(s) for s in lineage.related_sources)]
        parents = [ref(p) for p in lineage.parent_observations]
        graph[identifier] = {**ref(identifier), "@type": "prov:Entity", "prov:wasGeneratedBy": ref(recipe_id),
                             "prov:wasDerivedFrom": inputs + parents, "record": lineage.model_dump(mode="json")}
        previous = graph.get(recipe_id, {}).get("prov:used", [])
        used = {item["@id"]: item for item in previous + inputs + parents}
        graph[recipe_id] = {**ref(recipe_id), "@type": "prov:Activity", "prov:used": [used[k] for k in sorted(used)],
                            "record": lineage.recipe.model_dump(mode="json")}
        for parent_id, parent_lineage in zip(lineage.parent_observations, lineage.parent_lineage):
            observation(parent_id, parent_lineage)

    for rep in representations:
        graph[rep.representation_id] = {**ref(rep.representation_id), "@type": "prov:Entity",
            "prov:wasDerivedFrom": [ref(x) for x in rep.observation_ids], "record": rep.model_dump(mode="json")}
        for observation_id, lineage in zip(rep.observation_ids, rep.provenance):
            observation(observation_id, lineage)
    return {"@context": {"@version": 1.1, "prov": "http://www.w3.org/ns/prov#",
                         "record": {"@id": "https://cu-esiil.github.io/AI_ready_datasets/provenance#record", "@type": "@json"}},
            "@graph": [graph[k] for k in sorted(graph)]}
