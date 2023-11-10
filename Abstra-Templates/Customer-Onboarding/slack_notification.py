import os
import abstra.hooks as ah
import abstra.workflows as aw
from dotenv import load_dotenv
from slack_sdk import WebClient

# This hook uses environment variables.
load_dotenv()

stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

try:
    payload, query, headers = ah.get_request()
    client.chat_postMessage(
        channel="YOUR_CHANNEL",
        text=f"Hey team, the {name} ({email}) from {country} is interested in our services. We are going to contact him soon. :tada:",
    )
    ah.send_response(f"[{payload}] Ok")
except Exception as e:
    ah.send_response(f"[{payload}] Error", status_code=500)
