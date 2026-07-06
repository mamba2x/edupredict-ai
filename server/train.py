import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from config import DATASET_PATH, DATASET_SHEET, FEATURE_COLS, MODEL_DIR


def train_models():
    print("=" * 60)
    print("  EduPredict AI — CS Student Performance Model Training")
    print("=" * 60)

    # ── Load Excel Dataset ──────────────────────────────────────
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at '{DATASET_PATH}'. "
            "Please place cs_dataset.xlsx inside the server/data/ folder."
        )

    df = pd.read_excel(DATASET_PATH, sheet_name=DATASET_SHEET, engine="openpyxl")
    print(f"\n[INFO] Loaded {len(df)} records from sheet '{DATASET_SHEET}'")
    print(f"[INFO] Columns found: {list(df.columns)}")

    # ── Drop Student_ID — not a training feature ────────────────
    if "Student_ID" in df.columns:
        df = df.drop(columns=["Student_ID"])
        print("[INFO] Dropped 'Student_ID' column")

    # ── Drop rows where target is missing ───────────────────────
    df = df.dropna(subset=["Performance_Status"])
    print(f"[INFO] Records after dropping missing targets: {len(df)}")

    # ── Class distribution (raw, before encoding) ────────────────
    class_dist = df["Performance_Status"].value_counts().to_dict()
    total = len(df)
    class_dist_pct = {k: round(v / total * 100, 1) for k, v in class_dist.items()}
    print(f"[INFO] Class distribution: {class_dist}")

    # ── Encode Gender (Female=0, Male=1) ─────────────────────────
    le_gender = LabelEncoder()
    df["Gender"] = le_gender.fit_transform(df["Gender"])
    print(f"[INFO] Gender classes: {list(le_gender.classes_)}")

    # ── Encode Socioeconomic_Status (Low=0, Medium=1, High=2) ────
    oe_ses = OrdinalEncoder(categories=[["Low", "Medium", "High"]],
                            handle_unknown="use_encoded_value", unknown_value=-1)
    df["Socioeconomic_Status"] = oe_ses.fit_transform(
        df[["Socioeconomic_Status"]]
    ).flatten()

    # ── Encode Semester (First=0, Second=1) ──────────────────────
    oe_semester = OrdinalEncoder(categories=[["First", "Second"]],
                                 handle_unknown="use_encoded_value", unknown_value=-1)
    df["Semester"] = oe_semester.fit_transform(df[["Semester"]]).flatten()
    print("[INFO] Semester encoded: First=0, Second=1")

    # ── Level stays numeric (100, 200, 300, 400) ─────────────────
    df["Level"] = pd.to_numeric(df["Level"], errors="coerce")

    # ── Encode Target Label ───────────────────────────────────────
    le_status = LabelEncoder()
    df["Performance_Status"] = le_status.fit_transform(df["Performance_Status"])
    print(f"[INFO] Target classes: {list(le_status.classes_)}")

    # ── Verify all feature columns exist ─────────────────────────
    missing_features = [c for c in FEATURE_COLS if c not in df.columns]
    if missing_features:
        raise ValueError(
            f"The following required feature columns are missing from the dataset: "
            f"{missing_features}"
        )

    # ── Feature / Target split ────────────────────────────────────
    X = df[FEATURE_COLS].copy()
    y = df["Performance_Status"]

    # Drop any remaining NaN rows
    mask = X.notna().all(axis=1)
    X = X[mask]
    y = y[mask]
    print(f"[INFO] Training on {len(X)} clean records")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ── Scale numeric features ────────────────────────────────────
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # ── Define Models ─────────────────────────────────────────────
    models = {
        "Logistic Regression":  LogisticRegression(random_state=42, max_iter=1000,
                                                    class_weight="balanced"),
        "Random Forest":        RandomForestClassifier(n_estimators=200, random_state=42,
                                                        class_weight="balanced"),
        "Gradient Boosting":    GradientBoostingClassifier(n_estimators=200,
                                                            learning_rate=0.1,
                                                            random_state=42),
        "Support Vector Machine": SVC(probability=True, random_state=42,
                                       class_weight="balanced"),
    }

    insights = {
        "model_comparison": [],
        "feature_importance": [],
        "class_distribution": class_dist,
        "class_distribution_pct": class_dist_pct,
        "best_model_name": "",
        "dataset_info": {
            "total_records": total,
            "train_records": len(X_train),
            "test_records":  len(X_test),
            "features":      FEATURE_COLS,
            "target_classes": list(le_status.classes_),
        },
    }

    best_model      = None
    best_f1         = 0.0
    best_model_name = ""

    print("\n--- Model Evaluation ---")
    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)

        accuracy  = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        recall    = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        f1        = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        insights["model_comparison"].append({
            "name":      name,
            "accuracy":  round(float(accuracy),  4),
            "precision": round(float(precision), 4),
            "recall":    round(float(recall),    4),
            "f1_score":  round(float(f1),        4),
        })

        print(f"\n  {name}:")
        print(f"    Accuracy:  {accuracy:.4f}")
        print(f"    Precision: {precision:.4f}")
        print(f"    Recall:    {recall:.4f}")
        print(f"    F1-Score:  {f1:.4f}")

        # Select best by weighted F1 (robust for imbalanced classes)
        if f1 > best_f1:
            best_f1        = f1
            best_model     = model
            best_model_name = name

    print(f"\n[BEST] {best_model_name}  >>  F1: {best_f1:.4f}")
    insights["best_model_name"] = best_model_name

    # ── Feature Importance ────────────────────────────────────────
    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
    elif hasattr(best_model, "coef_"):
        importances = np.mean(np.abs(best_model.coef_), axis=0)
    else:
        importances = np.ones(len(FEATURE_COLS)) / len(FEATURE_COLS)

    fi_list = [
        {"feature": fn, "importance": round(float(imp), 6)}
        for fn, imp in zip(FEATURE_COLS, importances)
    ]
    fi_list.sort(key=lambda x: x["importance"], reverse=True)
    insights["feature_importance"] = fi_list

    max_imp = fi_list[0]["importance"] if fi_list else 1
    for item in fi_list:
        item["importance_normalised"] = round(item["importance"] / max_imp, 4)

    # ── Save All Artifacts ────────────────────────────────────────
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(best_model,  os.path.join(MODEL_DIR, "best_model.pkl"))
    joblib.dump(scaler,      os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(le_status,   os.path.join(MODEL_DIR, "le_status.pkl"))
    joblib.dump(le_gender,   os.path.join(MODEL_DIR, "le_gender.pkl"))
    joblib.dump(oe_ses,      os.path.join(MODEL_DIR, "oe_ses.pkl"))
    joblib.dump(oe_semester, os.path.join(MODEL_DIR, "oe_semester.pkl"))

    # Save feature column order so prediction always uses the same order
    with open(os.path.join(MODEL_DIR, "feature_cols.json"), "w") as f:
        json.dump(FEATURE_COLS, f, indent=2)

    with open(os.path.join(MODEL_DIR, "insights.json"), "w") as f:
        json.dump(insights, f, indent=4)

    print("\n[INFO] All artifacts saved to 'models/':")
    print("       best_model.pkl, scaler.pkl, le_status.pkl, le_gender.pkl,")
    print("       oe_ses.pkl, oe_semester.pkl, feature_cols.json, insights.json")
    print("=" * 60)


if __name__ == "__main__":
    train_models()
