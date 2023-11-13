from abstra.forms import *
from abstra.workflows import *

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""
stage = get_stage()
name = stage["name"]

display(
    "Upload the required documents:",
)

docs = (
    Page()
    .read_file("Please upload your documents:", key="doc")
    .run()
)

NewPath = f"./REQUIRED_DOCUMENTS/Updated{name}Document"

with open(NewPath, "wb") as file:
        file.write(docs.get("doc").file.read())

next_stage(
    [
        {
            "data": {
                "newpath": NewPath,
            },
            "stage": "document-analisis",
        }
    ]
)
