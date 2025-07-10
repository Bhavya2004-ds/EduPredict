import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.data_processing import get_student_insights, categorize_risk_level

def show():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>Performance Dashboard</h1>
        <p>Real-time insights into student performance and risk assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data exists
    if 'df' not in st.session_state or st.session_state.df is None:
        st.markdown("""
        <div class="info-card warning-card">
            <h3>No Data Available</h3>
            <p>Please upload student data first to view the dashboard insights.</p>
            <p>Navigate to the <strong>"Upload & Analyze"</strong> page to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show sample dashboard with dummy data
        st.markdown("---")
        st.markdown("### Dashboard Preview")
        show_sample_dashboard()
        return
    
    df = st.session_state.df
    
    # Get insights
    insights = get_student_insights(df)
    
    if 'Predicted_Score' not in df.columns:
        st.warning("Predictions not available. Please re-upload your data.")
        return
    
    # Overview metrics
    st.markdown('<p class="section-header">Key Performance Indicators</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{insights['total_students']}</div>
            <div class="metric-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #ef4444;">{insights['high_risk']}</div>
            <div class="metric-label">High Risk (< 40)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">{insights['moderate_risk']}</div>
            <div class="metric-label">Moderate Risk (40-50)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{insights['avg_score']}%</div>
            <div class="metric-label">Average Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown('<p class="section-header">Performance Analysis</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        fig = px.histogram(
            df, 
            x='Predicted_Score', 
            nbins=20,
            title='Score Distribution',
            color_discrete_sequence=['#2E86AB']
        )
        fig.add_vline(x=50, line_dash="dash", line_color="red", annotation_text="Risk Threshold")
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family="Inter"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Risk level pie chart
        risk_data = pd.DataFrame({
            'Risk Level': ['High Risk', 'Moderate Risk', 'Low Risk', 'Excellent'],
            'Count': [insights['high_risk'], insights['moderate_risk'], 
                     insights['low_risk'], insights['excellent']],
            'Color': ['#ef4444', '#f59e0b', '#10b981', '#8b5cf6']
        })
        
        fig = px.pie(
            risk_data, 
            values='Count', 
            names='Risk Level',
            title='Risk Level Distribution',
            color_discrete_sequence=risk_data['Color']
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family="Inter"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional insights
    st.markdown('<p class="section-header">Detailed Insights</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'gender_performance' in insights:
            st.markdown("#### Performance by Gender")
            gender_df = pd.DataFrame(list(insights['gender_performance'].items()), 
                                   columns=['Gender', 'Avg Score'])
            gender_df['Gender'] = gender_df['Gender'].map({0: 'Male', 1: 'Female'})
            
            fig = px.bar(
                gender_df, 
                x='Gender', 
                y='Avg Score',
                color='Avg Score',
                color_continuous_scale='viridis',
                title='Average Score by Gender'
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_family="Inter"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'extracurricular_impact' in insights:
            st.markdown("#### Extracurricular Impact")
            extra_df = pd.DataFrame(list(insights['extracurricular_impact'].items()), 
                                  columns=['Participation', 'Avg Score'])
            extra_df['Participation'] = extra_df['Participation'].map({0: 'No', 1: 'Yes'})
            
            fig = px.bar(
                extra_df, 
                x='Participation', 
                y='Avg Score',
                color='Avg Score',
                color_continuous_scale='plasma',
                title='Impact of Extracurricular Activities'
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font_family="Inter"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity summary
    st.markdown('<p class="section-header">Summary Report</p>', unsafe_allow_html=True)
    
    # Create summary cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="info-card success-card">
            <h4>Students Performing Well</h4>
            <p><strong>{insights['excellent'] + insights['low_risk']}</strong> students are predicted to score 50% or above</p>
            <p>That's <strong>{round((insights['excellent'] + insights['low_risk']) / insights['total_students'] * 100, 1)}%</strong> of all students!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="info-card warning-card">
            <h4>Students Needing Support</h4>
            <p><strong>{insights['high_risk'] + insights['moderate_risk']}</strong> students may need additional support</p>
            <p>Focus on <strong>{insights['high_risk']}</strong> high-risk students first</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        performance_trend = "Positive" if insights['avg_score'] >= 60 else "Needs Improvement"
        st.markdown(f"""
        <div class="info-card">
            <h4>Overall Performance</h4>
            <p>Class average: <strong>{insights['avg_score']}%</strong></p>
            <p>Trend: <strong>{performance_trend}</strong></p>
        </div>
        """, unsafe_allow_html=True)

def show_sample_dashboard():
    """Show a sample dashboard with dummy data"""
    st.markdown("*This is a preview with sample data*")
    
    # Sample metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">150</div>
            <div class="metric-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: #ef4444;">12</div>
            <div class="metric-label">High Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value" style="color: #f59e0b;">18</div>
            <div class="metric-label">Moderate Risk</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">67.3%</div>
            <div class="metric-label">Average Score</div>
        </div>
        """, unsafe_allow_html=True)