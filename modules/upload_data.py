import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from utils.data_processing import (
    preprocess_data, load_model, make_predictions, 
    highlight_risk_score, create_sample_data, categorize_risk_level
)

def show():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>Upload & Analyze Student Data</h1>
        <p>Upload your student dataset to get instant performance predictions and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Instructions section
    with st.expander("Data Upload Instructions", expanded=False):
        st.markdown("""
        ### Required CSV Format
        Your CSV file should contain the following columns:
        
        **Required Columns:**
        - `Student_ID`: Unique identifier for each student
        - `Age`: Student age
        - `Gender`: Male/Female
        - `Study_Hours_per_Week`: Hours spent studying per week
        - `Attendance_Rate`: Attendance percentage (0-100)
        - `Previous_Grade`: Previous academic grade (A/B/C/D)
        - `Parental_Education_Level`: Parent education level
        - `Internet_Access_at_Home`: Yes/No
        - `Extracurricular_Activities`: Yes/No
        
        **Optional Columns:**
        - `Family_Income_Level`: Low/Medium/High
        - Any other demographic or academic data
        
        **Tip:** Make sure your data is clean and contains no missing values for best results.
        """)
    
    # File upload section
    st.markdown('<p class="section-header">File Upload</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            help="Upload a CSV file containing student data"
        )
        
        # Sample data option
        if st.button("Use Sample Data for Demo", use_container_width=True):
            sample_df = create_sample_data()
            st.session_state.uploaded_df = sample_df
            st.success("Sample data loaded! Scroll down to see the analysis.")
            uploaded_file = "sample"  # Trigger processing
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>What You'll Get</h4>
            <ul style="text-align: left; margin-left: 1rem;">
                <li>Predicted exam scores</li>
                <li>Risk level classification</li>
                <li>Visual analytics</li>
                <li>At-risk student list</li>
                <li>Downloadable reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Process uploaded file
    if uploaded_file:
        try:
            # Load data
            if uploaded_file == "sample":
                df = st.session_state.uploaded_df
                st.info("Using sample data for demonstration")
            else:
                with st.spinner("Reading your data..."):
                    df = pd.read_csv(uploaded_file)
            
            # Display data info
            st.markdown('<p class="section-header">Data Overview</p>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                missing_values = df.isnull().sum().sum()
                st.metric("Missing Values", missing_values)
            
            # Show data preview
            with st.expander("Preview Data", expanded=False):
                st.dataframe(df.head(), use_container_width=True)
            
            # Data preprocessing and prediction
            with st.spinner("Analyzing data and making predictions..."):
                try:
                    # Preprocess data
                    df_processed = preprocess_data(df.copy())
                    
                    # Load model
                    model = load_model()
                    if model is None:
                        st.error("Could not load the prediction model. Please ensure 'model.pkl' is available.")
                        return
                    
                    # Make predictions
                    predictions = make_predictions(df_processed, model)
                    
                    # Add predictions to original dataframe
                    df['Predicted_Score'] = predictions
                    df['Risk_Level'] = df['Predicted_Score'].apply(lambda x: categorize_risk_level(x)[0])
                    df['Risk_Icon'] = df['Predicted_Score'].apply(lambda x: categorize_risk_level(x)[1])
                    
                    # Store in session state
                    st.session_state.df = df
                    
                    st.success("Analysis complete! Here are your results:")
                    
                except Exception as e:
                    st.error(f"Error during prediction: {str(e)}")
                    st.info("Please check that your data format matches the requirements.")
                    return
            
            # Results section
            st.markdown('<p class="section-header">Prediction Results</p>', unsafe_allow_html=True)
            
            # Key metrics
            total_students = len(df)
            high_risk = len(df[df['Predicted_Score'] < 40])
            moderate_risk = len(df[(df['Predicted_Score'] >= 40) & (df['Predicted_Score'] < 50)])
            low_risk = len(df[(df['Predicted_Score'] >= 50) & (df['Predicted_Score'] < 70)])
            excellent = len(df[df['Predicted_Score'] >= 70])
            avg_score = round(df['Predicted_Score'].mean(), 2)
            
            # Metrics display
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{total_students}</div>
                    <div class="metric-label">Total Students</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: #ef4444;">{high_risk}</div>
                    <div class="metric-label">High Risk (< 40)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: #f59e0b;">{moderate_risk}</div>
                    <div class="metric-label">Moderate Risk (40-50)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color: #10b981;">{low_risk + excellent}</div>
                    <div class="metric-label">Good Performance (50+)</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_score}%</div>
                    <div class="metric-label">Average Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Visualizations
            st.markdown('<p class="section-header">Score Distribution</p>', unsafe_allow_html=True)
            
            # Score distribution chart
            fig = px.histogram(
                df, 
                x='Predicted_Score', 
                nbins=25,
                title='Distribution of Predicted Exam Scores',
                color_discrete_sequence=['#2E86AB'],
                labels={'Predicted_Score': 'Predicted Score', 'count': 'Number of Students'}
            )
            
            # Add threshold lines
            fig.add_vline(x=40, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
            fig.add_vline(x=50, line_dash="dash", line_color="orange", annotation_text="Moderate Risk Threshold")
            fig.add_vline(x=70, line_dash="dash", line_color="green", annotation_text="Excellence Threshold")
            
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_family="Inter",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Results tables
            st.markdown('<p class="section-header">Detailed Results</p>', unsafe_allow_html=True)
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["All Students", "At-Risk Students", "Top Performers"])
            
            with tab1:
                st.markdown("#### All Student Predictions")
                display_df = df[['Student_ID', 'Predicted_Score', 'Risk_Level', 'Risk_Icon']].copy()
                display_df.columns = ['Student ID', 'Predicted Score', 'Risk Level', '']
                
                # Apply styling
                styled_df = display_df.style.applymap(
                    highlight_risk_score, 
                    subset=['Predicted Score']
                ).format({'Predicted Score': '{:.1f}%'})
                
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            with tab2:
                at_risk_students = df[df['Predicted_Score'] < 50].copy()
                if len(at_risk_students) > 0:
                    st.markdown(f"#### {len(at_risk_students)} Students Need Additional Support")
                    
                    display_df = at_risk_students[['Student_ID', 'Predicted_Score', 'Risk_Level']].copy()
                    display_df.columns = ['Student ID', 'Predicted Score', 'Risk Level']
                    display_df = display_df.sort_values('Predicted Score')
                    
                    styled_df = display_df.style.applymap(
                        highlight_risk_score, 
                        subset=['Predicted Score']
                    ).format({'Predicted Score': '{:.1f}%'})
                    
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                    
                    # Download button for at-risk students
                    csv = at_risk_students.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download At-Risk Students Report",
                        data=csv,
                        file_name="at_risk_students.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.success("Great news! No students are predicted to be at risk.")
            
            with tab3:
                top_performers = df[df['Predicted_Score'] >= 70].copy()
                if len(top_performers) > 0:
                    st.markdown(f"#### {len(top_performers)} Top Performing Students")
                    
                    display_df = top_performers[['Student_ID', 'Predicted_Score', 'Risk_Level']].copy()
                    display_df.columns = ['Student ID', 'Predicted Score', 'Risk Level']
                    display_df = display_df.sort_values('Predicted Score', ascending=False)
                    
                    styled_df = display_df.style.applymap(
                        highlight_risk_score, 
                        subset=['Predicted Score']
                    ).format({'Predicted Score': '{:.1f}%'})
                    
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No students are predicted to achieve excellence level (70%+) yet.")
            
            # Action recommendations
            st.markdown('<p class="section-header">Recommended Actions</p>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if high_risk > 0:
                    st.markdown(f"""
                    <div class="info-card danger-card">
                        <h4>Immediate Action Required</h4>
                        <p><strong>{high_risk}</strong> students are at high risk of failing.</p>
                        <ul style="text-align: left; margin-left: 1rem;">
                            <li>Schedule one-on-one meetings</li>
                            <li>Provide additional tutoring</li>
                            <li>Contact parents/guardians</li>
                            <li>Consider modified learning plans</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="info-card success-card">
                        <h4>No High-Risk Students</h4>
                        <p>Excellent! Your current teaching strategies are working well.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if moderate_risk > 0:
                    st.markdown(f"""
                    <div class="info-card warning-card">
                        <h4>Monitor Closely</h4>
                        <p><strong>{moderate_risk}</strong> students need extra support.</p>
                        <ul style="text-align: left; margin-left: 1rem;">
                            <li>Increase study group participation</li>
                            <li>Provide practice materials</li>
                            <li>Regular progress check-ins</li>
                            <li>Peer mentoring programs</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="info-card success-card">
                        <h4>Strong Performance</h4>
                        <p>Most students are on track for success!</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            st.info("Please check your file format and try again.")
    
    else:
        # Show helpful information when no file is uploaded
        st.markdown("""
        <div class="info-card">
            <h3>Ready to Get Started?</h3>
            <p>Upload your student data CSV file above to:</p>
            <ul style="text-align: left; margin-left: 2rem;">
                <li>Get instant performance predictions</li>
                <li>Identify at-risk students</li>
                <li>Visualize score distributions</li>
                <li>Generate actionable reports</li>
                <li>Download results for further analysis</li>
            </ul>
            <p style="margin-top: 1rem;"><strong>Don't have data?</strong> Click the "Use Sample Data" button to see how it works!</p>
        </div>
        """, unsafe_allow_html=True)