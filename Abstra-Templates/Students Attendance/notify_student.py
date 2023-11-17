import os
import abstra.hooks as ah
import abstra.workflows as aw
from dotenv import load_dotenv
from slack_sdk import WebClient

# This hook uses environment variables.
load_dotenv()

stage = aw.get_stage()
ans = stage["ans"]
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)
if ans == "Yes":
    client.chat_postMessage(
        channel="sa_planos",
        text=f"Hey your justificative was approved! :tada:",
    )
else:
    client.chat_postMessage(
        channel="sa_planos",
        text=f"Your justificative was not approved! :cry:",
    )