from enum import Enum
from pydantic import BaseModel

class MyAction(str, Enum):
    ALLOW = "ALLOW"
    FLAG = "FLAG"
    REMOVE = "REMOVE"

class MyActionModel(BaseModel):
    # Match Swagger examples using {"name": "FLAG"}
    name: MyAction

class MyObservation(BaseModel):
    text: str
    toxicity_score: float
    level: str
    # Fields below are included to satisfy OpenEnv serializer expectations on reset
    reward: float = 0.0
    done: bool = False
    info: dict = {}