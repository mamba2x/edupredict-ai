# EduPredict AI PlantUML Diagrams

This document contains the PlantUML source code for the four core diagrams of the **EduPredict AI** system. You can copy the code for each diagram and paste it into [plantuml.com](https://www.plantuml.com) or use a local PlantUML renderer to generate the images.

---

## 1. System Architecture Diagram
This diagram represents the deployment and architectural layers of the EduPredict AI system, showing the Vue 3 frontend, FastAPI backend, ML service pipeline, and database persistence layers.

```plantuml
@startuml EduPredict_AI_System_Architecture

!theme carbon
skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 10
skinparam Shadowing false
skinparam DefaultFontName "Helvetica Neue", Arial, sans-serif
skinparam DefaultFontSize 12
skinparam ArrowColor #64748B
skinparam ArrowThickness 1.5

' Custom styling colors
!define FE_COLOR #3B82F6
!define BE_COLOR #10B981
!define ML_COLOR #8B5CF6
!define DB_COLOR #F59E0B
!define DOC_COLOR #EF4444

skinparam rectangle {
    BackgroundColor #FFFFFF
    BorderColor #E2E8F0
    FontColor #1E293B
}

skinparam database {
    BackgroundColor #FEF3C7
    BorderColor #F59E0B
    FontColor #78350F
}

skinparam node {
    BackgroundColor #EFF6FF
    BorderColor #3B82F6
    FontColor #1E3A8A
}

title System Architecture of EduPredict AI

node "Client Browser" as ClientBrowser {
    rectangle "Vue 3 SPA (Frontend)" as VueApp #EFF6FF {
        component "Dashboard View\n(ChartJS Analytics)" as Dashboard
        component "Single Prediction Form" as PredictForm
        component "Batch Upload Zone\n(CSV/Excel Drag-and-Drop)" as BatchUpload
        component "Interventions Page" as Interventions
        component "Student Database View" as DBView
    }
}

node "Application Server" as AppServer {
    rectangle "FastAPI Service API" as FastAPI #ECFDF5 {
        component "API Router & Gateway" as Gateway
        component "/predict\n(Single Inference)" as PredictEndpoint
        component "/predict/batch\n(Bulk Inference)" as BatchPredictEndpoint
        component "/stats\n(Dashboard Metrics)" as StatsEndpoint
        component "/records\n(Historic Logs)" as RecordsEndpoint
    }

    rectangle "Core Services Layer" as Services #F5F3FF {
        component "ML Inference Engine" as MLEngine #8B5CF6 {
            component "Random Forest Classifier" as RFClassifier
            component "StandardScaler" as Scaler
            component "Label/Ordinal Encoders" as Encoders
        }
        component "Explanation Service\n(Heuristics Engine)" as ExplService #A78BFA
        component "Prediction Repository\n(Data Access Layer)" as Repository #C084FC
    }
}

node "Local Storage / Assets" as StorageAssets {
    folder "Trained ML Artifacts" as MLArtifacts #FEE2E2 {
        file "best_model.pkl\n(Random Forest)" as ModelPKL
        file "scaler.pkl\n(StandardScaler)" as ScalerPKL
        file "encoders.pkl\n(LE / OE Encoders)" as EncodersPKL
    }
    
    database "SQLite Database\n(students.db)" as DB #FEF3C7 {
        entity "predictions table" as PredictionsTable
    }
}

' Layout and connections
VueApp -[#3B82F6]-> Gateway : HTTP REST API Requests\n(Axios / JSON / Multipart FormData)
Gateway -[#10B981]-> PredictEndpoint
Gateway -[#10B981]-> BatchPredictEndpoint
Gateway -[#10B981]-> StatsEndpoint
Gateway -[#10B981]-> RecordsEndpoint

PredictEndpoint -[#8B5CF6]-> MLEngine : Sends raw input data
PredictEndpoint -[#8B5CF6]-> ExplService : Invokes heuristics
BatchPredictEndpoint -[#8B5CF6]-> MLEngine : Sends cohort DataFrame

MLEngine -[#EF4444]-> MLArtifacts : Loads .pkl models at startup
MLEngine -[#8B5CF6]-> Repository : Returns predictions & metrics
ExplService -[#8B5CF6]-> Repository : Returns positive/negative drivers

RecordsEndpoint -[#8B5CF6]-> Repository : Fetch historical logs
StatsEndpoint -[#8B5CF6]-> Repository : Fetch aggregated metrics

Repository -[#F59E0B]-> DB : Persists logs / Executes SQL queries

@enduml
```

---

## 2. Use Case Diagram
This diagram outlines the core use cases available to the Academic Advisor or Educator interacting with the EduPredict AI platform.

```plantuml
@startuml EduPredict_AI_Use_Cases

!theme carbon
skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 10
skinparam Shadowing false
skinparam DefaultFontName "Helvetica Neue", Arial, sans-serif
skinparam DefaultFontSize 12
skinparam ArrowColor #64748B
skinparam ArrowThickness 1.5

skinparam actor {
    BackgroundColor #EFF6FF
    BorderColor #3B82F6
    FontColor #1E3A8A
}

skinparam usecase {
    BackgroundColor #FFFFFF
    BorderColor #64748B
    FontColor #1E293B
}

left to right direction

actor "Academic Advisor / Educator" as Advisor

rectangle "EduPredict AI System" as System {
    usecase "Run Single Student Prediction" as UC_Single
    usecase "Input Student Demographics &\nAcademic Metrics" as UC_Input
    usecase "Generate Pedagogical Advice\n& Risk Explanations" as UC_Explain
    
    usecase "Run Batch Cohort Prediction" as UC_Batch
    usecase "Upload CSV/Excel Dataset" as UC_Upload
    usecase "Export Prediction CSV Report" as UC_Export
    
    usecase "View Visual Dashboard Analytics" as UC_Dashboard
    usecase "View KPI Cards & Charts\n(Prediction Distributions)" as UC_Charts
    
    usecase "Audit Historic Prediction Logs" as UC_Logs
    usecase "Search, Filter & Review Logs" as UC_Review
    usecase "Clear Database logs" as UC_Clear
}

' Associations
Advisor --> UC_Single
Advisor --> UC_Batch
Advisor --> UC_Dashboard
Advisor --> UC_Logs

' Includes and Extends relations
UC_Single ..> UC_Input : <<include>>
UC_Single ..> UC_Explain : <<include>>

UC_Batch ..> UC_Upload : <<include>>
UC_Batch ..> UC_Export : <<include>>

UC_Dashboard ..> UC_Charts : <<include>>

UC_Logs ..> UC_Review : <<include>>
UC_Logs ..> UC_Clear : <<extend>>

@enduml
```

---

## 3. Sequence Diagram (Prediction Process)
This sequence diagram tracks single and batch prediction requests as they travel from the client application through the FastAPI server to the ML service and persistence repository.

```plantuml
@startuml EduPredict_AI_Prediction_Sequence

!theme carbon
skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 10
skinparam Shadowing false
skinparam DefaultFontName "Helvetica Neue", Arial, sans-serif
skinparam DefaultFontSize 12
skinparam ArrowColor #475569
skinparam ArrowThickness 1.5

skinparam ParticipantPadding 10
skinparam BoxPadding 10

' Coloring participants
skinparam participant {
    BackgroundColor #FFFFFF
    BorderColor #94A3B8
    FontColor #1E293B
}

actor Advisor as "Academic Advisor\n(User)" #EFF6FF

box "Presentation Layer" #F1F5F9
    participant UI as "Vue 3 Client\n(Vite App)"
end box

box "Backend API Gateway" #ECFDF5
    participant Server as "FastAPI App\n(app.py)"
end box

box "Business Logic & ML Layer" #F5F3FF
    participant ML as "ML Service\n(ml_service.py)"
    participant Exp as "Explanation Service\n(heuristics.py)"
end box

box "Data Persistence" #FEF3C7
    participant Repository as "PredictionRepository\n(repository.py)"
    database DB as "SQLite DB\n(students.db)"
end box

autonumber

== Scenario 1: Single Student Prediction ==

Advisor -> UI: Fills prediction form & clicks "Run Prediction"
activate UI
UI -> UI: Validate input ranges\n(Age 15-60, CGPA 0-5)
UI -> Server: HTTP POST /predict (StudentInput JSON)
activate Server

Server -> Server: Parse payload & normalize inputs\n(e.g., Term "Alpha" -> "First")
Server -> ML: predict_single(student_data)
activate ML

Note over ML: Load scaler.pkl,\nbest_model.pkl & encoders

ML -> ML: Apply Gender LabelEncoder\n(Female -> 0, Male -> 1)
ML -> ML: Apply SES & Semester OrdinalEncoders
ML -> ML: Compute derived features\n(e.g., Course CA Average,\nWeak CA Count, Core CA Average)
ML -> ML: Scale 17-feature vector\n(StandardScaler)
ML -> ML: Execute best_model.predict_proba()

ML --> Server: Return prediction category & confidence
deactivate ML

Server -> Exp: build_explanation(student_data, derived_features)
activate Exp
Note over Exp: Evaluate values against thresholds\n(e.g., study hours < 8 or CA < 14)
Exp --> Server: Return lists of positive & negative risk drivers
deactivate Exp

Server -> Repository: insert_prediction(data, status, confidence, derived)
activate Repository
Repository -> DB: Exec SQL INSERT statement
activate DB
DB --> Repository: Confirmation
deactivate DB
Repository --> Server: Prediction logged successfully
deactivate Repository

Server --> UI: HTTP 200 OK (Prediction JSON + Explanations)
deactivate Server

UI --> Advisor: Render prediction result gauge,\npositive/negative factors, and advice
deactivate UI

== Scenario 2: Batch Cohort Prediction ==

Advisor -> UI: Drag-and-drop Excel/CSV & clicks "Upload"
activate UI
UI -> UI: Verify file extension\n(.xlsx / .csv)
UI -> Server: HTTP POST /predict/batch (Multipart FormData)
activate Server

Server -> Server: Parse file & extract records\ninto Pandas DataFrame
Server -> ML: predict_batch(dataframe)
activate ML
Note over ML: Preprocess, encode, scale,\nand run batch model inference
ML --> Server: Return DataFrame with status & confidence
deactivate ML

Server -> Repository: insert_predictions(result_df)
activate Repository
Repository -> DB: Exec batch SQL INSERT statements
activate DB
DB --> Repository: Confirmation
deactivate DB
Repository --> Server: Batch logs saved
deactivate Repository

Server --> UI: HTTP 200 OK (Returns predicted CSV file stream)
deactivate Server
UI --> Advisor: Automatically triggers file download (.csv)
deactivate UI

@enduml
```

---

## 4. Class Diagram (Backend Components)
This class diagram details the FastAPI routes, data transfer schemas, services, and repositories that power the EduPredict AI backend system.

```plantuml
@startuml EduPredict_AI_Class_Diagram

!theme carbon
skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 10
skinparam Shadowing false
skinparam DefaultFontName "Helvetica Neue", Arial, sans-serif
skinparam DefaultFontSize 12
skinparam ArrowColor #475569
skinparam ArrowThickness 1.5

' Styling class boxes
skinparam class {
    BackgroundColor #FFFFFF
    BorderColor #94A3B8
    HeaderBackgroundColor #EFF6FF
    FontColor #1E293B
    AttributeFontColor #475569
    MethodFontColor #0F172A
}

title Class Diagram of EduPredict AI Backend Components

class FastAPIApp {
    + app : FastAPI
    + predict_performance(data: StudentInput) : dict
    + predict_batch(file: UploadFile, replace: bool) : Response
    + get_stats() : dict
    + get_records() : list
}

class StudentInput {
    + Student_ID : Optional<str>
    + Gender : str
    + Age : int
    + Socioeconomic_Status : str
    + Level : int
    + Semester : str
    + Study_Hours_Per_Week : float
    + Previous_CGPA : float
    + Entry_Academic_Score : Optional<float>
    + previous_scores : List<float>
    + core_ca_scores : List<float>
    + elective_ca_scores : List<float>
    + university_ca_scores : List<float>
    + nuc_ca_scores : List<float>
    + validate_gender(v: str) : str
    + validate_prev_scores(v: list) : list
}

class MLService {
    - {static} _instance : MLService
    + best_model : RandomForestClassifier
    + scaler : StandardScaler
    + le_status : LabelEncoder
    + le_gender : LabelEncoder
    + oe_ses : OrdinalEncoder
    + oe_semester : OrdinalEncoder
    + load_models() : void
    + predict_single(data: StudentInput) : tuple
    + predict_batch(df: DataFrame) : DataFrame
    - _derive_features(data: StudentInput) : dict
}

class ExplanationService {
    + build_explanation(data: StudentInput, derived: dict) : list
}

class PredictionRepository {
    + insert_prediction(data: StudentInput, status: str, conf: float, derived: dict) : void
    + insert_predictions(dataframe: DataFrame) : void
    + replace_predictions(dataframe: DataFrame) : void
    + get_record_count() : int
    + get_recent_records(limit: int) : list
    + delete_all_records() : void
}

class DatabaseConnection {
    + DB_FILE : str
    + init_db() : void
    + get_db() : Connection
}

' Relationships
FastAPIApp ..> StudentInput : Validates >
FastAPIApp --> MLService : Invokes >
FastAPIApp --> ExplanationService : Invokes >
FastAPIApp --> PredictionRepository : Invokes >
MLService ..> StudentInput : Processes >
PredictionRepository --> DatabaseConnection : Connects to >
PredictionRepository ..> StudentInput : Saves >

@enduml
```
