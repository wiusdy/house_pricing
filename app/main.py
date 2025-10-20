from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="House Price Estimation API")
app.include_router(router)