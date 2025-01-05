from fastapi import APIRouter, Request, Form
import logging

status_router = APIRouter()


@status_router.post("/status-callback")
async def status_callback(request: Request):
    try:

        form_data = await request.form()  # Get form data
        data = dict(form_data)

        # Extract important fields
        call_sid = data.get("CallSid", "Unknown")
        call_status = data.get("CallStatus", "Unknown")
        caller = data.get("Caller", "Unknown")
        to = data.get("To", "Unknown")

        print(f"Call SID: {call_sid}, Call Status: {call_status}, Caller: {caller}, To: {to}")

        # Handle various statuses
        if call_status == "initiated":
            print("Call initiated")
        elif call_status == "completed":
            print("Call completed.")
        elif call_status == "busy":
            print("Call failed due to a busy line.")
        elif call_status == "failed":
            print("Call failed.")
        else:
            print(f"Other Call Status: {call_status}")

        return {"status": "received"}

    except Exception as e:
        logging.error(f"Error processing status callback: {e}")
        return {"status": "error", "message": str(e)}
