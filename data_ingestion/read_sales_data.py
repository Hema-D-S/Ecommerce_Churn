import os
import pandas as pd
import logging

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/data_ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Constants
SALES_CSV_PATH = r"C:\Users\user\Ecommerce_Churn\data\Sales.csv"
OUTPUT_CSV_PATH = r"C:\Users\user\Ecommerce_Churn\data\cleaned_sales.csv"
CHUNK_SIZE = 100_000
MAX_CHUNKS = 250  # Limit to 250 chunks (25 million rows approx)

def clean_chunk(df_chunk):
    # Drop unnamed columns
    df_chunk = df_chunk.loc[:, ~df_chunk.columns.str.contains('^Unnamed')]
    
    # Drop rows with missing order_id or product_id
    df_chunk.dropna(subset=["order_id", "product_id"], inplace=True)
    
    # Reset index
    df_chunk.reset_index(drop=True, inplace=True)
    
    return df_chunk

def read_sales_data():
    chunk_count = 0
    rows_total = 0

    # Delete old output file if it exists
    if os.path.exists(OUTPUT_CSV_PATH):
        os.remove(OUTPUT_CSV_PATH)

    logging.info(f"Starting to read Sales.csv in chunks from: {SALES_CSV_PATH}")
    
    try:
        for chunk in pd.read_csv(SALES_CSV_PATH, chunksize=CHUNK_SIZE):
            if chunk_count >= MAX_CHUNKS:
                break
            
            cleaned = clean_chunk(chunk)
            rows = cleaned.shape[0]
            rows_total += rows

            # Append to output CSV
            cleaned.to_csv(OUTPUT_CSV_PATH, mode='a', index=False, header=not os.path.exists(OUTPUT_CSV_PATH))

            chunk_count += 1
            percentage_done = (chunk_count / MAX_CHUNKS) * 100

            print(f"✅ Chunk {chunk_count}/{MAX_CHUNKS} processed ({percentage_done:.2f}%)")
            logging.info(f"Processed chunk {chunk_count}/{MAX_CHUNKS} - {rows} rows - {percentage_done:.2f}% done")

        logging.info(f"✅ Finished processing {chunk_count} chunks with {rows_total} total rows.")
        print(f"\n✅ Ingestion complete: {chunk_count} chunks, {rows_total} rows → saved to cleaned_sales.csv")

    except Exception as e:
        logging.error(f"❌ Error while reading sales data: {str(e)}")
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    read_sales_data()
