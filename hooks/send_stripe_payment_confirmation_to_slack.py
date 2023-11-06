import os
import sys
import json
from uuid import uuid4
from datetime import datetime

import stripe
import requests
import abstra.hooks as ah
from dotenv import load_dotenv

# This hook uses environment variables. To make it work properly, add Stripe and Slack API Key and a Stripe Webhook secret to your workspace's environment variables in the sidebar.
load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
hook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
slack_token = os.environ.get("SLACK_BOT_TOKEN")
req_sig = f"{datetime.now()} - {uuid4()}"

print(stripe.api_key)
def slack_msg(message, channel):
    res = requests.post(
        "https://slack.com/api/chat.postMessage",
        json={"channel": channel, "text": message},
        headers={
            "Authorization": "Bearer " + slack_token,
            "Content-type": "application/json; charset=utf-8",
        },
    )


try:
    # Stripe event
    payload, query, headers = ah.get_request()
    sig_header = headers.get("Stripe-Signature")
    event = stripe.Webhook.construct_event(payload, sig_header, hook_secret)
    print(sig_header)
    if event["type"] != "payment_intent.succeeded":
        raise Exception("Unhandled event type {}".format(event["type"]))
    ah.send_response(f"[{req_sig}] Processing")

    event_obj = event["data"]["object"]
    amount_str = f"{event_obj['currency']} {event_obj['amount'] / 100}"

    # Get stripe customer email
    customer_email = stripe.Customer.retrieve(event_obj["customer"])["email"]

    # Send a message in slack when the event fires
    slack_msg(f"{customer_email} paid {amount_str}", "sales")
except Exception as e:
    ah.send_response(f"[{req_sig}] Error", status_code=500)
    sys.exit(1)
