import sqlite3
import datetime

def get_all_queries():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM queries")
    rows = c.fetchall()
    conn.close()
    return rows

def update_query_status(query_id, status):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    closed_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status == 'Closed' else None
    c.execute("UPDATE queries SET status=?, query_closed_time=? WHERE query_id=?", (status, closed_time, query_id))
    conn.commit()
    conn.close()
