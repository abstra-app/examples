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

path = f"./REQUIRED_DOCUMENTS/{name}Document"

with open(path, "wb") as file:
        file.write(docs.get("doc").file.read())
   
next_stage(
    [
        {
            "data": {
            "path": path    
            },
            "stage": "document-analisis",
        }
    ]
)
