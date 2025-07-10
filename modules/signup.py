import streamlit as st
import hashlib
import json
from pathlib import Path
import re

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

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def show():
    st.markdown("""
    <div class="auth-header" style="text-align: center; margin-bottom: 2rem;">
        <h2>Create Your Account</h2>
        <p>Join EduPredict to unlock powerful analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Signup form
    with st.form("signup_form"):
        st.markdown("### Create Your Account")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="Enter your first name")
        with col2:
            last_name = st.text_input("Last Name", placeholder="Enter your last name")
        
        username = st.text_input("Username", placeholder="Choose a username")
        email = st.text_input("Email", placeholder="Enter your email address")
        
        col1, col2 = st.columns(2)
        with col1:
            password = st.text_input("Password", type="password", placeholder="Create a password")
        with col2:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
        
        # Role selection
        role = st.selectbox("Role", ["Teacher", "Administrator", "Analyst", "Other"])
        
        # Terms and conditions
        terms_accepted = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        col1, col2 = st.columns(2)
        with col1:
            signup_button = st.form_submit_button("Create Account", use_container_width=True)
        # No need for navigation button since we're using tabs
        
        if signup_button:
            # Validation
            if not all([first_name, last_name, username, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif not validate_email(email):
                st.error("Please enter a valid email address")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not terms_accepted:
                st.error("Please accept the Terms of Service and Privacy Policy")
            else:
                is_valid, message = validate_password(password)
                if not is_valid:
                    st.error(message)
                else:
                    users = load_users()
                    
                    # Check if username or email already exists
                    if username in users:
                        st.error("Username already exists")
                    elif any(user.get('email') == email for user in users.values()):
                        st.error("Email already registered")
                    else:
                        # Create new user
                        users[username] = {
                            'password': hash_password(password),
                            'email': email,
                            'first_name': first_name,
                            'last_name': last_name,
                            'role': role,
                            'created_at': str(st.session_state.get('current_time', 'now'))
                        }
                        
                        save_users(users)
                        st.success("Account created successfully! Please sign in.")
                        st.balloons()
                        
                        # Auto-login
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_data = users[username]
                        st.session_state.page = 'Dashboard'
                        st.rerun()
    
    # Password requirements
    st.markdown("""
    <div class="password-requirements">
        <h4>Password Requirements</h4>
        <ul>
            <li>At least 6 characters long</li>
            <li>Contains at least one letter</li>
            <li>Contains at least one number</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits of signing up
    st.markdown("""
    <div class="signup-benefits">
        <h4>Why Join EduPredict?</h4>
        <div class="benefits-grid">
            <div class="benefit-item">
                <h5>Advanced Analytics</h5>
                <p>Get deep insights into student performance and trends</p>
            </div>
            <div class="benefit-item">
                <h5>Easy Data Import</h5>
                <p>Upload CSV files and get instant predictions</p>
            </div>
            <div class="benefit-item">
                <h5>Interactive Dashboards</h5>
                <p>Visualize data with beautiful, interactive charts</p>
            </div>
            <div class="benefit-item">
                <h5>Risk Assessment</h5>
                <p>Identify at-risk students early for intervention</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)