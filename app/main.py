from fastapi import FastAPI
from app.api.tasks import task_router
from app.api.voice_webhook import voice_router
from app.api.status_callback import status_router
app = FastAPI()

# Include routers
app.include_router(task_router, prefix="/api/tasks")
app.include_router(voice_router, prefix="/api/voice")
app.include_router(status_router, prefix="/api")
@app.get("/")
def root():
    print("AI-powered calling agent is running")
    return {"message": "AI-powered calling agent is running"}
