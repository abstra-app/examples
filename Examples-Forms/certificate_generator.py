import requests
import pandas as pd

from abstra.forms import *
from zipfile import ZipFile
from docxtpl import DocxTemplate

# This form tries to access files in this workspace's file system. To make this form work, add a file with this name to your workspace's file system in the sidebar.
doc = DocxTemplate("src/files/certificate.docx")

display("Welcome to our Certificate Maker!", button_text="Let's get started")

multiple = read_multiple_choice(
    "Do you want to generate a single certificate or multiple, from a spreadsheet?",
    ["Single", "Multiple"],
)

if multiple == "Single":
    course = read("What is the course name?")
    hours = read_number("How many hours does this course account for?")
    date = read_date("What date should be on the certificate?")
    name = read("What is the student's full name?")
    context = {
        "name": name,
        "hours": hours,
        "course": course,
        "date": date.strftime("%d/%m/%Y"),
    }
    doc.render(context)
    filename = "/tmp/generated_certificate.docx"
    doc.save(filename)
    f = open(filename, "rb")
    Page().display("All done! Your certificate is ready! 🧑‍🎓").display_file(f).run(
        "Finish"
    )
else:
    # This form tries to access files in this workspace's file system. To make this form work, add a file with this name to your workspace's file system in the sidebar.
    f = open("src/files/certificates_template.xlsx", "rb")
    Page().display(
        "Ok! Start by downloading and filling out this spreadsheet with the details."
    ).display_file(f).run("Send")
    excel_file = False
    while excel_file == False:
        fileResponse = read_file(
            "After you fill in the spreadsheet with a list of certificates to be generated, upload the xlsx file here."
        )
        if "xlsx" in fileResponse.url:
            excel_file = (True,)
        else:
            display("Sorry, but you must upload a .xlsx file.", button_text="Try again")
    url = fileResponse.url
    r = requests.get(url)
    excel_file_path = "/tmp/temp.xlsx"
    open(excel_file_path, "wb").write(r.content)
    excel_records = pd.read_excel(excel_file_path)
    excel_records_df = excel_records.loc[
        :, ~excel_records.columns.str.contains("^Unnamed")
    ]
    list = excel_records_df.to_dict(orient="record")
    names = []
    zipObj = ZipFile("/tmp/certificates.zip", "w")
    for item in list:
        item["date"] = item["date"].strftime("%d/%m/%Y")
        doc.render(item)
        filename = f'/tmp/{item["name"]}_certificate.docx'
        doc.save(filename)
        zipObj.write(filename)
    zipObj.close()
    f = open("certificates.zip", "rb")
    Page().display("All done! Your certificates are ready! 🧑‍🎓").display_file(f).run(
        "Finish"
    )
