from abstra.workflows import get_data
from dotenv import load_dotenv
import os
import requests

load_dotenv()
slack_token = os.environ.get("SLACK_BOT_TOKEN")

name = get_data("name")
email = get_data("email")
income = get_data("income")
employer = get_data("employer")
loan_amount = get_data("loan_amount")
installments = get_data("installments")
score = get_data("score")
result = get_data("result")
rejection_reason = get_data("rejection_reason")
reviewing_user = get_data("reviewing_user")

res = requests.post(
        'https://slack.com/api/chat.postMessage',
    json={
        'channel': 'credit-onboarding-example',
        'text': f"""
💰🚫 New loan request denied. Information:

- *Name*: {name}, 
- *Email*: {email}, 
- *Declared income*: ${income:,.2f}, 
- *Employer*: {employer}, 
- *Loan amount*: ${loan_amount:,.2f}, 
- *Number of installments*: {installments}, 
- *Score*: {score}, 
- *Reason for rejection*: {rejection_reason}
- *Reviewer*: {reviewing_user}
"""},
    headers={
        'Authorization': 'Bearer ' + slack_token,
        'Content-type': 'application/json; charset=utf-8'
    })

print(res)