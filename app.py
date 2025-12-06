import streamlit as st
import sqlite3
import pandas as pd
from modules import auth, client, support

st.set_page_config(page_title="Client Query Management System", layout="wide")

# -----------------------------
# PAGE STATE CONTROLLER
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "user" not in st.session_state:
    st.session_state.user = None


# -----------------------------
# LOGIN PAGE
# -----------------------------
def login_page():
    st.title("Client Query Management System")
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = auth.login_user(username, password)
        if user:
            st.session_state.user = user
            st.session_state.page = "dashboard"
            st.rerun()  
        else:
            st.error("Invalid username or password.")

    st.write("---")
    if st.button("Register"):
        st.session_state.page = "register"
        st.rerun()  

# -----------------------------
# REGISTRATION PAGE
# -----------------------------
def register_page():
    st.title("Register")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        if auth.register_user(username, password):
            st.success("Registered successfully! Ask admin to assign role.")
            st.session_state.page = "login"
            st.rerun()  
        else:
            st.error("Username already exists.")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()  

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
def dashboard_page():
    user = st.session_state.user
    role = user["role"]
    user_id = user["user_id"]

    st.sidebar.subheader(f"Logged in as: **{role}**")

    if st.sidebar.button("Logout 🔒"):
        st.session_state.clear()
        st.rerun() 

    # ========== ADMIN DASHBOARD ==========
    if role == "admin":
        st.subheader("Admin Dashboard")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT userid, username, role FROM users")
        users = c.fetchall()
        conn.close()

        df_users = pd.DataFrame(users, columns=["ID", "Username", "Role"])
        df_users["ID"] = df_users.index + 1

        st.write("All Users:")
        st.dataframe(df_users)

        st.write("Assign Role to User")
        user_to_update = st.text_input("Username to Update Role")
        new_role = st.selectbox("Select Role", ["admin", "client", "support"])

        if st.button("Update Role"):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("UPDATE users SET role=? WHERE username=?", (new_role, user_to_update))
            conn.commit()
            conn.close()
            st.success(f"{user_to_update} updated to {new_role}")
            st.rerun()  

        st.write("All Queries:")
        queries = support.get_all_queries()
        df_queries = pd.DataFrame(queries, columns=[
            "Query ID", "Client ID", "Email",
            "Mobile Number", "Query Heading",
            "Query Description", "Status",
            "Created Time", "Closed Time"
        ])

        # Normalize status values
        df_queries['Status'] = df_queries['Status'].replace({"Opened": "Open"})


        df_queries_display = df_queries.drop(columns=["Client ID"])
        st.dataframe(df_queries_display)

        # --------- Admin Charts ----------
        st.write("---")
        st.subheader("📊 Analytics")

        if not df_users.empty:
            st.write("### Users by Role")
            st.bar_chart(df_users['Role'].value_counts())

        if not df_queries.empty:
            st.write("### Queries by Status")
            st.bar_chart(df_queries['Status'].value_counts())

            st.write("### Queries by Heading")
            st.bar_chart(df_queries['Query Heading'].value_counts())

            st.write("### Query Trend Over Time")
            df_queries['Created Time'] = pd.to_datetime(
                df_queries['Created Time'], errors='coerce'
            )
            time_counts = df_queries.groupby(df_queries['Created Time'].dt.date).size()
            st.line_chart(time_counts)

    # ========== CLIENT DASHBOARD ==========
    elif role == "client":
        st.subheader("Submit New Query")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        heading = st.text_input("Query Heading")
        description = st.text_area("Query Description")

        if st.button("Submit Query"):
            if email and mobile and heading and description:
                client.submit_query(user_id, email, mobile, heading, description)
                st.success("Query submitted successfully!")
                st.rerun()  
            else:
                st.warning("Please fill all fields.")

        st.subheader("My Queries")
        queries = client.get_my_queries(user_id)
        df_my_queries = pd.DataFrame(queries, columns=[
            "Query ID", "Client ID", "Email",
            "Mobile Number", "Query Heading",
            "Query Description", "Status",
            "Created Time", "Closed Time"
        ])
        st.dataframe(df_my_queries)

    # ========== SUPPORT DASHBOARD ==========
    elif role == "support":
        st.subheader("Support Dashboard")

        queries = support.get_all_queries()
        df_queries = pd.DataFrame(queries, columns=[
            "Query ID", "Client ID", "Email",
            "Mobile Number", "Query Heading",
            "Query Description", "Status",
            "Created Time", "Closed Time"
        ])

        # Normalize status values
        df_queries['Status'] = df_queries['Status'].replace({"Opened": "Open"})


        df_queries_display = df_queries.drop(columns=["Client ID"])
        st.dataframe(df_queries_display)

        st.write("---")
        st.subheader("Update Query Status")

        query_id = st.text_input("Enter Query ID")
        new_status = st.selectbox("Select Status", ["Open", "Pending", "Closed"])

        if st.button("Update Status"):
            if query_id.strip() != "":
                support.update_query_status(query_id, new_status)
                st.success("Status updated successfully!")
                st.rerun()  
            else:
                st.warning("Enter a Query ID.")

        st.write("---")
        st.subheader("📊 Query Analytics Dashboard")

        if not df_queries.empty:
            st.write("### Queries by Status")
            st.bar_chart(df_queries['Status'].value_counts())

            st.write("### Query Distribution by Heading")
            st.bar_chart(df_queries['Query Heading'].value_counts())

            st.write("### Query Trend Over Time")
            df_queries['Created Time'] = pd.to_datetime(
                df_queries['Created Time'], errors='coerce'
            )
            time_counts = df_queries.groupby(df_queries['Created Time'].dt.date).size()
            st.line_chart(time_counts)


# -----------------------------
# PAGE ROUTING
# -----------------------------
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "dashboard":
    dashboard_page()
