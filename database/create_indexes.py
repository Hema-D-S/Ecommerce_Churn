import sqlite3
import logging
import time
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

DB_PATH = "data/ecommerce_churn.db"  # ✅ Make sure this matches the actual filename
TABLE_NAME = "sales_data"
INDEXES = [
    ("idx_customer_id", "customer_id"),
    ("idx_total_orders", "total_orders"),
    ("idx_total_spent", "total_spent"),
]

def create_indexes():
    if not os.path.exists(DB_PATH):
        logging.error(f"Database file '{DB_PATH}' not found.")
        return

    logging.info("🔌 Connecting to SQLite database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}'")
        if not cursor.fetchone():
            logging.error(f"❌ Table '{TABLE_NAME}' not found in database.")
            return

        logging.info(f"⚙️ Starting to create {len(INDEXES)} indexes on '{TABLE_NAME}'...")

        for i, (index_name, column_name) in enumerate(INDEXES, 1):
            logging.info(f"🧱 [{i}/{len(INDEXES)}] Creating index '{index_name}' on column '{column_name}'...")
            try:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {TABLE_NAME} ({column_name})")
                conn.commit()
                percent = round((i / len(INDEXES)) * 100)
                logging.info(f"✅ Index '{index_name}' created successfully. [{percent}% done]")
            except sqlite3.Error as e:
                logging.warning(f"⚠️ Skipped creating index '{index_name}': {e}")

        logging.info("🏁 All indexes created.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_indexes()
