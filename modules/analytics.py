import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set matplotlib style for better plots
plt.style.use('default')
sns.set_palette("husl")

from utils.data_processing import get_student_insights

def show():
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>Advanced Analytics</h1>
        <p>Deep dive into student performance data with statistical analysis and insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data exists
    if 'df' not in st.session_state or st.session_state.df is None:
        st.markdown("""
        <div class="info-card warning-card">
            <h3>No Data Available</h3>
            <p>Please upload student data first to view advanced analytics.</p>
            <p>Navigate to the <strong>"Upload & Analyze"</strong> page to get started.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    df = st.session_state.df
    
    if 'Predicted_Score' not in df.columns:
        st.warning("Predictions not available. Please re-upload your data.")
        return
    
    # Analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "Performance Analysis", 
        "Correlation Analysis", 
        "Demographic Insights",
        "Statistical Summary"
    ])
    
    with tab1:
        show_performance_analysis(df)
    
    with tab2:
        show_correlation_analysis(df)
    
    with tab3:
        show_demographic_insights(df)
    
    with tab4:
        show_statistical_summary(df)

def show_performance_analysis(df):
    """Show detailed performance analysis using matplotlib"""
    st.markdown("### Performance Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot for score distribution
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.boxplot(df['Predicted_Score'], vert=True)
        ax.axhline(y=50, color='red', linestyle='--', label='Pass Threshold')
        ax.set_ylabel('Predicted Score')
        ax.set_title('Score Distribution (Box Plot)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # Histogram for detailed distribution
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(df['Predicted_Score'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
        ax.axvline(x=50, color='red', linestyle='--', label='Pass Threshold')
        ax.set_xlabel('Predicted Score')
        ax.set_ylabel('Number of Students')
        ax.set_title('Detailed Score Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    # Performance by study hours
    if 'Study_Hours_per_Week' in df.columns:
        st.markdown("### Study Hours vs Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(df['Study_Hours_per_Week'], df['Predicted_Score'], 
                               c=df['Predicted_Score'], cmap='viridis', alpha=0.6)
            ax.set_xlabel('Study Hours per Week')
            ax.set_ylabel('Predicted Score')
            ax.set_title('Study Hours vs Predicted Score')
            plt.colorbar(scatter, ax=ax, label='Score')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
        
        with col2:
            # Box plot by study hour bins
            df['Study_Hours_Bin'] = pd.cut(df['Study_Hours_per_Week'], 
                                          bins=[0, 10, 20, 30, 100], 
                                          labels=['0-10h', '11-20h', '21-30h', '30h+'])
            
            fig, ax = plt.subplots(figsize=(8, 6))
            df.boxplot(column='Predicted_Score', by='Study_Hours_Bin', ax=ax)
            ax.set_xlabel('Study Hours Bin')
            ax.set_ylabel('Predicted Score')
            ax.set_title('Score Distribution by Study Hours')
            plt.suptitle('')  # Remove default title
            st.pyplot(fig)

def show_correlation_analysis(df):
    """Show correlation analysis between variables"""
    st.markdown("### Variable Correlation Analysis")
    
    # Select numeric columns for correlation
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) > 1:
        # Correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Create correlation heatmap
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, 
                   square=True, fmt='.2f', ax=ax)
        ax.set_title('Correlation Matrix of Numeric Variables')
        st.pyplot(fig)
        
        # Top correlations with predicted score
        if 'Predicted_Score' in corr_matrix.columns:
            score_correlations = corr_matrix['Predicted_Score'].abs().sort_values(ascending=False)
            score_correlations = score_correlations[score_correlations.index != 'Predicted_Score']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Strongest Predictors")
                top_predictors = score_correlations.head(5)
                
                for var, corr in top_predictors.items():
                    correlation_strength = "Strong" if corr > 0.7 else "Moderate" if corr > 0.4 else "Weak"
                    st.metric(
                        label=var.replace('_', ' ').title(),
                        value=f"{corr:.3f}",
                        help=f"{correlation_strength} correlation with predicted score"
                    )
            
            with col2:
                # Correlation bar chart
                fig, ax = plt.subplots(figsize=(8, 6))
                top_predictors.head(5).plot(kind='barh', ax=ax, color='steelblue')
                ax.set_xlabel('Correlation Strength')
                ax.set_title('Top 5 Correlations with Predicted Score')
                ax.grid(True, alpha=0.3)
                st.pyplot(fig)
    else:
        st.info("Not enough numeric variables for correlation analysis.")

def show_demographic_insights(df):
    """Show demographic analysis"""
    st.markdown("### Demographic Performance Analysis")
    
    # Gender analysis
    if 'Gender' in df.columns:
        st.markdown("#### Performance by Gender")
        
        # Convert gender encoding back to readable format
        df_display = df.copy()
        if df['Gender'].dtype in ['int64', 'float64']:
            df_display['Gender'] = df_display['Gender'].map({0: 'Male', 1: 'Female'})
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Box plot by gender
            fig, ax = plt.subplots(figsize=(8, 6))
            df_display.boxplot(column='Predicted_Score', by='Gender', ax=ax)
            ax.set_xlabel('Gender')
            ax.set_ylabel('Predicted Score')
            ax.set_title('Score Distribution by Gender')
            plt.suptitle('')  # Remove default title
            st.pyplot(fig)
        
        with col2:
            # Gender statistics
            gender_stats = df_display.groupby('Gender')['Predicted_Score'].agg(['mean', 'std', 'count']).round(2)
            
            fig, ax = plt.subplots(figsize=(8, 6))
            gender_stats['mean'].plot(kind='bar', ax=ax, color=['lightblue', 'lightcoral'], 
                                    yerr=gender_stats['std'], capsize=4)
            ax.set_xlabel('Gender')
            ax.set_ylabel('Average Score')
            ax.set_title('Average Score by Gender')
            ax.tick_params(axis='x', rotation=0)
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
    
    # Extracurricular activities analysis
    if 'Extracurricular_Activities' in df.columns:
        st.markdown("#### 🏃‍♂️ Impact of Extracurricular Activities")
        
        df_display = df.copy()
        if df['Extracurricular_Activities'].dtype in ['int64', 'float64']:
            df_display['Extracurricular_Activities'] = df_display['Extracurricular_Activities'].map({0: 'No', 1: 'Yes'})
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 6))
            df_display.boxplot(column='Predicted_Score', by='Extracurricular_Activities', ax=ax)
            ax.set_xlabel('Extracurricular Activities')
            ax.set_ylabel('Predicted Score')
            ax.set_title('Score Distribution by Extracurricular Participation')
            plt.suptitle('')  # Remove default title
            st.pyplot(fig)
        
        with col2:
            extra_stats = df_display.groupby('Extracurricular_Activities')['Predicted_Score'].agg(['mean', 'std', 'count']).round(2)
            
            # Calculate the difference
            if len(extra_stats) == 2:
                diff = extra_stats.loc['Yes', 'mean'] - extra_stats.loc['No', 'mean']
                st.metric(
                    "Performance Boost",
                    f"{diff:.2f} points",
                    help="Average score difference between students with and without extracurricular activities"
                )
            
            st.dataframe(extra_stats, use_container_width=True)

def show_statistical_summary(df):
    """Show statistical summary and insights"""
    st.markdown("### Statistical Summary")
    
    # Basic statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Descriptive Statistics")
        
        stats_df = df['Predicted_Score'].describe().round(2)
        stats_dict = {
            'Metric': ['Count', 'Mean', 'Std Dev', 'Min', '25%', 'Median (50%)', '75%', 'Max'],
            'Value': [stats_df['count'], stats_df['mean'], stats_df['std'], 
                     stats_df['min'], stats_df['25%'], stats_df['50%'], 
                     stats_df['75%'], stats_df['max']]
        }
        
        stats_display_df = pd.DataFrame(stats_dict)
        st.dataframe(stats_display_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("#### 🎯 Performance Categories")
        
        # Risk level distribution
        high_risk = len(df[df['Predicted_Score'] < 40])
        moderate_risk = len(df[(df['Predicted_Score'] >= 40) & (df['Predicted_Score'] < 50)])
        low_risk = len(df[(df['Predicted_Score'] >= 50) & (df['Predicted_Score'] < 70)])
        excellent = len(df[df['Predicted_Score'] >= 70])
        total = len(df)
        
        categories_df = pd.DataFrame({
            'Category': ['High Risk (<40)', 'Moderate Risk (40-50)', 'Low Risk (50-70)', 'Excellent (70+)'],
            'Count': [high_risk, moderate_risk, low_risk, excellent],
            'Percentage': [f"{(high_risk/total*100):.1f}%", f"{(moderate_risk/total*100):.1f}%", 
                          f"{(low_risk/total*100):.1f}%", f"{(excellent/total*100):.1f}%"]
        })
        
        st.dataframe(categories_df, use_container_width=True, hide_index=True)
    
    # Distribution visualization
    st.markdown("#### Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Simple histogram with normal curve overlay
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Plot histogram
        n, bins, patches = ax.hist(df['Predicted_Score'], bins=20, density=True, 
                                  alpha=0.7, color='skyblue', edgecolor='black')
        
        # Plot normal distribution curve
        mu, sigma = df['Predicted_Score'].mean(), df['Predicted_Score'].std()
        x = np.linspace(df['Predicted_Score'].min(), df['Predicted_Score'].max(), 100)
        y = ((1/(sigma * np.sqrt(2 * np.pi))) * 
             np.exp(-0.5 * ((x - mu) / sigma) ** 2))
        ax.plot(x, y, 'r-', linewidth=2, label='Normal Distribution')
        
        ax.set_xlabel('Predicted Score')
        ax.set_ylabel('Density')
        ax.set_title('Score Distribution with Normal Curve')
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        # Simple statistics
        st.markdown("#### Distribution Shape")
        
        # Calculate basic statistics
        mean_score = df['Predicted_Score'].mean()
        median_score = df['Predicted_Score'].median()
        std_dev = df['Predicted_Score'].std()
        
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            st.metric("Mean", f"{mean_score:.2f}")
            st.metric("Std Dev", f"{std_dev:.2f}")
        
        with col2_2:
            st.metric("Median", f"{median_score:.2f}")
            skew_approx = (mean_score - median_score) / std_dev if std_dev > 0 else 0
            st.metric("Skew (approx)", f"{skew_approx:.2f}")
    
    # Outlier analysis
    st.markdown("#### Outlier Analysis")
    
    Q1 = df['Predicted_Score'].quantile(0.25)
    Q3 = df['Predicted_Score'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df['Predicted_Score'] < lower_bound) | (df['Predicted_Score'] > upper_bound)]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Outliers", len(outliers))
    
    with col2:
        st.metric("Lower Bound", f"{lower_bound:.1f}")
    
    with col3:
        st.metric("Upper Bound", f"{upper_bound:.1f}")
    
    if len(outliers) > 0:
        st.markdown("##### Outlier Students")
        outlier_display = outliers[['Student_ID', 'Predicted_Score']].copy()
        outlier_display.columns = ['Student ID', 'Predicted Score']
        st.dataframe(outlier_display, use_container_width=True, hide_index=True)
    else:
        st.success("No outliers detected in the score distribution.")
    
    # Key insights
    st.markdown("#### Key Statistical Insights")
    
    insights = []
    
    # Performance insights
    mean_score = df['Predicted_Score'].mean()
    if mean_score >= 70:
        insights.append("**Excellent Overall Performance**: The class average is in the excellent range.")
    elif mean_score >= 60:
        insights.append("**Good Overall Performance**: The class is performing well above the pass threshold.")
    elif mean_score >= 50:
        insights.append("**Moderate Performance**: The class average is just above the pass threshold.")
    else:
        insights.append("**Below Average Performance**: The class may need significant intervention.")
    
    # Distribution insights
    std_dev = df['Predicted_Score'].std()
    if std_dev < 10:
        insights.append("**Consistent Performance**: Low variability suggests similar performance levels across students.")
    elif std_dev > 20:
        insights.append("**High Variability**: Large spread in scores suggests diverse performance levels.")
    
    # Risk insights
    risk_percentage = (len(df[df['Predicted_Score'] < 50]) / len(df)) * 100
    if risk_percentage < 10:
        insights.append("**Low Risk Population**: Most students are predicted to perform well.")
    elif risk_percentage > 30:
        insights.append("**High Risk Population**: A significant portion of students may need support.")
    
    for insight in insights:
        st.markdown(insight)