from fastapi import APIRouter
from pydantic import BaseModel
from app.services.twillio_client import initiate_call
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

domain = os.getenv('DOMAIN')
task_router = APIRouter()

class TaskRequest(BaseModel):
    task_description: str
    recipient_name: str
    phone_number: str

@task_router.post("/")
async def create_task(task: TaskRequest):
    # Trigger Twilio call and return response
    print("Task Created")
    print(f"Hosted on {domain}")
    logging.info(f"Task created: {task.task_description}")
    call_sid = initiate_call(task.phone_number, "f8fc-2a02-8388-c001-e080-44c9-3a30-fe66-2983.ngrok-free.app") #should be domain from .env
    print("task and call created")
    return {"status": "Call initiated", "call_sid": call_sid}
