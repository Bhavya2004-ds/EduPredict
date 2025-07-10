# EduPredict - Student Performance Analytics

An AI-powered educational analytics platform that uses machine learning to predict student performance and identify at-risk students. Built with Streamlit for an intuitive, interactive user experience.

## Features

- ** AI-Powered Predictions**: Advanced machine learning algorithms for accurate performance forecasting
- **Interactive Dashboard**: Real-time metrics, visual analytics, and trend analysis
- **Advanced Analytics**: Statistical analysis, correlation studies, and demographic insights
- **Actionable Reports**: At-risk student identification with intervention recommendations
- **Privacy-First**: Local processing with no data transmission to external servers

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your model file**:
   - Place your trained machine learning model as `model.pkl` in the root directory
   - The model should be compatible with scikit-learn's joblib format

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## Data Format Requirements

Your CSV file should include the following columns:

### Required Columns:
- `Student_ID`: Unique identifier for each student
- `Age`: Student age (typically 16-20)
- `Gender`: Male/Female
- `Study_Hours_per_Week`: Weekly study hours
- `Attendance_Rate`: Attendance percentage (0-100)
- `Previous_Grade`: Previous academic grade (A/B/C/D)
- `Parental_Education_Level`: Parent education level
- `Internet_Access_at_Home`: Yes/No
- `Extracurricular_Activities`: Yes/No

### Example CSV Structure:
```csv
Student_ID,Age,Gender,Study_Hours_per_Week,Attendance_Rate,Previous_Grade,Parental_Education_Level,Internet_Access_at_Home,Extracurricular_Activities
STU001,17,Female,25,92.5,B,Bachelor,Yes,Yes
STU002,18,Male,15,87.3,C,High School,No,No
```

## Application Pages

### Dashboard
- Overview metrics and KPIs
- Performance distribution charts
- Risk level analysis
- Executive summary

### Upload & Analyze
- File upload interface
- Data preview and validation
- Prediction results
- Detailed student reports

### Advanced Analytics
- Statistical analysis
- Correlation studies
- Demographic insights
- Performance trends

### About
- Application information
- Usage instructions
- Technical details

## Risk Level Classifications

| Risk Level | Score Range | Description | Action Required |
|------------|-------------|-------------|-----------------|
| 🔴 High Risk | < 40% | Immediate intervention required | Urgent support needed |
| 🟡 Moderate Risk | 40-50% | Additional support recommended | Monitor closely |
| 🟢 Low Risk | 50-70% | On track for success | Continue current strategies |
| 🌟 Excellent | 70%+ | Outstanding performance | Consider advanced opportunities |

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **ML Library**: Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Statistics**: SciPy

## Privacy & Security

- **Local Processing**: All data is processed locally in your browser
- **No Data Storage**: No data is stored or transmitted to external servers
- **Session-Based**: Data is only retained during your current session
- **Compliance**: Designed with FERPA and GDPR principles in mind

## Usage Instructions

1. **Prepare Your Data**: Ensure your CSV file follows the required format
2. **Upload Data**: Navigate to "Upload & Analyze" and upload your file
3. **View Results**: Explore predictions and risk classifications
4. **Analyze Insights**: Use the Dashboard and Analytics pages for deeper insights
5. **Take Action**: Download reports and implement intervention strategies

## Sample Data

Don't have data ready? Use the "Sample Data" feature to explore the application with generated demo data.

## Troubleshooting

### Common Issues:

1. **Model file not found**:
   - Ensure `model.pkl` is in the root directory
   - Check that the model was saved using joblib

2. **CSV upload errors**:
   - Verify all required columns are present
   - Check for missing values or incorrect formats
   - Ensure consistent data types

3. **Performance issues**:
   - Large datasets (>5000 rows) may take longer to process
   - Consider sampling your data for initial exploration

## Model Requirements

The application expects a scikit-learn compatible model that:
- Accepts the preprocessed features as input
- Returns numeric predictions (exam scores)
- Is saved using joblib

### Example Model Training:
```python
import joblib
from sklearn.ensemble import RandomForestRegressor

# Train your model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, 'model.pkl')
```

## Best Practices

- **Data Quality**: Ensure clean, complete data for best results
- **Regular Updates**: Update predictions as new data becomes available
- **Intervention Focus**: Prioritize high-risk students for immediate attention
- **Holistic Approach**: Combine AI insights with teacher observations
- **Privacy Protection**: Remove or anonymize sensitive information

## Support

For questions, issues, or feature requests:
- Check the troubleshooting section above
- Review the About page within the application
- Ensure all dependencies are properly installed

## License

This project is designed for educational purposes. Please ensure compliance with your institution's data privacy policies when using student data.

---

**Built with ❤️ for educators who care about every student's journey**