import streamlit as st
import hashlib
import json
from pathlib import Path

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def load_users():
    """Load users from JSON file"""
    users_file = Path("users.json")
    if users_file.exists():
        with open(users_file, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def show():
    st.markdown("""
    <div class="auth-header" style="text-align: center; margin-bottom: 2rem;">
        <h2>Sign In to Your Account</h2>
        <p>Access your EduPredict dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if already logged in
    if st.session_state.get('logged_in', False):
        st.success(f"Welcome back, {st.session_state.get('username', 'User')}!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Go to Dashboard", use_container_width=True):
                st.session_state.page = 'Dashboard'
                st.rerun()
        
        st.markdown("---")
        if st.button("Logout", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.success("Logged out successfully!")
            st.rerun()
        
        return
    
    # Login form
    with st.form("login_form"):
        st.markdown("### Enter Your Credentials")
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("Sign In", use_container_width=True)
        # No need for navigation button since we're using tabs
        
        if login_button:
            if username and password:
                users = load_users()
                hashed_password = hash_password(password)
                
                if username in users and users[username]['password'] == hashed_password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_data = users[username]
                    st.success("Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please fill in all fields")
    
    # Demo credentials info
    st.markdown("""
    <div class="demo-info">
        <h4>Demo Account</h4>
        <p>
            <strong>Username:</strong> demo<br>
            <strong>Password:</strong> demo123
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features preview
    st.markdown("""
    <div class="features-preview">
        <h4>What you'll get access to:</h4>
        <div class="features-grid">
            <div class="feature-item">
                <h5>Dashboard</h5>
                <p>Real-time analytics and KPIs</p>
            </div>
            <div class="feature-item">
                <h5>Analytics</h5>
                <p>Advanced data insights</p>
            </div>
            <div class="feature-item">
                <h5>Data Upload</h5>
                <p>Import and analyze student data</p>
            </div>
            <div class="feature-item">
                <h5>Reports</h5>
                <p>Generate detailed reports</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)