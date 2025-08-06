import pandas as pd
import sqlite3

# Paths
csv_path = "feature_engineering/engineered_features.csv"
db_path = "data/ecommerce_churn.db"

# Load the CSV
features_df = pd.read_csv(csv_path)
total_rows = len(features_df)

# Connect to SQLite
conn = sqlite3.connect(db_path)

# Write to DB
features_df.to_sql("features", conn, if_exists="replace", index=False)

# Verify row count in DB
db_count = pd.read_sql_query("SELECT COUNT(*) AS row_count FROM features", conn).iloc[0]["row_count"]
conn.close()

# Calculate percentage
percent_written = (db_count / total_rows) * 100 if total_rows > 0 else 0

# Print status
print("✅ Engineered features written to DB.")
print(f"📊 Total rows in CSV: {total_rows}")
print(f"📥 Rows in DB table 'features': {db_count}")
print(f"✅ {percent_written:.2f}% of data successfully written to the database.")
