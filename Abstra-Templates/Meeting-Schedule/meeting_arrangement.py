import smtplib
from email.mime.text import MIMEText
import abstra.workflows as aw

# stage = aw.get_stage()
# email = stage["email"]
# name = stage["name"]
# country = stage["country"]


# Generic email sending code
# subject = "Email Subject"
# body = "This is the body of the text message"
# sender = "sender@gmail.com"
# recipients = ["receiver@gmail.com"]
# password = ""


# def send_email(subject, body, sender, recipients, password):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = sender
#     msg['To'] = ', '.join(recipients)
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
#        smtp_server.login(sender, password)
#        smtp_server.sendmail(sender, recipients, msg.as_string())
#     print("Message sent!")


# send_email(subject, body, sender, recipients, password)

# aw.next_stage(
#         [
#             {
#                 "assignee": "example@example.com",
#                 "data": {
#                     "name" : name,
#                     "email": email,
#                     "country": country,
#                 },
#                 "stage": "Meeting Schedule"
#             }
#         ]
#     )
