from abstra.forms import *
from abstra.tables import *

"""
In this form we are going to register a new client
"""
client = (
    Page()
    .read("Name")
    .read_email("Email")
    .read_dropdown(
        "Legal entity",
        [
            {"label": "Physical", "value": "physical"},
            {"label": "Juridical", "value": "juridical"},
        ],
    )
    .read("Country")
    .run("Send")
)

(
    name,
    email,
    legal_entity,
    country,
) = client.values()


insert(
    "client_database",
    {
        "name": name,
        "email": email,
        "legal_entity": legal_entity,
        "country": country,
    },
)

display(
    "Registration Successful.",
    button_text="See you next time",
)

# Now we are going to redirect to a new stage of the workflow for the client
new_stage = aw.next_stage(
    [
        {
            "assignee": stage["email"],
            "stage": "welcome_message",
        }
    ]
)
# and there is also a new stage for the team member
new_stage_member = aw.next_stage(
    [
        {
            "assignee": "foo@company.co",
            "stage": "meeting_arrangement",
        }
    ]
)
