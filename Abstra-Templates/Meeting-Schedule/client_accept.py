from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""

def render(partial):
    if partial.get("ans") != None and partial.get("ans") == "Yes":
        return  (
            Page()
                .read_date("When would you like to schedule the meeting?", key="new_date")
                .read_time("What time would you like to schedule the meeting?", key="new_time")
        )


stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]
date = stage["date"]
time = stage["time"]

client_confirmation = (
    Page()
    .display("Can we schedule a meeting with you on " + str(time.hour) + ":" + str(time.minute) + " on " + str(date.day) + "/"+ str(date.month) + "?")
    .read_multiple_choice("Yes or No?", ["Yes", "No"], key="ans")
    .reactive(render)
    .run()
)
ans = client_confirmation["ans"]
print(ans)
if ans == "Yes":
    aw.next_stage(
        [
            {
                "assignee": "example@example.com",
                "data": {
                    "name" : name,
                    "email": email,
                    "country": country,
                    "date": date,
                    "time": time,
                },
                "stage": "Slack notification"
            }
        ]
    )
else:
    date = client_confirmation["new_date"]
    time = client_confirmation["new_time"]
    aw.next_stage(
        [
            {
                "assignee": "example@example.com",
                "data": {
                    "name" : name,
                    "email": email,
                    "country": country,
                    "date": date,
                    "time": time,
                },
                "stage": "Meeting Arrangement"
            }
        ]
    )
