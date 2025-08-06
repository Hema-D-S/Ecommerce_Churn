import pandas as pd
import joblib

def predict_churn():
    print("🔮 Predicting churn...")

    model = joblib.load("models/churn_model.pkl")
    df = pd.read_csv("data/test.csv")

    if 'churned' in df.columns:
        df = df.drop(columns=['churned'])
    if 'customer_id' in df.columns:
        customer_ids = df['customer_id']
        df = df.drop(columns=['customer_id'])

    predictions = model.predict(df)

    results = pd.DataFrame({
        'customer_id': customer_ids,
        'predicted_churn': predictions
    })

    results.to_csv("output/predictions.csv", index=False)
    print("✅ Predictions saved to output/predictions.csv")
