import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples to generate for the defense demo
NUM_SAMPLES = 25

# Generate synthetic data
data = {
    "Age": np.random.randint(18, 26, NUM_SAMPLES),
    "Gender": np.random.choice(["Male", "Female"], NUM_SAMPLES),
    "Socioeconomic_Status": np.random.choice(["Low", "Medium", "High"], NUM_SAMPLES, p=[0.2, 0.6, 0.2]),
    
    # We will engineer three distinct profiles to show off the model's capabilities:
    # 1. High Performers (High attendance, high study hours, high previous grades)
    # 2. Average Performers (Medium metrics)
    # 3. At-Risk (Low attendance, low study hours, low grades)
}

attendance = []
study_hours = []
prev_grade = []
ca_score = []

for i in range(NUM_SAMPLES):
    if i < 8:
        # High Performer Profile
        attendance.append(np.random.uniform(85, 100))
        study_hours.append(np.random.uniform(15, 25))
        prev_grade.append(np.random.uniform(70, 95))
        ca_score.append(np.random.uniform(25, 40))
    elif i < 18:
        # Average Performer Profile
        attendance.append(np.random.uniform(65, 85))
        study_hours.append(np.random.uniform(8, 15))
        prev_grade.append(np.random.uniform(50, 70))
        ca_score.append(np.random.uniform(15, 25))
    else:
        # At-Risk Profile
        attendance.append(np.random.uniform(40, 65))
        study_hours.append(np.random.uniform(2, 8))
        prev_grade.append(np.random.uniform(30, 50))
        ca_score.append(np.random.uniform(5, 15))

# Shuffle the data to mix the profiles
indices = np.random.permutation(NUM_SAMPLES)

data["Attendance_Percentage"] = np.round(np.array(attendance)[indices], 1)
data["Study_Hours_Per_Week"] = np.round(np.array(study_hours)[indices], 1)
data["Previous_Term_Grade"] = np.round(np.array(prev_grade)[indices], 1)
data["Continuous_Assessment_Score"] = np.round(np.array(ca_score)[indices], 1)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_file = "defense_test_data.csv"
df.to_csv(output_file, index=False)
print(f"Generated {NUM_SAMPLES} records and saved to {output_file}")
