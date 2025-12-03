import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Queries Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS queries (
    query_id TEXT PRIMARY KEY,
    client_id INTEGER,
    email TEXT NOT NULL,
    mobile_number TEXT NOT NULL,
    query_heading TEXT NOT NULL,
    query_description TEXT NOT NULL,
    status TEXT DEFAULT "Open",
    query_created_time TEXT,
    query_closed_time TEXT,
    FOREIGN KEY(client_id) REFERENCES users(userid)
)
""")

conn.commit()
conn.close()
print("Database setup completed.")
