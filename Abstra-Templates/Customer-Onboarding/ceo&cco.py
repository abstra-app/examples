"""
Here we are going to send a email to the team member, aiming to arrange a meeting
"""
import smtplib
import abstra.workflows as aw

# Getting the client email from the previous stage
stage = aw.get_stage()
custumer_email = stage.data.get("email")
custumer_name = stage.data.get("name")
churn_reason = stage.data.get("churn_reason")


# Sending the CCO and CEO notification email
gmail_user = "bot@gmail.com"
gmail_password = "bot_password"

sent_from = gmail_user
to = ["CEO@gmail.com", "CCO@gmail.com"]
subject = "New client"
body = ""

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
