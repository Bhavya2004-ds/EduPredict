import streamlit as st

def show():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>About EduPredict</h1>
        <p>AI-powered student performance analytics for educational excellence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Overview section
    st.markdown('<p class="section-header">What is EduPredict?</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <p>EduPredict is an innovative educational analytics platform that uses machine learning to predict student performance and identify those at risk of academic failure. Our goal is to empower educators with data-driven insights to improve student outcomes and ensure no student is left behind.</p>
        <p>By analyzing various factors such as study habits, attendance, demographics, and historical performance, EduPredict provides actionable insights that help educators make informed decisions about intervention strategies and resource allocation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown('<p class="section-header">Key Features</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>AI-Powered Predictions</h4>
            <ul style="text-align: left;">
                <li>Advanced machine learning algorithms</li>
                <li>Accurate performance forecasting</li>
                <li>Risk level classification</li>
                <li>Real-time analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <h4>Interactive Dashboard</h4>
            <ul style="text-align: left;">
                <li>Real-time performance metrics</li>
                <li>Visual analytics and charts</li>
                <li>Trend analysis</li>
                <li>Executive summaries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>Advanced Analytics</h4>
            <ul style="text-align: left;">
                <li>Statistical analysis</li>
                <li>Correlation studies</li>
                <li>Demographic insights</li>
                <li>Performance distribution analysis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
            <h4>Actionable Reports</h4>
            <ul style="text-align: left;">
                <li>At-risk student identification</li>
                <li>Intervention recommendations</li>
                <li>Downloadable reports</li>
                <li>Progress tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown('<p class="section-header">How It Works</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>1. Upload Data</h4>
            <p>Upload your student CSV file with academic and demographic information</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
            <h4>2. AI Analysis</h4>
            <p>Our machine learning model analyzes the data and makes predictions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>3. View Insights</h4>
            <p>Explore interactive dashboards and detailed analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;"></div>
            <h4>4. Take Action</h4>
            <p>Implement targeted interventions based on recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data requirements section
    st.markdown('<p class="section-header">Data Requirements</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>Required Columns</h4>
            <ul style="text-align: left;">
                <li><strong>Student_ID:</strong> Unique identifier</li>
                <li><strong>Age:</strong> Student age (16-20)</li>
                <li><strong>Gender:</strong> Male/Female</li>
                <li><strong>Study_Hours_per_Week:</strong> Weekly study hours</li>
                <li><strong>Attendance_Rate:</strong> Attendance percentage (0-100)</li>
                <li><strong>Previous_Grade:</strong> Previous academic grade (A/B/C/D)</li>
                <li><strong>Parental_Education_Level:</strong> Parent education level</li>
                <li><strong>Internet_Access_at_Home:</strong> Yes/No</li>
                <li><strong>Extracurricular_Activities:</strong> Yes/No</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>Data Quality Tips</h4>
            <ul style="text-align: left;">
                <li>Ensure data is clean and complete</li>
                <li>Use consistent formatting</li>
                <li>Remove duplicate entries</li>
                <li>Validate data ranges</li>
                <li>Check for missing values</li>
            </ul>
            <h4>Supported Formats</h4>
            <ul style="text-align: left;">
                <li>CSV files (.csv)</li>
                <li>UTF-8 encoding recommended</li>
                <li>Header row required</li>
                <li>Maximum 10,000 rows</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Risk levels explanation
    st.markdown('<p class="section-header">Risk Level Classifications</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="info-card danger-card">
            <div style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">🔴</div>
            <h4>High Risk</h4>
            <p><strong>Score: < 40%</strong></p>
            <p>Immediate intervention required. Students need urgent support.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card warning-card">
            <div style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">🟡</div>
            <h4>Moderate Risk</h4>
            <p><strong>Score: 40-50%</strong></p>
            <p>Additional support recommended. Monitor closely.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card success-card">
            <div style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">🟢</div>
            <h4>Low Risk</h4>
            <p><strong>Score: 50-70%</strong></p>
            <p>On track for success. Continue current strategies.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="info-card" style="background: linear-gradient(135deg, #8b5cf6, #a855f7); color: white;">
            <div style="text-align: center; font-size: 2rem; margin-bottom: 1rem;">🌟</div>
            <h4>Excellent</h4>
            <p><strong>Score: 70%+</strong></p>
            <p>Outstanding performance. Consider advanced opportunities.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical information
    st.markdown('<p class="section-header">Technical Information</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>Machine Learning Model</h4>
            <ul style="text-align: left;">
                <li><strong>Algorithm:</strong> Ensemble Methods</li>
                <li><strong>Features:</strong> 9+ student attributes</li>
                <li><strong>Training Data:</strong> Historical student records</li>
                <li><strong>Accuracy:</strong> 85%+ prediction accuracy</li>
                <li><strong>Validation:</strong> Cross-validated performance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>Technology Stack</h4>
            <ul style="text-align: left;">
                <li><strong>Frontend:</strong> Streamlit</li>
                <li><strong>Backend:</strong> Python</li>
                <li><strong>ML Library:</strong> Scikit-learn</li>
                <li><strong>Data Processing:</strong> Pandas, NumPy</li>
                <li><strong>Visualization:</strong> Plotly, Matplotlib</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Privacy and security
    st.markdown('<p class="section-header">Privacy & Security</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>Data Protection</h4>
        <p>We take data privacy seriously and implement the following measures:</p>
        <ul style="text-align: left; margin-left: 2rem;">
            <li><strong>Local Processing:</strong> All data is processed locally in your browser</li>
            <li><strong>No Data Storage:</strong> We don't store or transmit your data to external servers</li>
            <li><strong>Session-Based:</strong> Data is only retained during your current session</li>
            <li><strong>Anonymization:</strong> Consider removing or anonymizing sensitive identifiers</li>
            <li><strong>Compliance:</strong> Designed with FERPA and GDPR principles in mind</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Support section
    st.markdown('<p class="section-header">Support & Resources</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>Getting Started</h4>
            <ol style="text-align: left; margin-left: 1rem;">
                <li>Prepare your student data in CSV format</li>
                <li>Navigate to "Upload & Analyze" page</li>
                <li>Upload your file or try sample data</li>
                <li>Explore the dashboard and analytics</li>
                <li>Download reports and take action</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>Best Practices</h4>
            <ul style="text-align: left; margin-left: 1rem;">
                <li>Regularly update student data</li>
                <li>Focus on high-risk students first</li>
                <li>Use insights for intervention planning</li>
                <li>Monitor trends over time</li>
                <li>Combine with teacher observations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #666;">
        <h3>EduPredict</h3>
        <p>Empowering educators with AI-driven insights for student success</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">
            Built with ❤️ for educators who care about every student's journey
        </p>
        <p style="font-size: 0.8rem; color: #888;">
            © 2024 EduPredict. Made with Streamlit and Python.
        </p>
    </div>
    """, unsafe_allow_html=True)