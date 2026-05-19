import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.database.connection import init_db
from backend.routes.auth_routes import router as auth_router
from backend.routes.upload_routes import router as upload_router
from backend.routes.rag_routes import router as rag_router


app = FastAPI(
    title="DocuMind AI",
    description="RAG-based context-aware document QA system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup():
    """
    Runs once when server starts.
    Creates DB tables if they don't exist.
    """
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)
    init_db()
    print("App started. Tables ready.")


app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(rag_router)


@app.get("/")
def root():
    return {
        "status": "running",
        "app": "DocuMind AI",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
