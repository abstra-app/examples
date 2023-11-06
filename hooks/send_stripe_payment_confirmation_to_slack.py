import os
import abstra.hooks as ah
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk import WebClient

# This hook uses environment variables. To make it work properly, add Stripe and Slack API Key and a Stripe Webhook secret to your workspace's environment variables in the sidebar.
load_dotenv()
# stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# hook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
# stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# hook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
slack_token = os.environ.get("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token) 

try:
    # Stripe event
    payload, query, headers = ah.get_request()
    # sig_header = headers.get("Stripe-Signature")
    # event = stripe.Webhook.construct_event(payload, sig_header, hook_secret)
    # print(sig_header)
    # if event["type"] != "payment_intent.succeeded":
    #     raise Exception("Unhandled event type {}".format(event["type"]))
    # ah.send_response(f"[{req_sig}] Processing")
    # sig_header = headers.get("Stripe-Signature")
    # event = stripe.Webhook.construct_event(payload, sig_header, hook_secret)
    # print(sig_header)
    # if event["type"] != "payment_intent.succeeded":
    #     raise Exception("Unhandled event type {}".format(event["type"]))
    # ah.send_response(f"[{req_sig}] Processing")

    # event_obj = event["data"]["object"]
    # amount_str = f"{event_obj['currency']} {event_obj['amount'] / 100}"
    # event_obj = event["data"]["object"]
    # amount_str = f"{event_obj['currency']} {event_obj['amount'] / 100}"


    ah.send_response(f"[{payload}] deu bom")
    # # Get stripe customer email
    # customer_email = stripe.Customer.retrieve(event_obj["customer"])["email"]
    client.chat_postMessage(
        channel="sa_planos",
        text="Hello sab from your app!"
    )
    ah.send_response(f"[{payload}] deu bom")
    # Send a message in slack when the event fires
except Exception as e:
    ah.send_response(f"[{payload}] Error", status_code=500)
