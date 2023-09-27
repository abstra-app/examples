from abstra.forms import *
import pandas as pd
from docxtpl import DocxTemplate
import os
import base64
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

Page().display(
    "Hey there! Download the spreadsheet below and fill it with your customers' info."
).display_file("src/files/customer_data_template.xlsx").run()

file = read_file("Upload the completed spreadsheet here:")

doc = DocxTemplate("src/files/invoice_template.docx")
df = pd.read_excel(file.file)
selection = read_pandas_row_selection(
    df, hint="Select which customers you'd like to generate an invoice to.", multiple=True
)

for item in selection:
    name = item["Name"]
    email = item["Email"]
    filename = f"/tmp/Template_rendered_{name}.docx"
    item["Date"] = pd.to_datetime(item["Date"]).strftime("%Y-%m-%d")
    doc.render(item)
    doc.save(filename)

    message = Mail(
        from_email=os.environ.get("SENDGRID_SENDER_EMAIL"),
        to_emails=email,  # replace this with 'item['Email']' to send to the spreadsheet emails
        subject="This month's invoice",
        html_content=f"Hello {name},<br<br> \
        Here's your invoice for this month. More information regarding payment can be found in the attachment.<br><br> \
        Hope you have a great week!",
    )

    with open(filename, "rb") as f:
        data = f.read()
        f.close()
        
    encoded_file = base64.b64encode(data).decode()
    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(filename),
        FileType(
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ),
        Disposition("attachment"),
    )
    message.attachment = attachedFile

    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)

display("All your emails have been sent - check your inbox! See you next time.")
