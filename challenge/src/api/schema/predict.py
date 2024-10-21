from pydantic import BaseModel
from typing import List, Any
    
class Flights(BaseModel):
    OPERA : str
    TIPOVUELO: str
    MES: int

class ModelInput(BaseModel):
    flights : List[Flights]