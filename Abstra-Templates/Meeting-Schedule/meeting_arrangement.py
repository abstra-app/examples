import abstra.workflows as aw
from abstra.forms import *

"""
Here we are going to send a email to the team member, aiming to arrange a meeting
"""
import smtplib

gmail_user = "bot@gmail.com"
gmail_password = "bot_password"

sent_from = gmail_user
to = ["person_a@gmail.com", "person_b@gmail.com"]  # Responsible team members emails
subject = "Meeting arrangement"
body = "Hi, there is a new client to be attended."

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (
    sent_from,
    ", ".join(to),
    subject,
    body,
)

try:
    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.ehlo()
    smtp_server.login(gmail_user, gmail_password)
    smtp_server.sendmail(sent_from, to, email_text)
    smtp_server.close()
    print("Email sent successfully!")
except Exception as ex:
    print("Something went wrong….", ex)

# Passing the variables to the next stage

stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]

aw.next_stage(
    [
        {
            "assignee": "example@example.com",
            "data": {
                "name" : name,
                "email": email,
                "country": country,
            },
            "stage": "Meeting Schedule"
        }
    ]
)
