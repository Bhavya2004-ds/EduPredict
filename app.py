import streamlit as st
import sys
from pathlib import Path

# Add the current directory to the Python path
sys.path.append(str(Path(__file__).parent))

from modules import dashboard, upload_data, analytics, about, login, signup
from utils.styles import load_css

# Page configuration
st.set_page_config(
    page_title="EduPredict - Student Performance Analytics",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# Initialize session state
if 'page' not in st.session_state:
    if st.session_state.get('logged_in', False):
        st.session_state.page = 'Dashboard'
    else:
        st.session_state.page = 'Auth'

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h1 style="color: #3B82F6; margin: 0;">EduPredict</h1>
        <p style="color: #666; margin: 0.5rem 0 2rem 0; font-style: italic;">
            Empowering educators with data-driven insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user is logged in
    is_logged_in = st.session_state.get('logged_in', False)
    
    if not is_logged_in:
        st.markdown("### Welcome to EduPredict")
        st.markdown("Please sign in or create an account to access the analytics platform.")
        
        if st.button("About EduPredict", key="About", use_container_width=True):
            st.session_state.page = 'About'
    else:
        # Show main navigation for logged in users
        pages = {
            "Dashboard": "Dashboard",
            "Upload & Analyze": "Upload",
            "Advanced Analytics": "Analytics", 
            "About": "About"
        }
        
        
        for display_name, page_key in pages.items():
            if st.button(display_name, key=page_key, use_container_width=True):
                st.session_state.page = page_key
    
    st.markdown("---")
    
    # Quick stats if data exists
    if 'df' in st.session_state and st.session_state.df is not None:
        st.markdown("### Quick Stats")
        df = st.session_state.df
        st.metric("Total Students", len(df))
        if 'Predicted_Score' in df.columns:
            at_risk = len(df[df['Predicted_Score'] < 50])
            st.metric("At-Risk Students", at_risk)
            avg_score = round(df['Predicted_Score'].mean(), 1)
            st.metric("Avg Score", f"{avg_score}%")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; font-size: 12px;">
        <p>Built with care for educators</p>
        <p>© 2024 EduPredict</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
if st.session_state.page == 'Auth':
    # Show login/signup tabs directly in app.py
    st.markdown("""
    <div class="main-header">
        <h1>EduPredict</h1>
        <p>Student Performance Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/Signup tabs
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        login.show()
    
    with tab2:
        signup.show()
        
elif st.session_state.page == 'Dashboard':
    if st.session_state.get('logged_in', False):
        dashboard.show()
    else:
        st.session_state.page = 'Auth'
        st.rerun()
elif st.session_state.page == 'Upload':
    if st.session_state.get('logged_in', False):
        upload_data.show()
    else:
        st.session_state.page = 'Auth'
        st.rerun()
elif st.session_state.page == 'Analytics':
    if st.session_state.get('logged_in', False):
        analytics.show()
    else:
        st.session_state.page = 'Auth'
        st.rerun()
elif st.session_state.page == 'About':
    about.show()