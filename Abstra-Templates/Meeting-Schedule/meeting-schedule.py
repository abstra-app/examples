from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime

"""
This is the first stage of the workflow where we get the client data
"""


<<<<<<< HEAD:Abstra-Templates/Customer-Onboarding/Meeting_Schedule.py
def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


=======
>>>>>>> 164968c77c5b510c836944e991e8596e7e4e990e:Abstra-Templates/Meeting-Schedule/meeting-schedule.py
stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]

# Doing the form for the client
meeting = (
    Page()
    .display(
        "A new client is interested in our services. Please fill the form below to schedule a meeting."
    )
    .display(
        "His name is "
        + name
        + " and his email is "
        + email
        + ". He is from "
        + country
        + "."
    )
    .read_date("When would you like to schedule the meeting?", key="date")
    .read_time("What time would you like to schedule the meeting?", key="time")
    .run("Send")
)

# Assigning the values to variables
<<<<<<< HEAD:Abstra-Templates/Customer-Onboarding/Meeting_Schedule.py
(date) = meeting.values()
date = preprocessing_date(date)
=======
(
    date,
    time
) = meeting.values()
print(date)
print(time)
>>>>>>> 164968c77c5b510c836944e991e8596e7e4e990e:Abstra-Templates/Meeting-Schedule/meeting-schedule.py
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
                "name": name,
                "email": email,
                "country": country,
                "date_month": str(date.month),
                "date_day": str(date.day),
                "time_hour": str(time.hour),
                "time_minute": str(time.minute),
            },
            "stage": "Client Accept",
        }
    ]
)
<<<<<<< HEAD:Abstra-Templates/Customer-Onboarding/Meeting_Schedule.py
=======
print("Hello")
>>>>>>> 164968c77c5b510c836944e991e8596e7e4e990e:Abstra-Templates/Meeting-Schedule/meeting-schedule.py
