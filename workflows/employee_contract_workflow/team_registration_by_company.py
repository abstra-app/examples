from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime
from abstra.tables import update


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date

# security check
user = get_user()
if not user.email.endswith("@abstra.app"):
    display("Unauthorized access. Please contact admin@abstra.app.")
    exit()

# getting the info from the previous page
stage = aw.get_stage()
team_member, team_member_id, team_email = stage["name"], stage["id"], stage["email"]

member = (
    Page()
    .display("Team Additional Data", size="large")
    .display(f"Please complete the following information about {team_member}:")
    .read_date("Start abstra at")
    .read("Position")
    .read_email("Abstra Email")
    .read_number("Salary", placeholder="R$ 0,00")
    .run()
)

start_abstra_at, position, abstra_email, salary = member.values()

start_abstra_at = preprocessing_date(start_abstra_at)

# Here we update the team member table with the info we got from the form above
result = update(
    "team",
    {
        "started_at": start_abstra_at,
        "position": position,
        "abstra_email": abstra_email,
        "salary": salary,
    },
    {"id": team_member_id},
)
