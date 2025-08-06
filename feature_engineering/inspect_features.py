import pandas as pd

df = pd.read_csv("feature_engineering/engineered_features.csv")

print("📊 Distribution of 'last_purchase_gap':")
print(df["last_purchase_gap"].describe())

print("\n🔎 How many are <= 90 days (non-churned)?")
print((df["last_purchase_gap"] <= 580).sum())

print("\n🔎 How many are > 90 days (churned)?")
print((df["last_purchase_gap"] > 580).sum())

print("\n🧾 Churn Label Distribution:")
print(df["churned"].value_counts())
