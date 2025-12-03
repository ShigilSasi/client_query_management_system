import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

users = [
    ("admin_user", "Admin@123", "admin"),
    ("client_user", "Client@123", "client"),
    ("support_user", "Support@123", "support")
]

conn = sqlite3.connect("database.db")
c = conn.cursor()

for username, password, role in users:
    c.execute("INSERT OR REPLACE INTO users (username, password, role) VALUES (?, ?, ?)",
              (username, hash_password(password), role))
    print(f"Added user: {username} ({role})")

conn.commit()
conn.close()
