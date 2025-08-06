# split_data.py
import pandas as pd
from sklearn.model_selection import train_test_split

# Load full feature-engineered dataset
df = pd.read_csv("feature_engineering/engineered_features.csv")

# Separate features and target
X = df.drop(columns=["churned"])
y = df["churned"]

# ✅ Check class distribution before splitting
print("🔎 Before split:")
print(y.value_counts(normalize=True))  # Shows ratio of 0s and 1s

# ✅ Perform stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ✅ Save splits
X_train.to_csv("data/train.csv", index=False)
X_test.to_csv("data/test.csv", index=False)
y_train.to_csv("data/y_train.csv", index=False)
y_test.to_csv("data/y_test.csv", index=False)

print("✅ Train/test split completed and saved.")
print("🔎 After split - y_train:")
print(y_train.value_counts(normalize=True))
