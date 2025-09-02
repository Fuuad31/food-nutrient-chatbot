# database.py

import sqlite3

def init_db():
    """Membuat tabel messages jika belum ada."""
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            session_id TEXT,
            role TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_message_to_db(session_id, role, content):
    """Menyimpan satu pesan ke dalam database."""
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                   (session_id, role, content))
    conn.commit()
    conn.close()