from abstra.forms import *
import abstra.workflows as aw

"""
This is the first stage of the workflow where we get the client data
<<<<<<< HEAD:Abstra-Templates/Customer-Onboarding/client_registration.py
"""
=======
'''

>>>>>>> 164968c77c5b510c836944e991e8596e7e4e990e:Abstra-Templates/Meeting-Schedule/client_registration.py
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
<<<<<<< HEAD:Abstra-Templates/Customer-Onboarding/client_registration.py
=======

print("Hello")
>>>>>>> 164968c77c5b510c836944e991e8596e7e4e990e:Abstra-Templates/Meeting-Schedule/client_registration.py
