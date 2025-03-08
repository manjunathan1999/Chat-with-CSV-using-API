import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Chat with CSV",
    page_icon="📊",
    menu_items={},
    initial_sidebar_state="expanded"
)

# Hide Streamlit style elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session state
if 'token' not in st.session_state:
    st.session_state.token = None
if 'messages' not in st.session_state:
    st.session_state.messages = []

# API base URL
BASE_URL = "http://localhost:8000"

def login(username, password):
    response = requests.post(
        f"{BASE_URL}/login",
        json={"username": username, "password": password}
    )
    if response.status_code == 200:
        st.session_state.token = response.json()["access_token"]
        return True
    return False

def register(username, password):
    response = requests.post(
        f"{BASE_URL}/register",
        json={"username": username, "password": password}
    )
    return response.status_code == 200

# Authentication UI
if not st.session_state.token:
    st.title("Welcome to Chat CSV 📊")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                if login(username, password):
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            submit = st.form_submit_button("Register")
            if submit:
                if register(new_username, new_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Registration failed")

else:
    st.title("Chat with CSV 📊")
    
    # Sidebar for data operations
    st.sidebar.header("Data Operations")
    table_type = st.sidebar.selectbox("Select Table", ["table1", "table2"])
    
    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # Import Data Button
    if st.sidebar.button("Import Data"):
        with st.spinner("Importing data..."):
            response = requests.post(
                f"{BASE_URL}/execute-sql",
                json={"type": table_type},
                headers=headers
            )
            if response.status_code == 200:
                st.sidebar.success("Data imported successfully!")
            else:
                st.sidebar.error("Failed to import data")

    # Ingest Data Button
    if st.sidebar.button("Ingest Data"):
        with st.spinner("Ingesting data..."):
            response = requests.post(
                f"{BASE_URL}/ingest",
                json={"type": table_type},
                headers=headers
            )
            if response.status_code == 200:
                st.sidebar.success("Data ingested successfully!")
            else:
                st.sidebar.error("Failed to ingest data")

    # Logout Button
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.messages = []
        st.rerun()

    # Chat Interface
    st.header("Ask Questions About Your Data")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about your data"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = requests.post(
                    f"{BASE_URL}/query",
                    json={"question": prompt, "type": table_type},
                    headers=headers
                )
                if response.status_code == 200:
                    answer = response.json()
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.write(answer)
                else:
                    st.error("Failed to get response")

    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit • Powered by LangChain")
