import pandas as pd
import sqlite3
import os
import logging

# Constants
CSV_FILE = "data/merged_sales_products.csv"
DB_FILE = "data/ecommerce_churn.db"
TABLE_NAME = "sales_data"
CHUNK_SIZE = 100000

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def count_total_rows(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for line in f)
    return total_lines - 1  # excluding header

def load_data_chunked():
    if not os.path.exists(CSV_FILE):
        logging.error(f"❌ File not found: {CSV_FILE}")
        return

    total_rows = count_total_rows(CSV_FILE)
    inserted_rows = 0

    logging.info(f"📦 Total rows to insert: {total_rows}")
    logging.info("🔌 Connecting to SQLite database...")

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        logging.info(f"🧹 Dropping existing table `{TABLE_NAME}` if exists...")
        cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        conn.commit()

        # Load and insert data in chunks
        logging.info(f"🚀 Starting chunked insertion with chunk size {CHUNK_SIZE}...")

        for chunk_index, chunk in enumerate(pd.read_csv(CSV_FILE, chunksize=CHUNK_SIZE)):
            chunk.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
            inserted_rows += len(chunk)

            percent_done = (inserted_rows / total_rows) * 100
            logging.info(f"✅ Inserted chunk {chunk_index + 1} | {inserted_rows}/{total_rows} rows ({percent_done:.2f}%)")

        conn.commit()
        conn.close()
        logging.info("🎉 All data successfully inserted into the SQLite database.")

    except Exception as e:
        logging.exception("❌ Failed to load data into SQLite:", exc_info=e)

if __name__ == "__main__":
    load_data_chunked()
