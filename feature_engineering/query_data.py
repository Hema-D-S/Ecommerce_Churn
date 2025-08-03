import sqlite3
import pandas as pd

def query_data_in_chunks(db_path: str, output_path: str, chunk_size: int = 100000):
    conn = sqlite3.connect(db_path)

    # SQL: aliasing for consistency with RFM scripts
    query = """
        SELECT 
            dim_customer_key AS customer_id,
            order_id,
            date_ AS order_date,
            unit_selling_price * procured_quantity AS total_spent
        FROM sales_data
    """

    try:
        chunks = pd.read_sql_query(query, conn, chunksize=chunk_size, parse_dates=["order_date"])
    except Exception as e:
        print("❌ Query failed. Check column names or expressions.")
        raise e

    first_chunk = True
    total_rows = 0

    for i, chunk in enumerate(chunks):
        chunk.dropna(subset=['customer_id', 'order_id', 'order_date', 'total_spent'], inplace=True)
        mode = 'w' if first_chunk else 'a'
        header = first_chunk

        chunk.to_csv(output_path, mode=mode, index=False, header=header)
        first_chunk = False
        total_rows += len(chunk)
        print(f"✅ Processed chunk {i+1} — Total rows written: {total_rows}")

    conn.close()
    print(f"\n🎯 Query complete. Final output saved to: {output_path}")

if __name__ == "__main__":
    query_data_in_chunks("data/ecommerce_churn.db", "feature_engineering/raw_customer_data.csv")
