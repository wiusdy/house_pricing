from fastapi import APIRouter
from app.models.data_models import HouseInput, PredictionResponse
from app.services.model_service import ModelService
from app.config.api_model_config import APIPredictConfig

router = APIRouter()

config = APIPredictConfig()
model_service = ModelService(config=config)

@router.post("/predict", response_model=PredictionResponse)
def predict_house_price(input_data: HouseInput):
    return model_service.predict(input_data)