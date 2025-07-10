import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
import streamlit as st

def preprocess_data(df):
    """
    Preprocess the student data for prediction
    """
    # Make a copy to avoid modifying the original
    df_processed = df.copy()
    
    # Binary encoding for categorical variables
    binary_cols = ["Gender", "Internet_Access_at_Home", "Extracurricular_Activities"]
    
    for col in binary_cols:
        if col in df_processed.columns:
            if col == "Gender":
                df_processed[col] = df_processed[col].map({'Male': 0, 'Female': 1})
            else:
                df_processed[col] = df_processed[col].map({'Yes': 1, 'No': 0})
    
    # Encode parental education level
    if "Parental_Education_Level" in df_processed.columns:
        le = LabelEncoder()
        df_processed["Parental_Education_Level"] = le.fit_transform(df_processed["Parental_Education_Level"])
    
    return df_processed

def load_model():
    """
    Load the trained model
    """
    try:
        model = joblib.load("model.pkl")
        return model
    except FileNotFoundError:
        st.error("Model file 'model.pkl' not found. Please ensure the model file is in the root directory.")
        return None

def make_predictions(df, model):
    """
    Make predictions on the preprocessed data
    """
    # Select features for prediction (exclude ID and target columns)
    feature_cols = [col for col in df.columns 
                   if col not in ["Student_ID", "Pass_Fail", "Final_Exam_Score", "Predicted_Score"]]
    
    X = df[feature_cols]
    predictions = model.predict(X)
    
    return predictions

def categorize_risk_level(score):
    """
    Categorize students based on predicted scores
    """
    if score < 40:
        return "High Risk", "🔴"
    elif score < 50:
        return "Moderate Risk", "🟡"
    elif score < 70:
        return "Low Risk", "🟢"
    else:
        return "Excellent", "🌟"

def get_student_insights(df):
    """
    Generate insights about the student data
    """
    insights = {}
    
    if 'Predicted_Score' in df.columns:
        insights['total_students'] = len(df)
        insights['avg_score'] = round(df['Predicted_Score'].mean(), 2)
        insights['high_risk'] = len(df[df['Predicted_Score'] < 40])
        insights['moderate_risk'] = len(df[(df['Predicted_Score'] >= 40) & (df['Predicted_Score'] < 50)])
        insights['low_risk'] = len(df[(df['Predicted_Score'] >= 50) & (df['Predicted_Score'] < 70)])
        insights['excellent'] = len(df[df['Predicted_Score'] >= 70])
        
        # Performance distribution
        insights['score_distribution'] = {
            'Below 40': insights['high_risk'],
            '40-50': insights['moderate_risk'], 
            '50-70': insights['low_risk'],
            '70+': insights['excellent']
        }
        
        # Gender analysis if available
        if 'Gender' in df.columns:
            gender_performance = df.groupby('Gender')['Predicted_Score'].mean()
            insights['gender_performance'] = gender_performance.to_dict()
        
        # Extracurricular impact if available
        if 'Extracurricular_Activities' in df.columns:
            extra_performance = df.groupby('Extracurricular_Activities')['Predicted_Score'].mean()
            insights['extracurricular_impact'] = extra_performance.to_dict()
    
    return insights

def highlight_risk_score(val):
    """
    Apply color highlighting based on risk level
    """
    if pd.isna(val):
        return ''
    
    if val < 40:
        return 'background-color: #ef4444; color: white; font-weight: bold; border-radius: 6px;'
    elif val < 50:
        return 'background-color: #f59e0b; color: white; font-weight: bold; border-radius: 6px;'
    elif val < 70:
        return 'background-color: #10b981; color: white; font-weight: bold; border-radius: 6px;'
    else:
        return 'background-color: #8b5cf6; color: white; font-weight: bold; border-radius: 6px;'

def create_sample_data():
    """
    Create sample data for demonstration purposes
    """
    np.random.seed(42)
    n_students = 100
    
    sample_data = {
        'Student_ID': [f'STU{i:03d}' for i in range(1, n_students + 1)],
        'Age': np.random.randint(16, 20, n_students),
        'Gender': np.random.choice(['Male', 'Female'], n_students),
        'Study_Hours_per_Week': np.random.randint(5, 40, n_students),
        'Attendance_Rate': np.random.uniform(60, 100, n_students),
        'Previous_Grade': np.random.choice(['A', 'B', 'C', 'D'], n_students, p=[0.2, 0.3, 0.3, 0.2]),
        'Parental_Education_Level': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_students, p=[0.3, 0.4, 0.2, 0.1]),
        'Internet_Access_at_Home': np.random.choice(['Yes', 'No'], n_students, p=[0.8, 0.2]),
        'Extracurricular_Activities': np.random.choice(['Yes', 'No'], n_students, p=[0.6, 0.4]),
        'Family_Income_Level': np.random.choice(['Low', 'Medium', 'High'], n_students, p=[0.3, 0.5, 0.2])
    }
    
    return pd.DataFrame(sample_data)