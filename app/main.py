from fastapi import FastAPI
from app1.api.tasks import task_router
from app1.api.voice_webhook import voice_router
from app1.api.status_callback import status_router
app = FastAPI()

# Include routers
app.include_router(task_router, prefix="/api/tasks")
app.include_router(voice_router, prefix="/api/voice")
app.include_router(status_router, prefix="/api")
@app.get("/")
def root():
    return {"message": "AI-powered calling agent is running"}
