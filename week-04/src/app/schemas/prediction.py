from pydantic import BaseModel, Field, ConfigDict

class PredictionRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    text: str = Field(min_length=1, max_length = 500)

class PredictionResponse(BaseModel):
    intent: str
    confidence: float