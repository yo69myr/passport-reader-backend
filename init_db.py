import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        creation_date TEXT NOT NULL,
        subscription TEXT NOT NULL,
        token TEXT
    )
''')

conn.commit()
conn.close()
