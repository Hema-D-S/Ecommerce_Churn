import pandas as pd
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# File paths and settings
INPUT_FILE = "data/processed_sales.csv"
OUTPUT_FILE = "data/cleaned_sales.csv"
CHUNK_SIZE = 100_000

# Critical columns we care about
CRITICAL_COLS = ['order_id', 'customer_id', 'product_id', 'order_date', 'sales_value']


def clean_chunk(chunk):
    # Drop unnamed and mostly empty columns
    chunk = chunk.loc[:, ~chunk.columns.str.contains('^Unnamed')]
    chunk = chunk.dropna(axis=1, thresh=int(0.5 * len(chunk)))

    # Check which critical columns exist in this chunk
    present_critical_cols = [col for col in CRITICAL_COLS if col in chunk.columns]
    if not present_critical_cols:
        return pd.DataFrame()  # Skip chunk if it lacks all required columns

    # Drop rows with missing values in critical columns that are present
    chunk.dropna(subset=present_critical_cols, inplace=True)

    # Convert 'order_date' to datetime if it exists
    if 'order_date' in chunk.columns:
        chunk['order_date'] = pd.to_datetime(chunk['order_date'], errors='coerce')
        chunk.dropna(subset=['order_date'], inplace=True)

    # Remove rows with sales_value <= 0 if the column exists
    if 'sales_value' in chunk.columns:
        chunk = chunk[chunk['sales_value'] > 0]

    return chunk


def clean_sales_data():
    if not os.path.exists(INPUT_FILE):
        logging.error(f"Input file does not exist: {INPUT_FILE}")
        return

    total_size = os.path.getsize(INPUT_FILE)
    processed_size = 0

    # Remove output file if it exists from a previous run
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        logging.info(f"Removed existing output file: {OUTPUT_FILE}")

    chunk_count = 0

    try:
        with pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE) as reader:
            for chunk in reader:
                chunk_count += 1
                cleaned_chunk = clean_chunk(chunk)

                if cleaned_chunk.empty:
                    logging.info(f"Chunk {chunk_count} skipped (no valid data)")
                    continue

                cleaned_chunk.to_csv(
                    OUTPUT_FILE,
                    mode='a',
                    index=False,
                    header=not os.path.exists(OUTPUT_FILE)
                )

                processed_size += chunk.memory_usage(deep=True).sum()
                percent = (processed_size / total_size) * 100
                logging.info(f"Chunk {chunk_count} cleaned — ~{percent:.2f}% done")
    except Exception as e:
        logging.error(f"Error during chunk processing: {e}")
        return

    logging.info(f"✅ Cleaning completed. Output saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    clean_sales_data()
