from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import Response
import pandas as pd
import io
from schemas import StudentInput
from services.ml_service import MLService
from services.explanation_service import ExplanationService
from database import PredictionRepository
from config import FEATURE_COLS, VALID_LEVELS, VALID_SEMESTERS, MAX_CA_SCORE, MAX_PREV_SCORE

router = APIRouter()
ml_service = MLService()

# ── Required columns for a model-ready batch file ────────────────────────────
BATCH_REQUIRED_COLS = [
    "Gender", "Age", "Socioeconomic_Status", "Level", "Semester",
    "Study_Hours_Per_Week", "Previous_CGPA",
    "Previous_Course_Average", "Lowest_Previous_Score", "Weak_Previous_Count",
    "Course_CA_Average", "Lowest_CA_Score", "Weak_CA_Count",
    "Core_CA_Average", "Elective_CA_Average", "University_CA_Average",
    "Total_Units",
]


# ── Single Student Prediction ─────────────────────────────────────────────────
@router.post("/predict")
def predict_performance(data: StudentInput):
    try:
        prediction, probabilities, confidence, derived = ml_service.predict_single(data)

        # Save to database
        PredictionRepository.insert_prediction(data, prediction, confidence, derived)

        # Build explanations
        explanations = ExplanationService.build_explanation(data, derived)

        response = {
            "prediction":    str(prediction),
            "probabilities": probabilities,
            "confidence":    confidence,
            "explanations":  explanations,
            "derived":       derived,
        }
        if data.Student_ID:
            response["student_id"] = data.Student_ID

        return response

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Batch Prediction ──────────────────────────────────────────────────────────
@router.post("/predict/batch")
async def predict_batch(
    file: UploadFile = File(...),
    replace: bool = Form(False)
):
    try:
        filename = file.filename or ""

        # ── Parse file (CSV or Excel) ─────────────────────────────────────
        if filename.lower().endswith(".csv"):
            contents = await file.read()
            df = pd.read_csv(io.BytesIO(contents))
        elif filename.lower().endswith((".xlsx", ".xls")):
            contents = await file.read()
            excel_file = pd.ExcelFile(io.BytesIO(contents), engine="openpyxl")
            sheet_name = "Model_Ready" if "Model_Ready" in excel_file.sheet_names else 0
            df = excel_file.parse(sheet_name)
        else:
            raise HTTPException(
                status_code=400,
                detail="Only .csv or .xlsx files are supported for batch upload."
            )

        # ── Normalize values to match API expectations ───────────────────
        if "Semester" in df.columns:
            df["Semester"] = df["Semester"].replace({"Alpha": "First", "Omega": "Second"})
        if "Socioeconomic_Status" in df.columns:
            df["Socioeconomic_Status"] = df["Socioeconomic_Status"].replace({"Middle": "Medium"})

        # ── Strip Performance_Status if present (that's what we predict) ─
        if "Performance_Status" in df.columns:
            df = df.drop(columns=["Performance_Status"])

        # ── Validate required model-ready columns ─────────────────────────
        missing = [c for c in BATCH_REQUIRED_COLS if c not in df.columns]
        if missing:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Missing required columns: {', '.join(missing)}. "
                    f"The batch file must contain all model-ready feature columns. "
                    f"Required: {', '.join(BATCH_REQUIRED_COLS)}"
                )
            )

        # ── Per-row validation ────────────────────────────────────────────
        errors = []
        for i, row in df.iterrows():
            row_num = i + 2  # 1-indexed with header
            if row["Gender"] not in ["Male", "Female"]:
                errors.append(f"Row {row_num}: Invalid Gender '{row['Gender']}'")
            if row["Socioeconomic_Status"] not in ["Low", "Medium", "High"]:
                errors.append(f"Row {row_num}: Invalid Socioeconomic_Status '{row['Socioeconomic_Status']}'")
            try:
                lvl = int(row["Level"])
                if lvl not in VALID_LEVELS:
                    errors.append(f"Row {row_num}: Invalid Level {lvl} (must be 100/200/300/400)")
            except (ValueError, TypeError):
                errors.append(f"Row {row_num}: Level must be a number (100/200/300/400)")
            if str(row["Semester"]) not in VALID_SEMESTERS:
                errors.append(f"Row {row_num}: Invalid Semester '{row['Semester']}' (must be First/Second)")
            if float(row.get("Lowest_CA_Score", 0)) > MAX_CA_SCORE:
                errors.append(f"Row {row_num}: Lowest_CA_Score {row['Lowest_CA_Score']} exceeds max {MAX_CA_SCORE}")
            if float(row.get("Lowest_Previous_Score", 0)) > MAX_PREV_SCORE:
                errors.append(f"Row {row_num}: Lowest_Previous_Score {row['Lowest_Previous_Score']} exceeds max {MAX_PREV_SCORE}")

        if errors:
            raise HTTPException(
                status_code=422,
                detail={"message": "Validation errors in uploaded file", "errors": errors[:20]}
            )

        # ── Run predictions ───────────────────────────────────────────────
        result_df = ml_service.predict_batch(df)

        # Keep Student_ID in output if present
        if "Student_ID" in df.columns:
            result_df["Student_ID"] = df["Student_ID"].values

        # Save to DB
        if replace:
            PredictionRepository.replace_predictions(result_df)
        else:
            PredictionRepository.insert_predictions(result_df)

        # ── Return as CSV download ────────────────────────────────────────
        out_cols = []
        if "Student_ID" in result_df.columns:
            out_cols.append("Student_ID")
        out_cols += ["Predicted_Performance_Status"]
        if "Confidence" in result_df.columns:
            out_cols.append("Confidence")
        # Append remaining columns
        remaining = [c for c in result_df.columns if c not in out_cols]
        out_cols += remaining

        csv_data = result_df[out_cols].to_csv(index=False)
        safe_name = filename.replace(" ", "_")
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=predictions_{safe_name}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
