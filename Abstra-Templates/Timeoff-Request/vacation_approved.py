"""
Here we are going to send a Welcome email to the new customer
"""
import abstra.workflows as aw
import smtplib

# Here we get the client email from the previous stage
stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
documents = stage["documents"]
correction = stage["correction"]

# Now we send the email
gmail_user = "bot@gmail.com"
gmail_password = "bot_password"

sent_from = gmail_user
to = email # Client email
subject = "Vacation Approved"
body = f"Hi {name}, enjoy your vacation!"

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