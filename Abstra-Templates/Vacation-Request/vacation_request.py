from abstra.forms import *
from abstra.workflows import *

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""

def render(partial):
    if partial.get("reason") and partial.get("reason") == "other":
        return Page().read("Please specify:")


motivation = (
    Page()
    .read("Employee's Name:")
    .read_number("Time-Off Request (Days):")
    .read_date("Beginning on:")
    .read_date("Ending on:")
    .read_dropdown("Reason for Request:",
                    [
                        {"label":"Vacation","value":"vacation"},
                        {"label":"To Vote","value":"vote"},
                        {"label":"Personal Leave","value":"personal"},
                        {"label":"Funeral/Bereavement","value":"funeral"},
                        {"label":"Jury Duty","value":"jury"},
                        {"label":"Family Reasons","value":"family"},
                        {"label":"Medical Leave","value":"medical"},
                        {"label":"Other","value":"other"},
                    ],
                    key="reason" 
                )
    .reactive(render)
    .run()
)