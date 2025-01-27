import streamlit as st
import pandas as pd

# In-memory "user database"
users = {}

# Session state to track logged-in user
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# Load the Excel file
def load_data():
    file_path = "Cost Index.xlsx"
    xl = pd.ExcelFile(file_path)
    data = {}
    
    # Load all sheets into a dictionary of dataframes
    for sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        df = df.dropna(how="all")  # Remove completely empty rows
        data[sheet_name] = df
    
    return data

def search_data(query, data):
    results = []
    query = query.lower()
    
    for sheet_name, df in data.items():
        matching_rows = df[df.astype(str).apply(lambda row: row.str.lower().str.contains(query, na=False)).any(axis=1)]
        if not matching_rows.empty:
            matching_rows.insert(0, "Category", sheet_name)  # Add category info
            results.append(matching_rows)
    
    return results

# Function to display the login/signup page
def login_signup_page():
    st.title("IA Construction")

    # Tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_btn"):
            if email in users and users[email] == password:
                st.session_state["user_email"] = email
                st.success("Logged in successfully!")
            else:
                st.error("Invalid email or password")

    with tab2:
        st.subheader("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input(
            "Confirm Password", type="password", key="confirm_password"
        )
        if st.button("Sign Up", key="signup_btn"):
            if email in users:
                st.error("Email already exists")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                users[email] = password
                st.session_state["user_email"] = email
                st.success("Account created successfully!")

# Function to display the home page
def home_page():
    st.title("Welcome to IA Construction")
    st.write(f"Logged in as: {st.session_state['user_email']}")
    query = st.text_input("Search for a price...")
    if st.button("Search"):
        if query:
            data = load_data()
            results = search_data(query, data)
            if results:
                for df in results:
                    st.write(df)
            else:
                st.error("No matching results found.")
        else:
            st.error("Please enter a search query.")
    if st.button("Logout"):
        st.session_state["user_email"] = None
        st.success("Logged out successfully!")

# App logic
if st.session_state["user_email"]:
    home_page()
else:
    login_signup_page()