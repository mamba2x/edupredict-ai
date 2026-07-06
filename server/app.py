from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db

from routes import predict, records, insights, stats

def create_app() -> FastAPI:
    app = FastAPI(title="Student Performance Prediction API", version="2.0")

    init_db()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(predict.router)
    app.include_router(records.router)
    app.include_router(insights.router)
    app.include_router(stats.router)

    @app.get("/health")
    def health_check():
        return {"status": "ok", "message": "Student Performance API is running."}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
