"""Bounded offline learning configuration; no model-authored operation selection."""
from typing import Literal
from pydantic import Field,model_validator
from ..contracts import Contract

class TrainingConfig(Contract):
    version: Literal['fire-prefix-training-v1']='fire-prefix-training-v1'
    mode: Literal['synthetic_control']='synthetic_control'
    generator_seed: int = Field(default=20261121,ge=0)
    train_fires: int = Field(default=128,ge=8,le=256)
    validation_fires: int = Field(default=48,ge=4,le=128)
    test_fires: int = Field(default=64,ge=4,le=128)
    depths: tuple[int,...] = (3,5,7,10)
    training_seeds: tuple[int,...] = (271,811,1729)
    epochs: int = Field(default=120,ge=1,le=300)
    learning_rate: float = Field(default=.01,gt=0,le=.1,allow_inf_nan=False)
    ridge_alpha: float = Field(default=1.,gt=0,allow_inf_nan=False)
    @model_validator(mode='after')
    def valid(self):
        if not self.depths or len(set(self.depths))!=len(self.depths) or any(d<3 or d>12 for d in self.depths):raise ValueError('bounded unique depth strata required')
        if not 1<=len(self.training_seeds)<=3 or len(set(self.training_seeds))!=len(self.training_seeds) or any(s<0 for s in self.training_seeds):raise ValueError('bounded unique initialization seeds required')
        return self
