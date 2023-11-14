from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime

"""
This is the first stage of the workflow where we get the client data
"""


stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]
date_day = stage["date_day"]
date_month = stage["date_month"]
time_hour = stage["time_hour"]
time_minute = stage["time_minute"]
print(date_day)

def render(partial):
    if partial.get("ans") != None and partial.get("ans") == "No":
        return  (
            Page()
                .read_date("When would you like to schedule the meeting?", key="new_date")
                .read_time("What time would you like to schedule the meeting?", key="new_time")
        )
        

if date_day != None:
    client_confirmation = (
        Page()
        .display("Can we schedule a meeting with you on " + time_hour + ":" + time_minute + " on " + date_day + "/"+ date_month + "? With " + name + " from " + country + "?")
        .read_multiple_choice("Is this alright?", ["Yes", "No"], key="ans")
        .reactive(render)
        .run()
        )
    
    if client_confirmation["ans"] == "No":(
        date,
        time
    ) = client_confirmation.values()
    else :
        aw.next_stage(
            [
                {
                    "assignee": "example@example.com",
                    "data": {
                        # "name": name,
                        # "email": email,
                        # "country": country,
                        "date_month": date_month,
                        "date_day": date_day,
                        "time_hour": time_hour,
                        "time_minute": time_minute,
                    },
                    "stage": "Client Accept",
            }
        ]
    )
else:
    client_confirmation = (
        Page()
        .read_date("When would you like to schedule the meeting?", key="new_date")
        .read_time("What time would you like to schedule the meeting?", key="new_time")
        .run()
    )     
    (
        date,
        time
    ) = client_confirmation["new_date"], client_confirmation["new_time"]    
    
# Assigning the values to variables

print(date)
print(time)
display(
    "Scheduled a meeting with " + name + " on " + str(date.day) + "/"+ str(date.month) + " at " + str(time.hour) + ":" + str(time.minute) + ".",
    button_text="Go catch the client :)"
)

# Passing the variables to the next stage
print("Hello")
aw.next_stage(
    [
        {
            "assignee": "example@example.com",
            "data": {
                # "name": name,
                # "email": email,
                # "country": country,
                "date_month": str(date.month),
                "date_day": str(date.day),
                "time_hour": str(time.hour),
                "time_minute": str(time.minute),
            },
            "stage": "Client Accept",
        }
    ]
)
