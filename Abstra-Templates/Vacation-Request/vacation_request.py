from abstra.forms import *
from abstra.workflows import *

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""


def render(partial):
    if partial.get("reason") and partial.get("reason") == "other":
        return Page().read("Please specify:",required=True ,key="other")


motivation = (
    Page()
    .read("Employee's Name:", key="name")
    .read_email("Employee's Email:", key="email")
    .read_number("Time-Off Request (Days):", key="days")
    .read_date("Beginning on:", key="start")
    .read_date("Ending on:", key="end")
    .read_dropdown(
        "Reason for Request:",
        [
            {"label": "Vacation", "value": "vacation"},
            {"label": "To Vote", "value": "vote"},
            {"label": "Personal Leave", "value": "personal"},
            {"label": "Funeral/Bereavement", "value": "funeral"},
            {"label": "Jury Duty", "value": "jury"},
            {"label": "Family Reasons", "value": "family"},
            {"label": "Medical Leave", "value": "medical"},
            {"label": "Other", "value": "other"},
        ],
        key="reason",
    )
    .reactive(render)
    .read("Your Manager's name", key="manname")
    .run()
)


next_stage(
    [
        {
            "assignee": "Team@member.com",
            "data": {
                "name": motivation.get("name"),
                "email": motivation.get("email"),
                "days": motivation.get("days"),
                "start": motivation.get("start"),
                "end": motivation.get("end"),
                "reason": motivation.get("reason"),
                "other": motivation.get("other"),
                "manname": motivation.get("manname"),
            },
            "stage": "vacation-approval",
        }
    ]
)
