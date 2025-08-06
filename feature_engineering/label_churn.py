import pandas as pd

def label_churn(merged_df, inactivity_threshold=580):
    print("[5/5] Labeling churn...")
    merged_df['churned'] = (merged_df['last_purchase_gap'] > inactivity_threshold).astype(int)
    print("[✅] Churn labeling completed (100%)\n")
    return merged_df

def save_features(final_df, output_file='feature_engineering/engineered_features.csv'):
    final_df.to_csv(output_file, index=False)
    print(f"[🎯] Engineered features saved to: {output_file}\n")
