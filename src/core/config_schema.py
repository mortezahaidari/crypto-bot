# src/core/config_schema.py
from pydantic import BaseModel, Field
from typing import List, Dict

class ExchangeConfig(BaseModel):
    id: str
    api_key: str
    api_secret: str
    enabled: bool = True

class StrategyConfig(BaseModel):
    name: str
    params: Dict

class BotConfig(BaseModel):
    exchanges: List[ExchangeConfig]
    strategies: List[StrategyConfig]
    risk_params: Dict = Field(default_factory=dict)