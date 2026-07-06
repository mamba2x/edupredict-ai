import pandas as pd
from database import get_db


class StatsService:
    @staticmethod
    def get_stats():
        with get_db() as conn:
            cursor = conn.cursor()

            # ── Total record count ────────────────────────────────────────
            cursor.execute("SELECT COUNT(*) FROM predictions")
            total = cursor.fetchone()[0]

            empty_response = {
                "total_students":        0,
                "excellent_count":       0,
                "average_count":         0,
                "at_risk_count":         0,
                "avg_study_hours":       0,
                "avg_cgpa":              0,
                "avg_ca":                0,
                "recent_predictions":    [],
                "weekly_volume":         {"Excellent": [0]*7, "Average": [0]*7, "At-Risk": [0]*7},
                "cgpa_vs_outcome":       [],
                "study_hours_vs_outcome":[],
                "level_distribution":    [],
            }

            if total == 0:
                return empty_response

            # ── Class counts ──────────────────────────────────────────────
            cursor.execute(
                "SELECT predicted_status, COUNT(*) FROM predictions GROUP BY predicted_status"
            )
            status_counts = {row[0]: row[1] for row in cursor.fetchall()}

            # ── Averages ──────────────────────────────────────────────────
            cursor.execute("""
                SELECT AVG(study_hours_per_week),
                       AVG(previous_cgpa),
                       AVG(course_ca_average)
                FROM predictions
            """)
            avgs = cursor.fetchone()

            # ── Recent 8 records ──────────────────────────────────────────
            cursor.execute(
                "SELECT * FROM predictions ORDER BY timestamp DESC LIMIT 8"
            )
            recent = [dict(row) for row in cursor.fetchall()]

            # ── Build DataFrame for chart computations ────────────────────
            cursor.execute("""
                SELECT timestamp, study_hours_per_week, previous_cgpa,
                       course_ca_average, level, predicted_status
                FROM predictions
            """)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=[
                'timestamp', 'study_hours_per_week', 'previous_cgpa',
                'course_ca_average', 'level', 'predicted_status'
            ])

            # ── Weekly volume (Mon–Sun) ────────────────────────────────────
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['day'] = df['timestamp'].dt.dayofweek

            weekly_volume = {"Excellent": [0]*7, "Average": [0]*7, "At-Risk": [0]*7}
            for status in weekly_volume:
                counts = df[df['predicted_status'] == status]['day'].value_counts()
                for d in range(7):
                    weekly_volume[status][d] = int(counts.get(d, 0))

            # ── Generic bucket helper ─────────────────────────────────────
            def calculate_buckets(col_name, buckets):
                result = []
                for b in buckets:
                    mask = (df[col_name] >= b['min']) & (df[col_name] < b['max'])
                    subset = df[mask]
                    n = len(subset)
                    exc = int(len(subset[subset['predicted_status'] == 'Excellent']))
                    avg = int(len(subset[subset['predicted_status'] == 'Average']))
                    rsk = int(len(subset[subset['predicted_status'] == 'At-Risk']))
                    result.append({
                        "label":     b['label'],
                        "excellent": round(exc / n * 100) if n else 0,
                        "average":   round(avg / n * 100) if n else 0,
                        "atRisk":    round(rsk / n * 100) if n else 0,
                    })
                return result

            # ── Previous CGPA vs Outcome ──────────────────────────────────
            cgpa_buckets = [
                {"label": "< 1.5",   "min": 0.0, "max": 1.5},
                {"label": "1.5–2.5", "min": 1.5, "max": 2.5},
                {"label": "2.5–3.5", "min": 2.5, "max": 3.5},
                {"label": "3.5–4.5", "min": 3.5, "max": 4.5},
                {"label": "≥ 4.5",   "min": 4.5, "max": 6.0},
            ]
            cgpa_vs_outcome = calculate_buckets('previous_cgpa', cgpa_buckets)

            # ── Study Hours vs Outcome ────────────────────────────────────
            hrs_buckets = [
                {"label": "< 5 hrs",   "min": 0,  "max": 5},
                {"label": "5–10 hrs",  "min": 5,  "max": 10},
                {"label": "10–15 hrs", "min": 10, "max": 15},
                {"label": "15–20 hrs", "min": 15, "max": 20},
                {"label": "20–25 hrs", "min": 20, "max": 25},
                {"label": "> 25 hrs",  "min": 25, "max": 100},
            ]
            study_hours_vs_outcome = calculate_buckets('study_hours_per_week', hrs_buckets)

            # ── Level distribution ────────────────────────────────────────
            level_counts = df['level'].value_counts().sort_index()
            level_distribution = [
                {"level": f"Level {int(lv)}", "count": int(cnt)}
                for lv, cnt in level_counts.items()
                if pd.notna(lv)
            ]

            return {
                "total_students":         total,
                "excellent_count":        status_counts.get("Excellent", 0),
                "average_count":          status_counts.get("Average", 0),
                "at_risk_count":          status_counts.get("At-Risk", 0),
                "avg_study_hours":        round(avgs[0], 1) if avgs[0] is not None else 0,
                "avg_cgpa":               round(avgs[1], 2) if avgs[1] is not None else 0,
                "avg_ca":                 round(avgs[2], 1) if avgs[2] is not None else 0,
                "recent_predictions":     recent,
                "weekly_volume":          weekly_volume,
                "cgpa_vs_outcome":        cgpa_vs_outcome,
                "study_hours_vs_outcome": study_hours_vs_outcome,
                "level_distribution":     level_distribution,
            }
