import sqlite3
import pandas as pd

# Path to your CSV
csv_path = "/home/shigilsasi/code/Guvi_Projects/client_query_management_system/synthetic_client_queries.csv"

# Read CSV
df = pd.read_csv(csv_path)

# Ensure mobile numbers are string
df['client_mobile'] = df['client_mobile'].astype(str)

# Format dates
df['date_raised'] = pd.to_datetime(df['date_raised']).dt.strftime("%Y-%m-%d %H:%M:%S")
df['date_closed'] = pd.to_datetime(df['date_closed'], errors='coerce').dt.strftime("%Y-%m-%d %H:%M:%S")

conn = sqlite3.connect("database.db")
c = conn.cursor()

for _, row in df.iterrows():
    c.execute("""
        INSERT OR IGNORE INTO queries(
            query_id, client_id, email, mobile_number, query_heading, query_description, status, query_created_time, query_closed_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['query_id'],
        None,  # No client_id for historical data
        row['client_email'],
        row['client_mobile'],
        row['query_heading'],
        row['query_description'],
        row['status'],
        row['date_raised'],
        row['date_closed']
    ))

conn.commit()
conn.close()
print("Historical CSV data imported successfully!")
