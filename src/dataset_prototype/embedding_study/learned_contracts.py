"""Closed prefix-prediction recipe and explicit synthetic/real evidence boundary."""
from datetime import date,datetime
from typing import Literal
import math
from pydantic import Field,model_validator
from ..contracts import Contract

class PrefixInput(Contract):
    version: Literal['fire-prefix-v1']='fire-prefix-v1'
    fire_id: str
    source_version: str
    synthetic: bool
    source_observation_ids: tuple[str,...]
    dates: tuple[date,...] = Field(min_length=3,max_length=12)
    available_at: tuple[datetime,...]
    issued_at: datetime
    growth_km2_day: tuple[float,...]
    @model_validator(mode='after')
    def support(self):
        n=len(self.dates)
        if not all(len(x)==n for x in (self.source_observation_ids,self.available_at,self.growth_km2_day)):raise ValueError('prefix shape')
        if len(set(self.source_observation_ids))!=n:raise ValueError('duplicate observation ID')
        if any((b-a).days!=1 for a,b in zip(self.dates,self.dates[1:])):raise ValueError('daily support required; no gap imputation')
        if self.issued_at.utcoffset() is None or any(t.utcoffset() is None or t>self.issued_at or t.date()<d for t,d in zip(self.available_at,self.dates)):raise ValueError('availability must be evidenced by issue time')
        if any(not math.isfinite(g) or g<0 for g in self.growth_km2_day):raise ValueError('finite nonnegative evidenced growth')
        return self

class PrefixOutcome(Contract):
    """Private independent subsequent observation, never an encoder input."""
    fire_id: str
    date: date
    observation_id: str
    growth_km2_day: float = Field(ge=0,allow_inf_nan=False)
    available_at: datetime

class RealPrefixApproval(Contract):
    """Input evidence contract only; never executes a source read or grants approval."""
    source_version: str
    source_checksums: dict[str,str]
    rights_evidence: str
    attribution: str
    support_recipe_digest: str
    availability_evidence: str
    human_decision_reference: str
    approved: bool = False
