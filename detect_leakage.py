import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

print("✅ Loading engineered features...")
df = pd.read_csv("feature_engineering/engineered_features.csv")

# Separate features and target
X = df.drop(columns=["churned"], errors='ignore')
y = df["churned"]

# Check if target accidentally exists in features
if "churned" in X.columns:
    print("❌ Leakage Detected: 'churned' is still in feature columns!")
    X = X.drop(columns=["churned"])

# Quick check: Correlation of features to target
print("\n✅ Top 5 features most correlated to churned:")
correlations = df.corr(numeric_only=True)["churned"].abs().sort_values(ascending=False)
print(correlations[1:6])  # Skip 'churned' itself

# Quick model to test suspiciously high AUC
print("\n✅ Training small leakage-check model...")
X_sample, _, y_sample, _ = train_test_split(X, y, test_size=0.8, random_state=42)

model = RandomForestClassifier(n_estimators=50, random_state=0, n_jobs=-1)
model.fit(X_sample, y_sample)
preds = model.predict_proba(X_sample)[:, 1]

auc = roc_auc_score(y_sample, preds)
print(f"\n🚨 AUC on small sample: {auc:.4f}")

if auc >= 0.98:
    print("⚠️ WARNING: AUC is extremely high. This could indicate data leakage.")
else:
    print("✅ AUC is reasonable. Leakage less likely.")

