from abstra.forms import *
from abstra.workflows import *

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""
display(
    "Upload the required documents:",
)

docs = (
    Page()
    .read_file("Please upload your documents:", key="doc")
    .run()
)

next_stage(
    [
        {
            "data": {
                "doc": docs.get("doc"),
            },
            "stage": "document-analisis",
        }
    ]
)
