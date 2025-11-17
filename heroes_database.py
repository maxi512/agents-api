import csv
import sqlite3
from pathlib import Path

CSV_PATH = Path(__file__).parent / "heroes.csv"
DB_PATH = Path(__file__).parent / "heroes.db"

def init_database():
    """Initialize the database with heroes from CSV file."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS heroes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                alias TEXT,
                universe TEXT NOT NULL
            )
        """)
        
        cursor.execute("DELETE FROM heroes")
        
        with open(CSV_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            heroes = []
            for idx, row in enumerate(reader, start=1):
                heroes.append((
                    idx,
                    row['name'],
                    row.get('real name') or None,
                    row['universe']
                ))
            
            cursor.executemany(
                "INSERT INTO heroes (id, name, alias, universe) VALUES (?, ?, ?, ?)",
                heroes
            )
            
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM heroes")
            count = cursor.fetchone()[0]
            print(f"Loaded {count} heroes from CSV to database")
    finally:
        conn.close()
