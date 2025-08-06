# modeling/shap_explain.py

import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt

def explain_model(model_path="models/churn_model.pkl", data_path="data/test.csv"):
    print("✅ 80% - Loading data and model...")

    model = joblib.load(model_path)
    df = pd.read_csv(data_path, nrows=1000)

    # ✅ Only drop 'churned' if it exists
    if "churned" in df.columns:
        df = df.drop(columns=["churned"])

    print("✅ 85% - Creating SHAP explainer...")
    explainer = shap.Explainer(model, df)
    shap_values = explainer(df)

    print("✅ 90% - Generating SHAP summary plot...")
    shap.summary_plot(shap_values, df)

    print("✅ 100% - SHAP summary complete.\n")

if __name__ == "__main__":
    explain_model()
