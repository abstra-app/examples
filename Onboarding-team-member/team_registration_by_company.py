from abstra.forms import *
from run_finance import *
import abstra.workflows as aw
from datetime import datetime
from abstra.tables import update

# Here we define a function to preprocess the data we want to insert into the database, if you are working with dates, you can use this function to convert the date to the format you want to insert into the database.


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


user = get_user()
if not user.email.endswith("@abstra.app"):
    display("Unauthorized access. Please contact admin@abstra.app.")
    exit()

# We use this method bellow to get a information of the stage that is running
stage = aw.get_stage()
team_member, team_member_id, team_email = stage["name"], stage["id"], stage["email"]

# Here we define a form to get some additional info from the team member
member = (
    Page()
    .display("Team Additional Data", size="large")
    .display(f"Please complete the following information about {team_member}:")
    .read_date("Start abstra at")
    .read("Position")
    .read_email("Abstra Email")
    .run()
)

start_abstra_at, position, abstra_email = member.values()

start_abstra_at = preprocessing_date(start_abstra_at)

# Here we update the team member table with the info we got from the form above
result = run_finance(
    update(
        "team",
        {
            "created_at": start_abstra_at,
            "position": position,
            "abstra_email": abstra_email,
        },
        {"id": team_member_id},
    )
)
