import sqlite3

def init_db():
    conn = sqlite3.connect("agent.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS github_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            token TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_github_credentials(username, token):
    conn = sqlite3.connect("agent.db")
    c = conn.cursor()
    c.execute("INSERT INTO github_auth (username, token) VALUES (?, ?)", (username, token))
    conn.commit()
    conn.close()

def get_github_credentials():
    conn = sqlite3.connect("agent.db")
    c = conn.cursor()
    c.execute("SELECT username, token FROM github_auth ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row if row else (None, None)
