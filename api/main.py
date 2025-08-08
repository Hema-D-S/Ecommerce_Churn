# api/main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import APIKeyHeader
import joblib
import pandas as pd
import numpy as np
import shap
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Customer Churn API")

# Load model and feature names
model = joblib.load("models/churn_model.pkl")
feature_names = joblib.load("models/feature_names.pkl")

# SHAP Explainer for tree-based model (Random Forest)
explainer = shap.TreeExplainer(model)

# API key header
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

# Root endpoint
@app.get("/", dependencies=[Depends(verify_api_key)])
def root():
    return {"message": "Churn Prediction API is running."}

# Predict endpoint
@app.post("/predict", dependencies=[Depends(verify_api_key)])
def predict_churn(payload: dict):
    try:
        df = pd.DataFrame([payload])

        # Reorder and filter columns
        df = df[feature_names]

        proba = model.predict_proba(df)[0][1]
        return {"churn_probability": round(float(proba), 4)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

# Explain endpoint
@app.post("/explain", dependencies=[Depends(verify_api_key)])
def explain_prediction(payload: dict):
    try:
        df = pd.DataFrame([payload])
        df = df[feature_names]

        # Get SHAP values
        shap_values = TreeExplainer(df)

        # For binary classification, shap_values is a 2D array [n_samples, n_features]
        # For some versions, it may return an object per sample, e.g., shap_values[0]
        # Use the first sample (assumes single prediction)
        if hasattr(shap_values, 'values'):
            # object-based output (recommended format)
            values = shap_values.values
            base_value = shap_values.base_values
            if isinstance(values, np.ndarray) and values.ndim == 2:
                values = values[0]
            if isinstance(base_value, np.ndarray) and base_value.ndim > 0:
                base_value = base_value[0]
        else:
            # fallback for older SHAP formats
            values = shap_values[0].values
            base_value = shap_values[0].base_values

        explanation = {
            "base_value": round(float(base_value), 4),
            "shap_values": {
                feature: round(float(shap_val), 4)
                for feature, shap_val in zip(feature_names, values)
            }
        }

        return explanation

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Explanation failed: {str(e)}")

