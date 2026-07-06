import os

DB_FILE = "students.db"
MODEL_DIR = "models"
DATASET_PATH = os.path.join("data", "cs_dataset.xlsx")
DATASET_SHEET = "Model_Ready"

# ── New CS Feature Columns (model-ready order) ──────────────────────────────
FEATURE_COLS = [
    "Gender",
    "Age",
    "Socioeconomic_Status",
    "Level",
    "Semester",
    "Study_Hours_Per_Week",
    "Previous_CGPA",
    "Previous_Course_Average",
    "Lowest_Previous_Score",
    "Weak_Previous_Count",
    "Course_CA_Average",
    "Lowest_CA_Score",
    "Weak_CA_Count",
    "Core_CA_Average",
    "Elective_CA_Average",
    "University_CA_Average",
    "Total_Units",
]

FEATURE_LABELS = {
    "Gender": "Gender",
    "Age": "Age",
    "Socioeconomic_Status": "Socioeconomic Status",
    "Level": "Level",
    "Semester": "Semester",
    "Study_Hours_Per_Week": "Weekly Study Hours",
    "Previous_CGPA": "Previous CGPA",
    "Previous_Course_Average": "Previous Course Average",
    "Lowest_Previous_Score": "Lowest Previous Score",
    "Weak_Previous_Count": "Weak Previous Courses",
    "Course_CA_Average": "Course CA Average",
    "Lowest_CA_Score": "Lowest CA Score",
    "Weak_CA_Count": "Weak CA Count",
    "Core_CA_Average": "Core CA Average",
    "Elective_CA_Average": "Elective CA Average",
    "University_CA_Average": "University CA Average",
    "Total_Units": "Total Units",
}

# ── Validation Constants ─────────────────────────────────────────────────────
VALID_GENDERS   = ["Male", "Female"]
VALID_SES       = ["Low", "Medium", "High"]
VALID_LEVELS    = [100, 200, 300, 400]
VALID_SEMESTERS = ["First", "Second"]

MAX_CA_SCORE       = 30.0   # individual CA score ceiling
MAX_PREV_SCORE     = 100.0  # individual previous course score ceiling
MAX_CGPA           = 5.0    # CGPA scale ceiling (Nigerian 5-point scale)
MAX_STUDY_HOURS    = 80.0
