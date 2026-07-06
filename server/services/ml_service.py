import joblib
import os
import json
import numpy as np
import pandas as pd
from config import MODEL_DIR, FEATURE_COLS
from schemas import StudentInput


def _safe_avg(lst):
    return float(np.mean(lst)) if lst else 0.0

def _safe_min(lst):
    return float(np.min(lst)) if lst else 0.0

def _weak_count(lst, threshold):
    return int(sum(1 for s in lst if s < threshold))


def compute_derived_features(data: StudentInput) -> dict:
    """
    Auto-compute the 10 fields the user does not enter directly.
    Called before prediction for both single and batch paths.

    Special case — 100 Alpha (Level 100, Semester First):
      previous_scores is empty; Entry_Academic_Score is used as the
      single previous-score proxy so that Previous_Course_Average,
      Lowest_Previous_Score, and Weak_Previous_Count are still meaningful.

    NUC/Vocational scores (nuc_ca_scores) are included in the overall
    Course_CA_Average / Lowest_CA_Score / Weak_CA_Count pools and in
    Total_Units — matching the dataset's own calculation logic.
    """
    is_100_alpha = (data.Level == 100 and data.Semester == "First")

    if is_100_alpha and data.Entry_Academic_Score is not None:
        # Use the entry score as the sole previous-score proxy
        prev = [data.Entry_Academic_Score]
    else:
        prev = data.previous_scores

    core   = data.core_ca_scores
    elec   = data.elective_ca_scores
    univ   = data.university_ca_scores
    nuc    = getattr(data, 'nuc_ca_scores', [])   # graceful fallback
    all_ca = core + elec + univ + nuc

    return {
        "Previous_Course_Average":  round(_safe_avg(prev),  4),
        "Lowest_Previous_Score":    round(_safe_min(prev),  4),
        "Weak_Previous_Count":      _weak_count(prev, 45),
        "Course_CA_Average":        round(_safe_avg(all_ca), 4),
        "Lowest_CA_Score":          round(_safe_min(all_ca), 4),
        "Weak_CA_Count":            _weak_count(all_ca, 15),
        "Core_CA_Average":          round(_safe_avg(core),  4),
        "Elective_CA_Average":      round(_safe_avg(elec),  4),
        "University_CA_Average":    round(_safe_avg(univ),  4),
        "Total_Units":              len(core) + len(elec) + len(univ) + len(nuc),
    }


class MLService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance.best_model   = None
            cls._instance.scaler       = None
            cls._instance.le_status    = None
            cls._instance.le_gender    = None
            cls._instance.oe_ses       = None
            cls._instance.oe_semester  = None
            cls._instance.feature_cols = FEATURE_COLS
            cls._instance.load_models()
        return cls._instance

    def load_models(self):
        try:
            self.best_model   = joblib.load(os.path.join(MODEL_DIR, "best_model.pkl"))
            self.scaler       = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
            self.le_status    = joblib.load(os.path.join(MODEL_DIR, "le_status.pkl"))
            self.le_gender    = joblib.load(os.path.join(MODEL_DIR, "le_gender.pkl"))
            self.oe_ses       = joblib.load(os.path.join(MODEL_DIR, "oe_ses.pkl"))
            self.oe_semester  = joblib.load(os.path.join(MODEL_DIR, "oe_semester.pkl"))

            feat_path = os.path.join(MODEL_DIR, "feature_cols.json")
            if os.path.exists(feat_path):
                with open(feat_path) as f:
                    self.feature_cols = json.load(f)

            print("[INFO] All ML artifacts loaded successfully.")
        except Exception as e:
            print(f"[WARN] Could not load ML artifacts: {e}")
            print("[WARN] Run train.py first to generate the model files.")

    # ── Encode a raw-input row into model-ready numeric values ────────────
    def _encode_row(self, row: dict) -> dict:
        row = dict(row)
        row["Gender"] = int(
            self.le_gender.transform([row["Gender"]])[0]
        )
        import pandas as _pd
        row["Socioeconomic_Status"] = float(
            self.oe_ses.transform(
                _pd.DataFrame([[row["Socioeconomic_Status"]]], columns=["Socioeconomic_Status"])
            )[0][0]
        )
        row["Semester"] = float(
            self.oe_semester.transform(
                _pd.DataFrame([[row["Semester"]]], columns=["Semester"])
            )[0][0]
        )
        return row

    # ── Single prediction ─────────────────────────────────────────────────
    def predict_single(self, data: StudentInput):
        if not self.best_model:
            raise RuntimeError("ML models not loaded. Run train.py first.")

        derived = compute_derived_features(data)

        raw_row = {
            "Gender":               data.Gender,
            "Age":                  data.Age,
            "Socioeconomic_Status": data.Socioeconomic_Status,
            "Level":                data.Level,
            "Semester":             data.Semester,
            "Study_Hours_Per_Week": data.Study_Hours_Per_Week,
            "Previous_CGPA":        data.Previous_CGPA,
            **derived,
        }

        encoded = self._encode_row(raw_row)
        feature_df = pd.DataFrame([encoded])[self.feature_cols]
        scaled = self.scaler.transform(feature_df)

        pred_enc = self.best_model.predict(scaled)[0]
        prediction = self.le_status.inverse_transform([pred_enc])[0]

        probabilities = {}
        confidence = 0.0
        if hasattr(self.best_model, "predict_proba"):
            probs = self.best_model.predict_proba(scaled)[0]
            classes = self.le_status.inverse_transform(self.best_model.classes_)
            probabilities = {
                str(c): round(float(p) * 100, 1)
                for c, p in zip(classes, probs)
            }
            confidence = probabilities.get(str(prediction), 0.0)

        return prediction, probabilities, confidence, derived

    # ── Batch prediction ──────────────────────────────────────────────────
    def predict_batch(self, df: pd.DataFrame):
        if not self.best_model:
            raise RuntimeError("ML models not loaded. Run train.py first.")

        result_df = df.copy()

        # Determine if derived cols are already present or need computing
        derived_cols = [
            "Previous_Course_Average", "Lowest_Previous_Score", "Weak_Previous_Count",
            "Course_CA_Average", "Lowest_CA_Score", "Weak_CA_Count",
            "Core_CA_Average", "Elective_CA_Average", "University_CA_Average",
            "Total_Units",
        ]
        has_derived = all(c in df.columns for c in derived_cols)

        if not has_derived:
            raise ValueError(
                "Batch file is missing derived columns. "
                "Please ensure the file contains the model-ready columns or "
                "use the single prediction form for manual entry."
            )

        # Encode categoricals
        enc_df = df[self.feature_cols].copy()
        enc_df["Gender"] = self.le_gender.transform(enc_df["Gender"])
        enc_df["Socioeconomic_Status"] = self.oe_ses.transform(
            enc_df[["Socioeconomic_Status"]]
        ).flatten()
        enc_df["Semester"] = self.oe_semester.transform(
            enc_df[["Semester"]]
        ).flatten()

        scaled = self.scaler.transform(enc_df)

        preds_enc = self.best_model.predict(scaled)
        predictions = self.le_status.inverse_transform(preds_enc)
        result_df["Predicted_Performance_Status"] = predictions

        # Confidence column
        if hasattr(self.best_model, "predict_proba"):
            probs = self.best_model.predict_proba(scaled)
            classes = self.le_status.inverse_transform(self.best_model.classes_)
            conf_list = []
            for i, pred in enumerate(predictions):
                idx = list(classes).index(pred)
                conf_list.append(round(float(probs[i][idx]) * 100, 1))
            result_df["Confidence"] = conf_list

        return result_df
