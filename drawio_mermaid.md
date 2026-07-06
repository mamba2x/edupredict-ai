# EduPredict AI Mermaid Diagrams for Draw.io (Simplified & Compact)

This document contains simplified, high-level Mermaid source codes for the four core diagrams of the **EduPredict AI** system. These versions are designed to be much more compact and clear, preventing layout sprawl or overlapping lines in Draw.io.

Import these directly into Draw.io via **+ (Insert) > Advanced > Mermaid**.

---

## 1. System Architecture Diagram
```mermaid
flowchart TD
    subgraph Client ["Client Browser"]
        UI["Vue 3 SPA Frontend<br>(Dashboard, Form, Upload, Database Views)"]
    end

    subgraph Server ["Application Server"]
        API["FastAPI Service API<br>(/predict, /predict/batch, /stats, /records)"]
        MLE["ML Inference Engine<br>(Random Forest Classifier)"]
        EXP["Explanation Service<br>(Rules-Based Heuristics)"]
        REP["Prediction Repository<br>(Data Access Layer)"]
    end

    subgraph Storage ["Local Storage & Assets"]
        PKL["ML Artifacts<br>(model, scaler, encoders pkls)"]
        DB[("SQLite Database<br>(students.db)")]
    end

    %% Connections
    UI -->|HTTP Requests / Axios| API
    API -->|Raw Inputs| MLE
    API -->|Heuristics Request| EXP
    
    MLE -->|Load Encodings/Weights| PKL
    MLE -->|Prediction & Confidence| REP
    EXP -->|Positive/Negative Drivers| REP
    API -->|Logs & Stats Queries| REP
    
    REP -->|SQL Insert / Query| DB

    %% Custom Styles for Draw.io
    style Client fill:#EFF6FF,stroke:#3B82F6,stroke-width:1.5px
    style Server fill:#ECFDF5,stroke:#10B981,stroke-width:1.5px
    style Storage fill:#FEF3C7,stroke:#F59E0B,stroke-width:1.5px
    style UI fill:#FFFFFF,stroke:#CBD5E1
    style API fill:#FFFFFF,stroke:#CBD5E1
    style MLE fill:#F5F3FF,stroke:#8B5CF6
    style EXP fill:#F5F3FF,stroke:#8B5CF6
    style REP fill:#F5F3FF,stroke:#8B5CF6
    style PKL fill:#FEE2E2,stroke:#EF4444
    style DB fill:#FFFFFF,stroke:#F59E0B
```

---

## 2. Use Case Diagram
```mermaid
flowchart LR
    Advisor["Academic Advisor"]
    
    subgraph System ["EduPredict AI System"]
        UC1(["Run Single Prediction<br>(Includes Explanations & Advice)"])
        UC2(["Run Batch Prediction<br>(Includes Excel/CSV Upload & Report Export)"])
        UC3(["View Analytics Dashboard<br>(KPIs & Charts)"])
        UC4(["Audit Historic Logs<br>(Search & Clear Records)"])
    end

    Advisor --> UC1
    Advisor --> UC2
    Advisor --> UC3
    Advisor --> UC4

    %% Custom Styles for Draw.io
    style Advisor fill:#EFF6FF,stroke:#3B82F6,stroke-width:2px,color:#1E3A8A
    style UC1 fill:#FFFFFF,stroke:#64748B
    style UC2 fill:#FFFFFF,stroke:#64748B
    style UC3 fill:#FFFFFF,stroke:#64748B
    style UC4 fill:#FFFFFF,stroke:#64748B
```

---

## 3. Sequence Diagram (Prediction Process)
```mermaid
sequenceDiagram
    autonumber
    actor Advisor as Advisor
    participant UI as Vue 3 Client
    participant API as FastAPI Server
    participant ML as ML & Heuristics
    participant DB as SQLite DB

    Note over Advisor, DB: Scenario 1: Single Student Prediction
    Advisor->>UI: Input metrics & click "Run Prediction"
    activate UI
    UI->>API: HTTP POST /predict (StudentInput)
    activate API
    API->>ML: Run Inference & Heuristics
    activate ML
    Note over ML: Scale inputs -> Predict RF -> Evaluate Rules
    ML-->>API: Return prediction category & drivers
    deactivate ML
    API->>DB: Log prediction record
    API-->>UI: Return JSON results & advice
    deactivate API
    UI-->>Advisor: Display gauge charts & advice
    deactivate UI

    Note over Advisor, DB: Scenario 2: Batch Cohort Prediction
    Advisor->>UI: Select Excel/CSV file & click "Upload"
    activate UI
    UI->>API: HTTP POST /predict/batch (Multipart File)
    activate API
    API->>ML: Run batch prediction
    activate ML
    ML-->>API: Return prediction dataset
    deactivate ML
    API->>DB: Bulk insert records
    API-->>UI: Return prediction CSV stream
    deactivate API
    UI-->>Advisor: Auto-download result report (.csv)
    deactivate UI
```

---

## 4. Class Diagram (Backend Components)
```mermaid
classDiagram
    class FastAPIApp {
        +app: FastAPI
        +predict_performance(data: StudentInput) dict
        +predict_batch(file: UploadFile) Response
        +get_stats() dict
        +get_records() list
    }

    class StudentInput {
        +Student_ID: str
        +Demographics: Gender, Age, SES
        +AcademicInfo: Level, Semester, StudyHours, CGPA
        +Scores: course/CA lists
        +validate()
    }

    class MLService {
        +best_model: RandomForestClassifier
        +scaler: StandardScaler
        +encoders: Encoders
        +predict_single(data) tuple
        +predict_batch(df) DataFrame
    }

    class ExplanationService {
        +build_explanation(data, derived) list
    }

    class PredictionRepository {
        +insert_prediction(data, status, conf) void
        +insert_predictions(df) void
        +get_stats() dict
        +get_recent_records() list
    }

    FastAPIApp --> StudentInput : Validates
    FastAPIApp --> MLService : Invokes
    FastAPIApp --> ExplanationService : Invokes
    FastAPIApp --> PredictionRepository : Invokes
    MLService ..> StudentInput : Processes
    PredictionRepository ..> StudentInput : Saves
```
