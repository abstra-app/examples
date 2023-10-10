import zipfile
import pandas as pd

from abstra.forms import *
from docxtpl import DocxTemplate


Page().display(
    "Hey there! Download the spreadsheet below and fill it with your customers' info."
).display_file("src/files/customer_data_template.xlsx").run()

uploaded_file = read_file("Upload the completed spreadsheet below:")
file_content = uploaded_file.content

df = pd.read_excel(file_content)

selection = read_pandas_row_selection(
    df,
    hint="Select which customers you'd like to generate an invoice to.",
    multiple=True,
)

doc = DocxTemplate("src/files/invoice_template.docx")

list = []
print(selection)
for item in selection:
    name = item["Name"]
    print(item["Date"])
    item["Date"] = pd.to_datetime(item["Date"]).strftime("%Y-%m-%d")
    doc.render(item)
    file_name = f"/tmp/Template_rendered_{name}.docx"
    doc.save(file_name)
    list.append(file_name)

invoice_zip_path = "/tmp/invoices.zip"

with zipfile.ZipFile("/tmp/invoices.zip", "w") as zipF:
    for invoice in list:
        zipF.write(invoice, compress_type=zipfile.ZIP_DEFLATED)

Page().display(f"Your invoices are ready! Download them below:").display_file(
    invoice_zip_path
).run()

display("See you next time!")
