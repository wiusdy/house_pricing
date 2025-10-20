from pydantic import BaseModel

class HouseInput(BaseModel):
    bedrooms: int
    bathrooms: float
    sqft_living: int
    sqft_lot: int
    floors: float
    sqft_above: int
    sqft_basement: int
    zipcode: str

class PredictionResponse(BaseModel):
    prediction: float
    model_version: str
    elapsed_time: float