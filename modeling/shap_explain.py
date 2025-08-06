# modeling/shap_explain.py

import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

def explain_model(X_test_file='data/test.csv', model_file='models/churn_model.pkl'):
    print("✅ 80% - Loading data and model...")

    # Load test data (limit for performance)
    df = pd.read_csv(X_test_file, nrows=1000)

    # Drop target column if present
    if 'churned' in df.columns:
        df = df.drop(columns=['churned'])

    # Load trained model
    model = joblib.load(model_file)

    print("✅ 85% - Creating SHAP explainer...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df)

    print("✅ 90% - Generating SHAP bar plot...")

    # Check the structure of shap_values
    if isinstance(shap_values, list):
        # If it's a list, use the second class (1)
        values_to_plot = shap_values[1]
    else:
        # If it's a single array, use it directly
        values_to_plot = shap_values

    plt.figure(figsize=(10, 6))
    shap.summary_plot(values_to_plot, df, plot_type="bar", show=True)

    print("✅ 100% - SHAP bar plot displayed.\n")

if __name__ == "__main__":
    explain_model()
