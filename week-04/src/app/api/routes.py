from fastapi import APIRouter
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.predictor import predict

router = APIRouter()

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/predict", response_model=PredictionResponse)
def predict_text(request: PredictionRequest) -> PredictionResponse:
    intent, confidence = predict(request.text)
    return PredictionResponse(intent=intent, confidence=confidence)