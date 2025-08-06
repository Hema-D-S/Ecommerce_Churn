# modeling/train_model.py

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

def train_model(X_file='data/train.csv',
                y_file='data/y_train.csv',
                model_file='models/churn_model.pkl'):

    print("✅ 30% - Loading training features...")
    chunks = pd.read_csv(X_file, chunksize=50000)

    X_list = []
    for chunk in chunks:
        # 🧼 Remove known leakage columns
        chunk = chunk.drop(columns=['last_purchase_gap', 'recency'], errors='ignore')
        X_list.append(chunk)

    X = pd.concat(X_list)

    print("✅ 40% - Loading training labels...")
    y = pd.read_csv(y_file).values.ravel()

    print("✅ 55% - Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X, y)

    feature_names = X.columns.tolist()
    joblib.dump(feature_names, "models/feature_names.pkl")


    print("✅ 70% - Saving model...")
    joblib.dump(model, model_file)

    print("✅ 100% - Model training complete and saved!\n")

if __name__ == "__main__":
    train_model()
