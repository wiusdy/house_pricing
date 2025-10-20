import pandas as pd
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_endpoint():
    df = pd.read_csv("/home/wiusdy/PhData/house_price_estimation/data/future_unseen_examples.csv", dtype={"zipcode": str})
    demographics = pd.read_csv("/home/wiusdy/PhData/house_price_estimation/data/zipcode_demographics.csv", dtype={"zipcode": str})
    
    # Filtra apenas zipcodes presentes nos dados demográficos
    df = df[df["zipcode"].isin(demographics["zipcode"])].reset_index(drop=True)

    first_example = df.iloc[0].to_dict()

    payload = {
        "bedrooms": int(first_example["bedrooms"]),
        "bathrooms": float(first_example["bathrooms"]),
        "sqft_living": int(first_example["sqft_living"]),
        "sqft_lot": int(first_example["sqft_lot"]),
        "floors": float(first_example["floors"]),
        "sqft_above": int(first_example["sqft_above"]),
        "sqft_basement": int(first_example["sqft_basement"]),
        "zipcode": str(first_example["zipcode"])
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()