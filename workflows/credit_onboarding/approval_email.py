from abstra.workflows import *
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from dotenv import load_dotenv

load_dotenv()
sendgrid_token = os.environ.get("SENDGRID_API_KEY")
sender_email = os.environ.get('SENDER_EMAIL')

name = get_data("name")
fname = name.split(" ")[0]
email = get_data("email")
income = get_data("income")
employer = get_data("employer")
loan_amount = get_data("loan_amount")
installments = get_data("installments")
score = get_data("score")
result = get_data("result")

html = f"""
<html>
<head>
    <style>
        .header-text {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            text-align: left;
        }}

        .paragraph-text {{
            font-size: 12px;
            color: #555;
            text-align: left;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div style="text-align: left; margin: 20px 0;">
        <img src="https://abstracloud-webflow-assets.s3.amazonaws.com/3750logo.png" width=200px>
    </div>
    <div class="header-text">
    {fname}, good news 🤑
    </div>
    <div class="paragraph-text">
        Your loan of $ {loan_amount:,.2f} has been approved! 💸💸
       
        We will contact you soon to finalize the process.
    </div>
</body>
</html>
"""

message = Mail(
        from_email=From(sender_email, "Scranton Credit [Abstra Example]"),
        to_emails=email, 
        subject=f"Loan approved, {fname}",
        html_content=html)

sg = SendGridAPIClient(sendgrid_token)
response = sg.send(message)

print(response.status_code)