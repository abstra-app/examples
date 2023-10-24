from abstra.forms import *
from abstra.tables import *
import abstra.workflows as aw
from datetime import datetime
from abstra.tables import update


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


def unpreprocessing_date(date):
    date = date[0:10]
    date = date.replace("/", "-")
    return date


# We use this method bellow to get a information of the stage that is running
stage = aw.get_stage()
team_id = stage["id"]
email = stage["email"]
name = stage["name"]


# We need to get the old team member info before updating the table
def get_team_info(team_id):
    sql = """SELECT name, birth_date, taxpayer_id, email,\
          identification_number, id_emited_by,\
          country, address, number_address, complement_address,\
          district, zip_code, shirt_size, bank_name, bank_account_number,\
          bank_branch_code FROM team WHERE id = $1;"""
    params = [team_id]
    return run(sql, params)[0]


old_team_info = get_team_info(team_id)
# Define a form to get some additional info from the team member
member_page = (
    Page()
    .display("Personal Data", size="large")
    .read("Full name", required=False, key="name", initial_value=old_team_info["name"])
    .read_date(
        "Birth date",
        required=False,
        key="birth_date",
        initial_value=unpreprocessing_date(old_team_info["birth_date"]),
    )
    .read_cpf("Individual Taxpayer Registration (CPF)", key="taxpayer_id", initial_value=old_team_info["taxpayer_id"][0:3]+"."+old_team_info["taxpayer_id"][3:6]+"."+old_team_info["taxpayer_id"][6:9]+"-"+old_team_info["taxpayer_id"][9:11])
    .read_email(
        "Email", required=False, key="email", initial_value=old_team_info["email"]
    )
    .read(
        "National ID number (RG)",
        required=False,
        key="identification_number",
        initial_value=old_team_info["identification_number"],
    )
    .read(
        "ID number issued by",
        required=False,
        key="id_emited_by",
        initial_value=old_team_info["id_emited_by"],
    )
    .read(
        "Country", required=False, key="country", initial_value=old_team_info["country"]
    )
    .read(
        "Address (without number)",
        required=False,
        key="address",
        initial_value=old_team_info["address"],
    )
    .read(
        "Address number",
        required=False,
        key="number_address",
        initial_value=old_team_info["number_address"],
    )
    .read(
        "Address Complement",
        required=False,
        key="complement_address",
        initial_value=old_team_info["complement_address"],
    )
    .read(
        "District",
        required=False,
        key="district",
        initial_value=old_team_info["district"],
    )
    .read(
        "Zip code",
        mask="00000-000",
        placeholder="00000-000",
        required=False,
        key="zip_code",
        initial_value=old_team_info["zip_code"],
    )
    .read(
        "Shirt size",
        required=False,
        key="shirt_size",
        initial_value=old_team_info["shirt_size"],
    )
)
# Here we define a form to get bank account data from the team member
bank_info_member_page = (
    Page()
    .display("Bank Account Data", size="large")
    .display("Please enter your bank account data.")
    .read(
        "Bank name",
        placeholder="Inter",
        required=False,
        key="bank_name",
        initial_value=old_team_info["bank_name"],
    )
    .read(
        "Bank account number",
        placeholder="0000000-0",
        required=False,
        key="bank_account_number",
        initial_value=old_team_info["bank_account_number"],
    )
    .read(
        "Bank branch code",
        placeholder="0001",
        required=False,
        key="bank_branch_code",
        initial_value=old_team_info["bank_branch_code"],
    )
)
member = run_steps([member_page, bank_info_member_page])
(
    name,
    birth_date,
    taxpayer_id,
    email,
    identification_number,
    id_emited_by,
    country,
    address,
    number_address,
    complement_address,
    district,
    zip_code,
    shirt_size,
    bank_name,
    bank_account_number,
    bank_branch_code,
) = (
    member["name"],
    member["birth_date"],
    member["taxpayer_id"],
    member["email"],
    member["identification_number"],
    member["id_emited_by"],
    member["country"],
    member["address"],
    member["number_address"],
    member["complement_address"],
    member["district"],
    member["zip_code"],
    member["shirt_size"],
    member["bank_name"],
    member["bank_account_number"],
    member["bank_branch_code"],
)
# Insert personal data
result = update(
    "team",
    {
        "name": name,
        "email": email,
        "identification_number": identification_number,
        "id_emited_by": id_emited_by,
        "country": country,
        "address": address,
        "number_address": number_address,
        "complement_address": complement_address,
        "district": district,
        "zip_code": zip_code,
        "shirt_size": shirt_size,
        "bank_name": bank_name,
        "bank_account_number": bank_account_number,
        "bank_branch_code": bank_branch_code,
    },
    {"id": team_id},
)
name, id, email = name, team_id, email
aw.next_stage(
    [
        {
            "assignee": email,
            "data": {
                "id": team_id,
                "name": name,
                "email": email,
            },
            "stage": "send-contract",
        }
    ]
)
