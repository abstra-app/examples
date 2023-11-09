from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime

'''
This is the first stage of the workflow where we get the client data
'''


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date

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
    .run("Send")
)

# Assigning the values to variables
(
    date
) = meeting.values()
date = preprocessing_date(date)
display(
    "Scheduled a meeting with " + name + " on " + date + ".",
    button_text="Go catch the client :)",
)

# Passing the variables to the next stage
aw.next_stage(
    [
        {
            "assignee": "example@example.com",
            "data": {
                "name" : name,
                "email": email,
                "country": country,
                "date": date,
            },
            "stage": "Client Accept"
        }
    ]
)

