# EduPredict AI PlantText UML Diagrams (Updated with Student Actor)

This document contains simplified, high-level PlantUML/PlantText source codes for the four core diagrams of the **EduPredict AI** system. These versions reflect the addition of the **Student** actor (who can run self-assessment single predictions, while the Advisor retains access to cohort batches, dashboards, and audit logs).

Copy the code for each diagram and paste it directly into [PlantText](https://www.planttext.com).

---

## 1. System Architecture Diagram
```plantuml
@startuml EduPredict_AI_System_Architecture

skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 8
skinparam Shadowing false
skinparam DefaultFontName "Arial"
skinparam DefaultFontSize 12
skinparam ArrowColor #64748B
skinparam ArrowThickness 1.5

skinparam rectangle {
    BackgroundColor #FFFFFF
    BorderColor #CBD5E1
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

node "Client Browser" {
    rectangle "Vue 3 SPA Frontend" as VueApp #EFF6FF {
        component "Student Self-Predict Portal\n(Single Prediction Form)" as StudentUI
        component "Advisor Admin Dashboard\n(Batch Upload, Analytics, Logs)" as AdvisorUI
    }
}

node "Application Server" {
    rectangle "FastAPI Service API" as FastAPI #ECFDF5 {
        component "API Gateways & Router\n(/predict, /predict/batch, /stats, /records)" as API
    }

    rectangle "Core Services Layer" as Services #F5F3FF {
        component "ML Inference Engine\n(Random Forest Classifier)" as MLEngine #8B5CF6
        component "Explanation Service\n(Rules Heuristics)" as ExplService #A78BFA
        component "Prediction Repository\n(Data Access Layer)" as Repository #C084FC
    }
}

node "Local Storage / Assets" {
    folder "Trained ML Artifacts" as MLArtifacts #FEE2E2 {
        file "Model & Scaler Pickles\n(model.pkl, scaler.pkl)" as ModelPKL
    }
    
    database "SQLite Database\n(students.db)" as DB #FEF3C7
}

' Connections
StudentUI -[#3B82F6]-> API : Run Single Prediction (POST /predict)
AdvisorUI -[#3B82F6]-> API : Admin & Batch Actions

API -[#10B981]-> MLEngine : Raw Inputs
API -[#10B981]-> ExplService : Heuristics Request

MLEngine -[#EF4444]-> ModelPKL : Load weights & scaling
MLEngine -[#8B5CF6]-> Repository : Predictions & Conf
ExplService -[#8B5CF6]-> Repository : Pos/Neg Drivers

API -[#8B5CF6]-> Repository : Queries & logs
Repository -[#F59E0B]-> DB : SQL insert / query

@enduml
```

---

## 2. Use Case Diagram
```plantuml
@startuml EduPredict_AI_Use_Cases

skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 8
skinparam Shadowing false
skinparam DefaultFontName "Arial"
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
actor "Student" as Student

rectangle "EduPredict AI System" as System {
    usecase "Run Single Prediction\n(Self-Assessment & Advice)" as UC1
    usecase "Run Batch Prediction\n(Cohort Upload & Export)" as UC2
    usecase "View Analytics Dashboard\n(KPIs & Charts)" as UC3
    usecase "Audit Historic Logs\n(Search & Clear Records)" as UC4
}

Advisor --> UC1
Advisor --> UC2
Advisor --> UC3
Advisor --> UC4

Student --> UC1

@enduml
```

---

## 3. Sequence Diagram (Prediction Process)
```plantuml
@startuml EduPredict_AI_Prediction_Sequence

skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 8
skinparam Shadowing false
skinparam DefaultFontName "Arial"
skinparam DefaultFontSize 12
skinparam ArrowColor #475569
skinparam ArrowThickness 1.5

skinparam ParticipantPadding 10
skinparam BoxPadding 10

skinparam participant {
    BackgroundColor #FFFFFF
    BorderColor #94A3B8
    FontColor #1E293B
}

actor User as "Advisor / Student" #EFF6FF
participant UI as "Vue 3 Client"
participant API as "FastAPI Server"
participant ML as "ML & Heuristics"
database DB as "SQLite DB"

autonumber

== Scenario 1: Single Student Prediction (Advisor or Student) ==

User -> UI: Input metrics & click "Run Prediction"
activate UI
UI -> API: HTTP POST /predict (StudentInput)
activate API
API -> ML: Run Inference & Heuristics
activate ML
Note over ML: Scale inputs -> Predict RF -> Evaluate Rules
ML --> API: Return prediction category & drivers
deactivate ML
API -> DB: Log prediction record
activate DB
DB --> API: Confirmation
deactivate DB
API --> UI: Return JSON results & advice
deactivate API
UI --> User: Display gauge charts & advice
deactivate UI

== Scenario 2: Batch Cohort Prediction (Advisor Only) ==

User -> UI: Select Excel/CSV file & click "Upload"
activate UI
UI -> API: HTTP POST /predict/batch (Multipart File)
activate API
API -> ML: Run batch prediction
activate ML
ML --> API: Return prediction dataset
deactivate ML
API -> DB: Bulk insert records
activate DB
DB --> API: Confirmation
deactivate DB
API --> UI: Return prediction CSV stream
deactivate API
UI --> User: Auto-download result report (.csv)
deactivate UI

@enduml
```

---

## 4. Class Diagram (Backend Components)
```plantuml
@startuml EduPredict_AI_Class_Diagram

skinparam BackgroundColor #F8FAFC
skinparam RoundCorner 8
skinparam Shadowing false
skinparam DefaultFontName "Arial"
skinparam DefaultFontSize 12
skinparam ArrowColor #475569
skinparam ArrowThickness 1.5

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

@enduml
```
