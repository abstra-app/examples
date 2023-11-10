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
date_month = stage["date_month"]
date_day = stage["date_day"]
time_hour = stage["time_hour"]
time_minute = stage["time_minute"]
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

try:
    payload, query, headers = ah.get_request()
    client.chat_postMessage(
        channel="YOUR_CHANNEL",
<<<<<<< HEAD:Abstra-Templates/Customer-Onboarding/slack_notification.py
        text=f"Hey team, the {name} ({email}) from {country} is interested in our services. We are going to contact him soon. :tada:",
    )
=======
        text=f"Hey team, the {name} ({email}) from {country} is interested in our services. We are going to have a meeting with him at
        " + time_hour + ":" + time_minute + " on " + date_day + "/"+ date_month   + ". :tada:",
)
>>>>>>> 164968c77c5b510c836944e991e8596e7e4e990e:Abstra-Templates/Meeting-Schedule/slack-notification.py
    ah.send_response(f"[{payload}] Ok")
except Exception as e:
    ah.send_response(f"[{payload}] Error", status_code=500)
