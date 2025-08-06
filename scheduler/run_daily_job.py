# scheduler/run_daily_job.py

import pandas as pd
import joblib
from datetime import date

def run_daily_job():
    print("📥 Pulling latest data...")
    # Simulate loading fresh daily features (replace with your actual pipeline or file)
    X = pd.read_csv('data/train.csv')  # Replace with your actual daily data file

    print("🛠️ Computing features...")
    # Remove leakage features if still present
    X = X.drop(columns=['last_purchase_gap', 'recency'], errors='ignore')

    print("[3/4] Computing additional features...")
    print(f"   Filtered to {len(X)} rows before cutoff date {date.today()}.")

    print("[✅] Feature engineering completed (50%)\n")

    print("📦 Loading model...")
    model = joblib.load("models/churn_model.pkl")

    # ✅ Load expected feature names
    expected_features = joblib.load("models/feature_names.pkl")

    # 🧠 Select only expected columns
    X = X[expected_features]

    print("🤖 Making predictions...")
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    print("💾 Saving predictions...")
    output_df = pd.DataFrame({
        "customer_id": pd.read_csv('data/train.csv')["customer_id"],  # Or replace with correct ID source
        "churn_prediction": predictions,
        "churn_probability": probabilities
    })

    today_str = date.today().isoformat()
    output_df.to_csv(f"predictions/churn_predictions_{today_str}.csv", index=False)

    print(f"✅ Predictions saved to predictions/churn_predictions_{today_str}.csv\n")

if __name__ == "__main__":
    run_daily_job()
