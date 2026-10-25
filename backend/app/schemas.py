from pydantic import BaseModel, Field
from typing import List

class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)

class Marker(BaseModel):
    text: str
    type: str
    explanation: str

class PredictionResponse(BaseModel):
    label: str
    confidence: float
    markers: List[Marker]
    explanation: str
    model: str
