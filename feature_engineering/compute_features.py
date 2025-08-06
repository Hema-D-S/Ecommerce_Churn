import pandas as pd

def compute_additional_features(input_csv: str):
    print("[3/4] Computing additional features...")
    df = pd.read_csv(input_csv, parse_dates=["order_date"])

    df.sort_values(['customer_id', 'order_date'], inplace=True)
    purchase_gaps = df.groupby('customer_id')['order_date'].diff().dt.days
    avg_purchase_interval = purchase_gaps.groupby(df['customer_id']).mean().fillna(0).reset_index(name='avg_purchase_interval')

    last_purchase_gap = df.groupby('customer_id')['order_date'].max().reset_index()
    snapshot_date = df['order_date'].max() + pd.Timedelta(days=1)
    last_purchase_gap['last_purchase_gap'] = (snapshot_date - last_purchase_gap['order_date']).dt.days

    features_df = avg_purchase_interval.merge(
        last_purchase_gap[['customer_id', 'last_purchase_gap']],
        on='customer_id'
    )

    print("[✅] Feature engineering completed (50%)\n")
    return features_df
