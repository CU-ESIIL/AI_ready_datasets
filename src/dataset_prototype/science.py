"""A descriptive fixture comparison, never evidence of predictive performance."""
from statistics import correlation


def summarize(observations):
    groups = {}
    for o in observations:
        key = (o.longitude, o.latitude, o.datetime_start, o.datetime_end)
        groups.setdefault(key, {})[o.variable] = o.value
    pairs = [(x["canopy_height"], x["nir_reflectance"]) for x in groups.values() if x.get("canopy_height") is not None and x.get("nir_reflectance") is not None]
    return {"fixture_only": True, "method": "Pearson correlation for exact coincident synthetic field/satellite pairs; no support equivalence asserted",
            "pairs": len(pairs), "correlation": correlation(*zip(*pairs)) if len(pairs) >= 2 and len({a for a, b in pairs}) > 1 and len({b for a, b in pairs}) > 1 else None,
            "limitation": "Synthetic values and deliberately aligned supports; no ecological or food/water-security inference."}
