import os
import abstra.hooks as ah
from dotenv import load_dotenv
from slack_sdk import WebClient

# This hook uses environment variables.
load_dotenv()

slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

try:
    payload, query, headers = ah.get_request()
    client.chat_postMessage(
        channel="YOUR_CHANNEL",
        text=f"Hello {payload['firstName']} {payload['lastName']} from your app!",
    )
    ah.send_response(f"[{payload}] Successful")
except Exception as e:
    ah.send_response(f"[{payload}] Error", status_code=500)
