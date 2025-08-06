import pandas as pd

def compute_rfm(input_csv: str):
    print("[1/4] Loading raw customer data...")
    df = pd.read_csv(input_csv, parse_dates=["order_date"])
    print(f"   Loaded {len(df)} rows.")

    print("[2/4] Computing RFM metrics...")
    snapshot_date = df['order_date'].max() + pd.Timedelta(days=1)
    rfm_df = df.groupby('customer_id').agg({
        'order_date': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'count',
        'total_spent': 'sum'
    }).reset_index()

    rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    print("[✅] RFM computation completed (25%)\n")

    return rfm_df
