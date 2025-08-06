import pandas as pd

def apply_decision_checks(rfm_df, features_df):
    print("[4/4] Running decision checks...")

    # Remove top 1% outliers in monetary value
    upper_limit = rfm_df['monetary'].quantile(0.99)
    rfm_df = rfm_df[rfm_df['monetary'] <= upper_limit]

    # Remove negative or zero monetary values
    rfm_df = rfm_df[rfm_df['monetary'] > 0]

    # Merge validated data
    merged_df = rfm_df.merge(features_df, on='customer_id', how='inner')

    print("[✅] Decision checks completed (75%)\n")
    return merged_df
