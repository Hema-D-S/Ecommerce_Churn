# modeling/evaluate_model.py

import pandas as pd
import joblib
from sklearn.metrics import classification_report, roc_auc_score

def evaluate_model(X_test_file='data/test.csv',
                   y_test_file='data/y_test.csv',
                   model_file='models/churn_model.pkl'):

    print("✅ 60% - Loading test features and labels...")
    X_test = pd.read_csv(X_test_file)
    
    # 🧼 Remove leakage-prone columns
    X_test = X_test.drop(columns=['last_purchase_gap', 'recency'], errors='ignore')

    y_test = pd.read_csv(y_test_file).values.ravel()  # Ensure it's 1D

    print("✅ 65% - Loading trained model...")
    model = joblib.load(model_file)

    print("✅ 70% - Generating predictions...")
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("✅ 80% - Evaluation Metrics:")
    print(classification_report(y_test, y_pred))
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

    print("✅ 100% - Evaluation complete.\n")

if __name__ == "__main__":
    evaluate_model()
