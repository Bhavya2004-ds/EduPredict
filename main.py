import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv("dataset/student_performance_dataset.csv")

# Keep Student_ID and Pass_Fail for later reference
# Encode binary categorical columns
binary_cols = ["Gender", "Internet_Access_at_Home", "Extracurricular_Activities"]
for col in binary_cols:
    df[col] = df[col].map({'Yes': 1, 'No': 0, 'Male': 0, 'Female': 1})

# Encode 'Parental_Education_Level'
df["Parental_Education_Level"] = LabelEncoder().fit_transform(df["Parental_Education_Level"])

# Define features (exclude Student_ID, Pass_Fail, Final_Exam_Score)
X = df.drop(["Student_ID", "Pass_Fail", "Final_Exam_Score"], axis=1)
y = df["Final_Exam_Score"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Model Evaluation:")
print(f"R² Score: {r2:.2f}")
print(f"RMSE: {rmse:.2f}")

# Predict on full dataset
df["Predicted_Score"] = model.predict(X)

# Flag students at risk
at_risk = df[df["Predicted_Score"] < 50]

# Show relevant info
print("\nStudents predicted to score below 50:")
print(at_risk[["Student_ID", "Predicted_Score", "Pass_Fail"]])


# Save the model
joblib.dump(model, "model.pkl")
print("Model saved as model.pkl")
