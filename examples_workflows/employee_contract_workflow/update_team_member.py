from abstra.forms import *
from abstra.tables import *
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

# We use this method bellow to get a information of the stage that is running
stage = aw.get_stage()
team_id = stage["id"]
email = stage["email"]
name = stage["name"]

# We need to get the old team member info before updating the table
def get_team_info(team_id):
    sql = "SELECT salary, complement_address, position, bank_account_number, id_emited_by, taxpayer_id, address, birth_date, zip_code, bank_name, email, number_address, phone_number, abstra_email, name, bank_branch_code, started_at, district, country, identification_number FROM team WHERE id = $1;"
    params = [team_id]
    return run(sql, params)[0]

old_team_info = get_team_info(team_id)

(
    salary_old,
    complement_address_old,
    position_old,
    bank_account_number_old,
    id_emited_by_old,
    taxpayer_id_old,
    address_old,
    birth_date_old,
    zip_code_old,
    bank_name_old,
    email_old,
    number_address_old,
    phone_number_old,
    abstra_email_old,
    name_old,
    bank_branch_code_old,
    started_at_old,
    district_old,
    country_old,
    identification_number_old,
) = old_team_info.values()

# Here we define a form to get some additional info from the team member
member_page = (
    Page()
    .display("Personal Data", size="large")
    .read("Full name", required=False, key="name")
    .read_email("Email", required=False, key="email")
    .read_date("Birth date", required=False, key="birth_date")
    .read_phone("Phone Number", required=False, key="phone_number")
    .read("National ID number (RG)", required=False, key="id_number")
    .read("ID number issued by", required=False, key="id_emited_by")
    .read_cpf(
        "Individual Taxpayer Registration (CPF)", required=False, key="taxpayer_id"
    )
    .read("Country", required=False, key="country")
    .read("Address (without number)", required=False, key="address")
    .read("Address number", required=False, key="number_address")
    .read("Address Complement", required=False, key="complement_address")
    .read("District", required=False, key="district")
    .read(
        "Zip code",
        mask="00000-000",
        placeholder="00000-000",
        required=False,
        key="zip_code",
    )
    .read("Shirt size", required=False, key="shirt_size")
)
# Here we define a form to get bank account data from the team member
bank_info_member_page = (
    Page()
    .display("Bank Account Data", size="large")
    .display("Please enter your bank account data.")
    .read("Bank name", placeholder="Inter", required=False, key="bank_name")
    .read(
        "Bank account number",
        placeholder="0000000-0",
        required=False,
        key="bank_account_number",
    )
    .read(
        "Bank branch code", placeholder="0001", required=False, key="bank_branch_code"
    )
)
member = run_steps([member_page, bank_info_member_page])
(
    name,
    email,
    birth_date,
    phone_number,
    id_number,
    id_emited_by,
    taxpayer_id,
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
    member["email"],
    member["birth_date"],
    member["phone_number"],
    member["id_number"],
    member["id_emited_by"],
    member["taxpayer_id"],
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
birth_date = preprocessing_date(birth_date)
phone_number = phone_number.raw
taxpayer_id = taxpayer_id.replace(".", "").replace("-", "")
# Insert personal data

def updating_team_info(dict info):
    for key, value in info.items():
        if value == "":
            info[key] = value_old
    return info

result = update(
    "team",
    {"id": team_id},
    {
        "name": name,
        "email": email,
        "birth_date": birth_date,
        "phone_number": phone_number,
        "identification_number": id_number,
        "id_emited_by": id_emited_by,
        "taxpayer_id": taxpayer_id,
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
)
name, id, email, taxpayer_id = name, team_id, email, taxpayer_id
# name, id, email = name, 4, email
aw.next_stage(
    [
        {
            "assignee": email,
            "data": {
                "id": team_id,
                "name": name,
                "email": email,
                "taxpayer_id": taxpayer_id,
            },
            "stage": "send-contract",
        }
    ]
)
