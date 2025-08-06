import pandas as pd

def compute_additional_features(input_csv: str, cutoff_date: str):
    print("[3/4] Computing additional features...")

    # Load full data and parse dates
    df = pd.read_csv(input_csv, parse_dates=["order_date"])

    # Filter data to only include orders before the cutoff
    df = df[df['order_date'] < pd.to_datetime(cutoff_date)]
    print(f"   Filtered to {len(df)} rows before cutoff date {cutoff_date}.")

    # Sort by customer and order date
    df.sort_values(['customer_id', 'order_date'], inplace=True)

    # Calculate average purchase interval
    purchase_gaps = df.groupby('customer_id')['order_date'].diff().dt.days
    avg_purchase_interval = purchase_gaps.groupby(df['customer_id']).mean().fillna(0).reset_index(name='avg_purchase_interval')

    # Calculate days since last purchase (relative to cutoff_date)
    last_purchase_gap = df.groupby('customer_id')['order_date'].max().reset_index()
    cutoff_dt = pd.to_datetime(cutoff_date)
    last_purchase_gap['last_purchase_gap'] = (cutoff_dt - last_purchase_gap['order_date']).dt.days

    # Merge features
    features_df = avg_purchase_interval.merge(
        last_purchase_gap[['customer_id', 'last_purchase_gap']],
        on='customer_id'
    )

    print("[✅] Feature engineering completed (50%)\n")
    return features_df
