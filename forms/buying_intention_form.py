"""
This scripts is used in Abstra Cloud (https://abstracloud.com) to collect buying intentions.
This is a good example on how using Python scripts can be much simpler than forms + external automations
"""

from abstra.forms import *
from requests import post
import os
from dotenv import load_dotenv
from slack_sdk import WebClient

# This form uses an environment variable. To make it work properly, add a Slack API Key to your wPorkspace's environment variables in the sidebar.
token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=token)
if "plan" in url_params:
    plan = url_params["plan"]
else:
    plan = "standard"

display(
    "Thank you for showing interest in our "
    + plan
    + " plan. We need some informations to get in touch."
)
name = read("Name")
email = read_email("Email")
company = read("Company name")

"""
This is the quickest way you can avoid sending messages
when someone on your company tests your script.
"""
if '@abstra.app' not in email:
    res = client.chat_postMessage(
        channel="sa_planos",
        text="Someone is interested in the "
        + plan
        + " plan. Their name is "
        + name
        + " and their email is "
        + email
        + ". Their company name is "
        + company
        + ".",
    )

display("We've got your information, we'll get in contact soon! 😉")
