# modeling/save_model_sqlite.py
import sqlite3

def register_model_to_db(model_path='models/churn_model.pkl',
                         db_path='data/database.sqlite'):
    print("✅ Registering model metadata to database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_registry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_path TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        INSERT INTO model_registry (model_path, status)
        VALUES (?, ?)
    ''', (model_path, 'active'))

    conn.commit()
    conn.close()
    print("✅ Model metadata saved.")

if __name__ == "__main__":
    register_model_to_db()
