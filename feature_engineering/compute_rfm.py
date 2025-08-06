import pandas as pd

def compute_rfm(input_csv: str, cutoff_date: str):
    print("[1/4] Loading raw customer data...")
    df = pd.read_csv(input_csv, parse_dates=["order_date"])
    print(f"   Loaded {len(df)} rows.")

    # Convert cutoff_date string to datetime
    cutoff_date = pd.to_datetime(cutoff_date)

    print(f"[2/4] Filtering data before cutoff date ({cutoff_date.date()})...")
    df = df[df["order_date"] < cutoff_date]
    print(f"   Remaining rows after cutoff: {len(df)}")

    if df.empty:
        raise ValueError("No data available before the cutoff date!")

    print("[3/4] Computing RFM metrics...")
    snapshot_date = cutoff_date
    rfm_df = df.groupby('customer_id').agg({
        'order_date': lambda x: (snapshot_date - x.max()).days,   # Recency
        'order_id': 'count',                                       # Frequency
        'total_spent': 'sum'                                       # Monetary
    }).reset_index()

    rfm_df.columns = ['customer_id', 'recency', 'frequency', 'monetary']
    print("[✅] RFM computation completed (25%)\n")

    return rfm_df
