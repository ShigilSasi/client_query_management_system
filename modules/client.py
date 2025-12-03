import sqlite3
import datetime

def submit_query(client_id, email, mobile_number, heading, description):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # Generate new query_id safely
    c.execute("SELECT query_id FROM queries")
    existing_ids = c.fetchall()
    max_id = max([int(q[0][1:]) for q in existing_ids if q[0].startswith('Q')], default=0)
    query_id = f"Q{max_id + 1:04d}"

    query_created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        INSERT INTO queries(query_id, client_id, email, mobile_number, query_heading, query_description, status, query_created_time)
        VALUES (?, ?, ?, ?, ?, ?, 'Open', ?)
    """, (query_id, client_id, email, mobile_number, heading, description, query_created_time))

    conn.commit()
    conn.close()

def get_my_queries(client_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM queries WHERE client_id=?", (client_id,))
    rows = c.fetchall()
    conn.close()
    return rows
