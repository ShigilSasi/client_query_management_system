# Client Query Management System

A Streamlit-based web application that allows clients to submit queries, support staff to manage and resolve them, and admins to monitor user roles and system activity.  
Built with **Python, Streamlit, and SQLite**.

---

##  Features

### Admin
- View all users and queries
- Assign roles (admin, client, support)
- Analytics dashboard:  
  -  Queries by Status  
  -  Query distribution by heading  
  -  Query trend over time  
  -  Users by role

###  Client
- Register / login securely
- Submit queries with details
- View own submitted queries and their status

###  Support Team
- View all client queries
- Update status: `Open`, `Pending`, `Closed`
- Query analytics dashboard

---

##  Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| Data Handling | Pandas |

---

##  Project Structure

client_query_management_system/
│
├── app.py # Main Streamlit app
├── database.db # SQLite database
├── modules/
│ ├── auth.py # Login & authentication
│ ├── client.py # Client operations
│ ├── support.py # Support operations
│
├── db_setup.py # DB schema creation
├── add_sample_users.py # Default users
├── import_csv.py # Import synthetic query data
├── synthetic_client_queries.csv
└── README.md



##  Login Roles

| Username | Password | Role |
|----------|----------|------|
| admin_user | Admin@123 | admin |
| client_user | Client@123 | client |
| support_user | Support@123 | support |

*(Configured from `add_sample_users.py`)*

---

## Initialize the database (only first time)

python3 db_setup.py
python3 add_sample_users.py

python3 import_csv.py  # Load sample query history

## Run Streamlit App 

streamlit run app.py

## Open in browser:
http://localhost:8501

## Security

Passwords stored using SHA-256 hashing

Role-based restricted access (Admin/Client/Support)