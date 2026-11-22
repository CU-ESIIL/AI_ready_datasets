"""Versioned multitask definitions and bounded synthetic-only experiment settings."""
from typing import Literal
from pydantic import Field,model_validator
from ..contracts import Contract

TASKS=('A','B','C','D')
DEFINITIONS={
 'A':'next calendar-day growth; regression log1p(km2/day)',
 'B':'sum of next three daily increments; regression log1p(km2)',
 'C':'mean of next three increments strictly exceeds mean of last three observed increments; binary; equality is false',
 'D':'population standard deviation (ddof=0) of next three daily increments; regression log1p(km2/day)',
 'E':'future next-three log1p-increment vector; top-10 outcome-distance relevance, not ecological analogs'}

class TransferConfig(Contract):
    version: Literal['fire-transfer-v1']='fire-transfer-v1'
    source_snapshot: str='reports/embedding_utility/fire_vase/results/milestone-4-learning-v1'
    scope: Literal['synthetic_only']='synthetic_only'
    horizon: Literal[3]=3
    epochs: int = Field(default=120,ge=1,le=200)
    seeds: tuple[int,...]=(271,811,1729)
    learning_rate: float=Field(default=.01,gt=0,le=.1,allow_inf_nan=False)
    ridge_alpha: float=Field(default=1.,gt=0,allow_inf_nan=False)
    bootstrap_replicates: int=Field(default=1000,ge=20,le=2000)
    bootstrap_seed: int=880031
    retrieval_k: Literal[10]=10
    @model_validator(mode='after')
    def bounds(self):
        if not 1<=len(self.seeds)<=3 or len(set(self.seeds))!=len(self.seeds) or any(s<0 for s in self.seeds):raise ValueError('unique bounded training seeds')
        return self
