import os
import abstra.hooks as ah
import abstra.workflows as aw
from dotenv import load_dotenv
from slack_sdk import WebClient

# This hook uses environment variables.
load_dotenv()

email = stage["email"]
name = stage["name"]
country = stage["country"]

slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

client.chat_postMessage(
    channel="sa_planos",
    text=f"Hey team, the {name} ({email}) from {brazil} is interested in our services. We are going to contact him soon. :tada:",
)
