from abstra.forms import Page
import abstra.workflows as aw
from abtra.tables import insert

"""
Here we are going to ask the team member about the outcome of the meeting
"""
result = (
    Page()
    .read_dropdown(
        "Meeting result",
        [
            {"label": "Successful", "value": "success"},
            {"label": "Failure", "value": "fail"},
        ],
        key="outcome_dropdown",
    )
    .run("Finish")
)


if result["outcome_dropdown"] == "success":
    new_stage = aw.next_stage(
        [
            {
                "assignee": stage["email"],
                "stage": "satisfaction_survey",
            }
        ]
    )

else:
    new_stage = aw.next_stage(
        [
            {
                "assignee": stage["email"],
                "stage": "churn_reasons",
            }
        ]
    )
