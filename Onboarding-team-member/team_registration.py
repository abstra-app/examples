from abstra.forms import *
from abstra.tables import run, insert
import abstra.workflows as aw
from datetime import datetime


# funtion to preprocess date format for postgres


def preprocessing_date(date):
    if date != None:
        date = datetime(date.year, date.month, date.day)
        date = date.replace(tzinfo=None)
        date = date.strftime("%Y/%m/%d, %H:%M:%S")
    return date


# Questions for the team member registration

member_page = (
    Page()
    .display("Personal Data", size="large")
    .read("Full name", key="name")
    .read_email("Email", key="personal_email")
    .read_date("Birth date", key="birth_date")
    .read_phone("Phone Number", key="phone_number")
    .read("National ID number (RG)", key="id_number")
    .read("ID number issued by", key="id_emited_by")
    .read_cpf("Individual Taxpayer Registration (CPF)", key="id_taxpayer")
    .read("Country", key="country")
    .read("Address (without number)", key="address")
    .read("Address number", key="number_address")
    .read("Address Complement", required=False, key="complement_address")
    .read("District", key="district")
    .read("Zip code", mask="00000-000", placeholder="00000-000", key="zip_code")
    .read("Shirt size", placeholder="M", key="shirt_size")
)

bank_info_member_page = (
    Page()
    .display("Bank Account Data", size="large")
    .display(
        "Please enter your bank account data. If you're subscribed to a company, please enter the company's bank account data."
    )
    .read("Bank name", placeholder="Inter", key="bank_name")
    .read("Bank account number", placeholder="0000000-0", key="bank_account_number")
    .read("Bank branch code", placeholder="0001", key="bank_branch_code")
)

step_run = run_steps(
    [member_page, bank_info_member_page]
)  # doing the forms in diferent steps

member = step_run[0]
bank_info_member = step_run[1]

# updating the member dictionary with the bank info

# assigning the answers to variables
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
) = member.values()
(bank_name, bank_account_number, bank_branch_code) = bank_info_member.values()

birth_date = preprocessing_date(birth_date)
phone_number = phone_number.raw
id_taxpayer = id_taxpayer.replace(".", "").replace("-", "")

# Insert personal data

adding_member = insert(
    "team",
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
    }
)

# result = run(
#     'INSERT INTO "team"(name, email, birth_date, phone_number,\
#   identification_number, id_emited_by, taxpayer_id, country,\
#   address, number_address, complement_address, district, zip_code, shirt_size,)\
#   VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13,\
#   $14) RETURNING id',
#     params=[name, personal_email, birth_date, phone_number, id_number,
#             id_emited_by, id_taxpayer, country,address, number_address,
#             complement_address, district, zip_code, shirt_size]
# )
# # Insert bank account data
# run('INSERT INTO "team_bank_account" (name, number, branch_code, team_id) VALUES($1, $2, $3, $4)',
#             params=[bank_name, bank_account_number,
#                     bank_branch_code, result[0]["id"]]
#             )

# name, id, email = name, result[0]["id"], personal_email

name, id, email, id_taxpayer = name, 31, personal_email, id_taxpayer

aw.next_stage(
    [
        {
            "assignee": "example@example.com",
            "data": {
                "id": id,
                "name": name,
                "email": email,
                "id_taxpayer": id_taxpayer,
            },
            "stage": "abstra-team-registration",
        }
    ]
)

# for you to test if the code is working
# print(stage.data)
# print(stage)
