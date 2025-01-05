from twilio.rest import Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
client = Client(account_sid, auth_token)
def initiate_call(phone_number, domain):
    """
    Initiates a Twilio call and connects it to a WebSocket stream.
    Tracks call lifecycle using statusCallback.
    """
    print("Initiating Call")
    call = client.calls.create(
        record=True,
        to=phone_number,
        from_=twilio_number,
        twiml=f"""
        <Response>
            <Start>
                <Stream url="wss://{domain}/api/voice/stream" />
            </Start>
            <Pause length="60" /> <!-- Keeps the call alive for 60 seconds of silence -->
        </Response>
        """,
        status_callback=f"https://{domain}/api/status-callback",
        status_callback_event=["initiated", "ringing", "answered", "completed"]
    )
    return call.sid
