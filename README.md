# EduPredict AI - Student Academic Performance Prediction System

EduPredict AI is a comprehensive, full-stack machine learning application developed to predict student academic performance. By analyzing key socio-economic, pedagogical, and behavioral factors (such as attendance, study hours, and past grades), this system identifies at-risk students, allowing educators to implement timely pedagogical interventions.

This project was built as a final year academic project.

---

## 🌟 Key Features

*   **Machine Learning Engine:** Evaluates multiple algorithms (Random Forest, Logistic Regression, Gradient Boosting, SVM) and selects the best-performing model dynamically.
*   **Single & Batch Predictions:** Predict a single student's performance or upload a `.csv` file for bulk processing.
*   **Insights Dashboard:** Explores class distributions, feature importances, and model comparisons visually.
*   **Historical Database:** Automatically saves predictions to an SQLite database for persistent auditing.
*   **Interventions Engine:** Provides actionable pedagogical advice based on the model's key predictive features.
*   **Modern UI/UX:** Built with Vue 3, Tailwind CSS, and a sleek glassmorphism aesthetic.

---

## 🏗️ System Architecture

### Frontend (`/client`)
*   **Framework:** Vue.js 3 (Composition API) + Vite
*   **Styling:** Tailwind CSS (Vanilla CSS components)
*   **Routing:** Vue Router for Single Page Application navigation
*   **HTTP Client:** Axios

### Backend (`/server`)
*   **Framework:** FastAPI (Python)
*   **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
*   **Database:** SQLite (`students.db`)
*   **Testing:** Pytest & HTTPX

---

## 🚀 Getting Started

### Prerequisites
*   **Python 3.8+**
*   **Node.js 16+**

### 1. Setting up the Backend (FastAPI + Machine Learning)

1. Navigate to the server directory:
   ```bash
   cd server
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. **Train the ML Models:** Before running the server, you must train the models to generate the required `.pkl` artifacts and `insights.json`.
   ```bash
   python train.py
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn app:app --reload
   ```
   *The backend will run at `http://127.0.0.1:8000`. You can view the automatic API documentation at `http://127.0.0.1:8000/docs`.*

### 2. Setting up the Frontend (Vue 3)

1. Open a new terminal and navigate to the client directory:
   ```bash
   cd client
   ```
2. Install the Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   *The frontend will run at `http://localhost:5173`.*

---

## 🧪 Running Tests

To ensure the backend API functions correctly, a suite of unit tests has been provided.

1. Navigate to the server directory:
   ```bash
   cd server
   ```
2. Run pytest:
   ```bash
   pytest test_app.py -v
   ```

---

## 📂 Project Structure

```text
├── client/                 # Vue 3 Frontend
│   ├── src/                # Vue components, router, styles
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
│
├── server/                 # FastAPI Backend
│   ├── data/               # Contains student_data.csv
│   ├── models/             # Auto-generated ML artifacts (*.pkl, insights.json)
│   ├── app.py              # Main FastAPI application
│   ├── train.py            # ML model training script
│   ├── test_app.py         # Unit tests for the API
│   ├── EDA.ipynb           # Exploratory Data Analysis Jupyter Notebook
│   └── requirements.txt    # Python dependencies
│
└── README.md               # Project documentation
```

---

## 📝 License & Academic Honesty
This project is submitted in partial fulfillment of the requirements for a final year university degree. All rights reserved by the author.
