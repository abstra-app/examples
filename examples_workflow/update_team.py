from abstra.forms import *
import abstra.workflows as aw
from datetime import datetime
import pycountry
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
countries = [c.name for c in list(pycountry.countries)]
# Here we define a form to get some additional info from the team member
member_page = (
    Page()
    .display("Personal Data", size="large")
    .read("Full name", required=False, key="name")
    .read_email("Email", required=False, key="personal_email")
    .read_date("Birth date", required=False, key="birth_date")
    .read_phone("Phone Number", required=False, key="phone_number")
    .read("National ID number (RG)", required=False, key="id_number")
    .read("ID number issued by", required=False, key="id_emited_by")
    .read_cpf(
        "Individual Taxpayer Registration (CPF)", required=False, key="id_taxpayer"
    )
    .read_dropdown("Country", countries, required=False, key="country")
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
)
# Here we define a form to get bank account data from the team member
bank_info_member_page = (
    Page()
    .display("Bank Account Data", size="large")
    .display(
        "Please enter your bank account data. If you're subscribed to a company, please enter the company's bank account data."
    )
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
step_run = run_steps(
    [member_page, bank_info_member_page]
)  # doing the forms in diferent steps
member = step_run[0]
(
    name,
    personal_email,
    birth_date,
    phone_number,
    id_number,
    id_emited_by,
    id_taxpayer,
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
    legal_entity_number,
    name_company,
    state_company,
    city_company,
    company_address,
    company_number_address,
    company_complement_address,
    company_district,
    company_zip_code,
) = (
    member["name"],
    member["email"],
    member["birth_date"],
    member["phone_number"],
    member["id"],
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
id_taxpayer = id_taxpayer.replace(".", "").replace("-", "")
legal_entity_number = (
    legal_entity_number.replace(".", "").replace("-", "").replace("/", "")
)
# Insert personal data
result = update(
    "team",
    {"id": team_id},
    {
        "name": name,
        "email": personal_email,
        "birth_date": birth_date,
        "phone_number": phone_number,
        "identification_number": id_number,
        "id_emited_by": id_emited_by,
        "taxpayer_id": id_taxpayer,
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
name, id, email, id_taxpayer = name, team_id, personal_email, id_taxpayer
# name, id, email = name, 4, personal_email
aw.next_stage(
    [
        {
            "assignee": personal_email,
            "data": {
                "id": team_id,
                "name": name,
                "email": email,
                "id_taxpayer": id_taxpayer,
            },
        }
    ]
)
