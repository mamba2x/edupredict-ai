import pandas as pd
import numpy as np
import os

def prepare_data():
    print("=" * 60)
    print("  Preparing Real-World UCI Student Performance Dataset")
    print("=" * 60)
    
    # Paths to raw files in finalyear_assignment2 root
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mat_path = os.path.join(root_dir, "student-mat.csv")
    por_path = os.path.join(root_dir, "student-por.csv")
    
    if not os.path.exists(mat_path) or not os.path.exists(por_path):
        # Try current directory as fallback
        mat_path = "student-mat.csv"
        por_path = "student-por.csv"
        if not os.path.exists(mat_path):
            raise FileNotFoundError("Raw student-mat.csv or student-por.csv not found.")
            
    print(f"[INFO] Reading Math cohort from: {mat_path}")
    df_mat = pd.read_csv(mat_path, sep=";")
    print(f"[INFO] Reading Portuguese cohort from: {por_path}")
    df_por = pd.read_csv(por_path, sep=";")
    
    def map_columns(df):
        mapped = pd.DataFrame()
        
        # 1. Age
        mapped['Age'] = df['age']
        
        # 2. Gender
        mapped['Gender'] = df['sex'].map({'F': 'Female', 'M': 'Male'})
        
        # 3. Socioeconomic_Status
        # Low: Medu & Fedu both <= 1. High: Medu or Fedu >= 4. Medium: Otherwise.
        max_edu = df[['Medu', 'Fedu']].max(axis=1)
        mapped['Socioeconomic_Status'] = np.select(
            [max_edu <= 1, max_edu >= 4],
            ['Low', 'High'],
            default='Medium'
        )
        
        # 4. Attendance_Percentage
        # (1 - absences / 93) * 100. Absences max is 93.
        attendance = (1.0 - (df['absences'] / 93.0)) * 100.0
        mapped['Attendance_Percentage'] = np.clip(np.round(attendance, 1), 0.0, 100.0)
        
        # 5. Study_Hours_Per_Week
        # studytime bins: 1 -> 1.5, 2 -> 3.5, 3 -> 7.5, 4 -> 12.5 hours
        mapped['Study_Hours_Per_Week'] = df['studytime'].map({1: 1.5, 2: 3.5, 3: 7.5, 4: 12.5})
        
        # 6. Previous_Term_Grade
        # G1 scaled from [0, 20] to [0, 100] -> G1 * 5
        mapped['Previous_Term_Grade'] = np.round(df['G1'] * 5.0, 1)
        
        # 7. Continuous_Assessment_Score
        # G2 scaled from [0, 20] to [0, 40] -> G2 * 2
        mapped['Continuous_Assessment_Score'] = np.round(df['G2'] * 2.0, 1)
        
        # 8. Performance_Status
        # G3 >= 15 -> Excellent, 10 <= G3 < 15 -> Average, G3 < 10 -> At-Risk
        conditions = [
            df['G3'] >= 15,
            (df['G3'] >= 10) & (df['G3'] < 15),
            df['G3'] < 10
        ]
        choices = ['Excellent', 'Average', 'At-Risk']
        mapped['Performance_Status'] = np.select(conditions, choices, default='Unknown')
        
        return mapped

    print("[INFO] Mapping Math cohort attributes...")
    mapped_mat = map_columns(df_mat)
    print(f"       Mapped {len(mapped_mat)} Math records.")
    
    print("[INFO] Mapping Portuguese cohort attributes...")
    mapped_por = map_columns(df_por)
    print(f"       Mapped {len(mapped_por)} Portuguese records.")
    
    # Combine both datasets
    combined_df = pd.concat([mapped_mat, mapped_por], ignore_index=True)
    print(f"[INFO] Combined both cohorts. Total records: {len(combined_df)}")
    
    # Save combined dataset to server/data/student_data.csv
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "student_data.csv")
    
    combined_df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved mapped real dataset to: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    prepare_data()
