import sqlite3
from contextlib import contextmanager
from config import DB_FILE


def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        # ── Drop old incompatible table if it exists ──────────────────────
        # The old schema used attendance_percentage / previous_term_grade /
        # continuous_assessment_score which no longer exist in the new dataset.
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        """)
        cursor.execute("SELECT version FROM schema_version WHERE version = 2")
        already_migrated = cursor.fetchone() is not None

        if not already_migrated:
            # Drop the old table so we can recreate with new columns
            cursor.execute("DROP TABLE IF EXISTS predictions")
            cursor.execute("INSERT OR IGNORE INTO schema_version (version) VALUES (2)")

        # ── Create new predictions table ──────────────────────────────────
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id                      INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp               DATETIME DEFAULT CURRENT_TIMESTAMP,
                student_id              TEXT,
                gender                  TEXT,
                age                     INTEGER,
                socioeconomic_status    TEXT,
                level                   INTEGER,
                semester                TEXT,
                study_hours_per_week    REAL,
                previous_cgpa           REAL,
                previous_course_average REAL,
                course_ca_average       REAL,
                total_units             INTEGER,
                predicted_status        TEXT,
                confidence              REAL
            )
        """)
        conn.commit()


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


class PredictionRepository:

    @staticmethod
    def insert_prediction(data, prediction_status: str, confidence: float = 0.0,
                          derived: dict = None):
        derived = derived or {}
        with get_db() as conn:
            conn.execute("""
                INSERT INTO predictions (
                    student_id, gender, age, socioeconomic_status,
                    level, semester, study_hours_per_week, previous_cgpa,
                    previous_course_average, course_ca_average, total_units,
                    predicted_status, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                getattr(data, 'Student_ID', None),
                data.Gender,
                data.Age,
                data.Socioeconomic_Status,
                data.Level,
                data.Semester,
                data.Study_Hours_Per_Week,
                data.Previous_CGPA,
                derived.get('Previous_Course_Average', 0.0),
                derived.get('Course_CA_Average', 0.0),
                derived.get('Total_Units', 0),
                str(prediction_status),
                round(float(confidence), 4),
            ))
            conn.commit()

    @staticmethod
    def _insert_row_from_dict(cursor, row: dict):
        cursor.execute("""
            INSERT INTO predictions (
                student_id, gender, age, socioeconomic_status,
                level, semester, study_hours_per_week, previous_cgpa,
                previous_course_average, course_ca_average, total_units,
                predicted_status, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get('Student_ID'),
            row.get('Gender'),
            row.get('Age'),
            row.get('Socioeconomic_Status'),
            row.get('Level'),
            row.get('Semester'),
            row.get('Study_Hours_Per_Week'),
            row.get('Previous_CGPA'),
            row.get('Previous_Course_Average', 0.0),
            row.get('Course_CA_Average', 0.0),
            row.get('Total_Units', 0),
            str(row.get('Predicted_Performance_Status', '')),
            round(float(row.get('Confidence', 0.0)), 4),
        ))

    @staticmethod
    def replace_predictions(dataframe):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM predictions")
            for _, row in dataframe.iterrows():
                PredictionRepository._insert_row_from_dict(cursor, dict(row))
            conn.commit()

    @staticmethod
    def insert_predictions(dataframe):
        with get_db() as conn:
            cursor = conn.cursor()
            for _, row in dataframe.iterrows():
                PredictionRepository._insert_row_from_dict(cursor, dict(row))
            conn.commit()

    @staticmethod
    def get_record_count():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM predictions")
            return cursor.fetchone()[0]

    @staticmethod
    def get_recent_records(limit: int = 10000):
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def delete_all_records():
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM predictions")
            conn.commit()
