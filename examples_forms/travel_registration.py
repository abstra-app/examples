from abstra.forms import *
from datetime import datetime
from abstra.tables import run, insert

# Here you can add your company's authentication.
# user = get_user()
# if not user.email.endswith('@mycompany.com'):
# exit()


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


def get_travel():
    travel = (
        Page()
        .display(
            "Hello! To register a new travel, please add the information required in the fields below:"
        )
        .read("Travel purpose", key="purpose")
        .read_date("Date of travel", key="date")
        .read("Country of travel", key="country")
        .read("City of travel", key="city")
        .run("Send")
    )
    return travel


travel = get_travel()

insert(
    "travel",
    {
        "purpose": travel["purpose"],
        "date": preprocessing_date(travel["date"]),
        "country": travel["country"],
        "city": travel["city"],
    },
)

display("All good! Your travel has been registered.")
