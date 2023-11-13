from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime

"""
Abstra forms are the simplest way to build user interfaces for your workflows.
"""

def render(partial):
    if partial.get("ans") != None and partial.get("ans") == "No":
        return  (
            Page()
                .read_date("When would you like to schedule the meeting?", key="new_date")
                .read_time("What time would you like to schedule the meeting?", key="new_time")
        )


stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]
date_month = stage["date_month"]
date_day = stage["date_day"]
time_hour = stage["time_hour"]
time_minute = stage["time_minute"]
print(name)
client_confirmation = (
    Page()
    .display("Can we schedule a meeting with you on " + time_hour + ":" + time_minute + " on " + date_day + "/"+ date_month + "?")
    .read_multiple_choice("Is this alright?", ["Yes", "No"], key="ans")
    .reactive(render)
    .run()
)
ans = client_confirmation["ans"]
print(ans)

if ans == "No":
    date_day = str(client_confirmation["new_date"].day)
    date_month = str(client_confirmation["new_date"].month)
    time_hour = str(client_confirmation["new_time"].hour)
    time_minute = str(client_confirmation["new_time"].minute)
    aw.next_stage(
        [
            {
                "assignee": "example@example.com",
                "data": {
                    "date_month": date_month,
                    "date_day": date_day,
                    "time_hour": time_hour,
                    "time_minute": time_minute,
                },
                "stage": "Meeting Arrangement"
            }
        ]
    )
