from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime

'''
This is the first stage of the workflow where we get the client data
'''


stage = aw.get_stage()
email = stage["email"]
name = stage["name"]
country = stage["country"]

# Doing the form for the client
meeting = (
    Page()
    .display("A new client is interested in our services. Please fill the form below to schedule a meeting.")
    .display("His name is " + name + " and his email is " + email + ". He is from " + country + ".")
    .read_date("When would you like to schedule the meeting?", key="date")
    .read_time("What time would you like to schedule the meeting?", key="time")
    .run("Send")
)

# Assigning the values to variables
(
    date,
    time
) = meeting.values()
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
                "name" : name,
                "email": email,
                "country": country,
                "date_month": str(date.month),
                "date_day": str(date.day),
                "time_hour": str(time.hour),
                "time_minute": str(time.minute),
            },
            "stage": "Client Accept"
        }
    ]
)
print("Hello")
