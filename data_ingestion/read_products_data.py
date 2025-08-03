import pandas as pd
import os
import logging

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

INPUT_FILE = "data/products.csv"
OUTPUT_FILE = "data/cleaned_products.csv"
CHUNK_SIZE = 100_000

RELEVANT_COLUMNS = ['product_id', 'product_name', 'brand', 'category']


def clean_product_chunk(chunk):
    # Keep only relevant columns that are present
    present_cols = [col for col in RELEVANT_COLUMNS if col in chunk.columns]
    chunk = chunk[present_cols]

    # Drop rows with missing product_id or product_name
    chunk.dropna(subset=['product_id', 'product_name'], inplace=True)

    # Drop duplicate products (by product_id)
    chunk.drop_duplicates(subset=['product_id'], inplace=True)

    return chunk


def load_product_data():
    if not os.path.exists(INPUT_FILE):
        logging.error(f"Product file not found: {INPUT_FILE}")
        return

    total_size = os.path.getsize(INPUT_FILE)
    processed_size = 0
    chunk_count = 0

    # Remove old cleaned file if exists
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        logging.info(f"Removed existing file: {OUTPUT_FILE}")

    try:
        with pd.read_csv(INPUT_FILE, chunksize=CHUNK_SIZE) as reader:
            for chunk in reader:
                chunk_count += 1
                cleaned = clean_product_chunk(chunk)

                if cleaned.empty:
                    logging.info(f"Chunk {chunk_count} skipped (no valid data)")
                    continue

                # Append cleaned chunk
                cleaned.to_csv(
                    OUTPUT_FILE,
                    mode='a',
                    index=False,
                    header=not os.path.exists(OUTPUT_FILE)
                )

                # Estimate progress based on memory used
                processed_size += chunk.memory_usage(deep=True).sum()
                percent = (processed_size / total_size) * 100
                logging.info(f"Chunk {chunk_count} processed — ~{percent:.2f}% complete")

    except Exception as e:
        logging.error(f"Error during product data loading: {e}")
        return

    logging.info(f"✅ Product data cleaning complete: {OUTPUT_FILE}")


if __name__ == "__main__":
    load_product_data()
