from abstra.forms import *
from run_finance import *
import abstra.workflows as aw
from datetime import datetime


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


user = get_user()
if not user.email.endswith('@abstra.app'):
    display("Unauthorized access. Please contact admin@abstra.app.")
    exit()

stage = aw.get_stage()
team_member, team_member_id, team_email = stage["name"], stage["id"], stage["email"]

member = Page().display("Team Additional Data", size='large')\
               .display(f"Please complete the following information about {team_member}:")\
               .read_date("Start abstra at")\
               .read("Position")\
               .read_email("Abstra Email")\
               .run()

start_abstra_at, position, abstra_email = member.values()

start_abstra_at = preprocessing_date(start_abstra_at)

result = run_finance(
    'UPDATE "team" SET created_at = COALESCE($1, created_at), position = COALESCE($2, position), abstra_email = COALESCE($3, abstra_email) WHERE id = $4',
    params=[start_abstra_at, position, abstra_email, team_member_id]
)
