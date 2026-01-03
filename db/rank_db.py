# db/rank_db.py
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "rank.db"

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_rank (
        user_id TEXT,
        username TEXT,
        date TEXT,
        tries INTEGER,
        finished INTEGER,
        PRIMARY KEY (user_id, date)
    )
    """)
    conn.commit()

def save_rank(user_id, username, date, tries, finished):
    cur.execute("""
    INSERT OR REPLACE INTO daily_rank
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, date, tries, finished))
    conn.commit()

def get_rank_by_date(date):
    cur.execute("""
    SELECT username, tries, finished
    FROM daily_rank
    WHERE date = ?
    ORDER BY finished DESC, tries ASC
    """, (date,))
    return cur.fetchall()

def has_played_today(user_id, date):
    cur.execute("""
    SELECT 1 FROM daily_rank
    WHERE user_id = ? AND date = ?
    """, (user_id, date))
    return cur.fetchone() is not None

