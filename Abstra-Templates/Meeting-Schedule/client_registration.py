from abstra.forms import *
import abstra.workflows as aw

"""
This is the first stage of the workflow where we get the client data
"""
stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]

# Doing the form for the client
client = (
    Page()
    .read("Name", key="name")
    .read_email("Email", key="email")
    .read_dropdown(
        "Entity",
        [
            {"label": "Bussiness", "value": "bussiness"},
            {"label": "Personal", "value": "personal"},
        ],
        key="entity",
    )
    .read("Country", key="country")
    .run("Send")
)

# Assigning the values to variables
(
    name,
    email,
    entity,
    country,
) = client.values()

display(
    "Registration Successful.",
    button_text="See you next time",
)

# Passing the variables to the next stage
aw.next_stage(
    [
        {
            "assignee": "example@example.com",
            "data": {
                "name": name,
                "email": email,
                "country": country,
            },
            "stage": "Meeting Arrangement",
        }
    ]
)
