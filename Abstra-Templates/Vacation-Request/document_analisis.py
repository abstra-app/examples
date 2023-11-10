from abstra.forms import *
from abstra.workflows import *

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""

stage = get_stage()
doc = stage["doc"]

display("Analyse the submitted documents:")

display_file(doc, download_text="Download")

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
                    "doc": doc,
                    "correction": analisis.get("correction"),
                },
                "stage": "document-rejection",
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