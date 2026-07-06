import pytest
from fastapi.testclient import TestClient
from app import app, init_db

# Initialize the DB so tests have a table to write to
init_db()

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Student Performance API is running."}

def test_predict_single_student_valid():
    payload = {
        "Age": 21,
        "Gender": "Female",
        "Socioeconomic_Status": "High",
        "Attendance_Percentage": 95.0,
        "Study_Hours_Per_Week": 20.0,
        "Previous_Term_Grade": 85.0,
        "Continuous_Assessment_Score": 40.0
    }
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probabilities" in data
    assert "explanations" in data
    assert len(data["explanations"]) > 0

def test_predict_single_student_invalid():
    # Missing required fields like 'Continuous_Assessment_Score'
    payload = {
        "Age": 21,
        "Gender": "Female",
        "Socioeconomic_Status": "High",
        "Attendance_Percentage": 95.0,
        "Study_Hours_Per_Week": 20.0,
        "Previous_Term_Grade": 85.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422 # FastAPI validation error

def test_get_insights():
    response = client.get("/insights")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "feature_importance" in data
        assert "model_comparison" in data
        assert "best_model_name" in data

def test_get_records():
    response = client.get("/records")
    assert response.status_code == 200
    data = response.json()
    assert "records" in data
    assert isinstance(data["records"], list)
