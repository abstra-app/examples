from abstra.forms import *
import os
import base64
from docxtpl import DocxTemplate
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
)

page = (
    Page()
    .display_markdown(
        """
## Hey there, glad to see you're interested in our product! Let me help you get started."""
    )
    .read("What is your name?")
    .read_multiple_choice(
        "What type of business are you?",
        ["Sales-led", "Product-led"],
    )
    .read_dropdown(
        "What's the size of your client base?",
        ["Up to 100", "100-500", "500-2000", "2000+"],
    )
    .run()
)

name, business, size = [str(x) for x in page.values()]
onb_filename = f"/tmp/Onboarding_rendered_{name}.docx"

context = {
    "name": name,
    "business": business.lower(),
    "size": size,
}

display(
    f"Great {name}, we will send you a doc with info tailored for {business.lower()} businesses with {size.lower()} customers. \
        \n\nWe just need your email."
)
auth = get_user()
email = auth.email

doc = DocxTemplate("files/onboarding_template.docx")
doc.render(context)
doc.save(onb_filename)

message = Mail(
    from_email=os.environ.get("SENDGRID_SENDER_EMAIL"),
    to_emails=email,
    subject="Example | Your doc has arrived",
    html_content=f"""
        <strong>Hi there, {name}! <br><br></strong>
        
        Here is your customized doc:
        """,
)

with open(onb_filename, "rb") as f:
    data = f.read()
    f.close()
encoded_file = base64.b64encode(data).decode()

attachedFile = Attachment(
    FileContent(encoded_file),
    FileName(onb_filename),
    FileType("application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    Disposition("attachment"),
)
message.attachment = attachedFile

sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
response = sg.send(message)

display("Your email is on it's way!")
