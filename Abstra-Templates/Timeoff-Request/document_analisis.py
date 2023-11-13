from abstra.forms import *
from abstra.workflows import *

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""
# Getting info from other stages
stage = get_stage()
path = stage["path"]
NewPath = stage["newpath"]

# Now we are going to display the updated document if it exists
display("Analyse the submitted documents:")

if NewPath == None:
    display_file(path, download_text="Download")
else:
    display_file(NewPath, download_text="Download")


def render(partial):
    if partial.get("analisis") and partial.get("analisis") == "no":
        return Page().read("What must be corrected ?", key="correction")
    
analisis = (
    Page()
    .read_dropdown(
        "Do you approve the documents?",
        [
            {"label": "Yes", "value": "yes"},
            {"label": "No", "value": "no"},
        ],
        key="analisis",
    )
    .reactive(render)
    .run()
)

if analisis.get("analisis") == "no":
    next_stage(
        [
            {
                "data": {
                    "analisis": analisis.get("analisis"),
                    "correction": analisis.get("correction"),
                },
                "stage": "Document Rejection",
            }
        ]
    )
else:
    next_stage(
        [
            {
                "data": {
                    "analisis": analisis.get("analisis"),
                },
                "stage": "Vacation Approved",
            }
        ]
    )