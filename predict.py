import pickle
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

from fastapi import FastAPI
import uvicorn

model_path = './models/pipeline.bin'

class InputData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    country: Literal['TR', 'DE', 'NL', 'FR', 'PL', 'RO', 'ES', 'US', 'GB', 'IT']
    bin_country: Literal['GB', 'DE', 'NL', 'FR', 'PL', 'RO', 'ES', 'US', 'TR', 'IT']
    channel: Literal['web', 'app']
    merchant_category: Literal['fashion', 'travel', 'grocery', 'gaming', 'electronics']
    promo_used: Literal[0, 1]
    avs_match: Literal[0, 1]
    cvv_result: Literal[0, 1]
    three_ds_flag: Literal[0, 1]
    night_hours: Literal[0, 1]
    account_age_days: int = Field(..., ge=0)
    total_transactions_user: int = Field(..., ge=0)
    avg_amount_user: float = Field(..., ge=0.0)
    amount: float = Field(..., ge=0.0)
    shipping_distance_km: float = Field(..., ge=0.0)
    month: int = Field(..., ge=0)
    day: int = Field(..., ge=0)
    hour: int = Field(..., ge=0)

class PredictResponse(BaseModel):
    fraud_probability: float
    is_fraud: bool

app = FastAPI(title="prediction")

with open(model_path, 'rb') as f_in:
    pipeline = pickle.load(f_in)

def predict_single(input_data):
    result = pipeline.predict_proba(input_data)[0, 1]
    return float(result)

@app.post("/predict")
def predict(input_data: InputData) -> PredictResponse:
    prob = predict_single(input_data.model_dump())

    return PredictResponse(
        fraud_probability=prob,
        is_fraud=prob >= 0.4
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9696)