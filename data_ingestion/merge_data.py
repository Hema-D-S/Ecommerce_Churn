import pandas as pd
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

CLEANED_SALES_FILE = "data/cleaned_sales.csv"
CLEANED_PRODUCT_FILE = "data/cleaned_products.csv"
OUTPUT_FILE = "data/merged_sales_products.csv"
CHUNK_SIZE = 500_000  # Adjust as per your RAM

def merge_sales_product():
    if not os.path.exists(CLEANED_SALES_FILE):
        logging.error(f"Cleaned sales file not found: {CLEANED_SALES_FILE}")
        return
    if not os.path.exists(CLEANED_PRODUCT_FILE):
        logging.error(f"Cleaned product file not found: {CLEANED_PRODUCT_FILE}")
        return

    # Load entire cleaned product data into memory (usually smaller than sales)
    product_df = pd.read_csv(CLEANED_PRODUCT_FILE)
    logging.info(f"Loaded cleaned product data: {product_df.shape}")

    # Remove output file if exists
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        logging.info(f"Removed existing merged file: {OUTPUT_FILE}")

    chunk_count = 0
    try:
        # Process sales in chunks
        with pd.read_csv(CLEANED_SALES_FILE, chunksize=CHUNK_SIZE) as sales_reader:
            for sales_chunk in sales_reader:
                chunk_count += 1
                # Merge sales chunk with product data on product_id (left join keeps all sales)
                merged_chunk = pd.merge(
                    sales_chunk,
                    product_df,
                    on='product_id',
                    how='left',
                    suffixes=('_sale', '_prod')
                )

                # Log if any sales rows have missing product info
                missing_products = merged_chunk['product_name'].isnull().sum()
                if missing_products > 0:
                    logging.warning(f"Chunk {chunk_count}: {missing_products} sales rows have missing product info")

                # Append merged chunk to output file
                merged_chunk.to_csv(
                    OUTPUT_FILE,
                    mode='a',
                    index=False,
                    header=not os.path.exists(OUTPUT_FILE)
                )
                logging.info(f"Chunk {chunk_count} merged and saved, rows: {merged_chunk.shape[0]}")

    except Exception as e:
        logging.error(f"Error during merging: {e}")
        return

    logging.info(f"✅ Merging complete. Output saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_sales_product()
